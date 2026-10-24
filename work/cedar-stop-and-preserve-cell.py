# Run as one new Kaggle cell: stop this owned server, preserve state; no inference.
from pathlib import Path
import json, time, runpy
out = Path('/kaggle/working/edi-cedar-20261024')
source = Path('/kaggle/temp/edi-cedar-20261024-source')
assert (out / 'latest-state.json').is_file(), 'Existing run is absent; do not relaunch.'
report = json.loads((out / 'autonomous-server.json').read_bytes())
if not report.get('server_stopped'):
    command = out / ('command-' + str(time.time_ns()) + '-stop.json')
    with command.open('x') as stream:
        json.dump({'stage': 'stop'}, stream)
    for _ in range(45):
        report = json.loads((out / 'autonomous-server.json').read_bytes())
        if report.get('server_stopped'):
            break
        time.sleep(1)
print('OWNED_SERVER_STOPPED', report.get('server_stopped', False))
runpy.run_path(str(source / 'checkpoint.py'))['display_checkpoint'](out, source)
print('Download this final checkpoint, then use Kaggle Run > Stop session.')
