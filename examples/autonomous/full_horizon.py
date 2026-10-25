"""Full-horizon authored transport case, no model inference or Cedar observations."""
from pathlib import Path
import json,os,secrets,sqlite3,sys
from datetime import timedelta
from hashlib import sha256
from edi.inquiry.application import ApplicationProfile,IntegratedApplication
from edi.reason.contracts import ModelBinding
from edi.shared.contracts import utc_now
from edi.shared.durable_io import canonical,digest,CallJournal
from edi.shared.errors import EDIError
from neutral_world import MISSION,start_world

def run(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=False);token=secrets.token_urlsafe(32);os.environ['EDI_BROKER_TOKEN']=token
 server=start_world(out,token,port=8097);now=utc_now();identity='full-horizon-neutral'
 binding=ModelBinding(model_id='authored-lifecycle-fixture',revision='1',provider='authored',engine='no-model',tokenizer_revision='unmeasured')
 profile=ApplicationProfile.model_validate_json(canonical({'application_id':identity,'run_id':identity,
  'observation':{'database':str(out/'owners.sqlite3'),'workspace_id':identity},
  'student':{'mode':'file-exchange','binding':binding,'directory':str(out/'exchange'),'attribution':'Authored lifecycle fixture; no model or scientific result'},
  'teacher':{'mode':'disabled','binding':ModelBinding()},
  'agency':{'database':str(out/'owners.agency.sqlite3'),'workspace_id':identity,'operator_ids':['engineering-operator']},
  'broker':{'grant':{'grant_id':identity,'session_id':identity,'workspace_id':identity,'endpoint':'http://127.0.0.1:8097',
   'token_sha256':sha256(token.encode()).hexdigest(),'mission_sha256':digest(MISSION),'operator_id':'engineering-operator',
   'not_before':(now-timedelta(seconds=1)).isoformat(),'expires_at':(now+timedelta(hours=6)).isoformat(),
   'operations':list(MISSION['public_operations']),'public_operations':MISSION['public_operations'],'maximum_requests':256}},
  'max_turns':64,'max_tokens':2097152,'session_seconds':21600}))
 (out/'application.json').write_text(profile.model_dump_json(indent=2))
 def events():return json.loads((out/'world-session.json').read_bytes())['requests']
 app=IntegratedApplication(profile);reopens=[];peak=0
 conclusion=('Authored full-horizon report. Observations: register entries 8,12,16 at ordinal labels. '
  'Hypotheses: an arithmetic continuation is possible; neither mechanism nor elapsed-time trend is identified. '
  'Rivals: transcribed sequence, sampling or instrument process. No independent repeat measured. '
  'Recommendations: measure timed independent repetitions and retain calibration before causal claims. '
  'Prediction:20 only conditionally on arithmetic continuation. Uncertainty and further checks remain.\n')*25
 try:
  for i in range(64):
   state=app.step();assert state['state']=='waiting-reasoner',(i,state)
   request=json.loads(Path(state['request_path']).read_bytes());peak=max(peak,Path(state['request_path']).stat().st_size)
   data=json.loads(request['messages'][1]['content'][0]['text'])
   assert data['inquiry']['controller_progress']['final_submission_due']==(i>=62)
   if i%8==0:
    before=events();app=IntegratedApplication(profile);assert app.step()==state and events()==before;reopens.append(i)
   if i==0:op={'operation':'world-call','arguments':{'operation':'sources','body':{}}}
   elif i in (1,2):op={'operation':'acquire-asset','arguments':{'document_id':'m17' if i==1 else 'r22'}}
   elif i==3:op={'operation':'world-call','arguments':{'operation':'ask','body':{'person_id':'capture-operator','question':'What timing, independent repeats and mechanism were recorded?'}}}
   elif i==63:op={'operation':'world-call','arguments':{'operation':'submit','body':{'conclusion':conclusion}}}
   else:op={'operation':'world-call','arguments':{'operation':'status','body':{}}}
   content={'rationale_summary':'Authored full-horizon resource/closure check, no model inference.',
    'limitation':'Transport fixture only; repeated status is intentional load, not a reasoning strategy.',
    'decision_basis':{'evidence_record_ids':[e['reference']['record_id'] for e in data['context']['evidence']],
     'understanding':'Use exact acquired fixture records.','information_need':'Full-horizon persistence and closure.',
     'expected_use':'Preserve and verify the final report at the last decision slot.'},'operation_proposals':[op]}
   p=out/('input-'+str(i)+'.json');p.write_text(canonical(content));app.import_reasoner(state['job_id'],p)
   state=app.step();assert state['state']==('completed' if i==63 else 'ready'),(i,state)
   if i%16==15:print('FULL_HORIZON_PROGRESS',i+1,flush=True)
  before=events();assert IntegratedApplication(profile).step()==state and events()==before
  assert state['turn']==64 and state['usage_unknown_jobs']==64 and state['used_tokens']==1048576
  ledger=json.loads((out/'world-session.json').read_bytes());assert ledger['conclusions']==[conclusion]
  integrity={}
  for p in out.glob('*.sqlite3'):
   with sqlite3.connect(p) as db:integrity[p.name]=db.execute('pragma integrity_check').fetchone()[0]
  assert all(v=='ok' for v in integrity.values())
  with sqlite3.connect(app.runtime.workflow.profile.database) as db:
   counts={t:dict(zip(('rows','reserved_bytes'),db.execute('select count(*),sum(bytes) from '+t).fetchone())) for t in ['io_investigation_c0','io_investigation_phases_c0']}
  assert counts['io_investigation_phases_c0']['reserved_bytes']>256*1024**2
  assert counts['io_investigation_c0']['reserved_bytes']>256*1024**2
  # The historical fixed allowance reproduces exhaustion without any model/broker work.
  old=CallJournal(out/'negative-control.sqlite3','historical',max_calls=196,max_bytes=256*1024**2)
  admitted=0
  try:
   for j in range(128):old.begin(str(j),{'fixture':j},reserve_bytes=4*1024**2);old.finish(str(j),{});admitted+=1
  except EDIError:pass
  assert admitted==63
  report={'passed':True,'scope':'Authored neutral64-decision lifecycle; no model or Cedar science',
   'accepted_responses':64,'native_rejections':0,'completed':state['state']=='completed','report_preserved_exact':True,
   'report_chars':len(conclusion),'pending_reopens':reopens,'terminal_reopen_new_calls':0,'request_peak_bytes':peak,
   'journals':counts,'historical_fixed_budget_admitted':admitted,'integrity':integrity,'source_frozen':True}
  (out/'full-horizon-result.json').write_text(json.dumps(report,indent=2));print('FULL_HORIZON_RESULT',json.dumps(report),flush=True)
 finally:server.shutdown();server.server_close()

if __name__=='__main__':run(sys.argv[1])
