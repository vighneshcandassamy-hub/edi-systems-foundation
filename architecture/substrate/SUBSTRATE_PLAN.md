# EDI substrate: functional retrospective and brainstorming baseline

Date: 2026-10-19 (Asia/Calcutta). Status: proposed functions and draft derived requirements, architecture REVISE.
Scope: review the eight conversational functions; define a simpler functional baseline for brainstorming and cross-check the complete supplied Meadows book. This historical functional baseline is extended by the linked blueprint; native learning rules and concrete contracts remain open. No substrate implementation or scientific qualification is claimed.

Current source review: [MEADOWS_REVIEW.md](MEADOWS_REVIEW.md). Page-by-page dispositions: [MEADOWS_PAGE_REVIEW.md](MEADOWS_PAGE_REVIEW.md). Draft component requirements: [REQUIREMENTS.json](REQUIREMENTS.json). All 235 PDF pages are accounted for; review covers extracted text and available labels/captions, with image-only cover metadata and visual/numerical limits explicit. The earlier selected-passages cross-check below is preserved as history.

## Capability and boundaries

The substrate is an individual EDI component with the capability to host persistent, revisable, semantic-neutral representations and their interactions. Multiple functions implement that capability. The ten-capability catalogue is a functional view; it does not replace component decomposition.

The observation component remains the authority for received native evidence and operational acquisition identity. The substrate references that evidence and hosts developing organization, interpretations and their histories. Missing or expired evidence remains explicitly unavailable. A substrate identity is not proof of physical identity.

Questioning needs executable substrate support: addressable relationships/interfaces, interaction traces, alternatives, controlled candidate changes, and revision records. The current blueprint proposes an internal inquiry coordinator and an optional reasoning-model adapter; its exact native learning rules remain to select. The substrate must not become passive storage by definition, nor should every semantic reasoning function be assigned to it without justification.

## Six proposed functions

| ID | Function | Required behavior | Parent system requirements | Prospective checks |
| --- | --- | --- | --- | --- |
| SUB-F001 | Form and compose | Instantiate representations of structures and their states from evidence or declared transformations; preserve order, composition, overlap, context and scale; permit compositions containing compositions without assuming additive behavior. | EDI-SYS-002, EDI-SYS-003, EDI-SYS-004 | SUB-V001, SUB-V007, SUB-V009, SUB-V013 |
| SUB-F002 | Connect and interact | Host relationships/interfaces and declared or proposed interaction/update rules. Distinguish exchange direction, response sign, changing strength and loop behavior; support delayed, nonlinear, multi-party and feedback mechanisms with explicit unknowns. | EDI-SYS-004, EDI-SYS-005, EDI-SYS-006, EDI-SYS-016 | SUB-V002, SUB-V007, SUB-V009, SUB-V010, SUB-V011, SUB-V015, SUB-V021 |
| SUB-F003 | Evolve and reorganize | Maintain continuity while changing state, structure, context boundaries and dependencies. Distinguish state, parameter, organization and policy changes; preserve history, authority and unchanged alternatives. | EDI-SYS-004, EDI-SYS-008, EDI-SYS-009 | SUB-V003, SUB-V008, SUB-V010, SUB-V012, SUB-V016, SUB-V019, SUB-V020 |
| SUB-F004 | Ground and preserve alternatives | Connect claims and changes to evidence, methods and versions. Retain qualitative/quantitative uncertainty, conflicts, hidden state, selection/exposure history and rival interpretations; distinguish measured, inferred, imported, simulated and actual substrate state. | EDI-SYS-003, EDI-SYS-005, EDI-SYS-006, EDI-SYS-014 | SUB-V004, SUB-V007, SUB-V012, SUB-V014, SUB-V017, SUB-V018, SUB-V022 |
| SUB-F005 | Enable inquiry and comparison | Expose bounded inspection, candidate changes and reproducible conditional predictions. Question mechanisms, assumptions, boundaries and attention allocation; preserve goal/constraint/evaluation authority, complete outcomes and measured-action distinctions. | EDI-SYS-005, EDI-SYS-007, EDI-SYS-010, EDI-SYS-016 | SUB-V005, SUB-V008, SUB-V014, SUB-V016, SUB-V017, SUB-V018, SUB-V019, SUB-V021, SUB-V022 |
| SUB-F006 | Persist and bound resources | Provide declared durability/recovery and bounded access/update work. Expose shared costs, overload, failed work and unavailable history; justify retention/compression including rare structures and recovery needs. | EDI-SYS-009, EDI-SYS-013, EDI-SYS-014, EDI-SYS-015 | SUB-V006, SUB-V008, SUB-V020 |

