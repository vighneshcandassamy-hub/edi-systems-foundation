"""One authored native mission plus optional serving grammar check; no inference."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'tests'))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--grammar',action='store_true')
    args=parser.parse_args()
    from test_decision_grounding import DecisionGroundingTests
    from edi import __version__
    from edi.reason.operation_args import serving_schema
    schema=serving_schema(controller_turn=True,controller_policy='information-seeking/1.1',evidence_references=[])
    grammar='not-run-on-this-host'
    schema_status='native Pydantic admission exercised; external schema checker not run'
    if args.grammar:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
        schema_status="valid"
        import xgrammar
        xgrammar.Grammar.from_json_schema(json.dumps(schema))
        grammar='compiled'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.with_suffix('.log').open('w',encoding='utf-8') as stream:
        suite=unittest.TestSuite([DecisionGroundingTests('test_native_grounded_mission_rejects_unsupported_basis_and_closes')])
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    files=['src/edi/reason/contracts.py','src/edi/reason/decision.py','src/edi/reason/gateway.py','src/edi/reason/operation_args.py','src/edi/reason/service.py','src/edi/reason/teaching.py','src/edi/inquiry/benchmark.py','tests/test_decision_grounding.py','tests/test_information_seeking.py']
    report={'version':__version__,'scope':'One authored native five-turn mission, actual broker handler, admission rejections, blind first assessments, revision feedback, closure and no-redispatch reopen. No model inference or autonomous reasoning result.','passed':result.wasSuccessful(),'tests_run':result.testsRun,'grammar':grammar,'json_schema':schema_status,'errors':[{'test':str(t),'traceback':s} for t,s in result.errors],'failures':[{'test':str(t),'traceback':s} for t,s in result.failures],'model_calls':0,'neural_weight_updates':0,'files_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}}
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
