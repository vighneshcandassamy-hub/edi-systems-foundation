"""Composition root for the existing C0-C7 owners and configured model roles.

Importing/validating configuration does not open stores, contact a provider,
start a process, acquire observations or execute an investigation.
"""
import os
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from edi.agency.benchmark import SimulationGrant
from edi.agency.config import AgencyProfile
from edi.analyze.config import AnalysisProfile
from edi.assess.config import AssessmentProfile
from edi.inquiry.contracts import WorkflowProfile
from edi.interpret.config import InterpretationProfile
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import ModelBinding
from edi.shared.config import LocalProfile
from edi.shared.contracts import Identifier, Record
from edi.shared.errors import EDIError, ErrorCode
from edi.world.config import WorldProfile


class StudentConnection(Record):
    binding: ModelBinding
    endpoint: str = "http://127.0.0.1:8008"
    api_key_env: Identifier = "EDI_VLLM_API_KEY"
    max_model_len: int = Field(default=16384, ge=16384)
    max_images: int = Field(default=1, ge=0, le=2)
    attribution: str = "Configured fixed student via vLLM; reported serving usage"


class TeacherConnection(Record):
    mode: Literal["file-exchange", "disabled"] = "file-exchange"
    binding: ModelBinding
    directory: Path = Field(default_factory=lambda: Path(".local/teacher-exchange"))
    identity_basis: Literal["operator-declared; provider identity not independently verified"] = "operator-declared; provider identity not independently verified"
    attribution: str = "Operator-imported teacher critique; generated assistance, not independent evidence"


class BrokerConnection(Record):
    grant: SimulationGrant
    token_env: Identifier = "EDI_BROKER_TOKEN"


class ApplicationProfile(Record):
    application_id: Identifier
    run_id: Identifier = Field(max_length=96)
    observation: LocalProfile
    student: StudentConnection
    teacher: TeacherConnection
    broker: BrokerConnection
    world: WorldProfile | None = None
    interpretation: InterpretationProfile | None = None
    reasoning: ReasoningProfile | None = None
    analysis: AnalysisProfile | None = None
    assessment: AssessmentProfile | None = None
    agency: AgencyProfile | None = None
    workflow: WorkflowProfile | None = None
    max_turns: int = Field(default=32, ge=1, le=1000)
    max_tokens: int = Field(default=262144, ge=16384)
    session_seconds: int = Field(default=3600, ge=1, le=604800)
    max_corrections: int = Field(default=1, ge=0, le=1)

    @model_validator(mode="after")
    def bindings(self):
        from urllib.parse import urlsplit
        endpoint = urlsplit(self.student.endpoint)
        if endpoint.scheme != "http" or endpoint.hostname != "127.0.0.1" or not endpoint.port or endpoint.path not in ("", "/") or endpoint.query or endpoint.fragment or endpoint.username:
            raise ValueError("student service must be explicitly configured on loopback")
        active = [self.student.binding] + ([self.teacher.binding] if self.teacher.mode != "disabled" else [])
        if any(value.model_id == "unbound" or value.revision == "unbound" or value.tokenizer_revision == "unknown"
                or any(item.startswith("REPLACE_") for item in (value.model_id, value.revision, value.tokenizer_revision)) for value in active):
            raise ValueError("active model roles require explicit bindings")
        if self.reasoning is not None and (self.reasoning.student != self.student.binding or self.reasoning.teacher != self.teacher.binding):
            raise ValueError("reasoning profile and configured model roles differ")
        workspace = self.observation.workspace_id
        for profile in (self.world, self.interpretation, self.reasoning, self.analysis, self.assessment, self.agency, self.workflow):
            if profile is not None and profile.workspace_id != workspace:
                raise ValueError("all owners must share the declared workspace")
        if self.broker.grant.workspace_id != workspace:
            raise ValueError("broker grant and application workspace differ")
        paths = [self.observation.database.resolve()]
        for name, profile in (("world", self.world), ("interpret", self.interpretation), ("reason", self.reasoning),
                ("analyze", self.analysis), ("assess", self.assessment), ("agency", self.agency), ("workflows", self.workflow)):
            paths.append((profile.database if profile is not None else self.observation.database.with_name(
                self.observation.database.stem + "." + name + ".sqlite3")).resolve())
        if len(set(paths)) != 8:
            raise ValueError("each owner requires its own database")
        return self

    @classmethod
    def load(cls, path):
        """Resolve configured paths relative to the configuration, never shell CWD."""
        import json
        path = Path(path).resolve()
        data = json.loads(path.read_bytes())
        observation = data.setdefault("observation", {})
        value = Path(observation.get("database", ".local/edi.sqlite3"))
        base = value if value.is_absolute() else path.parent / value
        observation["database"] = str(base)
        for name, suffix in (("world", "world"), ("interpretation", "interpret"), ("reasoning", "reason"),
                ("analysis", "analyze"), ("assessment", "assess"), ("agency", "agency"), ("workflow", "workflows")):
            if data.get(name) is not None:
                owner = data[name]
                value = Path(owner.get("database", str(base.with_name(base.stem + "." + suffix + ".sqlite3"))))
                owner["database"] = str(value if value.is_absolute() else path.parent / value)
                owner.setdefault("workspace_id", observation.get("workspace_id", "default"))
        if data.get("teacher") is not None:
            value = Path(data["teacher"].get("directory", ".local/teacher-exchange"))
            data["teacher"]["directory"] = str(value if value.is_absolute() else path.parent / value)
        return cls.model_validate_json(json.dumps(data))


