"""C3-owned append-only versions and a rebuildable current-reference index.

This module never opens the C1 database. Evidence correspondence uses its read port.
"""
from contextlib import contextmanager
from hashlib import sha256
import json
import shutil
import sqlite3
from time import monotonic

from pydantic import BaseModel

from edi.observe.ports import EvidenceReader
from edi.shared.contracts import utc_now
from edi.shared.errors import EDIError, ErrorCode
from edi.world.config import WorldProfile
from edi.world.contracts import (
    Admission, Decide, DependencyItem, DependencyView, Put, Ref, Representation, Retire,
    StoredRepresentation, WorldCommit, WorldCursor, WorldPage, WorldPatch, WorldQuery, iter_refs,
)

_SCHEMA = """
CREATE TABLE world_info (
    singleton INTEGER PRIMARY KEY CHECK(singleton=1), workspace_id TEXT NOT NULL,
    head INTEGER NOT NULL DEFAULT 0, versions INTEGER NOT NULL DEFAULT 0,
    stored_bytes INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE world_commits (
    revision INTEGER PRIMARY KEY, request_id TEXT NOT NULL UNIQUE,
    fingerprint TEXT NOT NULL, patch_json TEXT NOT NULL, commit_json TEXT NOT NULL
);
CREATE TABLE world_versions (
    record_id TEXT NOT NULL, version INTEGER NOT NULL REFERENCES world_commits(revision),
    family TEXT NOT NULL, scope_id TEXT NOT NULL, state TEXT NOT NULL,
    valid_status TEXT NOT NULL, valid_start TEXT, valid_end TEXT,
    document_json TEXT NOT NULL, PRIMARY KEY(record_id,version)
);
CREATE TABLE world_heads (
    record_id TEXT PRIMARY KEY, version INTEGER NOT NULL,
    FOREIGN KEY(record_id,version) REFERENCES world_versions(record_id,version)
);
CREATE TABLE world_dependencies (
    owner_id TEXT NOT NULL, owner_version INTEGER NOT NULL,
    target_id TEXT NOT NULL, target_version INTEGER NOT NULL,
    PRIMARY KEY(owner_id,owner_version,target_id,target_version),
    FOREIGN KEY(owner_id,owner_version) REFERENCES world_versions(record_id,version),
    FOREIGN KEY(target_id,target_version) REFERENCES world_versions(record_id,version)
        DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX world_reverse_dependencies ON world_dependencies(target_id,owner_id,owner_version);
CREATE TABLE world_consumers (consumer_id TEXT PRIMARY KEY, position INTEGER NOT NULL);
PRAGMA user_version=1;
"""


