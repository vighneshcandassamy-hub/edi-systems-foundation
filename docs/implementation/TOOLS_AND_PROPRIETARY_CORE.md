# Ecosystem tools, mathematical foundations and the proprietary core

Version 0.3 research extension, 20 October 2026. Input: `7b9c9f3bbf19bef6947fac4db271de8e805d207e`. Scope: implementation choices and prospective qualification, not a runtime build. This document supplements [component specifications](COMPONENTS.md), [contracts](CONTRACTS.md), [tradeoffs](TRADEOFFS.md) and [scaling and world growth](SCALING_AND_WORLD_GROWTH.md). The seven-chapter master and appendix remain unchanged authorities. Eight logical owners, 32 functions, 34 implementation requirements and 48 prospective cases are retained.

## 1. First-principles verdict

Build EDI's original representation, revision, mechanism-compilation, inquiry and cross-scale coordination code; reuse mathematical solvers, persistence, parsing, pretrained models and development infrastructure behind replaceable adapters. A pretrained model can propose a mechanism; an equation fit can suggest dynamics; neither grants the proposal independent evidential support. No reviewed tool supplies the complete EDI capability.

The elementary operations are: preserve an observation; attribute its meaning and referent; propose a structural account; derive consequences under conditions; compare with independent evidence; revise a scoped account; and choose the next informative feasible inquiry. Software ownership follows those operations rather than a product catalogue. The design must retain unknowns even when a tool insists on complete numerical inputs.

Three materially different alternatives were considered:

| Whole-system approach | Strength | Principal limitation for this mission | Decision |
| --- | --- | --- | --- |
| LLM plus retrieval/graph memory | Fastest route to source-grounded question answering; valuable comparator. | Retrieval and fluent explanation do not provide stock/flow execution, identification, prospective forecast integrity or cross-scale accounting. | Keep as a matched baseline and optional retrieval adapter. |
| Entirely custom learned world model and foundation model | Maximum control over objectives and representation; potentially reusable learned dynamics. | Requires training data, compute, evaluation and an open-ended representation-learning solution before ordinary capabilities work. | Research option; no mandatory initial training. |
| Entirely custom database, agent runtime and numerical solvers | Control over implementation details. | Recreates mature machinery while the main uncertainty is whether EDI learns useful structures. | Reject as the initial architecture. |
| Custom semantic/evidence/dynamics core with established numerical and model adapters | Explicit history, mechanisms, uncertainty, testing and domain expansion; can replace individual tools. | More design work than a chatbot; scientific benefit still needs evidence. | Preferred. |

Structural priors remain: identity, time, composition, quantities, interfaces, search grammars and pretrained knowledge. First-principles development makes these assumptions inspectable; it does not eliminate all priors. Mathematical sophistication is useful when it solves an identified failure more efficiently or accurately than a simpler method.

## 2. Priorities and the smallest credible starting stack

- **P0 — first integrated capability:** needed for one useful end-to-end fixture, including correctness and observability from the beginning.
- **P1 — intelligence development:** add a specialist when the fixture needs its mathematical capability; develop these within the same world model.
- **P2 — measured scale/availability:** adopt after a declared load, latency or resilience requirement justifies added infrastructure.
- **P3 — research:** evaluate on a frozen problem after simpler approaches expose a relevant shortfall.

P0 is a small modular Python application with Pydantic contracts, Pint quantity checks, Postgres, a native-artifact store, one reasoning-provider adapter, NumPy/SciPy numerical execution, durable SQL job/outbox records, pytest/Hypothesis and OpenTelemetry-compatible measurements. uv, Ruff and Pyright support development. There is no requirement to install every tool below. A known test can begin without embeddings, a graph server, local GPU serving or agent frameworks.

