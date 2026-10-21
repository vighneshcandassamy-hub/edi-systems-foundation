"""Validate actual stored bytes, database invariants and selected retrieval behavior."""
import argparse
import gzip
import hashlib
import json
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

def verify(root):
    inventory=json.loads((root/'metadata/files.json').read_text(encoding='utf-8'))
    status=json.loads((root/'metadata/IMPORT_STATUS.json').read_text(encoding='utf-8'))
    for item in inventory:
        p=root/item['path'];b=p.read_bytes() if p.exists() else gzip.decompress(Path(str(p)+'.gz').read_bytes())
        assert len(b)==item['size_bytes'],item['path']
        assert hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
    original=(root/'database/evidence.sqlite').read_bytes();compressed=(root/'database/evidence.sqlite.gz').read_bytes()
    assert gzip.decompress(compressed)==original
    assert hashlib.sha256(original).hexdigest()==status['sqlite_sha256']
    db=sqlite3.connect((root/'database/evidence.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert not db.execute('PRAGMA foreign_key_check').fetchall()
    assert db.execute('SELECT count(*) FROM records').fetchone()[0]==status['structured_records']
    assert db.execute('SELECT count(*) FROM text_blocks').fetchone()[0]==db.execute('SELECT count(*) FROM text_search').fetchone()[0]==status['searchable_text_blocks']
    assert db.execute('SELECT count(*) FROM evidence_files').fetchone()[0]==len(inventory)
    assert db.execute('SELECT count(*) FROM evidence_gaps').fetchone()[0]>=8
    assert not db.execute("SELECT 1 FROM records r JOIN evidence_files f USING(file_id) WHERE f.origin<>'native_download' LIMIT 1").fetchall()
    for series,count in status['records_by_series'].items():assert db.execute('SELECT count(*) FROM records WHERE series=?',(series,)).fetchone()[0]==count
    assert not db.execute('SELECT 1 FROM lineage l JOIN evidence_files c ON c.file_id=l.child_file_id JOIN evidence_files p ON p.file_id=l.parent_file_id WHERE c.root_evidence_group<>p.root_evidence_group').fetchall()
    edges=dict()
    for child,parent in db.execute('SELECT child_file_id,parent_file_id FROM lineage'):edges.setdefault(child,[]).append(parent)
    def visit(node,seen):
        assert node not in seen,'Lineage cycle'
        for parent in edges.get(node,[]):visit(parent,seen|{node})
    for node in edges:visit(node,set())
    sentinels=db.execute("SELECT count(*) FROM records WHERE series='nb_moths' AND CAST(json_extract(payload_json,'$.MOTH_COUNT') AS REAL)<0").fetchone()[0]
    assert sentinels>0
    def query(*args):return json.loads(subprocess.check_output([sys.executable,str(root/'scripts/query.py'),'--root',str(root),*args],text=True))
    obs=query('inventory');assert obs and all(x['role']=='observation' for x in obs)
    allfiles=query('--include-reference','inventory');assert len(allfiles)==len(inventory)>len(obs)
    sample=query('records','--series','nb_l2','--year','2024','--limit','2');assert sample['total_matched']==1458 and sample['returned']==2 and sample['has_more']
    ref=query('--include-reference','text','budworm','--limit','2');assert ref and all(x['role']=='reference' for x in ref)
    assert query('text','budworm','--limit','2')==[]
    file_result=query('file',obs[0]['file_id'],'--max-bytes','10');assert file_result['returned_bytes']==10 and file_result['has_more']
    # Exercise restore in a disposable copy with only compressed SQLite present.
    import shutil
    with tempfile.TemporaryDirectory() as temp:
        dest=Path(temp)/'corpus';shutil.copytree(root,dest);(dest/'database/evidence.sqlite').unlink()
        subprocess.check_output([sys.executable,str(dest/'scripts/restore.py'),'--root',str(dest)],text=True)
        assert hashlib.sha256((dest/'database/evidence.sqlite').read_bytes()).hexdigest()==status['sqlite_sha256']
    db.close()
    result={'passed':True,'scope':'Evidence storage, archive restore, lineage structure and read-only retrieval; no EDI/model evaluation.','verified_evidence_files':len(inventory),'structured_records':status['structured_records'],'text_blocks':status['searchable_text_blocks'],'sqlite_integrity':'ok','foreign_key_violations':0,'gzip_roundtrip':True,'reference_filter_test':True,'row_pagination_test':True,'byte_range_request_test':True,'negative_moth_sentinels_preserved':sentinels,'restore_from_compressed_snapshot':True,'benchmark_executed':False}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--save',action='store_true');a=p.parse_args();result=verify(a.root.resolve())
    if a.save:(a.root/'metadata/VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
