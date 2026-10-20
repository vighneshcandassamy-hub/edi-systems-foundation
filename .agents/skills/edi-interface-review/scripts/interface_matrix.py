"""Check directed interface inventory consistency, not semantic or product correctness."""
import argparse
import copy
import itertools
import json
from pathlib import Path

FACETS = ('ownership', 'authority', 'shape_versions', 'identity_scope', 'time_order',
          'delivery_idempotency', 'commit_recovery', 'retention', 'resource_limits',
          'errors', 'feedback_grounding')
GATES = ('architecture', 'contract', 'runtime', 'integration')
ACTIVE = ('required', 'optional')
DISPOSITIONS = ACTIVE + ('not_needed', 'prohibited', 'unresolved')


def concrete(value):
    return isinstance(value, str) and bool(value.strip()) and 'REPLACE_' not in value


def groups(ids, edges):
    reach = {i: {i} for i in ids}
    for a, b in edges:
        reach[a].add(b)
    for k in ids:
        for i in ids:
            if k in reach[i]:
                reach[i].update(reach[k])
    seen = set()
    result = []
    for i in ids:
        if i not in seen:
            group = sorted(j for j in ids if j in reach[i] and i in reach[j])
            seen.update(group)
            if len(group) > 1:
                result.append(group)
    return sorted(result)


