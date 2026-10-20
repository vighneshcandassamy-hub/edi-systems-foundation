# EDI architecture, tools and mathematical techniques — consolidated reference

Version 1.0 — 20 October 2026. Consolidation input: `fb3dc745ba27c4664e01ab4b18d20cbf593d9b46`. Purpose: one implementation reference for the architectural direction, starting-tool preferences, mathematical methods, conditional alternatives and remaining decisions discussed so far.

**Current stage: structure and specification before qualification or tests.** Nothing in this reference claims installed dependencies, implemented runtime, trained weights, tested integration, measured performance or a demonstrated intelligence advantage. Historical checks retain their original scope. This consolidation adds no component, interface lane, numerical target or qualification result.

## 1. Decision status and precedence

| Status | Meaning in this reference |
| --- | --- |
| Agreed architectural direction | The integrated systems architecture and subsequent student/teacher, pretrained-first and structure-first direction adopted in the conversation. |
| Initial implementation preference | The intended first engineering choice from the documented tool assessment. It is not an installed/version-pinned dependency or a claim that the owner individually approved every library. |
| Conditional capability | A technique or adapter retained for use when its data, mathematical and operational prerequisites apply. It is not mandatory on every observation or reasoning call. |
| Deferred alternative / research | An explicitly retained option, not part of the initial mandatory stack. |
| Open binding | Exact model, package version, provider, numerical grammar, platform or operating setting has not yet been selected. |

This document is the consolidated reading entry point for tool/mathematics choices. Detailed obligations remain in the linked requirements, contracts and component specifications. For model roles, the latest [reasoning integration](REASONING_INTEGRATION.md) takes precedence over earlier text that described one general reasoning-provider candidate without distinguishing teacher and local student. No historical source or failed result is overwritten.

## 2. Architecture baseline

| Item | Recorded decision |
| --- | --- |
| Conceptual foundation | Meadows Chapters 1–7 plus the appendix semantic reference; mathematical/engineering extensions remain identified as our synthesis. |
| Current full diagram | [Integrated reasoning diagram](INTEGRATED_REASONING_DIAGRAM.md), [Mermaid source](INTEGRATED_REASONING.mmd): 98 nodes and 286 named connections, retaining all 82 original nodes and 241 connections. |
| Full master | [Integrated master v0.8](../../architecture/world-model/Meadows_EDI_Integrated_Architecture_v0_8.md). The imported v0.7 conceptual snapshot remains preserved. |
| Software allocation | Eight logical owners, 32 functions. Diagram concepts and internal reasoning parts are not separate mandatory services. |
| Shared representation | Nine representation families, evidence/provenance, identity, temporal meaning, alternatives, uncertainty and revision across them. |
| Integration | Existing 28 component pairs / 56 directed lanes; implement justified connections, with one durable owner per state domain. |
| Initial deployment shape | Modular Python application, Postgres, source-native artifacts, bounded jobs/workers and replaceable parsing/model/numerical adapters. |
| Knowledge growth | One persistent world expanded in breadth, internal depth, resolution and time; shared referents and histories rather than isolated test-case memories. |
| Neural learning | Pretrained student and teacher versions; fixed weights initially; future training/checkpoint-adoption path separate and dormant. |
| Development sequencing | Establish the integrated structure first. Qualification, comparative tests and training are later work, not performed by this reference. |

### 2.1 Component responsibilities and intended tools

