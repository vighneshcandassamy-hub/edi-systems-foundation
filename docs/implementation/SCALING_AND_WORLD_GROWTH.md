# Efficient operation, cumulative world growth and intrinsic inquiry

Version 0.2 extension, 20 October 2026. Input design revision: `2af45f59169ec3855f10a8861d6e6acc4c8cfb07`, draft PR #1. Status: proposed architecture and operating targets, not implemented or measured. It extends the eight logical owners and nine representation families; it adds no mandatory service or new ontology of world entities.

## 1. Assessment of the current design

The current architecture permits the requested growth: C1 can accept subsequent observations, C3 can revise and compose representations, C4/F43 maintains a cross-system inquiry frontier, and C6 can identify discrepancies and draft findings. IMP-R09, IMP-R18 and IMP-R28 already cover informative inquiry, cross-system expansion and relevant temporal depth. This makes the forest a starting scope rather than a permanent domain boundary.

It does not yet provide an executable near-instant operating path, a concrete incremental dependency-maintenance contract, an abstraction/refinement contract across scales, or a persistent lifecycle for requesting missing access. A Postgres schema and an instruction to be curious would not supply those mechanisms. This extension allocates them to existing owners and adds IMP-R29–IMP-R34 and prospective E41–E48 cases. All prior model scenarios remain unrun.

Three forms of scale are different: more stored history/referents; more input/query load; and more complex questions, coupling or resolution. Fast local work over a growing store is a specific goal. A global question or globally coupled change may require work proportional to much of the model. No constant-time claim covers every graph, cascade or new scientific discovery.

The model of reality grows; adding knowledge does not itself enlarge or change the external world. Distinguish discovery of a pre-existing relationship, new evidence about one, and an actual physical/institutional change.

## 2. Jev and the appropriate speed objective

The owner's reference is **TypeSafe AI's Jev**, not JEPA. The previous tradeoff package omitted this relevant candidate. JEPA latent predictive architectures remain a separate optional research family; they do not supply evidence for Jev's latency.

TypeSafe reports approximately 70–500 ms for selected System One queries and evaluates defined workflows. Its release notes qualify geography, short inputs and benchmark construction; the advertised multiples are not EDI measurements or universal service guarantees. Treat these as reasons to evaluate a fast decision adapter, not proof that a full expanding world model can reach a new validated conclusion in that time. [S52]

Jev is suitable for focused typed judgments: choose among candidate tests, classify a known situation or assess a specific criterion from compact supplied state. Its documented questions are independently evaluated against shared state, so independent questions can share one request. A dependent question still needs the earlier result and possibly a second request. A fixed answer space should include `other`, `insufficient_evidence` or an explicit abstention route when appropriate. [S53–S54, S56]

TypeSafe's Choice/Score confidence is a statistic derived from the output distribution. It is not an independent measurement of truth or proof that the candidate set includes the right mechanism. Measure calibration/selective error on EDI tasks, preserve unknown alternatives and validate deterministic constraints separately. Do not adopt marketing language about type safety as a guarantee of correct causal conclusions. [S55]

The inspected model documentation distinguishes versioned Jev releases and moving aliases. It lists 1.13 as the stable alias target and 1.14 as a newer preview candidate at retrieval time. Bind an explicit revision and requalify thresholds on upgrades; do not silently inherit calibration or latency. This assessment does not call the API or assume account availability. [S60]

| Operating path | Work | Preferred implementation | Latency meaning |
| --- | --- | --- | --- |
| Reused/deterministic | Read a valid local projection; apply a known rule, lookup or compiled model. | Indexed queries, bounded in-memory working view and prevalidated code/numerics. | Best candidate for tens-of-milliseconds response when workload, freshness and hardware permit. |
| Fast probabilistic decision | Make a focused judgment among known options from bounded current state. | Optional Jev adapter, or a qualified small local discriminative model; batch independent questions. | Sub-second end-to-end target for a defined request shape; network, queueing and state assembly count. |
| Deliberate inquiry | Create new hypotheses, seek sources, refine a model, diagnose a novel nonlinear transition or build a missing decision space. | Existing reasoning LLM and causal/simulation tools in a background job. | Seconds or longer with progress, cutoff and uncertainty; not represented as a completed instant discovery. |
| Evidence acquisition | Obtain a new measurement, experiment, record or access grant. | C1 acquisition plus C0/C7 request/rights lifecycle. | External latency may dominate; current knowledge can be returned immediately with explicit limits. |

