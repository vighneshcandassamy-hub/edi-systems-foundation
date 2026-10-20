# Review methods

Use the minimum analysis that can change a design decision. Scale depth to ambiguity, consequence and cost. Never claim a checklist or repeated questioning guarantees correctness.

## Requirements and necessity

For each mandatory mechanism ask: which requirement demands it; what fails without it; what simpler alternative exists; what cost or assumption it adds; and what evidence would make it unnecessary. Mark source requirements, derived requirements and design decisions separately. Give each state transition, persistent record and authority an owner.

Trace both directions. Missing parents suggest unsupported additions; missing children/specifications suggest forgotten needs. A reference existing in JSON proves a link exists, not that the rationale is sound. Read at least the highest-risk complete trace manually.

## Five Whys

Choose consequential decisions or observed failures. Follow each explanation to an upstream need or explicit assumption. Stop before inventing a cause; five is a prompt, not a required chain length. Branch when causes differ. Distinguish rationale, hypothesis and measured causal evidence. Example: persistence -> long-gap continuity -> sessions restart -> memory cannot rely on RAM -> durable identity/evidence history. This explains a requirement, not recognition accuracy.

## Waterfall and return path

Cascade mission -> requirements -> functions -> allocation -> contracts -> implementation -> verification. Map results back upward. Distinguish verification of a specification from validation of intended use. Use progressive baselines rather than prohibit iterative correction. Examine failure cascades as well: one slow module, missing dependency, false association or full disk must have bounded effects and explicit recovery/abstention behavior.

## MECE and hypothesis handling

Define the unit, scope and time before partitioning. Orthogonal axes can each be exhaustive while combinations overlap. Capture state, processing state and identity status are different axes. A modality catalogue is usually overlapping. Rival hypotheses need to cover credible alternatives, not be declared mutually exclusive without justification. Include null, unchanged/no-effect, ambiguity and insufficient-evidence explanations where applicable.

## Decision analysis

Apply hard constraints first. Compare the simplest credible baseline, proposed approach and materially different options. State tradeoffs using evidence; use qualitative judgments until measurements justify scores/weights. Separate architecture pattern, training objective, pretrained checkpoint, storage/transport format and deployment product. A current model is not automatically the right mandatory component. Preserve source citations and retrieval date for changing claims.

## Failure and uncertainty analysis

Record mode -> cause/condition -> effect -> detection -> containment/recovery -> verification. Rank consequences qualitatively unless data supports probability/impact numbers. Include false merges, false certainty, missing observations, stale projections, dependency/version drift, duplicate/repeated effects and resource exhaustion where relevant. Check boundaries between modules, not only each module in isolation.

## Readiness

Classify findings by the gate they block. A hardware choice can remain open at architecture review if its required semantics, candidate options and qualification obligation are concrete; it cannot remain unspecified at runtime qualification. Unresolved ownership, impossible acceptance, hidden domain knowledge or unsafe evidence mutation can block architecture itself.

Do not freeze an unresolved interface merely to say the layer is finished. Conversely, do not demand production uptime evidence to approve an implementation architecture. Record the exact gate and evidence burden.
