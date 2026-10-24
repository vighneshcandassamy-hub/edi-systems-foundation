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
                # Explicitly retained defective draft before a distinct-source correction.
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
        self.assertTrue(any('pinned evidence cut' in x for x in rejected))
        self.assertTrue(any('repeat_reason' in x for x in rejected))
        self.assertTrue(any('feedback_response' in x for x in rejected))
        requests=json.loads((self.root/'world-session.json').read_text())['requests']
        operations=[x['operation'] for x in requests]
        self.assertEqual(operations,['mission','sources','read','read','ask','submit'])
        self.assertEqual([x.get('body',{}).get('document_id') for x in requests if x['operation']=='read'],['m17','r22'])
        for role,control,data in self.calls:
            stage=control['teaching']['stage']
            if stage in ('draft','independent'):self.assertEqual(data['prior_responses'],[])
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


if __name__=='__main__':unittest.main()