The response deadline and the investigation completion deadline are separate contracts. An acknowledgement or an old cached answer does not satisfy a fresh validated-answer target. The fast path must return a useful result under an admissible freshness/domain policy, or an explicit pending/unsupported/uncertain result that counts as such.

Q1 assumes an already bound typed query or known decision template. Translating an unfamiliar free-language question, assembling missing evidence or generating a novel explanation has its own measured Q3/Q4 cost. A structured result or evidence-backed template can be rendered quickly; a token-generated essay is not free work outside the latency boundary.

## 3. Incremental updates instead of repeated global reconstruction

Preserve every admitted occurrence and interpretation as before. Convert a model update into a small, versioned `ModelDelta` carrying affected referents, changed assertions/mechanisms, time scope, evidence basis and correction lineage. C3 remains the sole model revision authority.

Maintain a reverse dependency index from source/claim/referent/mechanism to the projections, compiled models, aggregate interfaces, query caches and current decisions that depend on it. Invalidate only declared dependents first; preserve an explicit conservative invalidation region when dependencies are incomplete. Identity merge/split, interpretation correction and model-version changes must use the same machinery as numerical updates.

For each update:

1. C1 commits the occurrence/availability and an outbox event.
2. C2 performs available native decoding/feature updates and queues semantic interpretation where required; capture does not await an LLM.
3. C3 admits a candidate or justified model delta under its versioned policy, checks the base revision and records affected dependencies.
4. C3 invalidates affected current projections and updates bounded local derivations from the delta, with an applied-event ID and checkpoint committed consistently.
5. C5 reevaluates only eligible affected compiled models; cycles/shared constraints are handled as coupled components with their specified numerical semantics.
6. C6 records changed prediction/error implications without altering old forecast seals; C0 schedules deeper inquiry if needed.

Coalesce redundant pending refreshes to the newest target revision where semantics permit; preserve all underlying evidence and transitions. A deletion/correction needs retraction-aware recomputation, not an append-only running sum that leaves the old value counted. Deduplicate deliveries by request/event identity, not by deleting genuine repeated observations.

Acyclic small dependency closures can be cheap. Strongly coupled feedback groups, changed global inputs or a high-degree shared resource may invalidate a large region. Yield to a bounded background repair job, expose the invalidation/freshness watermark and prevent stale critical decisions. A queue cap is a scheduling boundary, not proof that distant effects are absent.

Initial storage choice remains Postgres plus application-owned incremental projection tables maintained through transactional/outbox contracts. Ordinary Postgres materialized views are stored query results refreshed with `REFRESH`; selecting one does not automatically implement continuous delta maintenance. [S59] Materialize/Differential Dataflow is a later streaming-join/aggregation alternative if measured update pressure justifies another governed dependency; it does not provide EDI's causal/admission semantics. [S57]

## 4. Bounded working context, caching and reusable decisions

Keep durable world state separate from the working context for one question. Resolve the query into relevant referents, their required interfaces, the chosen temporal cut, alternatives, active constraints and unresolved frontier. Do not serialize the entire world into a model call. Include missing or omitted influential paths explicitly; dependency selection is itself subject to evaluation.

