"""Scoped integration regressions. All model/counter behavior is authored, not Qwen.

Set EDI_CEDAR_CHECKPOINT_ROOT to replay the retained public read envelope. No
hidden-world evaluator, remote transport, inference or benchmark is invoked.
"""
import base64
import json
import os
from pathlib import Path
import sqlite3
import unittest

import test_information_seeking as fixtures
from edi.reason.gateway import VllmBackend
from edi.shared.durable_io import canonical
from edi.shared.errors import EDIError


class ContextCapacityTests(unittest.TestCase):
    def setUp(self):
        self.h = fixtures.InformationSeekingTests()
        self.h.setUp()

    def tearDown(self):
        self.h.tearDown()

    @unittest.skipUnless(os.environ.get('EDI_CEDAR_CHECKPOINT_ROOT'), 'Preserved Cedar public envelope required')
    def test_saved_public_read_delivers_verified_native_bytes_and_bounded_cut(self):
        root = Path(os.environ['EDI_CEDAR_CHECKPOINT_ROOT']).resolve()
        with sqlite3.connect((root/'owners.sqlite3').as_uri()+'?mode=ro', uri=True) as c:
            raw = b''.join(bytes(x[0]) for x in c.execute(
                'select payload from payload_chunks where record_id=? order by ordinal',
                ('65b41b79-abf9-43eb-b2b7-c2a7a04c0956',)))
        body = json.loads(raw)
        loop = self.h.open(lambda control, data: fixtures.stop(), teacher=True,
            teaching_mode='intensive', input_token_cap=16384)
        state = loop.state()
        original = loop.connector._capture('saved-read-envelope', raw)
        result = {'http_status':200, 'body':body, 'evidence_record_id':original.observation.record_id}
        # Reuse the complete bytes already returned by the old public read. No new acquisition.
        asset = loop.connector.extract_returned_asset(result, body['id'], 'saved-native')
        expected = base64.b64decode(body['asset']['data'], validate=True)
        self.assertEqual(loop.runtime.observation.read_payload(asset.record_id, length=len(expected)), expected)
        self.assertEqual(asset.manifest.byte_count, 4353)
        self.assertTrue(expected.startswith(b'year,station,reading,unit,instrument_code'))
        self.assertEqual(loop.connector.extract_returned_asset(result, body['id'], 'saved-native').record_id, asset.record_id)
        self.assertEqual(loop.runtime.observation.read_payload(original.observation.record_id, length=len(raw)), raw)
        mission = state['evidence'][0]
        growing = [mission]
        for index in range(6):
            extra = loop.connector._capture('pressure-'+str(index), (b'x' * 8192))
            growing = loop._bounded_add(growing, loop._selection(extra.observation.record_id))
        self.assertEqual(growing[0], mission)
        state['evidence'] = [mission, loop._selection(asset.record_id)]
        # Deliberately saturating authored counter, used to verify control flow only.
        # It is NOT the pinned Qwen tokenizer and establishes no real-token savings.
        previews = []
        def counter(messages):
            data = json.loads(messages[1]['content'][0]['text'])
            previews.append(data)
            return 10000 + len(data['context']['evidence'][-1]['excerpt'])
        loop.student.count_tokens = counter
        episode = loop._inquiry(state, 'saved-fit')
        self.assertGreater(len(previews), 1)
        self.assertEqual(len(episode.jobs), 0)
        latest = episode.context.evidence[-1]
        self.assertLess(latest.selected_bytes, len(expected))
        self.assertIn('omitted ranges remain in C1', latest.limitation)
        self.assertIn('year,station', latest.excerpt)
        self.assertNotIn('eWVhcixzdGF0', latest.excerpt)
        self.assertTrue(any('Token-budget selection' in value for value in episode.context.limitations))
        fitted = json.loads(loop.phases.get('saved-fit:context-fit')['result'])
        self.assertLessEqual(fitted['trials'][-1]['input_tokens'] + fitted['stage_headroom_tokens'], 16384)
        self.assertEqual(self.h.calls, [])
        with sqlite3.connect(loop.runtime.reasoning.profile.database) as c:
            self.assertEqual(c.execute('select count(*) from io_inference_c4').fetchone()[0], 0)
        requests = json.loads((self.h.root/'world-session.json').read_bytes())['requests']
        self.assertEqual([x['operation'] for x in requests], ['mission'])
        # Corruption is detected before a native content record can be accepted.
        corrupt = json.loads(raw)
        corrupt['sha256'] = '0' * 64
        with self.assertRaises(EDIError):
            loop.connector.extract_returned_asset({**result,'body':corrupt},body['id'],'bad-hash')
        partial = json.loads(raw);partial['asset']['has_more'] = True
        self.assertIsNone(loop.connector.extract_returned_asset({**result,'body':partial},body['id'],'partial'))

    def test_unsatisfiable_context_yields_before_job_or_provider_dispatch(self):
        loop = self.h.open(lambda control, data: fixtures.stop())
        loop.student.count_tokens = lambda messages: 20000
        state = loop.step()
        self.assertEqual(state['state'], 'yielded')
        self.assertIn('cannot fit', state['stop_reason'])
        self.assertEqual(self.h.calls, [])
        self.assertEqual(state['known_input_tokens'], 0)
        self.assertEqual(state['used_tokens'], 0)
        with self.assertRaises(EDIError):
            loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual(loop.step(),state)

    def test_later_exact_capacity_failure_is_terminal_without_unknown_retry(self):
        loop = self.h.open(lambda control, data: fixtures.stop())
        counts = iter((100, 20000))
        loop.student.count_tokens = lambda messages: next(counts)
        state = loop.step()
        self.assertEqual(state['state'], 'yielded')
        self.assertIn('exceeds job cap', state['stop_reason'])
        self.assertEqual(self.h.calls, [])
        self.assertEqual(loop.step(), state)
        with sqlite3.connect(loop.runtime.reasoning.profile.database) as c:
            self.assertEqual(c.execute('select count(*) from io_inference_c4').fetchone()[0], 0)

    def test_revision_grammar_requires_nonnull_feedback_without_forcing_action(self):
        def basis(control, data, proposal):
            return {'evidence_record_ids':[], 'understanding':'Authored grammar fixture',
                'information_need':'Inspect available source directory', 'expected_use':'Read directory',
                'feedback_response':'Considered the critique; retain sources.' if control['teaching']['stage']=='revision' else None}
        loop = self.h.open(lambda control, data: fixtures.public('sources'), teacher=True,
            teaching_mode='intensive', controller_policy='information-seeking/1.1', decision_basis=basis)
        self.assertEqual(loop.step()['state'], 'ready')
        backend = VllmBackend('http://127.0.0.1:8008', self.h.binding.model_id)
        decisions = [(control,data) for role,control,data in self.h.calls if role=='student']
        for control,data in decisions:
            messages = [{'role':'system','content':canonical(control)},
                {'role':'user','content':[{'type':'text','text':canonical(data)}]}]
            shape = backend.generation_schema_for(messages)['$defs']['DecisionBasis']
            field = shape['properties']['feedback_response']
            if control['teaching']['stage']=='revision':
                self.assertEqual(field['type'], 'string')
                self.assertIn('feedback_response',shape['required'])
            else:
                self.assertIn('anyOf', field)
