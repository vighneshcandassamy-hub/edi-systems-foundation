"""Create a standalone notebook cell; construction performs no model execution."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    files = {"src/" + p.relative_to(repo / "src").as_posix(): p.read_bytes()
             for p in sorted((repo / "src").rglob("*.py"))}
    for name in ("complete_run.py", "engineering_server.py"):
        files[name] = (Path(__file__).parent / name).read_bytes()
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(repo), "status", "--porcelain"], text=True)
    manifest = {"git_head": head, "working_tree_changed": bool(dirty),
                "files": {n: hashlib.sha256(v).hexdigest() for n, v in files.items()}}
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
        archive.writestr("source-manifest.json", json.dumps(manifest, indent=2))
    data = memory.getvalue()
    installer = '''import json,pathlib,subprocess,sys,venv
out=pathlib.Path("/kaggle/working/edi-engineering-20261022")
for name,packages in [("serve",["vllm==0.21.0","transformers==4.57.6","pydantic==2.12.5","numpy<2.5"]),("compute",["pydantic==2.12.5","numpy==2.5.3","scipy==1.17.0"])]:
 env=pathlib.Path("/kaggle/temp/edi-engineering-"+name)
 venv.EnvBuilder(with_pip=False).create(env)
 py=str(env/"bin/python")
 with (out/(name+"-install.log")).open("x") as log:
  subprocess.run([sys.executable,"-m","pip","--python",py,"install","--no-cache-dir",*packages],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1200)
 (out/(name+"-packages.txt")).write_text(subprocess.check_output([sys.executable,"-m","pip","--python",py,"freeze"],text=True))
(out/"isolated-setup-complete.json").write_text(json.dumps({"status":"completed","paid_fallback":False}))
'''
    cell = '''import base64,hashlib,io,json,os,pathlib,shutil,subprocess,sys,time,zipfile
out=pathlib.Path("/kaggle/working/edi-engineering-20261022")
assert not out.exists(),"Existing native state requires resume, not reinitialization"
out.mkdir(parents=True)
pathlib.Path("/kaggle/temp").mkdir(parents=True,exist_ok=True)
assert shutil.disk_usage("/kaggle/temp").free>35*2**30
root=pathlib.Path("/kaggle/temp/edi-engineering-source");root.mkdir(exist_ok=False)
data=base64.b64decode(__EDI_BUNDLE__)
assert hashlib.sha256(data).hexdigest()==__EDI_DIGEST__
with zipfile.ZipFile(io.BytesIO(data)) as z:
 for n in z.namelist():assert not n.startswith("/") and ".." not in pathlib.PurePosixPath(n).parts
 z.extractall(root)
(out/"source-manifest.json").write_bytes((root/"source-manifest.json").read_bytes())
(out/"inventory.json").write_text(json.dumps({"python":sys.version,"gpus":subprocess.check_output(["nvidia-smi","--query-gpu=name,memory.total,driver_version","--format=csv,noheader"],text=True)},indent=2))
installer=out/"isolated_setup.py";installer.write_text(__EDI_INSTALLER__)
with (out/"isolated-setup.log").open("x") as log:
 setup=subprocess.Popen([sys.executable,str(installer)],stdout=log,stderr=subprocess.STDOUT)
deadline=time.monotonic()+2400
server=None
while time.monotonic()<deadline:
 if setup.poll() not in (None,0):raise RuntimeError("Preserve setup logs before repair")
 if (out/"isolated-setup-complete.json").exists() and server is None:
  env=dict(os.environ);env.pop("PYTHONPATH",None)
  with (out/"supervisor.log").open("x") as log:
   server=subprocess.Popen(["/kaggle/temp/edi-engineering-serve/bin/python",str(root/"engineering_server.py")],env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 for n in ("serve-install.log","compute-install.log","supervisor.log","initial-process-1.log"):
  p=out/n
  if p.exists():print(n,p.read_text(errors="replace")[-250:],flush=True)
 if (out/"teacher-pending.json").exists():print("Export and verify checkpoint before teacher import",flush=True);break
 p=out/"engineering-server.json"
 if p.exists():
  status=json.loads(p.read_bytes())
  if status.get("stage")=="failed" or (status.get("stage")=="engineering_initial_returned" and status.get("returncode")!=0):
   print("Retained native failure; export before repair",flush=True);break
 if server is not None and server.poll() is not None:raise RuntimeError("Preserve supervisor log")
 time.sleep(20)
else:raise TimeoutError("Preserve logs and native state")
'''
    cell = cell.replace("__EDI_BUNDLE__", repr(base64.b64encode(data).decode()))
    cell = cell.replace("__EDI_DIGEST__", repr(hashlib.sha256(data).hexdigest()))
    cell = cell.replace("__EDI_INSTALLER__", repr(installer))
    compile(cell, "engineering-notebook-cell", "exec")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="") as stream:
        stream.write(cell)
    print(json.dumps({"cell_bytes": len(cell.encode()), "bundle_sha256": hashlib.sha256(data).hexdigest(),
                      "files": len(files), "model_calls": 0}))


if __name__ == "__main__":
    main()
