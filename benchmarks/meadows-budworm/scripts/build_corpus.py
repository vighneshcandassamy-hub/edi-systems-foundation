"""Build the versioned evidence archive from downloaded primary-source snapshots.

The database indexes supplied evidence; it does not encode ecological truth or
run EDI. Optional scientific dependencies are used only for file extraction and
derived views. Native bytes are retained unchanged.
"""
import argparse
import csv
import datetime as dt
import gzip
import hashlib
import html
import io
import json
import math
import re
import shutil
import sqlite3
import subprocess
import wave
from decimal import Decimal
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

SCHEMA = '''
PRAGMA foreign_keys=ON;
CREATE TABLE corpus_meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE sources(source_id TEXT PRIMARY KEY,title TEXT NOT NULL,publisher TEXT NOT NULL,source_url TEXT NOT NULL,license_note TEXT NOT NULL,role TEXT NOT NULL,scope_note TEXT NOT NULL);
CREATE TABLE knowledge_areas(area_id TEXT PRIMARY KEY,description TEXT NOT NULL);
CREATE TABLE evidence_files(file_id TEXT PRIMARY KEY,path TEXT UNIQUE NOT NULL,source_id TEXT NOT NULL REFERENCES sources,sha256 TEXT NOT NULL,size_bytes INTEGER NOT NULL,format TEXT NOT NULL,origin TEXT NOT NULL,role TEXT NOT NULL,description TEXT NOT NULL,retrieved_at TEXT NOT NULL,root_evidence_group TEXT NOT NULL);
CREATE TABLE file_areas(file_id TEXT REFERENCES evidence_files,area_id TEXT REFERENCES knowledge_areas,PRIMARY KEY(file_id,area_id));
CREATE TABLE lineage(child_file_id TEXT REFERENCES evidence_files,parent_file_id TEXT REFERENCES evidence_files,relation TEXT NOT NULL,details TEXT NOT NULL,PRIMARY KEY(child_file_id,parent_file_id));
CREATE TABLE records(record_id TEXT PRIMARY KEY,file_id TEXT NOT NULL REFERENCES evidence_files,selector TEXT NOT NULL,series TEXT NOT NULL,event_time TEXT,event_year INTEGER,latitude REAL,longitude REAL,payload_json TEXT NOT NULL,UNIQUE(file_id,selector));
CREATE INDEX records_series_time ON records(series,event_time);
CREATE INDEX records_year ON records(event_year);
CREATE INDEX records_location ON records(latitude,longitude);
CREATE TABLE text_blocks(block_id TEXT PRIMARY KEY,file_id TEXT NOT NULL REFERENCES evidence_files,selector TEXT NOT NULL,text TEXT NOT NULL,role TEXT NOT NULL);
CREATE VIRTUAL TABLE text_search USING fts5(block_id UNINDEXED,file_id UNINDEXED,text);
CREATE TABLE evidence_gaps(gap_id TEXT PRIMARY KEY,area_id TEXT REFERENCES knowledge_areas,description TEXT NOT NULL,consequence TEXT NOT NULL);
CREATE VIEW observation_files AS SELECT * FROM evidence_files WHERE role='observation';
CREATE VIEW reference_files AS SELECT * FROM evidence_files WHERE role='reference';
'''


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
        if tag in ('p', 'div', 'h1', 'h2', 'h3', 'li', 'br'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip-1)
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def dumps(value): return json.dumps(value, ensure_ascii=False, allow_nan=False, default=str)