The Python version is an implementation binding decision. The installed Windows Python 3.14 does not establish compatibility of the scientific/ML stack. Resolve and lock a supported interpreter and package set; separate Linux/GPU or Julia workers when their dependencies conflict. uv workspaces share a lockfile and environment assumptions, so incompatible ML environments should remain separate rather than forcing them into one workspace. [S61]

## 3. Component-level build, reuse and alternative decisions

Tool capabilities below are drawn from the primary-source register. Preferences, priorities and adoption triggers are EDI engineering judgments. T01-T24 are machine-traced in [TOOLS.json](TOOLS.json), including upstream requirement/function/case links.

| ID / priority | Capability and initial preference | Alternatives and their tradeoffs | EDI code to own / adoption trigger |
| --- | --- | --- | --- |
| T01 / P0 | C0 scheduling: small explicit state machine, bounded workers, Postgres jobs/outbox and checkpoints. | LangGraph for branching agent execution; Temporal for durable distributed workflows. Both require careful replay, external-effect and version semantics; they solve different parts of the runtime. [S20-S21] | Inquiry budgets, priority, cancellation, retry/idempotency and progress meaning. Add a framework when custom branching or recovery complexity is measured. |
| T02 / P0 | C1 capture: native bytes/chunks, hashes, manifests, source/epoch registry and append-only occurrence metadata. | Single verified artifact directory for DEV1; managed object storage with independent durability/retention controls for HA. | Source continuity and receipt/commit/replay rules. No native evidence capture should wait for an LLM. |
| T03 / P0 | C2 interpretation: native text/CSV/JSON adapters, Docling for supported documents and FFmpeg for media plumbing; model interpretation only where needed. [S07-S08] | Provider multimodal models for difficult content; custom sensor/symbol/music/scientific-array adapters for native forms. No parser covers every possible meaning. | Selector/provenance mapping, event/structure role versus evidential basis and unknown-format preservation. Docling's video transcription does not itself interpret every visual event. |
| T04 / P0 | C2 identity: exact supported bindings and reversible association records; Splink for a structured-linkage candidate. [S09] | Embedding/vision linkage proposes candidates; manual references help development but cannot become hidden ground truth. | Same-source versus same-referent versus same-payload distinctions, contradiction handling, merge/split and invalidation. Similarity never directly merges canonical identities. |
| T05 / P0 | C3 persistence: Postgres typed tables plus extensible payloads, SQLAlchemy and Alembic. [S12-S13, S49-S50] | Neo4j for graph-heavy traversal; RDF/SHACL for semantic interoperability; each adds mapping and operational costs. [S18-S19] | Versioned temporal relation instances, role-indexed participants, admission, alternatives and evidence lineage. Postgres MVCC is not semantic bitemporality. |
| T06 / P0 | C3 growth: application-owned incremental projections, reverse dependency indexes and retraction-aware deltas. | Materialize for sustained streaming joins/aggregations; it introduces another governed service. [S57-S59] | Dependency signatures, stale-result policies, coarse/fine invalidation and repair watermarks. Move only when measured maintenance pressure justifies it. |
| T07 / P1 | C2/C3 retrieval: bounded structural/lexical queries first; pgvector plus a qualified embedding adapter when semantic recall is needed. [S10-S11, S14] | GraphRAG, LightRAG and Graphiti accelerate graph retrieval/memory integration. They do not replace EDI evidence admission or executable mechanisms. [S15-S17] | Query-context selection, access/time cuts, missing-frontier disclosure and retrieval evaluation. Source-backed claims survive replacement of embeddings or retrieval frameworks. |
| T08 / P0 | C4 deliberate proposal: one replaceable reasoning adapter, initially GPT-6.1 Sol as a cost/quality development candidate. [S01] | GPT-6 Astra, Claude Opus 5.5/Fable 5.1, Gemini 3.8 Flash, Qwen3.5-9B/Qwen3.6-35B-A3B and DeepSeek-V4 are task/deployment alternatives, not an established ranking. [S01-S06] | Hypothesis records, evidence selection, bounded revision and tool routing. Pin exact provider settings; choose using held-out mechanism and grounding tasks, not general leaderboard position. |
| T09 / P1 | Focused decisions: optional Jev adapter after task calibration; deterministic known rules are the cheaper initial baseline. [S52-S56, S60] | Small local discriminative/rule models; a generative model at bounded effort. Compare useful decision quality, coverage, uncertainty and complete latency. | Option-set completeness, abstention, escalation, permissions and applicability. Jev does not generate an unrestricted new mechanism space. |
| T10 / P0 | C5 dynamics: restricted mechanism representation compiled to NumPy/SciPy; choose a supported ODE solver and explicit event/history rules. [S26] | PySD imports established stock/flow models; SimPy handles discrete events; Mesa supports agent-based models. [S25, S27-S28] | Compiler, unit/accounting checks, common clock, pending-state transfer and supported/unsupported semantics. Do not build a novel ODE integrator first. |
| T11 / P1 | C5 advanced dynamics: add SUNDIALS IDA when actual models need algebraic constraints; JAX/Diffrax when repeated differentiable/stochastic solves justify them. [S64, S69, S76] | CasADi for differentiable optimization/control; Modelica for equation-based model interchange. These may require different model encodings. [S74, S81] | Backend capability declarations and semantic lowering; no claim every backend supports arbitrary delay, hybrid topology or DAE initialization. |
| T12 / P1 | C4/C5 mechanism discovery: compare simple response laws and PySINDy on suitable measured dynamics. [S31] | PySR searches symbolic expressions more freely; neural dynamics can fit complex functions with weaker direct interpretability. [S68, S64] | Candidate grammar, units, shared constraints, evidence tests and transfer checks. Equation recovery requires sufficiently informative measured variables; sparse form is an assumption. |
| T13 / P1 | C4/C6 causal assessment: DoWhy for explicit assumptions, identification and effect-estimation checks. [S30] | Tigramite for lagged/time-series structure proposals under algorithm-specific assumptions; causal inference under interventions may be preferable when feasible. [S29] | Hypothesis-to-data correspondence and retention of observational equivalence. Graph direction and time order do not establish an identified causal effect. |
| T14 / P1 | C5/C6 parameter uncertainty: PyMC for readable local Bayesian models and posterior-predictive assessment. [S32-S33] | NumPyro for JAX-based inference; sbi when a simulator is available but likelihood evaluation is impractical. [S65-S66] | Parameter/structural/measurement uncertainty distinctions, convergence diagnostics and scoped model alternatives. No universal posterior over all conceivable world structures is claimed. |
| T15 / P1 | C5 sensitivity: finite perturbation checks first, SALib Morris/Sobol methods when a scoped uncertainty model warrants them. [S67] | Analytical/local derivatives with SymPy/JAX; scenario ensembles for discontinuous or multimodal behavior. [S70, S76] | Select domains, dependency assumptions, thresholds and stakeholder-relevant outputs. Sensitivity is not causal identification. |
| T16 / P0 | C6 evaluation: sealed forecasts, independent outcomes, errors/proper scores and versioned comparison rules. | MAPIE/conformal prediction for qualified prediction intervals; River drift detectors for investigation triggers. [S42-S43] | Evidence independence, scoring cuts, discrepancy diagnosis and revision recommendations. Drift does not identify its cause; coverage assumptions can fail across regime changes. |
| T17 / P1 | C0/C4 curiosity: own persistent frontier, rivals, feasible tests and explicit relevance/cost ranking. | BoTorch for expensive parameterized numerical experiment optimization; information-gain/RL objectives are later bounded research alternatives. [S36, S41] | Breadth/depth/refinement/access lifecycle, stopping and inquiry yield. A novel observation with large random noise need not be informative. |
| T18 / P0 | C7 policy and action: explicit versioned policy/state machine, deterministic rights/feasibility and idempotent connector dispatch. | OR-Tools for discrete allocation; CVXPY for compatible convex planning; CasADi for supported continuous nonlinear control. [S37-S38, S81] | Proposal/authority/adoption/effect distinctions and actor information masks. Optimization cannot invent legitimate goals or authority. |
| T19 / P0 | Shared contracts: Pydantic strict validation and Pint; explicit tagged unknown/unsupported states. [S44-S45] | Plain dataclasses plus hand validation for minimal internal records; Z3 only when a nontrivial logical invariant justifies it. [S71] | Semantic validation, compatibility and invariants. Well-typed JSON or satisfiable constraints do not establish real-world correctness. |
| T20 / P0 | Development: uv, Ruff, Pyright, pytest and targeted Hypothesis state-machine tests. [S61-S63, S78-S79] | Existing unittest or a different type checker are adequate if they check the same obligations. Coding assistants help implement/review bounded changes, with tests and source review retained. | Domain contracts, independent reference fixtures, replay/failure cases and versioned decisions; no automated inference superiority from passing unit tests. |
| T21 / P0 | Measurements: OpenTelemetry-compatible spans/metrics and explicit per-run model/solver/resource records. [S48] | Local JSON/SQL summaries initially; a hosted trace/evaluation platform later if operationally justified. | Measure end-to-end tail latency, freshness, eligibility, failed work, token/compute/cost and restoration. Trace text is not independent scientific evidence. |
| T22 / P2 | High-volume analysis/hot kernels: SQL and NumPy first; Polars or DuckDB for suitable columnar/offline analysis. [S72-S73] | JAX compiled arrays or Rust/PyO3 for a profiled kernel; NetworkX for small reference graph algorithms, not the whole durable world in RAM. [S76-S77, S83] | Dependency closure/graph projection/bridge kernels with conformance references. Avoid duplicate authoritative stores and benchmark cold compilation/copies too. |
| T23 / P1 | Internal biology extension: import only supported SBML models through libRoadRunner after model/source qualification. [S75, S80] | Own supported population/cohort laws can be sufficient; a generic simulator with explicit biological mechanisms remains an option. | Map biological outputs into existing RefinementBridge contracts. A biochemical model does not by itself predict whole-insect/ecosystem response. |
| T24 / P3 | Learned reuse: distill proven recurring decisions or optimize a bounded reasoning program using DSPy. [S24, S84] | Local rules/compiled models first; Dreamer/V-JEPA-style latent models for separately qualified action or perceptual domains. [S39-S40] | Keep teacher lineage, independent outcomes, OOD/abstention and replacement checks. No early training of an entire foundation model or inference loop that rewrites its own acceptance criteria. |

