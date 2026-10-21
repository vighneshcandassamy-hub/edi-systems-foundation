"""Run real CPU engineering checks; fixture model transports are not inference."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    log_path = args.out / "cpu-tests.log"
    with log_path.open("w", encoding="utf-8") as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT / "tests")))
    sources = sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "tests").glob("*.py"))
    report = {"schema":"edi-benchmark-engineering-results-v1", "host_os":platform.system(),
        "python":platform.python_version(), "pydantic":importlib.metadata.version("pydantic"),
        "tests_run":result.testsRun, "tests_passed":result.testsRun-len(result.errors)-len(result.failures)-len(result.skipped),
        "errors":[{"test":str(t),"traceback":s} for t,s in result.errors],
        "failures":[{"test":str(t),"traceback":s} for t,s in result.failures],
        "passed":result.wasSuccessful(), "real_broker":True, "native_owner_stores":True,
        "model_transport":"authored wire fixtures only", "live_student_inference":False,
        "live_teacher_inference":False, "model_vision_understanding_tested":False,
        "full_P1_eight_owner_test_run":False, "unguided_pilot_run":False, "scientific_qualification":False,
        "test_log_sha256":hashlib.sha256(log_path.read_bytes()).hexdigest(),
        "source_sha256":{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    (args.out / "cpu-tests.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="source_sha256"}, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
