# Model and technique tradeoffs

Version 0.1, 20 October 2026. Status: researched implementation-architecture recommendation, not a runtime qualification. Source IDs resolve in [SOURCES.md](SOURCES.md). The codebase has not been built by this task.

See [tools, priorities and the proprietary core](TOOLS_AND_PROPRIETARY_CORE.md) for the deeper first-principles extension, including mathematical discovery/inference alternatives and adoption experiments.

## 1. Recommendation and selection method

Build a small Python application with eight logical modules, one transactional authority per state domain, source-native artifact storage, a versioned temporal system model, one replaceable reasoning-model interface, and explicit analysis backends. Use deterministic code for accounting, permissions, time, validation, persistence and numerical execution. Use pretrained models for interpretation, hypothesis proposals and explanations. Let evidence-backed updates evolve the world model; do not equate that with retraining the LLM.

The owner-supplied diagram has conceptual/modeling relationships, modeled real-world causal interactions, and analysis/revision flows. These are not interchangeable with software calls. A modeled tree, household policy, repair crew or information channel is represented as data and mechanisms, not a new server. Likewise the represented actor's policy is distinct from EDI's own authorization policy.

Hard constraints come first: preserve evidence; retain alternatives and unknowns; maintain event/structure and observation/prediction distinctions; preserve actor-visible timing; enforce state ownership; bound resources; expose unavailable support. A candidate failing one of these cannot win because of an attractive benchmark. Then compare capability fit, inspectability, operational complexity, resource demands, portability and replacement cost. No numerical selection scores or measured speed/cost rankings are invented.

The nine Meadows representation families remain the conceptual core. The proposed eight modules are an implementation decomposition, not a replacement ontology or a new eight-layer cognitive theory. All detailed functions, ownership and node mappings are in [COMPONENTS.md](COMPONENTS.md) and [TRACEABILITY.json](TRACEABILITY.json).

## 2. Whole-system alternatives

| Approach | Useful capabilities | Important limitation for this architecture | Decision |
| --- | --- | --- | --- |
| One frontier LLM with long context and tools | Fastest conceptual prototype; broad imported knowledge; useful explanations and document synthesis. | Prompt history is not durable accounting, versioned identity, explicit uncertainty or a numerical mechanism. Long context does not enforce original expectations or evidence independence. | Keep as the strongest simple baseline and a reasoning provider, rather than the whole architecture. |
| Conventional retrieval-augmented generation | Evidence retrieval and citations with small working contexts. | Similarity does not establish identity, causal structure, applicability or intervention response. Retrieval can omit a decisive rare observation. | Use as an essential retrieval facility and matched baseline. |
| GraphRAG / LightRAG | Entity-centered retrieval and relationship-based context; GraphRAG adds community summaries. | A retrieved semantic edge has no automatic units, dynamics, causal status or execution semantics. Microsoft GraphRAG currently states maintenance mode; indexing cost must be included. | Borrow retrieval ideas; prefer a small hybrid query path before adopting a whole indexing framework. [S16–S17] |
| Graphiti temporal context memory | Incremental relationship extraction, history, provenance and hybrid retrieval. | Automatic fact invalidation/admission is not EDI's truth criterion. Application-specific n-ary mechanisms, accounting and simulation still need design. | Closest memory-framework alternative; evaluate an adapter later. Initially retain EDI-owned admission and temporal contracts. [S15] |
| Explicit system dynamics alone | Inspectable stocks, flows, feedback, delays and conditional trajectories. | Does not infer a complete structure from arbitrary observations or cover all discrete, symbolic and human processes. | Core analysis technique for applicable models, not universal encoding. [S25–S27] |
| Learned latent world model / model-based RL | Learn predictive latent state and plan from interaction; promising for recurrent visual-control environments. | Needs a defined observation/action experience distribution and learning setup. Latent rollout success does not supply audited cross-domain semantics, stakeholder values or evidence-based social mechanisms. | Research extension for visual/action domains after a justified task; not the initial shared substrate. V-JEPA 2 and DreamerV3 are representative references. [S39–S40] |
| Recommended hybrid | Combine LLM proposals, explicit temporal mechanisms, numerical/statistical tools, retrieval, prospective evidence and scoped decisions. | More engineering than model-only; integration and causal non-identifiability remain real risks. | Preferred because each requirement gets an inspectable owner and unsupported cases can remain open. Advantage must still be measured. |

## 3. Reasoning and perception models

