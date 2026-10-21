"""Read-only evidence requests. This CLI is a corpus utility, not an EDI agent."""
import argparse
import base64
import gzip
import hashlib
import json
import sqlite3
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--include-reference',action='store_true',help='Explicitly expose reference explanations; this is not a security boundary.')
    sub=p.add_subparsers(dest='command',required=True)
    v=sub.add_parser('inventory');v.add_argument('--area')
    v=sub.add_parser('records');v.add_argument('--series');v.add_argument('--year',type=int);v.add_argument('--limit',type=int,default=10);v.add_argument('--offset',type=int,default=0);v.add_argument('--bbox',type=float,nargs=4,metavar=('WEST','SOUTH','EAST','NORTH'))
    v=sub.add_parser('text');v.add_argument('query');v.add_argument('--limit',type=int,default=10)
    v=sub.add_parser('file');v.add_argument('file_id');v.add_argument('--offset',type=int,default=0);v.add_argument('--max-bytes',type=int,default=32768)
    sub.add_parser('gaps');a=p.parse_args();root=a.root.resolve();dbpath=root/'database/evidence.sqlite'
    if not dbpath.exists():p.error('Run scripts/restore.py first.')
    db=sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
    role='' if a.include_reference else " AND f.role='observation'"
    if a.command=='inventory':
        q='SELECT DISTINCT f.* FROM evidence_files f LEFT JOIN file_areas a ON a.file_id=f.file_id WHERE 1=1'+role;args=[]
        if a.area:q+=' AND a.area_id=?';args.append(a.area)
        result=[dict(x) for x in db.execute(q+' ORDER BY f.path',args)]
    elif a.command=='gaps':result=[dict(x) for x in db.execute('SELECT * FROM evidence_gaps')]
    elif a.command=='records':
        if not 1<=a.limit<=200 or a.offset<0:p.error('Use limit 1..200 and nonnegative offset.')
        q='SELECT r.* FROM records r JOIN evidence_files f USING(file_id) WHERE 1=1'+role;args=[]
        for col,val in [('series',a.series),('event_year',a.year)]:
            if val is not None:q+=' AND r.'+col+'=?';args.append(val)
        if a.bbox:
            west,south,east,north=a.bbox
            if not (-180<=west<=east<=180 and -90<=south<=north<=90):p.error('Invalid bbox.')
            q+=' AND r.longitude BETWEEN ? AND ? AND r.latitude BETWEEN ? AND ?';args.extend([west,east,south,north])
        total=db.execute('SELECT count(*) FROM ('+q+')',args).fetchone()[0]
        rows=[dict(x) for x in db.execute(q+' ORDER BY r.record_id LIMIT ? OFFSET ?',args+[a.limit,a.offset])]
        for x in rows:x['payload']=json.loads(x.pop('payload_json'))
        result={'total_matched':total,'offset':a.offset,'returned':len(rows),'has_more':a.offset+len(rows)<total,'records':rows}
    elif a.command=='text':
        if not 1<=a.limit<=200:p.error('Use limit 1..200.')
        result=[dict(x) for x in db.execute('SELECT t.* FROM text_search s JOIN text_blocks t ON t.block_id=s.block_id JOIN evidence_files f ON f.file_id=t.file_id WHERE text_search MATCH ?'+role+' LIMIT ?',(a.query,a.limit))]
    else:
        if a.offset<0 or not 1<=a.max_bytes<=65536:p.error('Use nonnegative offset and max-bytes 1..65536.')
        row=db.execute('SELECT * FROM evidence_files f WHERE f.file_id=?'+role,(a.file_id,)).fetchone()
        if row is None:p.error('Unknown file or reference access not requested.')
        path=(root/row['path']).resolve();path.relative_to(root)
        data=path.read_bytes() if path.exists() else gzip.decompress(Path(str(path)+'.gz').read_bytes())
        if hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('File hash mismatch.')
        b=data[a.offset:a.offset+a.max_bytes];result={'file_id':a.file_id,'path':row['path'],'sha256':row['sha256'],'root_evidence_group':row['root_evidence_group'],'total_bytes':len(data),'offset':a.offset,'returned_bytes':len(b),'has_more':a.offset+len(b)<len(data),'encoding':'base64','data':base64.b64encode(b).decode()}
    print(json.dumps(result,ensure_ascii=False,indent=2));db.close()

if __name__=='__main__':main()
