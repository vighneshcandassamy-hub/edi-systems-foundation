# ADR-010 — Bounded C0 integration with explicit operator inputs

21 October 2026. Status: source implemented, unqualified. Input: `945460a2458cf343633ccf2e49e5355e43d66cea`. Latest owner direction: finalize integration and holistic test design; **do not test yet**.

## Context and decision

C1–C7 expose first native source subsets but Runtime composition alone does not constitute a durable workflow. [C0-W01–W11](../implementation/INTEGRATION_TRACE.json) flow existing IMP-R04/R07/R11/R12/R15/R19/R23/R25/R29/R33 obligations into bounded coordination, not new domain mechanisms or authority.

Add one lazy C0 SQLite FULL/WAL ledger, immutable plans/inputs, native step intents, terminal results and retained attempts. Reuse existing strict Pydantic records, component ports and local error/durability conventions. Use a finite operation registry and bounded JSON-pointer selectors to earlier committed artifacts or named inputs. Copy imported data literally; do not evaluate it as code, expressions or another template.

Native command identity remains deterministic and original resolved arguments are durable before invocation. Reserve terminal capacity and retain uncertain completion. Ordinary resume does not repeat pending work. Explicit stopped-runner reconciliation can retry the original native command under a new C0 attempt fence; native C5/C7 still own their execution guards. Physical disk failure, process interruption and cross-owner commits remain distinct.

Do not allow computed model output to become operator authority. The profile disables operator steps by default. Enabled operator steps require a whole separately recorded operator-decision input through `supply_operator`, with configured local identity matching the native request where applicable. These are trusted-local labels, not authenticated users. C3 model admission and C7 actual policy adoption remain different decisions owned by different components.

Persist declared result-acceptance conditions rather than assuming a successful RPC means a successful analysis. Keep failed native output available for inspection, while preventing it from entering downstream committed-step references. Keep ordinary JSON null as a valid output. Compact status and bounded output/attempt selection avoid re-embedding every artifact in every response.

## Alternatives and rationale

| Alternative | Assessment |
| --- | --- |
| One ad hoc demonstration script | Smallest initial effort but hides the recurring coordination/restart/authority requirements. Use later as a fixture driver, not the source of component ownership. |
| Current explicit bounded coordinator | Preferred first integration: installed dependencies, visible state/limits, native ports and no additional service or inference dependency. |
| General orchestration/agent framework | A researched future option; not required to connect these existing owner APIs. It would still need the same provenance/admission/recovery semantics. |
| Distributed workflow/broker/services | Defer until a workload/fault model requires them. This increment makes no HA, hard deadline or arbitrary-scale claim. |

KISS keeps one coordinator with acyclic finite plans, not a service per concept. Five Whys connects persistence to interrupted acknowledgement and original-evidence integrity; it is design rationale, not measured causality. The requirements waterfall has an explicit future evidence return path. MECE distinguishes data/operator authority, proposed/adopted policy, intended/completed/measured effect and ready/waiting/uncertain/failed/completed states; hypotheses and modalities are not assumed exclusive.

## Consequences and gates

All eight owner workspaces/paths are distinct. C0 calls native ports without holding its transaction across an owner call. Intake does not initialize C0/C3/C5/C7 or inference stores. Runtime composition still initializes C1 on startup, so operational C0 inspection during C1 startup failure remains open. Capacity is finite and reservation can refuse a maximal plan; deadlines are cooperative.

The [holistic test design](../implementation/INTEGRATED_TEST_DESIGN.md) separates local engineering, nonlinear ecology, human/latent causes, world growth/transfer and operational/comparative claims. Concrete models/fixtures/statistics and native student/vLLM/teacher bindings remain pre-execution decisions. No workflow, Runtime/store, model, solver, example, test, gate validator or benchmark ran. Source/interface self-review remains REVISE and is not independent qualification.
