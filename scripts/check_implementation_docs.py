"""Check design traceability/inventory only. Never execute an EDI model or benchmark."""
from pathlib import Path
import hashlib
import itertools
import json
import re

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'docs/implementation'
evidence = D / 'evidence'
evidence.mkdir(exist_ok=True)
output_path = evidence / 'document-checks.json'
if not output_path.exists():
    output_path.write_text('{"status":"pending","scope":"documentation_only"}\n', encoding='utf-8')
issues = []
def require(condition, message):
    if not condition:
        issues.append(message)
def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))
def id_map(rows, label):
    values = [r['id'] for r in rows]
    require(len(values) == len(set(values)), 'Duplicate ' + label)
    return {r['id']: r for r in rows}

data = read_json(D / 'TRACEABILITY.json')
interfaces = read_json(D / 'INTERFACES.json')
sources = read_json(D / 'SOURCES.json')
comps = id_map(data['components'], 'components')
funcs = id_map(data['functions'], 'functions')
reqs = id_map(data['implementation_requirements'], 'implementation requirements')
cases = id_map(data['cases'], 'cases')
up = id_map(data['upstream_requirements'], 'source requirements')
sys = id_map(data['system_requirements'], 'system requirements')
require(set(comps) == {f'C{i}' for i in range(8)}, 'Eight component owners')
require(len(funcs) == 32, 'Function inventory')
require(set(up) == {f'I7-R{i:02}' for i in range(1,55)}, 'I7 requirement inventory')
require(set(cases) == {f'E{i:02}' for i in range(1,41)}, 'Forty prospective cases')
require(len(reqs) == 28, 'Implementation requirement inventory')
for key, expected in [('appendix_requirements',20), ('retained_requirements',43), ('consumer_obligations',8), ('system_requirements',16)]:
    rows = data[key]
    id_map(rows, key)
    require(len(rows) == expected, key + ' count')
    for r in rows:
        require(bool(r['implementation_ids']) and set(r['implementation_ids']) <= set(reqs), 'Unallocated/unknown implementation link: '+r['id'])
for r in up.values():
    require(bool(r['implementation_ids']) and set(r['implementation_ids']) <= set(reqs), 'Unallocated I7 requirement '+r['id'])
for r in reqs.values():
    require(bool(r['parents']) and set(r['parents']) <= set(up), 'Invalid source parent '+r['id'])
    require(bool(r['system_parents']) and set(r['system_parents']) <= set(sys), 'Invalid system parent '+r['id'])
    require(bool(r['component_ids']) and set(r['component_ids']) <= set(comps), 'Invalid component allocation '+r['id'])
    require(bool(r['function_ids']) and set(r['function_ids']) <= set(funcs), 'Invalid function allocation '+r['id'])
    require(bool(r['verification_ids']) and set(r['verification_ids']) <= set(cases), 'Invalid case allocation '+r['id'])
    require(r['status'] == 'proposed_not_implemented', 'False implementation status '+r['id'])
    for fid in r['function_ids']:
        require(funcs[fid]['component_id'] in r['component_ids'], 'Function owner outside requirement allocation '+r['id']+' '+fid)
        require(r['id'] in funcs[fid]['requirement_ids'], 'Missing reverse function trace '+r['id'])
    for cid in r['verification_ids']:
        require(r['id'] in cases[cid]['requirement_ids'], 'Missing reverse case trace '+r['id'])
for f in funcs.values():
    require(f['component_id'] in comps and bool(f['requirement_ids']), 'Unowned or unjustified function '+f['id'])
for c in cases.values():
    require(bool(c['requirement_ids']), 'Unallocated case '+c['id'])
    require(c['status'] == 'specified_not_run' and c['evidence_ref'] is None and c['implementation_revision'] is None, 'False runtime evidence '+c['id'])
require(data['product_qualification'] == 'not_run', 'False product qualification')
for name, hash_key in [('master','master_sha256'),('appendix','appendix_sha256')]:
    p = ROOT / data['source_pin'][name]
    require(hashlib.sha256(p.read_bytes()).hexdigest() == data['source_pin'][hash_key], 'Changed source snapshot '+name)
