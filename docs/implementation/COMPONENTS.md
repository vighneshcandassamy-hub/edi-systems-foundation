# Component specification and implementation allocation

Version 0.1, 20 October 2026. Status: implementation-architecture proposal. All endpoints, packages and records below are proposed; there is no EDI runtime behind them yet. [TRADEOFFS.md](TRADEOFFS.md) gives alternatives and reasons. [CONTRACTS.md](CONTRACTS.md) defines shared contracts; [TRACEABILITY.json](TRACEABILITY.json) gives stable allocations and cases.

## 1. Source precedence and scope

Pin input repository revision `830b6ee5384b1c9a6cbd723f94cb8bd5bb3e353a`. Preserve the integrated seven-chapter architecture and appendix reference byte for byte. This package operationalizes them under the owner's current instruction to use existing LLMs. The supplied overview is preserved in [OVERVIEW.mmd](OVERVIEW.mmd); it complements the detailed 82-node conceptual master rather than replacing it.

The older observation/substrate plans and skill reference to `edi-lab` are historical discovery pointers. The current work and state authority are this repository. No old runtime is imported or qualified, and no old file is silently rewritten. Source-native intake remains distinct from learned interpretation. Initial use of pretrained LLMs is permitted; prior-free semantics is not an implementation gate.

There are three different system boundaries to keep explicit:

1. The world being investigated, including humans, institutions, ecosystems and physical mechanisms.
2. The analyst's model, including alternative explanations, simulated trajectories and uncertainty.
3. EDI's software, including jobs, databases, model calls, authorization and telemetry.

A modeled sensor failure is not the same object as a failed EDI worker. A modeled actor's goal is not automatically EDI's goal. A causal edge is not an RPC endpoint. Each representation records which boundary it belongs to.

## 2. Logical modules and state ownership

| ID / proposed package | Responsibility and owned state | Main techniques | Mandatory exclusion |
| --- | --- | --- | --- |
| C0 `edi.inquiry` | Questions, modeled/evaluative scope, job state, scheduling budgets, workflow decisions and findings delivery. | Typed specs, durable state machine, Postgres jobs/outbox. | Cannot declare a claim true or directly modify another owner's state. |
| C1 `edi.observe` | Source registry, source epochs, immutable occurrences, byte manifests, native payload references, acquisition cursors and receipt/coverage status. | Extensible source adapters, content addressing, transactional metadata and artifact durability protocol. | No forced semantic interpretation, identity guess or synthetic outcome promoted to observation. |
| C2 `edi.interpret` | Derived decode/feature artifacts, term mappings and candidate entity associations, with exact producer/model versions. | Native parsers, Docling, selected multimodal model, deterministic units and conditional linkage/embedding adapters. | Derived text, semantic similarity and source descriptions are proposals, not independent facts. |
| C3 `edi.world` | Canonical referents, nine-family representations, mechanism and hypothesis membership, model revisions, temporal assertion history and accepted-for-use decisions. | Postgres typed core/JSONB, append-only revisions, explicit validation, rebuildable graph/text/vector projections. | No destructive rewrite of acquired evidence; no universal scalar truth score. |
| C4 `edi.reason` | Inquiry frontier, candidate explanations, rationale summaries, proposed tests and structured discovery sessions. | One replaceable LLM, bounded tool loop, candidate discrimination; optional causal/system-identification tools. | May propose model/experiment changes; cannot execute external actions or admit its own claims as independently established. |
| C5 `edi.analyze` | Immutable analysis specifications, compiled mechanism artifacts, numerical/qualitative runs, scenario and prediction artifacts. | Restricted mechanism IR, SciPy first; conditional PySD/SimPy/Mesa and statistical adapters. | Trial state cannot overwrite operational or observation state. Unsupported dynamics fail explicitly. |
| C6 `edi.assess` | Sealed expectations, outcome correspondence, error records, calibration/diagnostic results and justified revision recommendations. | Prospective comparison, source-independence analysis, hypothesis tests, uncertainty diagnostics and optional drift/calibration tools. | Cannot revise earlier expectations, change acceptance thresholds after outcomes or count generated echoes as corroboration. |
| C7 `edi.agency` | Actual EDI authorization/adoption policy, permitted command lifecycle, execution receipts and operational policy versions; interfaces for modeled actor-policy interpretation. | Versioned rules, capability checks and constrained planner adapters when needed. | No external actuation in initial research mode; no automatic adoption from an LLM recommendation. |

