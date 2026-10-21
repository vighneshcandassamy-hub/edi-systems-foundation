# C4 bounded reasoning and exploration — first source increment

Later source handoff: app code 0.7.0 wires the native [C6 assessment](C6_ASSESSMENT_RUNTIME.md) selection/inquiry-review facade. This supersedes the earlier unavailable-query subset below only for that endpoint; native student/teacher inference and all qualification remain open. Original C4 episode/protocol semantics remain preserved.

Code **0.5.0**, input `11e3517544b78a79e6fc73b81c2345723f67b14c`. Status: **partial source implementation; runtime and scientific qualification deferred**. This increment supplies the inquiry structure and integration. It does not run a reasoning model or establish discovery, causal accuracy, scalability or speed.

## Authorities and requirement cascade

The [v0.8 master](../../architecture/world-model/Meadows_EDI_Integrated_Architecture_v0_8.md), [appendix semantics](../../architecture/reference/Meadows_Appendix_187_203_Semantic_Foundation_Reference_v1_0.md), [component specifications](COMPONENTS.md), [reasoning integration](REASONING_INTEGRATION.md), [growth policy](GROWTH_POLICY.json), [contracts](CONTRACTS.md) and [directed interfaces](INTERFACES.json) govern this increment. The [tools/math reference](ARCHITECTURE_TOOLS_AND_MATH_REFERENCE.md) distinguishes selected preferences from conditional methods. The 98-node/286-edge architecture, eight owners, 32 functions, original 34 implementation requirements and 48 cases are unchanged.

[C4_RUNTIME_TRACE.json](C4_RUNTIME_TRACE.json) maps the scoped C4 requirements through existing IMP parents and F40–F43 to source and future cases. [ADR-006](../decisions/ADR-006-bounded-reasoning-control.md) records the implementation choice. The [source review](evidence/c4-source-review.json) applies the component and interface skills, with all 56 directed lanes accounted for. It is an implementer self-review, not independent acceptance; overall verdict remains **revise**. All wider C1–C3 requirements remain open as previously recorded.

## Structure, functions and ownership

| Part | Function and reason | Source |
| --- | --- | --- |
| Typed inquiry/context | C0 supplies question, purpose, boundary, horizon, pinned world revision, explicit source ranges, selected protocol axes, unknowns, omitted frontier and budgets. An explicit cut prevents silent scope creep and retrospective evidence substitution. | `contracts.py`, `service.py` |
| Context assembly | Read-only C1 occurrences/ranges and C3 revision-pinned records/dependency views; provenance, origin class, event/report time and commit time survive. Whole selected objects get a hash check; partial ranges retain the parent digest and exact selector. | `Reasoning.investigate` |
| Systems protocol, F41 | Eleven selectable question axes question mechanisms/interfaces, first principles and uncertainty. Why/what-if prompts stop at missing evidence; no arbitrary mandatory depth of five. | `protocol.py` |
| Inquiry controller, F40–F42 | Persist jobs before export; import attributed structured candidates; retain rivals, assumptions, confounders, applicability, counterevidence and conditional predictions. Teacher critique remains fallible feedback. | `step`, `export_job`, `import_response` |
| Test design, F42 | Structured observation/qualitative/numerical test proposals state rival differences, channels, feasibility, confounding, cost/risk and identifiability limits. C4 emits C0 outbox items; C5 execution is future work. | `InquiryTest`, `OutboxItem` |
| Exploration frontier, F43 | Seven growth directions and eight triggers; preserve pending/deferred/denied/resolved unknowns. Rank open work with a declared deterministic heuristic. Explicitly retain other/unvisited frontier. | `FrontierItem`, `update_frontier`, `rank_frontier` |
| Episode journal | C4 owns a separate lazy SQLite database. Transactional optimistic sequence changes, immutable command outcomes, current episode projection, retries, one unresolved-job reservation and bounded quotas support later recovery verification. | `sqlite.py` |
| Candidate bridge | C4 stages the exact C3 patch before submission and records the receipt afterward. C3 retries resolve lost C4 receipts. C4 cannot accept, reject or retire world records. | `build_patch`, `submit` |

All paths above are under [src/edi/reason](../../src/edi/reason/). The controller does not invent a hypothesis when no response exists: inquiry state is ready, awaiting response, round complete or yielded. Records say whether a proposal was human authored or imported model output. These are not demonstrations of endogenous discovery.

## Meadows protocol coverage and limits

The protocol is a versioned **engineering interpretation**, not a new extraction or proof that every sentence of the book is implemented.

