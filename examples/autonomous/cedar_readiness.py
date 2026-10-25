"""Cedar connection/byte-envelope checks only; zero participant responses."""
import base64
import json
import os
from pathlib import Path
import sqlite3
import struct
import subprocess
import sys
import uuid
import zlib
from hashlib import sha256


def native_extra(source,out):
    sys.path[:0]=[str(source/'src'),str(source)]
    os.environ['EDI_MEADOWS_ROOT']=str(source/'meadows')
    from cedar_session import CedarSession
    from edi.inquiry.application import IntegratedApplication
    from edi.observe.contracts import Capture,OriginSpec
    from edi.reason.contracts import EvidenceSelection
    from edi.shared.durable_io import canonical
    from io import BytesIO
    import jsonschema,pydantic,numpy,scipy
    assert (pydantic.__version__,numpy.__version__,scipy.__version__)==('2.12.5','2.5.3','1.17.0')
    session=CedarSession(source,out,token=os.environ['EDI_BROKER_TOKEN'])
    app=IntegratedApplication(session.profile());state,request=session.pending()
    episode=app.runtime.reasoning.get(state['inquiry_id'])
    jsonschema.Draft202012Validator.check_schema(request['response_schema'])
    def chunk(tag,body):return struct.pack('!I',len(body))+tag+body+struct.pack('!I',zlib.crc32(tag+body)&0xffffffff)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b'\x00\x10\x80\xf0'))+chunk(b'IEND',b'')
    origin=app.runtime.register_origin(OriginSpec(namespace='edi.readiness.synthetic',native_source_id='synthetic-pixel',
        epoch='1',deliverer='authored-probe',channel='synthetic-image',adapter='cedar-readiness/1.0',binding_basis='configured'))
    record=app.runtime.observe(Capture(origin_ref=origin.origin_ref,idempotency_key='synthetic-pixel',kind='readiness-fixture',
        media_type='image/png',origin_class='simulation',lineage=('authored-readiness-fixture',),completeness='complete',
        expected_bytes=len(png),expected_sha256=sha256(png).hexdigest()),BytesIO(png)).observation
    image_selection=EvidenceSelection(record_id=record.record_id,length=len(png))
    image_request=episode.request.model_copy(update={'inquiry_id':'readiness-image-preview','request_id':'readiness-image-preview',
        'evidence':episode.request.evidence+(image_selection,)})
    image_size=app.reasoner.preview(image_request)
    image_episode=app.runtime.reasoning.preview(image_request)
    job=episode.jobs[-1].model_copy(update={'context_sha256':image_episode.context.sha256})
    image_episode=image_episode.model_copy(update={'jobs':(job,)})
    rendered=app.reasoner._request(job,image_episode)
    image_parts=[p for p in rendered['messages'][1]['content'] if p['type']=='image_url']
    assert len(image_parts)==1 and base64.b64decode(image_parts[0]['image_url']['url'].split(',',1)[1])==png
    assert rendered['image_refs'][0]['record_id']==record.record_id
    # A full 64KiB selected text and one image test the declared byte envelope.
    text=b'authored byte-envelope probe; not ecological evidence.\n'*1300
    text=text[:65536]
    large=app.runtime.observe(Capture(origin_ref=origin.origin_ref,idempotency_key='synthetic-large-text',kind='readiness-fixture',
        media_type='text/plain',origin_class='simulation',lineage=('authored-readiness-fixture',),completeness='complete',
        expected_bytes=len(text),expected_sha256=sha256(text).hexdigest()),BytesIO(text)).observation
    large_request=image_request.model_copy(update={'inquiry_id':'readiness-byte-preview','request_id':'readiness-byte-preview',
        'evidence':image_request.evidence+(EvidenceSelection(record_id=large.record_id,length=len(text)),)})
    large_size=app.reasoner.preview(large_request)
    assert large_size['input_tokens'] is None and large_size['request_bytes']<=262144
    assert app.teacher is None and app.profile.teacher.mode=='disabled' and not app.profile.use_teaching_memory
    with sqlite3.connect(app.runtime.reasoning.profile.database) as db:
        episodes=[json.loads(r[0]) for r in db.execute('select document from episodes')]
    assert len(episodes)==1 and sum(len(e['jobs']) for e in episodes)==1 and not any(e['responses'] or e['rejections'] for e in episodes)
    result={'schema_checked':True,'synthetic_image_identity_verified':True,'image_request_bytes':image_size['request_bytes'],
        'large_selected_text_bytes':len(text),'large_plus_image_request_bytes':large_size['request_bytes'],
        'byte_limit':262144,'exact_tokens':'unknown','teacher_jobs':0,'qwen_calls':0,'participant_responses':0,
        'versions':{'python':sys.version.split()[0],'pydantic':pydantic.__version__,'numpy':numpy.__version__,'scipy':scipy.__version__}}
    (out/'native-extra.json').write_text(json.dumps(result,indent=2))