P0 priority does not imply every named alternative is mandatory. For example T19 selects Pydantic/Pint initially, not Z3; T20 selects development tools, not a new hosting platform. Candidate versions, dependencies, model weights and service capabilities are unbound until implementation qualification.

## 4. The mathematical core we can implement ourselves

These are standard foundations and proposed EDI combinations, not claims of newly invented mathematics or validated novelty. Reuse reliable libraries to execute them while owning the model grammar, lifecycle and decisions about when they apply.

### 4.1 Typed temporal relation instances and compositions

Represent a mechanism as an attributed relation instance with multiple participant roles, directed information/transfer ports, valid/known times, equations/rules or unknown content, applicability, evidence, assumptions and alternatives. A binary graph is a useful traversal projection; it cannot express every joint response law. Overlapping views reference one referent and do not duplicate stocks.

We can own composition and refinement operators. Internally acausal algebraic constraints may require a simultaneous solve; do not pretend a solver's computational ordering proves physical causation. Modelica is an interoperability reference for equation-based composition, not a requirement to translate the entire qualitative world into it. [S74]

Implementation: C3 retains canonical data; C5 lowers a supported submodel into an explicit intermediate representation (IR). An adapter reports supported operators, units, state/history requirements, clock, numerical precision and failure outcomes. The IR is an EDI-specific contract and compiler boundary; SymPy or another symbolic engine is a backend, not the canonical authority.

