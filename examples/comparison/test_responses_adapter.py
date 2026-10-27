"""Model adapter spending/isolation checks with mock callbacks; no network."""
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from offline_runner import BoundaryError, fingerprint
from responses_adapter import BudgetedResponses, SpendPolicy, baseline_content, request_body


def packet(rid="request", arm="baseline"):
    payload={"mission":{"objective":"neutral mock only"},"public_manual":{},"notes":"ordinary notes","latest":None}
    return {"arm":arm,"request_id":rid,"payload":payload,"payload_sha256":fingerprint(payload),
            "model":{"id":"gpt-6.1-sol","revision":"api-alias-20261027","reasoning":"low"}}


class ModelChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.clients=[];self.calls=[]
    def tearDown(self):
        for client in self.clients:client.db.close()
        self.tmp.cleanup()
    def post(self,path,body):
        self.calls.append((path,body))
        if path=="/responses/input_tokens":return {"object":"response.input_tokens","input_tokens":100}
        return {"id":"mock-response","model":"gpt-6.1-sol","service_tier":"default","status":"completed",
                "usage":{"input_tokens":100,"output_tokens":50},
                "output":[{"type":"message","content":[{"type":"output_text","text":"{}"}]}]}
    def client(self,policy=SpendPolicy(approved_by_user=True),post=None):
        c=BudgetedResponses(Path(self.tmp.name)/"budget.sqlite",policy,post=post or self.post);self.clients.append(c);return c
    def test_default_rejects_before_any_callback(self):
        c=self.client(SpendPolicy())
        with self.assertRaises(BoundaryError):c.complete(packet())
        self.assertEqual(self.calls,[])
    def test_fixed_request_has_no_conversation_tools_or_previous_id(self):
        body=request_body(packet(),SpendPolicy())
        self.assertEqual(set(body),{"model","input","reasoning","max_output_tokens","store","stream","service_tier"})
        self.assertIs(body["store"],False)
        self.assertEqual(body["reasoning"],{"effort":"low"})
        self.assertEqual(body["service_tier"],"default")
    def test_both_initial_arms_can_count_before_either_generation(self):
        c=self.client();a=packet("a");b=packet("b")
        c.prepare(a);c.prepare(b)
        self.assertEqual([x[0] for x in self.calls],["/responses/input_tokens"]*2)
        c.complete(a);c.complete(b)
        self.assertEqual([x[0] for x in self.calls],["/responses/input_tokens"]*2+["/responses"]*2)
    def test_success_replays_retained_response_without_network(self):
        c=self.client();p=packet();first=c.complete(p)
        self.assertEqual(c.complete(p),first)
        self.assertEqual([x[0] for x in self.calls],["/responses/input_tokens","/responses"])
    def test_full_reservation_commits_before_callbacks(self):
        observed=[]
        def post(path,body):
            observed.append(c.db.execute("SELECT state,reserve_nusd FROM requests").fetchone())
            return self.post(path,body)
        c=self.client(post=post);c.complete(packet())
        self.assertTrue(all(state in ("reserved","generating") and cost==c.policy.reservation for state,cost in observed))
    def test_spend_limit_blocks_before_count_or_generation(self):
        p=SpendPolicy(approved_by_user=True,max_total_nusd=SpendPolicy().reservation)
        c=self.client(p);c.complete(packet("first"));before=len(self.calls)
        with self.assertRaises(BoundaryError):c.complete(packet("second"))
        self.assertEqual(len(self.calls),before)
    def test_over_input_cap_stops_before_generation(self):
        def post(path,body):self.calls.append((path,body));return {"object":"response.input_tokens","input_tokens":12289}
        c=self.client(post=post)
        with self.assertRaises(BoundaryError):c.complete(packet())
        self.assertEqual([x[0] for x in self.calls],["/responses/input_tokens"])
        self.assertEqual(c.db.execute("SELECT count(*) FROM token_counts").fetchone()[0],1)
    def test_unknown_usage_retains_result_and_blocks_entire_pair(self):
        def post(path,body):
            r=self.post(path,body)
            if path=="/responses":r.pop("usage")
            return r
        c=self.client(post=post)
        with self.assertRaises(BoundaryError):c.complete(packet())
        self.assertIsNotNone(c.db.execute("SELECT response FROM requests").fetchone()[0])
        before=len(self.calls)
        with self.assertRaises(BoundaryError):c.complete(packet("other"))
        self.assertEqual(len(self.calls),before)
    def test_timeout_does_not_automatically_retry_after_reopen(self):
        def post(path,body):self.calls.append((path,body));raise TimeoutError("mock lost receipt")
        c=self.client(post=post)
        with self.assertRaises(TimeoutError):c.complete(packet())
        reopened=self.client(post=post)
        with self.assertRaises(BoundaryError):reopened.complete(packet())
        self.assertEqual(len(self.calls),1)
    def test_changed_cut_and_model_cannot_dispatch(self):
        c=self.client();p=packet();p["payload"]["notes"]="changed"
        with self.assertRaises(BoundaryError):c.complete(p)
        p=packet();p["model"]["id"]="other-model"
        with self.assertRaises(BoundaryError):c.complete(p)
        self.assertEqual(self.calls,[])
    def test_known_token_bounds_include_actual_output(self):
        def post(path,body):
            r=self.post(path,body)
            if path=="/responses":r["usage"]["output_tokens"]=4097
            return r
        c=self.client(post=post)
        with self.assertRaises(BoundaryError):c.complete(packet())
        self.assertEqual(c.summary()["generation_slots_reserved"],1)
    def test_spending_policy_cannot_change_after_first_open(self):
        self.client()
        with self.assertRaises(BoundaryError):self.client(replace(SpendPolicy(approved_by_user=True),max_generation_calls=1))
    def test_malformed_output_is_retained_and_never_silently_repaired(self):
        def post(path,body):
            r=self.post(path,body)
            if path=="/responses":r["output"][0]["content"][0]["text"]="not-json"
            return r
        c=self.client(post=post)
        with self.assertRaises(ValueError):c.complete(packet())
        self.assertIn("not-json",c.db.execute("SELECT response FROM requests").fetchone()[0])
    def test_duplicate_and_nonfinite_model_json_block_without_dispatch_retry(self):
        for i,text in enumerate(('{"x":1,"x":2}','{"x":NaN}')):
            def post(path,body):
                r=self.post(path,body)
                if path=="/responses":r["output"][0]["content"][0]["text"]=text
                return r
            c=BudgetedResponses(Path(self.tmp.name)/(str(i)+".sqlite"),SpendPolicy(approved_by_user=True),post=post)
            self.clients.append(c)
            with self.assertRaises(BoundaryError):c.complete(packet(str(i)))
            self.assertEqual(c.db.execute("SELECT state FROM requests").fetchone()[0],"blocked")
    def test_measured_input_must_match_authenticated_count(self):
        def post(path,body):
            r=self.post(path,body)
            if path=="/responses":r["usage"]["input_tokens"]=101
            return r
        c=self.client(post=post)
        with self.assertRaises(BoundaryError):c.complete(packet())
    def test_bounded_complete_public_image_is_rendered_without_mutating_receipt(self):
        import base64
        raw=b"neutral-image-fixture";encoded=base64.b64encode(raw).decode()
        payload={"latest":{"body":{"format":"png","sha256":sha256(raw).hexdigest(),
            "asset":{"encoding":"base64","data":encoded,"offset":0,"has_more":False,"total_bytes":len(raw)}}}}
        content=baseline_content(payload)
        self.assertEqual(content[1]["type"],"input_image")
        self.assertEqual(payload["latest"]["body"]["asset"]["data"],encoded)
        self.assertNotIn(encoded,content[0]["text"])


if __name__=="__main__":unittest.main(verbosity=2)
