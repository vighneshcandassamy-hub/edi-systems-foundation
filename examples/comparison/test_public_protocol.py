"""Boundary regressions. Execute on Kaggle; no local project runtime."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from public_protocol import PublicProtocol,public_shapes,bind_schema
from local_qwen_adapter import BASE_SCHEMA

class PublicProtocolTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/"cedar-world").mkdir()
        self.db=sqlite3.connect(self.root/"cedar-world/run.sqlite")
        self.db.executescript("CREATE TABLE events(operation,response); CREATE TABLE attempts(operation,status); CREATE TABLE state(payload); INSERT INTO state VALUES ('PRIVATE-ID-SECRET');")
        self.db.commit();self.p=PublicProtocol(self.root,{})
    def tearDown(self):self.db.close();self.tmp.cleanup()
    def event(self,op,body,status=200):
        with self.db:
            if status==200:self.db.execute("INSERT INTO events VALUES (?,?)",(op,json.dumps(body)))
            self.db.execute("INSERT INTO attempts VALUES (?,?)",("/v2/"+op,status))
    def test_initial_discovery_no_fabricated_ids(self):
        v=self.p.snapshot();s=public_shapes(v)
        self.assertIn("search",s);self.assertNotIn("read",s);self.assertNotIn("act",s)
        self.assertNotIn("PRIVATE-ID",json.dumps(v))
    def test_sources_not_documents(self):
        self.event("sources",{"sources":[{"id":"S-1","name":"Archive"}]})
        self.assertFalse(self.p.snapshot()["documents"])
    def test_read_ids_and_stands_from_public_response_only(self):
        self.event("search",{"items":[{"id":"D-1","title":"Survey"}]})
        self.event("read",{"id":"D-1","body":"stand_id,value\nP-1,7\n"})
        v=self.p.snapshot();self.assertEqual(v["stand_ids"],["P-1"])
        self.assertEqual(v["acquired_document_ids"],["D-1"])
        s=public_shapes(v);self.assertEqual(s["act"]["anyOf"][0]["properties"]["kind"],{"const":"treat"})
    def test_rejected_read_excluded_before_next_preview(self):
        self.event("search",{"items":[{"id":"D-bad","title":"Missing"}]})
        self.p.begin({"operation":{"name":"read","args":{"document_id":"D-bad"}}})
        self.event("read",{},404)
        v=self.p.snapshot();self.assertNotIn("D-bad",v["documents"])
        self.assertIn("read",v["blocked_operations_at_this_cut"])
        self.p.finish();self.assertEqual(v,self.p.snapshot())
    def test_submit_lists_and_acquired_citations(self):
        self.event("read",{"id":"D-1","body":"{}"})
        s=public_shapes(self.p.snapshot())["submit"]
        self.assertEqual(s["properties"]["recommendations"]["type"],"array")
        self.assertEqual(s["properties"]["evidence_ids"]["items"]["enum"],["D-1"])
    def test_native_decoder_retains_internal_component_tools(self):
        from edi.reason.operation_args import serving_schema
        s=bind_schema(serving_schema(controller_turn=True,controller_policy="information-seeking/1.1"),"edi",self.p.snapshot())
        names=[b["properties"]["operation"]["const"] for b in s["$defs"]["OperationProposal"]["anyOf"]]
        self.assertIn("component-call",names);self.assertIn("world-call",names)
        self.assertNotIn("acquire-asset",names);self.assertNotIn("teacher-review",names)
    def test_baseline_history_shapes_match_existing_boundary(self):
        s=bind_schema(BASE_SCHEMA,"baseline",self.p.snapshot())
        branches=s["properties"]["operation"]["anyOf"]
        h=next(b for b in branches if b["properties"]["name"]["const"]=="history_search")
        self.assertEqual(set(h["properties"]["args"]["required"]),{"text","offset","limit"})

if __name__=="__main__":unittest.main()