### 4.2 Conditional dynamics, accumulation and stochastic observations

For a supported continuous submodel, use a general schematic form:

\[
\dot x(t)=S v(x(t),u(t),h_t;\theta,H)+b(t),\qquad
y_k=g(x(t_k),\phi_k;\theta,H)+\epsilon_k.
\]

Here x is stock/state, v process rates, S the declared process-to-stock accounting map, u drivers/policies, h retained delay history, b boundary terms, H a structural hypothesis, and g the observation/sampling model. S is not assumed to conserve every quantity: conversions, losses and external exchanges need explicit accounting. Observation noise, missingness and selection differ from actual process variability. Qualitative concerns remain representable without being forced into this numerical form.

Start with declared response laws and robust parameter fitting where appropriate. SciPy least_squares offers bounded nonlinear residual fitting, but its local minimum and the fitted parameters do not establish structural truth. [S82] Defer stochastic/DAE/delay backends until their operator and initialization semantics are supported. Numerical tolerance/refinement, events, conservation, negativity and pending commitments need explicit tests.

### 4.3 Parameter learning, structural alternatives and model criticism

Within a declared candidate model family:

\[
p(\theta,H\mid D)\propto p(D\mid\theta,H)\,p(\theta\mid H)\,p(H).
\]

This is useful only where prior/likelihood/data-dependence assumptions are specified. C1/C2 provenance must prevent duplicate derivatives of one source from multiplying support. Missing alternatives stay on the frontier. Use candidate scores/sets when a defensible cross-structure posterior is unavailable; label LLM plausibility as a proposal score rather than a posterior.

