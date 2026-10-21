"""Verify this documentation baseline. Does not execute modeled dynamics."""
from pathlib import Path
import hashlib,json,re,runpy

ROOT=Path(__file__).resolve().parents[1]
issues=[]
manifest=json.loads((ROOT/'evidence/import_manifest.json').read_text(encoding='utf-8'))
for item in manifest['entries']:
 p=ROOT/item['path']
 if not p.is_file():issues.append('Missing imported file: '+item['path']);continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:issues.append('Changed imported file: '+item['path'])
arch=next(ROOT/x['path'] for x in manifest['entries'] if x['origin']['kind']=='current_library_architecture')
ref=next(ROOT/x['path'] for x in manifest['entries'] if x['origin']['kind']=='current_library_reference')
s=arch.read_text(encoding='utf-8');a=ref.read_text(encoding='utf-8')
reqs=re.findall(r'^\| (I7-R\d{2}) \|',s,re.M)
cases=re.findall(r'^\| (I7-T\d{2,3}) \|',s,re.M)
if reqs!=[f'I7-R{i:02}' for i in range(1,55)]:issues.append('Master requirement definitions')
if cases!=[f'I7-T{i:02}' for i in range(1,193)]:issues.append('Master scenario definitions')
cross=s[s.index('## 50.'):s.index('## 51.')]
foundations=re.findall(r'^\| ((?:B|Z|F|U)\d{2}|C[567]-F\d{2}) \|',cross,re.M)
if len(foundations)!=346 or len(set(foundations))!=346:issues.append('Master foundation allocation')
graphs=re.findall(r'```mermaid\n(.*?)```',s,re.S)
if len(graphs)!=1:issues.append('One master diagram required')
g=graphs[0] if graphs else ''
nodes=re.findall(r'^\s*([A-Z][A-Z0-9]*)\["',g,re.M)
edges=re.findall(r'^\s*([A-Z][A-Z0-9]*)\s+(-->|-\.->)\|"([^\"]*)"\|\s*([A-Z][A-Z0-9]*)\s*$',g,re.M)
if len(nodes)!=82 or len(set(nodes))!=82 or len(edges)!=241:issues.append('Master diagram inventory')
direct={n:set() for n in nodes};undirected={n:set() for n in nodes}
for p,op,label,q in edges:
 if p not in direct or q not in direct:issues.append('Undefined diagram endpoint');continue
 direct[p].add(q);undirected[p].add(q);undirected[q].add(p)
def reach(start,links):
 seen=set();todo=[start]
 while todo:
  p=todo.pop()
  if p in seen:continue
  seen.add(p);todo.extend(links.get(p,set())-seen)
 return seen
if nodes and reach(nodes[0],undirected)!=set(nodes):issues.append('Disconnected master graph')
if {'OB','RE'}&reach('TR',direct):issues.append('Prediction-to-independent-source route')
refcross=a[a.index('## 15.'):]
refids=re.findall(r'^\| ((?:AD|AP|AT|AL|AG|AM)\d{2}) \|',refcross,re.M)
if len(refids)!=102 or len(set(refids))!=102:issues.append('Reference source allocation')
refreqs=re.findall(r'^\| (AF-R\d{2}) \|',a,re.M)
reftests=re.findall(r'^\| (AF-T\d{2}) \|',a,re.M)
if refreqs!=[f'AF-R{i:02}' for i in range(1,21)]:issues.append('Reference requirement definitions')
if reftests!=[f'AF-T{i:02}' for i in range(1,25)]:issues.append('Reference case definitions')
if 'PLANNED — NOT RUN' not in s or 'PLANNED — NOT RUN' not in a:issues.append('Missing scenario qualification')
for rel in ['README.md','architecture/README.md','docs/decisions/ADR-001-foundation-baseline.md']:
 p=ROOT/rel
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if target.startswith(('https://','http://','#')):continue
  if not (p.parent/target.split('#')[0]).exists():issues.append('Broken navigation link: '+rel+' -> '+target)
