"""Public client. Participant gets this file and README only, never operator world/state."""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def main():
    p=argparse.ArgumentParser()
    p.add_argument('operation',choices=['mission','sources','people','search','read','records','ask','measure','act','advance','status','propose','submit'])
    p.add_argument('--url',default='http://127.0.0.1:8766')
    p.add_argument('--json',default='-',help='JSON text or - to read stdin; must include a unique request_id')
    a=p.parse_args()
    body=json.loads(sys.stdin.read() if a.json=='-' else a.json)
    token=os.environ.get('EDI_BENCHMARK_TOKEN','')
    req=urllib.request.Request(a.url+'/v2/'+a.operation,data=json.dumps(body).encode(),
      headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=60) as r:result=json.load(r)
    except urllib.error.HTTPError as e:
        result=json.load(e);print(json.dumps(result,indent=2,ensure_ascii=False));return 1
    print(json.dumps(result,indent=2,ensure_ascii=False));return 0


if __name__=='__main__':raise SystemExit(main())
