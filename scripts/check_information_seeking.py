"""Check the current controller contract before starting a live student.

Native regressions use authored outputs and an in-process broker handler. The
optional grammar check requires the serving environment's jsonschema/xgrammar.
Neither mode contacts a provider or proves autonomous acquisition.
"""
import argparse
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
sys.path.insert(0, str(ROOT/'tests'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--grammar', action='store_true')
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    import test_information_seeking
    with args.output.with_suffix('.log').open('w', encoding='utf-8') as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromModule(test_information_seeking))
    report = {'version': '0.10.7.dev0', 'scope': 'authored native controller regressions; in-process HTTP handler; no model or socket',
        'passed': result.wasSuccessful(), 'tests_run': result.testsRun,
        'errors': [{'test':str(t),'traceback':s} for t,s in result.errors],
        'failures': [{'test':str(t),'traceback':s} for t,s in result.failures],
        'model_calls': 0, 'network_verified': False, 'grammar': 'not_requested'}
    if args.grammar:
        try:
            import jsonschema
            import xgrammar
            from edi.reason.operation_args import serving_schema
            schema = serving_schema(evidence_references=[], controller_turn=True,
                controller_policy='information-seeking/1.0')
            xgrammar.Grammar.from_json_schema(json.dumps(schema))
            validator = jsonschema.Draft202012Validator(schema)
            valid = {'rationale_summary':'Authored empty-cut decision', 'limitation':'No evidence or live reasoning',
                'operation_proposals':[test_information_seeking.stop()]}
            validator.validate(valid)
            for field in ('reason','assessment'):
                bad = copy.deepcopy(valid)
                bad['operation_proposals'][0]['arguments'].pop(field)
                if validator.is_valid(bad):
                    raise AssertionError('decoder accepted missing yield ' + field)
            report['grammar'] = 'compiled with xgrammar; valid stop accepted and incomplete stops rejected by JSON Schema'
        except Exception as exc:
            report.update(passed=False, grammar='failed', grammar_error=type(exc).__name__+': '+str(exc))
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
