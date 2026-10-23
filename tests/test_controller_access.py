"""Authored authority/transport regressions; no live inference."""
from datetime import datetime, timedelta, timezone
import json
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from pydantic import ValidationError
from edi.agency.benchmark import SimulationGrant
from edi.inquiry.benchmark import describe_access
from edi.reason.contracts import Episode
from edi.reason.gateway import render_job_messages
from edi.reason.service import Reasoning
from edi.shared.durable_io import digest
from edi.shared.errors import EDIError, ErrorCode


class AccessContractTests(unittest.TestCase):
    def setUp(self):
        now = datetime.now(timezone.utc)
        self.mission = {"objective": "Investigate an unresolved observation",
            "public_operations": {
                "sources": {"body": {}, "returns": "catalogue"},
                "ask": {"body": {"person_id": "available ID", "question": "request"}, "returns": "record"}}}
        self.grant = SimulationGrant.model_validate_json(json.dumps({
            "grant_id": "g", "session_id": "s", "workspace_id": "w",
            "endpoint": "http://127.0.0.1:8098", "token_sha256": "0"*64,
            "mission_sha256": digest(self.mission), "operator_id": "operator",
            "not_before": now.isoformat(), "expires_at": (now+timedelta(minutes=5)).isoformat(),
            "operations": ["mission", "sources"]}))
    def test_catalogue_is_adopted_intersection_not_authority_expansion(self):
        description = describe_access(self.mission, self.grant)
        self.assertEqual(set(description.operations), {"sources"})
        self.assertEqual(description.mission_sha256, self.grant.mission_sha256)
        self.assertNotIn("token_sha256", description.model_dump_json())
        bad = {**self.mission, "objective": "unadopted source instruction"}
        with self.assertRaises(EDIError) as caught:
            describe_access(bad, self.grant)
        self.assertEqual(caught.exception.code, ErrorCode.INTEGRITY)
    def test_description_bytes_and_names_are_bounded(self):
        bad = {"public_operations": {"sources": {"returns": "x"*16385}}}
        with self.assertRaises(ValidationError):
            describe_access(bad, self.grant.model_copy(update={"mission_sha256": digest(bad)}))
    def test_renderer_promotes_only_c0_description_and_matches_content_fields(self):
        from edi.reason.contracts import InquiryRequest, ModelBinding, Job, Context
        now = datetime.now(timezone.utc)
        binding = ModelBinding(model_id="authored", revision="1", provider="fixture",
            engine="fixture", tokenizer_revision="1")
        inquiry = InquiryRequest.model_validate_json(json.dumps({
            "workspace_id":"w", "inquiry_id":"i", "request_id":"i",
            "question":"Investigate", "purpose":"Fixture", "scope":"Fixture", "horizon":"one turn",
            "response_mode":"controller-turn", "model_revision":0,
            "controller_access":describe_access(self.mission,self.grant).model_dump(mode="json")}))
        context = Context(model_revision=0,world=(),dependencies=(),evidence=(),
            limitations=("No measurements acquired",),sha256="a"*64)
        job = Job(job_id="j",role="student",round=1,binding=binding,
            context_sha256=context.sha256,protocol_id="fixture",questions=(),
            input_token_cap=12288,output_token_cap=4096,created_at=now,reason="Fixture")
        ep = Episode(request=inquiry,sequence=1,created_at=now,updated_at=now,
            profile_snapshot={},operating_profile={},context=context,jobs=(job,))
        class Saved:
            export_job=Reasoning.export_job
            def get(self,unused): return ep
        runtime=SimpleNamespace(reasoning=Saved())
        messages,_=render_job_messages(runtime,binding,job,ep,schema_in_transport=True)
        control=json.loads(messages[0]["content"])
        self.assertEqual(set(control["controller_access"]["operations"]),{"sources"})
        self.assertNotIn("ask", control["controller_access"]["operations"])
        self.assertEqual(set(control["response_fields"]["required"]),
                         {"rationale_summary","limitation","operation_proposals"})
        self.assertNotIn("workspace_id",control["response_fields"]["fields"])
        data=json.loads(messages[1]["content"][0]["text"])
        self.assertEqual(data["context"]["evidence"],[])
        self.assertNotIn("candidate claims", control["rule"])
        # The teacher remains critique-only; no actionable controller surface.
        teacher=job.model_copy(update={"role":"teacher"})
        teacher_ep=ep.model_copy(update={"jobs":(teacher,)})
        with patch.object(Saved,"get",return_value=teacher_ep):
            teacher_messages,_=render_job_messages(runtime,binding,teacher,teacher_ep)
        teacher_control=json.loads(teacher_messages[0]["content"])
        self.assertNotIn("controller_access", teacher_control)
        self.assertNotIn("controller_turn", teacher_control)
        self.assertIn("Critique only",teacher_control["operation_rules"])


if __name__=="__main__":
    unittest.main()
