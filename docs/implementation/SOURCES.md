# Primary-source register

Research cutoff: 20 October 2026. These are official project/provider documents, standards, original model cards and research papers. Live pages can change; binding exact package/checkpoint revisions remains an implementation entry condition. Vendor benchmark rankings and advertised latency are not adopted as EDI results. Older papers are representative architectural alternatives, not assertions that no newer paper exists. No exhaustive worldwide SOTA search is claimed.

Recommendations and limitations in this design are engineering judgments unless explicitly attributed. This register records narrow support, rather than importing every marketing assertion from a source. No third-party source text or weights are copied into the repository.

| ID | Primary reference | What it supports and its limit |
| --- | --- | --- |
| S01 | [OpenAI model catalog](https://developers.openai.com/api/docs/models) | Current hosted reasoning/vision model IDs and advertised price tiers; provider claims, not EDI measurements. |
| S02 | [Claude model overview](https://platform.claude.com/docs/en/models/overview) | Current reasoning, vision and tool-use lineup; vendor latency labels are not matched EDI measurements. |
| S03 | [Gemini model catalog](https://ai.google.dev/gemini-api/docs/models) | Current multimodal model lineup and endpoint names; verify account and regional availability at binding. |
| S04 | [Qwen3.5-9B model card](https://huggingface.co/Qwen/Qwen3.5-9B) | Small open-weight multimodal candidate; deployment and task quality require qualification. |
| S05 | [Qwen3.6-35B-A3B model card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | Vision encoder plus language model, 35B total/3B active parameters; active parameters do not determine resident weight memory. |
| S06 | [DeepSeek-V4 preview](https://deepseek.com/en/news/v4-preview/) | Pro/Flash reasoning alternatives and API IDs; do not infer unlisted modality support. |
| S07 | [Docling supported formats](https://docling-project.github.io/docling/usage/supported_formats/) | Structured document conversions; source-native retention remains necessary. |
| S08 | [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html) | Media stream conversion; explicit stream/time mapping is an EDI contract. |
| S09 | [Splink documentation](https://moj-analytical-services.github.io/splink/index.html) | Probabilistic linkage for structured records; not universal cross-modal physical identity. |
| S10 | [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | Text embeddings; retrieval representation must remain versioned and separate from identity. |
| S11 | [Qwen3-VL-Embedding-2B](https://huggingface.co/Qwen/Qwen3-VL-Embedding-2B) | Multimodal retrieval candidate; alignment is not causal or identity proof. |
| S12 | [PostgreSQL JSON types](https://www.postgresql.org/docs/current/datatype-json.html) | JSON/JSONB storage; preserve original bytes outside normalized JSONB. |
| S13 | [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | Transaction semantics and retry obligations; bitemporal semantics are application-owned. |
| S14 | [pgvector](https://github.com/pgvector/pgvector/blob/master/README.md) | Exact/approximate vector search and filtered-recall considerations. |
| S15 | [Graphiti](https://github.com/getzep/graphiti/blob/main/README.md) | Incremental temporal context graphs and provenance; automatic invalidation needs EDI admission controls. |
| S16 | [Microsoft GraphRAG](https://github.com/microsoft/graphrag) | Graph-oriented retrieval/indexing; repository currently states maintenance mode and indexing cost caution. |
| S17 | [LightRAG](https://github.com/HKUDS/LightRAG) | Alternative graph-assisted retrieval implementation; not an executable dynamics engine. |
| S18 | [Neo4j graph database](https://neo4j.com/docs/getting-started/graph-database/) | Property graph representation and traversal; does not supply response laws by itself. |
| S19 | [W3C SHACL](https://www.w3.org/TR/shacl/) | RDF shape validation; shape validity is distinct from empirical truth. |
| S20 | [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Thread checkpoints versus cross-thread stores; neither defines EDI knowledge admission. |
| S21 | [Temporal workflows](https://docs.temporal.io/workflows) | Durable workflow service alternative for later operational complexity. |
| S22 | [ReAct](https://arxiv.org/abs/2210.03629) | Research pattern for interleaving reasoning and tool actions; not a guarantee of true mechanisms. |
| S23 | [Tree of Thoughts](https://arxiv.org/abs/2305.10601) | Explicit branching/search alternative; token and evaluation costs need controls. |
| S24 | [DSPy](https://arxiv.org/abs/2310.03714) | Program/prompt optimization alternative once reliable development examples and metrics exist. |
| S25 | [PySD](https://pysd.readthedocs.io/en/master/) | Vensim/XMILE translation and system-dynamics simulation, with documented unsupported functions. |
| S26 | [SciPy solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html) | ODE methods, event roots, stiff/nonstiff distinctions; not a universal delay/DAE solver. |
| S27 | [SimPy](https://simpy.readthedocs.io/en/latest/) | Discrete-event process simulation; continuous and hybrid coupling must be specified separately. |
| S28 | [Mesa](https://mesa.readthedocs.io/latest/) | Agent-based modeling; modeled humans need evidence-qualified rules. |
| S29 | [Tigramite](https://github.com/jakobrunge/tigramite) | Time-series causal discovery with method-specific assumptions, including stationarity and confounding distinctions. |
| S30 | [DoWhy](https://github.com/py-why/dowhy) | Causal effect identification, estimation and refutation under explicit assumptions. |
| S31 | [PySINDy](https://pysindy.readthedocs.io/en/stable/) | Sparse nonlinear system identification; library and measurement choices are priors. |
| S32 | [PyMC overview](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html) | Bayesian modeling and inference; prior/likelihood specification remains a modeling obligation. |
| S33 | [PyMC predictive checks](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/posterior_predictive.html) | Prior/posterior predictive checks; a good fit does not uniquely identify structure. |
| S34 | [Chronos forecasting](https://github.com/amazon-science/chronos-forecasting) | Chronos-2 pretrained numerical forecasting, including covariates; not causal intervention evidence. |
| S35 | [TimesFM](https://github.com/google-research/timesfm) | Current repository lists TimesFM 3.0 with separately restricted weights; 2.5 weights retain Apache-2.0 per repository notice. |
| S36 | [BoTorch](https://botorch.org/) | Bayesian optimization and acquisition functions; EDI experiment utility and constraints must be supplied. |
| S37 | [CVXPY](https://www.cvxpy.org/) | Convex optimization modeling; nonlinear nonconvex dynamics require an appropriate alternative or qualification. |
| S38 | [OR-Tools](https://developers.google.com/optimization) | Constraint/discrete optimization candidate; model feasibility is not real-world feasibility. |
| S39 | [V-JEPA 2](https://arxiv.org/abs/2506.09985) | Representative latent video prediction/planning research; scope does not establish a general social/ecological world model. |
| S40 | [DreamerV3](https://arxiv.org/abs/2301.04104) | Representative learned world-model RL across task environments; reward, experience and interface assumptions still apply. |
| S41 | [VIME](https://arxiv.org/abs/1605.09674) | Information-gain exploration research; does not prescribe EDI's multi-objective inquiry scheduler. |
| S42 | [MAPIE](https://github.com/scikit-learn-contrib/MAPIE) | Conformal prediction intervals and risk-control tooling; guarantees depend on the chosen method and assumptions. |
| S43 | [River ADWIN](https://riverml.xyz/latest/api/drift/ADWIN/) | Adaptive-window drift detector; an alert does not identify a causal change. |
| S44 | [Pydantic strict mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/) | Typed boundary validation; schema correctness does not establish semantic or causal correctness. |
| S45 | [Pint](https://pint.readthedocs.io/en/stable/) | Units and dimensional calculations; source interpretation and conversions must remain explicit. |
| S46 | [vLLM structured outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/) | Constrained-output serving candidate; syntax compliance is not factual validation. |
| S47 | [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | Schema-constrained output capability; refusal, truncation and semantic validation require handling. |
| S48 | [OpenTelemetry](https://opentelemetry.io/docs/) | Operational observability; use complete path cost and failure accounting. |
| S49 | [SQLAlchemy](https://docs.sqlalchemy.org/en/20/intro.html) | SQL Core/ORM persistence tooling; inspected documentation identifies 2.1 as current and 2.0 as maintenance. |
| S50 | [Alembic](https://alembic.sqlalchemy.org/en/latest/) | Versioned SQL schema migrations; EDI model-semantic migration is a separate operation. |
| S51 | [FastAPI](https://fastapi.tiangolo.com/) | Optional HTTP boundary; an in-process port remains the first implementation form. |


## Version 0.2 growth and decision-speed references

| ID | Primary reference | What it supports and its limit |
| --- | --- | --- |
| S52 | [TypeSafe Jev release and benchmark qualifications](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | Vendor-reported focused-decision latency and evaluation qualifications, including geography and request/workflow construction; not EDI measurements. |
| S53 | [TypeSafe decision primitives](https://docs.typesafe.ai/primitives) | Focused typed judgments, known choices, independent questions and dependent follow-ups; bounded output type does not establish causal truth. |
| S54 | [TypeSafe state](https://docs.typesafe.ai/concepts/state) | Shared structured state for independent judgments; choose only relevant grounded context. |
| S55 | [TypeSafe confidence](https://docs.typesafe.ai/confidence) | Confidence is computed from the output distribution; application thresholds and model behavior require task-specific validation. |
| S56 | [TypeSafe speculative fan-out](https://docs.typesafe.ai/patterns/fan-out) | Batching independent potential questions; dependency chains and total request budget remain relevant. |
| S57 | [Materialize fundamentals](https://materialize.com/docs/fundamentals/) | Incrementally maintained streaming results, built on Timely/Differential Dataflow; optional infrastructure, not EDI model semantics. |
| S58 | [PostgreSQL table partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html) | Physical table partitioning/pruning under compatible workloads; no automatic graph-sharding or universal latency guarantee. |
| S59 | [PostgreSQL materialized views](https://www.postgresql.org/docs/current/rules-materializedviews.html) | Persisted query results and explicit refresh; not automatic incremental maintenance of an evolving world model. |
| S60 | [TypeSafe models and version aliases](https://docs.typesafe.ai/models) | Versioned releases versus moving aliases, request shape and limits; bind and qualify the actual provider model/version before execution. |

## Tools and original-core research extension

Primary sources S61-S84 add mathematical/development candidates. Failed or redirecting documentation routes are noted in TOOLS_AND_PROPRIETARY_CORE.md; working primary repositories/standards were used. No candidate was installed or benchmarked.

| ID | Primary reference | Narrow support and limitation |
| --- | --- | --- |
| S61 | [uv workspace documentation](https://docs.astral.sh/uv/concepts/projects/workspaces/) | Shared lockfile/workspace behavior and limits when package environments conflict. |
| S62 | [Ruff documentation](https://docs.astral.sh/ruff/) | Python linting/formatting; development tool performance is not EDI runtime performance. |
| S63 | [Hypothesis stateful tests](https://hypothesis.readthedocs.io/en/latest/stateful.html) | Generated state-machine operation sequences for invariant/recovery tests; no scientific correctness guarantee. |
| S64 | [Diffrax getting started](https://docs.kidger.site/diffrax/usage/getting-started/) | JAX differential-equation tools including ODE/SDE/CDE; exact operators and numerical semantics need binding. |
| S65 | [NumPyro getting started](https://num.pyro.ai/en/stable/getting_started.html) | JAX-based probabilistic inference including MCMC and variational methods; model/likelihood assumptions remain explicit. |
| S66 | [sbi documentation](https://sbi.readthedocs.io/en/latest/) | Simulation-based parameter inference; posterior quality depends on simulator, prior and training/validation. |
| S67 | [SALib documentation](https://salib.readthedocs.io/en/latest/) | Morris, Sobol and other sensitivity methods; their input-dependence assumptions need qualification. |
| S68 | [PySR project](https://github.com/astroautomata/PySR) | Symbolic expression search with a Julia backend; an equation fit does not identify causal structure. |
| S69 | [SUNDIALS IDA documentation](https://sundials.readthedocs.io/en/latest/ida/) | DAE solver family; backend bindings, initialization, operator capabilities and platform support are not established by reading documentation. |
| S70 | [SymPy project](https://www.sympy.org/en/index.html) | Symbolic mathematics as a reusable backend, not an EDI model authority or empirical validator. |
| S71 | [Z3 guide](https://microsoft.github.io/z3guide/docs/logic/intro/) | Logical formula satisfiability under supported theories; formal consistency is distinct from external truth. |
| S72 | [Polars documentation](https://docs.pola.rs/) | Columnar data manipulation and lazy/streaming execution; measure actual query, memory and copy costs. |
| S73 | [DuckDB project](https://github.com/duckdb/duckdb) | Embedded analytical SQL and file analysis; proposed read/analysis role, not a duplicate authoritative world store. |
| S74 | [Modelica language specification 3.6](https://specification.modelica.org/maint/3.6/) | Equation-based composition interoperability reference; this cited version is not claimed to be the newest release. |
| S75 | [libRoadRunner documentation](https://libroadrunner.readthedocs.io/en/latest/) | SBML simulation candidate; inspected landing docs are older and explicitly exclude algebraic rules and delay equations, so installed capabilities must be qualified. |
| S76 | [JAX thinking in JAX](https://docs.jax.dev/en/latest/notebooks/thinking_in_jax.html) | Array JIT and shape restrictions; warm-up/shape change costs matter for an evolving world. |
| S77 | [PyO3 user guide](https://pyo3.rs/) | Rust/Python extension interface for profiled kernels; no automatic whole-system speedup. |
| S78 | [pytest documentation](https://docs.pytest.org/en/stable/) | Fixtures and functional test execution; infrastructure checks do not establish intelligence. |
| S79 | [Pyright project](https://github.com/microsoft/pyright) | Python static typing; type checking is separate from semantic/evidence validation. |
| S80 | [SBML specifications](https://sbml.org/documents/specifications/) | Systems-biology model exchange standards; each imported model and operator subset needs provenance and qualification. |
| S81 | [CasADi documentation](https://web.casadi.org/docs/) | Differentiation, numerical optimization and ODE/DAE/control building blocks; existing models may require a different encoding. |
| S82 | [SciPy bounded nonlinear least squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) | Bounded local residual optimization; a local optimum does not establish identification or a correct mechanism. |
| S83 | [NetworkX documentation](https://networkx.org/documentation/stable/) | Reference graph analysis algorithms; not selected as the durable full-world memory representation. |
| S84 | [DSPy project](https://github.com/stanfordnlp/dspy) | A language-model programming framework candidate; task metrics, optimization splits and original outcome evidence remain EDI responsibilities. |