obs = read_json(ROOT/'architecture/observation/REQUIREMENTS.json')
sub = read_json(ROOT/'architecture/substrate/REQUIREMENTS.json')
retained = id_map(data['retained_requirements'],'retained obligations')
for r in obs['observation_requirements']+sub['requirements']:
    require(r['id'] in retained and retained[r['id']]['statement'] == r['statement'] and retained[r['id']]['acceptance'] == r['acceptance'], 'Changed retained requirement '+r['id'])
overview = (D/'OVERVIEW.mmd').read_text(encoding='utf-8')
nodes = re.findall(r'^\s*([A-Z][A-Z0-9]*)\["([^\"]+)"\]', overview, re.M)
edges = re.findall(r'^\s*([A-Z][A-Z0-9]*)\s+(-->|-\.->)\|"([^\"]+)"\|\s*([A-Z][A-Z0-9]*)\s*$', overview, re.M)
require(len(nodes) == 42 and len(edges) == 69, 'Supplied overview inventory')
require(set(nodes) == {(r['id'],r['label']) for r in data['overview_nodes']}, 'Overview node coverage')
require(set(edges) == {(r['from'],r['notation'],r['label'],r['to']) for r in data['overview_edges']}, 'Overview edge coverage')
for n in data['overview_nodes']:
    require(n['primary_processor'] in comps and n['state_owner'] in comps, 'Unknown overview owner '+n['id'])
for e in data['overview_edges']:
    require(e['runtime_api'] is False, 'Conceptual edge mistaken for runtime API '+e['id'])
lanes = {(r['from'],r['to']) for r in interfaces['lanes']}
require(len(interfaces['lanes']) == 56 and lanes == set(itertools.permutations(comps,2)), 'Complete directed pair coverage')
for c in interfaces['contracts']:
    require(set(c['requirement_ids']) <= set(reqs), 'Unknown interface requirement '+c['id'])
    require(set(c['verification_ids']) <= set(cases), 'Unknown interface case '+c['id'])
    require(c['status'] == 'proposed', 'Unexpected contract qualification '+c['id'])
for c in interfaces['cases']:
    require(c == cases[c['id']], 'Divergent interface/case copy '+c['id'])
require(len(sources['sources']) == 51 and len({s['id'] for s in sources['sources']}) == 51, 'Source register inventory')
for s in sources['sources']:
    require(s['url'].startswith('https://') and s['kind'] == 'primary' and s['retrieved'] == '2026-10-20', 'Source metadata '+s['id'])
    require(s['url'] in (D/'SOURCES.md').read_text(encoding='utf-8'), 'Source register mismatch '+s['id'])
for p in list(D.glob('*.md'))+[ROOT/'docs/decisions/ADR-002-implementation-architecture.md']:
    txt=p.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',txt):
        if target.startswith(('https://','http://','#')):
            continue
        require((p.parent/target.split('#')[0]).is_file(), 'Broken document link '+p.name+' -> '+target)
result = {'status':'PASS' if not issues else 'FAIL','scope':'documentation_traceability_and_inventory_only',
          'source_baseline':data['source_pin']['commit'],'components':len(comps),'functions':len(funcs),
          'overview_nodes':len(nodes),'overview_edges':len(edges),'i7_requirements':len(up),
          'appendix_requirements':len(data['appendix_requirements']),'retained_layer_requirements':len(retained),
          'consumer_obligations':len(data['consumer_obligations']),'edi_system_requirements':len(sys),
          'implementation_requirements':len(reqs),'prospective_cases':len(cases),'pairs_reviewed':len(lanes)//2,
          'directed_lanes':len(lanes),'proposed_contracts':len(interfaces['contracts']),'primary_sources':len(sources['sources']),
          'source_snapshots_unchanged':not any('Changed source snapshot' in i for i in issues),
          'model_cases_run':False,'runtime_verified':False,'independent_review':False,'issues':issues}
output_path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
raise SystemExit(1 if issues else 0)
