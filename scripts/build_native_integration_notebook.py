"""Build the private Kaggle engineering notebook from this repository's source."""
import ast,base64,hashlib,io,json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
EXAMPLES=ROOT/"examples/free-compute"
files=sorted((ROOT/"src").rglob("*.py"))+[EXAMPLES/name for name in (
 "edi_native_probe.py","edi_native_worker.py","edi_neutral_investigation_v3.py","edi_neutral_loop_worker_v3.py")]
archive=io.BytesIO()
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
 for p in files:
  ast.parse(p.read_text(encoding="utf-8"))
  info=zipfile.ZipInfo(p.relative_to(ROOT).as_posix(),date_time=(1980,1,1,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED
  z.writestr(info,p.read_bytes())
raw=archive.getvalue();encoded=base64.b64encode(raw).decode();sha=hashlib.sha256(raw).hexdigest()
install='''import subprocess,sys,venv
from pathlib import Path
root=Path("/kaggle/temp/edi-free-vllm");root.mkdir(parents=True,exist_ok=True)
python=root/"env/bin/python"
if not python.exists():venv.EnvBuilder(with_pip=False).create(root/"env")
with Path("/kaggle/working/edi-native-install.log").open("w") as log:
    result=subprocess.run([sys.executable,"-m","pip","--python",str(python),"install","--no-cache-dir",
        "vllm==0.21.0","transformers==4.57.6","pydantic==2.12.5"],stdout=log,stderr=subprocess.STDOUT,timeout=1200)
assert result.returncode==0,"Preserve install log; do not launch inference"
print("Environment installed. GPU T4 x2 required.")
'''
launch='''import base64,hashlib,io,os,subprocess,zipfile
from pathlib import Path
payload=base64.b64decode('''+repr(encoded)+''')
assert hashlib.sha256(payload).hexdigest()=='''+repr(sha)+'''
root=Path("/kaggle/working/edi-native-source")
assert not root.exists(),"Use a fresh diagnostic directory; do not overwrite prior runs"
root.mkdir()
with zipfile.ZipFile(io.BytesIO(payload)) as z:
    assert all(name.startswith(("src/","examples/free-compute/")) and ".." not in Path(name).parts for name in z.namelist())
    z.extractall(root)
env=dict(os.environ,PYTHONPATH=str(root/"src"),HF_HUB_DISABLE_IMPLICIT_TOKEN="1",HF_HUB_DISABLE_PROGRESS_BARS="1")
env.pop("PYTHONHOME",None)
with Path("/kaggle/working/edi-native-worker.log").open("w") as log:
    child=subprocess.Popen(["/kaggle/temp/edi-free-vllm/env/bin/python",str(root/"examples/free-compute/edi_native_worker.py")],stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
print("Native numeric/image worker PID",child.pid)
'''
def monitor(prefix):
 return '''import json,subprocess
from pathlib import Path
for name in ["'''+prefix+'''server.json","'''+prefix+'''result.json"]:
    p=Path("/kaggle/working")/name
    if p.exists(): print(name,p.read_text())
print(subprocess.run(["nvidia-smi","--query-gpu=name,memory.used,utilization.gpu","--format=csv,noheader"],text=True,capture_output=True).stdout)
'''
loop='''import json
from pathlib import Path
assert json.loads(Path("/kaggle/working/edi-native-server.json").read_text()).get("server_stopped") is True
assert child.poll() is not None and not Path("/kaggle/working/edi-native-loop3-state").exists()
with Path("/kaggle/working/edi-native-loop3-worker.log").open("w") as log:
    child=subprocess.Popen(["/kaggle/temp/edi-free-vllm/env/bin/python",str(root/"examples/free-compute/edi_neutral_loop_worker_v3.py")],stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
print("Native C0 loop worker PID",child.pid)
'''
sections=[
 ("Private EDI native integration","Two engineering diagnostics using real fixed Qwen3-VL inference, not the forest benchmark. Select free GPU T4 x2 and enable internet for setup. No OpenAI credentials belong here. Run each launch cell once; repeat only monitors. Wait for each worker/server to stop, then export/hash-verify that trial before proceeding. Do not use Run All."),
 ("Install",install),("Launch numeric/image native check",launch),("Monitor native check",monitor("edi-native-")),
 ("Launch C0 neutral instrument investigation",loop),("Monitor C0 investigation",monitor("edi-native-loop3-"))]
cells=[]
for i,(heading,body) in enumerate(sections):
 cells.append({"cell_type":"markdown","id":f"native-heading-{i}","metadata":{},"source":[f"# {heading}\n"]+([body] if i==0 else [])})
 if i:
  ast.parse(body);cells.append({"cell_type":"code","id":f"native-code-{i}","metadata":{},"execution_count":None,"outputs":[],"source":body.splitlines(keepends=True)})
cells.append({"cell_type":"markdown","id":"native-preserve","metadata":{},"source":["Download and hash-verify each trial's JSON reports, logs, source/package inventory and raw state immediately, before another trial or session shutdown. The latest C0 trial failed; rerunning unchanged is not a readiness claim. Preserve failures. The examples stop owned model servers; also stop the Kaggle session to preserve quota. Generated source cache is temporary. This notebook is generated from repository source and contains no recorded outputs; actual evidence is stored separately."]})
notebook={"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python"},"edi_source_bundle_sha256":sha},"nbformat":4,"nbformat_minor":5}
(EXAMPLES/"edi-native-integration.ipynb").write_bytes((json.dumps(notebook,indent=2)+"\n").encode())
print(json.dumps({"notebook":"examples/free-compute/edi-native-integration.ipynb","source_files":len(files),"source_bundle_sha256":sha,"code_cells_parsed":5,"recorded_outputs":0}))