def probe(source,prep,python):
    source,prep=Path(source).resolve(),Path(prep).resolve()
    sys.path.insert(0,str(source));os.environ['EDI_MEADOWS_ROOT']=str(source/'meadows')
    from cedar_session import NotebookCedar,verify_source,BOUNDS
    manifest=verify_source(source)
    prep.mkdir(parents=True,exist_ok=True)
    report_path=prep/'cedar-readiness.json'
    if report_path.exists():
        saved=json.loads(report_path.read_bytes())
        assert saved['passed'] and saved['source_manifest_sha256']==sha256((source/'source-manifest.json').read_bytes()).hexdigest()
        return saved
    session=NotebookCedar(source,prep/('disposable-probe-'+uuid.uuid4().hex[:10]),python)
    try:
        state=session.open(scope='Disposable connection preflight only; no participant response or investigation')
        assert state['state']=='waiting-reasoner' and state['turn']==0
        _,request=session.pending();control=json.loads(request['messages'][0]['content'])
        assert set(control['controller_access']['operations'])==set(__import__('meadows_world').PUBLIC_OPERATIONS)
        assert request['reasoning_role']=='sole' and request['job']['teaching_stage']=='standard'
        def events():
            with sqlite3.connect((session.out/'cedar-world/run.sqlite').as_uri()+'?mode=ro',uri=True) as db:
                return list(db.execute('select id,operation from events order by rowid'))
        before=events();assert len(before)==1 and before[0][1]=='mission'
        request_bytes=Path(state['request_path']).read_bytes()
        assert session.reopen()==state and events()==before and Path(state['request_path']).read_bytes()==request_bytes
        count=len(list(session.out.glob('reasoner-response-*.json')))
        for job,content,expected in [(state['job_id'],'double encoded input',TypeError),('stale-job',{},ValueError)]:
            try:session.import_response(job,content)
            except expected:pass
            else:raise AssertionError('Invalid handoff was not blocked')
        assert len(list(session.out.glob('reasoner-response-*.json')))==count
        try:session.finalize()
        except ValueError:pass
        else:raise AssertionError('Evaluator must be fenced before termination')
        assert not (session.out/'post-terminal-evaluation.json').exists() and events()==before
        env=dict(os.environ,EDI_BROKER_TOKEN=session.token,PYTHONPATH=str(source/'src'),EDI_MEADOWS_ROOT=str(source/'meadows'))
        r=subprocess.run([str(python),str(source/'cedar_readiness.py'),'native-extra',str(source),str(session.out)],
                         cwd=source,env=env,text=True,capture_output=True,timeout=120)
        (prep/'native-extra.log').write_text(r.stdout+r.stderr)
        assert r.returncode==0,r.stderr[-3000:]
        extra=json.loads((session.out/'native-extra.json').read_bytes())
        assert events()==before
        integrity={}
        for p in session.out.rglob('*.sqlite3'):
            with sqlite3.connect(p) as db:integrity[p.relative_to(session.out).as_posix()]=db.execute('pragma integrity_check').fetchone()[0]
        with sqlite3.connect(session.out/'cedar-world/run.sqlite') as db:integrity['cedar-world/run.sqlite']=db.execute('pragma integrity_check').fetchone()[0]
        assert all(v=='ok' for v in integrity.values())
        report={'passed':True,'benchmark_started':False,'scope':'Disposable Cedar connection/export preflight; actual benchmark not launched',
            'source_manifest_sha256':sha256((source/'source-manifest.json').read_bytes()).hexdigest(),
            'source_revision':manifest['git_head'],'verified_source_and_input_files':len(manifest['files']),
            'frozen_world_files':sum(p.startswith('meadows/') for p in manifest['files']),
            'initial_request_bytes':len(request_bytes),'restart_same_pending_job':True,'restart_new_broker_calls':0,
            'broker_operations':['mission'],'fresh_actual_run_created':False,'handoff_guards_passed':True,
            'preterminal_evaluator_fenced':True,'integrity':integrity,'native_checks':extra,'bounds_for_actual_run':BOUNDS,
            'qualification':'Operational readiness for an unblinded manual assessment only; no model advantage or scientific result'}
        session.stop();report['probe_broker_stopped']=True
        report_path.write_text(json.dumps(report,indent=2))
        return report
    finally:
        if session.broker is not None:session.stop()

if __name__=='__main__':
    mode,source,out=sys.argv[1:4]
    if mode!='native-extra':raise ValueError('No benchmark entry point here')
    native_extra(Path(source),Path(out))
