"""Static consolidation checks. No broker/world/model/agent is started."""
import argparse
import gzip
import hashlib
import json
import re
import sqlite3
from pathlib import Path


def digest(data):return hashlib.sha256(data).hexdigest()


def within(root,relative):
    path=(root/relative).resolve()
    path.relative_to(root)
    return path


def verify(root):
    root=root.resolve()
    manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_text())
    assert manifest['package_id']=='EDI-MEADOWS-CW-DEV-0.2.1'
    checked=set()
    for item in manifest['files']:
        assert item['path']not in checked,'Duplicate package path'
        data=within(root,item['path']).read_bytes()
        assert len(data)==item['bytes'],item['path']
        assert digest(data)==item['sha256'],item['path']
        checked.add(item['path'])
    world_root=within(root,manifest['active_environment'])
    pin=json.loads((world_root/'reports/BUILD_PIN.json').read_text())
    assert digest((world_root/'reports/BUILD_PIN.json').read_bytes())==manifest['implementation_pin_sha256']
    for path,sha in pin['files_sha256'].items():
        assert digest(within(world_root,path).read_bytes())==sha,path
    allowed=manifest['participant_files']
    actual=sorted(str(p.relative_to(root)) for p in (root/'participant').rglob('*') if p.is_file())
    assert actual==sorted(allowed),'Unexpected/missing participant file'
    for target,source in manifest['participant_mirrors'].items():
        assert within(root,target).read_bytes()==within(root,source).read_bytes(),target
    storage=json.loads((root/'metadata/STORAGE.json').read_text())
    corpus_bytes=None
    for item in storage:
        stored=within(root,item['stored_path']).read_bytes()
        assert digest(stored)==item['storage_sha256'],item['stored_path']
        data=gzip.decompress(stored) if item['encoding']=='gzip' else stored
        assert digest(data)==item['sha256'],item['path']
        if item['path']=='database/evidence.sqlite':corpus_bytes=data
    corpus=sqlite3.connect(':memory:');corpus.deserialize(corpus_bytes)
    assert corpus.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert corpus.execute('SELECT count(*) FROM records').fetchone()[0]==32895
    assert corpus.execute('SELECT count(*) FROM text_blocks').fetchone()[0]==150
    assert corpus.execute('SELECT count(*) FROM evidence_files').fetchone()[0]==28
    corpus.close()
    wm=json.loads((world_root/'fixture/manifest.json').read_text())
    packed=(world_root/'fixture/archive.sqlite.gz').read_bytes()
    assert digest(packed)==wm['archive_gzip_sha256']
    archive_bytes=gzip.decompress(packed);assert digest(archive_bytes)==wm['archive_sha256']
    archive=sqlite3.connect(':memory:');archive.deserialize(archive_bytes)
    assert archive.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    counts={'documents':archive.execute('SELECT count(*) FROM documents').fetchone()[0],
            'sources':archive.execute('SELECT count(*) FROM sources').fetchone()[0],
            'roles':archive.execute('SELECT count(*) FROM people').fetchone()[0]}
    assert counts=={'documents':165,'sources':10,'roles':5}
    cat=json.loads((world_root/'RESOURCE_CATALOGUE.json').read_text())
    assert {d['id'] for d in cat['documents']}=={r[0] for r in archive.execute('SELECT id FROM documents')}
    archive.close()
    ops=json.loads((root/'participant/PUBLIC_OPERATIONS.json').read_text())
    assert len(ops['operations'])==13
    assert not any({'rationale','expected_observation','hypothesis'}&set(x['required_fields']) for x in ops['operations'])
    assert 'policy_options'not in json.loads((root/'participant/mission.json').read_text())
    validation=json.loads((world_root/'reports/VALIDATION.json').read_text())
    assert validation['passed'] and len(validation['checks'])==14
    assert all(x['status']=='pass' for x in validation['checks'])
    assert validation['edi_run']is False and validation['comparative_benchmark_run']is False
    readiness=json.loads((root/'READINESS.json').read_text())
    assert readiness['edi_run']=='not_run' and readiness['test_protocol']=='not_frozen'
    for relative in manifest['navigation_documents']:
        doc=within(root,relative)
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
            if link.startswith(('https://','http://','mailto:','#')):continue
            target=(doc.parent/link.split('#',1)[0]).resolve();target.relative_to(root)
            assert target.exists(),str(doc)+': '+link
    return {'package_id':manifest['package_id'],'passed':True,'scope':'static_consolidation_integrity_only',
        'files_verified':len(checked),'source_storage_objects_verified':len(storage),
        'implementation_files_pinned':len(pin['files_sha256']),'participant_files_verified':len(allowed),
        'corpus_records':32895,'corpus_text_blocks':150,'corpus_assets':28,**counts,
        'operations':13,'retained_environment_engineering_checks':14,
        'environment_runtime_campaign_rerun':False,'edi_run_started':False,'human_run_started':False,
        'scientific_or_comparative_qualification':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--report',type=Path)
    args=p.parse_args();result=verify(args.root)
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