| Owner | Functions | Intended implementation | Boundary that remains EDI-owned |
| --- | --- | --- | --- |
| C0 Inquiry | F00 define inquiry; F01 scope; F02 schedule/bound work; F03 deliver findings. | Explicit controller/state machine; Postgres durable job/outbox records and bounded workers. | Purpose, scope, resource budgets, inquiry scheduling, access-request consolidation, progress/finding delivery. |
| C1 Observe | F10 receive; F11 preserve/attribute; F12 select/replay; F13 bound capture/recovery. | Native bytes/chunks, hashes, manifests, source/epoch registry and artifact storage. | Source versus occurrence versus payload identity, continuity, receipt/durability, replay/gaps, generated lineage. |
| C2 Interpret | F20 decode; F21 qualify identity/meaning; F22 retrieval features; F23 submit claims. | Native parsers; Docling/FFmpeg when relevant; Pint; optional learned perception/linkage. | Evidence selectors, event/structure/basis distinctions, temporal meaning, reversible identity associations, unknown formats. |
| C3 World | F30 instantiate/compose; F31 admit changes; F32 expose views; F33 maintain projections. | Original typed temporal relation/model kernel over Postgres, SQLAlchemy/Alembic and incremental projections. | Canonical identity, composition, mechanism status, admission, version history, dependency invalidation, refinement bridges. |
| C4 Reason | F40 rival mechanisms; F41 investigate relationships; F42 rank inquiries; F43 expand frontier. | Systems reasoning controller, pretrained student via vLLM, selective pretrained teacher and mathematical-tool adapters. | Reasoning protocol, scoped context, hypothesis records, tool requests, uncertainty, breadth/depth exploration and episode provenance. |
| C5 Analyze | F50 compile; F51 execute scenarios; F52 sensitivity/uncertainty; F53 trajectories. | Original restricted mechanism representation/compiler, NumPy/SciPy first; specialist backends conditionally. | Supported mathematical semantics, units/accounting, clock/history, state carry-over, conditional outputs and unsupported outcomes. |
| C6 Assess | F60 seal expectations; F61 compare outcomes; F62 diagnose; F63 recommend revision/findings. | Original forecast/evidence/scoring records; appropriate statistical and uncertainty adapters. | Independent evidence, original forecasts, discrepancy categories, model criticism, learning/reuse decisions and inquiry yield. |
| C7 Agency | F70 actor-visible information; F71 intended action; F72 authorize/reconcile; F73 adopt policy. | Explicit versioned policy/state machine, deterministic permissions/feasibility, idempotent connectors; optional optimizers. | Actor information versus actual constraints; intent/authority/receipt/effect distinctions; operational policy/checkpoint adoption. |

### 2.2 Shared representation families

1. System view: boundary, level, resolution, horizon and external interfaces.
2. Constituent: identity, composition, membership, condition and lifecycle.
3. Stock: accumulated quantities/resources/buffers with units, bounds and history.
4. Flow/process: transfers, transformations, resource use and pending completion.
5. Information/influence link: direction, channel, receipt, meaning and availability.
6. Response relationship: joint inputs/outputs, nonlinear law/domain, parameters, delays or unresolved mechanism.
7. Function/purpose/reference/criterion: attributed roles, goals, incentives, standards and concerns.
8. Feedback path: referenced complete return path, conditional sign/dominance and timing; not extra dynamics counted twice.
9. History/conditional trajectory: observed, predicted or simulated evolution with distinct origin and conditions.

Multi-party relationships use role-indexed relation instances. Binary graph projections support traversal without replacing joint mechanism semantics. Source evidence, EDI's model of a system and the system's actual external state remain distinct.

## 3. Student, teacher, vLLM and learning

| Role / choice | Consolidated decision | Open binding |
| --- | --- | --- |
| Student | A pretrained instruction/reasoning model. Prefer a compatible open-weight checkpoint when local serving and later parameter adaptation are intended. | Exact checkpoint, size, dense/MoE architecture, precision, hardware fit and supported tools/modalities. |
| vLLM | The serving/inference engine for a compatible student; it is not the model being taught. | Compatible version, deployment environment, batching, context and memory configuration. |
| Teacher | A stronger pretrained model providing selective critique, worked examples, questions and proposed corrections. | Exact provider/checkpoint and supported interaction/scoring interfaces. |
| Initial weight policy | Fixed identified student and teacher weights. | No EDI training job or automatic weight change is configured. |
| Reasoning guidance | Versioned systems reasoning protocol; relevant operations selected per inquiry. | Concrete prompts/structured schemas and escalation settings. |
| World-model learning | Continuous evidence-qualified changes to representations, mechanisms, uncertainty and history. | Concrete admission/delta/schema implementation. |
| Future neural learning | Curated episodes -> explicit training job -> candidate checkpoint -> separately authorized adoption. | Training method, optimizer, adapter/full-weight choice, dataset and trainer are unselected. |
| Random initialization | Deferred research alternative, not the main first-iteration student. | Would require acquisition of general language/reasoning capabilities as well as EDI specialization. |
| Pretrained base without instruction post-training | Retained training-oriented alternative. It still contains learned pretraining priors. | Not selected for the initial operational student. |

