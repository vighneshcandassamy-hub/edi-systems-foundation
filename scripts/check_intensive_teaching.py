"""Run the native intensive teaching story; authored fixtures, zero live models."""
import argparse
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'tests'))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    import test_intensive_teaching
    from edi import __version__
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.with_suffix('.log').open('w',encoding='utf-8') as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_intensive_teaching))
    report={'version':__version__,'scope':'Authored teacher/student fixtures; native C0/C1/C2/C4/C7, in-process broker handler and real teacher file exchange; no model inference',
        'passed':result.wasSuccessful(),'tests_run':result.testsRun,'errors':[{'test':str(t),'traceback':s} for t,s in result.errors],
        'failures':[{'test':str(t),'traceback':s} for t,s in result.failures],
        'live_student_calls':0,'live_teacher_calls':0,'neural_weight_updates':0,'student_learning_demonstrated':False,
        'benchmark_ready':False,'live_blocker':'Opera disconnected; available Kaggle browser signed out'}
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
