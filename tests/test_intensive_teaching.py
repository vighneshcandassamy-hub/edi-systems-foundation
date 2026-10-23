"""One integrated teaching story plus recovery and memory counterexamples.

Every student/teacher response here is authored. This is engineering evidence,
not a live teaching result or a readiness qualification.
"""
import json
import os
import subprocess
from types import SimpleNamespace
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import test_information_seeking as fixtures
public, stop = fixtures.public, fixtures.stop
from edi.reason.contracts import StepRequest
from edi.shared.durable_io import canonical
from edi.shared.errors import EDIError


class IntensiveTeachingTests(unittest.TestCase):
    def setUp(self):
        # Composition, not inheritance: do not rerun the selective test suite.
        self.h = fixtures.InformationSeekingTests()
        self.h.setUp()

    def tearDown(self):
        self.h.tearDown()

    @staticmethod
    def critique(control, data):
        value = {'rationale_summary':'An information need can justify a permitted request. Compare available access with the unmet need.',
            'limitation':'Authored educational fixture; no measured model improvement', 'feedback_disposition':'retained-for-review'}
        if control['teaching']['stage']=='critique':
            value['procedural_guidance']=['When evidence is missing, distinguish an unsupported claim from an authorized request for that evidence.']
        return value

    @staticmethod
    def decision(control, data):
        if control['teaching']['stage']=='draft':
            return stop()  # A logically weak but well-formed proposal must reach teaching.
        operations = [x['operation'] for x in control['controller_progress']['public_outcomes']]
        if 'sources' not in operations:
            return public('sources')
        if 'read' not in operations:
            return public('read',document_id='m17')
        return public('submit',conclusion='Authored integration fixture only. Preserve attribution and unresolved next sample.')

    def open(self, **kwargs):
        return self.h.open(self.decision,teacher=True,teaching_mode='intensive',teacher_feedback=self.critique,**kwargs)

    def test_full_guided_acquire_read_submit_and_retained_history(self):
        loop=self.open()
        self.assertEqual(loop.step()['state'],'ready')
        first=self.h.calls[:4]
        self.assertEqual([c[1]['teaching']['stage'] for c in first],['independent','draft','critique','revision'])
        self.assertEqual(first[0][2]['prior_responses'],[])
        self.assertEqual(first[1][2]['prior_responses'],[])
        self.assertEqual(len(first[2][2]['prior_responses']),2)
        self.assertEqual(len(first[3][2]['prior_responses']),3)
        self.assertEqual(len({c[2]['context']['sha256'] for c in first}),1)
        self.assertTrue(all('available_access' in c[1]['teaching'] for c in first if c[0]=='teacher'))
        self.assertFalse(any(c[1].get('operation_argument_contracts') for c in first if c[0]=='teacher'))
        history=loop.runtime.reasoning.teaching_history()
        self.assertEqual(len(history),1)
        self.assertEqual(history[0]['status'],'provisional')
        self.assertTrue(history[0]['guidance'])
        # Reopen rather than carrying Python memory into the next turn.
        loop=self.open()
        self.assertEqual(loop.step()['state'],'ready')
        self.assertTrue(self.h.calls[4][2]['inquiry']['teaching_history'])
        self.assertEqual(loop.step()['state'],'completed')
        before=len(self.h.calls)
        self.assertEqual(self.open().step()['state'],'completed')
        self.assertEqual(len(self.h.calls),before)
        self.assertEqual(len(loop.runtime.reasoning.teaching_history()),3)
        episode=loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual([j.teaching_stage for j in episode.jobs],['independent','draft','critique','revision'])
        self.assertEqual(len(episode.responses),4)
        self.assertEqual(loop.state()['known_input_tokens'],1200)
        self.assertEqual(loop.state()['known_output_tokens'],600)

        # Exercise the production offline CLI, not only a Python-object reopen.
        from edi.inquiry.application import ApplicationProfile
        runtime=loop.runtime
        config={'application_id':'test','run_id':'run',
            'observation':runtime.profile.model_dump(mode='json'),
            'student':{'binding':self.h.binding.model_dump(mode='json')},
            'teacher':{'binding':self.h.teacher_binding.model_dump(mode='json'),'directory':str(self.h.root/'teacher-files')},
            'broker':{'grant':self.h.grant.model_dump(mode='json')},
            'reasoning':runtime.reasoning.profile.model_dump(mode='json'),
            'agency':runtime.agency.profile.model_dump(mode='json'),
            'workflow':runtime.workflow.profile.model_dump(mode='json'),
            'max_turns':5,'max_tokens':393216,'session_seconds':3600,'max_corrections':1,'teaching_mode':'intensive'}
        profile=ApplicationProfile.model_validate_json(canonical(config))
        (self.h.root/'application.json').write_text(profile.model_dump_json(),encoding='utf-8')
        # Construct every owner before recording the quiescent snapshot.
        runtime.world;runtime.interpretation;runtime.analysis;runtime.assessment
        source_root=Path(__file__).resolve().parents[1]
        example_root=source_root/'examples/autonomous' if (source_root/'examples/autonomous').exists() else source_root
        with patch.dict(os.environ,{'EDI_AUTONOMOUS_ROOT':str(self.h.root),'EDI_AUTONOMOUS_RUN_ID':'run','EDI_AUTONOMOUS_WORKSPACE':'test'}):
            spec=importlib.util.spec_from_file_location('teaching_snapshot_fixture',example_root/'run.py')
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            baseline=module.snapshot(SimpleNamespace(runtime=runtime,investigation=loop))
            (self.h.root/'restart-baseline.json').write_text(canonical(baseline),encoding='utf-8')
            proc=subprocess.run([sys.executable,str(example_root/'offline_restart.py'),'--run-root',str(self.h.root)],
                capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONPATH':str(source_root/'src')})
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        audit=json.loads((self.h.root/'offline-restart-audit.json').read_bytes())
        self.assertTrue(audit['passed'])
        self.assertEqual(audit['new_model_dispatches'],0)
        self.assertEqual(audit['new_broker_requests'],0)


    def test_file_teacher_and_student_can_be_pending_independently_and_resume(self):
        loop=self.open(file_teacher=True)
        state=loop.step()
        self.assertEqual(state['state'],'waiting-teacher')
        episode=loop.runtime.reasoning.get('run:inquiry:0')
        self.assertEqual([j.status for j in episode.jobs],['awaiting-import','completed'])
        self.assertEqual([c[1]['teaching']['stage'] for c in self.h.calls],['draft'])
        request=json.loads(Path(state['request_path']).read_bytes())
        self.assertEqual(json.loads(request['messages'][1]['content'][0]['text'])['prior_responses'],[])
        for expected_stage in ('independent','critique'):
            self.assertEqual(request['job']['teaching_stage'],expected_stage)
            feedback=self.critique({'teaching':{'stage':expected_stage}}, {})
            # Unknown usage remains unknown and is charged at its full reservation.
            path=self.h.root/(expected_stage+'.json');path.write_text(canonical(feedback),encoding='utf-8')
            loop.teacher.import_feedback(state['job_id'],path)
            loop=self.open(file_teacher=True)
            state=loop.step()
            if expected_stage=='independent':
                self.assertEqual(state['state'],'waiting-teacher')
                request=json.loads(Path(state['request_path']).read_bytes())
                self.assertEqual(len(json.loads(request['messages'][1]['content'][0]['text'])['prior_responses']),2)
        self.assertEqual(state['state'],'ready')
        self.assertEqual([c[1]['teaching']['stage'] for c in self.h.calls],['draft','revision'])
        self.assertEqual([x['operation'] for x in state['public_outcomes']],['mission','sources'])
        self.assertEqual(state['usage_unknown_jobs'],2)
        self.assertEqual(state['used_tokens'],32768+300)

    def test_provisional_teaching_survives_a_separate_controller_investigation(self):
        loop=self.open();loop.step()
        # A new C0 journal shares the native workspace/evidence and C4 memory.
        next_loop=self.open(workflow_name='next.workflows.sqlite3',run_id='next-run')
        state=next_loop.state();request=next_loop._inquiry(state,'next-run:inquiry:0')
        self.assertTrue(request.request.teaching_history)
        self.assertEqual(request.request.teaching_history[0]['status'],'provisional')
        self.assertEqual(request.request.teaching_history[0]['inquiry_id'],'run:inquiry:0')

    def test_reduced_assistance_can_recall_memory_while_clean_baseline_omits_it(self):
        loop=self.open();loop.step()
        learner=self.h.open(lambda *_: public('sources'),teacher=False,workflow_name='learner.workflows.sqlite3',
            run_id='learner',use_teaching_memory=True)
        state=learner.state();episode=learner._inquiry(state,'learner:inquiry:0')
        self.assertTrue(episode.request.teaching_history)
        self.assertFalse(episode.request.controller_progress.teacher_available)
        baseline=self.h.open(lambda *_: public('sources'),teacher=False,workflow_name='baseline.workflows.sqlite3',run_id='baseline')
        clean=baseline._inquiry(baseline.state(),'baseline:inquiry:0')
        self.assertEqual(clean.request.teaching_history,())

    def test_teacher_outage_never_silently_downgrades_to_unguided_execution(self):
        loop=self.open(file_teacher=True)
        first=loop.step();again=self.open(file_teacher=True).step()
        self.assertEqual(first['state'],'waiting-teacher')
        self.assertEqual(again['state'],'waiting-teacher')
        self.assertEqual(len(self.h.calls),1)
        self.assertEqual(len(json.loads((self.h.root/'world-session.json').read_bytes())['requests']),1)


if __name__=='__main__':
    unittest.main()