Current catalogs were checked on 20 October 2026. Availability, revisions and pricing must be rechecked when binding a provider. These preferences are based on advertised capabilities and integration fit, not a completed EDI model tournament.

The [scalability and world-growth extension](SCALING_AND_WORLD_GROWTH.md) adds Jev as the preferred hosted candidate for qualified fast, focused typed decisions. The original assessment omitted this relevant candidate. It also separates reusable/deterministic, fast probabilistic and deliberate inquiry paths; the reasoning-provider preference below applies to deliberate interpretation/hypothesis work, not every observation or action.

| Candidate | Role and capabilities relevant here | Tradeoff | Preference / adoption condition |
| --- | --- | --- | --- |
| OpenAI `gpt-6.1-sol` | Hosted text/image reasoning and tool-oriented work; provider positions it between its flagship and low-cost tier. | External service, changing alias, billable reasoning/output, account limits and proprietary weights. | Preferred first quality-oriented reasoning provider; use the same pinned model in EDI and LLM-only comparisons. [S01] |
| OpenAI `gpt-6-luna` / `gpt-6-astra` | Advertised high-volume economy / difficult reasoning tiers respectively. | Cheap extraction can miss relationships; escalation adds cost and creates a stronger model mix unless controls match it. | Luna is an optional extraction/routing candidate; Astra is a conditional escalation candidate. Start with one provider/model to isolate architecture effects. [S01] |
| Claude Sonnet 5.5 / Opus 5.5 / Fable 5.1 | Current text/image/tool-use family; catalog distinguishes speed-oriented work, longer agentic work and demanding reasoning. | Different schema/tool adapters, service dependence and unmeasured task performance. Cross-provider critique is still correlated learned reasoning, not independent empirical evidence. | Strong alternative and later provider-robustness comparison. Do not pay for a permanent panel by default. [S02] |
| Gemini 3.8 Flash | Current multimodal and agent-oriented candidate; useful when native audiovisual handling is the selected workload. | Modality-specific timestamp grounding, account support, schema behavior and actual cost need qualification. | Preferred hosted audiovisual challenger, rather than adding a separate model for every media format. [S03] |
| Qwen3.5-9B | Open-weight multimodal candidate for controllable local/offline experimentation. | Small-model reasoning and extraction errors can dominate. Precision, context and serving engine change results. | Preferred first local candidate if local deployment is required. It does not automatically match hosted reasoning quality. [S04] |
| Qwen3.6-35B-A3B | Open-weight vision-language MoE with 35B total and 3B activated parameters. | Resident weights, caches and vision processing exceed what “3B active” suggests. Commodity GPU fit is not established. | Preferred larger open-weight challenger when hardware is measured sufficient; not a mandatory laptop dependency. [S05] |
| DeepSeek-V4 Flash / Pro | Current reasoning alternatives with long-context positioning. | Verify exact modality and structured-output behavior; do not infer them from a reasoning claim or API compatibility. Large local deployment is a separate undertaking. | Secondary text-reasoning candidate if price/quality or hosting constraints justify it. [S06] |
| TypeSafe Jev | Focused probabilistic choice/score/yes-no decisions over supplied state; independent questions can share a request. | Supplied options/context can be incomplete; type validity and concentrated confidence do not establish factual/causal correctness. Version, language, caller-region latency and EDI calibration need qualification. | Preferred fast hosted decision candidate; retains deterministic admission/authorization and an abstention/escalation route. Deep hypothesis formation stays with the deliberate reasoning path. [S52–S56, S60] |

Initial routing is deliberately simple: deterministic extraction for native structured data; a single selected model for semantic proposals; escalation only on explicit failure, ambiguity or a consequential unresolved decision. Model output contains evidence selectors, alternative claims, assumptions, applicability and proposed tests. It never writes directly to accepted model state.

Structured output reduces malformed payloads, not false claims. Validate syntax, references, units, temporal permissions, evidence basis and declared applicability independently. Record provider/model/revision when available, prompt and tool-schema hashes, decoding and reasoning settings, response/refusal/truncation status and usage. A provider alias without a stable snapshot is marked mutable. [S44, S46–S47]

Price illustration only, from S01: the catalog lists Sol at $2 input / $10 output per million tokens, Luna at $0.10 / $0.50, and Astra at $10 / $50. A hypothetical uncached 20,000-input/3,000-output Sol call is $0.07 using those two rates. That is not measured task cost: billable reasoning, tools, retries, caching, embeddings, media and hosting require separate accounting. Nothing in this task starts paid inference.

