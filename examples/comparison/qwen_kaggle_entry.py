"""Kaggle-only entry. Installs pinned environments; runs tests; starts one
ephemeral local model; performs neutral smoke; then attempts one fresh pair.
No restart/fallback. All raw case/model files remain private operator artifacts.
"""
import base64
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import subprocess
import sys
import time
import uuid
import venv
import zipfile

MODEL_ID="Qwen/Qwen3-VL-8B-Instruct"
REVISION="0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
MODEL={"id":MODEL_ID,"revision":REVISION,"reasoning":"greedy-seed17"}

def run(source):
    if not Path("/kaggle/working").is_dir():
        raise RuntimeError("Execution restricted to Kaggle")
    source=Path(source).resolve()
    from cedar_session import verify_source
    manifest=verify_source(source)
    root=Path("/kaggle/working")/("qwen-cedar-"+uuid.uuid4().hex[:12])
    root.mkdir(exist_ok=False)
    marker=source.parent/"single-launch.json"
    if marker.exists():raise RuntimeError("This notebook source already launched; preserve and inspect its run")
    marker.write_text(json.dumps({"root":str(root),"created":time.time()}),encoding="utf-8")
    server=None;serve_log=None
    try:
        if shutil.disk_usage("/kaggle").free<45*1024**3:
            raise RuntimeError("At least45GiB free space required before installs/weights")
        gpu_text=subprocess.check_output(["nvidia-smi","--query-gpu=name,memory.total","--format=csv,noheader"],text=True)
        gpu_lines=[s for s in gpu_text.splitlines() if s.strip()]
        if len(gpu_lines)!=2 or any("T4" not in s for s in gpu_lines):
            raise RuntimeError("Reviewed launch configuration requires two T4 GPUs; no silent hardware/model substitution")
        (root/"gpu-inventory.txt").write_text(gpu_text,encoding="utf-8")
        envs={}
        print("QWEN_STAGE", "installing pinned environments",flush=True)
        for kind,packages in [
            ("serve",["vllm==0.21.0","transformers==4.57.6","pydantic==2.12.5","numpy<2.5"]),
            ("compute",["pydantic==2.12.5","numpy==2.5.3","scipy==1.17.0"])]:
            dest=Path("/kaggle/temp")/("qwen-cedar-"+kind+"-"+root.name)
            venv.EnvBuilder(with_pip=False).create(dest)
            python=str(dest/"bin/python");envs[kind]=python
            with (root/(kind+"-install.log")).open("xb") as log:
                subprocess.run([sys.executable,"-m","pip","--python",python,"install","--no-cache-dir",*packages],
                               stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1800)
            (root/(kind+"-packages.txt")).write_text(
                subprocess.check_output([sys.executable,"-m","pip","--python",python,"freeze"],text=True),encoding="utf-8")
        env=dict(os.environ,PYTHONPATH=str(source/"src")+os.pathsep+str(source))
        # Mandatory mock/boundary checks, including the unchanged older gates.
        with (root/"boundary-tests.log").open("xb") as log:
            subprocess.run([envs["compute"],"-m","unittest","test_offline_runner",
                "test_responses_adapter","test_controlled_run","test_local_qwen_adapter","test_public_protocol","-v"],
                cwd=source,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=300)
        # Fetch the public pinned snapshot without looking for account tokens.
        fetch=source/"qwen_fetch_snapshot.py"
        print("QWEN_STAGE", "boundary checks passed; fetching pinned weights",flush=True)
        subprocess.run([envs["serve"],str(fetch),str(root/"model-snapshot.json")],check=True,timeout=2400)
        snapshot=json.loads((root/"model-snapshot.json").read_bytes())
        with socket.socket() as sock:
            sock.bind(("127.0.0.1",0));port=sock.getsockname()[1]
        endpoint="http://127.0.0.1:"+str(port);secret=secrets.token_urlsafe(32)
        serve_env=dict(os.environ)
        # vLLM reads an explicit ephemeral key; never put it in notebooks/profile.
        serve_env["VLLM_API_KEY"]=secret
        serve_env["VLLM_NO_USAGE_STATS"]="1"
        serve_env["HF_HUB_DISABLE_TELEMETRY"]="1"
        serve_log=(root/"local-server-private.log").open("xb")
        args=[envs["serve"],"-m","vllm.entrypoints.openai.api_server",
              "--model",snapshot["directory"],"--served-model-name",MODEL_ID,
              "--host","127.0.0.1","--port",str(port),"--dtype","float16",
              "--tensor-parallel-size","2","--max-model-len","16384","--max-num-seqs","1",
              "--gpu-memory-utilization","0.85","--enforce-eager","--no-enable-prefix-caching",
              "--limit-mm-per-prompt",'{"image":1,"video":0}',"--mm-processor-cache-gb","0"]
        server=subprocess.Popen(args,env=serve_env,stdout=serve_log,stderr=subprocess.STDOUT)
        print("QWEN_STAGE", "starting local Qwen",flush=True)
        # Readiness polling never generates or restarts the worker.
        from urllib.request import Request,build_opener,ProxyHandler
        opener=build_opener(ProxyHandler({}));deadline=time.time()+900;ready=False
        while time.time()<deadline:
            if server.poll() is not None:raise RuntimeError("Local Qwen server exited; no restart")
            try:
                req=Request(endpoint+"/v1/models",headers={"Authorization":"Bearer "+secret})
                with opener.open(req,timeout=5) as reply:value=json.load(reply)
                ready=any(v.get("id")==MODEL_ID for v in value.get("data",[]))
                if ready:break
            except Exception:pass
            time.sleep(2)
        if not ready:raise RuntimeError("Local server readiness deadline exceeded")
        version=subprocess.check_output([envs["serve"],"-c","import importlib.metadata as m;print(m.version('vllm'))"],text=True).strip()
        if version!="0.21.0":raise RuntimeError("Serving version differs from fixed launch")
        receipt={"model":MODEL,"max_model_len":16384,"teacher_enabled":False,
                 "weight_files_sha256":snapshot["weight_files_sha256"],
                 "tokenizer_files_sha256":snapshot["tokenizer_files_sha256"],
                 "vllm_version":version,"gpu_inventory":gpu_lines,
                 "prefix_caching_enabled":False,"vision_preprocessor_cache_gb":0,"server_pid":server.pid}
        (root/"serving-receipt.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
        # Secret is supplied to this one child process via explicit env only.
        worker_env=dict(env,QWEN_LOCAL_EPHEMERAL_KEY=secret)
        worker=source/"qwen_worker.py"
        print("QWEN_STAGE", "local model ready; qualifying tool behavior",flush=True)
        subprocess.run([envs["compute"],str(worker),str(source),str(root),endpoint],
                       env=worker_env,check=True,timeout=22200)
        print("QWEN_PAIR_TERMINAL",str(root),flush=True)
    except Exception as exc:
        (root/"entry-blocked.json").write_text(json.dumps({
            "exception_type":type(exc).__name__,"benchmark_complete":False,
            "reason":"Inspect retained private stage logs; no automatic retry or fallback",
            "run_directory":str(root)},indent=2),encoding="utf-8")
        print("QWEN_COMPARISON_BLOCKED",type(exc).__name__,str(root),flush=True)
        raise
    finally:
        if server is not None and server.poll() is None:
            server.terminate()
            try:server.wait(timeout=30)
            except subprocess.TimeoutExpired:server.kill();server.wait(timeout=10)
        if serve_log is not None:serve_log.close()
        # Do not retain a reusable ephemeral serving key in an exported log.
        log=root/"local-server-private.log"
        if log.exists():
            text=log.read_text(encoding="utf-8",errors="replace")
            if "secret" in locals():text=text.replace(secret,"[ephemeral-key-redacted]")
            log.write_text(text,encoding="utf-8")
        (root/"shutdown.json").write_text(json.dumps({"local_model_stopped":server is None or server.poll() is not None}),encoding="utf-8")
    return str(root)
