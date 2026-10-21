# Explicit systems reasoning and the pretrained student decision

Design revision 0.4, 20 October 2026. Input implementation revision: `783a4509461ee3cf66d5580f92b7e6988dcddaaa`. Status: structural design extension; not implemented, trained, tested or qualified. The owner requested the integrated structure before qualification/tests. Historical v0.3 checker reports remain historical and do not assess this extension.

The [full integrated diagram](INTEGRATED_REASONING_DIAGRAM.md) evolves the detailed seven-chapter master, retaining its 82 conceptual nodes and 241 named connections. It makes reasoning execution, student/teacher assistance and future parameter learning explicit. The original compact [owner-supplied overview](OVERVIEW.mmd) and imported v0.7 master remain preserved source snapshots. This extension is EDI engineering synthesis rather than a claim that Meadows specifies neural learning algorithms.

## 1. Decision: pretrained, fixed weights initially

| Starting point | What it contains | Initial EDI decision |
| --- | --- | --- |
| Randomly initialized model | Architecture and tokenizer choices; no acquired language/world/reasoning capabilities in the weights. | Do not use as the main first-iteration student. Teacher supervision would also need to establish general capabilities. |
| Pretrained base model | Learned language/statistical/world representations from pretraining; not necessarily adapted to instructions or EDI tool use. | Keep as an alternative for a later deliberate training study; a base model is not a prior-free model. |
| Pretrained instruction/reasoning model | General acquired capabilities plus post-training behavior suited to instructions, reasoning or tool use. | Preferred initial student, using a compatible open-weight checkpoint if local operation and future parameter training are intended. |
| Pretrained student with EDI-specific parameter adaptation | The prior capabilities plus subsequent learning from selected systems-reasoning episodes. | Preserve a separate future path; no weight updates are enabled by this diagram. |

Initial configuration: pretrained student served by vLLM, fixed student weights, versioned systems-reasoning protocol and selective teacher assistance. The teacher also uses a fixed identified pretrained version. Actual model/checkpoint selection depends on available compute, supported vLLM architecture, license and capabilities; this design does not install or bind one.

Three update mechanisms must stay distinct:

1. World-model learning changes evidence-linked representations, mechanisms, uncertainty, identity and history in C3.
2. Context/protocol changes affect the instructions and information used for a particular inference without changing neural weights. Material protocol/policy changes are versioned, with adoption authority recorded.
3. Parameter learning changes student weights or adapters through an explicit training job and adopted checkpoint. That path is future/dormant initially.

The first two permit a changing persistent world while neural weights remain fixed. No claim is made that a prompt removes pretrained priors or replaces the model's internal reasoning algorithm. Meadows-inspired operations shape how EDI uses the model and, later, the behaviors training could target.

## 2. Explicit reasoning operations

The shared protocol selects relevant operations rather than requiring every question to traverse every step:

- Separate source reports, observed events, temporal patterns, structures, mechanisms and assumptions.
- Establish referents, meaning, units, time, sampling and relevant available history.
- Trace stocks/flows, joint constraints, feedback closure, delays and pending effects where applicable.
- Inspect nonlinear domains, saturation, thresholds, heterogeneity and changes of operating regime.
- Distinguish actor information, perception, incentives, intent and actual effects from EDI's own operational policy.
- Construct rival mechanisms and preserve unclassified observations, missing alternatives and insufficient evidence.
- Form conditional predictions and feasible discriminating inquiries using supported tools.
- Expand adjacent interfaces, refine internal structure or change resolution when relevant to the inquiry.
- Compare available evidence and consequences, diagnose discrepancies and propose retain/revise/reject/investigate decisions.

Five Whys and What If are available question patterns, not fixed recursion depths or substitutes for evidence. An unanswered why becomes an attributed unknown or acquisition request; it is not filled with a plausible biological or social mechanism.

## 3. New displayed parts and existing owners

These are internal responsibilities and external dependency roles, not sixteen new software components. Existing eight logical owners and 32 functions are retained.

| Diagram node | Responsibility | Authority / allocation |
| --- | --- | --- |
| RCTX | Bounded reasoning context, model cut, evidence selectors, scope and unknowns. | C4 F40/F41 workspace derived from C1/C3 reads; not another world store. |
| RPRO | Versioned systems reasoning protocol. | C4 reasoning implementation under C7-owned adopted operational policy; C0 enforces resource limits. |
| RCTL | Inquiry and tool controller. | C4 F40-F43; submits scheduling/tool requests through C0. It does not acquire new component powers. |
| RSTU | Pretrained student served by vLLM. | Replaceable inference dependency called through the owning adapter; fixed weights initially. |
| RTEA | Selective pretrained teacher guidance. | C4-owned teacher-adapter interaction, separately attributed; no model-state admission authority. |
| RALT | Rival mechanisms and explicit unknowns. | C4 F40/F41 proposals; represented in existing C3 hypothesis/model records after admission. |
| RTEST | Discriminating inquiries and supported scenarios. | C4 F42 designs; C0 schedules, C5 executes supported analysis. |
| RPATCH | Typed interpretations and model-change proposals. | C4/C2 proposal responsibilities through existing C3 ports, with base version and evidence. |
| RADMIT | Evidence-qualified model admission and revision. | C3 F31 only. Validates references, type/semantic/authority rules and retains contested status where appropriate. |
| RFRONT | Adjacent, internal and temporal exploration frontier. | C4 F43 proposes; C0 owns scheduling/budgets and outward delivery. |
| RACCESS | Missing access requests and standing-grant reuse. | C0/C7/C1 existing request, rights and acquisition responsibilities. No C4 direct execution bypass. |
| REPIS | Attributed student attempts, teacher feedback and outcome references. | C4 retains inquiry workspace/episode metadata; C1 preserves generated payloads with generated lineage; C6 owns assessment records. |
| TCUR | Future curated training episodes. | C6 assessment/selection recommendations and C0-controlled dataset job metadata; not automatic training acceptance. |
| TTRAIN | Future student parameter training. | Separately configured training dependency invoked by C0; no trainer or model weights installed here. |
| TCKPT | Candidate model/adapter checkpoints. | C0 operational artifact/version metadata; actual weights in a configured artifact backend, never in the Git repository. |
| TADOPT | Explicit operational checkpoint adoption. | C7 F73 under configured authority; candidate status is not adopted status. No automatic live weight mutation. |