class IntegratedApplication:
    """Explicit application construction; no model/broker request until step()."""
    def __init__(self, profile: ApplicationProfile):
        from edi.inquiry.runtime import Runtime
        from edi.inquiry.benchmark import Investigation
        from edi.observe.benchmark import BrokerConnector
        from edi.reason.exchange import TeacherExchangeGateway
        from edi.reason.gateway import NativeGateway, VllmBackend

        # Only named environment values are read; secret values never enter profiles.
        token = os.environ.get(profile.broker.token_env)
        serving_key = os.environ.get(profile.student.api_key_env)
        if not token or not serving_key:
            raise EDIError(ErrorCode.UNAVAILABLE, "configured broker/student environment credentials are absent")
        reason_profile = profile.reasoning or ReasoningProfile(workspace_id=profile.observation.workspace_id,
            database=profile.observation.database.with_name(profile.observation.database.stem + ".reason.sqlite3"),
            student=profile.student.binding, teacher=profile.teacher.binding)
        self.profile = profile
        self.runtime = Runtime(profile.observation, profile.world, profile.interpretation, reason_profile,
            profile.analysis, profile.assessment, profile.agency, profile.workflow)
        r, grant = self.runtime, profile.broker.grant
        from hashlib import sha256
        authority = r.agency_for("C0").benchmark_authority(grant, endpoint=grant.endpoint,
            token_sha256=sha256(token.encode()).hexdigest(), workspace_id=r.profile.workspace_id,
            session_id=grant.session_id)
        connector = BrokerConnector(r, grant.endpoint, token, grant.session_id, authority,
            r.workflow.profile.database, max_requests=grant.maximum_requests)
        backend = VllmBackend(profile.student.endpoint, profile.student.binding.model_id,
            api_key=serving_key, max_model_len=profile.student.max_model_len)
        student = NativeGateway(r, profile.student.binding, r.reasoning.profile.database, backend,
            backend.count_tokens, attribution=profile.student.attribution,
            max_images=profile.student.max_images, max_calls=profile.max_turns * 6)
        self.teacher = None if profile.teacher.mode == "disabled" else TeacherExchangeGateway(
            r, profile.teacher.binding, r.reasoning.profile.database, profile.teacher.directory,
            attribution=profile.teacher.attribution, max_calls=profile.max_turns * 2)
        self.investigation = Investigation(r, connector, student, r.workflow.profile.database,
            profile.run_id, teacher_gateway=self.teacher, max_turns=profile.max_turns,
            max_tokens=profile.max_tokens, session_seconds=profile.session_seconds,
            max_corrections=profile.max_corrections)

    def step(self):
        return self.investigation.step()

    def import_teacher(self, job_id, feedback):
        if self.teacher is None:
            raise EDIError(ErrorCode.UNAVAILABLE, "teacher disabled in this application profile")
        return self.teacher.import_feedback(job_id, feedback)
