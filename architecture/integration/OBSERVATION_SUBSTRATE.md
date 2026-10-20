# Observation and substrate integration plan

Date: 2026-10-19. Status: proposed contracts; design review REVISE. Product integration NOT RUN. Baseline input: private edi-lab commit a0c2c838c4ffb9cc0b7706082ad4ca5cf37a8d78. Companion: [substrate blueprint](../substrate/SUBSTRATE_BLUEPRINT.md), [observation specs](../observation/COMPONENT_SPECS.md).

## Scope and authority

Two system components, one unordered pair, two independently specified directed lanes. Eleven contract families are grouped into those lanes; bidirectional does not mean symmetric ownership. Internal parts have a separate [six-lane catalogue](SUBSTRATE_INTERNAL_INTERFACES.json). The [system catalogue](INTERFACES.json) records facets, requirements, prospective cases and findings.

Observation's four parts are its existing logical decomposition. Substrate has three proposed logical parts, initially one process: C1 durable representation fabric, C2 admission/change engine, C3 inquiry coordinator. The two catalogues do not redefine capability lists as component stacks.

OBS owns received native evidence, acquisition identity/assertions, commit and availability history. SUB owns representations, mechanisms, alternatives and selection/revision history. SUB cannot rewrite OBS records, directly promote physical identity, or acquire new external action authority through a query. OBS cannot decide SUB hypotheses merely because it accepted an operational assertion.

## Contract families

| ID | Lane | Operation and obligation |
| --- | --- | --- |
| INT-OS-001 | OBS → SUB | Committed evidence/descriptors, assertion/correction/availability changes and cursor. Enter SUB-C2 admission before SUB-C1 materialization. Receipt/staged is insufficient. |
| INT-OS-002 | SUB → OBS | Bounded get_record/read_payload/read_part, resolve_identity(valid_at, known_at, policy), coverage, commit_status and replay requests. Preserve native selectors and requested historical scope. |
| INT-OS-003 | OBS → SUB | Correlated query results/errors with native/derived distinction, revisions, cursor/watermark, unknown/unavailable/truncated status. No silent current-view substitution. |
| INT-OS-004 | SUB → OBS | Supported request_acquisition with stable ID, target/settings/duration/budget and selection lineage. No new intervention authority. |
| INT-OS-005 | OBS → SUB | Requested-versus-actual acquisition settings, status, cost and resulting committed observation references. Accepted request is not observed physical effect; denial/cancellation/timeout/unavailable are valid results. |
| INT-OS-006 | SUB → OBS | Attributed association/correction proposals through append/retract_assertion semantics. Proposal cannot directly merge accepted physical identities. |
| INT-OS-007 | OBS → SUB | Policy-scoped assertion acceptance/retraction/status and as-of consequences. Operational acceptance is not independently observed physical truth. |
| INT-OS-008 | SUB → OBS, optional | Budgeted versioned derivation job over retained selectors. Exact C4 request wire binding is proposed, not an existing concrete endpoint. |
| INT-OS-009 | OBS → SUB, optional | Derived result or failure with source/method/model/preprocessing versions and complete work costs. Result remains derived, including when ingested as an observation of internal computation. |
| INT-OS-010 | SUB → OBS | Consumer progress/demand/cancel. Exact acknowledgement/session binding remains to freeze. Durably commit SUB state/applied IDs/checkpoint before acknowledging progress. |
| INT-OS-011 | OBS → SUB | Flow/capability/lag/limit/lifecycle status so SUB can bound requests and represent missingness. A status message is not evidence of an external mechanism. |

These are logical contract families, not eleven new network services. OBS API families exist as design specifications; concrete implementation endpoints are not claimed. Derived results, committed deltas and query results may share transport while retaining their distinct meaning and correlation.

## Shared semantics and end-to-end checks

Identity: retain scope, source epoch, occurrence identity and revision. Payload hashes may deduplicate bytes, not erase separate occurrences. A similar image/label or shared embedding is not proof that the source/physical element is identical two years later. Candidate/unknown/disputed associations remain valid.

Time: distinguish valid/event/source, receipt, commit, known-at and model time. Preserve supplied clock uncertainty and order limitations. Acquisition-order cursors differ from event-time views; gaps and unknown coverage are not zero. Late corrections identify affected dependencies and historical interpretation, not a rewrite of native evidence.

Delivery and durability: retry-stable request/occurrence IDs and status lookups resolve duplicate or unknown outcomes. SUB-C2 admits; SUB-C1 commits representation changes, applied IDs and consumed checkpoint consistently, then acknowledges OBS. No global cross-component transaction or exactly-once physical action guarantee is assumed. Explicitly qualify the crash windows and fault model.

Retention: OBS has availability/tombstone semantics but no specified external pin/lease endpoint. The first contract handles eviction honestly: retain only authorized supported copies with lineage, or mark native support/replay unavailable. A durable derived representation does not guarantee eternal raw replay. A future lease requires a justified requirement and concrete lifecycle contract.

Compatibility: pin schema, selector, transform, model/weights/preprocessing and feature-space versions. Preserve unknown extensions without silently interpreting them. Regeneration consumes a budget; incompatible features are not silently compared. Read results expose projection lag.