Parent requirement authority: [observation/REQUIREMENTS.json](../observation/REQUIREMENTS.json), mission EDI-MIS-001. The mission/system requirements currently live there; this document does not relocate or silently alter that catalogue. Functions support system requirements without claiming to fulfill them alone. Sixteen draft derived component requirements are recorded in [REQUIREMENTS.json](REQUIREMENTS.json); six proposed specifications are allocated in the blueprint, while executable contracts remain pending. The component catalogue is the detailed allocation authority where the summary table above omits supporting links.

Previous eight-function mapping: instantiate plus composition -> F001; relationships -> F002 (expanded to interaction); identity/continuity plus reorganization -> F003; evidence/alternatives -> F004; exposure -> F005 (expanded to inquiry support); persistence/resources -> F006. These are responsibilities, not six mandated services or mutually exclusive mechanisms.

## Interfaces and interaction

Input, output and bidirectional describe permitted flow relative to a named representation boundary and context. The boundary may be a part, a composite or a larger organization. Actual activity and inferred world relationships have different evidential status.

An interface must be able to distinguish its participants and boundary, permitted direction, exchanged structure or state change, relevant context/time, and the evidence/method supporting its interpretation. These are logical concerns, not a finalized mandatory-field schema. Unknown direction must not silently become bidirectional. Absence of an observed interaction must not become proof that an interface cannot exist.

Interface direction is not causal proof. Symmetric similarity, co-occurrence, equivalence and containment need not be expressed as causal input/output paths. Relationships may involve more than two participants or have delayed/context-dependent effects. Bidirectional flow does not mean equal influence in both directions.

Interfaces must be expressible at nested levels when useful, without allocating a separate active port for every pixel, pair or hypothetical connection. Internal software operations and represented world interfaces must remain distinguishable. The eventual execution rules must bound cycles, propagation and concurrent changes.

## Growing organization

The component should permit a growing interconnected organization with reusable substructures, overlapping views and larger composites. It should also preserve disconnected regions and rival interpretations. Shared evidence alone does not justify merging identities or treating rival hypotheses as simultaneous facts. Recursive composition must preserve access to supporting detail and declare any information lost by compression.

No forced single giant representation, fixed hierarchy or universal graph/vector/field primitive is imposed. The blueprint proposes an addressable record-and-relation host with native views as a declared structural prior. Existing substrate iterations are candidate sources; their narrower qualified contracts do not establish this new component's capability.

## Questioning as an operational loop

1. Detect a reason to inspect a structure: new contradictory evidence, prediction mismatch, changed context, unresolved alternatives or a scheduled bounded review.
2. Inspect the evidence and assumptions supporting the affected relationship/interface.
3. Construct credible alternatives: retain unchanged, revise, split, combine, reverse a proposed direction, retract, or leave unresolved.
4. Identify what observations or permitted tests could distinguish those alternatives. Predict candidate consequences with explicit assumptions.
5. Prioritize investigation using a declared policy balancing expected information/decision value and cost. Defer or stop when available evidence cannot distinguish alternatives or further effort is not justified.
6. Compare subsequent evidence and revise only as warranted. Record provenance and affected dependencies, including failed proposals.

This is a proposed functional loop, not a selected algorithm or a claim that uncertainty can already be estimated accurately. Continuous means persistent readiness and revisitation, not uninterrupted model calls. An LLM's explanation is a proposal with imported training priors; repetition or internal agreement is not independent corroboration. Simulated what-if outcomes remain conditional on their model. External interventions pass through the system's action authority, not through an inferred relation alone.

## First-principles retrospective

KISS: combine overlapping responsibilities, keep six functions, avoid one-service-per-function and all-to-all interaction, retain one received-evidence authority. A plain append-only representation store is the simplest alternative; it covers persistence but leaves interaction, organization and inquiry semantics unspecified. Selecting a richer mechanism needs the next architecture discussion.

