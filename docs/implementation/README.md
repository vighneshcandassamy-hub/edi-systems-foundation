# EDI implementation architecture and technique assessment

Latest source checkpoint: code **0.9.0**, [C0 integrated workflow](C0_INTEGRATED_WORKFLOW.md): 51 native operation mappings, durable plans/inputs/step intents/results, bounded references, separate operator decisions, acceptance conditions and internal findings. [Trace](INTEGRATION_TRACE.json) allocates eleven coordination requirements and twenty-four unrun cases; [readiness](INTEGRATION_READINESS.md) separates actual source from unbound native models. The [holistic test design](INTEGRATED_TEST_DESIGN.md) is proposed, not executed. Latest owner instruction explicitly defers all testing/runtime execution. C0-C7 remain partial/unqualified; native inference, broader capability and scientific/production acceptance remain open. Earlier source/research assets retain their scopes and historical evidence.

Research specification version 0.3 — 20 October 2026. The research below retains its original proposed status. A subsequent [shared foundation/C1 code increment](FOUNDATION_C1_RUNTIME.md), code version 0.2.0, implements a limited local path without qualification. Start with [the model/technique tradeoffs](TRADEOFFS.md), then [component specifications](COMPONENTS.md) and [contracts](CONTRACTS.md).

The next [C3 world-hosting increment](C3_WORLD_RUNTIME.md), code version 0.3.0, adds concrete nine-family records, versioned candidate/admission history, C1 evidence correspondence and bounded revision/dependency views. It retains deferred qualification and does not implement the full substrate/discovery specification. [ADR-004](../decisions/ADR-004-versioned-world-hosting.md) records this scope.

The owner-requested [full integrated reasoning diagram](INTEGRATED_REASONING_DIAGRAM.md) and [reasoning/model decision](REASONING_INTEGRATION.md) are a separate v0.4 structural extension. They retain all detailed seven-chapter nodes, add explicit student/teacher guidance and a dormant future training path, and recommend fixed pretrained weights initially. Historical v0.3 qualification/checker reports do not assess this unqualified extension.

Start with the [consolidated architecture, tools and mathematics reference v1.0](ARCHITECTURE_TOOLS_AND_MATH_REFERENCE.md). It distinguishes the agreed structure, initial engineering preferences, conditional methods and open bindings without treating all researched tools as selected dependencies.

## Recommendation

Use a hybrid architecture: a replaceable LLM proposes interpretations and testable mechanisms; a typed temporal world model retains evidence, alternatives, nonlinear laws and history; appropriate numerical/causal tools execute scoped tests; independent outcomes support explicit revision. Start with a modular Python application, Postgres, source-native artifact storage and one selected reasoning provider. Add specialist frameworks only when a requirement and measured limitation justify them.

Current model roles follow REASONING_INTEGRATION.md: a compatible pretrained instruction/reasoning student served by vLLM, fixed weights initially, and a separate selectively used pretrained teacher. Exact checkpoints/providers remain open. The earlier hosted GPT-6.1 Sol and Qwen/Claude/Gemini/DeepSeek shortlist remains researched alternatives; a hosted closed-weight teacher/development candidate is not automatically the local vLLM student. No provider winner or performance advantage is established.

The speed and cumulative-world extension is specified in [Scaling and world growth](SCALING_AND_WORLD_GROWTH.md), with a [proposed intrinsic inquiry policy](GROWTH_POLICY.json). It adds qualified Jev fast decisions, incremental projections, breadth/depth/refinement/temporal growth and bounded access requests. FAST1 latency targets remain unmeasured. Deep reasoning retains the deliberate path above.

The [tools and proprietary-core assessment](TOOLS_AND_PROPRIETARY_CORE.md) and [machine decision catalogue](TOOLS.json) compare 24 choices, eight prospective adoption experiments and the mathematical mechanisms we should own. P0/P1/P2/P3 separate the initial stack, capability extensions, measured infrastructure growth and research.

## Complete specification package

