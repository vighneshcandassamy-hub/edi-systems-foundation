"""Run these model-boundary checks on Kaggle. No real inference is used."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from offline_runner import BoundaryError,Limits,fingerprint,wire
from local_qwen_adapter import LocalQwen,MODEL,Loopback

def packet(rid="a",limits=Limits()):
    payload={"mission":{"objective":"Neutral boundary fixture"},"public_manual":{"sources":{}},"notes":"","latest":None}
    return {"arm":"baseline","request_id":rid,"model":copy.deepcopy(MODEL),
            "limits":limits.__dict__,"payload":payload,"payload_sha256":fingerprint(payload)}

def proposal():
    return {"rationale":"Neutral fixture","uncertainty":"Not a scientific result",
            "predictions":[],"operation":{"name":"yield","args":{"reason":"Fixture only"}}}

class QwenBoundaryChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.clients=[];self.sent=[]
    def tearDown(self):
        for c in self.clients:c.db.close()
        self.temp.cleanup()
    def post(self,path,body):
        self.sent.append((path,body))
        if path=="/tokenize":return wire({"count":100,"max_model_len":16384}).encode()
        return wire({"model":MODEL["id"],"choices":[{"finish_reason":"stop",
            "message":{"content":wire(proposal())}}],
            "usage":{"prompt_tokens":100,"completion_tokens":50}}).encode()
    def client(self,post=None,limits=Limits(),name="model.sqlite3"):
        c=LocalQwen(Path(self.temp.name)/name,post=post or self.post,limits=limits)
        self.clients.append(c);return c
    def test_constructor_does_not_call_model(self):
        self.client();self.assertEqual(self.sent,[])
    def test_success_and_replay_use_one_generation(self):
        c=self.client();p=packet();first=c.complete(p)
        self.assertEqual(c.complete(p),first)
        self.assertEqual([x[0] for x in self.sent],["/tokenize","/v1/chat/completions"])
        self.assertEqual(json.loads(first)["proposal"],proposal())
    def test_two_initial_preparations_precede_generation(self):
        c=self.client();a=packet("a");b=packet("b")
        c.prepare(a);c.prepare(b)
        self.assertEqual([x[0] for x in self.sent],["/tokenize"]*2)
        c.complete(a);c.complete(b)
        self.assertEqual([x[0] for x in self.sent],["/tokenize"]*2+["/v1/chat/completions"]*2)
    def test_changed_cut_is_rejected(self):
        c=self.client();p=packet();c.prepare(p);p["payload"]["notes"]="changed"
        with self.assertRaises(BoundaryError):c.complete(p)
        self.assertEqual(len(self.sent),1)
    def test_changed_request_identity_payload_is_rejected(self):
        c=self.client();p=packet();c.prepare(p);p["payload"]["notes"]="changed"
        p["payload_sha256"]=fingerprint(p["payload"])
        with self.assertRaises(BoundaryError):c.complete(p)
        self.assertEqual(len(self.sent),1)
    def test_model_mismatch_is_rejected_before_dispatch(self):
        c=self.client();p=packet();p["model"]["revision"]="other"
        with self.assertRaises(BoundaryError):c.complete(p)
        self.assertEqual(self.sent,[])
    def test_input_overflow_stops_before_generation(self):
        def post(path,body):
            self.sent.append((path,body));return b'{"count":12289,"max_model_len":16384}'
        c=self.client(post)
        with self.assertRaises(BoundaryError):c.complete(packet())
        self.assertEqual([x[0] for x in self.sent],["/tokenize"])
    def test_invalid_tokenizer_answer_is_retained(self):
        c=self.client(lambda path,body:b'{"count":true,"max_model_len":16384}')
        with self.assertRaises(BoundaryError):c.complete(packet())
        self.assertEqual(c.db.execute("SELECT answer FROM counts").fetchone()[0],b'{"count":true,"max_model_len":16384}')
    def test_timeout_is_not_retried_after_reopen(self):
        def post(path,body):
            if path=="/tokenize":return self.post(path,body)
            self.sent.append((path,body));raise TimeoutError("Neutral lost reply")
        c=self.client(post)
        with self.assertRaises(TimeoutError):c.complete(packet())
        newer=self.client()
        with self.assertRaises(BoundaryError):newer.complete(packet())
        self.assertEqual([x[0] for x in self.sent],["/tokenize","/v1/chat/completions"])
    def test_unknown_usage_retains_original_and_blocks_pair(self):
        def post(path,body):
            raw=self.post(path,body)
            if path.endswith("completions"):
                obj=json.loads(raw);obj.pop("usage");return wire(obj).encode()
            return raw
        c=self.client(post)
        with self.assertRaises(BoundaryError):c.complete(packet())
        self.assertIsNotNone(c.db.execute("SELECT raw FROM calls").fetchone()[0])
        previous=len(self.sent)
        with self.assertRaises(BoundaryError):c.complete(packet("other"))
        self.assertEqual(len(self.sent),previous)
    def test_prompt_usage_mismatch_is_blocked(self):
        def post(path,body):
            raw=self.post(path,body)
            if path.endswith("completions"):
                obj=json.loads(raw);obj["usage"]["prompt_tokens"]=101;return wire(obj).encode()
            return raw
        c=self.client(post)
        with self.assertRaises(BoundaryError):c.complete(packet())
    def test_truncation_is_not_a_success(self):
        def post(path,body):
            raw=self.post(path,body)
            if path.endswith("completions"):
                obj=json.loads(raw);obj["choices"][0]["finish_reason"]="length";return wire(obj).encode()
            return raw
        c=self.client(post)
        with self.assertRaises(BoundaryError):c.complete(packet())
        summary=c.summary()["arms"]["baseline"]
        self.assertEqual(summary["completed"],0)
        self.assertEqual(summary["actual_completion_tokens_all_measured"],50)
        self.assertEqual(summary["unknown_usage_calls"],0)
    def test_model_cannot_claim_usage(self):
        def post(path,body):
            raw=self.post(path,body)
            if path.endswith("completions"):
                obj=json.loads(raw);v=proposal();v["usage"]={"input_tokens":0}
                obj["choices"][0]["message"]["content"]=wire(v);return wire(obj).encode()
            return raw
        c=self.client(post)
        with self.assertRaises(BoundaryError):c.complete(packet())
    def test_duplicate_model_json_is_rejected(self):
        def post(path,body):
            raw=self.post(path,body)
            if path.endswith("completions"):
                obj=json.loads(raw);obj["choices"][0]["message"]["content"]='{"rationale":"x","rationale":"y"}'
                return wire(obj).encode()
            return raw
        c=self.client(post)
        with self.assertRaises(BoundaryError):c.complete(packet())
    def test_per_arm_cap_precedes_network(self):
        limits=Limits(max_calls=1)
        c=self.client(limits=limits);c.complete(packet("first",limits));previous=len(self.sent)
        with self.assertRaises(BoundaryError):c.complete(packet("second",limits))
        self.assertEqual(len(self.sent),previous)
    def test_usage_totals_do_not_equal_reserved_tokens(self):
        c=self.client();c.complete(packet());s=c.summary()["arms"]["baseline"]
        self.assertEqual(s["actual_prompt_tokens_completed"],100)
        self.assertEqual(s["actual_completion_tokens_completed"],50)
        self.assertEqual(s["policy_tokens_reserved"],16384)
    def test_remote_or_credentialed_endpoint_is_forbidden(self):
        for endpoint in ("https://api.openai.com","http://localhost:8000",
                         "http://127.0.0.1:8000/v1","http://u:p@127.0.0.1:8000"):
            with self.assertRaises(BoundaryError):Loopback(endpoint,"x"*32)
    def test_invalid_image_binding_precedes_tokenization(self):
        c=self.client();p=packet()
        p["payload"]["latest"]={"body":{"format":"png","sha256":"wrong",
            "asset":{"encoding":"base64","offset":0,"has_more":False,"total_bytes":3,"data":"YWJj"}}}
        p["payload_sha256"]=fingerprint(p["payload"])
        with self.assertRaises(BoundaryError):c.complete(p)
        self.assertEqual(self.sent,[])
    def test_counter_port_binds_once_before_export(self):
        from edi.reason.reasoner_exchange import ReasonerExchangeGateway
        g=object.__new__(ReasonerExchangeGateway)
        g.directory=Path(self.temp.name);g.request_token_counter=None
        g.bind_request_token_counter(lambda native:100)
        self.assertEqual(g.request_token_counter({}),100)
        with self.assertRaises(Exception):g.bind_request_token_counter(lambda native:200)

if __name__=="__main__":unittest.main(verbosity=2)