PyMC is the readable first Bayesian candidate; NumPyro is an alternative when differentiability and repeated JAX workloads justify compilation. sbi can approximate simulator-parameter inference, but a misspecified simulator or prior can still produce a misleading posterior. [S32-S33, S65-S66] These are offline/background activities, not default work for every observation.

### 4.4 Discovering response laws rather than guessing all coefficients

One candidate SINDy-style objective is:

\[
\min_\Xi\;\|\dot X-\Theta(X,U)\Xi\|_W^2+\lambda\|\Xi\|_1.
\]

The dictionary Theta, measured coordinates, derivative estimates, weighting W and regularization are assumptions. Constraints can exclude dimensionally invalid or impossible candidates. PySINDy provides established identification methods; PySR explores symbolic expressions under a chosen operator/complexity search. [S31, S68] Neither recovers an arbitrary hidden ecosystem from a few events. Noisy derivatives, missing drivers, feedback/confounding and insufficient excitation require alternatives or abstention.

EDI can contribute a unit-aware, interface-aware candidate grammar, local search around discrepant mechanisms, and transfer tests across regimes. Prefer existing optimizers initially. A new search algorithm is justified only after a reproducible failure of the best relevant comparator; publish its assumptions and complete compute cost.

### 4.5 Nonlinearity, delays and regime changes

Nonlinearity is a property of a response law/domain, not merely a label on an edge. Test saturation, thresholds, hysteresis, interactions, shared capacities, stochastic drivers and delays with controlled scenarios. Local Jacobian eigenvalues near a supported equilibrium characterize local linearized behavior under its assumptions; they do not prove global stability for hybrid, delayed or changing systems.

Use finite perturbations, scenario sweeps and supported sensitivities; SALib provides Morris/Sobol and other sensitivity methods. [S67] Preserve dependencies among uncertain inputs; independent-input sensitivity formulas cannot silently absorb correlations. Compare coarse versus refined models near thresholds. Continuation/bifurcation or reachability tools are possible future specializations when a specific claim requires them, not mandatory initial services.

### 4.6 Curiosity as epistemic discrimination

For a defensible candidate distribution and feasible observation a, a possible criterion is:

