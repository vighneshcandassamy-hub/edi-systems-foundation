"""Create compact Git snapshots and a standalone corpus archive after validation."""
import argparse
import gzip
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def package(root,out):
    validation=json.loads((root/'metadata/VALIDATION.json').read_text(encoding='utf-8'))
    if not validation['passed']:raise ValueError('Validation must pass before packaging.')
    manifest=json.loads((root/'metadata/files.json').read_text(encoding='utf-8'))
    status=json.loads((root/'metadata/IMPORT_STATUS.json').read_text(encoding='utf-8'))
    # Refresh a lossless compressed storage object from each large current source.
    storage=[]
    for item in [*manifest,{'path':'database/evidence.sqlite','sha256':status['sqlite_sha256']}]:
        p=root/item['path'];compressed=Path(str(p)+'.gz')
        if p.stat().st_size>=500000 and p.suffix!='.gz' and p.suffix!='.sqlite':
            with p.open('rb') as src,compressed.open('wb') as dst:
                with gzip.GzipFile(filename='',mode='wb',fileobj=dst,mtime=0) as z:shutil.copyfileobj(src,z)
        target=compressed if compressed.exists() else p
        if target==compressed and hashlib.sha256(gzip.decompress(target.read_bytes())).hexdigest()!=item['sha256']:raise ValueError('Compressed snapshot differs: '+item['path'])
        storage.append({'path':item['path'],'sha256':item['sha256'],'stored_path':str(target.relative_to(root)),'storage_sha256':sha(target),'stored_bytes':target.stat().st_size,'encoding':'gzip' if target==compressed else 'identity'})
    (root/'metadata/STORAGE.json').write_text(json.dumps(storage,indent=2)+'\n',encoding='utf-8')
    def selected():
        for p in sorted(root.rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts or p.name.startswith('.') or p.name.endswith(('-journal','-wal','-shm')):continue
            if Path(str(p)+'.gz').exists():continue
            yield p
    paths=[p for p in selected() if p.name!='SHA256SUMS']
    (root/'SHA256SUMS').write_text(''.join(sha(p)+'  '+p.relative_to(root).as_posix()+'\n' for p in paths),encoding='utf-8')
    paths=list(selected())
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in paths:z.write(p,'meadows-budworm/'+p.relative_to(root).as_posix())
    print(json.dumps({'archive':str(out.resolve()),'archive_bytes':out.stat().st_size,'archive_sha256':sha(out),'git_files':len(paths)}))
    return paths

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--out',type=Path,required=True);a=p.parse_args();package(a.root,a.out)
