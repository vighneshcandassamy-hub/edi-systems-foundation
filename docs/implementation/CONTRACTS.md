# State, data and interface contracts

Version 0.1, 20 October 2026. Gate: proposed architecture contracts. This is a specification for implementation; no endpoint or serialized schema is claimed implemented. Full pair dispositions and operation facets are in [INTERFACES.json](INTERFACES.json). All model scenarios remain planned.

Version 0.2 extension: [SCALING_AND_WORLD_GROWTH.md](SCALING_AND_WORLD_GROWTH.md) adds proposed ModelDelta, projection/cache validity, RefinementBridge, ExplorationFrontier and KnowledgeRequest records and their guarded state transitions. The updated matrix allocates their operations over existing lanes; no new state owner is introduced. New data changes invalidate dependent current views; original forecast seals and source records remain immutable.

## 1. Contract boundaries and authority

The eight logical modules in [COMPONENTS.md](COMPONENTS.md) have separate state owners. The JSON matrix reviews every unordered pair and both directed lanes. Required lanes are logical operations/results, not a requirement for network services. In-process calls still obey the same authority and version rules. An optional deployment split cannot grant new mutation rights.

Only C1 commits source occurrences and evidence availability. C2 owns derivations but submits interpretation/identity proposals to C3. Only C3 admits and commits canonical model revisions. C4 proposes investigations and patches. C5 executes isolated analysis. C6 seals expectations and owns assessment results. C7 owns EDI's actual action/adoption policy. C0 coordinates jobs and budgets, carrying decisions between owners without impersonating them.

Admission is a versioned policy, not an unspecified truth oracle. Distinguish `received_candidate`, `schema_validated`, `candidate`, `accepted_for_use`, `rejected`, `withdrawn` and `superseded`. C3 can retain a well-formed LLM proposal as a candidate. Promoting it to accepted-for-use requires a recorded decision under the selected admission policy, with a declared use/scope, support or explicit assumption, remaining rivals and verification obligation. An empirical-evidence claim additionally requires linked independent observations/assessments; plausible prose or schema validity cannot satisfy it. Provisional hypothetical models may be analyzed without promotion. Exact policy rules and fixtures are a concrete contract-gate obligation.

Represented human/institutional policies, their perceived information and reported adoption are C3 world-model content. This is distinct from the C7 runtime policy that controls EDI's tools. A proposed intervention on a forest or feedback channel is not an enacted change. A modeled adoption may occur within an isolated simulation without authorizing a real-world command.

Commands and responses are distinct operations even on one request/response transport. For example, reading records does not grant deletion; acknowledging a model proposal does not prove it was accepted; accepting a model does not prove its truth. Direct C4/C5 execution through C7 is prohibited: action requests must reach the authorized C0/C7 workflow. Direct writes across owner schemas are prohibited even when the corresponding read lane is required.

## 2. Common transport and record discipline

Keep the outer message small. Native observation envelopes retained from the earlier plan are not silently redefined; this package specifies a proposed adapter mapping into typed runtime ports. Concrete migration/compatibility fixtures are required before contract PASS.

