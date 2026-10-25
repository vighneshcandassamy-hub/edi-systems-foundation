"""Manual sole-assistant Cedar session. Importing this module starts no run."""
import base64
from datetime import timedelta
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import sqlite3
import uuid

BOUNDS={'max_turns':64,'max_tokens':2097152,'session_seconds':21600,'max_corrections':1,'maximum_requests':256}

def verify_source(source):
    source=Path(source).resolve();manifest=json.loads((source/'source-manifest.json').read_bytes())
    for name,expected in manifest['files'].items():
        p=Path(name)
        if p.is_absolute() or '..' in p.parts:raise ValueError('Unsafe manifest path')
        if sha256((source/p).read_bytes()).hexdigest()!=expected:raise ValueError('Source/input changed: '+name)
    return manifest

class CedarSession:
    def __init__(self,source,out,*,token=None):
        self.source=Path(source).resolve();self.out=Path(out).resolve()
        self.token=token or __import__('secrets').token_urlsafe(32)
        self.broker=None;self.app=None
    def profile(self):
        from edi.inquiry.application import ApplicationProfile
        from edi.reason.contracts import ModelBinding
        from edi.shared.contracts import utc_now
        from edi.shared.durable_io import canonical,digest
        import meadows_world
        path=self.out/'application.json'
        if path.exists():return ApplicationProfile.load(path)
        now=utc_now();identity=self.out.name
        binding=ModelBinding(model_id='ChatGPT-current-assistant-session',revision='operator-declared-20261025',
            provider='explicit-session-file-exchange',engine='current-session-unverified',tokenizer_revision='unmeasured')
        data={'application_id':identity,'run_id':identity,
            'observation':{'workspace_id':identity,'database':str(self.out/'owners.sqlite3')},
            'student':{'mode':'file-exchange','binding':binding.model_dump(mode='json'),
                'directory':str(self.out/'reasoner-exchange'),'max_images':1,'max_request_bytes':262144,
                'attribution':'Current assistant sole C4 reasoner; explicit manual handoff; implementation/case context known; identity and usage unverified'},
            'teacher':{'mode':'disabled','binding':ModelBinding().model_dump(mode='json')},
            'agency':{'workspace_id':identity,'database':str(self.out/'owners.agency.sqlite3'),'operator_ids':['engineering-operator']},
            'broker':{'grant':{'grant_id':identity,'session_id':identity,'workspace_id':identity,
                'endpoint':'http://127.0.0.1:8098','token_sha256':sha256(self.token.encode()).hexdigest(),
                'mission_sha256':digest(meadows_world.MISSION),'public_operations':meadows_world.PUBLIC_OPERATIONS,
                'operator_id':'engineering-operator','not_before':(now-timedelta(seconds=1)).isoformat(),
                'expires_at':(now+timedelta(seconds=BOUNDS['session_seconds']+1800)).isoformat(),
                'operations':list(meadows_world.PUBLIC_OPERATIONS),'maximum_requests':BOUNDS['maximum_requests']}},
            'teaching_mode':'selective','use_teaching_memory':False,
            **{k:v for k,v in BOUNDS.items() if k!='maximum_requests'}}
        result=ApplicationProfile.model_validate_json(canonical(data))
        with path.open('x',encoding='utf-8') as f:f.write(result.model_dump_json(indent=2))
        return result
    def open(self,*,scope):
        verify_source(self.source)
        self.out.mkdir(parents=True,exist_ok=False)
        (self.out/'source-manifest.json').write_bytes((self.source/'source-manifest.json').read_bytes())
        (self.out/'world-selection.json').write_text(json.dumps({'kind':'cedar','scope':scope}))
        os.environ['EDI_BROKER_TOKEN']=self.token
        import meadows_world
        from edi.inquiry.application import IntegratedApplication
        profile=self.profile()
        self.broker=meadows_world.start_world(self.out,self.token)
        self.app=IntegratedApplication(profile)
        return self.step()
    def step(self):
        state=self.app.step()
        if state['state']=='ready':
            self.save('last-operation-state.json',state)
            state=self.app.step()
        self.save('latest-state.json',state)
        return state
    def save(self,name,value):
        (self.out/name).write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8')
    def pending(self):
        state=json.loads((self.out/'latest-state.json').read_bytes())
        if state['state']!='waiting-reasoner':raise ValueError('No pending sole-reasoner request')
        request=json.loads(Path(state['request_path']).read_bytes())
        if request['job']['job_id']!=state['job_id']:raise ValueError('Pending identity differs')
        return state,request
    def import_response(self,job_id,content):
        state,_=self.pending()
        if job_id!=state['job_id']:raise ValueError('Stale/wrong job; no input file created')
        if not isinstance(content,dict):raise TypeError('Proposal must be JSON object; no input file created')
        raw=json.dumps(content,allow_nan=False).encode('utf-8')
        if len(raw)>65536:raise ValueError('Response exceeds native byte budget')
        path=self.out/('reasoner-response-'+job_id+'.json')
        with path.open('xb') as f:f.write(raw)
        from edi.reason.exchange import ModelOutputRejected
        try:
            receipt=self.app.import_reasoner(job_id,path)
            self.save('reasoner-import-'+job_id+'.json',receipt)
        except ModelOutputRejected as exc:
            self.save('reasoner-rejection-'+job_id+'.json',{'error':str(exc),'native_original_retained':True})
        # Native bounded correction may export a new job; never generates a response.
        return self.step()
    def handoff(self):
        runpy.run_path(str(self.source/'checkpoint.py'))['display_checkpoint'](self.out,self.source)
        state=json.loads((self.out/'latest-state.json').read_bytes())
        if state['state']=='waiting-reasoner':
            _,request=self.pending()
            print('EDI_REASONER_REQUEST',json.dumps(request,separators=(',',':')),flush=True)
            from IPython.display import Image,display
            for part in request['messages'][1]['content']:
                if part['type']=='image_url':
                    display(Image(data=base64.b64decode(part['image_url']['url'].split(',',1)[1],validate=True)))
        print('CEDAR_SESSION_STATE',json.dumps({k:v for k,v in state.items() if k not in ('mission','evidence','artifact_frontier')}),flush=True)
    def reopen(self):
        from edi.inquiry.application import IntegratedApplication
        os.environ['EDI_BROKER_TOKEN']=self.token
        self.app=IntegratedApplication(self.profile())
        return self.step()
    def stop(self):
        if self.broker is not None:
            self.broker.shutdown();self.broker.server_close();self.broker=None
        self.save('shutdown.json',{'broker_stopped':True,'teacher_started':False,'qwen_started':False})
    def finalize(self):
        state=json.loads((self.out/'latest-state.json').read_bytes())
        if state['state'] not in ('completed','yielded'):raise ValueError('Evaluator unavailable before native termination')
        verify_source(self.source)
        import meadows_world
        report=meadows_world.evaluate_closed(self.out)
        self.save('post-terminal-evaluation.json',{'controller_state':state['state'],'official_outcome':report,
            'scope':'Unblinded operator-assisted development assessment; no comparative advantage claim'})
        self.stop();self.handoff()
        return report

