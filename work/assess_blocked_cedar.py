import hashlib,json,sqlite3
from pathlib import Path
root=Path(r'C:\workspace\edi-cedar-input-cap-20261024\53d2c145d033\extracted')
def db(n):return sqlite3.connect((root/n).as_uri()+'?mode=ro',uri=True)
state=json.loads((root/'latest-state.json').read_bytes())
with db('owners.reason.sqlite3') as c:
 eps=[json.loads(x[0]) for x in c.execute('select document from episodes')];eps.sort(key=lambda e:int(e['request']['inquiry_id'].rsplit(':',1)[-1]))
 calls=[(json.loads(q),json.loads(r) if r else None,a,s) for q,r,a,s in c.execute('select request,result,attempts,state from io_inference_c4 order by rowid')]
with db('owners.sqlite3') as c:
 wires={}
 for q,r,a,s in calls:
  raw=b''.join(bytes(x[0]) for x in c.execute('select payload from payload_chunks where record_id=? order by ordinal',(r['raw_record_id'],)))
  wire=json.loads(raw);content=json.loads(wire['choices'][0]['message']['content'])
  wires[q['job']['job_id']]={'input_tokens':r.get('input_tokens'),'output_tokens':r.get('output_tokens'),'wire_sha256':hashlib.sha256(raw).hexdigest(),'operation_proposals':content.get('operation_proposals'),'decision_basis':content.get('decision_basis')}
 rid=eps[-1]['context']['evidence'][-1]['reference']['record_id'];raw=b''.join(bytes(x[0]) for x in c.execute('select payload from payload_chunks where record_id=? order by ordinal',(rid,)));rv=json.loads(raw)
 selection={'record_id':rid,'raw_bytes':len(raw),'selected_bytes':8192,'selector':eps[-1]['context']['evidence'][-1]['reference']['selector'],'encoded_asset_characters':len(rv['asset']['data']),'body_offset':raw.find(b'"body"'),'body_characters':len(rv['body']),'selection_contains_partial_readable_body':True,'limitation':'Selection is a prefix of JSON, containing all encoded asset and only part of readable CSV; no student response to this cut occurred.'}
cycles=[]
for e in eps:
 stages=[]
 for j in e['jobs']:
  r=next((r for r in e['responses'] if r['job_id']==j['job_id']),None);reject=next((r for r in e['rejections'] if r['job_id']==j['job_id']),None)
  stage={k:j.get(k) for k in ('job_id','role','teaching_stage','status')}
  stage['decision_basis']=r.get('decision_basis') if r else None;stage['rationale_summary']=r.get('rationale_summary') if r else None;stage['limitation']=r.get('limitation') if r else None
  stage['operation_proposals']=r.get('operation_proposals') if r else None;stage['rejection_diagnostic']=reject.get('diagnostic') if reject else None
  if j['job_id'] in wires:stage['provider_wire']=wires[j['job_id']]
  stages.append(stage)
 cycles.append({'inquiry_id':e['request']['inquiry_id'],'context_sha256':e['context']['sha256'],'stages':stages,'formal_hypotheses':sum(len(r['hypotheses']) for r in e['responses']),'formal_tests':sum(len(r['tests']) for r in e['responses']),'formal_candidates':sum(len(r['candidates']) for r in e['responses'])})
with db('cedar-world/run.sqlite') as c: ops=[o for o, in c.execute('select operation from events order by rowid')]
report={'scope':'Read-only assessment of blocked nonterminal checkpoint; no inference, world action or official evaluation. Reported rationale is fallible generated text.','checkpoint_sha256':'53d2c145d033e9fcfe0d775efd1bf5fc647be00e221b67104abe46308e45ac34','runtime_source':'3d23e23663680cfcd1816df25fc8fa5135ae4ff6','state':{k:v for k,v in state.items() if k not in ('evidence','artifact_frontier','mission','last_public_result')},'controller_terminal_present':False,'student_provider_calls':len(calls),'provider_dispatch_attempts':sum(a for q,r,a,s in calls),'input_tokens':sum(v['input_tokens'] for v in wires.values()),'output_tokens':sum(v['output_tokens'] for v in wires.values()),'blocked_job_has_no_provider_journal_row':state['job_id'] not in wires,'completed_teacher_responses':sum(j['role']=='teacher' and j['status']=='completed' for e in eps for j in e['jobs']),'public_operations':ops,'selection_diagnosis':selection,'cycles':cycles,'limitations':['No final scientific submission or benchmark score.','No C3 model, C5 analysis or C6 assessment confirmed in this prefix.','Unknown teacher token usage; policy reservations are not measured compute, money or energy.','No weight updates, matched comparison, independent teacher isolation or transfer result.','GPU shutdown remains unverified.']}
p=Path('docs/implementation/evidence/cedar-blocked-20261024');p.mkdir(parents=True,exist_ok=True)
(p/'assessment.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('student_provider_calls','provider_dispatch_attempts','input_tokens','output_tokens','blocked_job_has_no_provider_journal_row','completed_teacher_responses','public_operations','selection_diagnosis')},indent=2))