Earlier GPT-6.1 Sol, GPT-6 Astra, Claude, Gemini, Qwen and DeepSeek entries are researched model candidates. They are **not all selected dependencies**. In particular a hosted closed-weight teacher/development model is not automatically a locally serveable vLLM student. Qwen names in the earlier comparison are candidates rather than a frozen current-checkpoint selection. Jev is an optional focused decision adapter, separate from this teacher/student distinction.

Three changes have different meanings: updating the world model, changing inference context/protocol, and changing neural weights. Fixed weights permit the first two; neither is automatically a neural training update. Pretrained knowledge remains attributed model assistance, not independently observed evidence.

### 3.1 Systems reasoning operations

Select the operations relevant to the inquiry: distinguish events/patterns/structures; establish meaning, identity and time; inspect stocks/flows/shared constraints; trace feedback and delays; examine nonlinear regimes; distinguish actor knowledge/incentives/actions; construct rivals; derive conditional consequences; seek discriminating evidence; expand outward or refine inward; and propose evidence-qualified revision.

Five Whys and What If are available patterns. No fixed questioning depth is imposed, and missing evidence stays unknown. Both teacher and student follow the explicit protocol while retaining useful general language, scientific and mathematical capabilities. Instructions do not erase pretraining or guarantee a different internal reasoning algorithm.

## 4. Starting software stack

These are initial implementation preferences at design level. Select compatible versions before installation; no installation occurs here.

| Tool / mechanism | Intended use | Source / detail |
| --- | --- | --- |
| Python | Main application and scientific-tool integration; use a compatible locked interpreter. | [Component deployment notes](COMPONENTS.md), T20. |
| uv | Dependency/environment management; isolate conflicting scientific/GPU/Julia environments where needed. | S61. |
| Pydantic | Typed record/schema validation, with explicit strictness and tagged unknown/error states. | S44, T19. |
| Pint | Quantity/unit operations; semantic meaning still requires EDI rules. | S45, T19. |
| Postgres | Canonical transactional metadata/model state, revisions, job/outbox records and projection tables. | S12-S13, T01/T05/T06. |
| SQLAlchemy and Alembic | Database access/mappings and explicit schema migrations. | S49-S50, T05. |
| Native artifact storage | Source bytes, manifests and durable artifact references; verified local directory under DEV1, scalable backend later. | [Capture/commit contracts](CONTRACTS.md), T02. |
| Native parsers | Preserve and decode supported text, numeric and structured inputs without compulsory model inference. | T03. |
| Docling | Supported document conversions, preserving original artifacts and source selectors. | S07, T03. |
| FFmpeg | Media stream handling/conversion and time mapping; semantic visual understanding is separate. | S08, T03. |
| NumPy and SciPy | Numerical arrays, supported dynamics, parameter fitting and reference calculations. | S26/S82, T10. |
| vLLM | Serve the selected compatible pretrained student. | S46 plus [reasoning integration](REASONING_INTEGRATION.md). |
| Replaceable teacher/model adapters | Selective guidance and interpretation with version, input, output and cost provenance. | S01-S06, T08; exact models open. |
| Original bounded controller | Explicit scheduling, durable jobs, idempotency, cancellation and budget accounting. | T01; not a mandatory LangGraph/Temporal deployment. |
| OpenTelemetry-compatible records | End-to-end timing and resource/failure/freshness visibility, with explicit operational/scientific meaning. | S48, T21. |
| Ruff and Pyright | Lint/format and static typing during development. | S62/S79, T20. |
| pytest and targeted Hypothesis | Reserved development test tooling for the later testing stage. Naming tools does not authorize or claim execution now. | S63/S78, T20. |

