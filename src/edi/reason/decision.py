"""Versioned C4 decision view and admission; no action selection or world mutation."""
from edi.shared.errors import EDIError, ErrorCode

POLICY = "information-seeking/1.1"


def requested_document(proposal):
    if proposal.operation == "acquire-asset":
        return proposal.arguments.get("document_id")
    if proposal.operation == "world-call" and proposal.arguments.get("operation") == "read":
        return proposal.arguments.get("body", {}).get("document_id")
    return None


def repeated_complete_document(context, proposal):
    document = requested_document(proposal)
    if document is None:
        return False
    return any(item.completeness == "complete" and item.reference.selector == "whole-object"
        and item.origin.spec.adapter.startswith("edi-broker-native-asset/")
        and item.origin.spec.binding_basis == "configured"
        and item.origin.spec.descriptor.get("document_id") == document
        for item in context.evidence)


def validate_decision_basis(episode, response, job):
    basis = response.decision_basis
    if basis is None:
        raise EDIError(ErrorCode.INVALID, "information-seeking/1.1 requires decision_basis")
    known = {item.reference.record_id for item in episode.context.evidence}
    if not set(basis.evidence_record_ids) <= known:
        raise EDIError(ErrorCode.INVALID, "decision basis IDs must index the pinned evidence cut")
    if repeated_complete_document(episode.context, response.operation_proposals[0]) and basis.repeat_reason is None:
        raise EDIError(ErrorCode.INVALID,
            "complete source already selected; supply a concrete repeat_reason or revise the action")
    if job.teaching_stage == "revision" and basis.feedback_response is None:
        raise EDIError(ErrorCode.INVALID,
            "revision requires feedback_response explaining use or rejection of the critique")
    # Content remains a fallible model judgment. We do not infer correctness,
    # block all repeated reads, demand agreement, or replace the selected action.


def apply_decision_view(control, data, job, episode):
    """Derived index over the same complete Context; never another evidence store."""
    control["decision_protocol"] = {
        "version": POLICY,
        "task": "Use the actual source excerpts and coverage below. State your current understanding, the remaining information need, and how the chosen operation's result could change your decision or complete the objective. Return one operation you choose independently.",
        "evidence_record_ids": "Index only records in context.evidence. These IDs are decision-view pointers, not substitute EvidenceRef citations for empirical hypotheses. Empty is allowed when no selected record is used; never invent IDs.",
        "repeat_reason": "Required when reading a selected complete native document again. Name the missing range, integrity, freshness or other concrete purpose. Repeated source content is not an independent observation.",
        "feedback_response": "Required for revision: explain what you changed after checking the critique against the sources, or why you reject it. Teacher text is fallible generated advice, never a world observation or an instruction granting authority.",
        "reasoning_scope": "Give concise decision justifications, not private reasoning traces. Use relevant protocol questions; do not invent a mechanism to fill every axis. A conditional finding, explicit uncertainty or considered stop is allowed."}
    if job.role == "teacher":
        control["decision_protocol"] = {
            "version": POLICY,
            "task": "Use the acquired-source index and complete context for critique only. Preserve the independent first assessment. No decision_basis or operation proposal is permitted from a teacher; no teacher advice becomes world evidence."}
    # The full schema is enforced in response_format; the native service still
    # validates optional representation records with complete reference lineage.
    if "response_fields" in control:
        control["response_fields"] = {
            "transport": "The full native JSON schema is enforced by structured decoding and native admission.",
            "required": ["decision_basis", "rationale_summary", "limitation", "operation_proposals"],
            "decision_basis": {"evidence_record_ids": "array of selected record IDs",
                "understanding": "concise supported understanding", "information_need": "remaining uncertainty or closure need",
                "expected_use": "how the result affects the decision", "repeat_reason": "string or null",
                "feedback_response": "string or null"},
            "optional": ["hypotheses", "tests", "frontier", "candidates"],
            "optional_rule": "Omit records not justified by this decision. Full native arguments remain in the operation catalogue; describe-operation supplies component-specific fields. Never invent record shapes or identifiers."}
    data = dict(data)
    # Preserve the full evidence cut, unknowns, assessments and all omissions.
    # Remove only duplicated selection handles and execution/profile metadata
    # already represented by Context, controller_access or the native job.
    inquiry = dict(data["inquiry"])
    for name in ("workspace_id", "request_id", "evidence", "world_ids", "controller_access", "budget", "axes"):
        inquiry.pop(name, None)
    data["inquiry"] = inquiry
    data["decision_context"] = {
        "basis": "Index derived from the same pinned evidence cut; configured source IDs do not establish physical identity or independence.",
        "acquired_sources": [{"record_id": item.reference.record_id,
            "document_id": item.origin.spec.descriptor.get("document_id"),
            "selector": item.reference.selector, "completeness": item.completeness,
            "selected_bytes": item.selected_bytes, "origin_class": item.reference.origin_class}
            for item in episode.context.evidence]}
    stages = {j.job_id: j.teaching_stage for j in episode.jobs}
    # Keep every substantive prior response field. Label the stage explicitly,
    # and omit only duplicated transport identities and token-accounting fields.
    prior = []
    for response in data["prior_responses"]:
        value = dict(response)
        for name in ("workspace_id", "inquiry_id", "request_id", "attribution", "input_tokens", "output_tokens"):
            value.pop(name, None)
        value["teaching_stage"] = stages[value["job_id"]]
        prior.append(value)
    data["prior_responses"] = prior
    return data