| Object | Mandatory minimum | Conditional extensions / semantics |
| --- | --- | --- |
| `CommandEnvelope` | `schema_version`, `workspace_id`, `request_id`, `operation`, `producer`, `body`, `profile_id`. | `idempotency_key` for mutations/dispatch; `base_revision` for revision-dependent updates; `deadline`, `budget_reservation`, `capability_ref` when applicable. No LLM prose in authority fields. |
| `ResultEnvelope` | `schema_version`, `request_id`, `status`, `producer`, `body_or_reference`. | `committed_revision`, `durability`, `watermark`, `next_cursor`, `truncation`, `usage`, `error` where applicable. `received`, `staged` and `committed` are distinct. |
| `RecordIdentity` | Workspace-scoped opaque record ID, record kind, revision or immutable content identity. | Native source namespace/ID/epoch remains separate. Entity association claims refer to multiple identities without replacing them. |
| `TemporalScope` | `known_at` and internal `committed_at`; explicit known/unknown status for valid/event time. | Valid interval, source event/measurement/report time, received time, clock ID/uncertainty, timezone/time basis, ordering/sequence/gap. Simulated time uses a separate clock/run ID. |
| `EvidenceRef` | Occurrence or artifact ID, immutable revision/hash, exact selector, origin class, derivation lineage. | Span, page/region, array coordinates, media track/time, part path; transform/model versions and common-source group. `no_selector` needs an explicit whole-object choice. |
| `Quantity` | Value or explicit missing/unknown kind; quantity/scale kind; unit or unknown reason; time/aggregation context. | Cardinal vs ordinal vs categorical; bounds/distribution and parameter/model links where supplied. Numeric strings are not silently coerced into physical quantities. |
| `Assertion` | Claim ID, subject/participants, predicate or native structure, descriptive role(s), basis, support/counterevidence, temporal/applicability scope and state. | Alternatives, mechanism role, association hypothesis, actor owner, model/prompt lineage and uncertainty axes. Scope and basis are independent of accepted-for-use status. |
| `ModelPatch` | Base revision, typed operations, affected referents, reason, evidence/assumption refs, proposer and requested admission class. | Migration/carry-over mapping, pending commitments, irreversible/loss consequences and verification refs for structural changes. |

Message schema evolution uses major/minor semantics at the contract boundary, not whichever package version happens to be installed. Unknown major versions are rejected without mutation. Additional optional fields within a compatible minor version can be preserved but cannot alter authority or numerical meaning. Required-feature flags are rejected when unsupported. Unknown extension payloads are retained opaquely only in explicit namespaces, with size limits. Changing the meaning of a predicate, unit or scale is a semantic revision, not an unannounced optional field.

Reference identity, delivery identity and content identity have different purposes. Use retry-stable request IDs for commands, occurrence IDs for acquisition events and cryptographic hashes for bytes. Shared content may serve many distinct occurrences. Hash equality never proves a physical referent or a second independent source.

## 3. Core domain records