Large media and model weights stay outside Git. Database acknowledgement and artifact durability must obey the same declared profile; they are not automatically one transaction across arbitrary backends.

## 5. Conditional tools, alternatives and adoption priorities

P0 denotes the first integrated capability; P1 a needed specialist capability; P2 a measured scaling/availability addition; P3 bounded research. A row's priority does not make all named alternatives mandatory. Original T01-T24 decisions and allocations are preserved in [TOOLS.json](TOOLS.json).

| ID / stage | Preferred or retained technique | Alternatives / adoption condition |
| --- | --- | --- |
| T01 / P0 | Original explicit controller and durable SQL jobs. | LangGraph for branching agent execution; Temporal for distributed durable workflow needs. Neither becomes the world-model authority. |
| T02 / P0 | Native evidence registry/manifests/artifacts. | Managed object storage and redundancy when required by the selected fault/capacity profile. Backend product remains open. |
| T03 / P0 | Native parsers, Docling and FFmpeg as needed. | Specialized vision/audio/sensor/symbolic/scientific adapters; multimodal models when relevant. Unknown inputs can remain retained without interpretation. |
| T04 / P0 | Evidence-qualified reversible identity associations. | Splink for structured linkage; text/visual embeddings for candidates. Similarity does not itself admit a physical-identity merge. |
| T05 / P0 | Original temporal model over Postgres/SQLAlchemy/Alembic. | Neo4j for graph traversal; RDF/SHACL for relevant interchange/constraint needs. These are conditional alternatives, not extra mandatory stores. |
| T06 / P0 | Original dependency index and retraction-aware projection maintenance. | Materialize for justified sustained streaming joins/aggregations. Ordinary Postgres materialized views alone do not implement continuous delta maintenance. |
| T07 / P1 | Bounded structural/lexical retrieval, then pgvector and a selected embedding adapter if needed. | GraphRAG, LightRAG, Graphiti and researched Qwen embedding candidates. Retrieval/memory aids do not replace executable mechanisms or admission. |
| T08 / P0 | Student/teacher roles through replaceable adapters, per the latest fixed-pretrained decision. | Earlier hosted/local model shortlist remains alternatives; exact checkpoints unbound. |
| T09 / P1 | Optional Jev for bounded typed decisions. | Deterministic rules, small local classifiers or a bounded generative call. Preserve abstention, option completeness and uncertainty; no universal causal confidence. |
| T10 / P0 | Original restricted compiler with NumPy/SciPy. | PySD for stock/flow model import, SimPy for discrete events, Mesa for agent models. Select only supported semantics. |
| T11 / P1 | Advanced numerical backend when the model requires it. | SUNDIALS IDA for DAE; JAX/Diffrax for suitable differentiable/stochastic workloads; CasADi for supported optimization/control; Modelica as a composition/interchange reference. |
| T12 / P1 | Simple candidate laws and PySINDy for suitable measured dynamics. | PySR symbolic search or neural dynamics where justified; candidate grammar, data assumptions and interpretability differ. |
| T13 / P1 | DoWhy for scoped causal assumptions/identification/effect assessment. | Tigramite for suitable time-series discovery. Method-specific hidden-variable, temporal and graph assumptions remain explicit. |
| T14 / P1 | PyMC as the first readable Bayesian modeling candidate. | NumPyro for suitable JAX inference; sbi when an appropriate simulator exists but likelihood evaluation is impractical. |
| T15 / P1 | Finite perturbations and SALib for suitable sensitivity questions. | SymPy/JAX derivatives or scenario ensembles according to continuity, dependence and domain. |
| T16 / P0 | Original forecast sealing, comparison and revision records. | MAPIE/conformal techniques for applicable predictive uncertainty; River/ADWIN for drift-triggered inquiry. Neither establishes the cause of drift. |
| T17 / P1 | Original inquiry frontier and explicit feasible discrimination/relevance/cost ranking. | Expected information gain/value of information where justified; BoTorch for expensive parameterized numerical experiment selection. |
| T18 / P0 | Original policy, permission, intent and execution lifecycle. | OR-Tools discrete planning; CVXPY compatible convex problems; CasADi supported nonlinear control. Solvers do not establish legitimate goals or authority. |
| T19 / P0 | Pydantic and Pint plus original semantic validation. | Plain internal dataclasses when sufficient; Z3 for a specific nontrivial formal constraint need. |
| T20 / P0 | uv, Ruff, Pyright and the later pytest/Hypothesis workflow. | Existing equivalent development tools remain replaceable; no runtime benchmark follows from these tools. |
| T21 / P0 | OpenTelemetry-compatible instrumentation and explicit run accounting. | Local records first; trace/evaluation service only when useful. Trace data and scientific evidence have distinct roles. |
| T22 / P2 | SQL/NumPy first; Polars or DuckDB for appropriate columnar/offline analysis. | JAX or Rust/PyO3 for a profiled kernel. NetworkX for bounded/reference graph analysis, not an in-memory duplicate of the entire world. |
| T23 / P1 | SBML/libRoadRunner as an optional internal-biology adapter. | Supported population/cohort laws may suffice. Imported biology needs a justified bridge to whole-insect/ecosystem outcomes; installed backend operators remain unbound. |
| T24 / P3 | Future distillation or learned reuse; DSPy for a suitable bounded reasoning program. | Rules/compiled models first; V-JEPA/Dreamer-style latent world models and other learned dynamics remain separate research choices. |