class NotebookCedar(CedarSession):
    """Broker in notebook; all native EDI calls in the pinned CPU Python process."""
    def __init__(self,source,out,python,*,token=None):
        super().__init__(source,out,token=token);self.python=str(python)
    def _native(self,stage,job=None,content=None):
        import subprocess
        env=dict(os.environ,EDI_BROKER_TOKEN=self.token,EDI_MEADOWS_ROOT=str(self.source/'meadows'),
                 PYTHONPATH=str(self.source/'src'))
        command=[self.python,str(self.source/'cedar_session.py'),stage,str(self.source),str(self.out)]
        if job is not None:command.append(job)
        result=subprocess.run(command,input=json.dumps(content,allow_nan=False) if content is not None else '',
            env=env,cwd=self.source,text=True,capture_output=True,timeout=120)
        if result.returncode:
            self.save('native-failure-'+uuid.uuid4().hex+'.json',{'stage':stage,'stdout':result.stdout,'stderr':result.stderr,'no_automatic_retry':True})
            raise RuntimeError(result.stderr[-3000:] or result.stdout[-3000:])
        return json.loads((self.out/'latest-state.json').read_bytes())
    def open(self,*,scope):
        verify_source(self.source);self.out.mkdir(parents=True,exist_ok=False)
        (self.out/'source-manifest.json').write_bytes((self.source/'source-manifest.json').read_bytes())
        self.save('world-selection.json',{'kind':'cedar','scope':scope})
        os.environ['EDI_MEADOWS_ROOT']=str(self.source/'meadows')
        import meadows_world
        self.broker=meadows_world.start_world(self.out,self.token)
        return self.step()
    def step(self):return self._native('step')
    def reopen(self):return self.step()
    def import_response(self,job_id,content):
        state,_=self.pending()
        if job_id!=state['job_id']:raise ValueError('Stale/wrong job; no input file created')
        if not isinstance(content,dict):raise TypeError('Proposal must be JSON object; no input file created')
        if len(json.dumps(content,allow_nan=False).encode())>65536:raise ValueError('Response exceeds native byte budget')
        return self._native('import',job_id,content)
    def finalize(self):
        state=json.loads((self.out/'latest-state.json').read_bytes())
        if state['state'] not in ('completed','yielded'):raise ValueError('Evaluator unavailable before native termination')
        self._native('evaluate');self.stop();self.handoff()
        return json.loads((self.out/'post-terminal-evaluation.json').read_bytes())

# Override the simple in-process entry point with the verified notebook/CPU boundary.
def start_cedar(source,readiness_file,python):
    source=Path(source).resolve();verify_source(source)
    ready=json.loads(Path(readiness_file).read_bytes())
    if not ready.get('passed') or ready.get('benchmark_started'):raise ValueError('Wrong readiness scope')
    if ready['source_manifest_sha256']!=sha256((source/'source-manifest.json').read_bytes()).hexdigest():raise ValueError('Readiness/source differs')
    session=NotebookCedar(source,Path('/kaggle/working')/('cedar-sole-'+uuid.uuid4().hex[:12]),python)
    session.open(scope='Actual sole-current-assistant Cedar development assessment; new state; no teacher')
    session.handoff();return session

if __name__=='__main__':
    import sys
    stage,source,out=sys.argv[1:4]
    source=Path(source).resolve();sys.path[:0]=[str(source/'src'),str(source)]
    verify_source(source)
    os.environ['EDI_MEADOWS_ROOT']=str(source/'meadows')
    from edi.inquiry.application import IntegratedApplication
    session=CedarSession(source,out,token=os.environ['EDI_BROKER_TOKEN'])
    session.app=IntegratedApplication(session.profile())
    if stage=='step':session.step()
    elif stage=='import':session.import_response(sys.argv[4],json.loads(sys.stdin.read()))
    elif stage=='evaluate':
        state=json.loads((session.out/'latest-state.json').read_bytes())
        if state['state'] not in ('completed','yielded'):raise ValueError('Evaluator unavailable before native termination')
        import meadows_world
        session.save('post-terminal-evaluation.json',{'controller_state':state['state'],
            'official_outcome':meadows_world.evaluate_closed(session.out),
            'scope':'Unblinded operator-assisted development assessment; no comparative advantage claim'})
    else:raise ValueError('Unknown explicit native operation')
