"""Build a declared constructed archive and private starting state; no model inference."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import sqlite3
from pathlib import Path
from PIL import Image, ImageDraw
import world

SOURCES = {
 'field': ('District survey office', 'Branch counts, trap logs and sampling notebooks'),
 'forest': ('Forest inventory service', 'Stand inventories, age estimates and canopy surveys'),
 'weather': ('Weather station', 'Seasonal instrument readings'),
 'operations': ('Operations archive', 'Treatment orders, harvest logs and work records'),
 'finance': ('District accounts', 'Invoices, budgets, payroll and supply commitments'),
 'laboratory': ('Laboratory archive', 'Feeding, treatment and chemistry trial sheets'),
 'correspondence': ('Correspondence registry', 'Minutes, complaints and institutional statements'),
 'maps': ('Cartographic office', 'Stand maps and survey heat maps'),
 'administration': ('General administration', 'Road access, staff rosters, stores and routine logs'),
 'external': ('External reference collection', 'Attributed real-domain records outside this constructed district')}


def js(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False, allow_nan=False)


def csv_bytes(rows):
    s = io.StringIO(newline='')
    keys = list(dict.fromkeys(k for r in rows for k in r))
    w = csv.DictWriter(s, fieldnames=keys)
    w.writeheader(); w.writerows(rows)
    return s.getvalue().encode()


def build(destination, corpus, seed=7021):
    if destination.exists():
        raise ValueError('Choose a new destination; existing build is never overwritten')
    destination.mkdir(parents=True)
    archive = sqlite3.connect(destination / 'archive.sqlite')
    archive.executescript('''CREATE TABLE sources(id TEXT PRIMARY KEY,title TEXT,description TEXT);
    CREATE TABLE documents(id TEXT PRIMARY KEY,source TEXT,title TEXT,year INTEGER,format TEXT,
      origin TEXT,body TEXT,metadata TEXT,asset BLOB,sha256 TEXT);
    CREATE TABLE people(id TEXT PRIMARY KEY,role TEXT,knowledge TEXT);
    CREATE INDEX documents_source ON documents(source);
    CREATE INDEX documents_year ON documents(year);''')
    for key, (title, description) in SOURCES.items():
        archive.execute('INSERT INTO sources VALUES (?,?,?)', (key, title, description))

    def put(source, title, year, fmt, body, asset=None, metadata=None, origin='constructed_record'):
        asset = body.encode() if asset is None else asset
        digest = hashlib.sha256(asset).hexdigest()
        identity = 'D' + hashlib.sha256((source + title + str(year) + digest).encode()).hexdigest()[:22]
        archive.execute('INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?,?)',
            (identity, source, title, year, fmt, origin, body, js(metadata or {}), b'' if source=='external' else asset, digest))
        return identity

    rows, plots = world.history(seed)
    series_ids={}
    units = {'insects':'larvae per 75 cm branch','enemies':'trap activity index',
             'foliage':'baseline foliage fraction','fir':'stand fraction','spruce':'stand fraction',
             'birch':'stand fraction','age':'estimated years'}
    for end in range(-70, 1, 10):
        chunk = [r for r in rows if end-9 <= r['year'] <= end]
        for metric, source in [('insects','field'),('enemies','field'),('foliage','forest'),
                               ('fir','forest'),('spruce','forest'),('birch','forest'),('age','forest')]:
            measurements = [{'year':r['year'],'station':r['plot'], 'reading':round(r[metric]*(1+.04*(2*world.noise(seed,'archive',metric,r['year'],r['plot'])-1)),5),
                             'unit':units[metric],'instrument_code':'F-2' if metric=='enemies' else 'A-1'} for r in chunk]
            title = '%s observation sheets %s to %s' % (metric, end-9, end)
            data = csv_bytes(measurements)
            series_ids[(metric,end)]=put(source, title, end, 'csv', data.decode(), data, {'sampling':'routine recorded samples; relative error up to 4%','series':metric})
        treatment = [{'year':r['year'],'work_unit':r['plot'],'method':r['method'],
                      'dose_fraction':r['treatment_dose'],'invoice_units':round(r['protection_cost'],3)} for r in chunk]
        data = csv_bytes(treatment)
        put('operations','Completed protection work %s to %s'%(end-9,end),end,'csv',data.decode(),data)
        data = csv_bytes([{'year':r['year'],'station':r['plot'],'temperature_anomaly_C':r['temperature_anomaly_C'],
                           'spring_rain_mm':r['spring_rain_mm']} for r in chunk if r['plot']=='S01'])
        put('weather','Station spring register %s to %s'%(end-9,end),end,'csv',data.decode(),data)
        for family in ('road_inspection','staff_roster','needle_chemistry','stores_batch'):
            values=[{'year':y,'location':'district','code':family,'reading':round(10+90*world.noise(seed,family,y),3)} for y in range(end-9,end+1)]
            data=csv_bytes(values)
            put('administration',family.replace('_',' ')+' register %s to %s'%(end-9,end),end,'csv',data.decode(),data)
        # Duplicated reports retain explicit source lineage rather than adding independent observations.
        summary = {'period':[end-9,end],'mean_insects':sum(r['insects'] for r in chunk)/len(chunk),
                   'programme_spending_units':sum(r['protection_cost'] for r in chunk)}
        base=put('finance','Annual accounts compilation ending '+str(end),end,'json',js(summary))
        put('correspondence','Office bulletin '+str(end),end,'txt','The accounts compilation is attached by reference.\n'+base,
            metadata={'derived_from':[base]})

    # Raw trial sheets, not explanatory conclusions. Trials are frozen before participant inquiries.
    trials=[]
    base_state={'id':'LAB','fir':.6,'spruce':.25,'birch':.15,'foliage':.8,'insects':1.,'enemies':.7,'stress':.1,'age':60.,'x':0,'y':0}
    for method in ('broad','selective'):
        for dose in (0.,.25,.5,1.):
            for rep in range(6):
                nxt,metrics=world.step(base_state,{'temperature_anomaly_C':0.,'spring_rain_mm':90.},{'method':method,'dose':dose})
                trials.append({'trial':len(trials)+1,'method':method,'dose_fraction':dose,'initial_larvae':1.,
                    'initial_enemy_index':.7,'subsequent_enemy_index':round(nxt['enemies']*(1+.03*(2*world.noise(seed,'trial',method,dose,rep)-1)),5),
                    'subsequent_larvae':round(nxt['insects'],5),'replicate':rep+1})
    data=csv_bytes(trials)
    put('laboratory','Treatment enclosure trial register',-2,'csv',data.decode(),data,{'conditions':'Matched starting state and weather; constructed enclosure trials, not field efficacy estimates'})
    feeding=[{'prey_per_trial':b,'enemy_activity':e,'prey_consumed':round(2.3*e*b*b/(.35**2+b*b),5)}
             for b in (.02,.05,.1,.3,.7,1.,2.,4.,8.) for e in (.3,.6,.9)]
    data=csv_bytes(feeding)
    put('laboratory','Feeding tray register',-3,'csv',data.decode(),data,{'unit':'standardized trial equivalents'})
    text='Branch samples use 75 cm equivalents. Trap F-2 is an activity index; it is not a count of all predators or a disease assay. Codes F, S and B on inventory sheets denote fir, spruce and birch. Missing records do not imply zero. Sampling counts and species scope must be read from the native sheet.'
    put('field','Instrument and inventory notes',-1,'txt',text)
    spatial={'type':'FeatureCollection','features':[{'type':'Feature','properties':{'stand':p['id']},
              'geometry':{'type':'Point','coordinates':[p['x'],p['y']]}} for p in plots]}
    put('maps','District stand locator',0,'geojson',js(spatial),metadata={'coordinate_system':'constructed district grid, not geographic longitude/latitude'})
    for metric in ('insects','foliage','enemies'):
        im=Image.new('RGB',(560,330),'white');draw=ImageDraw.Draw(im)
        draw.text((12,8),metric+' survey, simulation year 0 — CONSTRUCTED',fill='black')
        values=[{**r,metric:round(r[metric]*(1+.04*(2*world.noise(seed,'archive',metric,r['year'],r['plot'])-1)),5)} for r in rows if r['year']==0]
        upper=max(r[metric] for r in values)
        for r in values:
            intensity=int(230*min(1,r[metric]/max(upper,.01)))
            x=25+125*r['x'];y=48+78*r['y']
            draw.rectangle((x,y,x+110,y+62),fill=(255,255-intensity,255-intensity),outline='black')
            draw.text((x+5,y+7),r['plot'],fill='black')
            draw.text((x+5,y+28),str(round(r[metric],3)),fill='black')
        draw.text((12,300),'Scale: white=0; red='+str(round(upper,3))+'; '+units[metric],fill='black')
        stream=io.BytesIO();im.save(stream,format='PNG')
        put('maps',metric+' survey heat map',0,'png','Survey heat map, '+metric+'; see original image legend.',stream.getvalue(),
            {'derived_from':[series_ids[(metric,0)]],'observation_year':0,'representation':'visualization of the same recorded samples, not an independent field photograph'})
    documents={
      'manager':('District manager','The district is expected to maintain a timber supply and reduce recurring damage and expenditure. Existing procurement favors fir and spruce. Changes to commitments or priorities require a management decision.'),
      'mill':('Mill liaison','Orders require 18 timber units per year for the next five years. Delivery deficits must be recorded. We buy fir and spruce. Stable deliveries affect employment.'),
      'community':('Community secretary','Residents have filed concerns about broad-area chemical use, water and non-target wildlife. There is disagreement about acceptable tradeoffs with local employment. No unanimous numeric utility weighting exists.'),
      'accounts':('Accounts clerk','The current authorized annual operational envelope is 240 accounting units. Sampling, treatments and harvesting share it. Historical provincial totals and local invoices have different scopes.'),
      'archivist':('Records custodian','The archive contains records from simulation years -79 through 0. Collections can be browsed without a search phrase. Historical tree cores and pathogen assays were not collected in this constructed district. New supported measurements can be commissioned; past missing measurements cannot be recovered.')}
    people=[]
    for key,(role,text) in documents.items():
        doc=put('correspondence',role+' registry statement',0,'txt',text)
        knowledge=[{'text':text,'document_id':doc}]
        archive.execute('INSERT INTO people VALUES (?,?,?)',(key,role,js(knowledge)))
        people.append({'id':key,'role':role})
    for y in (-65,-40,-20,-5,0):
        text=('Procurement register: '+('white-pine buyers accepted mixed local stands; few spruce/fir contracts were recorded.' if y<-40 else
             'fir and spruce supply contracts are recorded; management expenditure is charged to the protection programme.')+
             ' Simulation year '+str(y)+'. Constructed administrative record; quantities not reconstructed from historical Canada.')
        put('finance','Procurement ledger '+str(y),y,'txt',text)
    # Expose the full existing source collection by document and records, preserving origin and lineage.
    original=sqlite3.connect('file:'+str(corpus.resolve())+'?mode=ro',uri=True);original.row_factory=sqlite3.Row
    corpus_root=corpus.parent.parent
    external_count=0
    for f in original.execute('SELECT * FROM evidence_files ORDER BY file_id'):
        path=corpus_root/f['path']
        if path.exists():asset=path.read_bytes()
        elif Path(str(path)+'.gz').exists():asset=gzip.decompress(Path(str(path)+'.gz').read_bytes())
        else:raise FileNotFoundError(str(path))
        if hashlib.sha256(asset).hexdigest()!=f['sha256']:raise ValueError('Source hash mismatch '+f['file_id'])
        text='\n'.join(r[0] for r in original.execute('SELECT text FROM text_blocks WHERE file_id=?',(f['file_id'],)))
        put('external',f['description'],None,f['format'],text,asset,
            {'original_file_id':f['file_id'],'source_id':f['source_id'],'role':f['role'],
             'root_evidence_group':f['root_evidence_group'],'path':f['path'],
             'scope':'External modern/domain reference; not measurements of this simulated district.'},origin=f['origin'])
        external_count+=1
    original.close()
    archive.commit()
    counts={'documents':archive.execute('SELECT count(*) FROM documents').fetchone()[0],
            'sources':len(SOURCES),'people':people,'external_assets':external_count,
            'formats':[r[0] for r in archive.execute('SELECT DISTINCT format FROM documents ORDER BY format')]}
    archive.close()
    mission={'scenario':'Cedar District constructed development world v0.2','origin':'Constructed ecology and institutions; attributed external records remain external.',
      'objective':'Investigate recurring forest damage and protection expenditure, and recommend or undertake authorized measures while maintaining district obligations.',
      'authority':'You may inspect records, ask registered roles, commission supported measurements, schedule treatments/harvest, advance the world and propose a revised objective. No hypothesis or policy menu is supplied.',
      'initial_year':0,'annual_budget_units':240,'maximum_world_year':50,
      'limits':'Not a historical reconstruction. Operator model, future state and evaluation files are private. No completed EDI benchmark is claimed.'}
    (destination/'mission.json').write_text(json.dumps(mission,indent=2)+'\n')
    (destination/'initial_state.json').write_text(json.dumps({'version':world.VERSION,'seed':seed,'year':0,'plots':plots,
           'spent':0.,'delivered':0.,'jobs':[],'next_job':1,'closed':False,'published':[],
           'outcomes':[],'proposals':[]},indent=2)+'\n')
    data=(destination/'archive.sqlite').read_bytes()
    (destination/'archive.sqlite.gz').write_bytes(gzip.compress(data,mtime=0))
    counts.update({'origin':'constructed development archive plus attributed external source assets',
       'archive_sha256':hashlib.sha256(data).hexdigest(),
       'archive_gzip_sha256':hashlib.sha256((destination/'archive.sqlite.gz').read_bytes()).hexdigest(),
       'world_sha256':hashlib.sha256(Path(world.__file__).read_bytes()).hexdigest(),
       'initial_state_sha256':hashlib.sha256((destination/'initial_state.json').read_bytes()).hexdigest(),
       'mission_sha256':hashlib.sha256((destination/'mission.json').read_bytes()).hexdigest(),
       'source_corpus_sha256':hashlib.sha256(corpus.read_bytes()).hexdigest(),
       'historical_rows':len(rows),'model_calibrated':False,'edi_run':False})
    (destination/'manifest.json').write_text(json.dumps(counts,indent=2)+'\n')
    return counts


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--corpus',type=Path,required=True)
    a=p.parse_args();print(json.dumps(build(a.out,a.corpus),indent=2))
