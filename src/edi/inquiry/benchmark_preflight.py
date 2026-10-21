"""Read-only execution-host checks. Never installs software or prints credentials."""
import argparse
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def command(arguments):
    try:
        p = subprocess.run(arguments, capture_output=True, text=True, timeout=10)
        return {"exit_code": p.returncode, "output": p.stdout.strip()[:2000], "error": p.stderr.strip()[:500]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"exit_code": None, "error": type(exc).__name__}


def inspect_host(*, teacher_required=True):
    gpu = command(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"])
    gpu_memory = []
    if gpu.get("exit_code") == 0:
        for line in gpu.get("output", "").splitlines():
            try: gpu_memory.append(int(line.split(",")[1].strip()))
            except (IndexError, ValueError): pass
    docker = command(["docker", "info", "--format", "{{.OSType}}"])
    try: pydantic_version = importlib.metadata.version("pydantic")
    except importlib.metadata.PackageNotFoundError: pydantic_version = None
    checks = [
        {"id":"python", "passed":(3,12) <= sys.version_info[:2] < (3,15), "observed":platform.python_version()},
        {"id":"pydantic", "passed":pydantic_version == "2.12.5", "observed":pydantic_version},
        {"id":"linux_container_daemon", "passed":docker.get("exit_code") == 0 and docker.get("output") == "linux", "observed":docker},
        {"id":"gpu_capacity_allowance", "passed":max(gpu_memory, default=0) >= 48000,
         "observed":gpu, "target":"48000 MiB provisional preparation allowance, not measured model fit"},
        {"id":"student_vllm", "passed":importlib.util.find_spec("vllm") is not None, "observed":"module present" if importlib.util.find_spec("vllm") else "not installed"},
        {"id":"teacher_credential", "passed":not teacher_required or bool(os.environ.get("OPENAI_API_KEY")), "observed":"configured" if os.environ.get("OPENAI_API_KEY") else "not configured", "required":teacher_required},
        {"id":"pinned_model_artifacts", "passed":False, "observed":"requires exact artifact manifest and neutral real inference/processor check"},
        {"id":"deployment_isolation", "passed":False, "observed":"requires negative probes of actual launched containers"},
        {"id":"constructed_forecast_profile", "passed":False, "observed":"unscored C4 hypotheses retained; native C6 constructed-world eligibility not qualified"}
    ]
    return {"schema":"edi-benchmark-host-preflight-v1", "scope":"read_only_host_and_launch_prerequisites",
        "host_os":platform.system(), "python_executable":sys.executable, "checks":checks,
        "ready_for_live_pilot":all(c["passed"] for c in checks), "model_inference_started":False,
        "teacher_required":teacher_required, "token_values_recorded":False}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path)
    p.add_argument("--student-only", action="store_true", help="does not qualify teacher integration")
    args = p.parse_args(argv)
    report = inspect_host(teacher_required=not args.student_only)
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded)
    return 0 if report["ready_for_live_pilot"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
