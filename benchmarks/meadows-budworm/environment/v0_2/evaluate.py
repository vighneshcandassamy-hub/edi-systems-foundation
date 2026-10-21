"""Offline operator outcome report. No narrative-match reward or pretend global optimum."""
import argparse
import json
import sqlite3
from pathlib import Path


def evaluate(run):
    with sqlite3.connect((run/'run.sqlite').resolve().as_uri()+'?mode=ro',uri=True) as c:
        s=json.loads(c.execute('SELECT payload FROM state WHERE id=1').fetchone()[0])
        events=c.execute('SELECT operation,count(*) FROM events GROUP BY operation').fetchall()
        attempts=c.execute('SELECT count(*),sum(status>=400),sum(bytes),sum(seconds) FROM attempts').fetchone()
    outcomes=s['outcomes'];metrics=[m for x in outcomes for m in x['metrics']]
    return {'status':'constructed_development_outcomes','years_elapsed':s['year'],
        'mean_damage_fraction':sum(m['damage_fraction'] for m in metrics)/len(metrics) if metrics else None,
        'total_operational_spending':sum(x['spent'] for x in outcomes),
        'total_timber_delivery':sum(x['delivered'] for x in outcomes),
        'five_year_committed_delivery_shortfall':sum(max(0.,18-x['delivered']) for x in outcomes if x['year']<=5),
        'broad_treatment_dose_sum':sum(j.get('dose',0)*len(j['plots']) for j in s['jobs'] if j['status']=='executed' and j.get('method')=='broad'),
        'terminal_mean_foliage':sum(p['foliage'] for p in s['plots'])/len(s['plots']),
        'terminal_mean_enemy_index':sum(p['enemies'] for p in s['plots'])/len(s['plots']),
        'objective_proposals':s['proposals'],'final_report':s.get('final'),
        'logical_operations':dict(events),'http_attempts':attempts[0],'http_failures':attempts[1]or 0,
        'transport_bytes':attempts[2]or 0,'broker_service_seconds':attempts[3]or 0,
        'model_tokens_energy_and_reasoning_latency_measured':False,
        'limits':'Outcome vector only. No ecological fidelity, causal discovery, optimum policy, calibration, human preference validity or EDI advantage is established.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);a=p.parse_args()
    print(json.dumps(evaluate(a.run),indent=2))