Do not fine-tune initially. First determine whether failures are caused by missing evidence, wrong identity, broken interfaces, wrong numerical semantics or a reasoning-model limitation. Consider supervised adaptation or DSPy optimization only after frozen development data, task metrics and contamination controls exist. Model weights must remain distinct from versioned world-model memory. [S24]

## 4. C0 — inquiry, scope and durable coordination

| Alternative | Capability | Tradeoff / decision |
| --- | --- | --- |
| Plain in-memory Python loop | Minimal code and direct debugging. | Loses progress across crashes; unsuitable as the only operational coordinator. |
| Explicit state machine with a Postgres job/outbox table | Durable stage identity, bounded queues, inspectable retries and one transactional store. | Requires modest workflow code and leases/fencing; preferred initial form because EDI must already define state ownership. |
| LangGraph with persistent checkpointer | Reusable graph execution/checkpoint facilities and pause/resume patterns. | Workflow memory is distinct from the shared world model. Additional checkpoint state needs retention and transactional integration. Preferred orchestration challenger when graph branching becomes costly to maintain. [S20] |
| Temporal | Durable service-level workflows and activities. | Additional server/operational surface and integration work. Adopt when multiple long-lived distributed workers, external actions and recovery requirements justify it. [S21] |
| Open-ended multi-agent debate / recursive planner | Parallel candidate generation and specialization. | Compounding token cost, duplicate evidence and correlated consensus; no inherent causal validation. Use only if a controlled ablation demonstrates added value. |

Use typed `InquirySpec`, separate causal scope and evaluative scope, and an explicit run budget. In background mode the inquiry objective can be uncertainty reduction or a qualified strategic concern; task mode adds an external question without replacing observation history. Boundary expansion follows a frontier of consequential interfaces, not recursive ingestion of the entire world. Selection and stopping are inspectable decisions.

## 5. C1/C2 — observations, interpretation and identity

| Problem | Techniques compared | Preferred choice and reason |
| --- | --- | --- |
| Native intake | Model-first universal parsing vs byte-preserving adapters vs one parser per format as a mandatory service. | Preserve original bytes and a common reference envelope; decode asynchronously. Unknown formats can be retained with `unsupported_interpretation`. This keeps capture independent of model availability. |
| Documents, tables and diagrams | Docling conversion, direct multimodal model, bespoke parsers. | Use format-native structure first; Docling as document adapter; model assistance for figures/ambiguous structure with page/region provenance. No text-only export replaces originals. [S07] |
| Image/video/artwork | Caption-only, multimodal interpretation, learned visual embeddings or latent video models. | Keep pixels/streams and time/region selectors; use the chosen vision-language model for claims. Preserve competing interpretations. V-JEPA is an optional learned-dynamics tool, not a required image intake step. [S03–S05, S39] |
| Audio/music | ASR-only, native audio model, waveform/features and symbolic MIDI/MusicXML parsing. | Preserve waveform or symbolic source; separate speech, sound, rhythm and score. Use native audiovisual model only when appropriate. Speech transcripts cannot substitute for music or arbitrary acoustic evidence. FFmpeg is a media adapter, not a semantics engine. [S03, S08] |
| Numerical/scientific/composite inputs | Flatten to prose, schema-native decoding, lossless container manifests. | Retain arrays, coordinate systems, units, sampling, ordered parts and cross-part selectors. Dedicated scientific/3D/CAD adapters are extensions; unsupported semantics remain explicit. |
| Long-term source identity | Stable authenticated source handle, timestamp/name match, embeddings, probabilistic record linkage. | Separate emitter identity/epoch, observation occurrence, payload hash, mentioned entity and physical referent. Stable handles support continuity; names and embeddings only propose links. Splink is useful for structured record linkage, not all modalities. [S09] |
| Cross-modal retrieval | Text embeddings, multimodal embeddings, late reranking. | Start with SQL metadata/text search plus Qwen3-Embedding-0.6B where semantic search is needed. Add Qwen3-VL-Embedding-2B for measured image/text/video retrieval gaps. Compare exact search before ANN. [S10–S11, S14] |

A new payload hash does not mean a new source; the same payload hash can occur in many genuine observations. A source returning after two years can be linked through a retained source identifier, epoch and history. When continuity is not supported, retain `unknown` or alternative associations instead of forcing a merge. Identity decisions are reversible assertions with downstream invalidation, not destructive edits.

