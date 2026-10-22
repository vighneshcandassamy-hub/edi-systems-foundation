"""Two neutral requests to a loopback vLLM server; no EDI benchmark."""
import base64, hashlib, io, json, os, secrets, signal, subprocess, sys, time, traceback
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from huggingface_hub import HfApi, snapshot_download
from PIL import Image, ImageDraw
ROOT=Path("/kaggle/temp/edi-free-vllm")
OUT=Path(os.environ.get("EDI_DIAGNOSTIC_OUT","/kaggle/working"))
OUT.mkdir(parents=True,exist_ok=True)
REPORT={"stage":"starting","sampler":"pytorch","profile_version":"kaggle-t4-native16k-xgrammar-v2","benchmark_started":False,"paid_fallback":False,"model":"Qwen/Qwen3-VL-8B-Instruct",
        "profile":{"dtype":"float16","tensor_parallel_size":2,"max_model_len":16384,"image_count":1,
                   "max_image_pixels":65536,"max_output_tokens_per_request":4096,"temperature":0,"seed":17}}
def update(stage,**fields):
    REPORT.update(stage=stage,**fields)
    temp=OUT/"edi-native-loop3-server.json.tmp"
    temp.write_text(json.dumps(REPORT,indent=2))
    temp.replace(OUT/"edi-native-loop3-server.json")
    print(stage,flush=True)
def post(body,key):
    request=Request("http://127.0.0.1:8008/v1/chat/completions",data=json.dumps(body).encode(),
                    headers={"Content-Type":"application/json","Authorization":"Bearer "+key})
    with urlopen(request,timeout=120) as response:
        return json.load(response)
server=None
log=None
try:
    import torch, vllm, transformers
    update("resolving_model",versions={"torch":torch.__version__,"cuda":torch.version.cuda,
                                      "vllm":vllm.__version__,"transformers":transformers.__version__})
    info=HfApi(token=False).model_info(REPORT["model"],revision='0c351dd01ed87e9c1b53cbc748cba10e6187ff3b',files_metadata=True)
    revision=info.sha
    if not revision or len(revision)!=40:
        raise RuntimeError("No exact model revision")
    expected={f.rfilename:getattr(f.lfs,"sha256",None) for f in info.siblings if getattr(f,"lfs",None)}
    update("downloading_model",model_revision=revision)
    snapshot=Path(snapshot_download(REPORT["model"],revision=revision,token=False,
        cache_dir=str(ROOT/"hf-cache"),
        allow_patterns=["*.json","*.safetensors","*.txt","*.jinja","*.model"],max_workers=4))
    manifest=[]
    update("hashing_model")
    for file in sorted(snapshot.rglob("*")):
        if not file.is_file():
            continue
        digest=hashlib.file_digest(file.open("rb"),"sha256").hexdigest()
        relative=file.relative_to(snapshot).as_posix()
        if expected.get(relative) and expected[relative]!=digest:
            raise RuntimeError("Model file digest mismatch: "+relative)
        manifest.append({"path":relative,"bytes":file.stat().st_size,"sha256":digest})
    (OUT/"edi-native-loop3-qwen-artifacts.json").write_text(json.dumps(
        {"repository":REPORT["model"],"revision":revision,"files":manifest},indent=2))
    key=secrets.token_urlsafe(32)
    env=dict(os.environ,HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1",
             HF_HUB_DISABLE_IMPLICIT_TOKEN="1",VLLM_NO_USAGE_STATS="1",DO_NOT_TRACK="1",
             VLLM_API_KEY=key,VLLM_WORKER_MULTIPROC_METHOD="spawn",VLLM_USE_FLASHINFER_SAMPLER="0")
    command=[sys.executable,"-m","vllm.entrypoints.openai.api_server",
        "--model",str(snapshot),"--served-model-name",REPORT["model"],
        "--tokenizer",str(snapshot),"--host","127.0.0.1","--port","8008",
        "--structured-outputs-config.backend","xgrammar",
        "--dtype","half","--tensor-parallel-size","2","--max-model-len","16384",
        "--gpu-memory-utilization","0.90","--max-num-seqs","1",
        "--max-num-batched-tokens","16384","--enforce-eager","--disable-custom-all-reduce",
        "--load-format","safetensors","--attention-backend","TRITON_ATTN",
        "--mm-encoder-attn-backend","TORCH_SDPA",
        "--limit-mm-per-prompt",json.dumps({"image":1,"video":0}),
        "--mm-processor-kwargs",json.dumps({"min_pixels":4096,"max_pixels":65536})]
    env.pop("PYTHONPATH",None)
    env.pop("PYTHONHOME",None)
    log=(OUT/"edi-native-loop3-server.log").open("w")
    update("starting_server",server_command=command)
    server=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
    deadline=time.monotonic()+720
    while time.monotonic()<deadline:
        if server.poll() is not None:
            raise RuntimeError("vLLM server exited with "+str(server.returncode))
        try:
            request=Request("http://127.0.0.1:8008/v1/models",headers={"Authorization":"Bearer "+key})
            with urlopen(request,timeout=2) as response:
                catalog=json.load(response)
            break
        except (URLError,TimeoutError):
            time.sleep(2)
    else:
        raise TimeoutError("vLLM startup deadline exceeded")
    update("native_edi_probe")
    import importlib.util
    spec=importlib.util.spec_from_file_location("edi_native_probe",str(Path(__file__).with_name("edi_neutral_investigation_v3.py")))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=module.run("http://127.0.0.1:8008",key,OUT)
    update("native_edi_completed" if result["status"]=="closed" else "native_edi_failed",
        edi_status=result["status"],turn_count=len(result["turns"]))

except Exception as error:
    update("failed",error_type=type(error).__name__,error=str(error)[:500])
    traceback.print_exc()
finally:
    if server and server.poll() is None:
        os.killpg(server.pid,signal.SIGTERM)
        try:
            server.wait(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(server.pid,signal.SIGKILL)
            server.wait(timeout=10)
    if log:
        log.close()
    REPORT["server_stopped"]=True
    update(REPORT["stage"])
    print(subprocess.run(["nvidia-smi","--query-gpu=name,memory.used,utilization.gpu","--format=csv,noheader"],text=True,capture_output=True).stdout,flush=True)