| Selected axis | Concepts it asks the proposer to consider |
| --- | --- |
| Evidence | Events versus patterns versus structure/mechanisms, identity, units, timestamps, source dependence and measurement change. |
| Boundary | Purpose, resolution, horizon, omissions, internal/adjacent/temporal exploration and incoming/outgoing interfaces. |
| Organization | Elements/composition/hierarchy, support dependencies, directed interfaces, why relationships exist and alternatives. |
| Accumulation | Stocks/flows, units, initial history, buffers, resources, limits and pending commitments. |
| Feedback/delay | Complete return paths, conditional polarity, sensing/attention/actuation, delay, loop dominance and oscillation. |
| Nonlinearity | Domains, saturation, thresholds, bottlenecks, interacting limits, hysteresis and changing regimes. |
| Agency | Information/perception/purpose/incentive/policy/intent/execution distinctions, bounded rationality, confounding and authority. |
| Resilience/evolution | Buffers, diversity, redundancy, maintenance, shared support, self-organization, hierarchy and tradeoffs. |
| Rivals | Credible no-effect, reporting, selection and unknown-driver alternatives; support/counterevidence and discrimination. |
| Intervention | Conditional traps/leverage hypotheses, information/rules/goals/frames, spillovers, delay and implementation. |
| Learning | Preserve expectations, uncertainty and error; select feasible discriminating observations and state stopping conditions. |

Axes are explicitly selected per inquiry. Prompting about a mechanism does not discover or validate it. The protocol does not implement differential equations, system identification, biological inference, trap detection or every leverage-point experiment. Those need C5/C6 and evidence. Pretrained knowledge and authored assumptions remain visible priors; this is not a semantic-neutral or bias-free system.

## Student, teacher and bounded control

The saved preference remains a pretrained instruction/reasoning **student served by vLLM** and a selectively used pretrained **teacher**, with fixed weights initially. vLLM is an inference engine. Exact checkpoint/revision, tokenizer, provider and hardware remain unbound. `ModelBinding` snapshots those future choices and allows only fixed weights in this increment. No vLLM package, network client, model or provider credentials are installed or loaded.

Jobs are export-only work reservations, not executed calls. `export_job` separates control instructions/schema from untrusted source data and includes the pinned context and retained response history. `InferencePort` documents the future dependency; the provided student/teacher adapters raise explicit unavailability. Configuring a model name does not activate inference. Native gateway dispatch, tokenization/context-window admission, deadlines, provider idempotency, bill reconciliation and model-output capture into C1 remain open.

For structural development, C0 can import a human-authored proposal. External model output requires an exact model binding/revision matching the job and an attribution. An unbound job cannot be presented as output from an actual model. This source-level check does not cryptographically verify the claimed author/provider.

The initial hard structural bounds are three candidate rivals per student round, two student rounds, at most four student/teacher jobs, and one unresolved exported job per workspace. Teachers require a declared novelty/unresolved/consequential/student-escalation trigger after a completed student round and share its exact evidence cut. They can supply critique only, with retained/challenged/deferred disposition; they cannot add world evidence or directly edit hypotheses. A student revision uses a new immutable hypothesis ID and preserves the original.

Each job conservatively reserves its entire input/output token cap from the inquiry budget. Reservations are never refunded on missing usage or cancellation. Reported usage is attributed, not provider-certified. Exceeding a reported cap is rejected for explicit external reconciliation. Actual inference cost and concurrent external dispatch cannot be guaranteed by an export-only controller. An unresolved job survives restart and blocks another reservation until resolved or explicitly cancelled; no automatic model retry occurs. Cancellation keeps an unknown-usage marker and yields. Exhausted round/job/token reservations produce a durable yield instead of further work.

## Interface and integration specification

| Directed lane | Implemented subset | Explicit remaining work |
| --- | --- | --- |
| C0 → C4, IF-04A | Typed investigate/step/frontier-update, scoped reads, status and outbox acknowledgement in the trusted local SDK/CLI. | Durable C0 scheduler, fairness, periodic review/notifications and policy-driven activation. |
| C4 → C0, IF-04B | Durable candidate/test/frontier/access-proposal outbox linked to episode artifacts. Acknowledgement records C0 receipt/disposition only. | Automatic delivery, scheduled C1/C5/C6 work and effect/result reconciliation. |
| C4 → C1, IF-10B; C1 → C4, IF-10A | Existing operation-restricted read facade; selected occurrence metadata/native byte ranges and original provenance. Unsupported media stays metadata-only. | Native multimodal reasoning and isolated decoders; access grants remain C0/C7 responsibilities. |
| C4 → C3, IF-15B; C3 → C4, IF-15A | Pinned query/get/dependency view, exact staged candidate patch and receipt. Existing references require selected explicit versions; intra-patch references may resolve post-patch. | Dedicated ModelDelta/refinement subscriptions, actor-view policy, incremental context refresh and fine-grained validity certificates. |
| C4 ↔ C6, IF-19A/B | Explicit unavailable assessment query; C0 may import attributed, unverified assessment notes in an inquiry. | Native assessment selection, inquiry-yield/calibration review and measured feedback. |

