"""Neutral transport checks only: no Cedar, model inference or network calls."""
import json
from pathlib import Path
import tempfile
import unittest
from offline_runner import Baseline, BoundaryError, Channel, Limits, NativeEDI, Pair, wire

MODEL = {"id": "neutral-fixture", "revision": "fixture-v1", "reasoning": "fixed"}
MANUAL = {"read": {}, "submit": {}}


def answer(packet, name="notes_replace", args=None):
    proposal = {"rationale": "Fixture only", "uncertainty": "No scientific inference",
                "predictions": ["Recorded before the fixture outcome"],
                "operation": {"name": name, "args": args if args is not None else {"text": "notes"}}}
    return wire({**{k:packet[k] for k in ("arm", "request_id", "payload_sha256")}, "proposal": proposal}).encode()


class BoundaryChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.channels = []

    def tearDown(self):
        for c in self.channels:
            c.db.close()
        self.tmp.cleanup()

    def channel(self, name="baseline", limits=Limits()):
        c = Channel(self.root / name, name, MODEL, limits)
        self.channels.append(c)
        return c

    def baseline(self, call=None, limits=Limits()):
        return Baseline(self.channel(limits=limits), {"objective": "neutral"}, MANUAL,
                        call or (lambda op,args: {"http_status":200,"body":{"receipt":args["request_id"]},"closed":op=="submit"}))

    def test_pending_reopen_is_identical_without_extra_reservation(self):
        c = self.channel(); original = c.export({"neutral": 1})
        other = self.channel()
        self.assertEqual(other.export({"neutral": 1}), original)
        self.assertEqual(other.usage()["calls"], 1)
        with self.assertRaises(BoundaryError): other.export({"neutral": 2})

    def test_foreign_response_never_dispatches(self):
        called = []; b = self.baseline(lambda *a: called.append(a))
        own = b.export(); other = self.channel("edi").export({"neutral": "other-arm"})
        with self.assertRaises(BoundaryError): b.consume(own["request_id"], answer(other, "read", {}))
        self.assertEqual(called, [])

    def test_duplicate_public_action_is_never_replayed(self):
        called = []
        def call(op,args):
            called.append((op,args)); return {"http_status":200,"body":{"ok":True},"closed":False}
        b = self.baseline(call); packet = b.export(); raw = answer(packet, "read", {"document_id":"neutral"})
        b.consume(packet["request_id"], raw)
        with self.assertRaises(BoundaryError): b.consume(packet["request_id"], raw)
        self.assertEqual(len(called), 1)

    def test_unknown_transport_outcome_survives_reopen_and_blocks(self):
        called = []
        def lost(op,args): called.append(op); raise TimeoutError("fixture lost receipt")
        b = self.baseline(lost); packet = b.export()
        with self.assertRaises(TimeoutError): b.consume(packet["request_id"], answer(packet,"read",{}))
        recovered = Baseline(self.channel(), {"objective":"neutral"}, MANUAL, lost)
        with self.assertRaises(BoundaryError): recovered.export()
        self.assertEqual(called, ["read"])

    def test_unfinished_response_application_blocks_new_model_job(self):
        c = self.channel(); packet = c.export({"neutral":1})
        c.retain(packet["request_id"], answer(packet))
        with self.assertRaises(BoundaryError): c.export({"neutral":2})

    def test_notes_and_searchable_raw_history_are_retained(self):
        b = self.baseline(); packet = b.export(); b.consume(packet["request_id"], answer(packet,args={"text":"needle"}))
        packet = b.export(); self.assertEqual(packet["payload"]["notes"], "needle")
        b.consume(packet["request_id"], answer(packet,"history_search",{"text":"needle","offset":0,"limit":20}))
        self.assertGreater(b.state()["latest"]["total"], 0)
        record_id = b.state()["latest"]["matches"][0]["id"]
        packet = b.export(); b.consume(packet["request_id"],answer(packet,"history_read",{"id":record_id,"offset":0,"limit":100}))
        self.assertEqual(b.state()["latest"]["encoding"], "base64-utf8")

    def test_reservation_budget_includes_rejected_outputs(self):
        limits = Limits(max_reserved_tokens=16384)
        c = self.channel(limits=limits); packet = c.export({"neutral":1})
        with self.assertRaises(BoundaryError): c.retain(packet["request_id"], b"malformed")
        with self.assertRaises(BoundaryError): c.export({"neutral":2})
        self.assertEqual(c.usage()["reserved_policy_tokens"], 16384)
        self.assertIsNone(c.usage()["actual_tokens"])

    def test_no_silent_request_truncation(self):
        c = self.channel(limits=Limits(max_request_bytes=100))
        with self.assertRaises(BoundaryError): c.export({"payload":"long" * 200})
        self.assertEqual(c.usage()["calls"], 0)

    def test_rejected_response_bytes_are_preserved(self):
        c = self.channel(); packet = c.export({"neutral":1})
        with self.assertRaises(BoundaryError): c.retain(packet["request_id"], b"broken-json")
        self.assertEqual(c.db.execute("SELECT result FROM calls").fetchone()[0], b"broken-json")

    def test_configuration_cannot_change_on_reopen(self):
        self.channel()
        with self.assertRaises(BoundaryError): self.channel(limits=Limits(max_calls=1))

    def test_validation_gets_only_one_correction(self):
        b = self.baseline()
        for _ in range(2):
            packet = b.export()
            with self.assertRaises(BoundaryError): b.consume(packet["request_id"], answer(packet,"not-in-catalogue",{}))
        self.assertEqual(b.state()["terminal"], "yielded-validation")
        with self.assertRaises(BoundaryError): b.export()

    def test_credentials_and_evaluator_are_not_model_operations(self):
        called = []; b = self.baseline(lambda *a: called.append(a)); packet = b.export()
        with self.assertRaises(BoundaryError): b.consume(packet["request_id"], answer(packet,"read",{"token":"not-a-real-token"}))
        self.assertEqual(called, [])

    def test_final_submit_requires_successful_public_receipt(self):
        b = self.baseline(lambda op,args:{"http_status":400,"body":{"error":"fixture"},"closed":False})
        packet = b.export(); b.consume(packet["request_id"], answer(packet,"submit",{"report":"fixture"}))
        self.assertIsNone(b.state()["terminal"])
        packet = b.export(); b.consume(packet["request_id"], answer(packet,"yield",{"reason":"fixture stop"}))
        self.assertEqual(b.state()["terminal"], "yielded")

    def test_pair_fences_evaluation_and_preserves_failure(self):
        pair = Pair(self.root, MODEL); self.channels.extend(pair.channels.values()); called = []
        with self.assertRaises(BoundaryError): pair.evaluate(lambda:called.append(True))
        pair.mark_terminal("baseline","failed")
        with self.assertRaises(BoundaryError): pair.evaluate(lambda:called.append(True))
        pair.mark_terminal("edi","completed")
        report = pair.evaluate(lambda:{"neutral":True})
        self.assertEqual(report["terminal"]["baseline"], "failed")
        self.assertEqual(pair.evaluate(lambda:called.append(True)), report)
        with self.assertRaises(BoundaryError): pair.mark_terminal("baseline","completed")
        with self.assertRaises(BoundaryError): pair.invoke_paid_model()
        self.assertEqual(called, [])
        pair.db.close()

    def test_expired_pending_request_and_late_response_are_blocked(self):
        c = self.channel(); packet = c.export({"neutral":1}); raw = answer(packet)
        with c.db: c.db.execute("UPDATE meta SET value='0' WHERE key='started'")
        with self.assertRaises(BoundaryError): c.export({"neutral":1})
        with self.assertRaises(BoundaryError): c.retain(packet["request_id"], raw)
        self.assertEqual(c.db.execute("SELECT result FROM calls").fetchone()[0], raw)

    def test_nonfinite_and_duplicate_json_are_retained_and_rejected(self):
        c = self.channel(); packet = c.export({"neutral":1})
        raw = answer(packet).replace(b'"predictions":[', b'"predictions":[NaN,')
        with self.assertRaises(BoundaryError): c.retain(packet["request_id"], raw)
        packet = c.export({"neutral":2})
        raw = answer(packet).replace(b'"proposal":', b'"arm":"baseline","proposal":')
        with self.assertRaises(BoundaryError): c.retain(packet["request_id"], raw)

    def test_native_model_and_cap_mismatch_cannot_export(self):
        c = self.channel("edi")
        class Session:
            out = c.directory / "native"
            def pending(self):
                return {"job_id":"fixture"}, {"job":{"job_id":"fixture", "binding":{"model_id":"wrong","revision":MODEL["revision"]},
                    "input_token_cap":12288,"output_token_cap":4096,"role":"student","teaching_stage":"standard"}}
        with self.assertRaises(BoundaryError): NativeEDI(c, Session()).export()
        self.assertEqual(c.usage()["calls"], 0)

    def test_native_adapter_rejects_shared_or_foreign_directory(self):
        c = self.channel("edi")
        class Session: out = self.root / "baseline" / "native"
        with self.assertRaises(BoundaryError): NativeEDI(c, Session())


if __name__ == "__main__":
    unittest.main(verbosity=2)