Interpretation and other functions can benefit from model assistance without routing every record through the teacher. Existing direct model adapters inside C2 may handle interpretation; cross-owner reasoning requests follow existing C0-mediated orchestration where no direct lane exists. No new C2-C4, C4-C5 or C4-C7 bypass is implied.

## 4. Interface and arrow semantics

The original diagram remains a conceptual relationship map. Its old edges are preserved, including specification edges about model revision. The added edges expose responsibilities and request/result relationships; they are not direct new APIs between every visual box.

| Relationship | Integration rule |
| --- | --- |
| C0 -> C4 and C4 -> C0 | Existing IF-04A/B: scoped inquiry, budgets, candidate patch/test/frontier/access proposals and status. |
| C1 -> C4 and C4 -> C1 | Existing IF-10A/B: record selection/payload ranges/coverage; generated teacher text remains generated evidence lineage. |
| C3 -> C4 and C4 -> C3 | Existing IF-15A/B: temporal snapshots, dependency validity and candidate patches. C3 admission remains the durable mutation boundary. |
| C4 -> C6 and C6 -> C4 | Existing IF-19A/B: assessment queries/results and inquiry-yield review; neither actor silently changes old forecasts. |
| Reasoning controller -> analysis -> controller | Requests are scheduled through C0 using existing C0-C5 contracts; results return through that workflow. There is no new direct C4-C5 lane. |
| Reasoning frontier -> access -> acquisition | Proposals reach C0; C7 handles required authority and C1 performs allowed acquisition. A request/grant is not an observation. |
| Student <-> teacher | Two directions: submitted attempt/context versus attributed critique/correction. Same named evidence cut unless an explicitly labeled pedagogic context is used. No teacher consensus becomes independent world evidence. |
| Episode -> training -> checkpoint -> serving | Future, explicit operational path. Frozen data/model/protocol provenance and authorized adoption are required. Recording an episode never causes weight training by itself. |

The conceptual actor policy nodes PI/PM/ADP describe actors inside the investigated system. TADOPT instead concerns the operational student model used by EDI. These are distinct state domains.

All 28 existing component pairs and 56 directed lanes retain their prior statuses. The displayed extension uses existing operation families; concrete model-service/trainer schemas and a future deployment topology remain unspecified. A newly independently operated service or changed lane needs its own later interface design before implementation.

## 5. Teacher guidance, training and budgets

The initial teacher gives explicit model-building critique, corrective examples, candidate edits and questions. It can be consulted for novel structures, unresolved ambiguity, consequential changes or a student escalation. Teacher and student consume one task's configured budgets; they do not receive independent unlimited recursion. Capture and known deterministic operations remain usable while teacher reasoning is pending or unavailable.

Textual feedback, supervised distillation, log-probability distillation and on-policy optimization are separate options. A hosted teacher's text output does not establish access to hidden reasoning, weights or arbitrary student-token log probabilities. Compatible scoring/tokenization/training interfaces and permitted use must be bound before a particular distillation method is chosen.

Teacher critique is fallible. It can be retained, challenged or deferred alongside student alternatives. The future learning path should preserve observation-supported mechanisms and successful alternatives instead of rewarding stylistic agreement with the teacher. No qualification, model comparison, training or benchmark is performed at this stage.

## 6. Structural status and provenance

This is an unqualified design extension following the owner's structure-first direction. Existing historical checker results apply to their pinned versions only. No new PASS verdict, tested integration, learned systems intelligence, speed or availability is asserted. Book snapshots remain byte-preserved in the repository; the new v0.8 integrated master preserves all earlier chapters and historical reviews while adding this implementation extension.

Primary references consulted on 20 October 2026:

- vLLM project: https://vllm.ai/ — inference/serving role, separate from student learning.
- Thinking Machines, On-Policy Distillation: https://thinkingmachines.ai/blog/on-policy-distillation/ — pretrained capability stages and teacher supervision of student-generated trajectories.
- Model Distillation recipes: https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/ — an example of separately configured inference/training infrastructure, not a selected mandatory provider.
- Reward-Gated On-Policy Distillation: https://arxiv.org/abs/2607.04037 — a research example of gating fallible teacher supervision.
- Rethinking On-Policy Self-Distillation: https://arxiv.org/abs/2607.05184 — task-specific findings about privileged-context training; no universal EDI result inferred.
- On-Policy Distillation Inherits the Teacher in VLMs: https://arxiv.org/abs/2610.20989 — task-specific transfer of teacher failure modes; not an EDI benchmark.

This supplements the 84-entry v0.3 research register rather than silently rewriting its audited inventory. Model provenance, protocol versions, adoption authority and the distinction between accepted world state and model parameters belong in the code structure from the beginning.
