"""Participant-only HTTP evidence broker. Never opens evaluator files or world.py."""
import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

def js(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)

class Invalid(Exception):
    def __init__(self,status,code,message):self.status=status;self.code=code;self.message=message

class Broker:
    def __init__(self,env,run):
        self.env=Path(env).resolve();self.run=Path(run).resolve();self.run.mkdir(parents=True,exist_ok=True);self.lock=threading.Lock()
        # Strict physical allowlist: no evaluator path, arbitrary filename, SQL or raw file endpoint.
        self.paths={s:self.env/s/(s+'.sqlite') for s in ('initial','investigation')}
        for path in self.paths.values():
            if not path.is_file():raise FileNotFoundError('Restore environment databases first: '+str(path))
        self.mission=json.loads((self.env/'participant/mission.json').read_text())
        self.audit=self.run/'audit.sqlite'
        with sqlite3.connect(self.audit) as c:
            c.executescript('CREATE TABLE IF NOT EXISTS events(request_id TEXT PRIMARY KEY,body_sha TEXT NOT NULL,operation TEXT NOT NULL,request_json TEXT NOT NULL,response_json TEXT NOT NULL,returned_bytes INTEGER NOT NULL,elapsed_seconds REAL NOT NULL); CREATE TABLE IF NOT EXISTS final_submission(id INTEGER PRIMARY KEY CHECK(id=1),payload_json TEXT NOT NULL);')
            if 'request_json' not in {x[1] for x in c.execute('PRAGMA table_info(events)')}:raise ValueError('Incompatible older audit schema; preserve it and choose a fresh run directory.')
            c.execute('CREATE TABLE IF NOT EXISTS http_attempts(id INTEGER PRIMARY KEY,operation TEXT,request_id TEXT,status INTEGER,returned_bytes INTEGER,elapsed_seconds REAL)')

    def connection(self,store):
        c=sqlite3.connect(self.paths[store].as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c

    @staticmethod
    def bounded_int(x,low,high,name):
        if type(x) is not int or not low<=x<=high:raise Invalid(400,'invalid_range',f'{name} must be an integer in {low}..{high}.')
        return x

    @staticmethod
    def public(row):
        return {'item_id':row['item_id'],'title':row['title'],'summary':row['summary'],
                'source_group':row['source_group'],'scope':json.loads(row['scope_json']),
                'format':row['format'],'asset_sha256':row['sha256']}

    def dispatch(self,operation,body):
        if not isinstance(body,dict):raise Invalid(400,'invalid_request','JSON object required.')
        allowed={
          'initial':{'request_id','offset','limit'},
          'catalogue':{'request_id','query','district','offset','limit'},
          'request':{'request_id','item_id','rationale','expected_observation','alternatives','offset','limit','include_asset','asset_offset','asset_limit','year_range'},
          'submit':{'request_id','policy','predicted_next_year_mean_insects','reasoning','evidence_ids','uncertainties'}}
        if operation not in allowed:raise Invalid(404,'not_found','Unknown public operation.')
        if set(body)-allowed[operation]:raise Invalid(400,'unknown_field','Unsupported request fields.')
        rid=body.get('request_id')
        if not isinstance(rid,str) or not 1<=len(rid)<=120:raise Invalid(400,'request_id_required','Use a nonempty request_id, at most 120 characters.')
        canonical=hashlib.sha256((operation+'\0'+js(body)).encode()).hexdigest()
        with self.lock,sqlite3.connect(self.audit) as audit:
            old=audit.execute('SELECT body_sha,response_json FROM events WHERE request_id=?',(rid,)).fetchone()
            if old:
                if old[0]!=canonical:raise Invalid(409,'request_conflict','request_id already belongs to a different request.')
                return json.loads(old[1])
            if audit.execute('SELECT 1 FROM final_submission').fetchone():raise Invalid(409,'session_closed','This session has already submitted its final answer.')
            started=time.perf_counter()
            if operation in ('initial','catalogue'):
                offset=self.bounded_int(body.get('offset',0),0,100000,'offset');limit=self.bounded_int(body.get('limit',20),1,50,'limit')
                store='initial' if operation=='initial' else 'investigation'
                with self.connection(store) as c:rows=list(c.execute('SELECT * FROM items ORDER BY item_id'))
                if operation=='catalogue':
                    query=body.get('query','');district=body.get('district')
                    if not isinstance(query,str) or len(query)>1000:raise Invalid(400,'invalid_query','query must be text, at most 1000 characters.')
                    if district is not None and (not isinstance(district,str) or len(district)>120):raise Invalid(400,'invalid_scope','district must be text.')
                    words=re.findall(r'\w+',query.casefold())
                    def rank(r):return sum(w in (r['title']+' '+r['summary']).casefold() for w in words)
                    if district is not None:rows=[r for r in rows if json.loads(r['scope_json']).get('district','').casefold()==district.casefold()]
                    if words:rows=[r for r in rows if rank(r)>0];rows.sort(key=lambda r:(-rank(r),r['item_id']))
                total=len(rows);page=rows[offset:offset+limit]
                items=[self.public(r) for r in page]
                if operation=='initial':
                    for x,r in zip(items,page):x['records']=json.loads(r['payload_json'])
                result={'status':'ok','operation':operation,'offset':offset,'returned':len(page),'total_matched':total,'has_more':offset+len(page)<total,'items':items}
            elif operation=='request':
                for field in ('rationale','expected_observation'):
                    if not isinstance(body.get(field),str) or not 1<=len(body[field].strip())<=8000:raise Invalid(400,'inquiry_required',f'Provide {field} before acquiring evidence.')
                alt=body.get('alternatives',[])
                if not isinstance(alt,list) or len(alt)>20 or any(not isinstance(x,str) or len(x)>2000 for x in alt):raise Invalid(400,'invalid_alternatives','alternatives must be a short text list.')
                iid=body.get('item_id')
                if not isinstance(iid,str):raise Invalid(400,'invalid_item','item_id must be text.')
                with self.connection('investigation') as c:r=c.execute('SELECT * FROM items WHERE item_id=?',(iid,)).fetchone()
                if r is None:raise Invalid(404,'unavailable','No requestable evidence with this item_id. Nothing was generated to fill the gap.')
                records=json.loads(r['payload_json']);yr=body.get('year_range')
                if yr is not None:
                    if not isinstance(yr,list) or len(yr)!=2 or any(type(x)is not int for x in yr) or yr[0]>yr[1]:raise Invalid(400,'invalid_time','year_range must contain two ordered integer simulation years.')
                    if yr[1]>self.mission['current_year']:raise Invalid(403,'future_unavailable','Future outcomes are not requestable.')
                    if any('year' not in x for x in records):raise Invalid(400,'incompatible_clock','These external records do not use simulation years.')
                    records=[x for x in records if yr[0]<=x['year']<=yr[1]]
                offset=self.bounded_int(body.get('offset',0),0,100000,'offset');limit=self.bounded_int(body.get('limit',100),1,200,'limit')
                page=records[offset:offset+limit];result={'status':'ok',**self.public(r),'offset':offset,'returned':len(page),'total_matched':len(records),'has_more':offset+len(page)<len(records),'records':page}
                if type(body.get('include_asset',False))is not bool:raise Invalid(400,'invalid_asset','include_asset must be boolean.')
                if body.get('include_asset',False):
                    if yr is not None:raise Invalid(400,'asset_scope_conflict','An original asset cannot be combined with a filtered year range; request rows or the unfiltered allowed asset separately.')
                    offset=self.bounded_int(body.get('asset_offset',0),0,10000000,'asset_offset');limit=self.bounded_int(body.get('asset_limit',32768),1,65536,'asset_limit');b=r['asset'];part=b[offset:offset+limit]
                    result['asset']={'encoding':'base64','total_bytes':len(b),'offset':offset,'returned_bytes':len(part),'has_more':offset+len(part)<len(b),'data':base64.b64encode(part).decode()}
            else:
                if body.get('policy')not in self.mission['policy_options']:raise Invalid(400,'invalid_policy','Choose a declared policy option.')
                val=body.get('predicted_next_year_mean_insects')
                if type(val)not in (int,float) or not 0<=val<=100:raise Invalid(400,'invalid_forecast','Supply a finite nonnegative density forecast, at most 100.')
                if not isinstance(body.get('reasoning'),str) or not 1<=len(body['reasoning'])<=20000:raise Invalid(400,'reasoning_required','Provide reasoning.')
                ids=body.get('evidence_ids',[])
                if not isinstance(ids,list) or len(ids)>500 or any(not isinstance(x,str) for x in ids):raise Invalid(400,'invalid_citations','evidence_ids must be a list of at most 500 IDs.')
                admitted=set()
                for (value,) in audit.execute('SELECT response_json FROM events'):
                    value=json.loads(value)
                    if value.get('item_id'):admitted.add(value['item_id'])
                    # Catalogue metadata alone is not the underlying observation.
                    if value.get('operation')=='initial':admitted.update(x['item_id'] for x in value.get('items',[]))
                # The exported initial database is already admitted at session start.
                with self.connection('initial') as c:admitted.update(x[0] for x in c.execute('SELECT item_id FROM items'))
                if set(ids)-admitted:raise Invalid(400,'unseen_evidence','Citations must refer to initial or actually acquired evidence.')
                if not isinstance(body.get('uncertainties',[]),list) or any(not isinstance(x,str) for x in body.get('uncertainties',[])):raise Invalid(400,'invalid_uncertainties','uncertainties must be a text list.')
                audit.execute('INSERT INTO final_submission VALUES (1,?)',(js(body),))
                result={'status':'accepted','message':'Final submission recorded. Evaluation is separate; no outcome feedback is exposed in this session.'}
            encoded=js(result);audit.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?)',(rid,canonical,operation,js(body),encoded,len(encoded.encode()),time.perf_counter()-started))
            return result