These are logical state owners, not eight mandatory processes. The smallest deployment is one application plus a durable store and artifact directory, with independently bounded intake, model and analysis work queues. Blocking inference/numerics run outside the intake loop. Each owner exposes a typed port; shared storage does not grant cross-owner write access.

The full all-pair inventory is [INTERFACES.json](INTERFACES.json). Its explicit reverse lanes represent independent operations or results, not symmetric privileges. Shared dependencies and indirect feedback are reviewed separately in [CONTRACTS.md](CONTRACTS.md).

## 3. Functions and node coverage

Every overview node is allocated in `TRACEABILITY.json`. The table below is the readable allocation. World-model content, including actor and capability content, is always retained by C3; listed modules own processing. Example mechanisms below are proposed implementations, not conclusions about a particular forest or household.

| Diagram nodes | Processing responsibility | Proposed functions and invariant |
| --- | --- | --- |
| Q, B, V | C0 with C3/C6 | F00 define inquiry; F01 scope causal and evaluative boundaries; F02 schedule; F03 deliver supported findings. Keep question, whose interests count, resolution and horizon distinct. |
| O, R | C1 | F10 receive; F11 preserve and attribute; F12 replay/select; F13 manage capacity and recovery. Preserve actual occurrences even when payload bytes repeat. |
| ME | C2 with C3 | F20 decode; F21 qualify identity/meaning; F22 derive retrieval features; F23 submit source-linked claims. Unknown time/identity/units remain unknown. |
| M, ORG, IF | C3 | F30 instantiate/compose; F31 transact revisions; F32 expose scoped views; F33 maintain/rebuild projections. Interfaces include direction, roles and authority without inferring causal sign. |
| ST, FL, LAW, TM, LIM, FB | C3/C5 | Persist quantities, multi-input laws, pending state and constraints; compile only supported dynamics. Loop views reference existing mechanisms and add no extra force. |
| CD, SUP, RP, GE, CH | C3/C5 with C7 where actual adoption is involved | Describe condition, dependencies, restoration resources, variation/selection and actual organizational transitions. Repair can fail; structural change is different from analyst revision. |
| HY, LEV, TRAP | C4 | F40 propose rivals; F41 investigate mechanisms; F42 rank tests; F43 expand cross-system frontier. Eight traps are mechanism templates to challenge, not classification truth labels. |
| SC, AN, PR, BH, OUT | C5 with C6 | F50 compile; F51 execute; F52 sensitivity/uncertainty; F53 explain conditional trajectories. Separate assumed drivers, realized behavior and consequences under stakeholder criteria. |
| ER, CMP, REV | C6 | F60 seal forecasts; F61 compare independent evidence; F62 diagnose discrepancies; F63 recommend retain/revise/reject/investigate. Preserve the original standard and forecast. |
| SE, PE, FR, GO, PI, INT, EX | C7/C3/C5 | F70 expose actor-specific information; F71 assess intended actions; F72 authorize/execute where permitted; F73 adopt owned policies. Domain actor knowledge cannot include the analyst's hidden global state. |
| PM, PP, AU, AD | C7/C6/C3 | Monitoring, policy amendment proposal, legitimate authority and actual adoption are separate transitions; declined/deferred proposals remain inspectable. |

## 4. C0 — inquiry and operations

Inputs: a task or background inquiry policy, available source/rights inventory, model/query selectors, stakeholder criteria and an operating profile. Outputs: a versioned inquiry, bounded work requests, traceable findings and explicit blocked/partial/deferred states. Persistent state: workflow event, parent task, leases, attempts, budget reservations/settlements, source frontier and delivery deduplication.

Functions F00–F03 choose scope without rewriting evidence, distinguish causal boundaries from evaluative interests, prioritize feasible work and assemble final/proactive findings with limits. A broad mission permits observing without a question; it does not authorize unbounded crawling, external actions or indefinite recursion.