Five Whys rationale chain: revisable knowledge needs organization to change; changing organization can affect dependent relationships; dependent effects require explicit interfaces and traces; traces need evidence and versioned changes; evidence/versioning permits evaluation and correction without rewriting observations. This is engineering rationale, not measured causal evidence for intelligence.

Waterfall and return: mission -> system requirements -> the six functions -> pending substrate requirements/specs -> pending contracts -> implementation -> prospective checks -> scoped capability evidence. A functional review cannot pass the later architecture/runtime gates.

Coverage review: construction/composition, interaction, reorganization, epistemic grounding, inquiry access and operational continuity cover the requested responsibilities at this abstraction. They interact and are not claimed to be mutually exclusive. Direction, temporal scope, evidence status and implementation state are separate axes.

Bias: avoid mandatory domain ontologies and opaque semantic routing. Declare primitive structures, update laws, proposal generators, inquiry objectives, imported encoders/models and thresholds. Structural choices cannot be assumption-free. Neutral naming alone does not establish neutral behavior; future controlled checks must examine relabeling, ordering, chosen topology and imported features where relevant.

Do not equate more connections, more questioning, lower uncertainty or a quieter state with more accurate intelligence. Allow open alternatives, noise, regime change and evidence-supported stability. Evaluate useful revision and prospective consequences, including null cases.

## Risks and prospective verification

| Check | Risk/condition | Required demonstration | State |
| --- | --- | --- | --- |
| SUB-V001 | Composition erases detail or forces incompatible modalities together | Retain selectable evidence/detail and alternate views through recursive composition; loss is declared. | Not run |
| SUB-V002 | Direction is mistaken for causation; feedback loops run unbounded | Exercise asymmetric, bidirectional, symmetric, unknown, delayed and multi-party cases; bounded interaction and distinct causal status. | Not run |
| SUB-V003 | False merge or stale dependency corrupts later knowledge | Split/retract a mistaken association, retain prior history, identify affected derived structures without rewriting raw evidence. | Not run |
| SUB-V004 | LLM explanation or repeated derivation becomes false independent support | Preserve producer/model lineage and shared-evidence dependencies; rival claims remain distinguishable. | Not run |
| SUB-V005 | Endless questioning or unnecessary churn | No-effect/indistinguishable alternatives can remain unchanged or unresolved; inquiry yields to explicit cost/authority limits. | Not run |
| SUB-V006 | Resource exhaustion or interrupted update leaves inconsistent structure | Declared workload/fault profiles demonstrate atomic or explicitly incomplete changes, bounded retrieval and recovery. Profiles pending. | Not run |
| SUB-V007 | Supplied names, features or topology covertly determine meanings | Controlled relabeling/feature/topology audits appropriate to the selected mechanism, with known structural priors recorded. | Not run |
| SUB-V008 | Candidate branch or outdated writer overwrites committed experience | Separate trial and committed state; stale updates, duplicates, concurrent revisions and missing evidence are handled explicitly. | Not run |

Observation obligations DOWN-001 through DOWN-008 remain required: claims versus facts (F004), unknown coverage (F004), correction/time/version (F003), bounded retrieval (F005/F006), imported feature compatibility (F001/F004), budgeted selective acquisition (F005), durability (F006) and full-task cost accounting (F006). Inquiry policies and action execution remain collaborative obligations for their own components.

## Earlier selected-passages cross-check against Thinking in Systems

Source: owner-supplied Donella H. Meadows, Thinking in Systems, edited by Diana Wright, copyright 2008. Source file Meadows-2008.-Thinking-in-Systems(2).pdf, 235 PDF pages, 2,700,340 bytes. Reference file ID: file_00000000a8348211abb1e4687542efb1. This earlier review used selected passages and is superseded in coverage by [MEADOWS_REVIEW.md](MEADOWS_REVIEW.md). Printed page numbers are 17 less than PDF page numbers in the body sections.

This is a conceptual coverage source, not evidence that a proposed AI mechanism works. The corrections below are our engineering inferences from the inspected passages, not a substrate architecture prescribed by Meadows. No copy of the supplied book is added to the repository.