def _json(record) -> str:
    return json.dumps(record.model_dump(mode="json"), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _pins(value, resolver):
    """Copy typed records while resolving Ref(None); do not interpret opaque dict values."""
    if isinstance(value, Ref):
        return Ref(record_id=value.record_id, version=resolver(value))
    if isinstance(value, BaseModel):
        return value.model_copy(update={name: _pins(getattr(value, name), resolver)
                                        for name in type(value).model_fields})
    if isinstance(value, tuple):
        return tuple(_pins(item, resolver) for item in value)
    return value


def _utc(value):
    from datetime import timezone
    return value.astimezone(timezone.utc).isoformat() if value is not None else None


class SQLiteWorldStore:
    def __init__(self, profile: WorldProfile, evidence: EvidenceReader):
        self.profile = profile
        self.evidence = evidence
        self.path = profile.database.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as con:
            con.execute("PRAGMA journal_mode=WAL")
            con.execute("BEGIN IMMEDIATE")
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version == 0:
                if con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                    raise EDIError(ErrorCode.UNSUPPORTED, "unrecognized world database")
                for statement in _SCHEMA.split(";"):
                    if statement.strip():
                        con.execute(statement)
                con.execute("INSERT INTO world_info(singleton,workspace_id) VALUES(1,?)",
                            (profile.workspace_id,))
            elif version != 1:
                raise EDIError(ErrorCode.UNSUPPORTED, "unsupported world database version")
            row = con.execute("SELECT workspace_id FROM world_info WHERE singleton=1").fetchone()
            if row is None or row[0] != profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "world database workspace mismatch")
            self._commit_sql(con)

    @contextmanager
    def _connection(self):
        con = None
        try:
            con = sqlite3.connect(self.path, timeout=self.profile.writer_timeout_seconds,
                                  isolation_level=None)
            con.execute("PRAGMA foreign_keys=ON")
            con.execute("PRAGMA synchronous=FULL")
            con.execute("PRAGMA cache_size=-8192")
            started, steps = monotonic(), 0

            def progress():
                nonlocal steps
                steps += 1000
                return int(steps > self.profile.max_sql_steps or
                           monotonic() - started > self.profile.max_sql_seconds)

            con.set_progress_handler(progress, 1000)
            yield con
        except sqlite3.Error as exc:
            if getattr(exc, "sqlite_errorcode", None) == sqlite3.SQLITE_INTERRUPT:
                raise EDIError(ErrorCode.CAPACITY, "world SQL work/time budget exceeded",
                               retryable=True) from exc
            raise EDIError(ErrorCode.STORAGE, f"world storage operation failed: {exc}",
                           retryable=True) from exc
        finally:
            if con is not None:
                con.set_progress_handler(None, 0)
                try:
                    if con.in_transaction:
                        con.rollback()
                finally:
                    con.close()

    @staticmethod
    def _commit_sql(con):
        try:
            con.execute("COMMIT")
        except sqlite3.Error as exc:
            raise EDIError(ErrorCode.UNKNOWN_COMMIT,
                           "world commit acknowledgement failed; resolve by request_id",
                           retryable=True) from exc

    def _encoded(self, value, limit):
        encoded = _json(value)
        if len(encoded.encode("utf-8")) > limit:
            raise EDIError(ErrorCode.CAPACITY, "world serialized record/patch limit exceeded")
        return encoded

    @staticmethod
    def _head(con):
        return con.execute("SELECT head FROM world_info WHERE singleton=1").fetchone()[0]

    def head(self) -> int:
        with self._connection() as con:
            return self._head(con)

    def _revision(self, con, revision):
        high = self._head(con)
        if revision is None:
            return high
        if type(revision) is not int or not 0 <= revision <= high:
            raise EDIError(ErrorCode.INVALID, "requested world revision is unavailable")
        return revision

    @staticmethod
    def _at(con, record_id, revision):
        row = con.execute(
            "SELECT document_json FROM world_versions WHERE record_id=? AND version<=? "
            "ORDER BY version DESC LIMIT 1", (record_id, revision),
        ).fetchone()
        return StoredRepresentation.model_validate_json(row[0]) if row else None

    def get(self, record_id: str, *, revision: int | None = None) -> StoredRepresentation:
        with self._connection() as con:
            con.execute("BEGIN")
            item = self._at(con, record_id, self._revision(con, revision))
            if item is None:
                raise EDIError(ErrorCode.NOT_FOUND, "representation unavailable at requested revision")
            return item

    def commit_status(self, request_id: str) -> WorldCommit | None:
        with self._connection() as con:
            row = con.execute("SELECT commit_json FROM world_commits WHERE request_id=?",
                              (request_id,)).fetchone()
            return WorldCommit.model_validate_json(row[0]) if row else None

    def consumer_position(self, consumer_id: str) -> int:
        if not consumer_id or len(consumer_id) > 256:
            raise EDIError(ErrorCode.INVALID, "invalid world consumer identifier")
        with self._connection() as con:
            row = con.execute("SELECT position FROM world_consumers WHERE consumer_id=?",
                              (consumer_id,)).fetchone()
            return row[0] if row else 0

    def _evidence(self, representations, patch):
        refs = [ref for rep in representations for ref in (*rep.support, *rep.counterevidence)]
        consumed_ids = patch.consumed.record_ids if patch.consumed is not None else ()
        if len(refs) + len(consumed_ids) > self.profile.max_evidence_per_patch:
            raise EDIError(ErrorCode.CAPACITY, "world evidence validation budget exceeded")
        records = {}
        for ref in refs:
            if ref.workspace_id != self.profile.workspace_id:
                raise EDIError(ErrorCode.DENIED, "cross-workspace evidence reference")
            source = records.get(ref.record_id)
            if source is None:
                source = self.evidence.get_record(ref.record_id)
                if source.scope_id != self.profile.workspace_id:
                    raise EDIError(ErrorCode.DENIED, "C1 evidence response workspace mismatch")
                if source.record_id != ref.record_id:
                    raise EDIError(ErrorCode.INTEGRITY, "C1 evidence response occurrence mismatch")
                records[ref.record_id] = source
            if source.manifest.sha256 != ref.sha256:
                raise EDIError(ErrorCode.INTEGRITY, "evidence hash differs from C1 manifest")
            if ref.origin_class != source.capture.origin_class or ref.lineage != source.capture.lineage:
                raise EDIError(ErrorCode.INTEGRITY, "evidence provenance differs from C1 declaration")
            if ref.selector != "whole-object":
                parts = ref.selector.split(":")
                if len(parts) != 3 or parts[0] != "bytes" or not parts[1].isdigit() or not parts[2].isdigit():
                    raise EDIError(ErrorCode.UNSUPPORTED, "only whole-object/bytes:start:end selectors supported")
                start, end = int(parts[1]), int(parts[2])
                if not 0 <= start <= end <= source.manifest.byte_count:
                    raise EDIError(ErrorCode.INVALID, "evidence selector outside acquired bytes")
        if patch.consumed is not None:
            consumed = patch.consumed
            if consumed.position < consumed.expected_position:
                raise EDIError(ErrorCode.CONFLICT, "world evidence progress cannot decrease")
            if not set(consumed_ids).issubset(records):
                raise EDIError(ErrorCode.INVALID, "consumed occurrences must be linked in this patch's evidence")
            if consumed.position > consumed.expected_position:
                if not consumed_ids or max(records[i].commit_position for i in consumed_ids) != consumed.position:
                    raise EDIError(ErrorCode.INVALID, "new progress must end at a linked committed C1 occurrence")
            if any(records[i].commit_position > consumed.position for i in consumed_ids):
                raise EDIError(ErrorCode.INVALID, "consumed occurrence exceeds proposed progress")

    def commit(self, patch: WorldPatch, *, allow_decisions: bool = False) -> WorldCommit:
        if patch.workspace_id != self.profile.workspace_id:
            raise EDIError(ErrorCode.DENIED, "patch workspace mismatch")
        if patch.proposer not in ("C0", "C2", "C4", "C6", "C7"):
            raise EDIError(ErrorCode.DENIED, "owner has no C3 proposal lane")
        if len(patch.operations) > self.profile.max_operations:
            raise EDIError(ErrorCode.CAPACITY, "too many world operations")
        if not allow_decisions and any(not isinstance(op, Put) or op.admission is not None
                                       for op in patch.operations):
            raise EDIError(ErrorCode.DENIED, "proposal ports accept candidate puts only")
        encoded_patch = self._encoded(patch, self.profile.max_patch_bytes)
        # Frozen Pydantic records still contain mutable JSON containers: use one admitted snapshot.
        patch = WorldPatch.model_validate_json(encoded_patch)
        # Authority channel is part of identity: a candidate retry cannot become an admin decision.
        fingerprint = sha256((str(allow_decisions) + "\n" + encoded_patch).encode("utf-8")).hexdigest()
        started = monotonic()
        with self._connection() as con:
            con.execute("BEGIN IMMEDIATE")
            previous = con.execute("SELECT fingerprint,commit_json FROM world_commits WHERE request_id=?",
                                   (patch.request_id,)).fetchone()
            if previous:
                if previous[0] != fingerprint:
                    raise EDIError(ErrorCode.CONFLICT, "world retry request differs from committed request")
                return WorldCommit.model_validate_json(previous[1]).model_copy(update={"duplicate": True})
            head, versions, stored_bytes = con.execute(
                "SELECT head,versions,stored_bytes FROM world_info WHERE singleton=1"
            ).fetchone()
            if patch.base_revision != head:
                raise EDIError(ErrorCode.CONFLICT, "stale world base revision; re-read and explicitly re-propose")
            if versions + len(patch.operations) > self.profile.max_versions:
                raise EDIError(ErrorCode.CAPACITY, "world version count quota reached")
            if shutil.disk_usage(self.path.parent).free < self.profile.min_free_disk_bytes:
                raise EDIError(ErrorCode.CAPACITY, "world free disk reserve reached", retryable=True)
            revision, stamp = head + 1, utc_now()
            plans = {}
            for op in patch.operations:
                record_id = op.representation.record_id if isinstance(op, Put) else op.record_id
                if record_id in plans:
                    raise EDIError(ErrorCode.INVALID, "one operation per representation per patch")
                old = self._at(con, record_id, head)
                if op.expected_version != (old.version if old else 0):
                    raise EDIError(ErrorCode.CONFLICT, "representation expected version mismatch")
                if isinstance(op, Put):
                    rep = op.representation
                    if old is not None and old.representation.structure.family != rep.structure.family:
                        raise EDIError(ErrorCode.INVALID, "representation family is immutable; create a new identity")
                    decision = op.admission or Admission(rationale="retained candidate; no automatic promotion")
                    state = decision.decision
                else:
                    if old is None:
                        raise EDIError(ErrorCode.NOT_FOUND, "decision/retirement target unavailable")
                    rep = old.representation
                    decision = op.admission if isinstance(op, Decide) else Admission(
                        decision="withdrawn", rationale=op.reason)
                    state = decision.decision if isinstance(op, Decide) else "retired"
                if decision.decision == "accepted_for_use" and not (rep.support or rep.assumptions):
                    raise EDIError(ErrorCode.INVALID, "modeling-use admission needs evidence or explicit assumptions")
                refs = list(iter_refs(rep))
                if len(refs) > self.profile.max_refs_per_record:
                    raise EDIError(ErrorCode.CAPACITY, "representation reference budget exceeded")
                plans[record_id] = (rep, decision, state, refs)
            evidence_representations = []
            for op in patch.operations:
                record_id = op.representation.record_id if isinstance(op, Put) else op.record_id
                if isinstance(op, Put) or (isinstance(op, Decide) and op.admission.decision == "accepted_for_use"):
                    evidence_representations.append(plans[record_id][0])
            # Withdrawal/retirement must remain possible when old evidence becomes unavailable.
            self._evidence(evidence_representations, patch)
            if patch.consumed is not None:
                progress = con.execute("SELECT position FROM world_consumers WHERE consumer_id=?",
                                       (patch.consumed.consumer_id,)).fetchone()
                if (progress[0] if progress else 0) != patch.consumed.expected_position:
                    raise EDIError(ErrorCode.CONFLICT, "world consumer progress expected position mismatch")
                if progress is None and con.execute("SELECT COUNT(*) FROM world_consumers").fetchone()[0] >= self.profile.max_consumers:
                    raise EDIError(ErrorCode.CAPACITY, "world consumer count quota reached")

            def resolve(ref):
                if ref.version is None and ref.record_id in plans:
                    return revision
                target = self._at(con, ref.record_id, head)
                if ref.version is None:
                    if target is None:
                        raise EDIError(ErrorCode.NOT_FOUND, "unresolved representation reference")
                    return target.version
                if ref.version == revision and ref.record_id in plans:
                    return revision
                row = con.execute("SELECT 1 FROM world_versions WHERE record_id=? AND version=?",
                                  (ref.record_id, ref.version)).fetchone()
                if row is None or ref.version > head:
                    raise EDIError(ErrorCode.NOT_FOUND, "pinned representation version unavailable")
                return ref.version

            result = WorldCommit(workspace_id=self.profile.workspace_id, request_id=patch.request_id,
                                 revision=revision, previous_revision=head, committed_at=stamp,
                                 changed_ids=tuple(plans), consumed=patch.consumed,
                                 decision_authority="C3-local-operator" if allow_decisions else "C3-candidate-policy")
            result_json = _json(result)
            con.execute("INSERT INTO world_commits VALUES(?,?,?,?,?)",
                        (revision, patch.request_id, fingerprint, encoded_patch, result_json))
            added_bytes = len(encoded_patch.encode("utf-8")) + len(result_json.encode("utf-8"))
            for record_id, (rep, decision, state, refs) in plans.items():
                if monotonic() - started > self.profile.max_commit_seconds:
                    raise EDIError(ErrorCode.CAPACITY, "world cooperative commit deadline exceeded")
                pinned = _pins(rep, resolve)
                item = StoredRepresentation(workspace_id=self.profile.workspace_id, version=revision,
                                            known_at=stamp, proposer=patch.proposer,
                                            change_kind=patch.change_kind, representation=pinned,
                                            state=state, admission=decision,
                                            decision_authority=result.decision_authority)
                document = self._encoded(item, self.profile.max_record_bytes)
                added_bytes += len(document.encode("utf-8"))
                if stored_bytes + added_bytes > self.profile.max_stored_bytes:
                    raise EDIError(ErrorCode.CAPACITY, "world serialized storage quota reached")
                valid = rep.validity
                con.execute("INSERT INTO world_versions VALUES(?,?,?,?,?,?,?,?,?)",
                            (record_id, revision, rep.structure.family, rep.scope_id, state,
                             valid.status, _utc(valid.start), _utc(valid.end), document))
                con.execute("INSERT INTO world_heads VALUES(?,?) ON CONFLICT(record_id) DO UPDATE SET version=excluded.version",
                            (record_id, revision))
                edges = {(ref.record_id, ref.version) for ref in iter_refs(pinned)}
                for target_id, target_version in edges:
                    con.execute("INSERT INTO world_dependencies VALUES(?,?,?,?)",
                                (record_id, revision, target_id, target_version))
            if patch.consumed is not None:
                con.execute("INSERT INTO world_consumers VALUES(?,?) ON CONFLICT(consumer_id) DO UPDATE SET position=excluded.position",
                            (patch.consumed.consumer_id, patch.consumed.position))
            con.execute("UPDATE world_info SET head=?,versions=versions+?,stored_bytes=stored_bytes+? WHERE singleton=1",
                        (revision, len(plans), added_bytes))
            self._commit_sql(con)
            return result

    def query(self, query: WorldQuery | None = None, *, revision: int | None = None,
              cursor: WorldCursor | None = None, limit: int = 100) -> WorldPage:
        if type(limit) is not int or not 1 <= limit <= self.profile.max_page_records:
            raise EDIError(ErrorCode.CAPACITY, "world page size outside profile")
        with self._connection() as con:
            con.execute("BEGIN")
            if cursor is not None:
                if cursor.workspace_id != self.profile.workspace_id:
                    raise EDIError(ErrorCode.DENIED, "world cursor workspace mismatch")
                if query is not None and query != cursor.query:
                    raise EDIError(ErrorCode.INVALID, "world cursor filters cannot change")
                if revision is not None and revision != cursor.revision:
                    raise EDIError(ErrorCode.INVALID, "world cursor revision cannot change")
                query, revision, after = cursor.query, cursor.revision, cursor.after_id
            else:
                query, after = query or WorldQuery(), ""
            revision = self._revision(con, revision)
            if revision == self._head(con):
                sql = ("SELECT v.document_json FROM world_heads h JOIN world_versions v "
                       "ON v.record_id=h.record_id AND v.version=h.version WHERE v.record_id>?")
                args = [after]
            else:
                sql = ("SELECT v.document_json FROM world_versions v WHERE v.record_id>? AND "
                       "v.version=(SELECT MAX(t.version) FROM world_versions t WHERE t.record_id=v.record_id AND t.version<=?)")
                args = [after, revision]
            if query.family is not None:
                sql += " AND v.family=?"
                args.append(query.family.value)
            if query.scope_id is not None:
                sql += " AND v.scope_id=?"
                args.append(query.scope_id)
            if query.state is not None:
                sql += " AND v.state=?"
                args.append(query.state)
            elif not query.include_inactive:
                sql += " AND v.state IN ('candidate','accepted_for_use')"
            if query.valid_at is not None:
                sql += (" AND (v.valid_status='unbounded' OR (v.valid_status='interval' AND "
                        "(v.valid_start IS NULL OR v.valid_start<=?) AND (v.valid_end IS NULL OR v.valid_end>?))")
                value = _utc(query.valid_at)
                args += [value, value]
                if query.include_unknown_validity:
                    sql += " OR v.valid_status='unknown'"
                sql += ")"
            sql += " ORDER BY v.record_id LIMIT ?"
            args.append(limit + 1)
            rows = con.execute(sql, args).fetchall()
            items = tuple(StoredRepresentation.model_validate_json(row[0]) for row in rows[:limit])
            next_cursor = None
            if len(rows) > limit:
                next_cursor = WorldCursor(workspace_id=self.profile.workspace_id, revision=revision,
                                          query=query, after_id=items[-1].representation.record_id)
            return WorldPage(workspace_id=self.profile.workspace_id, revision=revision,
                             items=items, next_cursor=next_cursor)

    def dependencies(self, record_id: str, *, revision: int | None = None,
                     direction: str = "dependencies", max_depth: int = 1) -> DependencyView:
        if direction not in ("dependencies", "dependents"):
            raise EDIError(ErrorCode.INVALID, "invalid dependency direction")
        if type(max_depth) is not int or not 1 <= max_depth <= self.profile.max_dependency_depth:
            raise EDIError(ErrorCode.CAPACITY, "dependency depth outside profile")
        with self._connection() as con:
            con.execute("BEGIN")
            revision = self._revision(con, revision)
            if self._at(con, record_id, revision) is None:
                raise EDIError(ErrorCode.NOT_FOUND, "dependency root unavailable")
            queue, visited, items, boundaries = [(record_id, 0)], set(), [], set()
            truncation = None
            while queue:
                current, depth = queue.pop(0)
                if current in visited:
                    continue
                if len(visited) >= self.profile.max_dependency_nodes:
                    truncation = "node-budget"
                    break
                visited.add(current)
                if depth >= max_depth:
                    continue
                if direction == "dependencies":
                    owner = self._at(con, current, revision)
                    rows = [] if owner is None else con.execute(
                        "SELECT owner_id,owner_version,target_id,target_version FROM world_dependencies "
                        "WHERE owner_id=? AND owner_version=? LIMIT ?",
                        (current, owner.version, self.profile.max_dependency_edges + 1),
                    ).fetchall()
                else:
                    rows = con.execute(
                        "SELECT d.owner_id,d.owner_version,d.target_id,d.target_version FROM world_dependencies d "
                        "WHERE d.target_id=? AND d.owner_version=(SELECT MAX(v.version) FROM world_versions v "
                        "WHERE v.record_id=d.owner_id AND v.version<=?) ORDER BY d.owner_id,d.target_version LIMIT ?",
                        (current, revision, self.profile.max_dependency_edges + 1),
                    ).fetchall()
                for owner_id, owner_version, target_id, target_version in rows:
                    if len(items) >= self.profile.max_dependency_edges:
                        truncation = "edge-budget"
                        break
                    visible = self._at(con, target_id, revision)
                    validity = ("missing" if visible is None else "inactive"
                                if visible.state in ("retired", "withdrawn", "rejected") else "changed"
                                if visible.version != target_version else "current")
                    items.append(DependencyItem(owner_id=owner_id, owner_version=owner_version,
                                                target_id=target_id, pinned_version=target_version,
                                                visible_version=visible.version if visible else None,
                                                visible_state=visible.state if visible else None,
                                                validity=validity))
                    next_id = target_id if direction == "dependencies" else owner_id
                    if next_id not in visited and depth + 1 >= max_depth:
                        boundaries.add(next_id)
                    if next_id not in visited and depth + 1 < max_depth:
                        if len(queue) >= self.profile.max_dependency_edges:
                            truncation = "frontier-budget"
                            break
                        queue.append((next_id, depth + 1))
                if truncation is not None:
                    break
            boundaries -= visited
            if truncation is None and boundaries:
                truncation = "depth-boundary"
            return DependencyView(revision=revision, root_id=record_id, direction=direction,
                                  max_depth=max_depth,
                                  items=tuple(items), visited_ids=tuple(sorted(visited)),
                                  complete=truncation is None, truncation=truncation,
                                  depth_boundary_ids=tuple(sorted(boundaries)))