def server(env,run,token,port=0):
    broker=Broker(env,run)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def reply(self,status,data):
            b=js(data).encode()
            with broker.lock,sqlite3.connect(broker.audit) as c:
                c.execute('INSERT INTO http_attempts(operation,request_id,status,returned_bytes,elapsed_seconds) VALUES (?,?,?,?,?)',(self.path,getattr(self,'request_id',None),status,len(b),time.perf_counter()-getattr(self,'started',time.perf_counter())))
            self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
        def authorized(self):return hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+token)
        def do_GET(self):
            self.started=time.perf_counter()
            if not self.authorized():return self.reply(401,{'status':'denied'})
            if self.path!='/v1/mission':return self.reply(404,{'status':'not_found'})
            self.reply(200,broker.mission)
        def do_POST(self):
            self.started=time.perf_counter()
            if not self.authorized():return self.reply(401,{'status':'denied'})
            try:
                if not self.path.startswith('/v1/'):raise Invalid(404,'not_found','Unknown public operation.')
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<=131072:raise Invalid(413,'request_size','JSON body must be 1..131072 bytes.')
                self.connection.settimeout(5)
                def reject_constant(x):raise ValueError('Non-finite JSON number')
                body=json.loads(self.rfile.read(n),parse_constant=reject_constant)
                if isinstance(body,dict) and isinstance(body.get('request_id'),str):self.request_id=body['request_id'][:120]
                result=broker.dispatch(self.path[4:],body);self.reply(200,result)
            except Invalid as e:self.reply(e.status,{'status':'error','code':e.code,'message':e.message})
            except (ValueError,TypeError,json.JSONDecodeError):self.reply(400,{'status':'error','code':'invalid_json_or_type','message':'Invalid JSON or field type.'})
            except TimeoutError:self.reply(408,{'status':'error','code':'read_timeout','message':'Timed out reading request body.'})
    http=ThreadingHTTPServer(('127.0.0.1',port),Handler);http.broker=broker;return http

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--environment',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--port',type=int,default=8765);a=p.parse_args()
    token=os.environ.get('EDI_BENCHMARK_TOKEN','')
    if len(token)<24:p.error('Set EDI_BENCHMARK_TOKEN to a fresh secret of at least 24 characters; do not commit it.')
    http=server(a.environment,a.run,token,a.port);print(f'Evidence broker listening on http://127.0.0.1:{http.server_port}',flush=True)
    try:http.serve_forever()
    except KeyboardInterrupt:pass
    finally:http.server_close()