| Record | Important required/conditional fields | Owner and transition rule |
| --- | --- | --- |
| `InquirySpec` | Question/background objective, causal scope, evaluative interests, included/excluded systems, horizons/resolution, available sources/rights, hypotheses, budgets and completion/stopping rule. | C0; new versions retain previous purpose and criteria. |
| `Occurrence` | Source binding/epoch, optional source sequence, native content manifest, event/receipt/known times and uncertainty, coverage/gap status, committed durability and acquisition selection lineage. | C1; append-only receipt/evidence history. |
| `Derivation` | Input evidence refs, decoder/model/checkpoint/prompt/tool-schema versions, transformations, output artifact refs, uncertainty, failure/partial status and complete usage. | C2; recomputation is a new derivation, never another source observation. |
| `AssociationDecision` | Candidate links, positive/negative evidence, source vs referent relation type, alternatives, validity/known time, decision rationale and supersession. | C3 admission; a split/reversal invalidates dependent projections and analysis eligibility. |
| `SystemSnapshot` | Immutable revision, nine-family records, active assertion membership, allowed alternative set, domain/boundary closure and dependencies. | C3; one snapshot is a view of represented beliefs, not a globally true world. |
| `MechanismSpec` | Role-indexed input/output participants, quantitative equation/rule or explicit unknown, units/scales, applicability, parameter uncertainty, temporal/history requirements, resource constraints and backend capabilities. | C3 describes; C5 compiles only a supported subset. |
| `ActorView` | Actor identity, available/received observations and timing, attention/interpretation assumptions, memory, attributed frames/goals, active policy and perceived options. | C3 snapshot; C5 cannot leak analyst-only state through the view. |
| `ScenarioSpec` | Model revision, actual initial state plus history and pending commitments, known-at cut, driver/intervention schedule, actor masks, horizon, outcome correspondence, numerical method, random seeds and budget. | C5 scenario namespace; references goals/criteria without overwriting them. |
| `RunRecord` | Scenario/config/compiler/backend versions, artifact hashes, start/end/status, predicted quantities, diagnostics, samples/ensembles, unsupported regions, partial work and usage. | C5; output is `simulation` or `forecast`, never an acquired outcome. |
| `ForecastSeal` | Original run/model/policy IDs, output targets, issue time/knowledge cut, assumptions, horizon, scoring/selection rule and immutable hash. | C6; corrections produce a new seal. |
| `Assessment` | Seal, selected independent outcomes, correspondence/availability checks, discrepancies, common-source/selection history, rivals, calibration/coverage limits and revision decision rationale. | C6; metric changes are versioned and cannot rescore away a failure. |
| `ActionProposal` | Actor/EDI boundary, purpose/criteria version, target, operation/parameters, predicted effects/limits, authorization required, current policy and budget. | C7 operational lifecycle; domain proposals remain C3 assertions until appropriate evidence. |
| `ExecutionReceipt` | Proposal/authorization/dispatch IDs, connector identity, idempotency/completion state, reported receipt and separate measured-effect references. | C7 receipt authority; original connector report is captured by C1 as a report with provenance. |
| `PolicyAmendment` | Existing/new version, owner/authority, monitoring/expectation basis, trigger, proposal, acceptance/rejection/defer, resources/timing and state carry-over. | C7 for actual EDI policy, C3 for modeled actor policy; analyst correction uses a different operation type. |
| `StrategicFinding` | Support/counterevidence, mechanism chain, scope/horizon, affected criteria/parties, uncertainty/rivals, novelty and expected decision relevance, test suggestion and review trigger. | C6 prepares, C0 publishes to configured internal findings channel; no implicit external message. |

## 4. Operations and port ownership

| Owner | Proposed operations | Returns / admission rule |
| --- | --- | --- |
| C0 | `start_inquiry`, `revise_scope`, `reserve_work`, `schedule`, `cancel`, `status`, `deliver_finding`. | Durable job ID and original result or explicit unresolved completion. Results never confer model or action authority. |
| C1 | `register_source`, `ingest`, `append_chunk`, `finalize`, `commit_status`, `select_records`, `read_payload`, `coverage`, `request_acquisition`, `export_restore`. | Occurrence/manifest IDs and durability, bounded cursor reads, supported acquisition outcome or refusal. Assertions about physical identity remain C3-owned. |
| C2 | `decode`, `interpret`, `propose_associations`, `derive_features`, `get_derivation`. | Versioned artifacts/candidate claims with exact input refs and usage. Model failure leaves C1 records available. |
| C3 | `read_snapshot`, `query_view`, `query_dependencies`, `propose_patch`, `admit_patch`, `commit_status`, `association_history`, `rebuild_projection`. | Base-revision/authority validation, committed new revision or typed conflict/rejection. An invalid candidate can be retained separately for audit. |
| C4 | `investigate`, `propose_mechanisms`, `design_test`, `rank_frontier`, `explain_proposal`. | Candidate patches/tests/frontier items, assumptions and stop/yield reason. No direct action dispatch. |
| C5 | `validate_capabilities`, `compile_model`, `run_scenario`, `sensitivity`, `get_run`, `cancel_run`. | Run ID, sealed artifacts and diagnostics or `unsupported_model` before numerical execution. |
| C6 | `seal_forecast`, `compare_outcome`, `diagnose_error`, `review_revision`, `query_assessments`, `draft_finding`. | Forecast seal or assessment/recommendation. Checks sources and knowledge cut before quantitative scoring. |
| C7 | `read_policy`, `check_action`, `request_adoption`, `dispatch_authorized`, `reconcile_execution`, `get_receipt`. | Explicit allowed/denied/deferred/uncertain result under a pinned operational policy; no action in initial research mode. |