First-iteration LLMs, tokenizers, feature extractors and the nine-family schema introduce priors. The current requirement is to expose those priors and their provenance. Universal prior-free perception or perfect identity recognition is not claimed.

## 6. C3 — representation substrate, history and retrieval

| Candidate | Capabilities | Main tradeoff | Decision |
| --- | --- | --- | --- |
| Vector store as memory | Similarity retrieval and small working context. | Cannot enforce identity, temporal assertions, accounting or mechanisms by similarity alone. | Secondary index only. |
| Postgres typed tables + JSONB + append-only revision/events | Transactions, constraints, explicit histories, extensible values and one operational authority. | Graph traversals and semantic bitemporality require application design; wide JSON blobs become difficult to validate. | Preferred canonical store: typed identity/time/status columns plus structured family payloads, not one untyped blob. [S12–S13] |
| Neo4j property graph | Convenient neighborhood/path queries and graph-oriented tooling. | Additional state authority/operations if introduced alongside records; property edges still need causal qualification and n-ary mechanism representation. | Add a rebuildable projection or choose it as primary only after a measured graph-query bottleneck and recovery comparison. [S18] |
| RDF/named graphs + SHACL | Interoperable vocabularies, explicit graph shapes and semantic exchange. | Reification/temporal/numerical semantics can increase modeling complexity; a shape pass is not truth. | Optional exchange/validation adapter when interoperability is required. [S19] |
| Graphiti as canonical memory | Temporal graph, extraction and retrieval already integrated. | Must adapt confidence/contradiction/identity admission, mechanisms and immutable sources rather than inherit automatic truth decisions. | Strong alternative for a bounded prototype, but direct EDI-owned records are preferred for the first controlled implementation. [S15] |

Represent multi-input relationships as first-class mechanism records with role-indexed participants, not an unexplained collection of binary edges. A graph is useful for organization, dependency and explanation; equations/rules and their domains supply predictive semantics. A delayed feedback cycle is allowed; a DAG-only schema would discard exactly the dynamics we need.

Use immutable model revisions, valid-time and known-at histories, exact source selectors, uncertainty axes and explicit assertion status. Materialized projections, summaries and embeddings are rebuildable and versioned. Query views may overlap without duplicating underlying stocks or commitments. Retrieval uses purpose/time/rights filters, keyword and semantic candidates, bounded dependency expansion and optional reranking. Record omitted frontier and truncated results. Summaries never become independent evidence.

## 7. C4 — reasoning, structural discovery and curiosity

| Method | Best fit | Limitation and preference |
| --- | --- | --- |
| Prompted Five Whys / self-reflection | Expose missing assumptions, alternative mechanisms and interface questions. | Repeated plausible answers are not evidence. Use as a bounded proposal template, stopping at unknown support. |
| ReAct-style tool use | Alternate explanation proposals with real retrieval, calculation and observation requests. | Tool access and outputs need authority and provenance. Preferred operational pattern, with explicit typed steps rather than a free-running transcript. [S22] |
| Tree search / Tree of Thoughts | Competing hypotheses or plans where branching and discriminating tests matter. | LLM self-scoring can reward the same bias and grows cost. Start with a small candidate set; branch only when outcomes justify it. [S23] |
| Tigramite PCMCI+/LPCMCI | Temporal causal candidates from suitable repeated numerical observations. | Method assumptions differ. PCMCI+ assumes no hidden confounding; LPCMCI permits latent confounding under its assumptions and can retain partial orientation. Neither gives unrestricted causal certainty. [S29] |
| DoWhy | Ask whether a specified effect is identified, estimate under a defended graph, and run refutations. | Not an oracle for missing mechanisms; many graphical formulations are acyclic. Use a justified time-unrolled causal view when suitable, never force the entire feedback world model into a static DAG. [S30] |
| PySINDy / sparse symbolic dynamics | Compact nonlinear law candidates from well-measured state and excitation. | Basis choice, hidden states, noise and numerical differentiation can bias results. Use as a specialist model proposer with out-of-regime checks. [S31] |
| Bayesian model/parameter inference | Keep parameter uncertainty and competing models; predict under explicit likelihoods. | Priors, identifiability and computational cost remain. PyMC is preferred for small scoped probabilistic mechanisms, not every record. [S32–S33] |
| Information gain / value of information | Choose observations that distinguish mechanisms and change a relevant decision. | A utility model and possible outcomes are needed; noisy novelty can be useless. Preferred curiosity principle, with a simple disagreement heuristic when probabilities are not calibrated. VIME supplies a research precedent, not a turnkey EDI algorithm. [S36, S41] |

