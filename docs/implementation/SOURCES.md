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

