"""Validate documentation links/trace and helper behavior, not the EDI product."""
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE='a0c2c838c4ffb9cc0b7706082ad4ca5cf37a8d78'
def read(p): return json.loads((ROOT/p).read_text())
def dump(p,v):
    (ROOT/p).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/p).write_text(json.dumps(v,indent=2)+'\n')
def load(p,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/p)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
checker=load('.agents/skills/edi-interface-review/scripts/interface_matrix.py','interface_checker')
gate=load('.agents/skills/edi-component-review/scripts/review_gate.py','component_gate')
r=read('architecture/substrate/REQUIREMENTS.json')
obs=read('architecture/observation/REQUIREMENTS.json')
reqs={x['id'] for x in r['requirements']}
parents={x['id'] for x in obs['system_requirements']}
cases=set(r['verification_case_ids'])
assert len(reqs)==16 and len(cases)==22
assert all(set(x['parents'])<=parents for x in r['requirements'])
assert all(set(x['verification_case_ids'])<=cases for x in r['requirements'])
assert set().union(*(set(x['requirement_ids']) for x in r['components']))==reqs
assert set().union(*(set(x['requirement_ids']) for x in r['specifications']))==reqs
assert set().union(*(set(x['verification_case_ids']) for x in r['specifications']))==cases
assert len(r['components'])==3 and len(r['specifications'])==6
assert all(x['status']=='proposed_not_implemented' for k in ('requirements','components','specifications') for x in r[k])

mapping=[([7,8,11],[1,7]),([1,5,7,9],[2,5]),([2,5,9,11],[2,5,12]),
         ([6,14,15],[3,8,9]),([8,16],[7,11]),([10,14],[6,7,9]),
         ([2,11,15],[4,10,12]),([13,14,16],[6,9,11])]
system=read('architecture/integration/INTERFACES.json')
system['downstream_allocations']=[dict(id=f'DOWN-{i:03d}',requirement_ids=[f'SUB-R{j:03d}' for j in rs],
    verification_ids=[f'INT-V{j:03d}' for j in vs],status='proposed_not_implemented') for i,(rs,vs) in enumerate(mapping,1)]
assert {x['id'] for x in system['downstream_allocations']}=={x['id'] for x in obs['consumer_contracts']}
assert system['downstream_allocations']==read('architecture/integration/INTERFACES.json')['downstream_allocations']
results={}
for p in ('architecture/integration/INTERFACES.json','architecture/integration/SUBSTRATE_INTERNAL_INTERFACES.json'):
    cat=read(p)
    result=checker.check(cat,ROOT)
    assert result['consistent'],result
    assert all(set(c['requirement_ids'])<=reqs for c in cat['contracts'])
    assert cat['review']['product_qualification']=='not_run'
    assert all(c['status']=='specified_not_run' for c in cat['cases'])
    results[p]=result

new_docs=['architecture/substrate/SUBSTRATE_BLUEPRINT.md','architecture/substrate/BUDWORM_CHALLENGE.md',
          'architecture/integration/OBSERVATION_SUBSTRATE.md',
          '.agents/skills/edi-interface-review/SKILL.md',
          '.agents/skills/edi-component-review/SKILL.md',
          'architecture/substrate/SUBSTRATE_PLAN.md']
links=[]
for p in new_docs:
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(ROOT/p).read_text()):
        if target.startswith(('http://','https://','#')): continue
        q=(ROOT/p).parent/target.split('#')[0]
        assert q.is_file(),(p,target)
        links.append(dict(source=p,target=target))
helpers=checker.self_test()
assert gate.self_test()['positive_reports']==2
core_hashes={p:sha(p) for p in [
 'architecture/substrate/SUBSTRATE_BLUEPRINT.md','architecture/substrate/BUDWORM_CHALLENGE.md',
 'architecture/substrate/REQUIREMENTS.json','architecture/integration/OBSERVATION_SUBSTRATE.md',
 'architecture/integration/INTERFACES.json','architecture/integration/SUBSTRATE_INTERNAL_INTERFACES.json',
 '.agents/skills/edi-interface-review/SKILL.md','.agents/skills/edi-interface-review/scripts/interface_matrix.py']}
receipt=dict(schema='edi-blueprint-document-checks-v1',scope='documentation_and_skill_checks_only',input_revision=BASE,
 sha256=core_hashes,requirements=16,logical_parts=3,proposed_specifications=6,substrate_cases=22,integration_cases=12,
 all_parent_requirement_ids_exist=True,all_requirements_allocated_to_parts_and_specs=True,
 all_cases_allocated_to_specs=True,downstream_obligations_allocated=8,checked_relative_links=links,
 matrix_results=results,helper_self_tests=helpers,product_tests_run=False,
 manual_review=['DOWN-007 → SUB-R002/R011/R015 → C2 admission/C1 durable commit → INT-OS-001/010 → INT-V004/V010/V012; no ack before durable state/checkpoint consistency.',
 'DOWN-001 → SUB-R007/R008/R011 → C3 proposed inquiry/C2 admission → INT-OS-004/005/006/007/009 → INT-V007; internal and operational acceptance are not external corroboration.',
 'Budworm challenge → SUB-R003/R004/R005/R007/R009/R013/R016: supports conditional dynamics, temporal scales, alternatives, boundaries and separate stakeholder goals; discovery not demonstrated.'],
 limitations=['ID/link/pair/helper consistency is not semantic completeness or scientific validation.',
 'Native proposal/prediction/promotion/scheduling rules and concrete contracts/operating profiles remain open.',
 'No runtime, HA, full-task efficiency or new learning result is measured.'])
dump('architecture/integration/evidence/BLUEPRINT_CHECKS.json',receipt)
review=read('architecture/substrate/evidence/FUNCTION_REVIEW.json')
assert not gate.check(review,ROOT),gate.check(review,ROOT)
skill_receipt=dict(scope='skill_format_and_helper_only',format_validation='passed',
 catalogue_results=results,helper_self_tests=helpers,
 component_review_consistency='passed',product_qualification='not_run',
 validation_command='python /root/.codex/skills/oai/skill-creator/scripts/quick_validate.py .agents/skills/edi-interface-review',
 sha256={p:sha(p) for p in ['.agents/skills/edi-interface-review/SKILL.md','.agents/skills/edi-interface-review/agents/openai.yaml','.agents/skills/edi-interface-review/scripts/interface_matrix.py']})
dump('architecture/integration/evidence/SKILL_VALIDATION.json',skill_receipt)
print(json.dumps(dict(trace='passed',links=len(links),component_review='consistent',matrices=results,self_test=helpers,product_tests_run=False),indent=2))
