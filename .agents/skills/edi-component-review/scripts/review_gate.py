"""Check review-report consistency; do not infer scientific or product readiness."""
import argparse
import copy
import json
from pathlib import Path

CRITERIA = {'mission_trace','boundary_contract','necessity_simplicity','evidence_uncertainty','resource_envelope','failure_recovery','sourced_choices','verification_scope'}
GATES = {'architecture','contract','runtime','integration'}


def check(report, root=None):
    errors=[]
    if not isinstance(report,dict):
        return ['report must be an object']
    def text(value):
        return isinstance(value,str) and bool(value.strip()) and 'REPLACE_' not in value
    def reference(value):
        if not text(value):
            return False
        if root is None or value.startswith(('https://','http://')):
            return True
        target=(root/value.split('#',1)[0]).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            return False
        return target.is_file()
    if report.get('schema') != 'edi-component-review-v1':
        errors.append('unsupported report schema')
    for key in ('reviewed_component','requested_scope','input_revision','next_step'):
        if not text(report.get(key)):
            errors.append('missing concrete '+key)
    gate=report.get('gate')
    if not isinstance(gate,str) or gate not in GATES:
        errors.append('invalid gate')
    verdict=report.get('verdict')
    if verdict not in ('pass','revise','blocked'):
        errors.append('invalid verdict')
    reviewer=report.get('reviewer',{})
    if not isinstance(reviewer,dict) or not text(reviewer.get('role')) or not isinstance(reviewer.get('independent'),bool):
        errors.append('reviewer role/independence must be explicit')
    trace=report.get('traceability',{})
    if not isinstance(trace,dict):
        trace={}; errors.append('invalid traceability')
    if not reference(trace.get('source')):
        errors.append('missing trace authority')
    if verdict=='pass' and (trace.get('checked') is not True or not reference(trace.get('evidence_ref'))):
        errors.append('pass requires a recorded trace check')
    criteria=report.get('criteria',[])
    if not isinstance(criteria,list):
        criteria=[]; errors.append('criteria must be a list')
    ids=[c.get('id') for c in criteria if isinstance(c,dict) and isinstance(c.get('id'),str)]
    if len(ids)!=len(criteria) or len(ids)!=len(set(ids)) or set(ids)!=CRITERIA:
        errors.append('criteria must contain each required ID exactly once')
    for c in criteria:
        if not isinstance(c,dict):
            continue
        if c.get('status') not in ('pass','revise','blocked','not_applicable') or not text(c.get('rationale')):
            errors.append('criterion needs valid status and rationale: '+str(c.get('id')))
        refs=c.get('references',[])
        if not isinstance(refs,list) or any(not reference(r) for r in refs):
            errors.append('invalid criterion references: '+str(c.get('id')))
            refs=[]
        if c.get('status')=='pass' and not refs:
            errors.append('passed criterion needs artifact reference: '+str(c.get('id')))
        if verdict=='pass' and c.get('status') not in ('pass','not_applicable'):
            errors.append('pass conflicts with unresolved criterion: '+str(c.get('id')))
    for key in ('findings','changes','verification','measurements'):
        if not isinstance(report.get(key),list):
            errors.append(key+' must be a list')
    for f in report.get('findings',[]) if isinstance(report.get('findings'),list) else []:
        if not isinstance(f,dict):
            errors.append('invalid finding'); continue
        if not text(f.get('id')) or not text(f.get('description')) or f.get('status') not in ('open','resolved','deferred'):
            errors.append('finding needs ID, description and state')
        blocking=f.get('blocking_at',[])
        if not isinstance(blocking,list) or any(not isinstance(g,str) or g not in GATES for g in blocking):
            errors.append('invalid finding blocking gates'); blocking=[]
        if verdict=='pass' and gate in blocking and f.get('status')!='resolved':
            errors.append('pass has unresolved gate-blocking finding: '+str(f.get('id')))
    for m in report.get('measurements',[]) if isinstance(report.get('measurements'),list) else []:
        if not isinstance(m,dict):
            errors.append('invalid measurement'); continue
        if m.get('state') not in ('proposed','not_run','measured'):
            errors.append('invalid measurement state')
        if m.get('state')=='measured':
            if 'value' not in m or not reference(m.get('evidence_ref')) or not text(m.get('revision')) or not text(m.get('conditions')):
                errors.append('measured result needs value, evidence, revision and conditions')
        elif 'value' in m:
            errors.append('unmeasured target must not contain achieved value')
    executed=[]
    for v in report.get('verification',[]) if isinstance(report.get('verification'),list) else []:
        if not isinstance(v,dict) or v.get('status') not in ('not_run','passed','failed','blocked') or v.get('kind') not in ('documentation','contract','runtime','integration'):
            errors.append('invalid verification case'); continue
        if v.get('status') in ('passed','failed'):
            if not reference(v.get('evidence_ref')) or not text(v.get('revision')):
                errors.append('executed case needs evidence and revision')
        if v.get('kind') in ('runtime','integration') and v.get('required') is True:
            executed.append(v)
    qualification=report.get('product_qualification')
    if qualification not in ('not_run','failed','passed_scoped'):
        errors.append('invalid product qualification state')
    if qualification=='passed_scoped' and (not executed or any(v.get('status')!='passed' for v in executed)):
        errors.append('product pass lacks passing required runtime evidence')
    if verdict=='pass' and gate in ('runtime','integration') and qualification!='passed_scoped':
        errors.append('runtime/integration pass requires scoped product evidence')
    if verdict=='pass' and gate=='integration' and not any(v.get('kind')=='integration' and v.get('required') is True and v.get('status')=='passed' for v in executed):
        errors.append('integration pass lacks integration evidence')
    return errors


