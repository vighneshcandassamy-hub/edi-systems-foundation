---
name: edi-component-review
description: Design, critically review, simplify, and improve EDI MVP layers or components with traceable requirements and evidence-based readiness gates. Use for a new or revised EDI architecture, chief-scientist retrospective, KISS/Five Whys/waterfall/MECE review, component specification, planning baseline, or architecture approval before implementation. Apply the observation-review method to each component without imposing observation-specific mechanisms on other layers.
---

# EDI component review

Produce the simplest justified component design and a truthful readiness decision. Repair in-scope gaps and reassess. Distinguish architecture approval, contract readiness, runtime verification, and integrated capability validation.

## Recover the current baseline

1. Read the repository's AGENTS.md, STATE.md, workflow and component plan; resolve the current branch/commit and authoritative requirements. Prefer current source artifacts over conversation summaries. Read [references/edi-context.md](references/edi-context.md) for source locations and EDI boundaries.
2. State the component, requested gate, authorized scope and intended consumer. Default to architecture review when only design is requested. Continue reversible work already authorized; do not introduce routine approval stops.
3. Preserve previous designs, frozen scientific code, failed results and held-out evaluation material. Do not start inference benchmarks, paid infrastructure, deployment, external messages or public release merely because this skill ran.

## Build the trace before selecting mechanisms

Map mission -> system requirement -> capability/layer requirement -> function -> component specification -> verification case -> evidence. Retain stable IDs, source, rationale, acceptance, owner/allocation, version and explicit status. Record future consumer obligations and unallocated requirements.

Use the repository's existing catalogue and validator. For Observe, REQUIREMENTS.json is authoritative; run its traceability tool rather than duplicate it. For a new layer, extend the format or create a compatible scoped catalogue. Distinguish required behavior from a proposed mechanism or engineering target. Declare assumptions and quantitative proposals.

Specify inputs/outputs, state, interfaces, authority, uncertainty, compatibility, failure behavior, resource limits and verification for each component. Keep a component because a requirement needs it, not because a named model, framework or service is available. Reuse [assets/component-plan-template.md](assets/component-plan-template.md).

## Challenge the design

Read [references/review-methods.md](references/review-methods.md) and apply these proportionately:

- KISS: challenge every mandatory field, service, transform, stored state and model dependency; combine owners where justified.
- Five Whys: trace consequential choices to an upstream need; distinguish rationale from experimentally established causes.
- Requirements waterfall with a verification return path: check allocation downward and fulfillment upward; allow evidence-driven iteration.
- MECE: test completeness and exclusivity within declared decision axes. Do not call overlapping modalities, causes or hypotheses MECE.
- Alternatives and counterexamples: compare the simplest credible alternative, the proposed design, and relevant current approaches against hard constraints. Browse primary sources when choices depend on current or uncertain technical facts.
- Failure-mode and capacity analysis: inspect error propagation, identity/evidence contamination, overloaded queues, long-term state growth, recovery, dependency loss, compatibility and deployment fault models. Apply only relevant analyses; justify any not-applicable item.

Read [references/operating-envelope.md](references/operating-envelope.md) when setting performance, token, cost, availability or scale claims. Scope measures to complete workloads and known faults. Do not promise zero priors, universal identity, unlimited scale or unconditional availability.

Do not transplant Observe's four modules, eight fields or model-free intake rule into reasoning or representation components. Re-derive those components' mechanisms and model budgets from their own requirements.

## Repair and reassess

List findings with severity, affected IDs, consequence, the gate they block and the smallest corrective action. Implement justified documentation/design corrections within scope; implement code only when implementation is authorized. Keep optional enhancements separate from gate-blocking defects.

Re-run affected checks after a change. Preserve original failures and quantitative targets; do not weaken acceptance to obtain a pass. After repeated non-progress, identify the missing mechanism, evidence or external dependency and return a specific diagnosis rather than loop indefinitely. Stop only on a justified gate decision or concrete blocker, not a vague offer to continue.

## Decide and record the gate

Assess eight criteria: mission_trace, boundary_contract, necessity_simplicity, evidence_uncertainty, resource_envelope, failure_recovery, sourced_choices, verification_scope. Explain each judgment with artifact references. Use pass, revise, blocked or justified not_applicable per criterion. State reviewer identity/role and whether the review is independent; never imply independent validation from self-review.

- Architecture PASS: no unresolved issue blocks the architecture gate; obligations are allocated, mechanisms coherent, assumptions explicit, verification feasible, and implementation risks/open choices bounded. Runtime targets can remain unmeasured.
- Contract PASS: concrete interface/state/version/error contracts satisfy the specified contract gate. Preserve open runtime obligations.
- Runtime PASS: required tests pass at a pinned implementation/configuration with evidence and declared scope. Plans, simulations of document flow or unit checks of this skill do not count.
- Integration PASS: downstream capability is demonstrated with appropriate controls and complete cost/failure accounting. Engineering integrity alone does not establish endogenous intelligence, transfer or superiority.

Use [assets/review-report-template.json](assets/review-report-template.json) and run:

```text
python scripts/review_gate.py REVIEW_REPORT.json --root REPOSITORY_ROOT
```

Treat the helper as a report-consistency check, not a scientific reviewer. Run the actual component checks separately when in scope. Return REVISE for correctable gate defects and BLOCKED for an explicit external dependency; do not issue PASS solely because a schema validates.

## Save the reusable handoff

Update the component's planning Markdown, requirement/decision records, scoped review report and repository checkpoint. Sync authorized private repository work and verify the published revision/diff. Preserve one authoritative plan and link supporting detail; avoid stale parallel baselines.

Report: gate/verdict, changes and reasons, checks/evidence, limits/open issues, exact saved location and next action. When an additional skill contributes, record its name/version, scoped finding, changed requirement/decision and verification consequence; a skill's assertion is not evidence by itself.

For changed component boundaries and integration, apply the companion [EDI interface review](../edi-interface-review/SKILL.md), including all-pair directed coverage and whole-system feedback analysis.