Job lifecycle: `proposed → admitted → queued → leased → running → succeeded | partial | failed | cancelled | uncertain_completion`. A lease includes a monotonically advancing fence for writes by its owner. A worker that lost its lease cannot commit another result. Separate retryable transient failure from a deterministic unsupported model. A result for an idempotent completed request returns the original result; a different payload under the same key is a conflict.

Preferred implementation uses one Postgres job/outbox schema alongside owner-isolated domain schemas. A committed intake notification cannot synchronously wait for an LLM. Scheduling reserves scarce tokens/work before dispatch and settles actual usage afterward; missing usage is unknown, not zero. Notifications carry references, not repeatedly embedded source documents. Optional FastAPI endpoints wrap the same ports; a web service is not necessary to validate the first path. [S13, S49–S51]

Failure behavior: continue admitted native intake while reasoning is unavailable within the configured spool limit; surface freshness lag; defer lowest-priority inquiry first; stop admission honestly when finite storage is exhausted. Jobs do not hide an outage by falling out of the denominator. C0 records application health separately from modeled domain conditions.

## 5. C1 — observation and evidence

Inputs: configured source-native chunks/objects and source context. Outputs: durable occurrence receipts, payload manifests, gap/coverage markers, bounded record selections and explicit unavailable status. Persistent state has independent identities for source handle/epoch, occurrence and payload. Source and subject/referent are different: a camera can observe many trees; many sources can mention one tree.

The long-lived source registry retains owner/provider namespace, native source identifier, authenticated binding basis where available, epoch/reset/replacement history and validity. A returning source with a supported continuity record reuses the association; a similar appearance does not prove it. An element's physical continuity is a C2/C3 hypothesis if the source does not identify it directly.

Admission separates transport validation, storage and interpretation. Large media/arrays use bounded chunks and manifests. Composite parts retain order and selectors. Keep text encodings, array shape/dtype, coordinates, symbolic score syntax, audio/video timestamps and stream identities where supplied. New or unknown media can be retained while the interpretation adapter is absent. The adapters cannot physically observe beyond their configured interfaces.

Durability protocol: write bytes to a staged artifact, compute/check its hash and byte count, make the artifact durable under the selected profile, then commit the occurrence/manifest and an outbox notification in one DB transaction. A DB reference must not acknowledge a blob that has not reached that profile's durability level. Recovery detects staged orphans, missing artifacts and incomplete manifests. There is no assumed atomic transaction spanning arbitrary object storage and Postgres.

Read/replay selects by workspace/source/epoch/time/cursor and returns occurrence identities, provenance, bytes or references, continuation cursor, gaps and retention status. At-least-once source delivery is allowed; duplicate notification is not duplicate physical observation. Backpressure, retention and loss semantics are explicit in the selected operating profile.

## 6. C2 — interpretation and entity correspondence

Inputs: C1 references, parser/model configuration, optional read-only C3 correspondence context, and a declared inference budget. Outputs: versioned derivations and candidate claims with spans/regions/time selections. Persistent derived artifacts include the exact input identities/hash, decoder/model settings and transformations. One transformation is not a new independent source.

A claim records its descriptive role (`event`, `state_sample`, `rate_sample`, `pattern`, `structure`, `mechanism`, `purpose`, or unclassified) independently of evidential basis (`measured_or_inspected`, `reported`, `inferred`, `assumed`, `unknown`). Structure may be observed directly; an event may be only reported. Multiple compatible tags are allowed with rationale; the classifier need not force every sentence into one box.

Meaning records retain original wording/symbol, proposed referent, quantity/units, scale type, aggregation, time and applicability. Use dimensional checks for cardinal quantities. Do not numerically average ordinal categories or convert a missing value to zero. Mathematical structure, spatial regions and musical sequence can remain native structures rather than prose. Pint helps with unit arithmetic; it cannot decide whether a source used a term correctly. [S45]

