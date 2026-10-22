"""Source/build contract checks only. No Runtime, fixture, store or model is run."""
import argparse
import ast
from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    issues, hashes = [], {}
    for path in sorted((ROOT / "src").rglob("*.py")):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        hashes[path.relative_to(ROOT).as_posix()] = sha256(path.read_bytes()).hexdigest()
    from edi.cli import _parser
    from edi.inquiry.application import ApplicationProfile
    from edi.inquiry.contracts import Operation
    from edi.inquiry.operations import contracts, call_schema
    from edi.inquiry.workflow import Workflow, OPERATORS
    from edi.reason.contracts import Episode, Response, RejectedResponse
    from edi.reason.operation_args import generation_schema, serving_schema
    from typing import get_args

    models = contracts()
    special = {"describe-operation", "observation-records"}
    if set(models) - special - set(get_args(Operation)):
        issues.append("component catalogue contains an unallocated workflow operation")
    if set(models) & OPERATORS:
        issues.append("model catalogue exposes operator steps")
    forbidden = {"reason-step", "reason-investigate", "reason-import", "world-commit", "observe-json", "observe-bytes", "register-origin"}
    if set(models) & forbidden:
        issues.append("model catalogue exposes raw intake, admission or recursive job control")
    # Inspect the actual C0 router, rather than claiming that a list of names
    # proves any runtime operation succeeded.
    router = ast.parse((ROOT / "src/edi/inquiry/workflow.py").read_text())
    literals = {node.value for node in ast.walk(router) if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    if set(models) - special - literals:
        issues.append("component catalogue lacks a matching native router branch")
    shapes = {name: model.model_json_schema() for name, model in models.items()}
    call, definitions = call_schema()
    schema = generation_schema()
    served = serving_schema()
    schema_documents = {"native_response": Response.model_json_schema(), "episode": Episode.model_json_schema(),
        "rejection": RejectedResponse.model_json_schema(), "application": ApplicationProfile.model_json_schema(),
        "generation": schema, "serving": served, "component_call": {**call, "$defs": definitions}, **shapes}
    refs = 0
    for name, document in schema_documents.items():
        def walk(value):
            nonlocal refs
            if isinstance(value, dict):
                if "$ref" in value:
                    refs += 1
                    reference = value["$ref"]
                    if not reference.startswith("#/$defs/") or reference[8:] not in document.get("$defs", {}):
                        issues.append("unresolved schema reference in " + name + ": " + reference)
                for child in value.values(): walk(child)
            elif isinstance(value, list):
                for child in value: walk(child)
        walk(document)
    commands = _parser()._subparsers._group_actions[0].choices
    expected = {"integration-config", "integration-step", "integration-teacher-import"}
    if not expected.issubset(commands): issues.append("application CLI entry point missing")
    if importlib.metadata.version("pydantic") != "2.12.5": issues.append("build contracts require pinned Pydantic 2.12.5")
    out = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    schema_path = out.with_name("generated-contracts.json")
    schema_path.write_text(json.dumps(schema_documents, indent=2) + "\n", encoding="utf-8", newline="")
    report = {"schema": "edi-component-source-checks/1.0", "scope": "source_and_generated_contracts_only",
        "consistent": not issues, "issues": issues, "python": sys.version.split()[0],
        "pydantic": importlib.metadata.version("pydantic"), "source_hashes": hashes,
        "component_operations": list(models), "operation_count": len(models),
        "schema_documents": len(schema_documents), "resolved_schema_references": refs,
        "schema_sha256": sha256(schema_path.read_bytes()).hexdigest(),
        "runtime_initialized": False, "stores_opened": 0, "product_tests_run": 0,
        "model_calls": 0, "benchmarks_run": 0, "product_qualification": "not_run"}
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="")
    print(json.dumps({key: value for key, value in report.items() if key != "source_hashes"}, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