def check(data, root=None):
    errors = []
    if not isinstance(data, dict):
        return {'errors': ['catalogue must be an object'], 'consistent': False}

    def ref(value):
        if not concrete(value):
            return False
        if value.startswith(('https://', 'http://')) or root is None:
            return True
        target = (root / value.split('#', 1)[0]).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            return False
        return target.is_file()

    def rows(key):
        values = data.get(key)
        if not isinstance(values, list) or any(not isinstance(x, dict) for x in values):
            errors.append(key + ' must be a list of objects')
            return []
        return values

    def unique(values, label):
        ids = [x.get('id') for x in values]
        if any(not concrete(i) for i in ids):
            errors.append(label + ' needs concrete IDs')
        ids = [i for i in ids if concrete(i)]
        if len(ids) != len(set(ids)):
            errors.append('duplicate ' + label + ' ID')
        return {x['id']: x for x in values if concrete(x.get('id'))}

    if data.get('schema') != 'edi-interface-review-v1':
        errors.append('unsupported schema')
    for key in ('scope', 'input_revision'):
        if not concrete(data.get(key)):
            errors.append('missing concrete ' + key)
    components = unique(rows('components'), 'component')
    if len(components) < 2 or any(not concrete(x.get('name')) for x in components.values()):
        errors.append('at least two named components required')
    contracts = unique(rows('contracts'), 'contract')
    cases = unique(rows('cases'), 'case')
    review = data.get('review', {})
    if not isinstance(review, dict):
        review = {}
    gate, verdict = review.get('gate'), review.get('verdict')
    if not isinstance(gate, str) or gate not in GATES:
        errors.append('invalid gate')
    if not isinstance(verdict, str) or verdict not in ('pass', 'revise', 'blocked'):
        errors.append('invalid verdict')
    if not isinstance(review.get('independent'), bool) or not concrete(review.get('scope_limit')):
        errors.append('review needs independence and scope limit')
    qualification = review.get('product_qualification')
    if not isinstance(qualification, str) or qualification not in ('not_run', 'failed', 'passed_scoped'):
        errors.append('invalid product qualification')
    lanes = rows('lanes')
    seen, linked, edges = set(), set(), []
    for lane in lanes:
        a, b = lane.get('from'), lane.get('to')
        if not concrete(a) or not concrete(b) or a not in components or b not in components:
            errors.append('lane has unknown component')
            continue
        if a == b:
            errors.append('self lane is not an intercomponent lane')
            continue
        if (a, b) in seen:
            errors.append('duplicate directed lane')
        seen.add((a, b))
        disposition = lane.get('disposition')
        if not isinstance(disposition, str) or disposition not in DISPOSITIONS:
            errors.append('invalid disposition')
        if not concrete(lane.get('rationale')):
            errors.append('lane needs rationale')
        links = lane.get('contract_ids')
        if not isinstance(links, list) or any(not concrete(i) for i in links):
            errors.append('invalid contract links')
            links = []
        if len(links) != len(set(links)):
            errors.append('duplicate contract link')
        if disposition in ACTIVE:
            edges.append((a, b))
            if not links:
                errors.append('active lane without contract')
        elif links:
            errors.append('inactive lane with contract')
        if disposition == 'unresolved' and verdict == 'pass':
            errors.append('pass has unresolved lane')
        for cid in links:
            contract = contracts.get(cid)
            if contract is None:
                errors.append('missing linked contract')
            elif (contract.get('from'), contract.get('to')) != (a, b):
                errors.append('contract linked in wrong direction')
            linked.add(cid)
    expected = set(itertools.permutations(components, 2))
    if seen != expected:
        errors.append('missing or excess directed lanes')
    if set(contracts) != linked:
        errors.append('unlinked or missing contract')
    profiles = data.get('contract_profiles', {})
    if not isinstance(profiles, dict):
        profiles = {}
        errors.append('contract_profiles must be an object')
    for contract in contracts.values():
        if not concrete(contract.get('title')):
            errors.append('contract needs title')
        for port in ('producer_port', 'consumer_port'):
            if not concrete(contract.get(port)):
                errors.append('contract needs ' + port)
        profile = profiles.get(contract.get('profile_ref'), {}) if concrete(contract.get('profile_ref')) else {}
        if contract.get('profile_ref') and not profile:
            errors.append('unknown profile')
        facets = contract.get('facets', {})
        if not isinstance(profile, dict) or not isinstance(facets, dict):
            errors.append('invalid facets/profile')
            facets = {}; profile = {}
        effective = {**profile, **facets}
        if any(not concrete(effective.get(k)) for k in FACETS):
            errors.append('missing contract facet: ' + contract['id'])
        reqs, vids = contract.get('requirement_ids'), contract.get('verification_ids')
        if not isinstance(reqs, list) or not reqs or any(not concrete(i) for i in reqs):
            errors.append('contract needs requirement links')
        if not isinstance(vids, list) or not vids or any(not concrete(i) or i not in cases for i in vids):
            errors.append('contract has missing case')
        status = contract.get('status')
        if not isinstance(status, str) or status not in ('proposed', 'concrete', 'implemented', 'runtime_verified'):
            errors.append('invalid contract status')
        if status == 'runtime_verified' and (not ref(contract.get('evidence_ref')) or not concrete(contract.get('implementation_revision'))):
            errors.append('runtime contract without evidence')
        if verdict == 'pass' and gate in ('contract', 'runtime', 'integration') and status == 'proposed':
            errors.append('pass has proposed contract')
    for case in cases.values():
        status = case.get('status')
        if not isinstance(status, str) or status not in ('specified_not_run', 'passed', 'failed', 'blocked'):
            errors.append('invalid case status')
        if not isinstance(case.get('required'), bool):
            errors.append('case needs required flag')
        if status in ('passed', 'failed') and (not ref(case.get('evidence_ref')) or not concrete(case.get('revision')) or not concrete(case.get('conditions'))):
            errors.append('executed case lacks evidence/revision/conditions')
    scc = groups(list(components), edges)
    feedback = rows('feedback_reviews')
    actual = []
    for item in feedback:
        cs = item.get('components')
        if not isinstance(cs, list) or any(not concrete(i) or i not in components for i in cs):
            errors.append('invalid feedback group'); continue
        actual.append(sorted(cs))
        vids = item.get('verification_ids')
        if not concrete(item.get('analysis')) or not isinstance(vids, list) or not vids or any(not concrete(i) or i not in cases for i in vids):
            errors.append('feedback review needs analysis/cases')
    if sorted(actual) != scc:
        errors.append('missing or duplicate feedback review')
    for finding in rows('findings'):
        blocking = finding.get('blocking_at', [])
        if not isinstance(blocking, list) or any(not isinstance(g, str) or g not in GATES for g in blocking):
            errors.append('invalid finding gates'); blocking = []
        if not concrete(finding.get('id')) or not concrete(finding.get('description')) or finding.get('status') not in ('open', 'resolved', 'deferred'):
            errors.append('invalid finding')
        if verdict == 'pass' and gate in blocking and finding.get('status') != 'resolved':
            errors.append('unresolved blocker')
    if qualification == 'passed_scoped' or (verdict == 'pass' and gate in ('runtime', 'integration')):
        required = [c for c in cases.values() if c.get('required') is True]
        if not required or any(c.get('status') != 'passed' for c in required) or not concrete(review.get('implementation_revision')) or not ref(review.get('configuration_ref')):
            errors.append('product qualification lacks passing pinned cases')
        if qualification != 'passed_scoped':
            errors.append('runtime/integration pass without scoped product qualification')
    return {'scope': 'interface_inventory_consistency_only', 'semantics_independently_verified': False,
            'component_count': len(components), 'pair_count': len(components)*(len(components)-1)//2,
            'directed_lane_count': len(lanes), 'contract_count': len(contracts),
            'feedback_groups': scc, 'consistent': not errors, 'errors': errors}


