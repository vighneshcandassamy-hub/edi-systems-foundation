"""Operator audit of existing evidence access, not an EDI reasoning test.

Reads only the initial/investigation snapshots, mission, and broker/world code.
Never opens evaluator data. Restores into a temporary directory; baseline is unchanged.
"""
import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
import secrets
import sqlite3
import tempfile
import threading
import urllib.error
import urllib.request
from pathlib import Path


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def audit(root):
    root = root.resolve()
    fixture = root / 'fixture'
    broker_module = module(root / 'broker.py', 'audited_broker')
    world = module(root / 'world.py', 'audited_world')
    snapshots = {}
    for role in ('initial', 'investigation'):
        path = fixture / role / (role + '.sqlite.gz')
        snapshots[role] = hashlib.sha256(path.read_bytes()).hexdigest()
    corpus = root.parents[1] / 'database/evidence.sqlite'
    corpus_before = hashlib.sha256(corpus.read_bytes()).hexdigest() if corpus.exists() else None
    with tempfile.TemporaryDirectory(prefix='edi-evidence-audit-') as temporary:
        env = Path(temporary) / 'environment'
        expected = {}
        for role in ('initial', 'investigation'):
            (env / role).mkdir(parents=True)
            path = env / role / (role + '.sqlite')
            path.write_bytes(gzip.decompress((fixture / role / (role + '.sqlite.gz')).read_bytes()))
            with sqlite3.connect(path) as connection:
                expected[role] = connection.execute('SELECT count(*) FROM items').fetchone()[0]
        (env / 'participant').mkdir()
        (env / 'participant/mission.json').write_bytes((fixture / 'participant/mission.json').read_bytes())
        token = secrets.token_urlsafe(32)
        http = broker_module.server(env, Path(temporary) / 'run', token)
        worker = threading.Thread(target=http.serve_forever, daemon=True)
        worker.start()
        url = 'http://127.0.0.1:' + str(http.server_port) + '/v1/'
        serial = 0

        def request(operation, payload):
            nonlocal serial
            serial += 1
            payload = dict(payload, request_id='operator-audit-' + str(serial))
            req = urllib.request.Request(url + operation, data=json.dumps(payload).encode(),
                  headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    return response.status, json.load(response)
            except urllib.error.HTTPError as error:
                return error.code, json.load(error)

        try:
            catalog = []
            offset = 0
            while True:
                code, result = request('catalogue', {'query': '', 'offset': offset, 'limit': 50})
                assert code == 200, result
                catalog.extend(result['items'])
                if not result['has_more']:
                    break
                offset += result['returned']
            assert len(catalog) == expected['investigation']
            assert len({x['item_id'] for x in catalog}) == len(catalog)
            initial = []
            offset = 0
            while True:
                code, result = request('initial', {'offset': offset, 'limit': 50})
                assert code == 200, result
                initial.extend(result['items'])
                if not result['has_more']:
                    break
                offset += result['returned']
            assert len(initial) == expected['initial']
            retrieved = []
            inquiries = {'rationale': 'Operator transport audit; not a participant hypothesis.',
                         'expected_observation': 'Return the existing recorded material, if available.'}
            for item in catalog:
                code, result = request('request', dict(inquiries, item_id=item['item_id'],
                           limit=200, include_asset=True, asset_limit=65536))
                assert code == 200, result
                records = list(result['records'])
                offset = result['returned']
                while result['has_more']:
                    code, result = request('request', dict(inquiries, item_id=item['item_id'],
                                         limit=200, offset=offset))
                    assert code == 200, result
                    records.extend(result['records'])
                    offset += result['returned']
                # Request the original asset separately, so record paging never loses it.
                code, result = request('request', dict(inquiries, item_id=item['item_id'],
                                       limit=1, include_asset=True, asset_limit=65536))
                assert code == 200, result
                asset = result['asset']
                data = bytearray(base64.b64decode(asset['data']))
                while asset['has_more']:
                    code, chunk = request('request', dict(inquiries, item_id=item['item_id'], limit=1,
                                      include_asset=True, asset_limit=65536, asset_offset=len(data)))
                    assert code == 200, chunk
                    asset = chunk['asset']
                    data.extend(base64.b64decode(asset['data']))
                assert hashlib.sha256(data).hexdigest() == item['asset_sha256']
                retrieved.append({'item_id': item['item_id'], 'title': item['title'],
                     'scope': item['scope'], 'format': item['format'],
                     'records': len(records), 'verified_asset_bytes': len(data)})
            searches = []
            for query in ('natural enemies', 'birds', 'parasites', 'feeding', 'forest composition',
                          'historical tree rings', 'mill demand', 'employment', 'manager correspondence',
                          'spraying', 'treatment', 'weather'):
                code, result = request('catalogue', {'query': query, 'limit': 50})
                assert code == 200, result
                searches.append({'query': query, 'matched': result['total_matched'],
                                 'titles': sorted({x['title'] for x in result['items']})})
            item_id = catalog[0]['item_id']
            probes = {}
            for name, operation, payload in [
                ('request_without_reasoning_template', 'request', {'item_id': item_id}),
                ('unknown_record', 'request', dict(inquiries, item_id='not-an-existing-record')),
                ('future_record', 'request', dict(inquiries, item_id=item_id, year_range=[61, 62])),
                ('ask_person', 'ask', {'question': 'What is the purpose of the protection budget?'}),
                ('new_measurement', 'measure', {'location': 'P01'}),
                ('intervention', 'act', {'location': 'P01'}),
                ('objective_clarification', 'clarify', {'question': 'Which outcomes matter?'}),
            ]:
                code, result = request(operation, payload)
                probes[name] = {'http_status': code, 'code': result.get('code'), 'message': result.get('message')}
            assert probes['request_without_reasoning_template']['http_status'] == 400
            assert probes['unknown_record']['http_status'] == 404
            assert probes['future_record']['http_status'] == 403
            assert all(probes[n]['http_status'] == 404 for n in
                       ('ask_person', 'new_measurement', 'intervention', 'objective_clarification'))
        finally:
            http.shutdown()
            http.server_close()
            worker.join(timeout=5)
    state = {'insects': 1., 'foliage': .8, 'mature_host': .6, 'enemies': .5}
    untreated, _ = world.step(state, weather=0., spray=0.)
    treated, _ = world.step(state, weather=0., spray=1.)
    structural_diagnostic = {
        'fixed_state': state,
        'untreated_next_enemies': untreated['enemies'],
        'treated_next_enemies': treated['enemies'],
        'direct_treatment_effect_on_enemies': treated['enemies'] - untreated['enemies'],
        'interpretation': 'Current enemy transition has no spray input. It cannot test the interlude\'s direct non-target treatment pathway. Indirect later effects through prey are distinct.'}
    unchanged = all(hashlib.sha256((fixture / role / (role + '.sqlite.gz')).read_bytes()).hexdigest() == digest
                    for role, digest in snapshots.items())
    if corpus_before:
        unchanged = unchanged and hashlib.sha256(corpus.read_bytes()).hexdigest() == corpus_before
    assert unchanged
    inputs = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in [root / 'broker.py', root / 'world.py', root / 'build.py',
                           fixture / 'participant/mission.json',
                           fixture / 'initial/initial.sqlite.gz',
                           fixture / 'investigation/investigation.sqlite.gz']}
    return {'scope': 'Operator HTTP reachability and structural diagnostic, not EDI inquiry/reasoning.',
            'baseline_revision': '6650dc94c4ea640e43fc52ccd42cfd93cad49c98', 'input_sha256': inputs,
            'initial_items_read': len(initial), 'requestable_items_discovered': len(catalog),
            'requestable_items_fetched_and_assets_verified': len(retrieved),
            'retrieved': retrieved, 'search_probes': searches, 'operation_probes': probes,
            'model_diagnostic': structural_diagnostic, 'baseline_unchanged': unchanged,
            'edi_run': False, 'historical_sufficiency_established': False,
            'interlude_discovery_ready': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = audit(Path(__file__).resolve().parent)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'retrieved'}, indent=2))
