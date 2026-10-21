"""C7 opt-in authority for a constructed world. Existing research policy is unchanged."""
from datetime import datetime
from typing import Literal
from urllib.parse import urlsplit

from pydantic import Field, JsonValue, model_validator

from edi.shared.contracts import Identifier, Record, utc_now
from edi.shared.durable_io import CallJournal, digest
from edi.shared.errors import EDIError, ErrorCode

PublicOperation = Literal["mission", "sources", "people", "search", "read", "records", "ask", "measure", "act", "advance", "status", "propose", "submit"]


class PublicIntent(Record):
    operation: PublicOperation
    body: dict[str, JsonValue]


class SimulationGrant(Record):
    """Trusted operator configuration, not a grant a model may adopt."""
    grant_id: Identifier
    session_id: Identifier
    workspace_id: Identifier
    endpoint: str
    token_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    mission_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    operator_id: Identifier
    not_before: datetime
    expires_at: datetime
    operations: tuple[PublicOperation, ...]
    maximum_requests: int = Field(default=300, ge=1, le=10000)
    authority: Literal["explicit-human-simulated-world-mission"] = "explicit-human-simulated-world-mission"

    @model_validator(mode="after")
    def valid(self):
        p = urlsplit(self.endpoint)
        if p.scheme != "http" or p.hostname != "127.0.0.1" or not p.port or p.path not in ("", "/") or p.username or p.password or p.query or p.fragment:
            raise ValueError("benchmark authority permits an exact loopback broker only")
        if any(x.utcoffset() is None for x in (self.not_before, self.expires_at)) or self.expires_at <= self.not_before:
            raise ValueError("grant needs an aware nonempty interval")
        if not self.operations or len(set(self.operations)) != len(self.operations):
            raise ValueError("grant needs distinct finite operations")
        return self


class BenchmarkAuthority:
    """C0 supplies already-selected requests. This port supplies no policy advice."""
    def __init__(self, path, grant: SimulationGrant, *, endpoint, token_sha256, workspace_id, session_id):
        self.grant = SimulationGrant.model_validate_json(grant.model_dump_json())
        if (grant.endpoint.rstrip("/"), grant.token_sha256, grant.workspace_id, grant.session_id) != (endpoint.rstrip("/"), token_sha256, workspace_id, session_id):
            raise EDIError(ErrorCode.DENIED, "broker identity does not match adopted simulated-world grant")
        self.journal = CallJournal(path, "benchmark_c7", max_calls=grant.maximum_requests + 1, max_bytes=16 * 1024**2)
        previous = self.journal.begin("standing-grant", grant, reserve_bytes=1024)
        self.journal.finish("standing-grant", {"grant_sha256": digest(grant), "operator_id": grant.operator_id})

    def authorize(self, intent: PublicIntent):
        now, g = utc_now(), self.grant
        if not g.not_before <= now < g.expires_at or intent.operation not in g.operations:
            raise EDIError(ErrorCode.DENIED, "operation absent from current simulated-world standing authority")
        request_id = intent.body.get("request_id")
        if not isinstance(request_id, str) or not 1 <= len(request_id) <= 120:
            raise EDIError(ErrorCode.INVALID, "public operation requires a stable bounded request ID")
        # Broker enforces exact public argument domains and physical world budgets.
        # This ledger enforces the external boundary and root grant count first.
        self.journal.begin(request_id, intent, reserve_bytes=1024)
        self.journal.finish(request_id, {"allowed": True, "grant_sha256": digest(g), "objective_change": "pending-human-review" if intent.operation == "propose" else None})
        return {"allowed": True, "grant_id": g.grant_id}
