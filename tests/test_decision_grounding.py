"""One authored native mission for the revised decision contract; zero live models."""
import json
import unittest
from test_information_seeking import InformationSeekingTests, public
from edi.reason.contracts import OperationProposal
from edi.reason.decision import validate_decision_basis
from edi.reason.gateway import VllmBackend
from edi.shared.durable_io import canonical
from edi.shared.errors import EDIError


class DecisionGroundingTests(unittest.TestCase):
    setUp = InformationSeekingTests.setUp
    tearDown = InformationSeekingTests.tearDown
    open = InformationSeekingTests.open

    def test_native_grounded_mission_rejects_unsupported_basis_and_closes(self):
        def choose(control, data):
            turn = data['inquiry']['controller_progress']['turn']
            stage = control['teaching']['stage']
            if turn == 0: return public('sources')
            if turn == 1: return {'operation':'acquire-asset','arguments':{'document_id':'m17'}}
            if turn == 2:
                # Rejected draft must reach critique before a distinct-source revision.
                doc = 'm17' if stage == 'draft' and not data['prior_rejections'] else 'r22'
                return {'operation':'acquire-asset','arguments':{'document_id':doc}}
            if turn == 3:
                return public('ask',person_id='capture-operator',question='Are elapsed times, a mechanism, an independent repeat or an actual next reading available?')
            return public('submit',conclusion='The register shows 8,12,16 and +4 per ordered entry. A next value of 20 assumes continuation. The sources do not establish elapsed intervals, a physical mechanism, an independent repeat or a measured next reading. Those measurements would be needed for a verified forecast.')

        def basis(control, data, proposal):
            turn = data['inquiry']['controller_progress']['turn']
            stage = control['teaching']['stage']
            value={'evidence_record_ids':[e['reference']['record_id'] for e in data['context']['evidence']],
                'understanding':'Authored decision uses only this pinned cut; no autonomous reasoning claim.',
                'information_need':'Measurement procedure and prediction limits, or a supported final report.',
                'expected_use':'Use the returned content to update the report; source availability is not a promise of an answer.',
                'repeat_reason':None,'feedback_response':'The critique is considered; this authored fixture retains the independently selected operation.' if stage=='revision' else None}
            if turn==1 and stage=='draft' and not data['prior_rejections']:
                value['evidence_record_ids']=['outside-pinned-cut']
            if turn==3 and stage=='revision' and not data['prior_rejections']:
                value['feedback_response']=None
            return value

        loop=self.open(choose,teacher=True,teaching_mode='intensive',controller_policy='information-seeking/1.1',decision_basis=basis)
        states=[loop.step() for _ in range(5)]
        self.assertEqual(states[-1]['state'],'completed')
        self.assertEqual([x['state'] for x in states[:-1]],['ready']*4)
        rejected=[]
        for turn in range(5):
            ep=loop.runtime.reasoning.get('run:inquiry:'+str(turn))
            rejected.extend(x.diagnostic for x in ep.rejections)
        self.assertEqual(len(rejected),3)
        failed=loop.runtime.reasoning.get('run:inquiry:2')
        self.assertEqual([j.teaching_stage for j in failed.jobs],['independent','draft','critique','revision'])
        self.assertEqual([j.status for j in failed.jobs],['completed','rejected','completed','completed'])
        self.assertFalse(any(next(j for j in failed.jobs if j.job_id==r.job_id).teaching_stage=='draft' for r in failed.responses))
        memory=next(x for x in loop.runtime.reasoning.teaching_history() if x['inquiry_id']=='run:inquiry:2')
        self.assertEqual(memory['status'],'provisional')
        # Full memory retains rejected draft identity rather than fabricating a response.
        with __import__('sqlite3').connect(loop.runtime.reasoning.profile.database) as db:
            entries=[json.loads(x[0]) for x in db.execute('SELECT result FROM io_teaching_memory_c4 WHERE state=?',('completed',))]
        lesson=next(x for x in entries if x['inquiry_id']=='run:inquiry:2')
        self.assertIsNone(lesson['draft_response_id'])
        self.assertEqual(lesson['rejected_draft_records'][0]['raw_record_id'],failed.rejections[0].raw_record_id)
        self.assertTrue(any('pinned evidence cut' in x for x in rejected))
        self.assertTrue(any('repeat_reason' in x for x in rejected))
        self.assertTrue(any('feedback_response' in x for x in rejected))
        requests=json.loads((self.root/'world-session.json').read_text())['requests']
        operations=[x['operation'] for x in requests]
        self.assertEqual(operations,['mission','sources','read','read','ask','submit'])
        self.assertEqual([x.get('body',{}).get('document_id') for x in requests if x['operation']=='read'],['m17','r22'])
        for role,control,data in self.calls:
            stage=control['teaching']['stage']
            if stage in ('draft','independent'):
                self.assertEqual(data['prior_responses'],[])
                self.assertEqual(data['prior_rejections'],[])
            if data['inquiry']['controller_progress']['turn']==2 and stage in ('critique','revision'):
                self.assertEqual(len(data['prior_rejections']),1)
                rejected_view=data['prior_rejections'][0]
                self.assertEqual(rejected_view['teaching_stage'],'draft')
                self.assertIn('repeat_reason',rejected_view['receipt']['diagnostic'])
                self.assertIn('m17',rejected_view['unaccepted_generated_output_utf8'])
            self.assertEqual(data['decision_context']['acquired_sources'][0]['record_id'],data['context']['evidence'][0]['reference']['record_id'])
            if role=='student':self.assertNotIn('record_fields',control['response_fields'])
            else:self.assertIn('critique only',control['decision_protocol']['task'])
        # Same-source repeats remain possible for an explicit purpose; validation
        # never substitutes a different action or certifies that purpose as true.
        ep=loop.runtime.reasoning.get('run:inquiry:2')
        revision=next(r for r in ep.responses if next(j for j in ep.jobs if j.job_id==r.job_id).teaching_stage=='revision')
        job=next(j for j in ep.jobs if j.job_id==revision.job_id)
        repeated=revision.model_copy(update={'operation_proposals':(OperationProposal(operation='acquire-asset',arguments={'document_id':'m17'}),)})
        with self.assertRaises(EDIError):validate_decision_basis(ep,repeated,job)
        repeated=repeated.model_copy(update={'decision_basis':repeated.decision_basis.model_copy(update={'repeat_reason':'Check for an independently reported source update; freshness is not assumed.'})})
        validate_decision_basis(ep,repeated,job)
        # The real backend enforces the selected-record ID choices in decoding.
        role,control,data=next(x for x in self.calls if x[0]=='student')
        schema=VllmBackend('http://127.0.0.1:8008',self.binding.model_id).generation_schema_for([{'content':canonical(control)},{'content':[{'text':canonical(data)}]}])
        self.assertIn('decision_basis',schema['required'])
        self.assertEqual(schema['$defs']['DecisionBasis']['properties']['evidence_record_ids']['items']['enum'],[data['context']['evidence'][0]['reference']['record_id']])
        before=len(self.calls)
        reopened=self.open(lambda *args:self.fail('Completed mission must not redispatch'),teacher=True,teaching_mode='intensive',controller_policy='information-seeking/1.1',decision_basis=basis)
        self.assertEqual(reopened.step(),states[-1]);self.assertEqual(len(self.calls),before)


    @staticmethod
    def ordinary_basis(control,data,proposal):
        return {'evidence_record_ids':[e['reference']['record_id'] for e in data['context']['evidence']],
            'understanding':'Authored recovery fixture.', 'information_need':'A supported report.',
            'expected_use':'Update the report from returned observations.', 'repeat_reason':None,
            'feedback_response':'I checked the retained rejection and critique against this cut.' if control['teaching']['stage']=='revision' else None}

    def test_rejected_draft_file_teacher_resumes_without_replay_and_never_executes(self):
        from pathlib import Path
        def choose(control,data):
            turn=data['inquiry']['controller_progress']['turn']
            if turn==0 and control['teaching']['stage']=='draft':
                # Deliberately malformed operation is retained at the gateway.
                return {'operation':'world-call','arguments':{}}
            return public('sources') if turn==0 else public('submit',conclusion='Authored recovery fixture; no scientific outcome claim.')
        def reopen():
            return self.open(choose,teacher=True,file_teacher=True,teaching_mode='intensive',
                controller_policy='information-seeking/1.1',decision_basis=self.ordinary_basis)
        loop=reopen();state=loop.step()
        self.assertEqual(state['state'],'waiting-teacher')
        ep=loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual([j.status for j in ep.jobs],['awaiting-import','rejected'])
        self.assertEqual(len(self.calls),1)
        again=reopen().step();self.assertEqual(state,again);self.assertEqual(len(self.calls),1)
        req=json.loads(Path(state['request_path']).read_bytes())
        self.assertEqual(json.loads(req['messages'][1]['content'][0]['text'])['prior_rejections'],[])
        for stage in ('independent','critique'):
            feedback={'rationale_summary':'The request catalogue defines operation and body; repair the rejected envelope against that contract.',
                'limitation':'Authored teacher, not an observation.', 'feedback_disposition':'retained-for-review'}
            if stage=='critique':feedback['procedural_guidance']=['Check native diagnostics and repair a rejected proposal before requesting execution.']
            path=self.root/(stage+'.json');path.write_text(canonical(feedback),encoding='utf-8')
            loop=reopen();loop.teacher.import_feedback(state['job_id'],path)
            loop=reopen();state=loop.step()
            if stage=='independent':
                self.assertEqual(state['state'],'waiting-teacher')
                req=json.loads(Path(state['request_path']).read_bytes())
                data=json.loads(req['messages'][1]['content'][0]['text'])
                self.assertEqual(len(data['prior_rejections']),1)
                self.assertEqual(data['prior_rejections'][0]['teaching_stage'],'draft')
                self.assertEqual(len(data['prior_responses']),1)
                self.assertEqual(len(self.calls),1)
        self.assertEqual(state['state'],'ready')
        self.assertEqual(len(self.calls),2)
        self.assertEqual(state['known_input_tokens'],200)
        self.assertEqual(state['known_output_tokens'],100)
        self.assertEqual(state['usage_unknown_jobs'],2)
        requests=json.loads((self.root/'world-session.json').read_bytes())['requests']
        self.assertEqual([x['operation'] for x in requests],['mission','sources'])
        # The retained provisional lesson references the true admitted revision.
        self.assertEqual(len(loop.runtime.reasoning.teaching_history()),1)

    def test_invalid_revision_still_exhausts_bound_without_any_action(self):
        def basis(control,data,proposal):
            value=self.ordinary_basis(control,data,proposal)
            value['evidence_record_ids']=['outside-pinned-cut']
            return value
        loop=self.open(lambda *_:public('sources'),teacher=True,teaching_mode='intensive',
            controller_policy='information-seeking/1.1',decision_basis=basis)
        state=loop.step()
        self.assertEqual(state['state'],'yielded')
        self.assertIn('bounded output correction exhausted',state['stop_reason'])
        ep=loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual([j.teaching_stage for j in ep.jobs],['independent','draft','critique','revision','revision'])
        self.assertEqual(len(ep.rejections),3)
        self.assertEqual(len(ep.responses),2)
        self.assertEqual(len(loop.runtime.reasoning.teaching_history()),0)
        self.assertEqual([x['operation'] for x in json.loads((self.root/'world-session.json').read_bytes())['requests']],['mission'])
        self.assertEqual(state['known_input_tokens'],500)
        self.assertEqual(state['known_output_tokens'],250)
        before=len(self.calls)
        reopened=self.open(lambda *_:self.fail('Terminal failure must not redispatch'),teacher=True,teaching_mode='intensive',
            controller_policy='information-seeking/1.1',decision_basis=basis)
        self.assertEqual(reopened.step(),state);self.assertEqual(len(self.calls),before)



    def test_unknown_student_completion_never_becomes_a_reviewable_rejection(self):
        from edi.shared.errors import ErrorCode
        loop=self.open(lambda *_:public('sources'),teacher=True,teaching_mode='intensive',
            controller_policy='information-seeking/1.1',decision_basis=self.ordinary_basis)
        sent=[]
        def unresolved(messages,job):
            sent.append(job.job_id)
            raise EDIError(ErrorCode.UNAVAILABLE,'Authored provider loss after dispatch claim')
        loop.student.send=unresolved
        state=loop.step()
        self.assertEqual(state['state'],'uncertain-completion')
        self.assertEqual(len(sent),1)
        ep=loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual(len(ep.rejections),0)
        self.assertEqual([j.teaching_stage for j in ep.jobs],['independent','draft'])
        self.assertEqual(ep.jobs[-1].status,'awaiting-import')
        again=loop.step()
        self.assertEqual(again['state'],'uncertain-completion')
        self.assertEqual(len(sent),1)
        self.assertEqual(len(loop.runtime.reasoning.get('run:inquiry:0').rejections),0)



    def test_saved_live_draft_reaches_critique_then_admitted_revision(self):
        from pathlib import Path
        from hashlib import sha256
        fixture=json.loads((Path(__file__).parent/'fixtures/rejected_draft_20261024.json').read_bytes())
        self.assertEqual(sha256(fixture['raw_content'].encode()).hexdigest(),fixture['raw_content_sha256'])
        def choose(control,data):
            turn=data['inquiry']['controller_progress']['turn']
            return public('sources') if turn==0 else {'operation':'acquire-asset','arguments':{'document_id':'m17' if turn==1 else 'r22'}}
        def feedback(control,data):
            if data['inquiry']['controller_progress']['turn']==2 and control['teaching']['stage']=='critique':
                self.assertEqual(len(data['prior_rejections']),1)
                self.assertIn('repeat_reason',data['prior_rejections'][0]['receipt']['diagnostic'])
                self.assertIn('Acquiring the full instrument register',data['prior_rejections'][0]['unaccepted_generated_output_utf8'])
            return {'rationale_summary':'Check the configured complete source and its actual coverage. A reread requires a concrete missing-range or update purpose; otherwise investigate the unresolved procedure through available sources.',
                'limitation':'Authored recovery coach; no new observations.','feedback_disposition':'retained-for-review'}
        loop=self.open(choose,teacher=True,teaching_mode='intensive',controller_policy='information-seeking/1.1',
            decision_basis=self.ordinary_basis,teacher_feedback=feedback)
        original_send=loop.student.send
        replays=[]
        def send(messages,job):
            data=json.loads(messages[1]['content'][0]['text'])
            if data['inquiry']['controller_progress']['turn']==2 and job.teaching_stage=='draft':
                value=json.loads(fixture['raw_content'])
                register=next(e for e in data['context']['evidence'] if e['origin']['spec']['descriptor'].get('document_id')=='m17')
                value['decision_basis']['evidence_record_ids']=[register['reference']['record_id']]
                content=canonical(value);replays.append(content)
                return content.encode(),content,100,50
            return original_send(messages,job)
        send.generation_schema_for=original_send.generation_schema_for
        loop.student.send=send
        for _ in range(3):state=loop.step()
        self.assertEqual(state['state'],'ready')
        self.assertEqual(len(replays),1)
        ep=loop.runtime.reasoning.get('run:inquiry:2')
        self.assertEqual([j.status for j in ep.jobs],['completed','rejected','completed','completed'])
        self.assertEqual(len(ep.rejections),1)
        requests=json.loads((self.root/'world-session.json').read_bytes())['requests']
        self.assertEqual([x['body'].get('document_id') for x in requests if x['operation']=='read'],['m17','r22'])
        self.assertEqual(len(loop.runtime.reasoning.teaching_history()),3)


if __name__=='__main__':unittest.main()