\[
\mathrm{EIG}(a)=\mathbb E_{Y_a\mid D,a}
\left[\mathrm{KL}\big(p(H,\theta\mid D,Y_a,a)\;\|\;p(H,\theta\mid D)\big)\right].
\]

This targets uncertainty reduction within a model family, not all unknown reality. Check access, ethical/operational scope, time and resource feasibility before ranking. Where decision consequences share a defensible utility scale, value of information can be compared with acquisition cost. Otherwise retain separate discrimination, relevance, feasibility and cost criteria rather than adding incomparable numbers into a falsely precise score.

An explicit heuristic with a preserved unknown frontier is preferable to invented probabilities. BoTorch can help optimize an expensive numerical experiment inside a specified search domain; it does not construct the whole domain or infer legitimate intervention authority. [S36] C4 creates/ranks candidates, C0 budgets work, C7 handles rights, C1 acquires evidence and C6 evaluates yield. Positive entropy/noise induction alone is not a learning objective.

### 4.7 Adaptive resolution and efficient incremental reasoning

Own the dependency graph between evidence, assertions, mechanisms, refinement bridges, projections and decisions. An admitted delta invalidates its declared dependents; a changed hypothesis can require topology changes rather than parameter adjustment. Corrections retract obsolete contributions and preserve original evidence/forecasts.

A refinement policy compares coarse/fine output differences and decision sensitivity over declared domains; it can keep a cheap summary, refine internal detail, or expand an external boundary. Bounds may be statistical, numerical or explicitly unknown. A small fitted error on the training trajectory is not an error bound for unseen regimes. Deterministic summary validity and resource accounting belong in EDI; kernels can later be compiled.

JAX can compile supported array programs; shape changes and compilation warm-up matter for an evolving graph. [S76] Rust/PyO3 can implement a profiled graph/serialization kernel. [S77] Neither language removes high-degree global coupling. Apply FAST1 to complete useful operations, including context, copies, queues and validation.

## 5. What should be proprietary, and what that means

| Candidate original EDI asset | Why it matters | Initial implementation and evidence obligation |
| --- | --- | --- |
| Representation/admission kernel | One cumulative world with contested mechanisms, time, identity and composition. | Original C3 code over ordinary persistence; prove reversibility, traceability and shared-resource accounting. |
| Mechanism IR and compiler | Turn supported system descriptions into consistent conditional predictions. | Original restricted grammar, checks and backend lowerings; compare reference models and reject unsupported operators. |
| Revision/dependency kernel | Incorporate new/corrected observations with bounded affected work and honest stale status. | Original delta, dependency, projection and repair logic; compare against full recomputation including global cascades. |
| Cross-scale refinement coordinator | Link insect biology, populations, forests and economic views without duplicating reality. | Original bridge lifecycle/applicability tests; demonstrate when detail helps and when it does not. |
| Inquiry/access policy | Explore relevant adjacent systems or deeper internal mechanisms on purpose. | Original frontier, feasibility, ranking and deduplication; evaluate useful discrimination and complete acquisition cost. |
| Learning and reuse controller | Retain useful mechanisms and notice invalid transfer. | Original evidence-gated reuse/revision; test unfamiliar regimes with reset, unrelated-memory and strong baselines. |

Original source code can be a private project asset while depending on established tools. That is separate from a novel scientific contribution, patentability, and ownership of third-party models/data. The table is an engineering ownership plan, not an IP clearance opinion. Record dependency license/notice, model-weight and API/data terms for the exact versions at binding; do not assume every candidate permits the same distribution or use. Do not copy third-party internals merely to rename them as proprietary.

We should build a new numerical, inference or search kernel only when: an existing option fails an explicit contract or measured target; the failure survives profiling and reasonable configuration; a narrower original algorithm has a clear objective/invariants; and matched evaluation plus maintenance cost supports the replacement. Keep the original backend as a conformance/reference option where practical.

