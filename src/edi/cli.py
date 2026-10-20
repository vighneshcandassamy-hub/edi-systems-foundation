"""Local JSON control plane; payload bytes never pass through JSON serialization."""
import argparse
import json
from pathlib import Path
import sys

from pydantic import ValidationError

from edi.inquiry.runtime import Runtime
from edi.interpret.config import InterpretationProfile
from edi.interpret.contracts import InterpretRequest, SubmissionRequest
from edi.observe.contracts import Capture, OriginSpec, ReplayCursor
from edi.shared.config import LocalProfile
from edi.shared.errors import EDIError, ErrorCode
from edi.world.config import WorldProfile
from edi.world.contracts import WorldCursor, WorldPatch, WorldQuery


def _parser():
    parser = argparse.ArgumentParser(prog="edi", description="EDI local observation/interpretation/world runtime (unqualified)")
    parser.add_argument("--config", type=Path, help="LocalProfile JSON; must include workspace_id/database")
    parser.add_argument("--database", type=Path, help="override local database path")
    parser.add_argument("--workspace", help="override workspace scope")
    parser.add_argument("--world-config", type=Path, help="WorldProfile JSON; default is a separate sibling database")
    parser.add_argument("--interpret-config", type=Path, help="InterpretationProfile JSON; default is a separate sibling database")
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
    sub.add_parser("world-head")
    for command in ("world-propose", "world-commit"):
        p = sub.add_parser(command)
        p.add_argument("patch", type=Path)
    p = sub.add_parser("world-get")
    p.add_argument("record_id")
    p.add_argument("--revision", type=int)
    p = sub.add_parser("world-query")
    p.add_argument("--query", type=Path)
    p.add_argument("--cursor", type=Path)
    p.add_argument("--revision", type=int)
    p.add_argument("--limit", type=int, default=100)
    p = sub.add_parser("world-dependencies")
    p.add_argument("record_id")
    p.add_argument("--revision", type=int)
    p.add_argument("--direction", choices=("dependencies", "dependents"), default="dependencies")
    p.add_argument("--depth", type=int, default=1)
    p = sub.add_parser("world-status")
    p.add_argument("request_id")
    for command in ("world-progress", "world-ack"):
        p = sub.add_parser(command)
        p.add_argument("consumer")
    p = sub.add_parser("interpret")
    p.add_argument("request", type=Path)
    p = sub.add_parser("derivation")
    p.add_argument("derivation_id")
    for command in ("interpret-build-patch", "interpret-submit"):
        p = sub.add_parser(command)
        p.add_argument("request", type=Path)
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
        world_profile = WorldProfile.model_validate_json(args.world_config.read_bytes()) if args.world_config else None
        interpretation_profile = InterpretationProfile.model_validate_json(args.interpret_config.read_bytes()) if args.interpret_config else None
        runtime = Runtime(LocalProfile.model_validate(overrides), world_profile, interpretation_profile)
        obs = runtime.observation
        world = runtime.world if args.command.startswith("world-") else None
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
        elif args.command == "world-head":
            _emit({"revision": world.head(), "workspace_id": runtime.profile.workspace_id})
        elif args.command in ("world-propose", "world-commit"):
            patch = WorldPatch.model_validate_json(args.patch.read_bytes())
            _emit(world.propose_patch(patch) if args.command == "world-propose" else world.commit(patch))
        elif args.command == "world-get":
            _emit(world.get(args.record_id, revision=args.revision))
        elif args.command == "world-query":
            query = WorldQuery.model_validate_json(args.query.read_bytes()) if args.query else None
            cursor = WorldCursor.model_validate_json(args.cursor.read_bytes()) if args.cursor else None
            _emit(world.query(query, revision=args.revision, cursor=cursor, limit=args.limit))
        elif args.command == "world-dependencies":
            _emit(world.dependencies(args.record_id, revision=args.revision,
                                     direction=args.direction, max_depth=args.depth))
        elif args.command == "world-status":
            result = world.commit_status(args.request_id)
            _emit(result if result is not None else {"status": "not-found", "request_id": args.request_id})
        elif args.command == "world-progress":
            _emit({"consumer": args.consumer, "position": world.consumer_position(args.consumer)})
        elif args.command == "world-ack":
            _emit({"consumer": args.consumer, "position": runtime.acknowledge_world_progress(args.consumer)})
        elif args.command == "interpret":
            _emit(runtime.interpretation.interpret(InterpretRequest.model_validate_json(args.request.read_bytes())))
        elif args.command == "derivation":
            _emit(runtime.interpretation.get_derivation(args.derivation_id))
        elif args.command in ("interpret-build-patch", "interpret-submit"):
            request = SubmissionRequest.model_validate_json(args.request.read_bytes())
            result = (runtime.interpretation.build_patch(request) if args.command == "interpret-build-patch"
                      else runtime.interpretation.submit(request))
            _emit(result)
        return 0
    except EDIError as exc:
        print(json.dumps(exc.as_dict()), file=sys.stderr)
    except (ValidationError, ValueError, OSError) as exc:
        print(json.dumps(EDIError(ErrorCode.INVALID, str(exc)).as_dict()), file=sys.stderr)
    return 2