Proposed inquiry cycle: unexpected evidence or a strategic unresolved interface → preserve the discrepancy → retrieve relevant local and wider dependencies → propose rivals including no-change/measurement/selection explanations → state different observable predictions → rank feasible tests → request permitted evidence or run a simulation → compare prospectively → revise with rationale. “Why” and “what if” are complementary tools inside this loop.

Where a defensible posterior exists, choose a test using expected information gain about mechanisms, optionally decision value, against cost and constraints. When no calibrated likelihood exists, record a heuristic `disagreement × relevance / expected_cost` rather than invent Shannon information. Raw entropy maximization is not the objective: random noise can raise entropy forever. Likewise convergence to a steady state is not universal; valid models may oscillate, evolve or remain uncertain.

Cross-system exploration is a prioritized graph frontier: link the tree ecosystem to logging, buyers, transport, prices and finance as evidence reveals consequential interfaces. Preserve the source and applicability of each connection; keep a deferred frontier for low-value or inaccessible links. A graph path is a route for questions and possible propagation, not proof of influence magnitude or sign.

## 8. C5 — executable analysis and nonlinear prediction

| Backend / technique | Useful capability | Decision and limit |
| --- | --- | --- |
| PySD | Familiar stock-flow models and imported XMILE/Vensim examples. | Preferred interoperability adapter for supported system-dynamics models; reject unsupported functions explicitly. [S25] |
| SciPy ODE integration | Explicit continuous dynamics, stiff/nonstiff methods, thresholds and numerical tolerances. | Preferred initial numerical backend behind a validated restricted mechanism representation. Root detection and integration need refinement tests; general delay equations and DAEs are not automatically supported. [S26] |
| SimPy | Discrete commitments, queues, repairs, resource contention and completion delays. | Add when a selected model needs discrete events. Co-simulation requires one clock and transfer accounting, not two independently advancing engines. [S27] |
| Mesa | Heterogeneous actors, local information and interactions. | Optional adapter when explicit heterogeneity changes the answer. It cannot supply unknown human psychological laws. [S28] |
| Qualitative constraint/sign analysis | Useful inference before coefficients are known. | Retain signed/possible effects with conditions and unknowns; do not print precise trajectories from qualitative labels. |
| Chronos-2 | Strong pretrained numerical forecasting challenger, including covariates. | Preferred statistical forecasting comparator and optional exogenous-driver model. Future covariates must actually be available at forecast time. It is not evidence for intervention causality. [S34] |
| TimesFM 3.0 / 2.5 | Additional pretrained forecasting candidates. | Current 3.0 weights have a separate non-commercial/non-production license; avoid making them a default product dependency. Consider permissible 2.5 or licensed access when appropriate. This is a concrete selection tradeoff, not a claim of model quality. [S35] |
| Neural ODE / latent recurrent world model / learned surrogate | Expressive dynamics or faster repeated rollouts after data exists. | Defer until an identified modeling bottleneck and held-out regime tests justify the added training, grounding and calibration cost. [S39–S40 are representative latent-model references] |

The initial implementation should cover one explicit numeric backend and qualitative unknowns well. Do not build a universal simulator before choosing a capability. An imported model, a new simulation and real observation retain different statuses. A response-law library is an inductive bias to disclose, not a catalog of proven world relationships.

Nonlinearity assessment includes saturation, thresholds, joint constraints, changing feedback dominance, multiple equilibria/hysteresis where supported, delayed overshoot and regime change. Separate a new operating point from changed parameters, changed rules, altered topology, changed inputs and changed measurement. Use alternative models, parameter ensembles and perturbation/sensitivity runs; a single fitted curve is insufficient.

For hybrid operation, advance continuous state only to the next discrete event, apply simultaneous changes under a specified deterministic order or simultaneous solve, account shared resources once, then restart integration. A simultaneous algebraic cycle requires an appropriate nonlinear/DAE method or `unsupported`, not a hidden topological sort. These semantics are an adoption gate for that backend.

Counterfactual language is restricted: ordinary scenario substitution is a conditional simulation. A unit-specific causal counterfactual additionally requires a justified structural causal model, observation-conditioned latent/noise inference and a consistent intervention/re-prediction procedure. Return not-identifiable when alternatives cannot be distinguished.

