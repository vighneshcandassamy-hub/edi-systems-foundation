"""CPU engineering checks. Authored model fixtures are NOT live inference evidence."""
import base64
from datetime import timedelta
from hashlib import sha256
import importlib
from io import BytesIO
import json
from pathlib import Path
import secrets
import sqlite3
import sys
import tempfile
from threading import Thread
import unittest

from edi.agency.benchmark import BenchmarkAuthority, PublicIntent, SimulationGrant
from edi.agency.config import AgencyProfile
from edi.inquiry.contracts import WorkflowProfile
from edi.inquiry.benchmark import Investigation
from edi.inquiry.runtime import Runtime
from edi.observe.benchmark import BrokerConnector, http_json
from edi.observe.contracts import Capture, OriginSpec
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import InquiryRequest, ModelBinding, Response, StepRequest
from edi.reason.gateway import NativeGateway, OpenAITeacherBackend
from edi.shared.config import LocalProfile
from edi.shared.contracts import utc_now
from edi.shared.durable_io import CallJournal, canonical, digest
from edi.shared.errors import EDIError, ErrorCode

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / 'benchmarks/meadows-budworm/environment/v0_2'
sys.path.insert(0, str(WORLD))
broker = importlib.import_module('broker')


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.token = secrets.token_urlsafe(32)
        self.server = broker.server(WORLD / 'fixture', self.root / 'world', ROOT / 'benchmarks/meadows-budworm/database/evidence.sqlite', self.token)
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.endpoint = 'http://127.0.0.1:' + str(self.server.server_port)
        self.profile = LocalProfile(database=self.root/'c1.sqlite', workspace_id='engineering', min_free_disk_bytes=0)
        self.binding = ModelBinding(model_id='fixture-wire-not-a-real-model', revision='authored-fixture-v1', provider='unit-test', engine='injected-fixture', tokenizer_revision='test-counter-v1')
        self.reason_profile = ReasoningProfile(database=self.root/'c4.sqlite', workspace_id='engineering', student=self.binding, teacher=self.binding, min_free_disk_bytes=0)
        self.agency_profile = AgencyProfile(database=self.root/'c7.sqlite', workspace_id='engineering', min_free_disk_bytes=0)
        self.workflow_profile = WorkflowProfile(database=self.root/'c0.sqlite', workspace_id='engineering', min_free_disk_bytes=0)
        self.runtime = Runtime(self.profile, reasoning_profile=self.reason_profile, agency_profile=self.agency_profile, workflow_profile=self.workflow_profile)
        self.grant = SimulationGrant(grant_id='engineering', session_id='engineering', workspace_id='engineering',
            endpoint=self.endpoint, token_sha256=sha256(self.token.encode()).hexdigest(), mission_sha256=digest(json.loads((WORLD/'fixture/mission.json').read_text())),
            operator_id='test-operator', not_before=utc_now()-timedelta(seconds=1), expires_at=utc_now()+timedelta(hours=2),
            operations=tuple(x['operation'] for x in json.loads((WORLD/'PUBLIC_OPERATIONS.json').read_text())['operations']))
        self.authority = self.make_authority()
        self.connector = self.make_connector()

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join()
        self.temp.cleanup()

    def make_authority(self, grant=None):
        return self.runtime.agency.benchmark_authority(grant or self.grant, endpoint=self.endpoint,
            token_sha256=sha256(self.token.encode()).hexdigest(), workspace_id='engineering', session_id='engineering')

    def make_connector(self, transport=http_json, runtime=None):
        return BrokerConnector(runtime or self.runtime, self.endpoint, self.token, 'engineering', self.authority,
            self.root/'c0.sqlite', transport=transport)

    def call(self, op, **body):
        body.setdefault('request_id', secrets.token_hex(8))
        return self.connector.call(PublicIntent(operation=op, body=body))

    def inquiry(self, record_id=None):
        evidence = []
        if record_id:
            obs = self.runtime.observation.get_record(record_id)
            evidence = [{'record_id':record_id, 'length':obs.manifest.byte_count}]
        req = InquiryRequest.model_validate_json(canonical({'workspace_id':'engineering', 'request_id':'inquire', 'inquiry_id':'inquire',
            'question':'Inspect supplied neutral evidence', 'purpose':'Engineering only', 'scope':'Bounded selected data',
            'horizon':'Not a scientific evaluation', 'model_revision':0, 'evidence':evidence}))
        ep = self.runtime.reasoning.investigate(req)
        return self.runtime.reasoning.step(StepRequest(workspace_id='engineering', inquiry_id='inquire', request_id='student-job', action='student', reason='Test native handoff'))

    @staticmethod
    def fixture_response(messages, job):
        identity = json.loads(messages[0]['content'])['response_identity']
        data = {**identity, 'rationale_summary':'Authored transport fixture, no model executed', 'hypotheses':[],
            'limitation':'Unit-test control only; not autonomous reasoning'}
        wire = canonical({'fixture_response':data}).encode()
        return wire, canonical(data), 100, 50

    def gateway(self, send=None, counter=None):
        return NativeGateway(self.runtime, self.binding, self.root/'c4.sqlite', send or self.fixture_response,
            counter or (lambda m:100), attribution='AUTHORED UNIT-TEST TRANSPORT; NO MODEL EXECUTED')

    def test_exact_c1_capture_and_replay(self):
        result = self.call('mission', request_id='mission')
        again = self.call('mission', request_id='mission')
        self.assertEqual(result, again)
        raw = self.runtime.observation.read_payload(result['evidence_record_id'], length=result['response_bytes'])
        self.assertEqual(sha256(raw).hexdigest(), result['sha256'])
        self.assertEqual(self.connector.journal.get('mission')['attempts'], 1)

    def test_request_identity_conflict(self):
        self.call('search', request_id='same', query='first')
        with self.assertRaises(EDIError) as caught:
            self.call('search', request_id='same', query='changed')
        self.assertEqual(caught.exception.code, ErrorCode.CONFLICT)

    def test_lost_receipt_does_not_duplicate_work(self):
        first = True
        def lose(url, body, headers):
            nonlocal first
            result = http_json(url, body, headers)
            if first:
                first = False
                raise TimeoutError('injected lost committed response')
            return result
        connector = self.make_connector(lose)
        intent = PublicIntent(operation='measure', body={'request_id':'lost', 'plots':['S01'], 'metric':'foliage'})
        with self.assertRaises(TimeoutError): connector.call(intent)
        result = connector.call(intent)
        self.assertEqual(result['http_status'], 200)
        status = self.call('status')['body']
        self.assertEqual(len(status['jobs']), 1)
        self.assertEqual(status['spent_this_year'], 0)
        self.call('advance', years=1)
        self.assertEqual(self.call('status')['body']['spent_this_year'], 2)
        self.assertEqual(connector.journal.get('lost')['attempts'], 2)

    def test_restart_preserves_original_request_and_evidence(self):
        before = self.call('status', request_id='restart')
        reopened = Runtime(self.profile, reasoning_profile=self.reason_profile, agency_profile=self.agency_profile, workflow_profile=self.workflow_profile)
        after = self.make_connector(runtime=reopened).call(PublicIntent(operation='status', body={'request_id':'restart'}))
        self.assertEqual(before, after)
        self.assertEqual(reopened.observation.get_record(after['evidence_record_id']).manifest.sha256, after['sha256'])

    def test_asset_reassembly_external_origin_and_hash(self):
        docs = self.call('search', source='external', limit=100)['body']['items']
        doc = next(x for x in docs if x['format']=='png')
        obs = self.connector.acquire_asset(doc['id'], 'asset')
        self.assertEqual(obs.manifest.sha256, doc['sha256'])
        self.assertEqual(obs.capture.origin_class, 'external')
        self.assertEqual(obs.capture.profiles['document_id'], doc['id'])
        self.assertFalse(obs.capture.profiles['derived_is_independent_evidence'])

    def test_all_public_operations_and_pending_objective(self):
        self.assertEqual(self.call('sources')['http_status'], 200)
        self.assertEqual(self.call('people')['http_status'], 200)
        docs = self.call('search', source='external', limit=100)['body']['items']
        csv = next(x for x in docs if x['format']=='csv')
        self.assertEqual(self.call('read', document_id=csv['id'])['http_status'], 200)
        rows = self.call('records', document_id=csv['id'], limit=2)
        self.assertEqual(rows['http_status'], 200)
        self.assertEqual(self.call('ask', person_id='manager', question='Provide your recorded information')['http_status'], 200)
        self.assertEqual(self.call('measure', plots=['S01'], metric='foliage')['http_status'], 200)
        self.assertEqual(self.call('act', kind='treat', plots=['S01'], method='selective', dose=0.1)['http_status'], 200)
        self.assertEqual(self.call('advance', years=1)['http_status'], 200)
        proposal = self.call('propose', objective='Authored engineering proposal', reason='Verify proposal boundary')['body']
        self.assertEqual(proposal['status'], 'pending_human_review')
        self.assertTrue(proposal['original_objective_unchanged'])
        self.assertEqual(self.call('mission')['http_status'], 200)
        self.assertEqual(self.call('status')['http_status'], 200)
        self.assertEqual(self.call('submit', conclusion='AUTHORED ENGINEERING CHECK; NOT AN EDI INVESTIGATION')['http_status'], 200)
        self.assertEqual(self.call('status')['http_status'], 409)

    def test_grant_scope_and_expiry(self):
        expired = self.grant.model_copy(update={'not_before':utc_now()-timedelta(hours=2), 'expires_at':utc_now()-timedelta(hours=1)})
        with tempfile.TemporaryDirectory() as d:
            a = BenchmarkAuthority(Path(d)/'c7.sqlite', expired, endpoint=self.endpoint, token_sha256=sha256(self.token.encode()).hexdigest(), workspace_id='engineering', session_id='engineering')
            with self.assertRaises(EDIError): a.authorize(PublicIntent(operation='status', body={'request_id':'expired'}))
        with self.assertRaises(ValueError): SimulationGrant.model_validate_json(canonical({**self.grant.model_dump(mode='json'), 'endpoint':'https://example.com'}))

    def test_denied_public_request_is_evidence(self):
        result = self.call('measure', plots=['S01'], metric='unsupported')
        self.assertEqual(result['http_status'], 422)
        self.assertTrue(self.runtime.observation.get_record(result['evidence_record_id']))

    def test_missing_auth_and_private_path(self):
        status, _ = http_json(self.endpoint+'/v2/status', {'request_id':'wrong-auth'}, {})
        self.assertEqual(status, 401)
        status, _ = http_json(self.endpoint+'/private/state', {'request_id':'private'}, {'Authorization':'Bearer '+self.token})
        self.assertEqual(status, 404)

    def test_gateway_fixture_native_import_and_no_redispatch(self):
        ep = self.inquiry()
        gateway = self.gateway()
        response = gateway.complete(ep.jobs[-1], ep)
        result = self.runtime.reasoning.import_response(response)
        self.assertEqual(result.jobs[-1].status, 'completed')
        self.assertEqual(gateway.complete(ep.jobs[-1], ep), response)
        self.assertEqual(gateway.journal.get(ep.jobs[-1].job_id)['attempts'], 1)

    def test_model_timeout_is_not_retried(self):
        count = 0
        def timeout(messages, job):
            nonlocal count
            count += 1
            raise TimeoutError('authored provider timeout')
        ep = self.inquiry(); gateway = self.gateway(send=timeout)
        with self.assertRaises(TimeoutError): gateway.complete(ep.jobs[-1], ep)
        with self.assertRaises(EDIError) as caught: gateway.complete(ep.jobs[-1], ep)
        self.assertEqual(caught.exception.code, ErrorCode.UNKNOWN_COMMIT)
        self.assertEqual(count, 1)

    def test_token_cap_blocks_before_dispatch(self):
        ep = self.inquiry(); gateway = self.gateway(counter=lambda m:100000)
        with self.assertRaises(EDIError) as caught: gateway.complete(ep.jobs[-1], ep)
        self.assertEqual(caught.exception.code, ErrorCode.CAPACITY)
        self.assertIsNone(gateway.journal.get(ep.jobs[-1].job_id))

    def test_actual_image_bytes_in_wire_fixture(self):
        # A fixed 1x1 PNG used solely to inspect the native image route.
        image = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jWZkAAAAASUVORK5CYII=')
        origin = self.runtime.register_origin(OriginSpec(namespace='neutral-image', native_source_id='pixel', epoch='1', deliverer='fixture', channel='image', adapter='authored-image'))
        obs = self.runtime.observe(Capture(origin_ref=origin.origin_ref, idempotency_key='image', media_type='image/png', origin_class='generated', completeness='complete'), BytesIO(image)).observation
        ep = self.inquiry(obs.record_id)
        messages, refs = self.gateway().messages(ep.jobs[-1], ep)
        url = messages[1]['content'][1]['image_url']['url']
        self.assertEqual(base64.b64decode(url.split(',')[1]), image)
        self.assertEqual(refs[0]['sha256'], sha256(image).hexdigest())
        # This is image *transport* verification, not a model vision result.

    def test_teacher_cannot_propose_actions(self):
        ep = self.inquiry(); gateway = self.gateway()
        response = gateway.complete(ep.jobs[-1], ep); self.runtime.reasoning.import_response(response)
        ep = self.runtime.reasoning.step(StepRequest(workspace_id='engineering', inquiry_id='inquire', request_id='teacher-job', action='teacher', reason='Fixture critique', teacher_trigger='consequential'))
        bad = Response.model_validate_json(canonical({**response.model_dump(mode='json'), 'job_id':ep.jobs[-1].job_id,
            'request_id':'teacher-response', 'response_id':'teacher-response', 'feedback_disposition':'retained-for-review',
            'operation_proposals':[{'operation':'world-call','arguments':{'operation':'advance','body':{}}}]}))
        with self.assertRaises(EDIError) as caught:self.runtime.reasoning.import_response(bad)
        self.assertEqual(caught.exception.code, ErrorCode.DENIED)

    def test_teacher_key_missing_is_explicit(self):
        with self.assertRaises(EDIError): OpenAITeacherBackend('')

    def test_journal_atomic_dispatch_claim(self):
        journal = CallJournal(self.root/'claim.sqlite', 'test')
        journal.begin('job', {'original':True})
        self.assertTrue(journal.claim_once('job'))
        self.assertFalse(CallJournal(self.root/'claim.sqlite', 'test').claim_once('job'))

    def test_dynamic_c0_choices_use_native_c4_records(self):
        step = 0
        def chosen(messages, job):
            nonlocal step
            identity = json.loads(messages[0]['content'])['response_identity']
            operation = {'operation':'world-call','arguments':{'operation':'sources' if step==0 else 'submit', 'body':{} if step==0 else {'conclusion':'AUTHORED SCHEDULER CONTROL; NOT INFERENCE'}}}
            step += 1
            data = {**identity, 'rationale_summary':'Authored dynamic dispatch control', 'limitation':'No real model executed', 'operation_proposals':[operation]}
            return canonical({'fixture':data}).encode(), canonical(data), 100, 50
        investigation = Investigation(self.runtime, self.connector, self.gateway(send=chosen), self.root/'c0.sqlite', 'dynamic', max_turns=4)
        first = investigation.step(); self.assertEqual(first['state'], 'ready')
        second = investigation.step(); self.assertEqual(second['state'], 'completed')
        self.assertEqual(step, 2)
        self.assertEqual(investigation.state()['state'], 'completed')
        self.assertEqual(len(self.runtime.reasoning.get('dynamic:inquiry:0').responses), 1)
        self.assertTrue(self.runtime.reasoning.get('dynamic:inquiry:1').context.evidence)


if __name__ == '__main__':
    unittest.main(verbosity=2)
