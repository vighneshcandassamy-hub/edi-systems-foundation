"""Two neutral requests to a loopback vLLM server; no EDI benchmark."""
import base64, hashlib, io, json, os, secrets, signal, subprocess, sys, time, traceback
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from huggingface_hub import HfApi, snapshot_download
from PIL import Image, ImageDraw
ROOT=Path("/kaggle/temp/edi-free-vllm")
OUT=Path("/kaggle/working")
REPORT={"stage":"starting","sampler":"pytorch","profile_version":"kaggle-t4-fp16-v1","benchmark_started":False,"paid_fallback":False,"model":"Qwen/Qwen3-VL-8B-Instruct",
        "profile":{"dtype":"float16","tensor_parallel_size":2,"max_model_len":4096,"image_count":1,
                   "max_image_pixels":65536,"max_output_tokens_per_request":32,"temperature":0,"seed":17}}
def update(stage,**fields):
    REPORT.update(stage=stage,**fields)
    temp=OUT/"edi-free-vllm-probe.json.tmp"
    temp.write_text(json.dumps(REPORT,indent=2))
    temp.replace(OUT/"edi-free-vllm-probe.json")
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
    (OUT/"edi-free-qwen-artifacts.json").write_text(json.dumps(
        {"repository":REPORT["model"],"revision":revision,"files":manifest},indent=2))
    key=secrets.token_urlsafe(32)
    env=dict(os.environ,HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1",
             HF_HUB_DISABLE_IMPLICIT_TOKEN="1",VLLM_NO_USAGE_STATS="1",DO_NOT_TRACK="1",
             VLLM_API_KEY=key,VLLM_WORKER_MULTIPROC_METHOD="spawn",VLLM_USE_FLASHINFER_SAMPLER="0")
    command=[sys.executable,"-m","vllm.entrypoints.openai.api_server",
        "--model",str(snapshot),"--served-model-name",REPORT["model"],
        "--tokenizer",str(snapshot),"--host","127.0.0.1","--port","8008",
        "--dtype","half","--tensor-parallel-size","2","--max-model-len","4096",
        "--gpu-memory-utilization","0.90","--max-num-seqs","1",
        "--max-num-batched-tokens","4096","--enforce-eager","--disable-custom-all-reduce",
        "--load-format","safetensors","--attention-backend","TRITON_ATTN",
        "--mm-encoder-attn-backend","TORCH_SDPA",
        "--limit-mm-per-prompt",json.dumps({"image":1,"video":0}),
        "--mm-processor-kwargs",json.dumps({"min_pixels":4096,"max_pixels":65536})]
    env.pop("PYTHONPATH",None)
    env.pop("PYTHONHOME",None)
    log=(OUT/"edi-free-vllm-server.log").open("w")
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
    update("neutral_text_request")
    text_response=post(dict(model=REPORT["model"],messages=[{"role":"user","content":"What is 1 + 1? Reply with the digit only."}],
                            max_tokens=32,temperature=0,seed=17),key)
    image=Image.new("RGB",(256,128),"white")
    draw=ImageDraw.Draw(image)
    draw.rectangle((16,16,112,112),fill=(255,0,0))
    draw.ellipse((144,16,240,112),fill=(0,0,255))
    raw=io.BytesIO(); image.save(raw,format="PNG"); data=raw.getvalue()
    (OUT/"edi-free-neutral-image.png").write_bytes(data)
    update("neutral_image_request",image_sha256=hashlib.sha256(data).hexdigest())
    image_response=post(dict(model=REPORT["model"],messages=[{"role":"user","content":[
        {"type":"text","text":"Name the shape and its color on the left, then on the right."},
        {"type":"image_url","image_url":{"url":"data:image/png;base64,"+base64.b64encode(data).decode()}}]}],
        max_tokens=32,temperature=0,seed=17),key)
    (OUT/"edi-free-neutral-responses.json").write_text(json.dumps(
        {"text":text_response,"image":image_response},indent=2))
    update("neutral_requests_completed",
        text_answer=text_response["choices"][0]["message"]["content"],
        image_answer=image_response["choices"][0]["message"]["content"],
        text_usage=text_response.get("usage"),image_usage=image_response.get("usage"))
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