| Asset | Contents |
| --- | --- |
| [Consolidated reference v1.0](ARCHITECTURE_TOOLS_AND_MATH_REFERENCE.md) | Agreed architecture/model direction, complete starting and conditional tool catalogue, 22 mathematical techniques, original EDI assets, integration rules, source map and open bindings. |
| [Tradeoffs](TRADEOFFS.md) | Whole-system alternatives; current reasoning/perception models; parsing, identity, retrieval/storage, orchestration, curiosity, causal inference, numerical/latent world models, uncertainty and policy/planning choices. |
| [Component specifications](COMPONENTS.md) | Eight logical owners, 32 functions, nine representation families, inputs/outputs/state/authority/failures and capability-by-capability integration. |
| [Contracts](CONTRACTS.md) | Proposed typed records, admission semantics, operation families, identity/time/delivery/recovery/retention/resource rules, shared dependencies and composed feedback paths. |
| [Directed interface catalogue](INTERFACES.json) | All 28 unordered component pairs / 56 directed lanes; 40 required operation/result contracts and explicit justified no-links/prohibited bypasses; eleven contract facets and a whole-system feedback review. |
| [Traceability catalogue](TRACEABILITY.json) | All 42 nodes / 69 connections in the supplied overview; 54 I7 requirements, 20 appendix requirements, 43 retained observation/substrate requirements, eight downstream obligations and 16 EDI system requirements, allocated through 34 implementation requirements and 32 functions to prospective cases. |
| [Verification and critical review](VERIFICATION.md) | 48 proposed cases; finite DEV1 profile and later HA profile; matched controls, failure analysis, KISS/Five Whys/MECE review, adoption conditions and development sequence. |
| [Primary-source register](SOURCES.md) / [machine register](SOURCES.json) | 84 primary references checked during the research, with the narrow support and limitations used for decisions. |
| [Scope](RESEARCH_SCOPE.md) / [preserved supplied overview](OVERVIEW.mmd) | Research boundary and the exact node/edge content of the owner's overview. |
| [Component self-review](evidence/component-review.json) / [document checks](evidence/document-checks.json) / [interface checks](evidence/interface-checks.json) | Scoped review and checker results. These are documentation evidence, never successful runtime or intelligence tests. |

## Authority and interpretation

Input repository baseline: `830b6ee5384b1c9a6cbd723f94cb8bd5bb3e353a`. The [seven-chapter master](../../architecture/world-model/Meadows_Chapters_1_2_3_4_5_6_7_Integrated_Architecture_Audit_v0_7.md) and [appendix reference](../../architecture/reference/Meadows_Appendix_187_203_Semantic_Foundation_Reference_v1_0.md) remain the unchanged conceptual/semantic authorities. The provided overview is a compact presentation, not a replacement for the detailed conceptual master or its 346 catalogue allocations.

Eight software modules are not eight new cognitive primitives or a service per diagram box. Domain state, model state and EDI operational state are distinct. Structural priors, imported pretrained knowledge and uncertainty remain visible. A graph edge does not supply an executable causal mechanism, and a fit to one behavior does not identify a unique system structure.

This is the new prospective implementation proposal. Historical plans/reviews retain their original status. Architecture consistency is separate from concrete schema/contract readiness, runtime integration, scientific evidence and production capacity. Existing model scenarios and all new product cases remain planned and unrun.

## Check the documentation

```text
python scripts/check_implementation_docs.py
python .agents/skills/edi-interface-review/scripts/interface_matrix.py docs/implementation/INTERFACES.json --root .
python .agents/skills/edi-component-review/scripts/review_gate.py docs/implementation/evidence/component-review.json --root .
python scripts/verify_baseline.py
```

Extension input revision: `2af45f59169ec3855f10a8861d6e6acc4c8cfb07`. The next implementation artifact is the concrete typed contracts, including ModelDelta, projection validity, RefinementBridge and KnowledgeRequest, and one source/identity/time fixture for the first chosen capability. No runtime build or inference benchmark was started in this assessment.


## Active single-reasoner configuration — 25 October 2026

The owner selected the current assistant as EDI's sole C4 reasoning model, with teacher disabled and explicit native proposal exchange. [Single-assistant connection](SINGLE_ASSISTANT_REASONER.md) records the active configuration and its qualification limits. Historical teacher/student source snapshots remain preserved.