Entity linking proposes a continuity/association basis, alternatives and contradictions. Exact source bindings, supporting identifiers, temporal compatibility, structured linkage, text/visual evidence and negative constraints have different strengths. Keep `same_payload`, `same_source`, `mentions_same_entity`, `possible_same_physical_referent`, `part_of` and `replacement_of` distinct. Reject naive transitive closure of uncertain links. A merge is a versioned association decision with a reversible mapping and dependent-view invalidation, never deletion of old evidence.

Submit candidates to C3; syntactic validation may reject malformed proposals, while semantically undecidable proposals remain candidates. Store LLM-only proposals as imported assistance even if plausible. Unavailable context produces partial/unknown output, not fabricated knowledge.

## 7. C3 — shared representation and substrate

Inputs: attributed candidate claims, explicit changes, evidence selectors, and scoped read requests. Outputs: immutable model snapshots, typed views, admission decisions, conflict reports and invalidation events. Persistent authority is the versioned model; projections and embeddings are caches.

| Family | Minimum payload beyond common identity/provenance/time/status | Critical check |
| --- | --- | --- |
| System view | Boundary, purpose of view, level, resolution, horizon, included/excluded referents, external drivers/sinks and closure assumptions. | A former driver cannot also be counted as its newly internalized cause. |
| Constituent | Roles, membership, composition, condition, lifecycle and shared dependencies. | Overlapping views reference one underlying referent. |
| Stock | Quantity kind, units/scale, value/history or unknown, initial basis, inflow/outflow references, bounds and reserve/access distinctions. | Accumulation accounting; “important” does not imply a numeric stock. |
| Flow/process | Source/destination roles, affected quantities, conversion/loss, rate/time basis, rule and prerequisites, resource use and completion/pending semantics. | One realized transfer affects all participants consistently. |
| Information/influence link | Sender/recipient, direction, channel or physical dependency, meaning, availability/receipt/attention, distortion and uncertainty. | A published signal is not necessarily perceived or acted on. |
| Response relationship | Role-indexed joint inputs/outputs, equation/rule or unresolved explanation, parameter values/domains, delays, capacities and alternatives. | N-ary dependence and nonlinear applicability; no unexplained edge coefficient. |
| Function/purpose/reference/criterion | Distinct role, attributed owner, stated/inferred basis, calculation, horizon, conflicts, feasibility and normative scope. | A desired target is not an achieved outcome or every actor's goal. |
| Feedback path | Ordered references to mechanisms, closure evidence, conditional sign, delays, shared resources and applicability. | Closed path and polarity are separate; do not count the path as extra dynamics. |
| History/conditional trajectory | Referents, time/units/aggregation, initial state/history, policy/model versions, driver assumptions, run identity, horizon and uncertainty. | Observation, forecast and simulation retain distinct origin. |

Representation operations: instantiate, link, compose, retire, split/merge association, rewire proposed organization, branch model, admit/reject/retain a claim and expose bounded views. All mutations include base revision and operation type. C3 validates references, state transition authority, temporal meaning and conflicts; it commits a new revision with rationale. Actual structural change, changed actor policy and analyst correction have separate operation types. State carry-over includes pending orders/repairs, stocks, cohorts and membership changes.

Use relation instances with participant roles for multi-input laws and multi-party exchanges. Store a binary projection for graph traversal when useful, with an explicit pointer back to the originating mechanism; do not treat it as a complete law. A mechanism can be descriptive, qualitative, executable or unsupported. Accepted-for-use is a scoped modeling decision, not a universal truth label.

Time has at least valid interval, source event/measurement time when supplied, received/known-at time and internal commit/revision time. Preserve clock basis and uncertainty. Multi-record changes use one local transaction and an optimistic base-revision check; stale proposals are rejected or explicitly rebased and re-reviewed. Postgres MVCC alone does not implement semantic bitemporality. [S13]

Source occurrence references and original forecasts remain stable. Corrections append supersession/contradiction/interpretation relationships. Retention tombstones and unavailable data propagate through dependent assertions and analysis eligibility. Index rebuild cannot silently reintroduce retired interpretations or mix embedding spaces.

## 8. C4 — reasoning and inquiry development

Inputs: a scoped question or background trigger, C3 snapshots, C1 evidence, C6 error assessments and budget. Outputs: candidate model patches, alternative hypotheses, experiment designs, boundary expansion proposals and qualified rationale summaries. It owns no accepted world-model state.