## 6. Integration and scale consequences

No added owner, service or lane is required by this research. All 28 pairs/56 directed lanes retain their statuses. Third-party libraries run inside the appropriate owner; independently operated providers, stores and workflow services remain external dependencies with explicit contracts. An optional infrastructure adoption needs a fresh boundary/fault/identity/interface review before deployment.

Highest-risk paths inspected:

1. Parser/model proposal -> C3 admission: source selector, identity, time, unknowns and imported assistance survive transformation; model output cannot directly become accepted truth.
2. C3 IR -> solver -> C6: units, time/history, valid domain, backend/operator version and forecast cut survive compilation and evaluation; analysis cannot write accepted model state.
3. Discovery -> fit -> evaluation -> revision: candidate construction/selection data are separated from outcome tests; an LLM-generated simulator is not an independent source.
4. C4 inquiry -> C0 schedule -> C7 access -> C1 acquisition -> C2/C3 update: one missing-access request, scope respected, denial retained, acquired material provenance preserved; a grant is not an observation.
5. Fine-detail update -> bridge -> coarse projection -> wider prediction: invalidate all declared affected dependencies, including shared constraints and retained commitments; display unresolved effects.
6. Workflow/database/artifact boundaries: retries and replay cannot duplicate real effects; no distributed exactly-once promise follows from a queue or framework name.

Initial maintainability choice: one application and transaction owner per durable state domain, explicit protocols instead of cyclic imports, dependency injection at adapters, migrations, deterministic replay of committed records and isolated numerical jobs. A display/API is a read/proposal client through existing ports; it does not add a model state authority.

Partitioning, replicas, object durability and bounded workers are the first scale path; a graph server, streaming engine, workflow cluster or GPU server is a conditional physical evolution. Keep accepted semantic state distinct from retrieval graphs and analysis exports. Scientific result caches include evidence/model/domain/backend dependencies. No result is made fresh merely because it was fast.

## 7. Development order and falsifiable adoption experiments

| Increment | Concrete outcome | Preferred tooling and gate |
| --- | --- | --- |
| D0 | Typed source/identity/time, ModelDelta, projection validity, RefinementBridge and KnowledgeRequest fixtures; pin interpreter and dependencies. | Pydantic/Pint, uv, schema/semantic checks. Contract gate; no blanket readiness claim. |
| D1 | One small complete observation -> hypothesis -> supported simulation -> independent comparison -> revision loop in a shared world. | P0 stack, one reasoning provider and deliberately limited numerical grammar. Start measuring cost/latency and preserving failures immediately. |
| D2 | The same world expands into an adjacent economic view and inward into insect life stages; old forecasts and contested explanations survive. | Add only needed P1 discovery/inference adapters. Keep unrelated and conventional-memory comparators. |
| D3 | Qualify local useful speed, growth, retractions, high-degree changes, outage/recovery and maintenance. | FAST1/DEV1; add P2 infrastructure only against an observed bottleneck or explicit HA requirement. |
| D4 | Test learned surrogates, distillation, latent dynamics or an original search kernel against a documented shortfall. | Bounded P3 experiment; held-out tasks, complete training/inference costs and independent empirical outcomes. |

The following adoption experiments refine the existing E01-E48 obligations; they do not replace them, weaken thresholds or claim new results. A01-A08 are specified_not_run, with no implementation revision or evidence artifact.

