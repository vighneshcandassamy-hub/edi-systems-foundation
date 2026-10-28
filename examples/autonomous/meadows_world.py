"""Operator adapter for the unchanged Cedar v0.2 broker and public manual.

The participant receives native public responses through C1 only. This single
host diagnostic is not independently isolated or a blind comparison. No private
world state, audit or evaluator output is included in a model request.
"""
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
from threading import Thread

HERE=Path(__file__).resolve().parent
DEFAULT=HERE.parents[1]/"benchmarks/meadows-budworm"
ROOT=Path(os.environ.get("EDI_MEADOWS_ROOT",str(DEFAULT if DEFAULT.exists() else HERE/"meadows"))).resolve()
ENV=ROOT/"environment/v0_2"
MISSION=json.loads((ENV/"fixture/mission.json").read_bytes())
MANUAL=json.loads((ENV/"PUBLIC_OPERATIONS.json").read_bytes())
PUBLIC_OPERATIONS={x["operation"]:{"description":x["description"],
    "required_body_fields":[n for n in x["required_fields"] if n!="request_id"],
    "optional_body_fields":x["optional_or_kind_specific_fields"],
    "note":"C0 supplies request_id. Consult the public participant manual for allowed values."} for x in MANUAL["operations"]}
# Public documentation supplements argument domains, not observations or plans.
PUBLIC_OPERATIONS["act"]["public_manual"]=(ENV/"PARTICIPANT.md").read_text(encoding="utf-8")
PUBLIC_OPERATIONS["act"]["action_shapes"]=MANUAL["action_shapes"]
PUBLIC_OPERATIONS["measure"]["measurement"]=MANUAL["measurement"]

def load_broker():
    # The unchanged broker imports its pinned sibling world module.
    existing=sys.modules.get("world")
    if existing is not None and Path(existing.__file__).resolve()!=ENV/"world.py":
        raise RuntimeError("Conflicting world module; use a fresh process")
    if str(ENV) not in sys.path:sys.path.insert(0,str(ENV))
    spec=importlib.util.spec_from_file_location("edi_cedar_broker",ENV/"broker.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def restore_corpus():
    path=ROOT/"database/evidence.sqlite"
    manifest=json.loads((ENV/"fixture/manifest.json").read_bytes())
    if not path.exists():
        data=gzip.decompress(path.with_suffix(".sqlite.gz").read_bytes())
        if hashlib.sha256(data).hexdigest()!=manifest["source_corpus_sha256"]:
            raise ValueError("Pinned corpus digest mismatch")
        with path.open("xb") as stream:stream.write(data)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest["source_corpus_sha256"]:
        raise ValueError("Existing corpus differs from frozen manifest")
    return path

def start_world(out,token,port=8098):
    broker=load_broker();http=broker.server(ENV/"fixture",Path(out)/"cedar-world",restore_corpus(),token,port)
    Thread(target=http.serve_forever,daemon=True).start()
    return http

def broker_snapshot(out):
    # Operator preservation only. This object never enters the student prompt.
    path=Path(out)/"cedar-world/run.sqlite"
    with sqlite3.connect(path.as_uri()+"?mode=ro",uri=True) as db:
        requests=[{"request_id":r[0],"operation":r[1]} for r in db.execute("SELECT id,operation FROM events ORDER BY rowid")]
        state=json.loads(db.execute("SELECT payload FROM state WHERE id=1").fetchone()[0])
    return {"requests":requests,"conclusions":[state["final"]] if state.get("final") else []}

def evaluate_closed(out):
    # Called only after native controller termination; never returned to models.
    spec=importlib.util.spec_from_file_location("edi_cedar_evaluator",ENV/"evaluate.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.evaluate(Path(out)/"cedar-world")