F40 creates candidates with explicit support and rivals. F41 questions mechanism existence, direction, units, delay, domain, hidden inputs, alternative causal stories and omitted interfaces. F42 chooses informative and feasible inquiries. F43 expands the system-of-systems frontier based on relevance, uncertainty, predicted impact and costs, preserving deferred/unknown interfaces. The reasoning model proposes; deterministic code checks references and permissions; actual observations and qualified tests determine admissibility.

Candidate hypothesis minimum: explanatory claim, represented mechanisms and scope, evidence/dependence list, assumptions, counterevidence, discriminating predictions, expected observation channels, possible confounders, applicability and status. Include measurement/reporting change, selection effects, unknown drivers and no-effect alternatives where credible. An LLM's confidence label is not a calibrated posterior.

Initial search is bounded and serial by default. A concrete development profile permits at most three rival candidates per expansion, two revision rounds before yielding and one model call concurrently; see [VERIFICATION.md](VERIFICATION.md). These are proposed operational ceilings to prevent runaway work, not limits on what a system can ultimately learn. Additional work is queued with an explicit reason. No fixed Five Whys depth is required when evidence runs out earlier.

Tool outputs are typed, provenance-linked records. Retrieval failure is distinct from no evidence existing; an empty result set after an approximate query is not universal absence. A hypothesis that cannot yet be numerically simulated can still generate a qualitative observation request. Identifiability failures preserve competing structures and state what observation could separate them.

## 9. C5 — analysis and conditional dynamics

Inputs: pinned C3 snapshot, `ScenarioSpec`, initial state/history, actor information masks, driver/intervention schedule, analysis method and budget. Outputs: `RunRecord`, predictions with correspondence and uncertainty, trajectories, conservation/feasibility diagnostics and supported/unsupported status. It owns simulation state only.

Compile a restricted mechanism representation, not arbitrary LLM-generated Python. Supported operators initially include typed arithmetic, bounded lookups and declared stock/flow dependencies. The compile gate checks units, referenced roles, required history, equation/rule domains, capacity/accounting constraints, allowed operations and backend capability. Implementation must pin the actual grammar and reject unsupported operators before a contract pass. A qualitative unknown is legal model content but not a numeric executable law.

Source equations and appendix numerical reproduction ambiguities retain their original statement and status. Competing corrected/alternative formalizations receive separate versions with rationale and evidence; the compiler must not silently repair a source equation and label it the author's exact model.

For continuous models: explicit ODE state, valid initial conditions, parameter domains, output intervals, solver, tolerances, discontinuity/event policy and numerical diagnostics. For fixed delays: retain input history and declare interpolation/initial-history semantics or use an equivalent pipeline approximation with error qualification. Native arbitrary-delay support is not promised by `solve_ivp`.

For discrete models: specify queue membership, pending commitment identity, cancellation, ordering, resource acquisition/release and event tie rules. For hybrid models: one clock and atomic transfer semantics across solver/event boundaries. For algebraic cycles or DAE systems: declare the needed solver and consistency initialization or return unsupported. Topology changes transfer state using a versioned mapping; never initialize away inconvenient backlog.

Actor simulation uses only received/available observations and its own memory/policy at time t. Execution uses the actual modeled constraints and can fail even if the actor expected success. Separate local outcomes from consequences through wider interfaces, other stakeholders and later horizons. Keep terminal obligations beyond the reporting horizon visible.

The eight trap analyses reference candidate constituent paths and necessary conditions. Several can coexist; a name is not a diagnosis. Leverage points reference targets and directions, implementation authority, timing, resources and competing criteria; Meadows' ordering does not supply a universal ranking of beneficial interventions.

## 10. C6 — evidence comparison and model learning

Inputs: a forecast registered before its selected outcomes become available, independent outcome selections, correspondence definition, held-out cut and evaluation criteria. Outputs: signed/dimensional errors, proper scores when applicable, alternative error explanations, confidence/coverage limitations, a revision recommendation and a finding draft.

