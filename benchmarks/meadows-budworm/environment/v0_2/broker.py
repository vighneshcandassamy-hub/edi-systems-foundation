"""Single-host operator controller. No model calls, answer labels or public hidden-state route."""
import argparse
import base64
import gzip
import hashlib
import hmac
import json
import math
import os
import re
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import world


def js(x): return json.dumps(x,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':'))


class Invalid(Exception):
    def __init__(self,code,message,status=400): self.code,self.message,self.status=code,message,status


def integer(x,lo,hi,name):
    if type(x)is not int or not lo<=x<=hi: raise Invalid('invalid_range',name)
    return x


def number(x,lo,hi,name):
    if type(x)not in (int,float) or not math.isfinite(x) or not lo<=x<=hi: raise Invalid('invalid_number',name)
    return x


def text(x,name,limit=8000):
    if not isinstance(x,str) or not x.strip() or len(x)>limit: raise Invalid('invalid_text',name)
    return x


FIELDS={
 'mission':set(), 'sources':set(), 'people':set(), 'status':set(),
 'search':{'query','source','offset','limit'},
 'read':{'document_id','include_asset','asset_offset','asset_limit'},
 'records':{'document_id','offset','limit'},
 'ask':{'person_id','question'},
 'measure':{'plots','metric'},
 'act':{'kind','plots','method','dose','fraction','year'},
 'advance':{'years'}, 'propose':{'objective','reason'},
 'submit':{'conclusion','recommendations','uncertainties','evidence_ids','forecast'}}

OPERATIONS={
 'mission':'Read the original objective and authority.',
 'sources':'Browse the complete source directory.', 'people':'Browse registered roles.',
 'search':'Search ordinary archive text/metadata; empty query browses all records. No relevance labels.',
 'read':'Read a document and optionally its original bytes in bounded chunks.',
 'records':'Read rows from an external source asset by its public document ID.',
 'ask':'Send a question to a registered role; return its bounded source-linked records, not generated expertise.',
 'measure':'Commission an instrument observation; available next simulation year.',
 'act':'Schedule a supported treatment or harvest for a future simulation year.',
 'advance':'Advance simulation time; execute admitted work and publish due observations.',
 'status':'Inspect public time, spending, jobs, observations and submitted proposals.',
 'propose':'Record a proposed objective revision for operator/human consideration; original objective remains authoritative.',
 'submit':'Record a final conclusion without selecting a preset policy. Closes the session.'}


