"""One focused engineering campaign. No human, EDI or LLM benchmark is run."""
import argparse
import base64
import gzip
import hashlib
import json
import math
import random
import secrets
import shutil
import sqlite3
import tempfile
import threading
import urllib.request
import urllib.error
from pathlib import Path
from broker import server
from evaluate import evaluate
from world import step,history,future,rollout,POLICIES

def verify(env):
    checks={};manifest=json.loads((env/'manifest.json').read_text())
    for item in manifest['databases']:
        p=env/item['path'];b=p.read_bytes()
        assert hashlib.sha256(b).hexdigest()==item['sha256']
        assert gzip.decompress(Path(str(p)+'.gz').read_bytes())==b
        with sqlite3.connect(p) as c:assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    checks['three_databases_and_gzip_snapshots_verified']=True
    initial=sqlite3.connect(env/'initial/initial.sqlite');invest=sqlite3.connect(env/'investigation/investigation.sqlite');truth=sqlite3.connect(env/'evaluator/evaluator.sqlite')
    assert initial.execute('SELECT count(*) FROM items').fetchone()[0]==manifest['build']['items']['initial']==30
    assert invest.execute('SELECT count(*) FROM items').fetchone()[0]==manifest['build']['items']['investigation']==129
    assert not initial.execute("SELECT 1 FROM sqlite_master WHERE name IN ('labels','history','policy_outcomes','private_meta')").fetchall()
    assert not invest.execute("SELECT 1 FROM sqlite_master WHERE name IN ('labels','history','policy_outcomes','private_meta')").fetchall()
    assert hashlib.sha256((env/'participant/initial.sqlite').read_bytes()).hexdigest()==manifest['databases'][0]['sha256']
    checks['participant_database_has_no_evaluator_tables']=True
    for (payload,) in invest.execute('SELECT payload_json FROM items'):
        rows=json.loads(payload)
        assert all(r.get('year',0)<=60 for r in rows)
    checks['no_future_rows_in_request_store']=True
    # Metadata and asset format do not carry an explicit relevant/noise label.
    for c in (initial,invest):
        for row in c.execute('SELECT scope_json,title,summary,asset FROM items'):
            scope=json.loads(row[0]);assert not {'class','relevance','noise','expected_answer','reason','channel'}&set(scope)
            assert all(x not in (row[1]+' '+row[2]).lower() for x in ('distractor','irrelevant','noise'))
    checks['explicit_relevance_labels_absent_from_public_items']=True
    groups=initial.execute('SELECT source_group,count(*) FROM items GROUP BY source_group HAVING count(*)>1').fetchall();assert len(groups)==7
    checks['duplicate_bulletins_share_original_source_groups']=True
    labelcounts=dict(truth.execute('SELECT class,count(*) FROM labels GROUP BY class'))
    assert labelcounts['independent_distractor']>=18 and labelcounts['scope_mismatch']>=18
    s={'insects':1.7,'foliage':.7,'mature_host':.8,'enemies':.5}
    assert step(s,1.,.8,.02,nuisance={'certification':0})==step(s,1.,.8,.02,nuisance={'certification':10000})
    checks['independent_distractor_has_zero_effect_on_transition']=True
    # Same seed/world must produce exactly the same historical and policy evidence.
    seed=int(truth.execute("SELECT value FROM private_meta WHERE key='seed'").fetchone()[0]);hist,terminal=history(seed)
    for name,policy in POLICIES.items():
        stored=json.loads(truth.execute('SELECT payload FROM policy_outcomes WHERE policy=?',(name,)).fetchone()[0])
        assert rollout(terminal,policy,future(seed))==stored
    checks['frozen_counterfactuals_match_generator']=True
    with tempfile.TemporaryDirectory() as temp:
        run=Path(temp)/'run';token=secrets.token_hex(24);http=server(env,run,token);thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start();base='http://127.0.0.1:'+str(http.server_port)
        def call(operation,body=None,auth=True):
            data=None if body is None else json.dumps(body).encode()
            req=urllib.request.Request(base+'/v1/'+operation,data=data,headers={'Authorization':'Bearer '+(token if auth else 'invalid'),'Content-Type':'application/json'})
            try:
                with urllib.request.urlopen(req,timeout=5) as r:return r.status,json.load(r)
            except urllib.error.HTTPError as e:return e.code,json.loads(e.read())
        assert call('mission',auth=False)[0]==401
        assert call('mission')[1]['current_year']==60
        assert call('score')[0]==404 and call('../evaluator/evaluator.sqlite')[0]==404
        checks['auth_and_private_endpoint_denial']=True
        code,brief=call('initial',{'request_id':'brief','limit':50});assert code==200 and brief['total_matched']==30
        code,catalog=call('catalogue',{'request_id':'catalog','query':'forest insect monitoring','limit':50});assert code==200 and catalog['returned']>0
        assert call('catalogue',{'request_id':'none','query':'unrecorded ocean salinity isotope'})[1]['items']==[]
        assert call('catalogue',{'request_id':'inject','query':"' OR 1=1; DROP TABLE items; --"})[0]==200
        checks['public_catalogue_and_unavailable_search']=True
        iid=truth.execute("SELECT item_id FROM labels WHERE store='investigation' AND class='discriminating_measurement'").fetchone()[0]
        request={'request_id':'assay','item_id':iid,'rationale':'Compare response across prey densities.','expected_observation':'The increase may level off at high density.','alternatives':['Proportional response','Saturating response'],'limit':2,'include_asset':True,'asset_limit':17}
        code,evidence=call('request',request);assert code==200 and evidence['returned']==2 and evidence['has_more']
        assert len(base64.b64decode(evidence['asset']['data']))==17 and evidence['asset']['has_more']
        assert call('request',request)[1]==evidence
        assert call('request',{**request,'rationale':'Different request under same ID.'})[0]==409
        assert call('request',{**request,'request_id':'missing-why','rationale':''})[0]==400
        assert call('request',{**request,'request_id':'future','year_range':[61,70]})[0]==403
        assert call('request',{**request,'request_id':'unavailable','item_id':'not-a-recorded-resource'})[0]==404
        assert call('request',{**request,'request_id':'badfield','database':'evaluator'})[0]==400
        assert call('request',{**request,'request_id':'oversized-page','limit':201})[0]==400
        assert call('request',{**request,'request_id':'oversized-asset','asset_limit':65537})[0]==400
        assert call('initial',{'request_id':'negative-offset','offset':-1})[0]==400
        checks['request_pagination_asset_range_rationale_and_idempotency']=True
        checks['future_unknown_item_and_arbitrary_file_requests_denied']=True
        checks['row_asset_and_offset_bounds_enforced']=True
        with sqlite3.connect(run/'audit.sqlite') as c:
            assert c.execute("SELECT count(*) FROM events WHERE request_id='assay'").fetchone()[0]==1
            recorded=json.loads(c.execute("SELECT request_json FROM events WHERE request_id='assay'").fetchone()[0]);assert recorded['rationale']==request['rationale'] and recorded['expected_observation']==request['expected_observation'] and recorded['alternatives']==request['alternatives']
            assert c.execute('SELECT count(*) FROM http_attempts WHERE status>=400').fetchone()[0]>=7
        checks['pre_acquisition_rationale_expectations_and_alternatives_retained']=True
        # A new broker instance reads the same durable session journal after a restart.
        http.shutdown();http.server_close();thread.join(timeout=5)
        http=server(env,run,token);thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start();base='http://127.0.0.1:'+str(http.server_port)
        assert call('request',request)[1]==evidence
        checks['restart_recovers_exact_admission_response']=True
        submit={'request_id':'final','policy':'continue','predicted_next_year_mean_insects':1.,'reasoning':'Scripted engineering fixture; not a reasoning agent result.','evidence_ids':[iid],'uncertainties':['This fixture does not assess inference quality.']}
        assert call('submit',{**submit,'request_id':'bad-cite','evidence_ids':['not-admitted']})[0]==400
        code,ack=call('submit',submit);assert code==200 and 'outcome' not in ack and 'score' not in ack
        assert call('request',{**request,'request_id':'after-final'})[0]==409
        assert call('submit',{**submit,'request_id':'second-final'})[0]==409
        assert call('submit',submit)[1]==ack
        checks['one_final_submission_no_reward_feedback_and_session_close']=True
        result=evaluate(env,run)
        assert math.isfinite(result['outcome']['objective']) and not result['relevance_labels_used_as_reward']
        assert result['http_attempts_including_retries_and_failures']>result['distinct_requested_items']
        checks['operator_scoring_and_failed_retry_cost_accounting']=True
        http.shutdown();http.server_close();thread.join(timeout=5)
    initial.close();invest.close();truth.close()
    return {'passed':True,'scope':'Two-store environment and actual HTTP inquiry/submit/score path using a scripted fixture only.','checks':checks,
            'initial_items':30,'requestable_items':129,'label_counts_operator_only':labelcounts,
            'edi_model_run':False,'human_benchmark_run':False,'comparative_advantage':'NOT TESTED','ecological_fidelity':'UNVALIDATED CONSTRUCTED WORLD'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--environment',type=Path,required=True);p.add_argument('--out',type=Path);a=p.parse_args();result=verify(a.environment.resolve())
    if a.out:a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