| ID | Comparison and predeclared acceptance obligation | Existing cases |
| --- | --- | --- |
| A01 | Simple retrieval/LLM, structured conventional model and EDI on the same observations, tools, task cuts and full cost. Hold out changed mechanisms; include missing/ambiguous evidence. Require useful gain on preselected task metrics with uncertainty, not a handpicked success narrative. | E14, E20-E23, E36-E38, E46, E48 |
| A02 | Deterministic, Jev, small/local and generative focused-decision adapters on matched contexts. Pin selective error/calibration/coverage and output-domain policy before latency comparison; include missing correct option, dependence, timeout and OOD. | E22, E38, E40, E42, E48 |
| A03 | Candidate nonlinear laws, PySINDy and PySR on controlled observable dynamics with varied noise, sampling, excitation, hidden driver and regime. Report prediction, structural recovery when known, identifiability failures and search cost separately. | E09, E14, E17-E18, E23, E37 |
| A04 | Numerical backend conformance on supported ODE/event/history cases, and explicit unsupported DAE/delay cases before adding a new backend. Compare trajectories, invariant tolerances, event timing and carry-over; include precision and compilation cost. | E10-E12, E17-E19, E40, E44 |
| A05 | Fit/uncertainty candidates on identifiable, non-identifiable and misspecified models; check diagnostics and held-out predictive calibration, not just training loss. Keep confounding and model error distinct from parameter uncertainty. | E14, E20-E23, E31, E37 |
| A06 | Inquiry heuristic against random/novelty-only and justified information/value criteria under equal acquisition budgets. Include noisy but irrelevant observations, inaccessible data and inconclusive outcomes; compare held-out decision/prediction benefit and access-request burden. | E15-E16, E30-E31, E45-E46, E48 |
| A07 | Incremental SQL/application views versus full recomputation, then any proposed Materialize/native-kernel replacement at the same semantics/cutoff. Include corrections, merges/splits, global invalidation, cold start and full restore/maintenance cost. | E32-E35, E38-E41, E43, E47-E48 |
| A08 | Coarse/fine model with valid bridge, invalid bridge and no useful extra detail; expand breadth/depth without resetting memory. Verify quantities, nonlinear aggregation, uncertainty, pending state and cost; a larger graph alone does not pass. | E08-E11, E16, E37, E44, E46-E48 |

Exact package/provider pins, selected fixture, task metric margins and statistical analysis plan remain entry conditions for their execution. No paid API calls, weights, runtime, automated acquisition, deployment or benchmark were started by this research.

## 8. Critical assessment and remaining choices

KISS: retain eight logical owners and a minimal P0 stack; every optional tool has a capability trigger and replacement boundary. Five Whys: persistence is needed for cumulative learning; revision is needed because observations/confidence/identity change; dependency invalidation is needed because those changes affect old conclusions; bounded views are needed for useful speed; explicit access/inquiry policies are needed because information is incomplete and acquisition has cost. These are design rationales, not experimentally established causal explanations.

Coverage axes: all eight owners and 32 functions are allocated; storage, runtime orchestration, model serving, mathematical inference and domain semantics are compared as distinct decisions. Multiple methods can collaborate rather than being falsely declared mutually exclusive. The review preserves original requirements and all no-link directions. No new contract operation or state authority is introduced here.

Main unresolved choices: the concrete supported IR grammar; first domain fixture and accessible independent observations; task-specific discovery/transfer metrics; compatible package/model/OS/hardware pins; defensible inference assumptions; fast-decision quality/coverage thresholds; license/data/service binding; and measured migration triggers. These block concrete contract/runtime/scientific qualification where relevant. They do not prevent a reviewable research recommendation.

Research limits: this is a targeted current primary-source assessment, not an exhaustive global SOTA ranking. Several live documentation routes failed or redirected; working official project repositories/standards were used for DuckDB, DSPy, PySR and Modelica. The inspected libRoadRunner landing documentation is an older version and explicitly excludes some operators; it is evidence for a candidate adapter, not a current installed-backend capability guarantee. Vendor catalogues describe candidates, not an EDI winner. Source/version and OS compatibility must be checked again when binding dependencies.

Recommendation: proceed with the original EDI core plus established numerical/persistence/model adapters. Preserve the ability to replace methods and create new algorithms, but make a specific demonstrated gap earn that investment. Architecture self-review supports this bounded proposal; all contract, runtime, scale, intelligence and comparative claims retain their separate evidence gates.
