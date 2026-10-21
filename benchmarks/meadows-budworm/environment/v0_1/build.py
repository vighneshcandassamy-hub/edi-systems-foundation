"""Build two evidence databases and a physically separate evaluator database."""
import argparse
import csv
import gzip
import hashlib
import html
import io
import json
import random
import shutil
import sqlite3
from pathlib import Path
from world import history, future, rollout, POLICIES, VERSION, step

SCHEMA='''
PRAGMA foreign_keys=ON;
CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE items(item_id TEXT PRIMARY KEY,title TEXT NOT NULL,summary TEXT NOT NULL,
 source_group TEXT NOT NULL,scope_json TEXT NOT NULL,format TEXT NOT NULL,
 payload_json TEXT NOT NULL,asset BLOB NOT NULL,sha256 TEXT NOT NULL);
CREATE VIRTUAL TABLE search USING fts5(item_id UNINDEXED,title,summary);
'''

def js(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
def sha(b):return hashlib.sha256(b).hexdigest()

def asset(fmt,title,rows):
    if fmt=='json':return js({'title':title,'records':rows}).encode()
    if fmt=='csv':
        out=io.StringIO();w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);return out.getvalue().encode()
    if fmt=='txt':return (title+'\n'+'\n'.join('; '.join(f'{k}: {v}' for k,v in r.items()) for r in rows)).encode()
    if fmt=='xml':
        from xml.etree.ElementTree import Element,SubElement,tostring
        root=Element('measurements',title=title)
        for r in rows:
            x=SubElement(root,'observation')
            for k,v in r.items():SubElement(x,'field',name=k).text=str(v)
        return tostring(root,encoding='utf-8',xml_declaration=True)
    # Exact code-rendered data chart, with the underlying rows retained alongside it.
    values=[float(r['value']) for r in rows];lo=min(values);span=max(max(values)-lo,.01)
    pts=' '.join(f'{40+i*720/max(len(values)-1,1):.1f},{220-150*(v-lo)/span:.1f}' for i,v in enumerate(values))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="280" viewBox="0 0 800 280"><rect width="800" height="280" fill="white"/><text x="35" y="30" font-size="16">{html.escape(title)}</text><polyline points="{pts}" fill="none" stroke="#287080" stroke-width="2"/><text x="35" y="265" font-size="12">Observation order; numeric rows and units accompany this chart.</text></svg>').encode()

