# Four-component proposal: design review

**Gate: architecture — revise.** The corrected design retains O, S, R and X. It repairs the unsafe ownership, recovery and feedback assumptions, but the acquire-new-observation mission still lacks a named, authorized outside source/action capability. All endpoint contracts are proposed; no runtime or integration qualification exists.

| Gate | Decision | Evidence / remaining condition |
| --- | --- | --- |
| Architecture | revise | Smallest corrections specified below; F08 still blocks the complete acquire mission. |
| Contract | revise | 21 application/model operations and 2 outside native-ingress operations are proposed. Endpoint schemas, authority/admission policies, M terms and numeric limits are unagreed (F08–F10). |
| Runtime | blocked | No pinned implementation/configuration or executed product cases (F11). |
| Integration | blocked | No end-to-end recovery, authority, grounding, resource or acquisition evidence (F08–F11). |

This is self-review of a proposed design, not an independent endpoint review. `catalogue.json` contains the contracts, all eleven checklist facets per effective contract, requirement flowdown, cases, findings, dependency inventory and feedback review. `checker-result.json` is the raw bundled structural-checker result; `source-pin.json` records scope and source identity.

## Smallest justified correction

1. **O stays a seven-day native receipt store with append/get/subscribe.** Do not add an acknowledgement, lease, deletion or acquisition operation. S resumes from its own committed cursor. R may get retained observations, but may not append generated answers as ordinary external evidence. X has no O payload access.
2. **S commits representations, applied occurrence IDs and its cursor atomically.** Crash before commit permits safe replay; crash after commit resumes from durable state. This is a proposed local transaction requirement, not a claim that the unspecified store already supports it. O stream handoff/durability/cursor semantics require endpoint agreement. After an outage outside O's actual retention horizon, report a gap rather than promise recovery.
3. **Deduplicate redelivery by occurrence, not content.** Distinct receipts can share a content hash. Preserve source/epoch claims, occurrence IDs, native values/unknowns, temporal scope and correction lineage. Hash equality proves neither a repeated occurrence nor physical sameness. Source authentication remains an external obligation.
4. **S is the sole durable admission authority for its representation, physical-identity and accepted-state domains.** R submits inference/identity proposals; X submits simplified acceptance proposals. S validates expected revision, evidence, compatibility and admission policy, and returns a durable disposition. Until policy exists, retain pending or reject. Operational acceptance remains separate from external truth.
5. **Keep generated material typed as generated.** R/M answers enter S as proposals with supporting observations, model/version and derivation lineage. X exposes unavailable support, selection history and shared dependencies. R/X agreement through the same M is correlated; it is not independent confirmation or evidence of calibrated confidence.
6. **Bound inquiry as one work item.** Stable request/work IDs, a shared remaining attempts/deadline/token/cost budget and finite queue/byte/concurrency limits survive retries and restarts. Failed work and unknown M completion consume budget. Native intake receives a positive reserved capacity; inquiry yields on exhaustion. Local commits never wait while holding locks for another component/model. Numeric caps and measured capacity remain open.
7. **Separate embedding spaces by model provenance.** Select by provider/model/revision/preprocessing/dimension/normalization/metric; preserve schema versions and reject unsupported combinations. Equal dimensions do not imply compatibility. Any migration is explicit and lineage-preserving.
8. **Limit acquisition honestly.** R can reread O's retained observations. A suggestion, model output or missing O id cannot authorize a new external observation. Until a provider/action contract is specified, return `acquisition_unavailable`. Optional direct X→M assistance stays disabled pending policy; X can report from S/R.

Indefinite S references retain metadata, not O payload availability. Mark expiry/unavailable support and carry that limitation into reports; do not silently create a permanent payload archive. Storage/backup/admission costs still need policy.

## Application pair matrix

Read requests and read results are separate operations. A response does not imply a symmetric capability. Every required direction is restricted to its operation allowlist; direct foreign-store writes are prohibited even on otherwise required lanes.

| Pair | First → second | Second → first | Why retain this connection |
| --- | --- | --- | --- |
| O, S | Required: retained observation results | Required: get/subscribe requests | Representation and bounded recovery require native observations. No acknowledgement. |
| O, R | Required: get result/unavailability | Required: get request | Resolve a known missing retained observation without inventing acquisition. |
| O, X | Prohibited | Prohibited | X needs S/R summaries and lineage, not native payloads. |
| S, R | Required: state and proposal dispositions | Required: reads, typed inference and identity proposals | Reason/revise while S retains admission authority. |
| S, X | Required: authorized summaries and dispositions | Required: reads and simplified acceptance proposals | Report and propose accepted state without competing commits. |
| R, X | Required: reasoning/acquisition outcomes | Required: questions/acquisition suggestions | Close the reporting/inquiry status loop without conveying action authority. |

Six application pairs / twelve directed lanes are complete. No internal services are invented from logical responsibilities; there is no separate internal-part deployment matrix to justify.

## Outside boundaries and shared dependencies

M is independently governed and is therefore registered as an external component, preserving four application components. This expands the catalogue to ten pairs / twenty directed lanes.