| ID | Gap or under-specification in the initial six-function proposal | Proposed correction and function allocation | Source passages inspected |
| --- | --- | --- | --- |
| SUB-G001 | Parts and connections were clearer than their changing state. | Distinguish representation identity, state, accumulation and change; preserve units when supplied and unknown units otherwise. F001/F002. | Printed pp. 17-18; PDF 34-35. |
| SUB-G002 | In/out/bidirectional described access but not what an interaction does. | Support exchange content, rate, transition rules, delay, context and higher-order conditions; do not assume pairwise additive effects. F002. | Printed pp. 13-14, 25-27, 91-94; PDF 30-31, 42-44, 108-111. |
| SUB-G003 | Recorded time did not explicitly require representable delayed and history-dependent behavior. | Preserve event/receipt/model time distinctions and allow memory, asynchronous observations and multiple time scales; same observed present need not imply the same inferred state. F002/F003/F004. | Printed pp. 103-105; PDF 120-122. |
| SUB-G004 | Feedback was mentioned but cycles and stability could still be conflated with direct bidirectionality or universal convergence. | Support multi-step feedback and context-dependent response; permit stable, oscillatory, growing, decaying and regime-changing behavior where supported. F002/F003. | Printed pp. 25-27, 91-94; PDF 42-44, 108-111. |
| SUB-G005 | Representation boundaries and context were not explicitly revisable hypotheses. | Support overlapping/nested scopes, unknown external influences and alternate boundaries; keep the system's actual acquisition/action boundary distinct from hypothesized world boundaries. F001/F003/F004. | Printed pp. 95-96, 104; PDF 112-113, 121. |
| SUB-G006 | Larger composition could be mistaken for sufficient explanation of collective behavior. | Allow coarse views and reusable substructures while retaining dependence on interactions and access to finer evidence; declare information loss and time/scale validity. F001/F004. | Printed pp. 79-84, 91-94; PDF 96-101, 108-111. |
| SUB-G007 | Function, purpose, learned regularity, constraints and the system's objectives were not explicitly separated. | Host inferred functional roles as revisable claims; distinguish them from stated goals, engineered inquiry objectives and declared constraints. Do not assign intention to every process. F004/F005. | Printed pp. 14-17, 106-107; PDF 31-34, 123-124. |
| SUB-G008 | Visible state, hidden state and alternative mechanisms needed a more explicit boundary. | Preserve uncertainty about unobserved influences and observationally indistinguishable mechanisms; questioning may conclude insufficient evidence. A persuasive model explanation is not external corroboration. F004/F005. | Printed pp. 106-107, 172; PDF 123-124, 189. |

These concerns fit the six responsibilities. No seventh function, mandatory domain ontology, universal stock-flow schema or fixed primitive is introduced. Stocks/flows, feedback, hierarchy and purpose are phenomena the host must be able to accommodate when useful, not labels it must impose on every image, composition or observation.

Terminology for the next architecture discussion: an element is a candidate constituent at a chosen scale; its state is its condition at a time; a relationship is an association or dependency claim; an interface is a boundary across which interaction is expressed; structure is their organization; dynamics describe how state evolves; a representation is the substrate's partial encoding of some of these. Changing state and changing structure are different operations. No single object schema is fixed by these definitions.

Keep three levels explicit: actual substrate execution state; represented observations/inferred state of the world; candidate prediction or simulation state. A modeled mass flow may have a conservation constraint; a copied information signal does not thereby consume the source signal. Constraints and compatibility rules need provenance and applicable context, and unknown units or mechanics must remain unknown.

Architecture choices must distinguish fixed host/update mechanisms, mechanisms learned through experience, and proposals imported from a reasoning model. Permission to alter organization does not itself specify an endogenous learning mechanism. Increased complexity, settled state or extra questioning is not a scientific success criterion.

Additional prospective cases (all not run):