| Reusable artifact | Required validity information | Reuse condition |
| --- | --- | --- |
| Derived state / query result | Source/model revisions, query/selector, known-at cut, dependency signature, projection watermark and completeness/freshness status. | Current dependencies and the caller's freshness policy permit reuse; otherwise recompute or disclose limitation. |
| Compiled mechanism/model | Model/grammar/compiler/backend versions, units, domain, history and numerical policy. | Same supported semantics and valid operating domain; a new regime or topology reopens compilation/qualification. |
| Decision template | Question/options/criteria versions, model revision, input feature contract, applicable domain, calibrated operating region and allowed action class. | Preconditions hold; deterministic permission/feasibility checks still pass independently. |
| Learned local surrogate | Training/evaluation source cuts, teacher and truth provenance, domain, uncertainty/abstention rule and drift monitors. | Held-out and changed-regime tests pass; do not promote teacher agreement to independent empirical truth. |
| Hierarchical summary | Aggregation semantics, population/scale, interface outputs, error/uncertainty characterization, validity and detail provenance/availability. | The query stays within the summary's tested domain and retained information is sufficient. |

Query and decision caches are governed projections inside existing owners, not a second world-model authority. A lookup key must include semantic/permission/time/model dependencies, not just similar wording. Repeated decisions may later be compiled into rules or small models after evidence supports generalization. Distillation is optional; it needs frozen data, complete cost accounting and failure/OOD tests before use.

Start with Python orchestration, prepared/indexed SQL, bounded I/O, batched arrays and supported numerical kernels. Profile copying, serialization, transactions and model calls before moving a hot kernel to another language. Rewriting the entire codebase in a lower-level language does not remove global rescans, remote inference or incorrect dependency semantics.

## 5. Expanding the world along four independent axes

| Growth direction | Forest example | Necessary contract |
| --- | --- | --- |
| Breadth / adjacent systems | Forest → logging firms → mills → furniture demand → trade and financing. | New referents and interface hypotheses, sources and boundary assumptions; retain unresolved return paths and affected parties. |
| Depth / decomposition | Budworm → life stages → feeding/reproduction physiology → biological mechanisms. | Composition/refinement links, distinct organism/cohort/species identities, native data, units/time scales and evidence. |
| Resolution / heterogeneity | Regional forest average → stand cohorts → individual-tree variation or local microclimate. | Aggregation/disaggregation and sampling assumptions; avoid applying a population mean as a known individual law. |
| Temporal refresh / history | Seasonal observations, delayed predation effects, old management choices and new resistance. | Valid/known time, model/regime versions, delayed commitments and retained history. |

New test cases are views over a shared evolving model. Bind their entities through supported identity/association evidence. The same mill or insect population can appear in multiple views without creating separate copies of its resources or history. Domain-specific data modules are adapters; they should not become isolated forests of unrelated memory.

An unfamiliar observation can remain unclassified or be attached to competing structures while inquiry continues. The existing nine families are structural priors; extend payloads/relations and schema versions when justified instead of forcing unknown content into a falsely precise stock-flow law. Record the cost and compatibility impact of any new representation operator.

## 6. Refinement bridges and summaries across scales

Introduce a proposed `RefinementBridge` record within C3. It relates coarse and fine views; it does not equate them. Required content:

- Parent/child view IDs and shared/aggregate referents; composition role and overlapping membership rules.
- Input/output interfaces, separate directed dependencies, exchanged quantity/meaning, units/scales and temporal alignment.
- Aggregation or transformation rule, conservation/counting applicability, initial/history/pending-state mapping and double-count exclusions.
- Assumptions, valid domain, uncertainty or explicit unknown error, fine-detail provenance/availability and update/refinement triggers.
- Model/bridge revisions and dependency signature; coarse/fine consistency check and the operation that activates a new resolution.

For the insect, internal biological hypotheses might affect survival, development time, feeding and reproduction. Those aggregate outputs influence a population mechanism; population/ecological conditions may in turn change individual conditions. The two directions need separately supported laws. No hormone, gene or biochemical mechanism is invented to fill a gap.

Use coarse descriptions while they answer the question within a justified applicability envelope. Refine when residuals, regime/domain changes, heterogeneous outcomes, sensitive decision thresholds or a discriminating test show that internal detail could matter. A detailed model may fail to improve prediction; retain that result. More detail is not automatically more truth or more intelligence.