The matrix specifies operation-direction links, producer/consumer ports, requirements, cases and eleven facets for every active lane. The common profile covers compatible behaviors only. Requests for evidence/model/assessment reads are separate from their returned result lanes. Mutation results identify the admitting owner and revision.

## 5. Delivery, ordering, commit and recovery

1. Source delivery and worker notifications may be at least once. Admit idempotent commands using a stable key plus payload fingerprint; conflicting reuse is rejected. Do not deduplicate genuine occurrences merely because content is identical.
2. Ordering is per source/epoch or explicit local commit sequence. No global physical-time ordering is inferred. Time uncertainty, late arrivals, gaps, out-of-order input and multi-clock comparisons remain explicit.
3. Each owner commits its domain state and notification in a local transaction. A workflow spanning owners is a sequence of idempotent committed steps; no fictional distributed atomic transaction is assumed.
4. Jobs use bounded leases/fences. A stale worker result cannot overwrite a newer revision. Recovery replays committed steps and queries uncertain completion before retrying effects. A process restart is not a new observation or successful experiment.
5. Snapshot-based analysis pins model/input/history/known-at cuts. Retrieval and projection watermarks accompany reads. A stale index may be bypassed by an authoritative query or returned as stale; it is never silently current.
6. Evidence availability, model acceptance, outcome truth and external effect remain distinct states. `committed` means a declared storage guarantee, not factual confirmation.

Transactionally admitting several modeled flows means computing one joint change set from the same modeled state and enforcing shared capacities once. It is different from a sequence of software notifications. A `stock_delta` is not applied twice when two feedback-path views reference the same transfer.

## 6. Errors and resource semantics

Typed statuses: `ok`, `partial`, `unsupported`, `unavailable`, `denied`, `conflict`, `timeout`, `cancelled`, `capacity_exceeded`, `invalid_input`, `integrity_mismatch`, `stale_projection`, `not_identifiable`, `unknown_completion`. Include attributable owner/operation, retryability, durable receipt/revision where any, and retained partial-artifact refs. Error text cannot itself change authority.

Native reads paginate by records and bytes; media reads can select byte/time ranges but preserve selector semantics. A caller must explicitly accept truncated context. Derivation/model calls have maximum input/output work, wall time, concurrency and budget. Analysis has limits on state count, simulated horizon, events, solver work, ensemble size and artifact bytes. Every extension declares its own resource profile rather than inheriting a misleading universal token budget.

The proposed development profile in [VERIFICATION.md](VERIFICATION.md) is finite. Admission can reject or defer work; these outcomes remain counted. Queue saturation must not cause unbounded in-memory retention or silent evidence loss. Cancellation records partial cost and distinguishes acknowledged cancellation from an external effect that may already have occurred.

Retention uses a declared availability horizon and holds for original forecasts, lineage and critical references. Evicted bytes produce tombstones and an invalidation/limitation path for dependent claims. Rebuildable indexes can be dropped before source evidence, subject to policy. No file or model claim promises indefinite access to data already removed. Backup/restore must cover both artifact bytes and transactional references at a consistent recoverable point.

## 7. Shared dependencies and indirect paths