def build(downloads, root):
    import fitz
    import numpy as np
    import openpyxl
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from PIL import Image

    for sub in ('data/raw', 'data/derived', 'database', 'metadata', 'docs'):
        (root/sub).mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).isoformat()
    dbpath = root/'database/evidence.sqlite'
    staged = root/'database/.evidence.building.sqlite'
    for candidate in (staged,Path(str(staged)+'-journal')):
        if candidate.exists():candidate.unlink()
    db = sqlite3.connect(staged); db.execute('PRAGMA journal_mode=DELETE'); db.executescript(SCHEMA)
    (root/'database/schema.sql').write_text(SCHEMA, encoding='utf-8')
    db.executemany('INSERT INTO corpus_meta VALUES (?,?)', [
        ('version','0.1.0'), ('created_at',stamp), ('scope','Meadows budworm evidence seed corpus'),
        ('status','BUILT_NOT_BENCHMARKED'), ('previous_database','Unavailable; this is a new reconstruction, not a byte-identical recovery.'),
        ('identity_rule','Record identity is file content hash plus native selector. Root groups express shared evidence, not physical entity identity.'),
        ('null_rule','Original strings, nulls, source flags and negative sentinel codes are retained. Undocumented codes remain uninterpreted.')])
    areas = {
        'population':'Larval and adult insect population observations and sampling effort',
        'forest':'Host trees, stand attributes, forest ecology and forest uses',
        'weather':'Daily meteorological measurements and station metadata',
        'management':'Monitoring, treatment, institutions, stated objectives and decisions',
        'space_time':'Locations, chronology, geometry and asynchronous observations',
        'methods':'Sampling methods, uncertainty, reporting and extraction limitations'}
    db.executemany('INSERT INTO knowledge_areas VALUES (?,?)', areas.items())
    definitions = {
        'nb_l2': ('NB spruce budworm L2 survey','Government of New Brunswick','https://gnb.socrata.com/datasets/e4t9-ku3d','New Brunswick Open Government Licence (publisher metadata licenseId NBOGL).','observation','2017-2025 provincial survey. CSV and GeoJSON are alternate exports of the same observations.'),
        'nb_moths': ('NB spruce budworm pheromone trapping','Government of New Brunswick','https://gnb.socrata.com/datasets/bw6q-5rw4','New Brunswick Open Government Licence; retained publisher metadata.','observation','Trap data and original codes. Negative sentinel values are preserved, not treated as valid counts.'),
        'nrcan_larvae': ('SBW L2/L4 samples and defoliation 1998-2022','Natural Resources Canada','https://open.canada.ca/data/en/dataset/42ca63ee-aa9a-4437-8810-7d54d328229e','Government of Canada open-data distribution. Exact dataset licence could not be independently retrieved; confirm before public redistribution.','observation','Study spans Ottawa River valley, North Shore and NB. Sheet row order is not an undocumented cross-sheet join key.'),
        'eccc_weather': ('Fredericton CDA CS daily weather 2022-2023','Environment and Climate Change Canada','https://api.weather.gc.ca/collections/climate-daily','Open Government Licence - Canada. Preserve station flags and API metadata.','observation','One station and two years. Regional context only: no asserted weather-to-survey-site match.'),
        'maine_report': ('Spruce Budworm in Maine 2021, March 2022','Maine Forest Service / Michael Parisio','https://www.sprucebudwormmaine.org/wp-content/uploads/2022/03/MFS-Spruce-Budworm-in-Maine-2021-Final-Report.pdf','Publicly distributed agency report. No blanket redistribution licence verified; retained in private research archive with attribution.','reference','16-page report includes human explanations, methods, charts, photographs and treatment maps; not blind raw evidence.'),
        'usfs_fir': ('Silvics: Balsam Fir','USDA Forest Service','https://research.fs.usda.gov/silvics/balsam-fir','US federal government text; third-party credits, if any, retain their own rights.','reference','Species reference and forest uses, not contemporaneous stand measurements.'),
        'usfs_spruce': ('Silvics: Black Spruce','USDA Forest Service','https://research.fs.usda.gov/silvics/black-spruce','US federal government text; third-party credits, if any, retain their own rights.','reference','Species reference, not observed stand age/foliage time series.')}
    db.executemany('INSERT INTO sources VALUES (?,?,?,?,?,?,?)',[(k,*v) for k,v in definitions.items()])
    inventory = []; bypath = {}; rows_all = []; records_by_series = Counter()

    def register(path, source, fmt, origin, description, area_ids, parents=(), role=None):
        p = root/path; sha = digest(p); fid = 'f_'+sha[:24]
        group = source
        r = role or definitions[source][4]
        db.execute('INSERT INTO evidence_files VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                   (fid,path,source,sha,p.stat().st_size,fmt,origin,r,description,'2026-10-21 (receipt date; per-file clock time not captured)',group))
        for a in area_ids: db.execute('INSERT INTO file_areas VALUES (?,?)',(fid,a))
        for par,rel,detail in parents: db.execute('INSERT INTO lineage VALUES (?,?,?,?)',(fid,bypath[par],rel,detail))
        bypath[path]=fid
        inventory.append(dict(file_id=fid,path=path,source_id=source,sha256=sha,size_bytes=p.stat().st_size,format=fmt,origin=origin,role=r,root_evidence_group=group,description=description))
        return fid

    def record(fid,selector,series,payload,event_time=None,event_year=None,lat=None,lon=None):
        rid='r_'+hashlib.sha256((fid+'\0'+selector).encode()).hexdigest()[:28]
        db.execute('INSERT INTO records VALUES (?,?,?,?,?,?,?,?,?)',(rid,fid,selector,series,event_time,event_year,lat,lon,dumps(payload)))
        records_by_series[series]+=1
        rows_all.append(dict(record_id=rid,file_id=fid,selector=selector,series=series,event_time=event_time,event_year=event_year,latitude=lat,longitude=lon,payload=payload))
        return rid

    def text(fid,selector,value,role):
        value=value.strip()
        if not value:return
        bid='t_'+hashlib.sha256((fid+'\0'+selector).encode()).hexdigest()[:28]
        db.execute('INSERT INTO text_blocks VALUES (?,?,?,?,?)',(bid,fid,selector,value,role))
        db.execute('INSERT INTO text_search VALUES (?,?,?)',(bid,fid,value))

    log=json.loads((downloads/'download-log.json').read_text())
    mapping={
        'l2.csv':('nb_l2','csv','All downloaded survey rows; source fields unchanged.',['population','forest','space_time','methods']),
        'l2_metadata.json':('nb_l2','json','Publisher dataset description, licence and field definitions.',['methods']),
        'l2_native.geojson':('nb_l2','geojson','Native spatial export; same underlying survey as CSV, not additional observations.',['population','space_time']),
        'pheromone.csv':('nb_moths','csv','All downloaded trap rows; preserve original negative codes.',['population','forest','space_time']),
        'pheromone_metadata.json':('nb_moths','json','Publisher trap dataset metadata.',['methods']),
        'larval_study.xlsx':('nrcan_larvae','xlsx','Original study workbook, four sheets; no edits or inferred row joins.',['population','forest','methods']),
        'weather.json':('eccc_weather','geojson','730 native daily weather features with measurement flags.',['weather','space_time']),
        'weather_collection.json':('eccc_weather','json','Official ECCC collection metadata and field context.',['methods','weather']),
        'maine_report.pdf':('maine_report','pdf','Original complete report with maps, charts and narrative.',['population','management','methods','forest']),
        'balsam_fir.html':('usfs_fir','html','Original species-reference HTML.',['forest','methods']),
        'black_spruce.html':('usfs_spruce','html','Original species-reference HTML.',['forest','methods'])}
    for name,(sid,fmt,description,aids) in mapping.items():
        p=downloads/name
        if not p.exists():continue
        matches=[x for x in log if x['name']==name]
        if not matches or matches[-1]['status']!='downloaded':continue
        if fmt in ('json','geojson'):json.loads(p.read_text())
        if fmt=='html' and ('Request Rejected' in p.read_text() or len(p.read_bytes())<1000):continue
        target='data/raw/'+name; shutil.copyfile(p,root/target)
        parents=[]
        if name=='l2_native.geojson':parents=[('data/raw/l2.csv','alternate_export','Matched by native OBJECTID; exact value/geometry parity is checked.')]
        register(target,sid,fmt,'native_download',description,aids,parents,role='reference' if 'metadata' in name or 'collection' in name else None)

    l2=list(csv.DictReader((root/'data/raw/l2.csv').open(encoding='utf-8-sig')))
    l2fid=bypath['data/raw/l2.csv']; geo=json.loads((root/'data/raw/l2_native.geojson').read_text())
    geo_by_id={str(f['properties']['objectid']):f for f in geo['features']}
    assert len(geo_by_id)==len(l2)==len(geo['features'])
    l2_ids=[]; native_issues=[]
    for i,row in enumerate(l2,2):
        date=dt.datetime.strptime(row['COLLECTION_DATE'],'%m/%d/%Y %I:%M:%S %p %z')
        lon,lat=map(float,re.findall(r'-?\d+\.\d+',row['point']))
        f=geo_by_id[row['OBJECTID']]
        assert f['geometry']['coordinates']==[lon,lat]
        for k in ('l2_total','l2_average','l2_branch1','l2_branch2','l2_branch3','plot_id'):
            assert Decimal(str(f['properties'][k]))==Decimal(row[k.upper()])
        rid=record(l2fid,'csv_row:'+str(i),'nb_l2',row,date.isoformat(),date.year,lat,lon);l2_ids.append(rid)
        counts=[float(row[k]) for k in ('L2_BRANCH1','L2_BRANCH2','L2_BRANCH3','L2_TOTAL') if row[k]!='']
        if any(x<0 for x in counts):native_issues.append({'record_id':rid,'issue':'negative source code retained; interpretation unresolved'})
        elif len(counts)==4 and sum(counts[:3])!=counts[3]:native_issues.append({'record_id':rid,'issue':'source branch sum differs from L2_TOTAL; preserved unchanged'})
    with (root/'data/raw/pheromone.csv').open(encoding='utf-8-sig') as f:traps=list(csv.DictReader(f))
    for i,row in enumerate(traps,2):
        date=None
        try: date=dt.datetime.strptime(row['DATE_IN'],'%d %B %Y').date()
        except ValueError:pass
        coords=re.findall(r'-?\d+\.\d+',row['the_geom']); lon,lat=map(float,coords) if len(coords)==2 else (None,None)
        record(bypath['data/raw/pheromone.csv'],'csv_row:'+str(i),'nb_moths',row,date.isoformat() if date else None,date.year if date else None,lat,lon)
    book=openpyxl.load_workbook(root/'data/raw/larval_study.xlsx',read_only=True,data_only=True)
    for sheet in book:
        raw=list(sheet.values);headers=list(raw[0]); yearcol=next((i for i,v in enumerate(headers) if str(v).startswith('Year/')),None)
        for i,values in enumerate(raw[1:],2):
            if all(x is None for x in values):continue
            obj=dict(zip(headers,values));year=values[yearcol] if yearcol is not None else None
            record(bypath['data/raw/larval_study.xlsx'],f'sheet:{sheet.title}/row:{i}','nrcan_'+sheet.title,obj,event_year=int(year) if isinstance(year,(int,float)) else None)
        text(bypath['data/raw/larval_study.xlsx'],'headers:'+sheet.title,dumps(headers),'reference')
    weather=json.loads((root/'data/raw/weather.json').read_text())
    assert weather['numberReturned']==weather['numberMatched']==len(weather['features'])==730
    for f in weather['features']:
        props=f['properties'];lon,lat=f['geometry']['coordinates']
        assert props['PROVINCE_CODE']=='NB' and props['CLIMATE_IDENTIFIER']=='8101605'
        record(bypath['data/raw/weather.json'],'feature:'+str(f['id']),'eccc_daily',props,props['LOCAL_DATE'],props['LOCAL_YEAR'],lat,lon)

    # Extract references and pixels from actual documents, retaining page selectors.
    pdf=fitz.open(root/'data/raw/maine_report.pdf');pdftext=[]
    for i,page in enumerate(pdf,1):
        t=page.get_text();pdftext.append(f'\n--- PDF page {i} ---\n'+t)
        for j,para in enumerate(re.split(r'\n\s*\n',t)):
            for start in range(0,len(para),1200):text(bypath['data/raw/maine_report.pdf'],f'page:{i}/block:{j}/char:{start}',para[start:start+1200],'reference')
    path='data/derived/maine_report_text.txt';(root/path).write_text(''.join(pdftext),encoding='utf-8')
    register(path,'maine_report','txt','extracted_text','PDF extraction; page markers retained, reading order may be imperfect.',['management','methods'],[('data/raw/maine_report.pdf','text_extraction','PyMuPDF get_text; no OCR was applied.')])
    for page_no in (3,10):
        p=pdf[page_no-1];out=f'data/derived/maine_page_{page_no:02d}.png';p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(root/out)
        register(out,'maine_report','png','rendered_page',f'Render of report PDF page {page_no}, including original map/chart and annotations.',['space_time','management'],[('data/raw/maine_report.pdf','page_render',f'PDF page {page_no}, 86.4 dpi; not a fresh field image.')])
    # Native embedded image bytes: extraction does not turn the photograph into an independent observation.
    images=pdf[11].get_images(full=True)
    if images:
        image=pdf.extract_image(images[-1][0]);path='data/derived/maine_embedded_photo.'+image['ext'];(root/path).write_bytes(image['image'])
        register(path,'maine_report',image['ext'],'extracted_embedded_image','Embedded image from PDF page 12; source caption/context remains in report.',['population','forest'],[('data/raw/maine_report.pdf','embedded_image','PDF page 12; native image stream extracted, never asserted as independent evidence.')])
    for name,sid in [('balsam_fir.html','usfs_fir'),('black_spruce.html','usfs_spruce')]:
        src='data/raw/'+name
        if src not in bypath:continue
        parser=PlainText();parser.feed((root/src).read_text(encoding='utf-8',errors='replace'))
        t='\n'.join(re.sub(r'\s+',' ',s).strip() for s in ''.join(parser.parts).splitlines() if s.strip())
        path='data/derived/'+name.replace('.html','.txt');(root/path).write_text(t,encoding='utf-8')
        register(path,sid,'txt','extracted_text','HTML text extraction; original HTML retained.',['forest'],[(src,'text_extraction','Standard-library HTMLParser, script/style omitted.')])
        for i in range(0,len(t),1200):text(bypath[src],'char:'+str(i),t[i:i+1200],'reference')
    for name in ('l2_metadata.json','pheromone_metadata.json','weather_collection.json'):
        src='data/raw/'+name
        if src not in bypath:continue
        value=json.loads((root/src).read_text());t=value.get('description',value.get('title',''))
        for i in range(0,len(t),1200):text(bypath[src],'description:'+str(i),t[i:i+1200],'reference')

    # Multiple representations of existing measurements, always in the same lineage group.
    path='data/derived/l2_records.jsonl'
    with (root/path).open('w',encoding='utf-8') as f:
        for row in rows_all:
            if row['series']=='nb_l2':f.write(dumps(row)+'\n')
    register(path,'nb_l2','jsonl','derived_serialization','All L2 records with stable record IDs and source row selectors.',['population','space_time'],[('data/raw/l2.csv','serialization','One JSON event per CSV record; not additional evidence.')])
    path='data/derived/l2_sample.xml';x=Element('observations',source_file_id=l2fid,subset='first 100 source rows; original order')
    for rid,row in zip(l2_ids[:100],l2[:100]):
        el=SubElement(x,'observation',record_id=rid)
        for k,v in row.items():SubElement(el,'field',name=k).text=v
    ElementTree(x).write(root/path,encoding='utf-8',xml_declaration=True)
    register(path,'nb_l2','xml','derived_serialization','First 100 source rows in a nested format; explicit subset.',['population'],[('data/raw/l2.csv','serialization','Only first 100 source rows; IDs link to original records.')])
    years=np.array([dt.datetime.strptime(r['COLLECTION_DATE'],'%m/%d/%Y %I:%M:%S %p %z').year for r in l2])
    totals=np.array([float(r['L2_TOTAL']) if r['L2_TOTAL'] else np.nan for r in l2])
    valid=(totals>=0)&np.isfinite(totals)
    ys=sorted(set(years));summary=[]
    for y in ys:
        m=(years==y)&valid;summary.append(dict(year=int(y),n_source_rows=int((years==y).sum()),n_nonnegative_total=int(m.sum()),mean_L2_TOTAL=float(totals[m].mean()),median_L2_TOTAL=float(np.median(totals[m]))))
    path='data/derived/l2_annual_summary.csv'
    with (root/path).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=summary[0]);w.writeheader();w.writerows(summary)
    register(path,'nb_l2','csv','derived_aggregate','Descriptive annual mean/median of L2_TOTAL; varying sample sites and effort, not a population growth estimate.',['population','methods'],[('data/raw/l2.csv','aggregation','All source years; exclude blank/negative totals, retain denominator counts.')])
    path='data/derived/l2_measurements.npz';np.savez_compressed(root/path,record_ids=np.array(l2_ids),year=years,total=totals,valid_nonnegative_total=valid)
    register(path,'nb_l2','npz','derived_array','Scientific arrays with record IDs and explicit validity mask.',['population','space_time'],[('data/raw/l2.csv','array_encoding','Negative codes retained; mask only controls derived views.')])
    fig,ax=plt.subplots(figsize=(9,4.4));fig.subplots_adjust(bottom=.23,top=.88);xx=[r['year'] for r in summary];yy=[r['mean_L2_TOTAL'] for r in summary]
    ax.plot(xx,yy,'o-',color='#246a78');ax.set(title='L2 survey: annual mean of reported total per sampled site',xlabel='Collection year',ylabel='Mean L2_TOTAL (source count)');ax.grid(alpha=.2)
    fig.text(.5,.03,'Derived view. Sample sites and effort change by year; this is not a causal trend estimate.',ha='center',fontsize=8)
    for ext in ('png','svg'):
        path='data/derived/l2_annual_chart.'+ext;fig.savefig(root/path,dpi=130,bbox_inches='tight')
        register(path,'nb_l2',ext,'derived_chart','Annual aggregate visualized; all inputs and denominators retained.',['population','methods'],[('data/derived/l2_annual_summary.csv','plot','Matplotlib line plot; no inferred ecological mechanism.')])
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,7),layout='constrained')
    coords=np.array([list(map(float,re.findall(r'-?\d+\.\d+',r['point']))) for r in l2]);latest=years==max(ys)
    ax.scatter(coords[latest,0],coords[latest,1],s=5,c='#246a78',alpha=.7)
    ax.set(title=f'L2 sample locations, {max(ys)}',xlabel='Longitude (degrees)',ylabel='Latitude (degrees)');ax.grid(alpha=.2)
    path='data/derived/l2_locations.png';fig.savefig(root/path,dpi=110);plt.close(fig)
    register(path,'nb_l2','png','derived_map','Point map of latest-year survey locations; no basemap or spatial interpolation.',['space_time'],[('data/raw/l2_native.geojson','plot','Native point coordinates; latest year only.')])
    # Time-indexed visual and audio encodings exercise format ingestion only.
    frames=[];frame_paths=[]
    for i,row in enumerate(summary):
        fig,ax=plt.subplots(figsize=(6.4,3.6),dpi=100);ax.bar(xx[:i+1],yy[:i+1],color='#246a78');ax.set_xlim(min(xx)-.5,max(xx)+.5);ax.set_ylim(0,max(yy)*1.15)
        ax.set(title=f'Derived L2 survey summary through {row["year"]}',xlabel='Collection year',ylabel='Mean L2_TOTAL');fig.tight_layout()
        fig.canvas.draw();arr=np.asarray(fig.canvas.buffer_rgba()).copy();frames.append(Image.fromarray(arr).convert('RGB'));plt.close(fig)
    path='data/derived/l2_timeline.gif';frames[0].save(root/path,save_all=True,append_images=frames[1:],duration=650,loop=0)
    register(path,'nb_l2','gif','derived_animation','One frame per annual aggregate; chronology is years, playback duration is artificial.',['population','space_time'],[('data/derived/l2_annual_summary.csv','animation','650 ms/year display time, unrelated to physical time.')])
    rate=16000;segments=[]
    for v in yy:
        t=np.arange(int(.4*rate))/rate;frequency=220+660*v/max(yy);segments.append((.2*np.sin(2*np.pi*frequency*t)*np.sin(np.pi*np.arange(len(t))/len(t))).astype(np.float32))
    pcm=(np.concatenate(segments)*32767).astype('<i2');path='data/derived/l2_sonification.wav'
    with wave.open(str(root/path),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(pcm.tobytes())
    register(path,'nb_l2','wav','derived_sonification','Synthetic tones encoding annual means. No field recording, speech or new biological evidence.',['population','space_time'],[('data/derived/l2_annual_summary.csv','sonification','Ascending years; 0.4 s/year, frequency = 220 + 660*mean/max(mean) Hz.')])
    temp=root/'data/derived/.frames';temp.mkdir(exist_ok=True)
    for i,frame in enumerate(frames):frame.save(temp/f'{i:03d}.png')
    path='data/derived/l2_timeline.mp4'
    subprocess.run(['ffmpeg','-y','-v','error','-framerate','2','-i',str(temp/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(root/path)],check=True)
    shutil.rmtree(temp)
    register(path,'nb_l2','mp4','derived_video','Encoded annual-chart sequence, not real-world video.',['space_time','population'],[('data/derived/l2_annual_summary.csv','video_encoding','Two artificial frames per second; one frame per annual summary.')])
    # Human-readable card contains only derived statistics and source pointers.
    path='data/derived/observation_card.html';(root/path).write_text('<!doctype html><meta charset="utf-8"><title>L2 source card</title><h1>L2 survey source card</h1><p>Derived summary, not independent evidence.</p><pre>'+html.escape(json.dumps(summary,indent=2))+'</pre><p>Original dataset: <a href="https://gnb.socrata.com/datasets/e4t9-ku3d">GNB L2 Mapping</a></p>',encoding='utf-8')
    register(path,'nb_l2','html','derived_summary','Readable derived observation card with source link.',['population'],[('data/derived/l2_annual_summary.csv','presentation','Plain HTML summary, no external resources.')])

    gaps=[('G01','population','Matched predator, parasitoid and pathogen abundance histories are absent.','Predator saturation and natural-control mechanisms cannot be identified from these data alone.'),
          ('G02','forest','No matched longitudinal stand age, foliage biomass and tree-ring histories.','Slow forest-state feedbacks remain underdetermined.'),
          ('G03','management','No complete georeferenced treatment/harvest histories matched to L2 sampling units.','Treatment selection and treatment effects cannot be causally disentangled here.'),
          ('G04','weather','Only Fredericton station, 2022-2023.','Not a province-wide or site-matched climate history.'),
          ('G05','management','No matched industrial prices, production incentives or decision logs.','Species-use references and agency reports do not establish individual stakeholder incentives.'),
          ('G06','methods','No independently acquired field audio, real-world video, point clouds, radar or hyperspectral arrays.','Derived media test encodings only; these native modalities are coverage gaps.'),
          ('G07','methods','Published ecological explanations are included as reference material.','Reference files must be withheld by an enforced future benchmark broker for blind discovery; the database itself is not an access-control boundary.'),
          ('G08','methods','Some source codes, sampling selection and time precision are undocumented or incomplete.','Do not interpret sentinels as counts, infer random sampling, or invent exact timestamps.')]
    db.executemany('INSERT INTO evidence_gaps VALUES (?,?,?,?)',gaps)
    db.commit();assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert not db.execute('PRAGMA foreign_key_check').fetchall()
    nrecords=db.execute('SELECT count(*) FROM records').fetchone()[0];ntexts=db.execute('SELECT count(*) FROM text_blocks').fetchone()[0]
    db.execute('VACUUM');db.close()
    # This is an offline maintainer build with no concurrent writers. Never
    # reuse a journal left by an interrupted earlier build of the old snapshot.
    oldjournal=Path(str(dbpath)+'-journal')
    if oldjournal.exists():oldjournal.unlink()
    staged.replace(dbpath)
    with dbpath.open('rb') as f,gzip.GzipFile(filename='',mode='wb',fileobj=(root/'database/evidence.sqlite.gz').open('wb'),mtime=0) as z:shutil.copyfileobj(f,z)
    (root/'metadata/files.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
    (root/'metadata/sources.json').write_text(json.dumps([dict(source_id=k,title=v[0],publisher=v[1],source_url=v[2],license_note=v[3],role=v[4],scope_note=v[5]) for k,v in definitions.items()],indent=2),encoding='utf-8')
    (root/'metadata/acquisition_log.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    (root/'metadata/source_issues.json').write_text(json.dumps(native_issues,indent=2),encoding='utf-8')
    result=dict(status='BUILT_NOT_BENCHMARKED',version='0.1.0',created_at=stamp,structured_records=nrecords,records_by_series=dict(records_by_series),searchable_text_blocks=ntexts,evidence_files=len(inventory),evidence_formats=sorted(set(x['format'] for x in inventory)),native_downloads=sum(x['origin']=='native_download' for x in inventory),derived_or_extracted_files=sum(x['origin']!='native_download' for x in inventory),source_groups_present=sorted(set(x['source_id'] for x in inventory)),sqlite_sha256=digest(dbpath),compressed_sqlite_sha256=digest(root/'database/evidence.sqlite.gz'),database_integrity='ok',foreign_key_violations=0,l2_csv_geojson_rows_matched=len(l2),source_issues_retained=len(native_issues),original_database_recovered=False,benchmark_executed=False)
    (root/'metadata/IMPORT_STATUS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--downloads',type=Path,required=True);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();build(args.downloads,args.root)