class Broker:
    def __init__(self,environment,run,corpus):
        self.env,self.run,self.corpus=map(lambda x:Path(x).resolve(),(environment,run,corpus))
        self.run.mkdir(parents=True,exist_ok=True)
        self.lock=threading.Lock()
        self.mission=json.loads((self.env/'mission.json').read_text())
        manifest=json.loads((self.env/'manifest.json').read_text())
        for path,key in [(Path(world.__file__),'world_sha256'),(self.env/'initial_state.json','initial_state_sha256'),(self.env/'mission.json','mission_sha256')]:
            if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest[key]:raise ValueError('Pinned configuration mismatch: '+key)
        if hashlib.sha256(self.corpus.read_bytes()).hexdigest()!=manifest['source_corpus_sha256']:
            raise ValueError('Pinned external corpus mismatch')
        archive=self.env/'archive.sqlite'
        if not archive.exists():
            packed=(self.env/'archive.sqlite.gz').read_bytes()
            if hashlib.sha256(packed).hexdigest()!=manifest['archive_gzip_sha256']: raise ValueError('Archive gzip hash mismatch')
            data=gzip.decompress(packed)
            if hashlib.sha256(data).hexdigest()!=manifest['archive_sha256']: raise ValueError('Archive content hash mismatch')
            temporary=archive.with_suffix('.restoring');temporary.write_bytes(data);temporary.replace(archive)
        if hashlib.sha256(archive.read_bytes()).hexdigest()!=manifest['archive_sha256']: raise ValueError('Archive mismatch')
        self.archive=archive
        # Resume only against the same immutable files and model implementation.
        self.identity=hashlib.sha256((manifest['archive_sha256']+manifest['source_corpus_sha256']+
            hashlib.sha256((self.env/'initial_state.json').read_bytes()).hexdigest()+
            hashlib.sha256(Path(__file__).read_bytes()).hexdigest()+
            hashlib.sha256(Path(world.__file__).read_bytes()).hexdigest()).encode()).hexdigest()
        self.db=self.run/'run.sqlite'
        with sqlite3.connect(self.db) as c:
            c.executescript('''CREATE TABLE IF NOT EXISTS state(id INTEGER PRIMARY KEY CHECK(id=1),payload TEXT);
             CREATE TABLE IF NOT EXISTS identity(id INTEGER PRIMARY KEY CHECK(id=1),value TEXT);
             CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,body_sha TEXT,operation TEXT,request TEXT,response TEXT);
             CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY,operation TEXT,status INTEGER,bytes INTEGER,seconds REAL);''')
            existing=c.execute('SELECT value FROM identity WHERE id=1').fetchone()
            if existing and existing[0]!=self.identity: raise ValueError('Run identity/configuration mismatch; preserve run and use a new directory')
            c.execute('INSERT OR IGNORE INTO identity VALUES (1,?)',(self.identity,))
            c.execute('INSERT OR IGNORE INTO state VALUES (1,?)',((self.env/'initial_state.json').read_text(),))

    def connection(self):
        c=sqlite3.connect(self.archive.as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
        return c

    def public_document(self,row):
        return {k:row[k] for k in ('id','source','title','year','format','origin','sha256')}

    def asset_bytes(self,row):
        if row['source']!='external':return row['asset']
        root=self.corpus.parent.parent
        path=(root/json.loads(row['metadata'])['path']).resolve()
        try:path.relative_to(root)
        except ValueError:raise Invalid('invalid_source','Source path outside pinned archive',503)
        if path.is_file():data=path.read_bytes()
        elif Path(str(path)+'.gz').is_file():data=gzip.decompress(Path(str(path)+'.gz').read_bytes())
        else:raise Invalid('source_unavailable','Pinned source asset is unavailable',503)
        if hashlib.sha256(data).hexdigest()!=row['sha256']:raise Invalid('source_integrity','Pinned source asset changed',503)
        return data

    def state_public(self,s):
        return {'year':s['year'],'annual_budget_units':240,'spent_this_year':s['spent'],
          'timber_delivered_this_year':s['delivered'],'jobs':s['jobs'],'observations':s['published'],
          'objective_proposals':s['proposals'],'closed':s['closed']}

    def dispatch(self,operation,body):
        if operation not in FIELDS: raise Invalid('unknown_operation','Unsupported public operation',404)
        if not isinstance(body,dict): raise Invalid('invalid_request','JSON object required')
        if set(body)-FIELDS[operation]-{'request_id'}: raise Invalid('unknown_field','Unsupported field')
        rid=text(body.get('request_id'),'request_id',120)
        digest=hashlib.sha256((operation+'\0'+js(body)).encode()).hexdigest()
        with self.lock,sqlite3.connect(self.db) as c:
            c.execute('BEGIN IMMEDIATE')
            old=c.execute('SELECT body_sha,response FROM events WHERE id=?',(rid,)).fetchone()
            if old:
                if old[0]!=digest: raise Invalid('request_conflict','Request ID already committed with different contents',409)
                return json.loads(old[1])
            s=json.loads(c.execute('SELECT payload FROM state WHERE id=1').fetchone()[0])
            if s['closed']: raise Invalid('session_closed','Final report already submitted',409)
            result=self.perform(operation,body,s)
            encoded=js(result)
            c.execute('UPDATE state SET payload=? WHERE id=1',(js(s),))
            c.execute('INSERT INTO events VALUES (?,?,?,?,?)',(rid,digest,operation,js(body),encoded))
            return result

    def perform(self,operation,b,s):
        if operation=='mission': return {'mission':self.mission,'operations':OPERATIONS}
        if operation=='sources':
            with self.connection() as c: return {'sources':[dict(r) for r in c.execute('SELECT * FROM sources ORDER BY id')]}
        if operation=='people':
            with self.connection() as c: return {'people':[dict(r) for r in c.execute('SELECT id,role FROM people ORDER BY id')]}
        if operation=='status': return self.state_public(s)
        if operation=='search':
            query=b.get('query','');source=b.get('source')
            if not isinstance(query,str) or len(query)>1000: raise Invalid('invalid_query','query')
            if source is not None: text(source,'source',100)
            offset=integer(b.get('offset',0),0,100000,'offset');limit=integer(b.get('limit',30),1,100,'limit')
            tokens=re.findall(r'\w+',query.casefold())
            with self.connection() as c: rows=list(c.execute('SELECT * FROM documents ORDER BY id'))
            if source: rows=[r for r in rows if r['source']==source]
            def score(r):
                hay=(r['title']+' '+r['body']+' '+r['metadata']).casefold()
                return sum(t in hay for t in tokens)
            if tokens: rows=[r for r in rows if score(r)>0];rows.sort(key=lambda r:(-score(r),r['id']))
            page=rows[offset:offset+limit]
            return {'items':[self.public_document(r) for r in page],'total':len(rows),'offset':offset,'has_more':offset+len(page)<len(rows)}
        if operation in ('read','records'):
            doc=text(b.get('document_id'),'document_id',100)
            with self.connection() as c: r=c.execute('SELECT * FROM documents WHERE id=?',(doc,)).fetchone()
            if not r:
                pub=next((x for x in s['published'] if x['id']==doc),None)
                if pub and operation=='read': return {'id':doc,'body':js(pub),'origin':'constructed_measurement'}
                raise Invalid('unavailable','No such admitted archive document',404)
            metadata=json.loads(r['metadata'])
            if operation=='records':
                fid=metadata.get('original_file_id')
                if not fid: raise Invalid('unsupported','Use read for this native document; structured external rows unavailable',422)
                offset=integer(b.get('offset',0),0,100000,'offset');limit=integer(b.get('limit',100),1,200,'limit')
                with sqlite3.connect(self.corpus.as_uri()+'?mode=ro',uri=True) as c:
                    rows=c.execute('SELECT record_id,selector,payload_json FROM records WHERE file_id=? ORDER BY record_id LIMIT ? OFFSET ?',(fid,limit+1,offset)).fetchall()
                return {'document_id':doc,'offset':offset,'has_more':len(rows)>limit,'rows':[{'record_id':r[0],'selector':r[1],'payload':json.loads(r[2])} for r in rows[:limit]]}
            result={**self.public_document(r),'body':r['body'][:60000],'body_truncated':len(r['body'])>60000,'metadata':metadata}
            if type(b.get('include_asset',False))is not bool: raise Invalid('invalid_asset','include_asset must be boolean')
            if b.get('include_asset'):
                offset=integer(b.get('asset_offset',0),0,50000000,'asset_offset')
                limit=integer(b.get('asset_limit',32768),1,65536,'asset_limit')
                asset=self.asset_bytes(r);part=asset[offset:offset+limit]
                result['asset']={'encoding':'base64','offset':offset,'total_bytes':len(asset),'has_more':offset+len(part)<len(asset),'data':base64.b64encode(part).decode()}
            return result
        if operation=='ask':
            person=text(b.get('person_id'),'person_id',100);question=text(b.get('question'),'question')
            with self.connection() as c: row=c.execute('SELECT role,knowledge FROM people WHERE id=?',(person,)).fetchone()
            if row is None: raise Invalid('unavailable','No registered role',404)
            return {'person_id':person,'question':question,'response_kind':'bounded_record_disclosure',
                'materials':json.loads(row['knowledge']),
                'limitation':'These are this role\'s recorded statements. No additional answer is inferred; unsupported details remain unknown.'}
        if operation in ('measure','act'):
            ids=b.get('plots')
            if not isinstance(ids,list) or not 1<=len(ids)<=12 or any(not isinstance(x,str) for x in ids) or len(set(ids))!=len(ids):
                raise Invalid('invalid_plots','Provide 1..12 distinct registered stand IDs')
            if set(ids)-{p['id'] for p in s['plots']}: raise Invalid('unavailable','Unknown stand',404)
            if len([j for j in s['jobs'] if j['status']=='pending'])>=100: raise Invalid('capacity','Pending work limit',429)
            due=integer(b.get('year',s['year']+1),s['year']+1,min(50,s['year']+5),'year')
            job={'id':'J'+str(s['next_job']),'plots':ids,'due_year':due,'status':'pending'}
            if operation=='measure':
                metric=b.get('metric')
                if metric not in ('insects','enemies','foliage','fir','spruce','birch','age'): raise Invalid('unsupported','Instrument not available',422)
                job.update(kind='measure',metric=metric,cost=2*len(ids))
            else:
                kind=b.get('kind')
                if kind=='treat':
                    if set(b)&{'fraction'}: raise Invalid('incompatible_field','fraction is for harvest')
                    method=b.get('method');dose=number(b.get('dose'),0.,1.,'dose')
                    if method not in ('broad','selective'): raise Invalid('unsupported','Unknown treatment method',422)
                    job.update(kind=kind,method=method,dose=dose,cost=dose*len(ids)*(8 if method=='broad' else 11))
                elif kind=='harvest':
                    if set(b)&{'method','dose'}: raise Invalid('incompatible_field','method/dose are for treatment')
                    fraction=number(b.get('fraction'),0.,.35,'fraction')
                    job.update(kind=kind,fraction=fraction,cost=5*fraction*len(ids))
                else: raise Invalid('unsupported','Supported physical actions are treat and harvest',422)
                # One job per intervention kind/stand/year avoids undefined overlapping treatments.
                if any(j['status']=='pending' and j['due_year']==due and j['kind']==kind and set(j['plots'])&set(ids) for j in s['jobs']):
                    raise Invalid('schedule_conflict','Overlapping intervention already scheduled',409)
            reserved=sum(j['cost'] for j in s['jobs'] if j['status']=='pending' and j['due_year']==due)
            if reserved+job['cost']>240: raise Invalid('budget_exceeded','Annual scheduled work exceeds authorization',409)
            if operation=='measure':
                # Cost is paid when work executes; all scheduled work shares the annual envelope.
                pass
            s['jobs'].append(job);s['next_job']+=1
            return {'status':'scheduled','job':job,'measurement_available_after':'advance to due year'}
        if operation=='advance':
            years=integer(b.get('years',1),1,5,'years')
            if s['year']+years>50: raise Invalid('horizon','World horizon reached',409)
            released=[]
            for _ in range(years):
                year=s['year']+1;weather=world.climate(s['seed'],year)
                due=[j for j in s['jobs'] if j['status']=='pending' and j['due_year']==year]
                spent=sum(j['cost'] for j in due);delivered=0.;plots=[];metrics=[]
                for p in s['plots']:
                    treatment=next((j for j in due if j['kind']=='treat' and p['id'] in j['plots']),None)
                    harvesting=next((j for j in due if j['kind']=='harvest' and p['id'] in j['plots']),None)
                    nxt,m=world.step(p,weather,treatment,harvesting['fraction'] if harvesting else 0.)
                    plots.append(nxt);metrics.append(m);delivered+=m['timber_units']
                for job in due:
                    job['status']='executed';job['executed_year']=year
                    if job['kind']=='measure':
                        readings=[world.observe(s['seed'],year,p,job['metric'],job['id']) for p in plots if p['id'] in job['plots']]
                        item={'id':'O'+job['id'],'job_id':job['id'],'year':year,'origin':'constructed_measurement','readings':readings}
                        released.append(item);s['published'].append(item)
                # Routine reports are observations with declared scope, not a hidden-state dump.
                public={'id':'R'+str(year),'year':year,'origin':'constructed_routine_report',
                    'mean_observed_foliage':sum(world.observe(s['seed'],year,p,'foliage','routine')['value'] for p in plots)/len(plots),
                    'operational_spending_units':spent,'timber_delivered_units':delivered,'contract_units':18 if year<=5 else None,
                    'delivery_shortfall_units':max(0.,18-delivered) if year<=5 else None}
                s['published'].append(public);released.append(public)
                s['outcomes'].append({'year':year,'metrics':metrics,'plots':plots,'spent':spent,'delivered':delivered})
                s.update(year=year,plots=plots,spent=spent,delivered=delivered)
            return {'year':s['year'],'published':released,'status':'advanced'}
        if operation=='propose':
            proposal={'id':'P'+str(len(s['proposals'])+1),'year':s['year'],
                'objective':text(b.get('objective'),'objective'),'reason':text(b.get('reason'),'reason'),
                'status':'pending_human_review','original_objective_unchanged':True}
            s['proposals'].append(proposal);return proposal
        if operation=='submit':
            conclusion=text(b.get('conclusion'),'conclusion',20000)
            for name in ('recommendations','uncertainties','evidence_ids'):
                if not isinstance(b.get(name,[]),list) or len(b.get(name,[]))>100 or any(not isinstance(x,str) or len(x)>8000 for x in b.get(name,[])):
                    raise Invalid('invalid_list',name)
            # Citations must be acquired document/observation IDs, not guesses from catalogue metadata.
            acquired={x['id'] for x in s['published']}
            with sqlite3.connect(self.db) as c:
                for op,response in c.execute("SELECT operation,response FROM events WHERE operation IN ('read','ask')"):
                    value=json.loads(response)
                    if op=='read':acquired.add(value['id'])
                    else:acquired.update(x['document_id'] for x in value['materials'])
            if set(b.get('evidence_ids',[]))-acquired: raise Invalid('unseen_evidence','Cite acquired documents or published observations')
            if 'forecast'in b and (not isinstance(b['forecast'],dict) or len(js(b['forecast']))>20000): raise Invalid('invalid_forecast','forecast object')
            s['final']={'year':s['year'],**b};s['closed']=True
            return {'status':'accepted','message':'Report retained. No evaluator answer or reward is returned.'}
        raise Invalid('unsupported','Operation not implemented',422)


def server(environment,run,corpus,token,port=0):
    if not isinstance(token,str) or len(token)<24: raise ValueError('Use a fresh token of at least 24 characters')
    broker=Broker(environment,run,corpus)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*a): pass
        def reply(self,status,value):
            data=js(value).encode()
            with broker.lock,sqlite3.connect(broker.db) as c:
                c.execute('INSERT INTO attempts(operation,status,bytes,seconds) VALUES (?,?,?,?)',
                    (self.path,status,len(data),time.perf_counter()-self.started))
            self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        def do_POST(self):
            self.started=time.perf_counter()
            if not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+token):return self.reply(401,{'status':'denied'})
            try:
                if not self.path.startswith('/v2/'):raise Invalid('not_found','Unknown path',404)
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<=131072:raise Invalid('request_size','Body must be 1..131072 bytes',413)
                self.connection.settimeout(5)
                def reject(x):raise ValueError('Nonfinite number')
                body=json.loads(self.rfile.read(n),parse_constant=reject)
                result=broker.dispatch(self.path[4:],body);self.reply(200,result)
            except Invalid as e:self.reply(e.status,{'status':'error','code':e.code,'message':e.message})
            except (ValueError,TypeError):self.reply(400,{'status':'error','code':'invalid_request'})
            except TimeoutError:self.reply(408,{'status':'error','code':'read_timeout'})
    http=ThreadingHTTPServer(('127.0.0.1',port),Handler);http.broker=broker
    return http


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--environment',type=Path,required=True);p.add_argument('--run',type=Path,required=True)
    p.add_argument('--corpus',type=Path,required=True);p.add_argument('--port',type=int,default=8766);a=p.parse_args()
    http=server(a.environment,a.run,a.corpus,os.environ.get('EDI_BENCHMARK_TOKEN',''),a.port)
    print('Listening on loopback port',http.server_port,flush=True)
    try:http.serve_forever()
    except KeyboardInterrupt:pass
    finally:http.server_close()