Do not run every biological submodel for every timber-market query. Update the relevant aggregate interface when fine information changes it; invalidate downstream summaries when bounds or applicability break. Preserve access to detail and explicit losses, rather than pretending compression preserves every possible future question. Rare/extreme behavior and nonlinear aggregation deserve separate checks; averages can hide a tipping point.

## 7. Intrinsic exploration and access requests

This is a software policy with persistent state, triggers and outcome measures inside C0/C4/C6/C7. A prompt to “be curious,” a Markdown agent skill, or the count of generated questions is not its implementation.

Trigger candidates include: unexplained prediction residual; contradictory source; uncertain/high-impact interface; approaching a nonlinear threshold; old assumption needing refresh; insufficient resolution; a decision sensitive to an unmeasured quantity; or an adjacent system likely to change the answer. Periodic review can find dormant gaps, using a bounded rotating frontier rather than scanning every representation on every event.

The frontier distinguishes `expand_adjacent`, `refine_internal`, `resolve_identity`, `refresh_temporal`, `test_mechanism`, `check_boundary` and `review_abstraction`. Each item stores target/hypotheses, trigger, expected decision relevance, feasible evidence channels, estimated costs, alternatives and a stopping/review condition. Multiple hypotheses may share one data request; repeated missing links do not need repeated user prompts.

Where defended outcome probabilities and likelihoods exist, use expected information gain or value of information. Otherwise use an explicitly heuristic ranking of discrimination potential, consequence/relevance, confidence in the test's usefulness, acquisition feasibility and cost. Keep the terms separate and versioned. Jev may judge narrow criteria or select among proposed tests; its scores are not calibrated likelihoods of all unknown world mechanisms.

Proposed `KnowledgeRequest` fields: request/dedup ID, target and inquiry direction, specific unknown, rival predictions, why resolving it matters, requested data/source/sampling/time coverage, minimum useful evidence, current access/alternatives, expected benefit/cost, requested capability scope and retention, requester, policy/version, status, expiry/review trigger and eventual evidence/outcome links.

Lifecycle: `proposed → ranked → feasible_under_existing_access | needs_access → acquired | requested → granted | denied | deferred | expired → investigated → useful | inconclusive | disproven | superseded`. This is a state machine with guarded transitions, not a requirement to traverse every label. Granting access does not mean evidence was acquired; acquisition does not mean the hypothesis was confirmed.

Existing configured grants are reused within their scope. C0/C1 obtain already permitted data without repeatedly asking the user. Genuinely missing access is presented as one reviewable capability request through the existing C0/C7 policy path. A denial is retained and is not repeatedly re-requested without a materially changed need or scope. Requests are coalesced by target, unknown, capability scope and hypothesis family; expiry and cooldown suppress noise.

Proposed default discretionary notification budget: at most two new consolidated access suggestions per project/day and a seven-day repeat cooldown for materially unchanged requests. These are configurable user-experience settings, not scientific constants or automatic permission rules. Urgent findings follow a separately configured policy; the model cannot bypass the policy by calling every unknown urgent. Existing user authorization persists until changed or expired under its recorded scope.

Example request: “Current observations cannot distinguish climate-driven larval survival from food-quality effects. Development-stage records, local humidity/temperature and feeding measurements over the relevant spring interval could separate these explanations. Access to dataset X would let us test that distinction; we already have Y, which supports only a weaker comparison.” Do not promise a dataset exists or is accessible without checking it.

## 8. Ownership and interfaces for the extension

