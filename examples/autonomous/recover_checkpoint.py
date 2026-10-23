"""Recover an automatic EDI checkpoint from a downloaded notebook; never execute it."""
import argparse
import base64
import hashlib
import html
import io
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="Private output directory outside Git for raw state")
    parser.add_argument("--checkpoint-sha256", help="Recover only this exact retained snapshot when a notebook has several checkpoints for one run")
    args = parser.parse_args()
    notebook_bytes = args.notebook.read_bytes()
    notebook = json.loads(notebook_bytes)
    checkpoints = {}
    for cell in notebook["cells"]:
        for output in cell.get("outputs", []):
            value = output.get("data", {}).get("text/html", [])
            value = "".join(value) if isinstance(value, list) else value
            if not value:
                continue
            marker = "EDI_NATIVE_CHECKPOINT_MANIFEST_V1 "
            if marker not in value:
                continue
            manifest = json.loads(html.unescape(value.split(marker, 1)[1].split("</pre>", 1)[0]))
            for match in re.finditer(r"data:application/zip;base64,([A-Za-z0-9+/=]+)", value):
                raw = base64.b64decode(match.group(1), validate=True)
                digest = hashlib.sha256(raw).hexdigest()
                if len(raw) > 16 * 1024**2 or len(raw) != manifest["bytes"] or digest != manifest["sha256"]:
                    raise ValueError("Checkpoint size/digest differs from its recorded manifest")
                checkpoints[digest] = (raw, manifest)
    if not checkpoints:
        raise ValueError("No automatic EDI checkpoint in the selected notebook")
    if args.checkpoint_sha256:
        if args.checkpoint_sha256 not in checkpoints:
            raise ValueError("Selected checkpoint digest is absent from notebook")
        checkpoints = {args.checkpoint_sha256: checkpoints[args.checkpoint_sha256]}
    for digest, (raw, manifest) in checkpoints.items():
        directory = PurePosixPath(manifest["run_directory"]).name
        if not 1 <= len(directory) <= 96 or not all(c.isalnum() or c == "-" for c in directory):
            raise ValueError("Unrecognized bounded run directory")
        root = args.output / directory
        root.mkdir(parents=True, exist_ok=True)
        archive = root / "edi-native-state.zip"
        if archive.exists() and archive.read_bytes() != raw:
            raise ValueError("Different raw checkpoint already exists under this run identity")
        with zipfile.ZipFile(io.BytesIO(raw)) as bundle:
            members = bundle.infolist()
            if len(members) > 1000 or sum(item.file_size for item in members) > 256 * 1024**2:
                raise ValueError("Expanded checkpoint exceeds the recovery envelope")
            for item in members:
                name = item.filename
                if PureWindowsPath(name).drive or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts or "\\" in name or stat.S_ISLNK(item.external_attr >> 16):
                    raise ValueError("Unsafe checkpoint member")
            if bundle.testzip() is not None:
                raise ValueError("Checkpoint ZIP CRC failure")
            archive.write_bytes(raw)
            bundle.extractall(root / "extracted")
        report = {"archive": str(archive.resolve()), "bytes": len(raw), "sha256": digest,
            "zip_crc": "passed", "notebook_sha256": hashlib.sha256(notebook_bytes).hexdigest(),
            "manifest": manifest, "scope": "transport verified; native source/state checks remain separate"}
        (root / "DOWNLOAD_VERIFIED.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