secret_patterns=[re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'),re.compile(r'github_pat_[A-Za-z0-9_]{50,}'),re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),re.compile(r'https?://[^/\s:@]+:[^/\s@]+@')]
# The original foundation was text-only. The combined execution tree includes
# a frozen heterogeneous benchmark. Approve only its independently pinned bytes;
# do not exempt arbitrary files under the benchmark directory.
approved_binary=set()
package=ROOT/'benchmarks/meadows-budworm'
if package.is_dir():
 try:
  package_manifest=package/'PACKAGE_MANIFEST.json'
  verifier=package/'scripts/verify_benchmark_package.py'
  if hashlib.sha256(package_manifest.read_bytes()).hexdigest()!='7272310747e7bc6bf75a03d99f3aca11f923755aa85a4f04cb0277e6132206e1':raise ValueError('frozen package manifest changed')
  if hashlib.sha256(verifier.read_bytes()).hexdigest()!='7a31867f43e336e072ac57e3a6c91349dcb1d0699347f174c2268111a40b4074':raise ValueError('frozen package verifier changed')
  class PortableInventoryRoot(type(package)):
   # v0.2.1 compares str(relative_path) to POSIX manifest identifiers.
   # Windows accepts either separator for I/O; only path presentation changes.
   def __str__(self):return super().__str__().replace('\\','/')
  runpy.run_path(str(verifier))['verify'](PortableInventoryRoot(package))
  inventory=json.loads(package_manifest.read_text(encoding='utf-8'))
  approved_binary.update((package/x['path']).resolve() for x in inventory['files'])
  # Restored originals are reproducible aliases, not additional stored sources.
  for item in json.loads((package/'metadata/STORAGE.json').read_text(encoding='utf-8')):
   alias=(package/item['path']).resolve();alias.relative_to(package.resolve())
   if alias.is_file():
    if hashlib.sha256(alias.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('restored source differs: '+item['path'])
    approved_binary.add(alias)
  alias=package/'environment/v0_2/fixture/archive.sqlite'
  if alias.is_file():
   expected=json.loads((alias.parent/'manifest.json').read_text(encoding='utf-8'))['archive_sha256']
   if hashlib.sha256(alias.read_bytes()).hexdigest()!=expected:raise ValueError('restored world archive differs')
   approved_binary.add(alias.resolve())
 except Exception as exc:
  issues.append('Benchmark package integrity: '+str(exc))
files=[]
for p in ROOT.rglob('*'):
 if not p.is_file() or '.git' in p.relative_to(ROOT).parts or '__pycache__' in p.parts:continue
 if p.relative_to(ROOT).parts[0] in {'.venv','.venv-benchmark','.local','work','tmp'}:continue
 files.append(p)
 if p.name.startswith('.env') or p.suffix in {'.gguf','.safetensors','.pem','.key'}:issues.append('Disallowed payload: '+p.relative_to(ROOT).as_posix())
 try:txt=p.read_text(encoding='utf-8')
 except UnicodeDecodeError:
  if p.resolve() not in approved_binary:issues.append('Unexpected binary: '+p.relative_to(ROOT).as_posix())
  continue
 if any(pattern.search(txt) for pattern in secret_patterns):issues.append('Potential credential: '+p.relative_to(ROOT).as_posix())
result={'status':'PASS' if not issues else 'FAIL','scope':'documentation/import/graph checks only','imported_files':len(manifest['entries']),'payload_files_checked':len(files),'master_foundations':len(foundations),'master_requirements':len(reqs),'master_prospective_cases':len(cases),'master_nodes':len(nodes),'master_edges':len(edges),'reference_source_entries':len(refids),'reference_requirements':len(refreqs),'reference_prospective_cases':len(reftests),'model_cases_run':False,'remote_status_checked_by_this_script':False,'issues':issues}
print(json.dumps(result,indent=2))
raise SystemExit(1 if issues else 0)
