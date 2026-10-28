"""Only executed by the Kaggle entry; neutral inference precedes fresh Cedar."""
import base64
import copy
import json
import struct
import zlib
import os
from pathlib import Path
import sys
from offline_runner import BoundaryError,wire
from local_qwen_adapter import MODEL,Loopback,strict
from qwen_run import run
from qwen_tool_gate import qualify

def smoke(post,root):
    prompt=[{"role":"system","content":"Neutral format check only. No ecology or benchmark answers."},
            {"role":"user","content":"Public source S-1 contains document D-1. Hypothesis H-1 is declared. "
             "Return document_id D-1 and discriminates containing H-1. Source and document IDs are different."}]
    schema={"type":"object","additionalProperties":False,
            "required":["document_id","discriminates"],"properties":{
              "document_id":{"const":"D-1"},
              "discriminates":{"type":"array","items":{"const":"H-1"},"minItems":1,"maxItems":1}}}
    def chunk(name,data):
        return struct.pack(">I",len(data))+name+data+struct.pack(">I",zlib.crc32(name+data)&0xffffffff)
    pixels=(b"\x00"+b"\xff\x00\x00"*32)*32
    image=(b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",32,32,8,2,0,0,0))+
           chunk(b"IDAT",zlib.compress(pixels))+chunk(b"IEND",b""))
    receipts=[]
    for label in ("first-neutral","second-neutral"):
        messages=copy.deepcopy(prompt);current_schema=copy.deepcopy(schema)
        expected={"document_id":"D-1","discriminates":["H-1"]}
        if label=="second-neutral":
            messages[1]["content"]=[
                {"type":"text","text":prompt[1]["content"]+" Also name the main color of the synthetic calibration image."},
                {"type":"image_url","image_url":{"url":"data:image/png;base64,"+base64.b64encode(image).decode()}}]
            current_schema["required"].append("color")
            current_schema["properties"]["color"]={"enum":["red","green","blue","yellow"]}
            expected["color"]="red"
        count_raw=post("/tokenize",{"model":MODEL["id"],"messages":messages,"add_generation_prompt":True})
        counted=strict(count_raw);n=counted.get("count")
        if type(n) is not int or n<0 or n>12288 or counted.get("max_model_len")!=16384:
            raise BoundaryError("Neutral smoke tokenizer/context failed")
        body={"model":MODEL["id"],"messages":messages,"max_tokens":256,"temperature":0,"seed":17,
              "response_format":{"type":"json_schema","json_schema":{"name":"neutral_ids","strict":True,"schema":current_schema}}}
        raw=post("/v1/chat/completions",body)
        (root/(label+"-raw.json")).write_bytes(raw)
        obj=strict(raw);choice=obj["choices"][0];out=strict(choice["message"]["content"]);usage=obj["usage"]
        if (obj["model"]!=MODEL["id"] or choice["finish_reason"]!="stop"
            or out!=expected
            or usage["prompt_tokens"]!=n or type(usage["completion_tokens"]) is not int
            or not 0<=usage["completion_tokens"]<=256):
            raise BoundaryError("Neutral schema/identity/usage smoke failed")
        if label=="second-neutral" and n<=receipts[0]["input_tokens"]:
            raise BoundaryError("Image token contribution not established")
        receipts.append({"label":label,"input_tokens":n,"output_tokens":usage["completion_tokens"],
                         "vision_input":label=="second-neutral"})
    (root/"neutral-model-smoke.json").write_text(json.dumps({"passed":True,"calls":receipts,"cedar_world_started":False},indent=2),encoding="utf-8")

if __name__=="__main__":
    source,root=Path(sys.argv[1]),Path(sys.argv[2])
    key=os.environ.pop("QWEN_LOCAL_EPHEMERAL_KEY")
    post=Loopback(sys.argv[3],key)
    smoke(post,root)
    qualify(post,root)
    receipt=json.loads((root/"serving-receipt.json").read_bytes())
    approval={"authorized":True,"kaggle_only":True,"paid_services":False,
              "model":MODEL,"neutral_checks_passed":True,"local_model_smoke_passed":True,"actual_tool_gate_passed":True}
    run(source,root/"actual-pair",endpoint=sys.argv[3],serving_token=key,
        approval=approval,serving_receipt=receipt,post=post)
