"""Local JSON control plane; payload bytes never pass through JSON serialization."""
import argparse
import json
from pathlib import Path
import sys

from pydantic import ValidationError

from edi.inquiry.runtime import Runtime
from edi.observe.contracts import Capture, OriginSpec, ReplayCursor
from edi.shared.config import LocalProfile
from edi.shared.errors import EDIError, ErrorCode


def _parser():
    parser = argparse.ArgumentParser(prog="edi", description="EDI local observation runtime (unqualified)")
    parser.add_argument("--config", type=Path, help="LocalProfile JSON; must include workspace_id/database")
    parser.add_argument("--database", type=Path, help="override local database path")
    parser.add_argument("--workspace", help="override workspace scope")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("capabilities")
    p = sub.add_parser("register-origin")
    p.add_argument("spec", type=Path)
    p = sub.add_parser("ingest")
    p.add_argument("capture", type=Path)
    p.add_argument("payload", type=Path)
    p = sub.add_parser("get")
    p.add_argument("record_id")
    p = sub.add_parser("origin")
    p.add_argument("origin_ref")
    p = sub.add_parser("status")
    p.add_argument("origin_ref")
    p.add_argument("idempotency_key")
    p = sub.add_parser("replay")
    p.add_argument("--cursor", type=Path, help="previous page's cursor object, saved as JSON")
    p.add_argument("--origin")
    p.add_argument("--limit", type=int, default=100)
    p = sub.add_parser("read")
    p.add_argument("record_id")
    p.add_argument("output", type=Path)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--length", type=int, default=65536)
    p = sub.add_parser("checkpoint")
    p.add_argument("consumer")
    p.add_argument("--position", type=int, help="omit to read current checkpoint")
    sub.add_parser("coverage")
    p = sub.add_parser("backup")
    p.add_argument("destination", type=Path)
    return parser


def _emit(value):
    if isinstance(value, tuple):
        value = [item.model_dump(mode="json") for item in value]
    elif hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    print(json.dumps(value, ensure_ascii=False, allow_nan=False))


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        profile = LocalProfile.model_validate_json(args.config.read_bytes()) if args.config else LocalProfile()
        overrides = profile.model_dump()
        if args.database is not None:
            overrides["database"] = args.database
        if args.workspace is not None:
            overrides["workspace_id"] = args.workspace
        runtime = Runtime(LocalProfile.model_validate(overrides))
        obs = runtime.observation
        if args.command == "capabilities":
            _emit(runtime.capabilities())
        elif args.command == "register-origin":
            _emit(runtime.register_origin(OriginSpec.model_validate_json(args.spec.read_bytes())))
        elif args.command == "ingest":
            _emit(runtime.observe_file(Capture.model_validate_json(args.capture.read_bytes()), args.payload))
        elif args.command == "get":
            _emit(obs.get_record(args.record_id))
        elif args.command == "origin":
            _emit(obs.get_origin(args.origin_ref))
        elif args.command == "status":
            _emit(obs.commit_status(args.origin_ref, args.idempotency_key))
        elif args.command == "replay":
            cursor = ReplayCursor.model_validate_json(args.cursor.read_bytes()) if args.cursor else None
            _emit(obs.replay(cursor=cursor, origin_ref=args.origin, limit=args.limit))
        elif args.command == "read":
            data = obs.read_payload(args.record_id, offset=args.offset, length=args.length)
            with args.output.open("xb") as target:
                target.write(data)
            _emit({"status": "written", "bytes": len(data), "output": str(args.output)})
        elif args.command == "checkpoint":
            position = (obs.get_checkpoint(args.consumer) if args.position is None
                        else obs.checkpoint(args.consumer, args.position))
            _emit({"consumer": args.consumer, "position": position})
        elif args.command == "coverage":
            _emit(obs.coverage())
        elif args.command == "backup":
            obs.backup(args.destination)
            _emit({"status": "copied", "destination": str(args.destination), "qualification": "not-run"})
        return 0
    except EDIError as exc:
        print(json.dumps(exc.as_dict()), file=sys.stderr)
    except (ValidationError, ValueError, OSError) as exc:
        print(json.dumps(EDIError(ErrorCode.INVALID, str(exc)).as_dict()), file=sys.stderr)
    return 2
