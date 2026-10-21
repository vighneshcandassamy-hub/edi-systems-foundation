"""Explicit public allowlist. Never export archive, world, initial state, runs or operator reports."""
import argparse
import json
import zipfile
from pathlib import Path


def export(destination):
    root=Path(__file__).resolve().parent
    if destination.exists():raise ValueError('Refusing to overwrite an existing participant archive')
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for name in ('client.py','PUBLIC_OPERATIONS.json','PARTICIPANT.md'):
            z.write(root/name,name)
        z.write(root/'fixture/mission.json','mission.json')
    return {'file':str(destination),'contains':['client.py','PUBLIC_OPERATIONS.json','PARTICIPANT.md','mission.json'],
            'limit':'Run the participant under a separate account/container without operator files or credentials.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    print(json.dumps(export(a.out),indent=2))
