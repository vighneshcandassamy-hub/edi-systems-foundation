"""Native controller regression fixtures. No student or teacher model executes."""
from datetime import timedelta
import gc
from io import BytesIO
from unittest.mock import patch
from hashlib import sha256
import json
from pathlib import Path
import secrets
import sys
import tempfile
import unittest

from edi.agency.benchmark import SimulationGrant
from edi.agency.config import AgencyProfile
from edi.inquiry.benchmark import Investigation
from edi.inquiry.runtime import Runtime
from edi.observe.benchmark import BrokerConnector
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import InquiryRequest, ModelBinding, OperationProposal
from edi.reason.gateway import NativeGateway
from edi.reason.operation_args import generation_schema, serving_schema
from edi.shared.config import LocalProfile
from edi.shared.contracts import utc_now
from edi.shared.durable_io import canonical, digest
from edi.shared.errors import EDIError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'examples/autonomous' if (ROOT / 'examples/autonomous').exists() else ROOT))
from neutral_world import MISSION, start_world


def stop(alternative='sources'):
    return {'operation': 'yield', 'arguments': {
        'reason': 'Deliberate authored pause; no successful investigation is claimed',
        'assessment': {'disposition': 'paused', 'unresolved_needs': ['Unmeasured next sample'],
            'alternatives_considered': [{'operation': alternative,
                'reason_for_not_using': 'Fixture judgment only; does not assert exhaustion or execution'}],
            'resume_when': 'New evidence or a changed decision to use available access'}}}


def public(name, **body):
    return {'operation': 'world-call', 'arguments': {'operation': name, 'body': body}}


class InformationSeekingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.token = secrets.token_urlsafe(32)
        class InProcessServer:
            def __init__(self, address, handler):
                self.RequestHandlerClass = handler
            def serve_forever(self): pass
            def shutdown(self): pass
            def server_close(self): pass
        # Exercise the unchanged broker HTTP handler without a socket. Host
        # policy blocks TCP loopback. This is deliberately not network evidence.
        with patch('neutral_world.ThreadingHTTPServer', InProcessServer):
            self.server = start_world(self.root, self.token)
        self.endpoint = 'http://127.0.0.1:8098' 
        self.binding = ModelBinding(model_id='authored-fixture', revision='1',
            provider='fixture', engine='no-model', tokenizer_revision='fixture-counter')
        self.teacher_binding = self.binding.model_copy(update={'model_id': 'authored-teacher-fixture'})
        self.calls = []
        now = utc_now()
        self.grant = SimulationGrant(grant_id='test', session_id='test', workspace_id='test',
            endpoint=self.endpoint, token_sha256=sha256(self.token.encode()).hexdigest(),
            mission_sha256=digest(MISSION), operator_id='fixture',
            not_before=now-timedelta(seconds=1), expires_at=now+timedelta(minutes=10),
            operations=tuple(MISSION['public_operations']))

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        gc.collect()
        self.temp.cleanup()

    def open(self, choose, *, teacher=False):
        runtime = Runtime(LocalProfile(database=self.root/'owners.sqlite3', workspace_id='test', min_free_disk_bytes=0),
            reasoning_profile=ReasoningProfile(database=self.root/'reason.sqlite3', workspace_id='test',
                student=self.binding, teacher=self.teacher_binding, min_free_disk_bytes=0),
            agency_profile=AgencyProfile(database=self.root/'agency.sqlite3', workspace_id='test',
                operator_ids=('fixture',), min_free_disk_bytes=0))
        def send(messages, job):
            control = json.loads(messages[0]['content'])
            data = json.loads(messages[1]['content'][0]['text'])
            self.calls.append((job.role, control, data))
            if job.role == 'teacher':
                content = {'rationale_summary': 'Authored critique only', 'limitation': 'No inference',
                    'feedback_disposition': 'retained-for-review'}
            else:
                content = {'rationale_summary': 'Authored regression', 'limitation': 'No inference',
                    'operation_proposals': [choose(control, data)]}
            return canonical(content).encode(), canonical(content), 100, 50
        student = NativeGateway(runtime, self.binding, runtime.reasoning.profile.database,
            send, lambda messages: 100, attribution='Authored fixture; no live model')
        teacher_gateway = NativeGateway(runtime, self.teacher_binding, runtime.reasoning.profile.database,
            send, lambda messages: 100, attribution='Authored teacher fixture; no live model',
) if teacher else None
        authority = runtime.agency_for('C0').benchmark_authority(self.grant, endpoint=self.endpoint,
            token_sha256=self.grant.token_sha256, workspace_id='test', session_id='test')
        def transport(url, body, headers):
            raw = canonical(body).encode()
            handler = self.server.RequestHandlerClass.__new__(self.server.RequestHandlerClass)
            handler.path = '/v2/' + url.rsplit('/', 1)[1]
            handler.headers = {**headers, 'Content-Length': str(len(raw))}
            handler.rfile, handler.wfile = BytesIO(raw), BytesIO()
            handler.send_response = lambda status: setattr(handler, 'response_status', status)
            handler.send_header = lambda *args: None
            handler.end_headers = lambda: None
            handler.do_POST()
            return handler.response_status, handler.wfile.getvalue()
        connector = BrokerConnector(runtime, self.endpoint, self.token, 'test', authority,
            runtime.workflow.profile.database, transport=transport)
        return Investigation(runtime, connector, student, runtime.workflow.profile.database, 'run',
            teacher_gateway=teacher_gateway, max_turns=5, max_tokens=131072)

    def test_unassessed_yield_is_retained_then_corrected_without_forcing_a_source(self):
        def choose(control, data):
            if data['prior_rejections']:
                return public('sources')
            return {'operation': 'yield', 'arguments': {}}
        loop = self.open(choose)
        state = loop.step()
        self.assertEqual(state['state'], 'ready')
        episode = loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual(len(episode.rejections), 1)
        self.assertEqual(len(episode.responses), 1)
        self.assertIn('assessment', episode.rejections[0].diagnostic)
        self.assertEqual(state['known_input_tokens'], 200)
        self.assertEqual(state['known_output_tokens'], 100)
        self.assertEqual([x['operation'] for x in state['public_outcomes']], ['mission', 'sources'])
        self.assertEqual(self.calls[0][1]['controller_progress']['public_outcomes'][0]['operation'], 'mission')
        self.assertFalse(self.calls[0][1]['controller_progress']['teacher_available'])
        self.assertNotIn('assessment', self.calls[0][2]['context']['evidence'][0]['excerpt'])

    def test_deliberate_stop_is_allowed_before_acquisition_and_reopens_without_calls(self):
        loop = self.open(lambda control, data: stop())
        state = loop.step()
        self.assertEqual(state['state'], 'yielded')
        self.assertEqual(state['yield_assessment'], stop()['arguments']['assessment'])
        self.assertEqual([x['operation'] for x in state['public_outcomes']], ['mission'])
        self.assertEqual(len(self.calls), 1)
        requests = json.loads((self.root/'world-session.json').read_bytes())['requests']
        reopened = self.open(lambda control, data: self.fail('terminal state must not call a model'))
        self.assertEqual(reopened.step(), state)
        self.assertEqual(json.loads((self.root/'world-session.json').read_bytes())['requests'], requests)
        self.assertEqual(len(self.calls), 1)

    def test_progress_carries_actual_receipts_and_remaining_budget_on_restart(self):
        choices = iter([public('sources'), public('read', document_id='m17'), stop()])
        choose = lambda control, data: next(choices)
        loop = self.open(choose)
        loop.step()
        loop = self.open(choose)
        state = loop.step()
        progress = self.calls[-1][1]['controller_progress']
        self.assertEqual(progress['turn'], 1)
        self.assertEqual(progress['remaining_turns'], 4)
        self.assertEqual(progress['remaining_policy_units'], 131072-150)
        self.assertEqual([x['operation'] for x in progress['public_outcomes']], ['mission', 'sources'])
        self.assertEqual(state['public_outcomes'][-1]['http_status'], 200)
        self.assertEqual(loop.step()['state'], 'yielded')
        self.assertEqual(len(self.calls), 3)

    def test_nonexistent_stop_alternative_is_rejected_and_valid_stop_remains_possible(self):
        loop = self.open(lambda control, data: stop('made-up-access') if not data['prior_rejections'] else stop())
        state = loop.step()
        self.assertEqual(state['state'], 'yielded')
        self.assertEqual(len(loop.runtime.reasoning.get('run:inquiry:0').rejections), 1)
        self.assertEqual(len(self.calls), 2)

    def test_unconfigured_teacher_returns_correction_feedback(self):
        loop = self.open(lambda control, data: {'operation':'teacher-review','arguments':{'trigger':'unresolved'}}
            if not data['prior_rejections'] else public('sources'))
        self.assertEqual(loop.step()['state'], 'ready')
        episode = loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual(len(episode.rejections), 1)
        self.assertTrue(all(role == 'student' for role, _, _ in self.calls))

    def test_model_selected_teacher_cycle_stays_critique_only(self):
        loop = self.open(lambda control, data: public('sources') if any(
            r['feedback_disposition'] != 'not-applicable' for r in data['prior_responses']) else
            {'operation':'teacher-review','arguments':{'trigger':'unresolved'}}, teacher=True)
        self.assertEqual(loop.step()['state'], 'ready')
        self.assertEqual([role for role, _, _ in self.calls], ['student','teacher','student'])
        critique = self.calls[1][1]
        self.assertNotIn('controller_progress', critique)
        self.assertNotIn('controller_access', critique)
        self.assertIn('Critique only', critique['operation_rules'])
        episode = loop.runtime.reasoning.get('run:inquiry:0')
        self.assertFalse(episode.responses[1].operation_proposals)

    def test_actual_closure_receipt_is_required_for_completed_state(self):
        choices = iter([public('sources'), public('read', document_id='m17'),
            public('submit', conclusion='Authored control: fixture data only, no scientific claim')])
        loop = self.open(lambda control, data: next(choices))
        self.assertEqual(loop.step()['state'], 'ready')
        self.assertEqual(loop.step()['state'], 'ready')
        state = loop.step()
        self.assertEqual(state['state'], 'completed')
        self.assertEqual(state['public_outcomes'][-1]['operation'], 'submit')
        self.assertEqual(state['public_outcomes'][-1]['http_status'], 200)
        self.assertNotIn('yield_assessment', state)
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(self.open(lambda *_: self.fail('terminal redispatch')).step(), state)

    def test_failed_public_receipt_is_not_presented_as_success_or_access_exhaustion(self):
        choices = iter([public('read', document_id='not-a-document'), stop()])
        loop = self.open(lambda control, data: next(choices))
        state = loop.step()
        self.assertEqual(state['state'], 'ready')
        self.assertEqual(state['public_outcomes'][-1]['http_status'], 422)
        self.assertEqual(loop.step()['state'], 'yielded')
        self.assertEqual(self.calls[-1][1]['controller_progress']['public_outcomes'][-1]['http_status'], 422)

    def test_empty_cut_legacy_and_new_decoder_requirements_are_separate(self):
        legacy = generation_schema()
        current = serving_schema(evidence_references=[], controller_turn=True,
            controller_policy='information-seeking/1.0')
        def arguments(schema):
            return next(b for b in schema['$defs']['OperationProposal']['anyOf']
                if b['properties']['operation']['const']=='yield')['properties']['arguments']
        self.assertEqual(arguments(legacy)['required'], [])
        self.assertEqual(set(arguments(current)['required']), {'reason','assessment'})
        self.assertEqual(current['properties']['operation_proposals']['minItems'], 1)
        OperationProposal.model_validate_json(json.dumps(stop()))
        with self.assertRaises(ValueError):
            generation_schema(controller_policy='unknown')
        with self.assertRaises(ValueError):
            InquiryRequest(workspace_id='w', inquiry_id='i', request_id='i', question='q', purpose='p',
                scope='s', horizon='h', model_revision=0, controller_policy='information-seeking/1.0')


if __name__ == '__main__':
    unittest.main()