FastAPI is retained as an optional HTTP boundary (S51); in-process owner ports can come first. A UI, API server, message broker, orchestration cluster or graph service is not required merely because the conceptual diagram contains many nodes. No broker, cloud provider, Kubernetes deployment or trainer has been selected.

## 6. Mathematical techniques and their implementation meaning

This is the complete mathematical-method reference for the present design, including explicitly conditional/deferred techniques. These are standard foundations and proposed EDI combinations, not claims of new mathematics or demonstrated superiority.

| ID | Technique | EDI use and prerequisites | Intended tools / status |
| --- | --- | --- | --- |
| M01 | Typed temporal, multi-party relation structures | Represent composition, directed interfaces, joint response laws, shared referents and evidence/known-time history. Binary edges are traversal projections of richer relations. | Original C3 representation kernel; core design. |
| M02 | Dimensional analysis and semantic constraints | Check quantity kind, units, scale and legal operations. Missing values remain unknown; ordinal categories do not become cardinal by coercion. | Pint plus original validators; core design. |
| M03 | Stock/flow accounting and ODE dynamics | Compute accumulation under declared rates, boundary terms and supported response laws. State initial conditions, units, domain and numerical policy. | NumPy/SciPy; core supported-submodel design. |
| M04 | Delay/history and discrete/hybrid dynamics | Preserve prehistory, pending effects, resource queues, event ordering and a common clock. Ordinary ODE support is not arbitrary-delay support. | Original semantics; SimPy/PySD/Mesa or another compatible backend conditionally. |
| M05 | Algebraic constraints / DAE | Solve coupled state/equation constraints with appropriate initialization and solver support. Computational ordering is not proof of physical causation. | SUNDIALS IDA / CasADi conditionally; Modelica reference/interchange. |
| M06 | Nonlinear response and local stability analysis | Examine saturation, thresholds, hysteresis, interactions, changing feedback dominance and regimes. Local Jacobian analysis is local, not a global stability proof. | Finite perturbations/SciPy; symbolic or automatic derivatives conditionally. |
| M07 | Bounded nonlinear parameter fitting | Fit declared response parameters to suitable data while respecting domains and diagnostics. Local fit and training error do not identify a unique mechanism. | SciPy least_squares; conditional on an explicit fit model. |
| M08 | Sparse system identification | Infer candidate compact dynamics from sufficiently informative measured variables and a declared function dictionary. Noise, hidden drivers and excitation matter. | PySINDy; conditional specialist. |
| M09 | Symbolic regression | Search interpretable expressions under a specified operator/complexity grammar, units and domain constraints. A plausible expression still needs evidence. | PySR; retained alternative to restricted law search. |
| M10 | Causal identification and time-series structure inference | Separate association, temporal precedence, model structure and identified intervention effects. Preserve confounding and observational equivalence. | DoWhy/Tigramite; scoped, assumption-dependent use. |
| M11 | Bayesian parameter/model-family inference | Estimate conditional uncertainty under specified priors, likelihoods and data dependence. Missing structural alternatives remain unknown. | PyMC first candidate; NumPyro alternative. |
| M12 | Simulation-based inference | Infer simulator parameters when an appropriate generative simulator exists but likelihood evaluation is impractical. Simulator/prior errors remain consequential. | sbi; conditional, not default per observation. |
| M13 | Global/local sensitivity | Determine which inputs, parameters or interfaces affect particular outputs within a domain; respect correlated-input assumptions and discontinuities. | Finite perturbations, SALib Morris/Sobol, supported derivatives. |
| M14 | Information gain / value of information | Rank feasible inquiries by discrimination or decision benefit. Requires defensible predictive probabilities/utilities; otherwise use explicit separate heuristic criteria. | Original inquiry controller; BoTorch for suitable numerical search. |
| M15 | Constrained optimization and control | Select feasible actions/resources under declared goals, model assumptions, timing and authority. | OR-Tools, CVXPY, CasADi according to problem class; conditional. |
| M16 | Forecast scoring, calibration and change detection | Preserve original expectations; compare independent outcomes; separate prediction error, uncertainty calibration and drift from causal explanation. | Original C6 records; proper scores; optional MAPIE/River. Qualification/test execution deferred. |
| M17 | Coarse/fine aggregation and refinement | Link internal detail to aggregate interfaces without duplicate quantities/history. State applicability, lost information and error/unknown bounds; refine when needed. | Original RefinementBridge and resolution policy; core design. |
| M18 | Incremental computation and dependency closure | Apply deltas/retractions; invalidate affected derived results; expose global fan-out/backlogs and fresh/stale status. | Original reverse indexes/projections over SQL; optional Materialize/native kernel. |
| M19 | Teacher-guided parameter learning | Separate live critique from supervised distillation, token/log-probability distillation and on-policy learning. Record generated lineage and compatible training interfaces. | Future trainer unselected; initial weights fixed. |
| M20 | Learned surrogates, neural/latent dynamics and reuse | Approximate repeatedly useful supported computations or train domain-specific predictive representations. Teacher agreement is not independent empirical truth. | Optional later learned models/DSPy/latent-model research. |
| M21 | Symbolic algebra and formal satisfiability | Manipulate supported expressions or check specified logical constraints; mathematical consistency does not establish external reality. | SymPy/Z3 conditionally; not canonical model owners. |
| M22 | Automatic differentiation and compiled array kernels | Reuse derivatives/batched calculations for suitable numerical programs. Changing shapes, compilation, precision and data copies affect costs. | JAX/Diffrax conditionally; Rust/PyO3 for profiled native kernels. |