Resources: use bounded pages/ranges, inquiry queue/trial limits, supported acquisition limits and a shared root budget. Count transfer, retrieval, parsing, optional model inference, retries, failed/cancelled work, storage and recovery. Exact integrated capacity/fault profile remains pending. An optional worker/model outage must not stall qualified native acquisition/commit.

Feedback: a result from EDI or an LLM can be recorded for audit but cannot corroborate its own external claim. Preserve source/dependency and selection lineage across OBS → SUB → inquiry → acquisition → OBS. Report both denied and non-discriminating requests. Selection is part of what EDI learns about its exposure, not invisible random sampling.

## Existing downstream obligations

| OBS obligation | SUB requirement allocation | Integration cases |
| --- | --- | --- |
| DOWN-001 Claims/derived output are not validated facts | SUB-R007, R008, R011 | INT-V001, V007 |
| DOWN-002 Unknown identity/time/coverage remain explicit | SUB-R001, R005, R007, R009 | V002, V005 |
| DOWN-003 Corrections and as-of interpretation | SUB-R002, R005, R009, R011 | V002, V005, V012 |
| DOWN-004 Bounded access and unavailable history | SUB-R006, R014, R015 | V003, V008, V009 |
| DOWN-005 Imported model lineage/compatibility | SUB-R008, R016 | V007, V011 |
| DOWN-006 Acquisition budget/selection | SUB-R010, R014 | V006, V007, V009 |
| DOWN-007 Durability/recovery | SUB-R002, R011, R015 | V004, V010, V012 |
| DOWN-008 Complete task costs | SUB-R013, R014, R016 | V006, V009, V011 |

## Prospective integration verification

| ID | Required case | State |
| --- | --- | --- |
| INT-V001 | Mixed native input becomes attributable representation without discarding selectors or importing certainty | NOT RUN |
| INT-V002 | Correction/retraction preserves historical states and identifies affected dependencies | NOT RUN |
| INT-V003 | Bounded historical query returns correct scope, continuation and explicit unsupported/unavailable results | NOT RUN |
| INT-V004 | Duplicate/reordered deliveries and unknown outcomes do not lose occurrences or apply an update twice | NOT RUN |
| INT-V005 | Epoch/clock reset, late evidence and coverage gaps remain explicit | NOT RUN |
| INT-V006 | Acquisition request yields attributable actual result or denial/cancellation/timeout with costs | NOT RUN |
| INT-V007 | Internal/model/administrative echo never becomes independent corroboration | NOT RUN |
| INT-V008 | Evidence eviction invalidates raw-access promises while preserving honest availability/support state | NOT RUN |
| INT-V009 | Overload bounds full work/cost and isolates optional inquiry from native intake | NOT RUN |
| INT-V010 | Crash/restart at handoff boundaries preserves durable state/applied IDs/checkpoint and recovery semantics | NOT RUN |
| INT-V011 | Schema/model/preprocessing/feature-space mismatch is isolated or explicitly migrated | NOT RUN |
| INT-V012 | Stale/conflicting/unsupported/out-of-scope changes cannot silently mutate authoritative state | NOT RUN |

## Internal and outside dependencies

The internal catalogue covers all three pairs/six lanes. C1↔C2 supplies bounded state/version/commit requests and outcomes. C1↔C3 supplies bounded reads/change views; C3 direct writes are prohibited. C2↔C3 carries attributed trial/change requests and their validation/outcomes. Review the whole strongly connected group for proposal/commit/read feedback, budget cycles and self-confirmation.

Optional model dependency: C3 → model sends selected bounded context, pinned configuration, deadline and budget with no write/action capability. Model → C3 returns attributed proposals, usage and errors, never independent evidence. Freeze provider retention, availability, version and cost policies before enabling it. Failure defers inquiry. This dependency is inventoried separately from the two product components; if independently governed as another component, add it to the registry and regenerate every pair.

Sources/actuators remain outside this two-component boundary. Supported acquisitions do not authorize new physical experiments. Observation source loss, human intervention and external time uncertainty cannot be solved by an internal acknowledgement.

## Findings and gate

| Finding | Disposition and blocked work |
| --- | --- |
| INT-G001 | Freeze concrete schemas, version/error bindings and fixtures before contract/runtime pass. |
| INT-G002 | Missing external retention pin resolved at design level by explicit unavailable fallback; no invented endpoint. Qualify eviction behavior at runtime. |
| INT-G003 | Exact progress/ack session and C4 job request bindings pending; contract/runtime blocked until specified. |
| INT-G004 | Operational identity decisions separated from physical truth; natural cross-modal identity accuracy remains unqualified. |
| INT-G005 | Freeze integrated workloads, resource/fault profile and recovery semantics; no measured efficiency, scale or HA claim. |

The reusable edi-interface-review skill performs all-pair directed inventory and feedback review. With three components it reviews three pairs/six lanes; with four, six pairs/twelve lanes. A not_needed/prohibited decision is legitimate. JSON helper success establishes structural consistency only. Current design review is self-review, REVISE; product runtime/integration NOT RUN. No implementation or comparison is started by this document.
