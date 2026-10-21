"""Human/machine participant client: reads only the public evidence API."""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

def main():
    p=argparse.ArgumentParser();p.add_argument('operation',choices=['mission','initial','catalogue','request','submit']);p.add_argument('--url',default='http://127.0.0.1:8765');p.add_argument('--json',help='Request JSON; use - for stdin. Omit for mission.');a=p.parse_args()
    token=os.environ.get('EDI_BENCHMARK_TOKEN')
    if not token:p.error('Set the participant token in EDI_BENCHMARK_TOKEN.')
    body=None
    if a.operation!='mission':
        if not a.json:p.error('Supply --json with request_id and operation fields.')
        body=(sys.stdin.read() if a.json=='-' else a.json).encode();json.loads(body)
    req=urllib.request.Request(a.url+'/v1/'+a.operation,data=body,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:print(json.dumps(json.load(r),indent=2))
    except urllib.error.HTTPError as e:
        print(e.read().decode(),file=sys.stderr);raise SystemExit(1)

if __name__=='__main__':main()
