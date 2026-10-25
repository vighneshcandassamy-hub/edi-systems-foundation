"""Automatic notebook checkpoint, independent of model/teacher execution."""
import base64
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import zipfile


def display_checkpoint(out, source, *, emit_payload=True):
    from IPython.display import HTML, display
    out, source = Path(out), Path(source)
    if not out.exists():
        print("EDI_CHECKPOINT_UNAVAILABLE: run directory absent", flush=True)
        return
    memory = io.BytesIO()
    immutable_source_omissions=[]
    with zipfile.ZipFile(memory, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(out.rglob("*")):
            if not path.is_file() or path.name.endswith(("-wal", "-shm", ".tmp")) or path.name.startswith("checkpoint-"):
                continue
            if path.suffix in (".sqlite3", ".sqlite"):
                temporary = out / ("checkpoint-backup-" + path.name)
                with sqlite3.connect(path) as original, sqlite3.connect(temporary) as target:
                    original.backup(target)
                archive.writestr(path.relative_to(out).as_posix(), temporary.read_bytes())
                temporary.unlink()
            else:
                archive.write(path, path.relative_to(out).as_posix())
        source_manifest=source/"source-manifest.json"
        if source_manifest.exists():
            pinned=json.loads(source_manifest.read_bytes())
            for name,expected in sorted(pinned["files"].items()):
                relative=Path(name)
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError("Invalid pinned source path")
                path=source/relative
                if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise ValueError("Source changed during run: "+name)
                public_startup={"meadows/environment/v0_2/PUBLIC_OPERATIONS.json",
                    "meadows/environment/v0_2/PARTICIPANT.md",
                    "meadows/environment/v0_2/fixture/mission.json"}
                if path.suffix==".py" or name in public_startup:
                    archive.write(path,"source/"+name)
                else:
                    immutable_source_omissions.append(name)
            archive.write(source_manifest,"source/source-manifest.json")
        else:
            for path in sorted(source.rglob("*.py")):
                archive.write(path, "source/" + path.relative_to(source).as_posix())
    data = memory.getvalue()
    if len(data) > 16 * 1024**2:
        raise ValueError("Checkpoint exceeds the declared 16 MiB export envelope")
    manifest = {"schema": "edi-automatic-native-checkpoint/1.0", "created_at": datetime.now(timezone.utc).isoformat(),
        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "run_directory": str(out),
        "basis": "consistent per-database backups; terminal/status artifacts separately determine controller completion and cross-owner quiescence",
        "controller_terminal_present": (out / "terminal.json").exists(),
        "forest_benchmark_started": (out/"world-selection.json").exists() and json.loads((out/"world-selection.json").read_bytes()).get("kind")=="cedar", "model_calls_by_export": 0,
        "source_basis":"Native Python and public startup text retained; immutable world assets remain in the original launch bundle with full source-manifest hashes. Full service recovery requires that pinned input bundle.",
        "immutable_source_omissions":immutable_source_omissions}
    path = out / "checkpoint-native.zip"
    path.write_bytes(data)
    (out / "checkpoint-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if not emit_payload:
        print("EDI_CHECKPOINT_SAVED", json.dumps({k:manifest[k] for k in ("bytes","sha256","run_directory")}), flush=True)
        return manifest
    encoded = base64.b64encode(data).decode()
    display(HTML('<a download="edi-native-checkpoint.zip" href="data:application/zip;base64,' + encoded
        + '">Download native checkpoint ZIP</a><pre>EDI_NATIVE_CHECKPOINT_MANIFEST_V1 '
        + json.dumps(manifest, sort_keys=True) + '</pre>'))
    # The downloadable notebook retains the HTML payload even if its VM expires.
    print("EDI_NATIVE_CHECKPOINT_MANIFEST_V1", json.dumps(manifest, sort_keys=True), flush=True)
    for name in ("latest-state.json", "restart-mismatch.json", "restart-integrity.json"):
        path = out / name
        if path.exists():
            print("EDI_NATIVE_DIAGNOSTIC", name, path.read_text(encoding="utf-8")[:12000], flush=True)
    terminal = out / "terminal.json"
    if terminal.exists():
        result = json.loads(terminal.read_bytes())
        for episode in result["snapshot"]["episodes"]:
            print("EDI_NATIVE_REJECTIONS", json.dumps(episode["rejections"]), flush=True)