def build(root,corpus,seed=4317):
    # Build in a fresh directory. The caller chooses a new version or explicitly removes a prior dev fixture.
    if root.exists():raise FileExistsError('Refusing to overwrite environment: '+str(root))
    for name in ('initial','investigation','evaluator','participant','reports'): (root/name).mkdir(parents=True)
    rng=random.Random(seed);target,terminal=history(seed);other,_=history(seed+177)
    districts=['Alder Reach','Birch Reach']
    dbs={name:sqlite3.connect(root/name/(name+'.sqlite')) for name in ('initial','investigation')}
    for name,c in dbs.items():
        c.executescript(SCHEMA);c.executemany('INSERT INTO metadata VALUES (?,?)',[
            ('schema','two-store-environment-0.1'),('origin','Constructed development scenario; not field observations.'),
            ('database_role',name),('available_through_year','60'),('clock','Simulation years; not calendar years.')])
    labels=[];admissions=[];lookup={};all_items=[]
    mission={
      'environment':'bug-tree-investigation-development-0.1','origin':'Constructed scenario with separately attributed real-domain context.',
      'current_year':60,'target_district':'Alder Reach','target_plots':[f'P{i:02d}' for i in range(1,9)],
      'problem':'Forest damage and protection spending recur. Investigate which information explains the target forest, distinguish competing explanations, and choose a ten-year management policy.',
      'objective':'Minimize mean foliage-loss fraction + 0.20 * mean annual spending units, with penalties of 5 times terminal foliage below 0.40 and 5 times annual per-plot spending above 1.10.',
      'policy_options':list(POLICIES),'policy_definitions':POLICIES,
      'submission':{'policy':'one policy option','predicted_next_year_mean_insects':'nonnegative number under chosen policy','reasoning':'explanation','evidence_ids':'list of admitted item IDs','uncertainties':'list'},
      'limits':'Only observations through simulation year 60 are requestable. Future outcomes are private. Human and machine clients use identical public endpoints. No relevance labels are supplied.'}
    (root/'participant/mission.json').write_text(json.dumps(mission,indent=2)+'\n')

    def put(store,title,summary,scope,rows,group,classification,reason,channel,fmt=None):
        fmt=fmt or rng.choice(['json','csv','txt','xml','svg'])
        iid='E'+f'{rng.getrandbits(72):018x}';b=asset(fmt,title,rows)
        public=(iid,title,summary,group,js(scope),fmt,js(rows),b,sha(b))
        dbs[store].execute('INSERT INTO items VALUES (?,?,?,?,?,?,?,?,?)',public)
        dbs[store].execute('INSERT INTO search VALUES (?,?,?)',(iid,title,summary))
        labels.append((iid,store,classification,reason,channel))
        all_items.append({'item_id':iid,'store':store,'sha256':sha(b),'format':fmt,'source_group':group})
        lookup[iid]=dict(rows=rows,scope=scope,title=title)
        return iid

    # All channels share the same schema, origin declaration and format distribution.
    # The metadata contains legitimate unit/scope facts, never usefulness labels.
    channels=[
      ('branch_density','Branch larval monitoring','target_measurement','insects','Alder Reach','target spruce budworm','larvae per standardized branch','Local insect state enters the target transition.'),
      ('foliage_stock','Forest canopy monitoring','target_measurement','foliage','Alder Reach','host-tree foliage','fraction of baseline foliage','Local foliage affects carrying capacity and the objective.'),
      ('host_structure','Forest composition monitoring','target_measurement','mature_host','Alder Reach','mature susceptible host trees','fraction of stand','Local host composition changes slowly and affects capacity.'),
      ('natural_enemies','Insect natural-enemy monitoring','target_measurement','enemies','Alder Reach','target insect natural enemies','standardized activity index','Local natural control enters the transition with a delayed response.'),
      ('spring_conditions','Spring development conditions','target_measurement','weather','Alder Reach','spring weather','standardized anomaly','Local weather changes growth; it is not sufficient alone.'),
      ('treatment_blocks','Forest protection operations','target_measurement','spray','Alder Reach','target insect treatment','fractional treatment intensity','Local historical actions and selection must be distinguished from effects.'),
      ('branch_density','Branch larval monitoring','scope_mismatch','insects','Birch Reach','target spruce budworm','larvae per standardized branch','Independent district is not the target state; may aid a scope check but is not a local causal measurement.'),
      ('foliage_stock','Forest canopy monitoring','scope_mismatch','foliage','Birch Reach','host-tree foliage','fraction of baseline foliage','Nearby-looking forest observations belong to a separate district.'),
      ('natural_enemies','Insect natural-enemy monitoring','scope_mismatch','enemies','Birch Reach','target insect natural enemies','standardized activity index','Predator observations are from a different district, not the target plots.'),
      ('moth_activity','Forest moth activity','stage_scope_mismatch',None,'Alder Reach','non-target needle-miner moth','adult trap captures','Same forest/insect terminology, but a different species and life stage.'),
      ('canopy_coverage','Forest canopy monitoring','denominator_mismatch',None,'Alder Reach','all tree species including non-host trees','fractional canopy cover, all species','All-species cover is not susceptible-host foliage; context must not be substituted for local food stock.'),
      ('protection_spending','Forest protection expenditure','aggregate_mismatch',None,'Provincial programme','all districts and insect programmes','nominal programme spending index','Provincial expenditure is not the treated area/intensity in the target district.'),
      ('timber_certification','Forest health and timber certification','independent_distractor',None,'Alder Reach','wood-product quality grading','certification index','Administrative random series has no input to the simulated target dynamics or objective.'),
      ('spray_batch_quality','Forest insect treatment batch quality','independent_distractor',None,'Alder Reach','unused reserve treatment batches','assay quality index','Measurements concern unused reserve batches, not products applied to target plots.'),
      ('budburst_reviews','Forest budburst observation programme','independent_distractor',None,'Alder Reach','ornamental non-host trees at office grounds','review index','Same seasonal/tree vocabulary; no role in target-plot state transitions.'),
      ('budworm_enzyme','Budworm stress-response assays','independent_distractor',None,'Alder Reach','target spruce budworm enzyme activity','relative biochemical activity','Same insect, plots and years, but this constructed biochemical channel has no input to the world transition or objective; a real biological claim is not implied.'),
      ('needle_chemistry','Host-tree needle chemistry','independent_distractor',None,'Alder Reach','balsam-fir needle trace-element assay','relative trace-element assay index','Same host trees, plots and years. This constructed assay is causally inactive in this development world, not a statement about real tree chemistry.'),
      ('branch_density_archive','Branch larval monitoring archive','time_scope_mismatch',None,'Alder Reach','archived demonstration stand, replaced before target monitoring','larvae per branch','District name is shared, but the historical stand was replaced; no continuity to target plots.'),
      ('sample_effort','Forest insect monitoring effort','interpretation_context',None,'Alder Reach','survey sampling effort','branches per reporting unit','Helps interpret observations but is not a biological forcing.'),
      ('method_calibration','Forest insect measurement calibration','interpretation_context',None,'Alder Reach','branch-length reporting protocol','centimetres per sampled branch','Method context prevents incorrect unit comparisons; not a biological cause.')]
    for idx,(channel,title,cl,key,district,subject,unit,reason) in enumerate(channels):
        # Independent nuisance generator is never passed into world.history or step.
        nr=random.Random(seed+10000+idx);nuisance=[nr.uniform(.1,1.0) for _ in range(60)]
        # Select one independent historical candidate with chance resemblance to target insects.
        # Only its *past* is selected; no future value drives or predicts the transition by construction.
        if channel in ('timber_certification','budworm_enzyme'):
            y=[sum(x['insects'] for x in target if x['year']==t)/8 for t in range(1,61)]
            def corr(a,b):
                ma=sum(a)/len(a);mb=sum(b)/len(b);num=sum((x-ma)*(z-mb) for x,z in zip(a,b));den=(sum((x-ma)**2 for x in a)*sum((z-mb)**2 for z in b))**.5
                return num/den if den else 0.
            candidates=[[nr.uniform(.1,1.) for _ in range(60)] for _ in range(96)]
            nuisance=max(candidates,key=lambda z:abs(corr(z[-10:],y[-10:])))
            reason+=' Its last ten values were selected from independent candidates for accidental historical correlation; this does not establish causal influence or future predictive value.'
        for start in range(1,61,10):
            rows=[]
            for year in range(start,start+10):
                cohort=target if district!='Birch Reach' else other
                if key:
                    for row in (x for x in cohort if x['year']==year):
                        rows.append({'year':year,'plot':row['plot'],'value':round(row[key],6)})
                else:
                    value=nuisance[year-1]
                    if channel=='sample_effort':value=24 if year<45 else 48
                    if channel=='method_calibration':value=75 if year<45 else 45
                    if channel=='canopy_coverage':value=.82+.08*nuisance[year-1]
                    if channel=='protection_spending':value=100+year*2+25*nuisance[year-1]
                    if channel=='moth_activity':value=round(20*nuisance[year-1])
                    if channel in ('budworm_enzyme','needle_chemistry','timber_certification'):
                        for j in range(8):rows.append({'year':year,'plot':f'P{j+1:02d}','value':round(value+.005*j,6)})
                    else:rows.append({'year':year if cl!='time_scope_mismatch' else year-80,'plot':'district_summary','value':round(value,6)})
            scope={'district':district,'subject':subject,'unit':unit,'years':[rows[0]['year'],rows[-1]['year']],
                   'sampling':'constructed recorded measurements; reported precision retained','origin':'constructed_scenario',
                   'representation_note':'The numeric rows are the underlying data for any chart/XML/text view.'}
            if key=='insects':scope['value_basis']='Reported values are normalized to a 75 cm branch equivalent, independent of raw collection length.'
            group='S'+sha((district+'|'+channel+'|'+str(start)).encode())[:16]
            summary=f'{subject}; {district}; reporting interval {scope["years"][0]} to {scope["years"][1]}; {unit}.'
            put('investigation',title,summary,scope,rows,group,cl,reason,channel)
            if start==51:
                # Sparse initial excerpts preserve scope metadata and make later requests valuable.
                initialrows=[r for r in rows if r['year'] in (rows[-1]['year']-9,rows[-1]['year']-5,rows[-1]['year'])]
                put('initial',title,summary,scope,initialrows,group,cl,reason,channel)
                if idx in (0,1,5,6,9,11,12):
                    # A bulletin is a second presentation of exactly the same source group.
                    put('initial',title+' bulletin',summary,scope,initialrows,group,'duplicate',
                        'Repeats an existing source group; never independent confirmation.',channel,fmt='txt')
    # Requestable experiments expose discriminating evidence, without explaining its mechanism.
    feeding=[];nr=random.Random(seed+890)
    for density in (.05,.1,.2,.4,.8,1.6,3.2,6.4):
        for replicate in range(1,5):
            consumed=2*.5*density*density/(.16+density*density)
            feeding.append({'year':58,'prey_density':density,'enemy_activity':.5,'replicate':replicate,'value':round(max(0,consumed+nr.gauss(0,.008)),6)})
    for species,cl in [('target spruce budworm','discriminating_measurement'),('non-target needle-miner moth','stage_scope_mismatch')]:
        rows=feeding if cl=='discriminating_measurement' else [{**x,'value':round(.13*x['prey_density'],6)} for x in feeding]
        scope={'district':'Alder Reach','subject':species,'unit':'consumed prey per standardized trial','years':[58,58],'origin':'constructed_scenario','sampling':'replicated laboratory feeding assay; controlled prey density'}
        put('investigation','Forest insect feeding assays',f'{species}; branch-associated insect feeding; replicated assays.',scope,rows,
            'S'+sha(species.encode())[:16],cl,'Assay relevance depends on species identity and whether it measures the proposed response.','feeding_assay',fmt='csv')
    rows=[]
    # A frozen controlled contrast permits investigating the misleading biochemical association.
    for level in (.1,.4,.7,1.0):
        for replicate in range(1,5):
            state={'insects':.9,'foliage':.7,'mature_host':.75,'enemies':.45}
            observed,_=step(state,.2,nuisance={'enzyme_activity':level})
            rows.append({'year':59,'enzyme_activity':level,'replicate':replicate,'value':round(observed['insects'],6)})
    scope={'district':'Alder Reach','subject':'target spruce budworm enzyme activity','unit':'next-step larval density at fixed initial state','years':[59,59],'origin':'constructed_scenario','sampling':'controlled biochemical contrasts; foliage, weather, enemies and initial larvae held fixed'}
    put('investigation','Budworm physiology and development assays','Target-insect controlled development assays at several biochemical activity levels.',scope,rows,'S'+sha(b'physiology-controlled-contrast')[:16],
        'discriminating_measurement','Shows no response to this constructed biochemical manipulation under the recorded controlled conditions; it does not prove universal biological irrelevance.','biochemical_contrast',fmt='csv')
    # Real corpus examples remain honest, external context; no fabricated target-plot provenance.
    c=sqlite3.connect(corpus.resolve().as_uri()+'?mode=ro',uri=True)
    for series in ('nb_l2','nb_moths','nrcan_L2','nrcan_L4','nrcan_Defoliation','eccc_daily'):
        source=c.execute('SELECT record_id,file_id,selector,payload_json FROM records WHERE series=? ORDER BY record_id LIMIT 12',(series,)).fetchall()
        rows=[{'record_id':a,'file_id':b,'selector':d,'source_record':json.loads(v)} for a,b,d,v in source]
        scope={'district':'Real-world source geography; not Alder Reach','subject':'Published insect/forest/weather records','origin':'real_corpus_excerpt','unit':'native source units','years':'native source dates; not simulation years'}
        iid=put('investigation','Forest and insect field-record examples',f'External monitoring examples from source series {series}; native source identifiers retained.',scope,rows,'S'+sha(series.encode())[:16],
             'external_context','May inform domain/method understanding; not measurements of this constructed district.',series,fmt='json')
        if series in ('nb_l2','nb_moths','eccc_daily'):
            put('initial','Forest and insect field-record examples',f'External monitoring examples from source series {series}; native source identifiers retained.',scope,rows[:3],'S'+sha(series.encode())[:16],
                'external_context','Domain context only; not target-plot observations.',series,fmt='json')
    c.close()
    for name,c in dbs.items():
        c.commit();assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok';c.close()
        p=root/name/(name+'.sqlite')
        with p.open('rb') as src,gzip.GzipFile(filename='',mode='wb',fileobj=p.with_suffix('.sqlite.gz').open('wb'),mtime=0) as z:shutil.copyfileobj(src,z)
    truth=sqlite3.connect(root/'evaluator/evaluator.sqlite')
    truth.executescript('CREATE TABLE labels(item_id TEXT PRIMARY KEY,store TEXT,class TEXT,reason TEXT,channel TEXT); CREATE TABLE history(payload TEXT); CREATE TABLE policy_outcomes(policy TEXT PRIMARY KEY,payload TEXT); CREATE TABLE private_meta(key TEXT PRIMARY KEY,value TEXT);')
    truth.executemany('INSERT INTO labels VALUES (?,?,?,?,?)',labels)
    truth.executemany('INSERT INTO history VALUES (?)',[(js(x),) for x in target])
    outcomes={name:rollout(terminal,policy,future(seed)) for name,policy in POLICIES.items()}
    truth.executemany('INSERT INTO policy_outcomes VALUES (?,?)',[(k,js(v)) for k,v in outcomes.items()])
    truth.executemany('INSERT INTO private_meta VALUES (?,?)',[('seed',str(seed)),('world_version',VERSION),('counterfactual_scope','Identical future weather across five finite policy options; not an optimum over all possible policies.'),('primary_scoring','Policy outcome and forecast error; private relevance labels are diagnostic only.')])
    truth.commit();truth.close()
    p=root/'evaluator/evaluator.sqlite'
    with p.open('rb') as src,gzip.GzipFile(filename='',mode='wb',fileobj=p.with_suffix('.sqlite.gz').open('wb'),mtime=0) as z:shutil.copyfileobj(src,z)
    # Participant export is deliberately independent of the investigation/evaluator files.
    shutil.copyfile(root/'initial/initial.sqlite',root/'participant/initial.sqlite')
    manifests=[]
    for name in ('initial','investigation','evaluator'):
        p=root/name/(name+'.sqlite');manifests.append({'role':name,'path':str(p.relative_to(root)),'sha256':sha(p.read_bytes()),'compressed_sha256':sha(p.with_suffix('.sqlite.gz').read_bytes()),'bytes':p.stat().st_size})
    counts={name:sum(x[1]==name for x in labels) for name in ('initial','investigation')}
    report={'status':'DEVELOPMENT_ENVIRONMENT_BUILT','world_version':VERSION,'source_corpus_sha256':sha(corpus.read_bytes()),'items':counts,
            'formats':sorted(set(x['format'] for x in all_items)), 'source_groups':len(set(x['source_group'] for x in all_items)),
            'initial_excerpt_and_duplicate_groups':True,'future_exposed_to_participant':False,'edi_run':False,'human_run':False,
            'scientific_scope':'One constructed development world, not ecological calibration or qualification; generated relevance depends on the declared mission.'}
    (root/'manifest.json').write_text(json.dumps({'databases':manifests,'build':report},indent=2)+'\n')
    (root/'evaluator/labels.json').write_text(json.dumps([dict(zip(('item_id','store','class','reason','channel'),x)) for x in labels],indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--corpus',type=Path,required=True);p.add_argument('--seed',type=int,default=4317);a=p.parse_args();build(a.out,a.corpus,a.seed)