def self_test():
    base={'schema':'edi-component-review-v1','reviewed_component':'synthetic component','gate':'architecture','requested_scope':'design_only','input_revision':'synthetic-fixture-v1','reviewer':{'role':'test_fixture','independent':False},'traceability':{'source':'synthetic/requirements.json','checked':True,'evidence_ref':'synthetic/trace-check.json'},'criteria':[{'id':k,'status':'pass','rationale':'Synthetic reference for checker behavior, not a real design approval.','references':['synthetic/design.md']} for k in sorted(CRITERIA)],'findings':[],'changes':[],'verification':[],'measurements':[],'product_qualification':'not_run','verdict':'pass','next_step':'Exercise report consistency only.'}
    assert not check(base),check(base)
    tests=[]
    r=copy.deepcopy(base); r['criteria'].pop(); tests.append(('missing_criterion',r,'each required ID'))
    r=copy.deepcopy(base); r['criteria'].append(r['criteria'][0]); tests.append(('duplicate_criterion',r,'each required ID'))
    r=copy.deepcopy(base); r['criteria'][0]['status']='revise'; tests.append(('false_design_pass',r,'unresolved criterion'))
    r=copy.deepcopy(base); r['findings']=[{'id':'X','description':'unresolved authority','status':'deferred','blocking_at':['architecture']}]; tests.append(('deferred_blocker',r,'gate-blocking'))
    r=copy.deepcopy(base); r['measurements']=[{'state':'proposed','value':100}]; tests.append(('target_as_result',r,'unmeasured target'))
    r=copy.deepcopy(base); r['measurements']=[{'state':'measured','value':100}]; tests.append(('unsupported_measurement',r,'measured result needs'))
    r=copy.deepcopy(base); r['gate']='runtime'; tests.append(('runtime_without_evidence',r,'scoped product evidence'))
    r=copy.deepcopy(base); r['product_qualification']='passed_scoped'; tests.append(('paperwork_as_runtime',r,'passing required runtime evidence'))
    r=copy.deepcopy(base); r['traceability']['checked']=False; tests.append(('unchecked_trace',r,'recorded trace check'))
    r=copy.deepcopy(base); r['criteria'][0]['id']=[]; tests.append(('malformed_criterion_id',r,'each required ID'))
    r=copy.deepcopy(base); r['gate']=[]; tests.append(('malformed_gate',r,'invalid gate'))
    for name,r,expected in tests:
        assert any(expected in e for e in check(r)),name
    r=copy.deepcopy(base); r['verdict']='revise'; r['criteria'][0]['status']='revise'; assert not check(r)
    return {'positive_reports':2,'negative_reports_rejected':[n for n,_,_ in tests]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('report',nargs='?',type=Path)
    p.add_argument('--root',type=Path)
    p.add_argument('--self-test',action='store_true')
    args=p.parse_args()
    result={'scope':'report_consistency_only','readiness_independently_verified':False}
    if args.self_test:
        result['self_test']=self_test()
    if args.report:
        errors=check(json.loads(args.report.read_text(encoding='utf-8')),args.root)
        result.update({'report':str(args.report),'consistent':not errors,'errors':errors})
        print(json.dumps(result,indent=2))
        return 1 if errors else 0
    if not args.self_test:
        p.error('supply a review report or --self-test')
    print(json.dumps(result,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