### 6.1 Working mathematical forms

For a supported continuous model:

\[
\dot{x}(t)=S\,v(x(t),u(t),h_t;\theta,H)+b(t),\qquad
y_k=g(x(t_k),\phi_k;\theta,H)+\epsilon_k.
\]

Here x is state/stock, v rates, S the accounting map, u inputs/policy, h retained history, theta parameters, H a structural hypothesis, b boundary terms and g the observation/sampling mechanism. Transformations, losses and external exchanges are explicit; not every quantity is conserved. Measurement error, process variability, missingness and selection are different concerns.

For a declared model family with defensible likelihood/prior assumptions:

\[
p(\theta,H\mid D)\propto p(D\mid\theta,H)\,p(\theta\mid H)\,p(H).
\]

An LLM plausibility score is not this posterior. Derivatives or summaries of one source do not become independent corroborating observations.

A candidate sparse-identification objective is:

\[
\min_{\Xi}\;\|\dot{X}-\Theta(X,U)\Xi\|_W^2+\lambda\|\Xi\|_1.
\]

Coordinates, candidate dictionary, derivative estimation, noise/weights, regularization and admissible laws remain assumptions. A fitted law can be useful while its causal interpretation remains unresolved.

A possible inquiry criterion, within a specified candidate family, is:

\[
\mathrm{EIG}(a)=\mathbb{E}_{Y_a\mid D,a}
\left[\mathrm{KL}\left(p(H,\theta\mid D,Y_a,a)\;\|\;p(H,\theta\mid D)\right)\right].
\]

Use it only when the distributions are defensible. Otherwise retain separate discrimination, relevance, cost and feasibility criteria. High entropy or novelty caused by random noise is not automatically valuable learning. These equations are implementation templates, not a universal model of all reality.

### 6.2 Numerical and inferential boundaries

- A graph connection is not an executable law; a numerical backend may return unsupported.
- DoWhy's documented GCM machinery uses acyclic graphs. Use justified scoped/time-indexed formulations where applicable; preserve the original feedback world and do not silently delete cycles.
- Non-identifiable mechanisms can remain alternatives despite good predictive fit.
- Scalar confidence, posterior uncertainty, model incompleteness, numerical error and missing observations are different quantities.
- Coarse averages can hide nonlinear thresholds; additional detail can also fail to improve an answer.
- A teacher, simulator or generated model is not an independent source of real-world observations.
- Formal constraints and native-code speed do not guarantee the world model is correct.

## 7. Original EDI code we intend to own

| Original asset | Responsibility | Reused foundations |
| --- | --- | --- |
| Representation/admission kernel | Canonical shared model, history, alternatives, identity and evidence-qualified revisions. | Postgres, typed schemas and migrations. |
| Mechanism representation/compiler | Supported operator grammar, units/accounting, state/history and backend lowering. | Established symbolic/numerical solvers. |
| Revision/dependency kernel | Deltas, retractions, invalidation, projections, freshness and repair. | Transactions, indexes and optional streaming infrastructure. |
| Cross-scale refinement coordinator | Breadth/depth/resolution/temporal bridges and shared-resource consistency. | Appropriate aggregation and numerical tools. |
| Inquiry/access controller | Triggered frontier, discriminating questions, feasibility, requests, deduplication and stopping. | Teacher/student proposals, optional information/optimization methods. |
| Learning/reuse controller | Original forecasts, evidence comparison, discrepancy diagnosis, justified revision and knowledge applicability. | Statistical tools and separately versioned model adapters. |

This is an engineering ownership plan. It does not establish novel mathematics, patentability or ownership of third-party tools/models/data. Exact dependency, weight and service terms remain binding choices. No new custom optimizer, database or ODE solver is mandated by the discussion; retain room for an original algorithm when a concrete limitation justifies it.

## 8. Integration rules to preserve in the code structure

1. One durable state authority per domain. C3 admits accepted model changes; models submit proposals.
2. Existing component ports govern reads, proposals and results. A diagram arrow is not permission for direct cross-owner writes.
3. C4 analysis requests use C0 scheduling and existing C0-C5 contracts. Missing access uses C0/C7/C1. No new C4-C5/C7 bypass is introduced.
4. Student and teacher interaction preserves separate request and feedback directions, source cuts, model/protocol versions and generated lineage.
5. Actor policy inside the modeled ecosystem differs from EDI operational policy and checkpoint adoption.
6. Scenarios and simulations remain distinguishable from actual observations. Independent comparisons retain original sealed forecasts.
7. Capture can continue within its resource profile while optional reasoning is pending/unavailable.
8. Standalone input/source adapters extend observation breadth without changing the world-state authority.
9. Interpretation and other functions may use learned assistance through their owning adapters; not every record requires the teacher.
10. Future training/checkpoints are explicitly versioned and adopted; retaining an episode never automatically mutates live weights.

The common proposed records include native occurrence/source manifests, attributed claims, role-indexed model relations, model revisions/patches, ModelDelta, projection validity, RefinementBridge, ExplorationFrontier, KnowledgeRequest, ScenarioSpec, RunRecord, sealed forecasts/comparisons and attributed learning episodes. Concrete schemas remain to be written.

## 9. Long-term growth, speed and resource requirements