| Dependency | Owner / permitted use | Integration risk and containment |
| --- | --- | --- |
| Postgres | One deployment, owner-specific schemas/ports; direct cross-owner DML denied. C0 jobs, C1 occurrences, C3 models, C6 assessments and C7 operational policy have distinct authorities. | Shared outage/connection exhaustion can stop several modules. Reserve intake capacity, bound pools, expose health and use a consistent recovery point. A DB outage cannot be fixed by a self-confirming LLM response. |
| Artifact storage | Owner-tagged namespaces for original evidence, derivations, trials and assessment artifacts. Immutable refs/hashes; authorized bounded readers. | DB/object inconsistency, orphan bytes and partial manifests. Use staged write/verify/commit protocol and recovery reconciliation. |
| Hosted/local model service | Read-only selected context with declared source rights; only C2/C4 and explicitly selected adapters call it under C0 budget. | Correlated hallucination, timeout, mutable aliases, unexpected usage. Preserve producer/version/usage; no store/action credentials or direct mutation authority. |
| Embeddings/text/graph projections | C3 model projection and C2 derivation outputs; rebuild from authoritative versions. | Stale knowledge, incompatible vector spaces, missed filtered neighbors. Namespace by model/revision, watermark and semantic cut; use exact/authoritative fallbacks where required. |
| Clocks and ID generation | Record physical/source/monotonic/simulation clocks explicitly; opaque scoped IDs. | Clock skew can leak future evidence into past decisions. Preserve known-at admission cut and uncertainty; reject unqualified comparisons. |
| External sources/search and action connectors | Explicitly configured rights, selection and usage; C1 acquires, C7 gates actions. | Missing coverage, biased exposure, report echoes and uncertain effects. Preserve selection lineage, declared gaps, receipt/effect separation and idempotency constraints. |
| Numerical/statistical backends | C5 isolated execution, C4 specialist proposal tools, C6 diagnostic adapters; exact capability/version manifests. | Unsupported semantics or unstable numerics can look like causal surprise. Validate capabilities before dispatch; retain numerical diagnostics and alternate-law checks. |
| Telemetry/backup | C0 operational monitoring and qualified recovery procedure. | Logs can omit client-visible failures; backups may miss object bytes. Record offered-work denominator and restore both storage domains. Operational telemetry is not domain evidence unless acquired and attributed as such. |

These are governed dependencies, inventoried separately from the eight application owners. Adding a separately administered stateful service reopens the component registry and pair/feedback review. Dependency paths may bypass a visually absent module edge; ownership checks apply at storage and adapter boundaries too.

## 8. Whole-system feedback review

The active software lanes form one strongly connected group through scheduling, read requests/results and proposal/assessment return paths. This does not imply that the modeled world is one undifferentiated feedback loop. The review must inspect the following composed failure paths:

- **Generated-evidence echo:** C4 proposal → C3 candidate → C5 simulation → C6 expectation/assessment → C4. Original C1 observation lineage is required before treating output as corroboration. Simulated data remain tagged through export/reimport and subsequent summarization. Common-source derivations remain one evidence group.
- **Time leakage:** source/model/assessment query → actor choice or prediction. A later report or revised model cannot be passed as available-at-t input. Selector cuts and actor masks travel with snapshots and evidence results.
- **Authority escalation:** inquiry or modeled policy proposal → C0 → C7. C0 can schedule review, but only C7's pinned action policy authorizes dispatch. Simulation success cannot authorize an external operation or policy amendment.
- **Saturation/deadlock:** committed intake event → queued interpretation → model/analysis → assessment → more inquiry. All queues are bounded; no owner holds a DB transaction or intake acknowledgement while waiting for a model, another owner or an external action. Worker exhaustion defers inquiry and exposes lag.
- **Correlated model consensus:** shared pretrained model/embeddings → several agreeing claims. Repetition is not independent support. Independent sources or prospective observations, plus selection/dependence checks, are needed for admission.
- **Revision cascade:** identity/rule/boundary correction → caches/scenarios/forecasts. Keep old forecasts scored under their original model; mark dependent current views stale; rebuild or explicitly re-evaluate without rewriting historical outcomes.
- **Selection bias:** current hypotheses choose observations → supportive retrieval → stronger confidence → narrower search. Preserve the unvisited frontier, rival predictions, null checks and independently reserved outcome windows. Report when chosen observations cannot distinguish models.

Cases in [VERIFICATION.md](VERIFICATION.md) and the matrix cover these paths. Pair completeness is only inventory evidence. Semantic correctness, crash recovery and scientific learning require actual pinned implementation runs.
