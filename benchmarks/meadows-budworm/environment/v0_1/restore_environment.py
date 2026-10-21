"""Restore immutable environment databases and verify their exact content hashes."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

def restore(root):
    manifest=json.loads((root/'manifest.json').read_text())
    for row in manifest['databases']:
        p=root/row['path'];compressed=Path(str(p)+'.gz')
        if hashlib.sha256(compressed.read_bytes()).hexdigest()!=row['compressed_sha256']:raise ValueError('Compressed snapshot hash mismatch: '+row['role'])
        data=gzip.decompress(compressed.read_bytes())
        if hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('Snapshot content mismatch: '+row['role'])
        if p.exists():
            if p.read_bytes()!=data:raise ValueError('Existing database differs; refusing overwrite: '+str(p))
        else:
            tmp=Path(str(p)+'.restoring');tmp.write_bytes(data);tmp.replace(p)
    print('Restored and verified three operator databases. Do not give evaluator or investigation files to participants.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--environment',type=Path,required=True);a=p.parse_args();restore(a.environment)
