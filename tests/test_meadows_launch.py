"""Authored native Cedar connection, unchanged frozen broker, zero inference."""
import json
from pathlib import Path
import unittest
from edi.shared.durable_io import canonical,digest
from edi.shared.errors import EDIError
import test_information_seeking as fixtures
public=fixtures.public
import test_decision_grounding as decisions
import meadows_world

class MeadowsLaunchTests(unittest.TestCase):
    def setUp(self):
        self.h=fixtures.InformationSeekingTests();self.h.setUp()
    def tearDown(self):self.h.tearDown()
    def test_frozen_mission_separate_manual_native_inquiry_and_closure(self):
        module=meadows_world.load_broker()
        broker=module.Broker(meadows_world.ENV/'fixture',self.h.root/'cedar-world',meadows_world.restore_corpus())
        original=canonical(meadows_world.MISSION)
        self.h.grant=self.h.grant.model_copy(update={'mission_sha256':digest(meadows_world.MISSION),
            'operations':tuple(meadows_world.PUBLIC_OPERATIONS),'public_operations':meadows_world.PUBLIC_OPERATIONS})
        choices=[public('sources'),public('people'),public('submit',conclusion='Authored connection check only. No investigation or ecological conclusion.')]
        def choose(control,data):return choices[data['inquiry']['controller_progress']['turn']]
        def transport(url,body,headers):
            try:return 200,canonical(broker.dispatch(url.rsplit('/',1)[-1],body)).encode()
            except module.Invalid as exc:return exc.status,canonical({'status':'error','code':exc.code,'message':exc.message}).encode()
        loop=self.h.open(choose,teacher=True,teaching_mode='intensive',controller_policy='information-seeking/1.1',decision_basis=decisions.DecisionGroundingTests.ordinary_basis)
        loop.connector.transport=transport
        for i in range(3):state=loop.step()
        self.assertEqual(state['state'],'completed')
        self.assertEqual(canonical(state['mission']),original)
        self.assertNotIn('public_operations',state['mission'])
        ep=loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual(set(ep.request.controller_access.operations),set(self.h.grant.operations))
        self.assertIn('document_id',ep.request.controller_access.operations['read']['required_body_fields'])
        self.assertIn('Cedar District',ep.context.evidence[0].excerpt)
        audit=meadows_world.broker_snapshot(self.h.root)
        self.assertEqual([r['operation'] for r in audit['requests']],['mission','sources','people','submit'])
        self.assertEqual(len(audit['conclusions']),1)
        report=meadows_world.evaluate_closed(self.h.root)
        self.assertEqual(report['years_elapsed'],0)
        self.assertEqual(report['logical_operations']['submit'],1)
        self.assertFalse(report['model_tokens_energy_and_reasoning_latency_measured'])
        # Public descriptions cannot grant a private/undeclared operation.
        bad=self.h.grant.model_dump(mode='json');bad['public_operations']['private-state']={}
        with self.assertRaises(ValueError):type(self.h.grant).model_validate(bad)
        # Embedded mission catalogues remain authoritative when present.
        from edi.inquiry.benchmark import describe_access
        mission={'objective':'fixture','public_operations':{'mission':{'body':{}}}}
        g=self.h.grant.model_copy(update={'mission_sha256':digest(mission)})
        self.assertEqual(set(describe_access(mission,g).operations),{'mission'})

if __name__=='__main__':unittest.main()