## 9. C6 — assessment, revision and strategic findings

Compare preserved forecasts with genuinely new or independently held-out outcomes. Use task-appropriate errors, proper probabilistic scores and calibration where distributions are supplied, temporal holdouts, source-dependence checks and decision consequence criteria. Prospective replay is preferred to narrative plausibility. A second LLM's agreement can be a critique signal, not an independent observation.

PyMC predictive checks support scoped probabilistic diagnostics; MAPIE is an optional conformal-calibration alternative when the selected method's assumptions are credible. Nonstationarity, dependence and adaptive selection can invalidate naive coverage claims. River ADWIN can flag changed stream statistics, but a drift alarm is neither a causal explanation nor automatic permission to change the accepted model. [S33, S42–S43]

Model revision, real structural change, changed policy, changed action and parameter re-estimation receive different operation types. Consolidation retains evidence and competing models; it does not average away a rare contradiction. A strategic finding must state the chain of mechanisms, affected criteria, horizon, applicability, support, uncertainty and the next discriminating observation. It can be emitted without a user question through a configured findings channel, with deduplication and a budget. It cannot create external messages or actions by itself.

## 10. C7 — actors, policies, repair and adoption

| Technique | Fit | Decision |
| --- | --- | --- |
| Versioned rules / constrained state machines | Inspectable actor-specific perceptions, memory, goals, policy, attempts and constraints. | Preferred first actor representation and EDI action gate; uncertainty remains where the actual rule is unknown. |
| Model-predictive or constrained planning | Explicit goals, bounded horizon and known dynamics. | Preferred planning extension if a selected use case needs it; CVXPY for applicable convex formulations, OR-Tools for suitable discrete constraints. Nonconvex ecology does not become convex by choosing CVXPY. [S37–S38] |
| Agent-based simulation | Heterogeneous households, firms or species with local information and interaction. | Optional Mesa adapter, with alternative behavior rules and sensitivity rather than one universal rational/hormonal human model. [S28] |
| RL / model-based RL | Repeated action and reward with sufficient controlled experience. | Defer until reward, observability, permitted action and sample budgets are justified. Dreamer is a candidate for such a domain, not a substitute for governance or evidence. [S40] |
| Always-on LLM actor for every entity | Expressive language-mediated behavior. | Expensive, nondeterministic and difficult to calibrate; reserve for an explicit experiment where it adds value. |

The modeled world may have no central controller. Represent rules, norms, physical laws, private goals and analyst criteria separately. Humans can notice a meter, ignore it, misunderstand it or have other constraints. Repair can consume scarce resources, fail, substitute another capability or generate dependency. Organization change can alter membership and interfaces while preserving existing stocks, history and commitments. These are mechanisms within C3/C5, not mandatory automatic behaviors of EDI itself.

Actual EDI external actions require an explicit authorization policy and a configured connector. Proposal, authorization, dispatch, receipt and observed effect are separate records. A receipt is not proof of effect. Initial research mode disables external actuation. Internal acceptance of a model revision is a different authority path from changing a household, institution, sensor channel or EDI's operating goal.

## 11. What we reuse, what we build, and what can replace it

Reuse storage, validation, parsers, pretrained models and mature numerical/statistical tools. Build the EDI-specific contracts: semantic/temporal evidence distinctions; versioned mechanisms and hypothesis sets; identity corrections; observation-versus-simulation boundaries; actor-visible information; inquiry selection; prospective comparison; controlled revision; and complete cost accounting.

The replaceable boundaries are model provider, parser, embedding/reranker, storage projection and analysis backend. No application requirement should depend on a vendor's hidden reasoning format, an embedding coordinate, a single graph database or a prompt transcript. Use explicit output records and evidence references.

Adopt a more complex option when a pinned comparison shows the simpler design misses a stated requirement: Neo4j for graph-query pressure; LangGraph for branching/checkpoint complexity; Temporal for distributed durability; multimodal embeddings for missed cross-modal retrieval; larger LLM for demonstrated reasoning failures; learned dynamics for useful data-supported prediction gaps. Record the measured trigger and migration plan before adoption.

The final design review, operating limits, unresolved choices and development gates are in [VERIFICATION.md](VERIFICATION.md). This assessment supports proceeding to concrete contract development after review; it does not establish intelligence, superiority, production availability or completed implementation.
