"""Deterministic, bounded C1 prefix scan; the caller cannot choose favorable outcomes."""
from hashlib import sha256

from edi.assess.scoring import parse_measurement
from edi.observe.contracts import ReplayCursor
from edi.shared.contracts import EvidenceRef
from edi.shared.errors import EDIError, ErrorCode


class ScanStopped(Exception):
    pass


def reference(source):
    return EvidenceRef(workspace_id=source.scope_id, record_id=source.record_id,
        sha256=source.manifest.sha256, origin_class=source.capture.origin_class, lineage=source.capture.lineage)


def select_outcomes(reader, seal, watermark, profile, tick):
    selected, blocked, coverage = {}, {}, []
    records, byte_count = 0, 0
    for origin in seal.outcome_origins:
        points = [p for p in seal.points if p.case.origin_ref == origin.origin_ref]
        cursor = ReplayCursor(workspace_id=seal.request.workspace_id, after=0, watermark=watermark, origin_ref=origin.origin_ref)
        scanned, exhausted, stop_reason, last_position = 0, False, None, 0
        try:
            while True:
                tick()
                if records >= profile.max_scan_records: raise ScanStopped("global outcome scan-record budget exhausted")
                page = reader.replay(cursor=cursor, origin_ref=origin.origin_ref, limit=min(profile.page_size, profile.max_scan_records - records))
                if (page.cursor.workspace_id != seal.request.workspace_id or page.cursor.watermark != watermark
                        or page.cursor.origin_ref != origin.origin_ref):
                    raise EDIError(ErrorCode.INTEGRITY, "C1 replay cut/scope differs from C6 selection")
                previous_position = cursor.after
                for source in page.items:
                    tick()
                    records += 1; scanned += 1
                    if (source.scope_id != seal.request.workspace_id or source.origin_ref != origin.origin_ref
                            or source.source_id != origin.source_id or not previous_position < source.commit_position <= watermark):
                        raise EDIError(ErrorCode.INTEGRITY, "C1 replay identity/source/order differs from sealed selection")
                    previous_position = source.commit_position
                    last_position = source.commit_position
                    if source.kind != "measurement-v1": continue
                    pending = [p for p in points if p.case.case_id not in selected]
                    if not pending: break
                    event = source.capture.time.event_time
                    if event.status != "known" or source.capture.time.clock_id != "UTC":
                        for p in pending: blocked.setdefault(p.case.case_id, (source, "earlier measurement has unknown/incompatible event clock; matching cannot be certified"))
                        continue
                    candidates = [p for p in pending if event.value == p.target_time]
                    if not candidates: continue
                    size = source.manifest.byte_count
                    if size > profile.max_payload_bytes or byte_count + size > profile.max_total_read_bytes:
                        raise ScanStopped("outcome payload admission/read budget exhausted")
                    if source.capture.critical_profiles or source.manifest.media_type.split(";", 1)[0] != "application/json":
                        for p in candidates: blocked.setdefault(p.case.case_id, (source, "earlier matching-time record has unsupported critical profiles/media semantics"))
                        continue
                    try:
                        data = reader.read_payload(source.record_id, offset=0, length=size)
                        byte_count += len(data)
                        if len(data) != size or sha256(data).hexdigest() != source.manifest.sha256:
                            raise ValueError("C1 selected payload size/digest differs")
                        measurement = parse_measurement(data)
                    except (ValueError, UnicodeError, RecursionError) as exc:
                        for p in candidates: blocked.setdefault(p.case.case_id, (source, "earlier matching-time measurement cannot be decoded: " + str(exc)[:512]))
                        continue
                    for p in candidates:
                        if measurement.variable == p.case.variable:
                            selected[p.case.case_id] = (source, measurement)
                if page.cursor.after < previous_position or page.cursor.after < cursor.after or page.cursor.after > watermark:
                    raise EDIError(ErrorCode.INTEGRITY, "C1 replay cursor escaped the processed cut")
                cursor = page.cursor
                if not page.has_more:
                    exhausted = True
                    break
                if all(p.case.case_id in selected for p in points):
                    stop_reason = "first occurrences resolved within scanned prefix"
                    break
                if not page.items: raise ScanStopped("C1 returned a non-progressing partial page")
        except ScanStopped as exc:
            stop_reason = str(exc)
        except EDIError as exc:
            if exc.code not in (ErrorCode.NOT_FOUND, ErrorCode.UNAVAILABLE, ErrorCode.STORAGE, ErrorCode.CAPACITY): raise
            stop_reason = "source retrieval unavailable; not evidence of absence: " + str(exc)[:512]
        coverage.append({"origin_ref": origin.origin_ref, "source_id": origin.source_id,
            "watermark": watermark, "scanned_records": scanned, "after": last_position,
            "exhausted": exhausted, "stop_reason": stop_reason})
    return selected, blocked, tuple(coverage), {"scanned_records": records, "payload_bytes_read": byte_count}
