"""Pinned public Qwen snapshot and exact file hashes; no token lookup."""
import hashlib
import json
from pathlib import Path
import sys
from huggingface_hub import snapshot_download

MODEL="Qwen/Qwen3-VL-8B-Instruct"
REVISION="0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024**2),b""):h.update(chunk)
    return h.hexdigest()

if __name__=="__main__":
    p=Path(snapshot_download(MODEL,revision=REVISION,token=False))
    if p.name!=REVISION:raise RuntimeError("Downloaded snapshot revision differs")
    weights={f.name:digest(f) for f in p.glob("*.safetensors")}
    tokens={f.name:digest(f) for f in p.iterdir() if f.is_file() and
            (f.name.startswith("tokenizer") or "processor" in f.name or "chat_template" in f.name)}
    if not weights or not tokens:raise RuntimeError("Incomplete weight/tokenizer snapshot")
    Path(sys.argv[1]).write_text(json.dumps({"directory":str(p),"weight_files_sha256":weights,
        "tokenizer_files_sha256":tokens},indent=2),encoding="utf-8")
