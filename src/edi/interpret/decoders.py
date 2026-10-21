"""Bounded deterministic decoders. Metadata/lexical features are not semantic understanding."""
import csv
import io
import json
import struct
import wave
import zlib

from edi.interpret.config import InterpretationProfile
from edi.shared.errors import EDIError, ErrorCode

IMPLEMENTATION = "edi.native-decoders/1.0"


def select_decoder(requested, media_type):
    if requested != "auto":
        return requested
    media = media_type.split(";", 1)[0].strip().lower()
    if media == "application/json" or media.endswith("+json"):
        return "json"
    return {"text/csv": "csv", "image/png": "png-metadata",
            "audio/wav": "wav-metadata", "audio/x-wav": "wav-metadata"}.get(
                media, "text-utf8" if media.startswith("text/") else "opaque")


class _Number(str):
    pass


class _Pairs(list):
    pass


def _json_tree(text, profile, tick):
    depth, count, quoted, escaped = 0, 0, False, False
    for index, char in enumerate(text):
        if index % 4096 == 0:
            tick()
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            count += 1
        elif char in "]}":
            depth -= 1
        elif char in ",:":
            count += 1
        if depth > profile.max_depth or count > profile.max_nodes * 2:
            raise EDIError(ErrorCode.CAPACITY, "JSON depth/structure preflight limit reached")

    def bad_constant(value):
        raise ValueError(f"nonstandard JSON constant {value} is unsupported")

    value = json.loads(text, parse_int=_Number, parse_float=_Number,
                       object_pairs_hook=_Pairs, parse_constant=bad_constant)
    nodes = 0

    def node(item, depth=0):
        nonlocal nodes
        tick()
        nodes += 1
        if nodes > profile.max_nodes or depth > profile.max_depth:
            raise EDIError(ErrorCode.CAPACITY, "JSON node/depth limit reached")
        if isinstance(item, _Number):
            return {"kind": "number", "lexeme": str(item)}
        if isinstance(item, _Pairs):
            entries = []
            for key, value in item:
                key.encode("utf-8", errors="strict")
                entries.append({"key": key, "value": node(value, depth+1)})
            return {"kind": "object", "entries": entries}
        if isinstance(item, list):
            return {"kind": "array", "items": [node(v, depth+1) for v in item]}
        if item is None:
            return {"kind": "null"}
        if isinstance(item, bool):
            return {"kind": "boolean", "value": item}
        item.encode("utf-8", errors="strict")
        return {"kind": "string", "value": item}

    result = node(value)
    return result, {"json_nodes": nodes}, ("Object entry order and duplicate keys retained; numeric lexemes are distinct from strings",)


def _decode(decoder, data: bytes, delimiter: str, profile: InterpretationProfile, tick):
    """Return status, JSON output, versioned native features, and warnings."""
    tick()
    if decoder == "png-metadata":
        if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[8:16] != b"\x00\x00\x00\rIHDR":
            raise ValueError("PNG signature/first IHDR chunk is missing")
        if zlib.crc32(data[12:29]) & 0xffffffff != struct.unpack(">I", data[29:33])[0]:
            raise EDIError(ErrorCode.INTEGRITY, "PNG IHDR CRC mismatch")
        width, height, bit_depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", data[16:29])
        allowed = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8), 4: (8, 16), 6: (8, 16)}
        if not 0 < width < 2**31 or not 0 < height < 2**31 or bit_depth not in allowed.get(color, ()) or compression != 0 or filtering != 0 or interlace not in (0, 1):
            raise ValueError("unsupported/invalid PNG IHDR values")
        result = {"width": width, "height": height, "bit_depth": bit_depth,
                  "color_type": color, "interlace": interlace, "pixels_decoded": False}
        return "metadata-only", result, {"width": width, "height": height}, ("Only IHDR checked; later chunks/pixels are not validated or understood",)
    if decoder == "wav-metadata":
        with wave.open(io.BytesIO(data), "rb") as audio:
            result = {"channels": audio.getnchannels(), "sample_width_bytes": audio.getsampwidth(),
                      "sample_rate_hz": audio.getframerate(), "declared_frames": audio.getnframes(),
                      "compression": audio.getcomptype(), "samples_decoded": False}
        return "metadata-only", result, result.copy(), ("Header metadata only; declared frames are not a verified complete waveform",)
    text = data.decode("utf-8", errors="strict")
    if len(text) > profile.max_text_characters:
        raise EDIError(ErrorCode.CAPACITY, "decoded text character limit reached")
    if decoder == "text-utf8":
        return "decoded", {"text": text, "encoding": "utf-8"}, {
            "characters": len(text), "line_count": len(text.splitlines())}, ()
    if decoder == "json":
        output, features, warnings = _json_tree(text, profile, tick)
        return "decoded", output, features, warnings
    if decoder == "csv":
        rows, cells = [], 0
        for row in csv.reader(io.StringIO(text, newline=""), delimiter=delimiter, strict=True):
            tick()
            cells += len(row)
            if cells > profile.max_cells or len(rows) >= profile.max_nodes:
                raise EDIError(ErrorCode.CAPACITY, "CSV row/cell limit reached")
            rows.append(row)
        return "decoded", {"rows": rows, "header_assumed": False, "delimiter": delimiter}, {
            "rows": len(rows), "cells": cells,
            "max_columns": max((len(row) for row in rows), default=0)}, (
                "Cells remain strings; empty cells are not numeric zero; parsed cell paths are not raw byte spans",)
    raise EDIError(ErrorCode.UNSUPPORTED, "decoder is not installed")


def decode(decoder, data: bytes, delimiter: str, profile: InterpretationProfile, tick):
    try:
        return _decode(decoder, data, delimiter, profile, tick)
    except (csv.Error, wave.Error, struct.error, zlib.error) as exc:
        raise EDIError(ErrorCode.INVALID, f"native decoder rejected input: {str(exc)[:512]}") from exc
