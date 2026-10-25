"""CPU-native EDI with one manually transported ChatGPT reasoner. No model server."""
from datetime import timedelta
from hashlib import sha256
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE_ROOT=ROOT if (ROOT/'src').exists() else ROOT.parents[1]
sys.path.insert(0,str(SOURCE_ROOT/'src'))
from edi.shared.contracts import utc_now
from edi.shared.durable_io import canonical,digest
from edi.reason.contracts import ModelBinding
from edi.inquiry.application import ApplicationProfile,IntegratedApplication
OUT=Path(os.environ['EDI_ASSISTANT_ROOT'])

def save(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2),encoding='utf-8')

def application():
    from active_world import MISSION,PUBLIC_OPERATIONS
    path=OUT/'application.json'
    if not path.exists():
        now=utc_now();identity=OUT.name;token=os.environ['EDI_BROKER_TOKEN']
        # Session identity is explicitly declared, never presented as provider authentication.
        binding=ModelBinding(model_id='ChatGPT-current-assistant-session',revision='operator-declared-20261025',
            provider='explicit-session-file-exchange',engine='current-session-unverified',tokenizer_revision='unmeasured')
        profile={'application_id':identity,'run_id':'assistant-'+identity,
            'observation':{'workspace_id':identity,'database':str(OUT/'owners.sqlite3')},
            'student':{'mode':'file-exchange','binding':binding.model_dump(mode='json'),
                'directory':str(OUT/'reasoner-exchange'),'max_images':1,
                'attribution':'Current ChatGPT assistant as sole C4 reasoner; manual transport; implementation context known; identity/usage not independently verified'},
            'teacher':{'mode':'disabled','binding':ModelBinding().model_dump(mode='json')},
            'agency':{'workspace_id':identity,'database':str(OUT/'owners.agency.sqlite3'),'operator_ids':['engineering-operator']},
            'broker':{'grant':{'grant_id':identity,'session_id':identity,'workspace_id':identity,
                'endpoint':'http://127.0.0.1:8098','token_sha256':sha256(token.encode()).hexdigest(),
                'mission_sha256':digest(MISSION),'public_operations':PUBLIC_OPERATIONS,
                'operator_id':'engineering-operator','not_before':(now-timedelta(seconds=1)).isoformat(),
                'expires_at':(now+timedelta(hours=2)).isoformat(),
                'operations':list(PUBLIC_OPERATIONS if PUBLIC_OPERATIONS is not None else MISSION['public_operations']),
                'maximum_requests':64}},
            'teaching_mode':'selective','use_teaching_memory':False,'max_turns':24,'max_tokens':786432,
            'session_seconds':3600,'max_corrections':1}
        parsed=ApplicationProfile.model_validate_json(canonical(profile))
        with path.open('x') as f:f.write(parsed.model_dump_json(indent=2))
    return IntegratedApplication(ApplicationProfile.load(path))

def run(stage,job=None,response_path=None):
    app=application()
    if stage=='import':
        current=json.loads((OUT/'latest-state.json').read_bytes())
        assert current['state']=='waiting-reasoner' and current['job_id']==job
        receipt=app.import_reasoner(job,Path(response_path));save('reasoner-import-'+job+'.json',receipt)
    state=app.step()
    if state['state']=='ready':
        save('last-operation-state.json',state)
        state=app.step()
    save('latest-state.json',state)
    return state

if __name__=='__main__':
    try:
        state=run(*sys.argv[1:])
        print('EDI_REASONER_STATE',canonical({k:v for k,v in state.items() if k not in ('mission','evidence','artifact_frontier')}),flush=True)
    except Exception as exc:
        import traceback
        save('assistant-process-failure-'+str(__import__('time').time_ns())+'.json',
             {'error_type':type(exc).__name__,'error':str(exc),'traceback':traceback.format_exc(),'no_automatic_retry':True})
        raise
