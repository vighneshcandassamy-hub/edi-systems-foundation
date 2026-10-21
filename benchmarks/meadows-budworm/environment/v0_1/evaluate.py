"""Operator-only final scoring; no feedback endpoint is exposed to participants."""
import argparse
import json
import sqlite3
from pathlib import Path

def evaluate(environment,run):
    truth=sqlite3.connect((environment/'evaluator/evaluator.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
    audit=sqlite3.connect((run/'audit.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
    final=audit.execute('SELECT payload_json FROM final_submission WHERE id=1').fetchone()
    if final is None:raise ValueError('No final submission; no policy quality can be scored.')
    final=json.loads(final[0]);outcomes={k:json.loads(v) for k,v in truth.execute('SELECT policy,payload FROM policy_outcomes')};outcome=outcomes[final['policy']]
    requests=[];admitted=set()
    for operation,value,n,elapsed in audit.execute('SELECT operation,response_json,returned_bytes,elapsed_seconds FROM events ORDER BY rowid'):
        value=json.loads(value)
        if operation=='request':
            label=truth.execute('SELECT class,reason FROM labels WHERE item_id=?',(value['item_id'],)).fetchone()
            requests.append({'item_id':value['item_id'],'diagnostic_class':label[0],'bytes':n,'broker_seconds':elapsed});admitted.add(value['item_id'])
    counts={}
    for r in requests:counts[r['diagnostic_class']]=counts.get(r['diagnostic_class'],0)+1
    bytes_total=audit.execute('SELECT coalesce(sum(returned_bytes),0) FROM events').fetchone()[0]
    attempts,transport_bytes,failed_attempts=audit.execute('SELECT count(*),coalesce(sum(returned_bytes),0),coalesce(sum(status>=400),0) FROM http_attempts').fetchone()
    result={'status':'development_submission_scored','chosen_policy':final['policy'],'outcome':outcome,
            'regret_against_five_declared_options':outcome['objective']-min(x['objective'] for x in outcomes.values()),
            'next_year_forecast_absolute_error':abs(final['predicted_next_year_mean_insects']-outcome['next_year_mean_insects']),
            'distinct_requested_items':len(admitted),'diagnostic_request_classes':counts,'unique_event_payload_bytes':bytes_total,
            'http_attempts_including_retries_and_failures':attempts,'transport_returned_bytes':transport_bytes,'failed_http_attempts':failed_attempts,
            'initial_snapshot_bytes':(environment/'participant/initial.sqlite').stat().st_size,
            'relevance_labels_used_as_reward':False,'token_energy_or_model_latency_measured':False,
            'limit':'One constructed development scenario; no claim of an optimal policy, calibrated ecology or EDI advantage.'}
    truth.close();audit.close();return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--environment',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path);a=p.parse_args();result=evaluate(a.environment,a.run)
    if a.out:a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