| Owner | Added specification within existing functions |
| --- | --- |
| C0 F00/F02/F03 | Fast/deep deadlines and reservations, inquiry scheduling, access-request aggregation/delivery and standing-grant reuse. |
| C1 F11/F13 | Delta/availability notifications, bounded replay and retained source identity; actual source acquisition after a supported request. |
| C2 F21/F23 | Compact evidence-qualified feature/interpretation updates; deterministic constraints and source grounding remain separate from fast probabilistic suggestions. |
| C3 F30–F33 | ModelDelta, reverse dependencies, retraction-aware projections, RefinementBridge and cache/view validity; sole canonical model authority. |
| C4 F40–F43 | Persistent multi-direction frontier, test ranking, optional fast decision adapter, independent-question batching and escalation for missing hypotheses/detail. |
| C5 F50–F53 | Reusable compiled models, coupled-region updates and coarse/fine analysis with explicit applicability and numerical limitations. |
| C6 F61–F63 | Calibration/selective error, inquiry yield, abstraction error, contradiction/recency triggers and prospective model-growth assessment. |
| C7 F70–F73 | Standing source/action scopes, access-request decisions and guarded fast execution; confidence never grants authority. |

The component registry stays at eight logical owners. All 56 lanes are re-reviewed, with affected operation/facet/verification allocations updated. Existing C0↔C4 lanes carry exploration work; C0↔C7 carry access-policy review; C0↔C1 carry permitted acquisition; C3 query/proposal lanes carry deltas, dependency/bridge requests and results. A grant result is not a new causal observation. Optional Jev is a governed model adapter inside existing boundaries; adding a separate administered streaming service would reopen the dependency/component review before adoption.

## 9. Proposed latency and growth qualification profile FAST1

FAST1 supplements DEV1; it does not weaken its durable-capture, source-integrity or recovery obligations. All settings are targets to validate on a pinned machine/version and realistic caller region. No result is measured in this task.

| Operation / workload | Proposed acceptance target | Boundary and limitations |
| --- | --- | --- |
| Q1 warm scoped read / known deterministic decision | p95 ≤100 ms; p99 ≤250 ms. | Useful result from caller dispatch through complete eligible response, including service/network hops and dependency/freshness/authorization checks on the pinned topology. No remote model required; no silent stale answer. |
| Q2 bounded local derived-model update | p95 ≤250 ms; p99 ≤500 ms. | Complete promised local projection update for a delta affecting at most 32 source/model records and eight registered derived views. Larger closures become explicit queued jobs; queue acknowledgement does not count as completed recomputation. |
| Q3 fast probabilistic selection | p95 ≤500 ms; p99 ≤1,000 ms, quality and abstention thresholds prospectively pinned. | One model request, at most 4k input tokens/16 independent questions, bounded state assembly and ≤128 referents/512 relation entries selected before tokenization. Network/queue/validation count; exceeding the shape triggers another profile or deliberate path. |
| Q4 novel model building / data acquisition | Separate completion metric, budget and progress contract. | No sub-second discovery promise. Return currently supported knowledge with cutoff/unknowns; measure time to an actually validated new answer separately. |
| Store growth test | 10,000 →100,000 →1,000,000 referents at fixed active work, input/query workload and hardware. | Four relation instances per referent for the initial synthetic fixture, plus mixed history; disclose realistic high-degree and coupled variants. Larger scales need another qualified profile. |
| Local growth stability | Meet Q1/Q2 targets; proposed p95 latency growth ≤3× between smallest/largest store at matched active work. | Record cache warm/cold behavior, query plans, actual bytes, touched dependencies, maintenance and all failures. Index/storage growth is still real. |
| Sustained work | DEV1 offered input plus 10 Q1 queries/s; Q3 requests are separately rate/budget limited. | No assumption that every one of 50 records/s gets a hosted decision; selective triggering/batching is part of the design. |
| Memory/storage | Working caches and queues stay within the pinned DEV1 allocation; durable evidence/model/lineage storage growth is measured separately. | “Bounded active memory” is not “constant total storage.” Compaction, reindex, retention and backup/restore costs count. |

Specify the fraction of requests eligible for each fast path and the fraction escalated, denied, stale, partial or unresolved. An apparent low-latency result that punts almost everything or omits disconfirming context fails useful-operation assessment. Measure required fresh behavior against an authoritative reference, not only cache speed.

