"""Automatic notebook checkpoint, independent of model/teacher execution."""
import base64
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import zipfile


def display_checkpoint(out, source):
    from IPython.display import HTML, display
    out, source = Path(out), Path(source)
    if not out.exists():
        print("EDI_CHECKPOINT_UNAVAILABLE: run directory absent", flush=True)
        return
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(out.rglob("*")):
            if not path.is_file() or path.name.endswith(("-wal", "-shm", ".tmp")) or path.name.startswith("checkpoint-"):
                continue
            if path.suffix == ".sqlite3":
                temporary = out / ("checkpoint-backup-" + path.name)
                with sqlite3.connect(path) as original, sqlite3.connect(temporary) as target:
                    original.backup(target)
                archive.writestr(path.relative_to(out).as_posix(), temporary.read_bytes())
                temporary.unlink()
            else:
                archive.write(path, path.relative_to(out).as_posix())
        for path in sorted(source.rglob("*.py")):
            archive.write(path, "source/" + path.relative_to(source).as_posix())
    data = memory.getvalue()
    if len(data) > 16 * 1024**2:
        raise ValueError("Checkpoint exceeds the declared 16 MiB export envelope")
    manifest = {"schema": "edi-automatic-native-checkpoint/1.0", "created_at": datetime.now(timezone.utc).isoformat(),
        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "run_directory": str(out),
        "basis": "consistent per-database backups; terminal/status artifacts separately determine controller completion and cross-owner quiescence",
        "controller_terminal_present": (out / "terminal.json").exists(),
        "forest_benchmark_started": False, "model_calls_by_export": 0}
    path = out / "checkpoint-native.zip"
    path.write_bytes(data)
    (out / "checkpoint-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
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