Forecast registration seals model/policy/driver versions, assumptions, cutoff, output variables, horizon and evaluation rule. Later correction creates a new forecast with its own timestamp; the original remains scored. Comparison checks source dependence and generated lineage, available-at time, units/aggregation, missing/censored outcomes and selection/exposure. An evidence group derived from one source does not count as several corroborators.

Diagnose observation error, semantic misalignment, numerical error, unexpected drivers, wrong parameters, wrong rule/topology, changed policy and non-identifiability separately. A lower prediction error on the fit window does not by itself choose between observationally equivalent structures. Revision recommendation states affected claims and descendants, retained rivals, remaining uncertainty, expected benefit and new verification burden.

C3 owns admission; C6 recommends it with evidence. Any policy amendment then follows its separate owner/authority path through C7. Data selection, calibration and acceptance are pinned before evaluation. Drift detectors can request investigation, not silently reset history or normalize away failure.

Proactive finding minimum: newness/priority basis, affected party/goal/horizon, causal or associative chain with status, support/counterevidence, alternatives, uncertainty, suggested test/action class and expiry/review trigger. C0 controls delivery and deduplication under a configured channel. Strategic usefulness is an outcome to evaluate, not simply the count of generated insights.

## 11. C7 — policy, intent and adoption

Inputs: attributed actor model state for simulation, an authorized EDI policy version, action proposals, adopted update decisions and connector configuration. Outputs: intended-action records, authorization/refusal/defer decisions, dispatch/receipt status and policy-adoption history. The canonical model representation remains C3-owned; actual runtime execution policy is C7-owned.

Separate five mechanisms: ordinary action under fixed policy; parameter change within policy; proposed policy amendment; authorized/adopted new policy; analyst revision about what policy an external actor uses. Model these as distinct versioned operations. Original goals and evaluation standards remain available after change.

Research mode permits internal read-only tools and declared simulations. External acquisition selection must be within configured source rights; physical/financial/message actions require a separate authorized profile. A model recommendation cannot grant itself that profile. Tool contracts distinguish attempted operation, external acknowledgement and subsequently measured effects; unknown completion is reconciled before a potentially duplicative retry.

Repair and reorganization of the investigated system use explicit mechanisms, shared budgets and timelines in C3/C5. Repair and failover of EDI's own software use C0's operational profile. Neither implies guaranteed resilience or infinite repair support. Goal, rule or interface changes include actor ownership and resource/implementation constraints rather than automatic acceptance.

## 12. Proposed package and deployment evolution

Future code layout: `edi/{contracts,inquiry,observe,interpret,world,reason,analyze,assess,agency}`, with `adapters/{sources,models,parsers,analysis,storage}`, SQL migrations and one focused integrated campaign. `contracts` holds shared record definitions, not a new state owner. Dependencies point through owner ports. Parser/model/backend adapters implement versioned capabilities and failure outcomes.

Initial deployment: local development application, Postgres and an artifact directory with verified backups/replay. Hosted model access avoids requiring a local GPU; offline mode uses a separately qualified adapter. The current Windows Python 3.14 installation is not evidence that every planned ML library supports it. Select and lock a compatible Python/dependency set at contract implementation; isolate model serving if it needs Linux/GPU-specific packages.

Scale in measured stages: partition occurrence metadata by workspace/source/time; store large artifacts outside transactional rows; rebuild derivative indexes; add bounded workers; isolate hot-source queues; add replicas and object redundancy under a named HA profile. Introduce a graph service, event broker or orchestration cluster only after a requirement and measured trigger justify it. No capacity profile covers arbitrary world-scale data.

## 13. Requirement and evidence status

Traceability flows mission → EDI system requirements → I7/appendix and retained layer obligations → implementation requirement → function/module → contract → prospective case → evidence. `TRACEABILITY.json` preserves original requirement rows alongside allocations rather than changing their meanings. It also covers the observation consumer obligations and every overview node/edge.

[VERIFICATION.md](VERIFICATION.md) states profile targets, acceptance designs, failure modes, KISS/Five Whys review, unresolved choices and gates. Proposed contracts require concrete schemas/fixtures and pinned dependencies before a contract pass. Model calls, production uptime, learned transfer and scientific advantage remain not run. The specification is intended to be reviewable before any runtime implementation begins.