C4 never calls C2, C5 or C7 directly. C0 can orchestrate C2-derived C3 context, schedule C5 tests or request C7 access decisions. No cross-owner SQL, C1 evidence mutation, action execution, external notification, grant, training/adoption or hidden deployment is introduced. All 28 pairs/56 direction dispositions remain unchanged. Logical bidirectionality does not imply symmetric authority.

The shared eleven contract facets apply with these C4 overrides: ownership/authority are allocated above; concrete shapes use strict frozen records/schema `1.0` with extra fields rejected; compatibility/migration remains explicit future work; identity uses workspace/occurrence/source/epoch plus exact selectors; time/order uses original source times, pinned world revision and local episode sequence; delivery uses namespaced command fingerprints and original outcomes; commit/recovery uses journal/projection transactions plus staged C3 receipts; retention is finite append-only with no eviction policy installed; resources are bounded as below; errors use shared unavailable/unsupported/denied/conflict/capacity/integrity/storage/unknown-commit codes; grounding separates source/generated/simulation lineage, authored/imported hypotheses and teacher critique. Future adapters must satisfy each facet before a contract/runtime PASS.

## Evidence, hypothesis and patch constraints

Every source reference in imported hypotheses/candidate changes must match an exact selected C1 reference, including workspace, digest, selector, origin and lineage. Source text may be evidence for what a source reports, not an independent observation proving its assertions. World candidates carry their existing admission state and dependency warnings into the context. A depth-limited or stale dependency view remains visibly incomplete. Imported C6 notes are attributed unverified summaries, not certified assessments.

Hypothesis and test IDs are immutable across rounds. Tests may discriminate retained or new hypotheses. Proposed world writes belong to a current student hypothesis, have `basis=hypothesis`, and contain no admission. Existing edits must match a selected base version; dependencies point to selected pinned records or explicit post-patch candidates. C3 still enforces base revisions, references and its candidate policy. Successful persistence is not scientific acceptance. C4 never silently rebases a stale explanation; C0 must start a fresh inquiry/cut with linked history if its world has changed.

The context hash binds the bounded world/evidence/dependency cut; the episode separately preserves inquiry purpose, horizon, unknowns, imported notes, protocol questions, bindings and profile. There is no automatic cache of valid conclusions and no freshness certificate. `rank_frontier` returns the pinned revision/hash, unvisited scope and a requirement for C0 to refresh validity before scheduling.

Frontier dedup uses target, unknown, normalized capability scope and hypothesis family. Identical proposals do not issue another outbox message. Denied/resolved work can reopen only with a new material-change rationale. Permission grants are never inferred from capability scope. The growth policy's two discretionary requests/day and seven-day unchanged cooldown are **C0 notification-policy proposals**, not falsely claimed as installed by C4. No notifications are emitted here. This source increment keeps whole finite episodes; cumulative graph projections/refinement/federation remain future adapters.

## Operating envelope and recovery

Defaults: request 256 KiB, context 128 KiB, episode 1 MiB, 128 frontier items, 256 retained outbox items, 16 staged submissions, 10,000 episodes, 50,000 journaled commands and 512 MiB conservatively accounted JSON storage. One in-process operation slot and one cross-process unresolved-job reservation per workspace; SQLite writer timeout five seconds; context checks use a cooperative ten-second budget. These are finite local limits, not guarantees of process isolation, strict wall-time termination, physical database/WAL size, distributed high availability or almost-instant reasoning. No latency/throughput/token-efficiency result is measured.

The journal retains immutable command-result snapshots and a current episode projection in one local transaction. A repeated operation/request ID with the same request/semantic profile/protocol/implementation returns its original snapshot, which may be older than current state; `get` reads current state. Changed input or model binding under that identity conflicts. Operational storage/byte/time limits may be changed explicitly to recover capacity without changing the model binding or original inquiry budget; the original profile and each committed transition's operating profile are retained. Optimistic sequence checks protect concurrent writers; query current state after a conflict. Request status is namespaced by operation. An unknown local commit is reconciled through original command status/retry. Quotas do not delete prior alternatives or reclaim acknowledged messages silently; if a finite episode fills, C0 needs explicit capacity adjustment or a continuation/retention policy. A physically full disk still requires operator repair before another durable transition.