| Pair | First → second | Second → first | Decision |
| --- | --- | --- | --- |
| O, M | Prohibited | Prohibited | No model authority on native receipt or storage. |
| S, M | Not needed | Not needed | Callers R/X retain M interaction; S accepts typed proposals. No direct store access. |
| R, M | Required proposed inference request | Required proposed generated result | Separate disclosure/cost responsibility from generated advisory output. |
| X, M | Optional proposed request | Optional proposed result | No added confidence requirement justifies making this path mandatory. |

The catalogue separately reviews native-source→O append and O→source append transport outcome, with eleven facets each. It does not invent a named source component, acknowledgement or durable-success capability. Source identity/epoch, authentication, schema, idempotency, receipt durability, seven-day expiry and unknown-completion behavior are unagreed.

The absence of an external acquisition provider is F08, not a fictitious contract. Before enabling it, name its source/action authority, permitted operation, request/result/effect ports, identity, temporal scope, budget, retention and independently grounded effect evidence.

Shared O/S storage, R/X work records, clocks, scheduler, network and credentials are inventoried separately. Required obligations include local transaction capability, retained applied IDs over the agreed replay/retry horizon, separate owner credentials, source/receipt/commit/knowledge/model-time distinctions, monotonic budgets across recovery, bounded storage and queues, failure isolation and native intake reservation. No actual infrastructure topology, timing precision, availability or capacity is asserted.

M policy must pin provider/model version, disclosed projection, tenant isolation, retention/deletion, quotas, billing/usage and timeout/partial/unsupported behavior. Unknown completion may have incurred cost. M receives no store credentials or tools; no model calls occurred here.

## Whole-system and causal review

The active graph is one strongly connected group: O/S/R/X/M (including optional X/M). Reviewing pairs alone would miss these cycles:

- O→S→O recovery can skip observations if the cursor advances before representation commit. S's atomic local checkpoint resolves the design defect, subject to O retention and endpoint semantics.
- S→R→O→S and S→R→S can turn generated answers into apparent independent support. Typed inference and denial of generated native ingress cut that amplification; source/selection lineage remains visible.
- S→X→S can simplify away uncertainty or overwrite newer corrections. Expected-revision proposals and S admission preserve unknowns and prevent stale acceptance.
- X→R→M→R→X can amplify correlated confidence, consume unbounded resources and starve native intake. Shared lineage, one total budget, reserved capacity and explicit terminal status bound the proposed loop. Saturation, circular waits and failure isolation remain unmeasured.

Five-why check: false confidence follows repeated “evidence”; repeated evidence follows generated reentry; reentry follows erased origin classification; erased classification follows unqualified O admission; unqualified admission follows treating payload equality/transport as truth. The smallest repair is provenance-preserving native admission and typed S proposals, not a new component or a full mesh.

## Checks, evidence and limits

Input: `forward-proposal.md`, SHA-256 `fccbf8d9530e4555099ffd17d16782003ad970cd45a876e56e92a494495e96f7`. The source was rehashed unchanged after writing the outputs. No sibling architecture drafts or prior agent artifacts were read. No ancestor AGENTS guidance was found at the checked ancestor paths; no companion component-review skill existed at the conventional adjacent path. No endpoint specifications or implementation were supplied. The content hash pins the input; no git/remote revision verification is claimed.

The bundled checker was run without modification:

```text
python /root/.codex/skills/remote-skills/edi-interface-review/scripts/interface_matrix.py /workspace/scratch/3e9b405bc235/forward-output/catalogue.json --root /workspace/scratch/3e9b405bc235
```

Result: consistent, no errors; 5 registered components (4 applications + M), 10 pairs, 20 lanes, 21 linked operations, one reviewed feedback group. Checker self-tests were not required because the checker was unchanged. The checker does not validate semantics, requirements or extra outside-boundary records.

A separate local trace check resolved all 11 requirements, checked all contract/case/finding requirement references, verified each of the 23 operation contracts has linked planned cases covering its requirements, confirmed both outside native operations have all eleven facets, and checked the 12 application lanes and unchanged source hash. Early trace-check omissions were corrected by adding an explicit snapshot case and appropriate case links before the final successful check. All 18 required product cases are specified, **none executed**. They cover occurrence identity, crash/recovery, expiry, authority, generated feedback, version spaces, duplicate/reorder/cancel, budgets, absent acquisition, stale acceptance, model failure, bypasses, shared confidence, missing O reads, corrections, clocks, append uncertainty and snapshot scope.

Semantic review was a design walkthrough of the proposal and effective contracts; no checker pass proves semantic correctness, runtime behavior, source authenticity, throughput, calibration, intelligence or superiority. No live service, model inference, paid action, product implementation or publication occurred. Outputs are confined to this authorized directory; no checkpoint/remote outside it was changed.

Next action: resolve F08 with a named authorized acquisition boundary (or explicitly narrow the mission to retained-data rereads), then agree F09–F10 endpoint/policy details. Runtime/integration gates require separate implementation authorization, pinned implementation/configuration and actual passing required cases.