Broad cascades and genuinely global queries are included as counterexamples: their work may grow with coupling or world size. They must surface honest backlog/freshness, preserve original evidence and prevent stale eligibility for consequential decisions. Parallel work, partitioning and approximation can help only under a qualified correctness/applicability contract.

## 10. Long-term physical scale strategy

Index first for workspace, source/epoch, referent, time/revision and reverse dependency access. Use prepared bounded queries; store large native artifacts outside rows. Partition immutable occurrence/history by useful time/source/workspace keys when actual size and query patterns justify it. PostgreSQL partitioning prunes physical data by compatible predicates; it is not automatic graph sharding or a proof of low latency for all joins. [S58]

Partition canonical entities by explicit ownership/key, with cross-partition relations referring to the same identity. Do not assign a separate physical copy for every domain view. Track hot shared referents (climate, prices or a common supply resource), coalesce invalidations and qualify global-change propagation. A distributed cut must declare consistent snapshot/version/watermark semantics; local acknowledgement is not universal graph convergence.

Separate hot current projections and frequent compiled models from warm histories and colder native artifacts. Keep source and forecast holds/rare important evidence according to an explicit policy. Compression records losses and invalidates unsupported inference; raw removal must remain visible through availability tombstones. Retention budget decisions cannot manufacture knowledge that was never acquired.

Independent read replicas/projections and worker pools can scale queries or processing; a write/admission bottleneck or high-degree dependency may require a changed partition strategy. Add a broker/streaming engine or compiled native kernel only after profiling a stated bottleneck. Requalify recovery, cost and semantics with each topology change. This is an evolution path, not an unlimited-scale assurance.

## 11. Prospective extension cases

| ID | Case | Acceptance |
| --- | --- | --- |
| E41 | Incremental correctness and locality under store growth. | At the FAST1 sizes, delta/retraction and incremental views match a separately recomputed authoritative reference for the same cutoff; record actual touched work and warm/cold latency. Q1/Q2 and growth targets apply only to their declared operation shapes. |
| E42 | Fast decision quality, batching and escalation. | Compare Jev, deterministic and appropriate small/generative alternatives on matched bounded contexts; pin selective error/calibration and coverage before exposure. Include missing correct option, dependence between questions, OOD inputs and timeouts. No model output bypasses deterministic constraints. |
| E43 | Global fan-out and stale-cache containment. | A high-degree/shared driver invalidates all declared dependents; bounded processing exposes remaining backlog. A warm stale cached result cannot be silently returned as fresh or used beyond its permitted policy. |
| E44 | Coarse/fine abstraction and nonlinear aggregation. | Refinement bridges preserve units, time, identity, resource/count semantics and commitments. Demonstrate valid coarse reuse and a counterexample where heterogeneity/thresholds require refinement; compare supported output ranges. |
| E45 | Missing access, standing grants and request fatigue. | Reuse an existing scoped grant; create an evidence-specific missing-access request; coalesce duplicates; honor denial/expiry; enforce notification policy and record useful/inconclusive acquisition outcomes. |
| E46 | Breadth and depth expansion in one evolving world. | Start with forest observations, add an adjacent logging/market view and internal insect-life-stage evidence without resetting history or duplicating shared referents/resources. Retain unsupported biological mechanisms and update only justified bridges. |
| E47 | Long-running growth, corrections and maintenance. | Reconnect sources, revise identity/rules, compact/reindex, retain/evict evidence and recover a pinned model cut while the store grows. Bound active memory/queues and count full maintenance/storage costs and unavailable evidence. |
| E48 | End-to-end useful speed and inquiry yield. | Measure capture/model freshness, eligible useful response latency, validated-answer time, escalation coverage, exploration benefit and complete cost under FAST1/DEV1. Include correct abstention and failed inquiries; an acknowledgement-only or omission-driven speedup does not pass. |

All eight cases are specified, not run. No performance or discovery advantage is established by this document. The initial source/identity/time contract increment should include dependency/delta/validity and KnowledgeRequest fields now so later growth does not require a semantic rewrite. Begin with a small fixture, then qualify growth and latency independently of narrative examples.