Core mechanisms: bounded task contexts, indexed temporal/identity access, incremental updates/retractions, reverse dependency indexes, valid reusable projections/compiled models, explicit watermarks and qualified coarse/fine summaries. Routine local work should primarily track the affected active portion rather than require complete-world rescanning. Globally coupled changes and questions may still require broad work.

The [FAST1/DEV1 specification](SCALING_AND_WORLD_GROWTH.md) records unmeasured targets, including p95 100 ms eligible warm deterministic reads, p95 250 ms bounded local updates and p95 500 ms bounded focused probabilistic decisions. These have declared operation shapes, freshness/quality boundaries, end-to-end costs and exceptions; they are not universal response guarantees. Deep inquiry/acquisition has separate completion semantics. No new target is created here.

Grow one world in four directions: adjacent systems, internal decomposition, heterogeneous resolution and temporal refresh. Reuse identity/evidence where supported, preserve deferred/unknown boundaries, and invalidate downstream conclusions when assumptions change. Standing grants can be reused; missing-access requests state the specific evidence need and are deduplicated. Proposed notification settings remain configurable design settings, not enabled automations.

Physical scale additions are conditional: partitions, bounded worker pools, replicas, more durable artifact storage, a graph/streaming/workflow service or compiled kernels. Backups alone do not establish high availability; no arbitrary scale or constant-time global reasoning is claimed.

## 10. Open implementation bindings

| Open item | What must be concretely decided |
| --- | --- |
| Models | Exact pretrained student and teacher checkpoints/providers; role, supported inputs/tools, version, context and inference settings. |
| Platform | Compatible Python, OS, CPU/GPU/memory, numerical/serving packages and locked dependency versions. |
| Contracts | Concrete native, identity/time, delta/validity, refinement, access, model-service and episode schemas. |
| Mathematics | First supported operator grammar, backend capabilities, initial/history/event semantics, solver settings and method applicability. |
| Data | First observation sources/fixture, rights, time/correspondence and independent evidence availability. |
| Operation | Concrete budgets, concurrency/escalation, retention/durability profile and migration strategy. |
| Future training | Dataset/feedback selection, scoring access, trainer, objective, adaptation method and checkpoint lifecycle. Dormant initially. |
| Conditional tools | Which specialists are actually needed for the first capability; the entire catalogue is not an installation list. |

## 11. Reference map and handoff

| Asset | Use |
| --- | --- |
| This document | Consolidated architecture/tool/mathematics decision reference. |
| [Integrated diagram](INTEGRATED_REASONING_DIAGRAM.md) / [v0.8 master](../../architecture/world-model/Meadows_EDI_Integrated_Architecture_v0_8.md) | Current full structure and retained conceptual detail. |
| [Reasoning integration](REASONING_INTEGRATION.md) / [allocation](REASONING_INTEGRATION.json) | Student/teacher, fixed weights, controller/admission/training and existing owner/lane mappings. |
| [Component specifications](COMPONENTS.md) / [contracts](CONTRACTS.md) / [interfaces](INTERFACES.json) | Detailed functions, state, boundaries, authority, errors and proposed operation families. |
| [Tools/proprietary assessment](TOOLS_AND_PROPRIETARY_CORE.md) / [24 decisions](TOOLS.json) | Alternatives, rationale, build/reuse boundary and prospective adoption experiments. |
| [Scaling/world growth](SCALING_AND_WORLD_GROWTH.md) / [growth policy](GROWTH_POLICY.json) | Incremental operation, refinement, frontier/access lifecycle and unmeasured profiles. |
| [Requirements traceability](TRACEABILITY.json) | Existing mission/system/layer/function/case allocations; no requirement is redefined by this consolidation. |
| [Primary references](SOURCES.md) / [register](SOURCES.json) | 84 registered research entries, plus teacher/distillation references in REASONING_INTEGRATION.md. Live versions remain subject to binding. |
| [Historical verification plan](VERIFICATION.md) | Future obligations, not authorization to run them during the structure-first stage. |

Next development artifact: the integrated code structure and concrete owner/adapter contracts aligned with this reference and the full diagram. This document does not start that build, install tools, train models, run tests/qualification, deploy services or create autonomous acquisition tasks.