Outbox references contain the producing `artifact_sequence`; `get(inquiry_id, sequence=...)` or `reason-get INQUIRY --sequence N` retrieves the immutable artifact cut even after a frontier disposition changes. Acknowledgement preserves that reference and records a local receipt rationale, without claiming execution.

C3 submission is two phase: stage exact patch locally, propose through the candidate port, save receipt locally. A crash or quota failure after C3 commits leaves the stage available for an exact retry; C3 returns its original receipt even if the current head has advanced. There is no distributed transaction, exactly-once network claim, complete restore/retention or migration/failover implementation. Authenticated multi-user access and actor-specific context policy remain open; this is a trusted local composition SDK.

## Source review: rationale, simplicity and failures

Five Whys: retain an episode because reasoning must be revisitable; revisiting needs the original expectations and cut; those need pinned evidence/model versions; pinning needs owner-provided immutable records; therefore C4 references C1/C3 and journals its own proposals rather than copying authoritative state or letting a model admit itself.

Requirements cascade (waterfall assessment): system purpose → IMP requirements → F40–F43 → typed functions/interfaces → bounded persistence → specified future failure/scientific cases. Source allocation does not imply a finished runtime gate. MECE is used as an audit aid: context, questioning/proposals, discrimination, exploration, state/recovery and authority/resources are separately allocated; coupled mechanisms and unknowns stay linked. The eleven axes are overlapping inquiry lenses, not a claim that reality is a MECE partition.

KISS choice: one controller, one typed contract module, a small protocol catalogue and one local owner store; existing C1/C3 facades are reused. No multi-agent framework, second world graph, speculative math dependency, new service owner or automatic weight-update path is added. The immutable episode snapshots are deliberately simple but consume more journal space than deltas; hard bounds and later adapter replacement are explicit.

Critical findings repaired in source: restrict response evidence to the pinned cut; reject model-output attribution on unbound jobs; isolate teacher critique; forbid unselected dependencies and self-admission; keep an unresolved reservation durable; preserve unknown usage on cancellation; retain denied/deferred frontiers; stage cross-store submissions before side effects. No claim is made that prompting guarantees correct hypotheses, that exported source content cannot influence a future model, or that software graph connectivity proves domain causation.

| Failure/condition | Effect and detection | Containment/recovery | Future case |
| --- | --- | --- | --- |
| Wrong source/epoch/range or stale dependency cut | Contaminated explanation; scope/hash/identity/dependency checks expose mismatch or incompleteness. | Reject mismatches; preserve dependency limitations; request a new cut if needed. | C4-V001/002 |
| Untrusted source instructions or teacher agreement | Misleading hypothesis or self-confirmation; no native model isolation is established. | Separate exported control/data, retain origin/critique status, forbid teacher world edits; future gateway/evaluator must test resistance. | C4-V003/005/006 |
| Duplicate work, unknown external completion, concurrent writers | Repeated cost/effects or lost state; fingerprints, pending-job reservation and episode sequence detect conflicts. | Return original outcomes, retain reservations, explicitly cancel/yield and reconcile externally. | C4-V004/011/015 |
| Full queue/disk or slow owner read | Cannot advance; explicit capacity/storage error or cooperative deadline. | Preserve earlier state, reject admission, let C0 narrow scope/continue later; physical disk/HA remains open. | C4-V013/016 |
| C3 committed but C4 receipt lost | Uncertain local submission completion. | Retry exact staged patch under original C3 request ID; no silent rebase. | C4-V012/018 |
| Frontier update overwrites earlier proposal or denial repeats | Wrong work scheduled or repeated access pressure. | Versioned outbox cut, immutable journal, dedup and material-change reopening; C0 rate policy remains future. | C4-V010/014 |

## Usage assets and deferred verification

[Examples](../../examples/reason/README.md) are authored instructions/templates, not executed demonstrations. Generated schemas are under [schemas](../../schemas/). CLI commands: `reason-investigate`, `reason-step`, `reason-get`, `reason-export-job`, `reason-import-response`, `reason-frontier-update`, `reason-rank-frontier`, `reason-outbox-ack`, `reason-build-patch`, `reason-submit`, `reason-status`; optional `--reason-config` selects the fourth owner database/profile. C1 commands and capabilities do not instantiate C4 or load models.

Checks performed: Python AST parsing, application imports, CLI parser construction, JSON/TOML parsing, new Markdown link targets and schema generation from model classes. These are source/artifact checks only. **No Runtime/store instance, example, product test, review-gate validator, qualification case, model call, benchmark, simulation, training or deployment ran.** Runtime crash/retry/quota/concurrency behavior and scientific reasoning are specified but unrun. The next source owner is C5 analysis; native C4 inference/gateway selection remains an explicit prerequisite for autonomous reasoning, independent of building that owner next.
