"""Restore byte-identical source files and SQLite from Git's gzip snapshots."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

def restore(root):
    manifest=json.loads((root/'metadata/files.json').read_text(encoding='utf-8'))
    expected={x['path']:x['sha256'] for x in manifest}
    status=json.loads((root/'metadata/IMPORT_STATUS.json').read_text(encoding='utf-8'))
    expected['database/evidence.sqlite']=status['sqlite_sha256']
    for rel,sha in expected.items():
        p=root/rel
        if p.exists():
            if hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError('Existing file differs; refusing overwrite: '+rel)
            continue
        compressed=Path(str(p)+'.gz')
        if not compressed.exists():raise FileNotFoundError(rel)
        b=gzip.decompress(compressed.read_bytes())
        if hashlib.sha256(b).hexdigest()!=sha:raise ValueError('Checksum mismatch: '+rel)
        temporary=Path(str(p)+'.restoring');temporary.write_bytes(b);temporary.replace(p)
    return {'restored_and_verified':len(expected)}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=parser.parse_args();print(json.dumps(restore(a.root)))
