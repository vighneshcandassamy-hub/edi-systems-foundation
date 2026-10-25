"""Authored sole-reasoner integration/transport regressions; no model inference."""
from io import BytesIO
import json
import os
from pathlib import Path
from unittest.mock import patch
import unittest
import test_information_seeking as fixtures
from test_information_seeking import public, stop
from edi.inquiry.application import ApplicationProfile, IntegratedApplication
from edi.observe.benchmark import BrokerConnector
from edi.reason.contracts import ModelBinding
from edi.shared.durable_io import canonical
from edi.shared.errors import EDIError

class SoleReasonerTests(unittest.TestCase):
    setUp=fixtures.InformationSeekingTests.setUp
    tearDown=fixtures.InformationSeekingTests.tearDown
    def app(self):
        profile=ApplicationProfile.model_validate_json(canonical({'application_id':'sole-fixture','run_id':'sole-run',
            'observation':{'database':str(self.root/'owners.sqlite3'),'workspace_id':'test','min_free_disk_bytes':0},
            'student':{'mode':'file-exchange','binding':self.binding.model_dump(mode='json'),
                       'directory':str(self.root/'exchange'),'attribution':'Authored sole-reasoner fixture; no model'},
            'teacher':{'mode':'disabled','binding':ModelBinding().model_dump(mode='json')},
            'broker':{'grant':self.grant.model_dump(mode='json')},
            'agency':{'database':str(self.root/'agency.sqlite3'),'workspace_id':'test',
                      'operator_ids':['fixture'],'min_free_disk_bytes':0},
            'max_turns':5,'max_tokens':262144,'session_seconds':600}))
        def transport(url,body,headers):
            raw=canonical(body).encode();h=self.server.RequestHandlerClass.__new__(self.server.RequestHandlerClass)
            h.path='/v2/'+url.rsplit('/',1)[1];h.headers={**headers,'Content-Length':str(len(raw))}
            h.rfile,h.wfile=BytesIO(raw),BytesIO();h.send_response=lambda status:setattr(h,'response_status',status)
            h.send_header=lambda *a:None;h.end_headers=lambda:None;h.do_POST()
            return h.response_status,h.wfile.getvalue()
        def connector(*a,**kw):return BrokerConnector(*a,**kw,transport=transport)
        env={k:v for k,v in os.environ.items() if k!='EDI_VLLM_API_KEY'};env['EDI_BROKER_TOKEN']=self.token
        with patch.dict(os.environ,env,clear=True),patch('edi.observe.benchmark.BrokerConnector',side_effect=connector),\
                patch('edi.reason.gateway.VllmBackend',side_effect=AssertionError('No Qwen service allowed')):
            return IntegratedApplication(profile)
    def export(self,app):
        state=app.step();self.assertEqual(state['state'],'waiting-reasoner')
        request=json.loads(Path(state['request_path']).read_bytes())
        self.assertEqual(request['reasoning_role'],'sole')
        self.assertIsNone(app.teacher)
        self.assertFalse(json.loads(request['messages'][1]['content'][0]['text'])['inquiry']['controller_progress']['teacher_available'])
        return state,request
    def content(self,request,operation):
        data=json.loads(request['messages'][1]['content'][0]['text'])
        return {'rationale_summary':'Authored transport check, no model intelligence claim.',
            'limitation':'Fixture observations only; not a live reasoning result.',
            'decision_basis':{'evidence_record_ids':[e['reference']['record_id'] for e in data['context']['evidence']],
                'understanding':'Use exact acquired fixture evidence.','information_need':'Discover a public document.',
                'expected_use':'Inspect the actual response before another decision.','repeat_reason':None,'feedback_response':None},
            'operation_proposals':[operation]}
    def import_content(self,app,state,content):
        p=self.root/'response.json';p.write_text(canonical(content));return app.import_reasoner(state['job_id'],p)
    def test_single_reasoner_acquisition_reopen_and_unknown_usage(self):
        app=self.app();state,req=self.export(app)
        self.assertEqual(self.app().step(),state)
        self.import_content(app,state,self.content(req,public('sources')))
        with self.assertRaises(EDIError):self.import_content(app,state,self.content(req,public('sources')))
        next_state=app.step();self.assertEqual(next_state['state'],'ready')
        self.assertEqual(next_state['usage_unknown_jobs'],1)
        self.assertEqual(next_state['known_input_tokens'],0)
        app=self.app();state,req=self.export(app)
        self.import_content(app,state,self.content(req,{'operation':'acquire-asset','arguments':{'document_id':'m17'}}))
        next_state=app.step();self.assertEqual(next_state['state'],'ready')
        app=self.app();state,req=self.export(app)
        data=json.loads(req['messages'][1]['content'][0]['text'])
        self.assertTrue(any(e['origin']['spec']['descriptor'].get('document_id')=='m17' for e in data['context']['evidence']))
        self.import_content(app,state,self.content(req,stop()))
        terminal=app.step();self.assertEqual(terminal['state'],'yielded')
        before=json.loads((self.root/'world-session.json').read_text())['requests']
        self.assertEqual(self.app().step(),terminal)
        self.assertEqual(json.loads((self.root/'world-session.json').read_text())['requests'],before)
        self.assertEqual([x['operation'] for x in before],['mission','sources','read'])
        for i in range(3):
            ep=app.runtime.reasoning.get('sole-run:inquiry:'+str(i))
            self.assertTrue(all(j.role=='student' and j.teaching_stage=='standard' for j in ep.jobs))
    def test_import_identity_injection_retained_rejected(self):
        app=self.app();state,req=self.export(app);content=self.content(req,public('sources'))
        content['job_id']='invented'
        with self.assertRaises(EDIError):self.import_content(app,state,content)
        receipt=app.reasoner.receipt(state['job_id'])
        self.assertEqual(receipt['outcome'],'rejected');self.assertIn('identity',receipt['diagnostic'])
        self.assertTrue(receipt['raw_record_id'])
    def test_changed_request_file_is_not_silently_replaced(self):
        app=self.app();state,req=self.export(app);Path(state['request_path']).write_text('{}')
        again=app.step()
        self.assertEqual(again['state'],'yielded')
        self.assertIn('original reasoner request changed',again['stop_reason'])
    def test_bad_json_goes_to_new_bounded_correction_without_teacher(self):
        app=self.app();state,req=self.export(app);p=self.root/'invalid.json';p.write_text('{')
        with self.assertRaises(EDIError):app.import_reasoner(state['job_id'],p)
        state2,req2=self.export(app);self.assertNotEqual(state2['job_id'],state['job_id'])
        data=json.loads(req2['messages'][1]['content'][0]['text'])
        self.assertEqual(len(data['prior_rejections']),1)
        self.import_content(app,state2,self.content(req2,public('sources')))
        self.assertEqual(app.step()['state'],'ready')
    def test_invalid_usage_is_not_reported_as_measured(self):
        app=self.app();state,req=self.export(app);content=self.content(req,public('sources'))
        content['usage']={'input_tokens':True}
        with self.assertRaises(EDIError):self.import_content(app,state,content)
        receipt=app.reasoner.receipt(state['job_id'])
        self.assertIsNone(receipt['input_tokens']);self.assertIsNone(receipt['output_tokens'])
    def test_unknown_hypothesis_is_still_rejected_natively(self):
        app=self.app();state,req=self.export(app);content=self.content(req,public('sources'))
        # Exact bad retained reference from the old run; no old authority/state is replayed.
        content['hypotheses']=[]
        from edi.reason.contracts import InquiryTest
        fields=InquiryTest.model_fields
        bad={k:'Authored fixture' for k,v in fields.items() if v.is_required()}
        bad.update(test_id='fixture-test',kind='observation',status='proposed-unrun',
                   channels=['sources'],discriminates=['undeclared-hypothesis'])
        content['tests']=[bad]
        self.import_content(app,state,content)
        state2,req2=self.export(app)
        rejection=json.loads(req2['messages'][1]['content'][0]['text'])['prior_rejections'][0]
        self.assertEqual(rejection['receipt']['diagnostic'],'test references unknown hypothesis')
    def test_sole_reasoner_profile_rejects_teacher_cycle(self):
        from pydantic import ValidationError
        p=self.app().profile.model_dump(mode='json');p['teacher']['mode']='file-exchange'
        with self.assertRaises(ValidationError):ApplicationProfile.model_validate_json(canonical(p))
    def test_byte_capacity_is_not_an_exact_token_claim(self):
        app=self.app();state,req=self.export(app)
        row=app.investigation.phases.get('sole-run:inquiry:0:context-fit')
        result=json.loads(row['result'])
        self.assertIsNone(result['stage_headroom_tokens']);self.assertIsNone(result['trials'][0]['input_tokens'])
        self.assertEqual(result['policy'],'edi-external-session-byte-cut/1.0')
        self.assertEqual(app.reasoner.journal.get(state['job_id'])['attempts'],0)

if __name__=='__main__':unittest.main()