def fixture(n=2):
    ids = [chr(65+i) for i in range(n)]
    return {'schema': 'edi-interface-review-v1', 'scope': 'synthetic inventory only',
            'input_revision': 'synthetic-v1', 'components': [{'id': i, 'name': i} for i in ids],
            'lanes': [{'from': a, 'to': b, 'disposition': 'not_needed',
                       'rationale': 'Synthetic independent components.', 'contract_ids': []}
                      for a, b in itertools.permutations(ids, 2)],
            'contract_profiles': {}, 'contracts': [], 'cases': [], 'feedback_reviews': [], 'findings': [],
            'review': {'gate': 'architecture', 'verdict': 'revise', 'independent': False,
                       'product_qualification': 'not_run', 'scope_limit': 'Synthetic checker fixture only.'}}


def duplex_fixture():
    r = fixture()
    r['contract_profiles'] = {'base': {k: 'Synthetic declared behavior for '+k for k in FACETS}}
    r['cases'] = [{'id': 'V1', 'required': True, 'status': 'specified_not_run'}]
    for i, lane in enumerate(r['lanes']):
        cid = 'C'+str(i)
        lane.update(disposition='required', contract_ids=[cid])
        r['contracts'].append({'id': cid, 'from': lane['from'], 'to': lane['to'],
                               'title': 'Synthetic exchange', 'status': 'proposed', 'profile_ref': 'base',
                               'producer_port': 'p', 'consumer_port': 'q', 'requirement_ids': ['R1'],
                               'verification_ids': ['V1']})
    r['feedback_reviews'] = [{'components': ['A', 'B'], 'analysis': 'Synthetic bounded loop.', 'verification_ids': ['V1']}]
    return r


def self_test():
    for n in (2, 3, 4):
        assert check(fixture(n))['consistent']
        assert check(fixture(n))['directed_lane_count'] == n*(n-1)
    base = duplex_fixture()
    assert check(base)['consistent']
    tests = []
    def test(name, fn):
        r = copy.deepcopy(base); fn(r)
        assert not check(r)['consistent'], name
        tests.append(name)
    test('missing_reverse', lambda r: r['lanes'].pop())
    test('duplicate_lane', lambda r: r['lanes'].append(r['lanes'][0]))
    test('unknown_component', lambda r: r['lanes'][0].update(to='Z'))
    test('self_lane', lambda r: r['lanes'][0].update(to='A'))
    test('active_without_contract', lambda r: r['lanes'][0].update(contract_ids=[]))
    test('wrong_direction', lambda r: r['contracts'][0].update(to='A', **{'from': 'B'}))
    test('inactive_with_contract', lambda r: r['lanes'][0].update(disposition='prohibited'))
    test('missing_facet', lambda r: r['contract_profiles']['base'].pop('retention'))
    test('missing_case', lambda r: r['cases'].clear())
    test('missing_feedback_review', lambda r: r['feedback_reviews'].clear())
    test('runtime_without_evidence', lambda r: r['review'].update(gate='runtime', verdict='pass'))
    test('runtime_contract_without_evidence', lambda r: r['contracts'][0].update(status='runtime_verified'))
    test('false_product_qualification', lambda r: r['review'].update(product_qualification='passed_scoped'))
    test('malformed_gate', lambda r: r['review'].update(gate=[]))
    test('malformed_disposition', lambda r: r['lanes'][0].update(disposition=[]))
    test('malformed_case_status', lambda r: r['cases'][0].update(status=[]))
    def blocker(r):
        r['review']['verdict'] = 'pass'
        r['findings'] = [{'id': 'G1', 'description': 'unresolved authority', 'status': 'deferred', 'blocking_at': ['architecture']}]
    test('unresolved_blocker', blocker)
    return {'positive_reports': 4, 'negative_reports_rejected': tests}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('catalogue', nargs='?', type=Path)
    p.add_argument('--root', type=Path)
    p.add_argument('--self-test', action='store_true')
    a = p.parse_args()
    result = {}
    if a.self_test:
        result['self_test'] = self_test()
    if a.catalogue:
        result.update(check(json.loads(a.catalogue.read_text(encoding='utf-8')), a.root))
    if not result:
        p.error('supply a catalogue or --self-test')
    print(json.dumps(result, indent=2))
    return 1 if result.get('consistent') is False else 0


if __name__ == '__main__':
    raise SystemExit(main())
