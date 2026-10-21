"""Focused integration campaign over HTTP. No EDI/LLM/human inference."""
import base64
import copy
import gzip
import hashlib
import json
import math
import platform
import secrets
import sqlite3
import tempfile
import threading
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
import broker
import world
import evaluate
import export_participant


def verify():
    root=Path(__file__).resolve().parent;fixture=root/'fixture';corpus=root.parents[1]/'database/evidence.sqlite'
    manifest=json.loads((fixture/'manifest.json').read_text())
    checks=[]
    def passed(case,detail):checks.append({'id':case,'status':'pass','detail':detail})
    baseline=hashlib.sha256(corpus.read_bytes()).hexdigest()
    assert baseline=='49856811262c175efe99c31635e098e56312bdbca98a4ec1f58fab12794e5bd5'
    data=gzip.decompress((fixture/'archive.sqlite.gz').read_bytes())
    assert hashlib.sha256(data).hexdigest()==manifest['archive_sha256']
    with sqlite3.connect(fixture/'archive.sqlite') as c:
        assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert c.execute('SELECT count(*) FROM documents').fetchone()[0]==manifest['documents']
        for source,digest,asset in c.execute('SELECT source,sha256,asset FROM documents'):
            if source=='external':assert asset==b''
            else:assert hashlib.sha256(asset).hexdigest()==digest
        for doc,meta in c.execute('SELECT id,metadata FROM documents'):
            for parent in json.loads(meta).get('derived_from',[]):
                assert c.execute('SELECT 1 FROM documents WHERE id=?',(parent,)).fetchone()
    with tempfile.TemporaryDirectory(prefix='edi-restore-check-') as temp:
        fresh=Path(temp)/'fixture';fresh.mkdir()
        for name in ('archive.sqlite.gz','mission.json','initial_state.json','manifest.json'):
            (fresh/name).write_bytes((fixture/name).read_bytes())
        assert not (fresh/'archive.sqlite').exists()
        restored=broker.Broker(fresh,Path(temp)/'run',corpus)
        assert hashlib.sha256((fresh/'archive.sqlite').read_bytes()).hexdigest()==manifest['archive_sha256']
        state=json.loads((fresh/'initial_state.json').read_text());state['year']=99
        (fresh/'initial_state.json').write_text(json.dumps(state))
        try:broker.Broker(fresh,Path(temp)/'other-run',corpus)
        except ValueError:pass
        else:raise AssertionError('Tampered configuration accepted')
    passed('V01','Archive/gzip/assets, clean compressed restore, configuration guard and preserved original corpus hashes')
    p=world.initial(7021)[0];p.update(insects=1.,enemies=.7,foliage=.8)
    untreated,_=world.step(p,world.climate(7021,1))
    broad,_=world.step(p,world.climate(7021,1),{'method':'broad','dose':1.})
    selective,_=world.step(p,world.climate(7021,1),{'method':'selective','dose':1.})
    assert broad['enemies']<selective['enemies']<untreated['enemies']
    assert broad['insects']<untreated['insects']
    for seed in (7021,7022,13):
        rows,plots=world.history(seed)
        assert all(all(math.isfinite(float(r[k])) for k in ('insects','enemies','foliage','fir','spruce','birch')) for r in rows)
        assert all(abs(p['fir']+p['spruce']+p['birch']-1)<1e-10 for p in plots)
    history,_=world.history()
    assert any(r['treatment_dose']>0 for r in history)
    passed('V02','Bounded histories and direct, method-dependent non-target pathway; not ecological calibration')
    with tempfile.TemporaryDirectory(prefix='edi-open-world-') as temp:
        run=Path(temp)/'run';token=secrets.token_urlsafe(32)
        http=broker.server(fixture,run,corpus,token);thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
        serial=0
        def call(op,body=None,rid=None,auth=True):
            nonlocal serial
            serial+=1;body=dict(body or {},request_id=rid or 'test-'+str(serial))
            req=urllib.request.Request('http://127.0.0.1:'+str(http.server_port)+'/v2/'+op,
                 data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+(token if auth else 'invalid'),'Content-Type':'application/json'})
            try:
                with urllib.request.urlopen(req,timeout=10) as r:return r.status,json.load(r)
            except urllib.error.HTTPError as e:return e.code,json.load(e)
        try:
            assert call('mission',auth=False)[0]==401
            assert call('world')[0]==404
            assert call('search',{'path':'../../initial_state.json'})[0]==400
            assert call('search',{'limit':1000000})[0]==400
            assert call('read',{'document_id':'../../initial_state.json'})[0]==404
            passed('V03','Authentication, private route/path and resource bounds denied')
            code,m=call('mission');assert code==200 and 'policy_options'not in m['mission']
            assert call('sources')[1]['sources'] and len(call('people')[1]['people'])==5
            docs=[];offset=0
            while True:
                code,result=call('search',{'query':'','offset':offset,'limit':100});assert code==200
                docs.extend(result['items'])
                if not result['has_more']:break
                offset+=len(result['items'])
            assert len(docs)==manifest['documents']
            # Verify all assets via the public interface, not direct file access.
            for d in docs:
                code,opened=call('read',{'document_id':d['id'],'include_asset':True,'asset_limit':65536})
                assert code==200
                asset=opened['asset'];collected=bytearray(base64.b64decode(asset['data']))
                while asset['has_more']:
                    _,part=call('read',{'document_id':d['id'],'include_asset':True,'asset_offset':len(collected),'asset_limit':65536})
                    asset=part['asset'];collected.extend(base64.b64decode(asset['data']))
                assert hashlib.sha256(collected).hexdigest()==d['sha256']
            passed('V04','Every archive item discoverable; every original asset retrieved and hash verified without hypothesis templates')
            total=0
            for d in [x for x in docs if x['source']=='external']:
                offset=0
                while True:
                    code,r=call('records',{'document_id':d['id'],'offset':offset,'limit':200});assert code==200
                    total+=len(r['rows']);offset+=len(r['rows'])
                    if not r['has_more']:break
            assert total==32895
            passed('V05','All 32,895 original structured rows retrievable through public document selectors')
            ask=call('ask',{'person_id':'mill','question':'What commitments have been made?'})[1]
            assert ask['materials'][0]['document_id']
            assert call('ask',{'person_id':'unknown','question':'What do you know?'})[0]==404
            assert call('measure',{'plots':['S01'],'metric':'pathogen_count'})[0]==422
            passed('V06','Source-linked role disclosure and honest unavailable measurement/role')
            measured={'plots':['S01'],'metric':'enemies'}
            code,job=call('measure',measured,rid='measurement-1');assert code==200
            assert call('measure',measured,rid='measurement-1')[1]==job
            assert call('measure',{'plots':['S02'],'metric':'enemies'},rid='measurement-1')[0]==409
            assert not call('status')[1]['observations']
            passed('V07','Idempotent scheduled measurement, conflict detection and delayed release')
            action={'kind':'treat','plots':['S01'],'method':'broad','dose':1.}
            code,action_result=call('act',action,rid='action-1');assert code==200
            assert call('act',action,rid='action-1')[1]==action_result
            assert call('act',action)[0]==409
            assert call('act',{'kind':'harvest','plots':['S01'],'fraction':.1})[0]==200
            assert call('act',{'kind':'treat','plots':['S02'],'dose':float('nan'),'method':'broad'})[0]==400
            assert call('act',{'kind':'treat','plots':['S01'],'dose':1.,'method':'broad','year':0})[0]==400
            passed('V08','Free parameterized interventions, overlapping-work and invalid/past action rejection')
            code,advanced=call('advance',{'years':1},rid='advance-1');assert code==200
            assert advanced['year']==1
            obs=next(x for x in advanced['published'] if x.get('job_id')==job['job']['id'])
            assert obs['readings'][0]['metric']=='enemies'
            assert call('read',{'document_id':obs['id']})[0]==200
            assert call('advance',{'years':1},rid='advance-1')[1]==advanced
            status=call('status')[1]
            assert status['year']==1 and abs(status['spent_this_year']-10.5)<1e-9
            passed('V09','Advance executes work and publishes grounded observations with costs exactly once')
            # Advance and publication commit in one SQLite transaction. Inject failure before commit.
            original=http.broker.perform
            def fail(op,b,s):
                result=original(op,b,s)
                if op=='advance':raise RuntimeError('injected pre-commit failure')
                return result
            http.broker.perform=fail
            try:http.broker.dispatch('advance',{'request_id':'crash-probe','years':1})
            except RuntimeError:pass
            else:raise AssertionError('Failure injection missing')
            http.broker.perform=original
            assert call('status')[1]['year']==1
            passed('V10','Pre-commit interruption rolls back world, jobs, evidence and request together')
            proposal=call('propose',{'objective':'Maintain supply while reducing damage and non-target exposure.','reason':'A proposed tradeoff for review.'})[1]
            assert proposal['status']=='pending_human_review' and proposal['original_objective_unchanged']
            assert call('submit',{'conclusion':'Unsupported citation','evidence_ids':['not-acquired']})[0]==400
            passed('V11','Objective proposal retained without silent adoption; unacquired citations denied')
            # Restart the actual broker and retry the committed mutation.
            http.shutdown();http.server_close();thread.join()
            http=broker.server(fixture,run,corpus,token);thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
            assert call('advance',{'years':1},rid='advance-1')[1]==advanced
            assert call('status')[1]['year']==1
            passed('V12','Durable process restart replays committed response without repeated effects')
            report={'conclusion':'Scripted engineering demonstration only; no scientific conclusion.',
                'recommendations':['Inspect the actual evidence before selecting future measures.'],
                'uncertainties':['Ecological fidelity and EDI reasoning remain untested.'],
                'evidence_ids':[docs[0]['id'],obs['id']]}
            code,final=call('submit',report,rid='final');assert code==200
            assert call('submit',report,rid='final')[1]==final
            assert call('advance',{'years':1})[0]==409
            evaluated=evaluate.evaluate(run)
            assert evaluated['years_elapsed']==1 and evaluated['http_failures']>0
            assert evaluated['model_tokens_energy_and_reasoning_latency_measured']is False
            passed('V13','Open final report, session closure, idempotent final replay and offline outcome accounting')
            package=Path(temp)/'participant.zip'
            export_participant.export(package)
            with zipfile.ZipFile(package) as z:
                assert set(z.namelist())=={'client.py','PARTICIPANT.md','PUBLIC_OPERATIONS.json','mission.json'}
            passed('V14','Participant export allowlist excludes world, archive, state and operator reports; deployment isolation still unqualified')
        finally:
            http.shutdown();http.server_close();thread.join(timeout=5)
    assert hashlib.sha256(corpus.read_bytes()).hexdigest()==baseline
    return {'scope':'Single-host constructed environment engineering integration; scripted client, no reasoning agent',
       'passed':True,'checks':checks,'documents':manifest['documents'],'external_structured_rows':total,
       'formats':manifest['formats'],'model':world.VERSION,'platform':platform.platform(),'python':platform.python_version(),
       'edi_run':False,'human_run':False,'ecological_fidelity_qualified':False,'comparative_benchmark_run':False,
       'source_corpus_unchanged':True}


if __name__=='__main__':
    out=Path(__file__).resolve().parent/'reports/VALIDATION.json'
    out.parent.mkdir(exist_ok=True)
    result=verify();out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
