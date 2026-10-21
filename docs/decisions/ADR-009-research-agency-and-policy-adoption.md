# ADR-009 — Research agency and explicit owned policy adoption

Date: 21 October 2026. Status: implemented source subset; unqualified. Decision owner: C7 through the trusted local operator boundary. Input: `686da92ec4a9c0892998aee1b85280b723d8f199`.

## Problem and requirements

The architecture separates perceived information, intent, realized execution, policy review and legitimate adoption. C0–C6 cannot gain action authority merely by emitting a recommendation. C7 must retain that distinction with finite resources and recoverable handoffs. IMP-R04/R07/R11/R12/R14/R15/R19/R23/R25/R29/R32/R33 allocate F70–F73; the [C7 trace](../implementation/C7_RUNTIME_TRACE.json) scopes the first implementation.

## Decision

Reuse the existing strict typed records, owner-restricted ports and local SQLite FULL/WAL pattern. C7 owns a separate lazy ledger; C1 remains evidence authority and C3 remains model/admission authority. Policy has a fixed research-readonly grammar with exact-origin/record grants. Only native observation metadata selection and pinned model reads have dispatch adapters. External action/acquisition and direct C5 simulation dispatch remain unsupported.

Record amendments separately from adoption. Local operator adopt/reject/defer uses a base-policy CAS; it is absent from the component facade. Purpose/standards changes require explicit goal versioning. Do not install a default grant or infer authorization from model prose. The local operator ID allowlist is a configuration assumption, not authentication.

Commit an immutable, single-use command intent and prepaid completion allowance before invocation. Recheck current policy/grant/expiry, sample time after lock acquisition, and fence cooperative work by active command/policy. Interrupted work stays unresolved; original retry returns status instead of redispatch. A local report archived byte-for-byte in C1 supports explicit reconciliation, not independently observed effect. Mark these reports generated with lineage.

Qualify explicit actor-information masks without appending global state. Supplied content/perception/psychology remains attributed and uncertain. C3-native actor visibility and C5 actor dynamics are still unavailable. Submit modeled policy/organization descriptions as staged candidate-only C3 puts; no actual domain adoption is inferred.

Access review reuses current standing grants and coalesces exact needs with retained denial/defer intervals. It neither acquires information nor sends a notification. C0 scheduling/notification ownership is preserved.

## Alternatives and tradeoffs

| Option | Assessment |
| --- | --- |
| Stateless allowlist and direct calls | Smaller, but loses adopted standards/history, uncertain completion and original review decisions. Insufficient for IMP-R12/R23. |
| Current typed ledger plus two internal adapters | Preferred finite first increment. Reuses installed dependencies and does not require an LLM for authority checks. Single-host trust, cooperative deadlines and finite storage remain limitations. |
| Generic agent framework/planner with arbitrary tools | Adds capability and policy ambiguity without satisfying explicit authority or evidence requirements. Not selected for this subset. |
| Production policy engine, signed capabilities and durable distributed workers | Relevant later when authenticated services/external connectors and failure domains are specified. Not added before the bounded local workflow needs them. |

This is an engineering flowdown of existing research-mode constraints and established repository patterns, not a claim of a newly superior policy algorithm or current third-party product ranking. No new dependency or mathematical model is selected; no changing external product claim is required to justify this increment.

## Assumptions, consequences and verification

Assume a trusted local operator/process/filesystem and sufficiently consistent UTC clock. A configured ID, source descriptor or content hash does not prove legitimate identity, physical perception, causal effect or truth. One unresolved command blocks policy adoption and another dispatch; this bounds ambiguity but can reduce availability. Reconciliation can require restoring C1 capacity/availability. Receipt quota is logically reserved; physical disk failure remains possible.

New C7 version 0.8.0 has explicit contracts/schemas, requirements, future cases and [source/interface review](../implementation/evidence/c7-source-review.json). All original lane dispositions remain unchanged. Runtime/security/recovery/scientific tests, independent review, complete requirements, hard isolation, backups/retention/migration/HA and production scale remain open. No runtime or gate validator was run under the owner's structure-first direction.
