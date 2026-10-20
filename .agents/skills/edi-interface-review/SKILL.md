---
name: edi-interface-review
description: Review EDI interfaces and integration across every component pair in both directed lanes and across system feedback loops. Use when adding or changing a component, port, data/control flow, schema, identity rule, learning path, shared dependency, or deployment boundary. Produce traceable contracts and scoped readiness decisions without requiring a fully connected system.
---

# EDI interface review

Review every pair; implement only justified connections. Treat bidirectional exchange as two independently specified directions with potentially different authority.

## Recover scope

Read repository guidance, checkpoint, component plans, requirements and both endpoint specifications at pinned revisions. Apply the companion component-review skill where present. State the requested gate and authorized work. Preserve scientific baselines; this skill alone does not authorize product implementation, inference benchmarks, paid services or publication.

Read [references/interface-checklist.md](references/interface-checklist.md). Start from [assets/interface-review-template.json](assets/interface-review-template.json); its unresolved placeholders deliberately cannot pass.

## Enumerate and specify

1. Register actual system components. Review every unordered pair and both directed lanes: n(n−1)/2 pairs and n(n−1) lanes. Mark each lane required, optional, not_needed, prohibited or unresolved with a rationale. Reassess no-link decisions when responsibilities change. Do not confuse a capability catalogue with deployable components.
2. Keep internal-part matrices separate from system matrices. Inventory outside dependencies and source/action obligations separately; promote independently governed dependencies to components when appropriate. Read requests and results are separate operations. A return transport does not imply symmetric capabilities.
3. Specify each active lane's operation-level authority, producer and consumer ports, requirement IDs, cases, and all eleven checklist facets. Permit reads/proposals while prohibiting direct mutation where required. Distinguish proposed contracts from existing endpoints. Never invent a lease, acknowledgement or action capability to make a diagram close.
4. Trace mission/system obligations through producer responsibility, consumer responsibility, contract and verification evidence. Inspect native values, unknowns, corrections, temporal scope and incompatible versions—not merely JSON type compatibility.

## Review the whole system

Inspect shared stores, models, clocks, infrastructure and indirect paths. Review multi-party interactions, strongly connected groups and higher-order feedback, including delays, retries, circular waits, saturation, selection bias and generated material returning as apparent independent evidence. Pair completeness alone cannot establish system integration.

Require one durable authority for each state domain and explicit admission authority for updates. Separate retained evidence, inference, trial state, operational acceptance and external truth. Follow duplicate/reorder/crash/recovery paths end to end. Check complete resource cost and how failed inquiry yields to native intake. Declare unavailable history rather than promise unbounded replay.

Record findings, affected requirements, consequences, gate blocked and smallest correction. Repair authorized design gaps, then reassess. Keep unsupported enhancements optional; do not force a full mesh or split logical owners into services without a requirement.

## Check and decide

Run the bundled checker from this skill directory:

```text
python scripts/interface_matrix.py CATALOGUE.json --root REPOSITORY_ROOT
python scripts/interface_matrix.py --self-test
```

Run self-tests when changing the checker. Inspect the contracts and endpoint documents independently of its output: structural consistency does not prove semantic correctness, runtime behavior or intelligence. The helper does not resolve requirement IDs against external catalogues; run repository trace checks too.

Record architecture, contract, runtime and integration gates separately as pass, revise or blocked. A runtime/integration pass requires actual required cases at a pinned implementation/configuration with evidence and conditions. Planned cases and skill tests are not product qualification. Keep unresolved gate blockers visible; do not weaken gates to obtain a pass.

Save the design, matrices, evidence, open issues and next action in the authorized private repository; update its checkpoint and verify the remote revision/diff. Report what changed, why, what was checked and the practical limits. Do not claim independent review when self-reviewing.