| Check | Risk/condition | Required demonstration | State |
| --- | --- | --- | --- |
| SUB-V009 | State, flow and signal are confused | Preserve accumulation versus rate and appropriate declared dimensions; material transfer and copied information retain distinct update semantics. No automatic constraint is imposed when units/laws are unknown. | Not run |
| SUB-V010 | Delay/history is discarded during representation updates | Two histories with the same observed current value but different delayed responses remain distinguishable or explicitly ambiguous; asynchronous and event/receipt/model time are preserved. | Not run |
| SUB-V011 | Pairwise edges or direct bidirectionality erase system dynamics | Represent a multi-step feedback loop, a context-dependent threshold and a joint interaction; compare predicted outcomes against subsequent evidence without requiring a fixed equilibrium. | Not run |
| SUB-V012 | Fixed boundaries conceal external influence or regime change | Revise a candidate scope/context after contradictory evidence while preserving earlier evidence and unresolved hidden causes. Observational equivalence does not force a causal conclusion. | Not run |
| SUB-V013 | Coarse composition silently loses consequential detail | Compare a composed view with its supporting details at declared time/scale; expose compression loss and test whether the view retains distinctions needed for the chosen prediction. | Not run |
| SUB-V014 | Inferred purpose or simulated explanation becomes a goal or fact | Preserve observed behavior, inferred function, supplied goal, inquiry objective, declared constraint and simulated outcome as distinguishable records; unsupported mechanisms remain alternatives. | Not run |

## Complete-book review and component requirement trace

The owner subsequently requested a page-by-page review of the entire supplied book. [MEADOWS_REVIEW.md](MEADOWS_REVIEW.md) records twelve consequential findings, section coverage, rationale, limits and prospective checks. [MEADOWS_PAGE_REVIEW.md](MEADOWS_PAGE_REVIEW.md) accounts individually for all 235 PDF pages. This is a conceptual source review, not reproduction of all illustrations/simulations or independent verification of cited works.

The six functions remain. The full review strengthens interface semantics, timing/revision cadence, attention/selection feedback, resilience, change authority, objective/proxy separation, imported-assistance attribution, qualitative uncertainty and executable-model contracts. Five Whys is not forced into a unique linear root-cause chain.

| Function | Draft component requirements |
| --- | --- |
| SUB-F001 | SUB-R001, SUB-R006, SUB-R009 |
| SUB-F002 | SUB-R003, SUB-R004, SUB-R005, SUB-R016 |
| SUB-F003 | SUB-R002, SUB-R005, SUB-R009, SUB-R011, SUB-R012, SUB-R015 |
| SUB-F004 | SUB-R001, SUB-R002, SUB-R006, SUB-R007, SUB-R008, SUB-R009, SUB-R011, SUB-R013, SUB-R016 |
| SUB-F005 | SUB-R005, SUB-R007, SUB-R008, SUB-R010, SUB-R011, SUB-R013, SUB-R014, SUB-R016 |
| SUB-F006 | SUB-R010, SUB-R014, SUB-R015 |

SUB-V015 through SUB-V022 are specified in the complete review. The component catalogue links each requirement to upstream system obligations, functions, source pages and prospective cases. No source principle is treated as proof of a proposed mechanism. No mandatory stock-flow ontology, universal confidence scalar, fixed hierarchy, fixed equilibrium or perpetual model-call loop is added.

## Earlier functional readiness and next discussion

Self-review result: revised functional proposal is suitable for brainstorming, with sixteen draft component requirements and twenty-two prospective product cases, all not run. Overall architecture gate remains REVISE because primitive/update semantics, state authority, concrete contracts, inquiry allocation and operating envelopes remain open. Contract/runtime/integration qualification: not run. No scientific superiority or general intelligence claim.

Next discussion: compare the minimum substrate primitives and interaction/update rules that can realize these functions, including the relevant existing EDI mechanisms. Choose a smallest complete working learning/inquiry loop only after the functions and boundaries are settled. Do not begin implementation or benchmarks from this document alone.

## Current architecture proposal and owner review

[SUBSTRATE_BLUEPRINT.md](SUBSTRATE_BLUEPRINT.md) consolidates the six functions into three logical parts and six proposed specifications. [OBSERVATION_SUBSTRATE.md](../integration/OBSERVATION_SUBSTRATE.md) reviews both system directions, eleven contract families, all eight downstream obligations, internal lanes and feedback. [BUDWORM_CHALLENGE.md](BUDWORM_CHALLENGE.md) challenges nonlinear, multi-timescale discovery without equating stability with a fixed equilibrium.

This proposal supersedes the earlier next-step request to begin architecture brainstorming. Next: owner review of the blueprint, then concrete contracts, one selected native inquiry strategy and an operating profile before product implementation. Architecture REVISE; all twenty-two substrate and twelve integration cases remain NOT RUN.
