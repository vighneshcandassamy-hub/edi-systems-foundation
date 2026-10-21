# C7 agency, information qualification and owned policy

Later integration handoff: [C0 code 0.9.0](C0_INTEGRATED_WORKFLOW.md) coordinates existing C7 operations with separate operator-decision inputs. It does not close C7 qualification or connect external actuators. The owner's latest direction defers testing until the [holistic design](INTEGRATED_TEST_DESIGN.md) is reviewed; no runtime was executed.

21 October 2026. First source increment, code 0.8.0. Input: private architecture-branch revision `686da92ec4a9c0892998aee1b85280b723d8f199`. Status: **partial source implementation, unqualified**. Overall contract self-review remains **REVISE**. This document specifies the concrete subset; it does not replace the original architecture or declare every C7 obligation fulfilled.

The owner authorized C7 development against the agreed requirements, interfaces, rationale, schemas, assumptions and decisions. The continuing structure-first direction defers product execution and qualification. No policy was adopted, source accessed, command dispatched, report archived, modeled system changed or external action performed while authoring this increment.

## 1. Authorities and C6 prerequisite review

The [seven-chapter foundation](../../architecture/world-model/Meadows_Chapters_1_2_3_4_5_6_7_Integrated_Architecture_Audit_v0_7.md), [appendix semantics](../../architecture/reference/Meadows_Appendix_187_203_Semantic_Foundation_Reference_v1_0.md), [component allocation](COMPONENTS.md), [contracts](CONTRACTS.md), [directed matrix](INTERFACES.json), [implementation trace](TRACEABILITY.json), [reasoning integration](REASONING_INTEGRATION.md) and [architecture/tools/mathematics reference](ARCHITECTURE_TOOLS_AND_MATH_REFERENCE.md) remain authorities for their scopes. Original conceptual snapshots and historical evidence are unchanged. [ADR-009](../decisions/ADR-009-research-agency-and-policy-adoption.md) records this increment's choices.

C6's fourteen scoped requirements and source review were examined before this build. Its immutable forecast/confirmation, fixed-cut outcome selection, scalar/probability scores, missingness/dependence controls, fallible diagnostics, revision/finding/inquiry records and candidate-only submission are present in source with open verification. C6's existing review is REVISE, not full specification acceptance. Source authenticity/clock trust, independence, calibration, scientific utility, complete costs, recovery, retention and HA remain unestablished. C7 neither changes those judgments nor counts advice as authorization.

C7 needs no direct C6 port. C0 can carry an attributed C6 recommendation into a policy amendment's `imported_advice` IDs and rationale. Those IDs are unverified attribution, not C6-native retrieval, scientific validation or authority. The prohibited C6→C7 shortcut remains prohibited. C5's numerical validity and native C4 student/teacher inference also remain open.

## 2. Two boundaries with different owners

| Boundary | Canonical owner | This increment |
| --- | --- | --- |
| Investigated human, institution or ecosystem | C3 representation; supported C5 trial dynamics | C7 qualifies explicitly attributed actor-information masks and submits candidate descriptions of policy/organization. It does not infer psychology, enact a domain policy or implement an actor simulator. |
| EDI's operational permissions | C7 | Versioned research policy, finite scoped grants, command authorization, internal read dispatch, receipts, report reconciliation and explicit local policy adoption. |

Represented goals are never EDI grants. Analyst revision about a person's policy is not a change to that person. C3 candidate acceptance is neither operational adoption nor empirical truth. Tool completion is neither successful goal achievement nor a measured real-world effect.

## 3. Functions and scoped trace

The [C7 trace](C7_RUNTIME_TRACE.json) maps mission → original implementation requirements → sixteen scoped requirements → F70–F73 → source/contracts → twenty-four **unrun** verification cases. Original parent requirements remain wider than this increment.

| Function | Implemented source subset | Wider obligations still open |
| --- | --- | --- |
| F70 qualify actor-visible information | `qualify_actor_view` checks pinned actor/model/evidence correspondence and UTC knowledge/availability/receipt/perception cuts; only supplied content is exposed. | Verified attention/perception/meaning, arbitrary clock mappings, C3-native actor policy, C5 dynamic actor execution and automatic evidence-content interpretation. |
| F71 assess intended action | `check_action` pins purpose/policy/grant, exact tool scope, item limits, grant interval and decision expiry; unsupported requests receive a refusal. | Planning/value optimization, external acquisition and dynamic resource feasibility across real systems. |
| F72 authorize/reconcile execution | Durable single-use intent, bounded internal read adapters, immutable receipt/status, explicit uncertainty/reconciliation, original report capture and access review. | External connectors, hard process supervision, authenticated identities, distributed capabilities and measured effects. |
| F73 adopt owned policy | Immutable amendments; explicit operator adopt/reject/defer; optimistic base revision; retained purpose/standards/history; unresolved commands block adoption. | Automatic policy learning, independent legitimate-authority validation, complex migrations, organizational/state transitions and production rollout. |

## 4. Typed contract inventory

[Contracts](../../src/edi/agency/contracts.py) inherit strict, frozen, extra-forbidden `Record` with schema version 1.0 and finite numeric values. Times explicitly carried by grant/view/report/disposition inputs must be timezone aware. Unknown policy state is `None`, not an implicitly installed default. IDs are workspace-scoped opaque identifiers; hashes identify retained content, not authority or external truth. Unsupported versions/fields are rejected.

| Contract family | Essential information and rationale |
| --- | --- |
| `Policy`, `Grant`, `PolicyVersion` | Purpose version/text, standards, assumptions, named exact-origin or exact-world-ID grants, operation/item/time bounds, decision TTL and cooldown. These define what an ordinary command can do without changing its policy. |
| `AmendmentRequest`, `Amendment`, `AdoptionRequest`, `Adoption` | Base revision, change class, proposed full policy, trigger, attribution, advice IDs, rationale, implementation/resources and carry-over; separate recorded operator decision and committed policy version. Proposal cannot install itself. |
| `ActionRequest`, `ActionDecision` | Runtime boundary, intention/arguments, expected effects/limits, named grant, purpose/policy versions, allowed/denied status, reasons, authorization interval and exact adoption hash. Explanation text never creates permission. |
| `DispatchRequest`, `ExecutionIntent`, `ExecutionReceipt`, `ExecutionStatus` | Stable dispatch/command/decision IDs, durable original decision, local commit boundary, completion/failed/reported/abandoned status, results, diagnostics and separate `measured_effect=not-established`. An unresolved intent is not silently retried. |
| `ActorViewRequest`, `VisibleDatum`, `ActorView` | Pinned actor/model cut, explicit evidence or model refs, attributed content, channel, availability/receipt/perception times, owned goals/frames/memory/policy and clock assumption. No global model record is appended to the actor output. |
| `AccessRequest`, `AccessScope`, `AccessReview`, `AccessDispositionRequest` | Target/unknown/hypothesis family, minimum useful evidence, exact finite access scope, current grants, coalescing key, denial/defer interval and C0 notification ownership. A request or review does not grant access. |
| `ReportRequest`, `ReportStage`, `ReportArchive`, `ReconcileRequest` | Exact UTF-8 report text, report origin/attribution/time, frozen C1 capture, durable C1 receipt and explicit local reconciliation decision. Original report bytes remain distinct from C7's interpretation. |
| `ModelUpdateRequest`, `ModelStage`, `ModelSubmission` | Candidate-only represented-world puts, base/record versions, explicit change kind and attribution, exact staged C3 patch and original commit receipt. No operational adoption is inferred. |
| `ArtifactCursor`, `ArtifactPage` | Bounded kind/position/watermark selection, workspace, continuation and retained JSON artifacts; no unbounded history promise. |

Twenty-one generated JSON schemas are in [schemas](../../schemas/). No credentials, inference weights, network targets, arbitrary Python/shell commands or executable expression fields are added. JSON content remains data.

## 5. Policy lifecycle and authority

There is no policy on a new C7 ledger. The trusted local operator must explicitly propose a bootstrap amendment at revision zero and separately decide adoption. `request_adoption` records a proposal only. `decide_adoption` is absent from the component facade and accepts only IDs configured in `AgencyProfile.operator_ids`. **This is a trusted local SDK/CLI boundary, not authentication:** an operator name is not a signed identity. Untrusted remote callers must not be connected to it without a later authenticated deployment boundary.

Ordinary action leaves policy unchanged. A `parameter` amendment can change only decision TTL and access cooldown. A `policy` amendment can change grants/rules without silently changing purpose/standards. Any changed purpose text, purpose version or evaluation standards requires `change_kind=goal` and a new purpose version. All prior standards remain in immutable adopted history; C6 forecasts and scoring rules are never rewritten.

An adopted purpose-version ID cannot later name different purpose text or standards. A deliberate rollback may reference a historical purpose version only with its original meaning and a new recorded policy adoption.

Adoption atomically checks the current base revision and appends a new policy version in C7's own transaction. Reject/defer decisions remain inspectable and do not advance the head. An amendment with a terminal adopt/reject decision cannot acquire a second terminal decision; a deferred amendment can be reviewed again if its base is still current. There is no hidden rebase. A changed or rolled-back policy is another explicit amendment/version.

An active or unresolved command blocks adoption. This deliberately avoids changing grants halfway through an unaccounted command. Ledgers, C3 state, pending evidence, standards and original command decisions are retained. Old unstarted authorizations fail dispatch after the policy changes. Complex policy migrations and in-flight external commitments are unsupported.

## 6. Actions, scopes and dispatch

The policy grammar can grant only two internal read operations:

| Operation | Required scope | Result |
| --- | --- | --- |
| `select-observations` | One explicitly granted C1 origin, optional workspace/origin-bound fixed-watermark cursor and limit ≤ grant limit. | Native occurrence metadata and continuation; no payload decoding, source acquisition or interpretation. |
| `select-world` | Exact granted record IDs, explicit model revision, unique pinned record versions and item limit. | Bounded trusted EDI model records with candidate/uncertainty metadata; explicitly not an actor view or validity certificate. |

`external-action`, `acquire-source` and `run-simulation` are representable unsupported intentions so refusal is auditable. C7 has no network, filesystem action, message, payment, physical actuator or C5 execution adapter. Existing declared simulation execution belongs to C0→C5; this increment adds no direct C7→C5 lane. A policy cannot enable an operation outside this grammar even if its explanatory prose requests it.

An allowed decision records the exact policy adoption hash, purpose version and named unexpired covering grant. Dispatch rechecks policy, grant scope and time. After obtaining the database writer lock, it checks authorization expiry using a freshly sampled local time, enforces single consumption of the decision and one unresolved command per workspace, reserves completion capacity, and durably commits the original intent **before** invoking its read adapter.

Cooperative checks before/after native work and between selected records check deadline, active-command/policy fence and authorization interval. They cannot forcibly interrupt an underlying SQLite/owner call or prove secure revocation across processes. Result content is byte bounded before receipt persistence. A known typed read error becomes a failed receipt; unexpected faults or uncertain commits leave the intent unresolved. Receipts have no measured-effect assertion. Local read results can be stale, hypothetical or factually wrong even when the command completed.

## 7. Recovery, reports and reconciliation

Retrying an original dispatch request returns its original command status; it never invokes the tool again. Reusing its ID with changed parameters conflicts. A different request cannot consume the same decision again. If the intent exists without a receipt, status is `completion-unresolved`, regardless of whether a worker might still be running. The operator must coordinate worker cessation before treating abandonment as a clean restart; no process supervisor is implemented.

`archive_report` first persists exact text and a frozen C1 `Capture`, then submits those exact UTF-8 bytes through a dedicated C1 report facade. The C0 operator must have registered an origin with namespace `edi.agency.reports`, adapter `edi-c7-report/1.0` and deliverer `C0-local-operator`. C7 cannot register it or use an unrelated origin. The facade accepts only bounded generated `execution-report` captures with C7 lineage, expected length and digest. Lost C1 acknowledgements are reconciled by resubmitting the identical staged capture/idempotency key. There is no shared C1/C7 transaction.

C7 then stores the original C1 receipt. `reconcile_execution` requires that archived report, the same execution ID, a configured local operator, an attributed rationale and `reported-completion`, `reported-failure` or `abandoned`. The reconciliation request is retained in the terminal receipt. These statuses report an operator's account; they do not reconstruct lost tool results or verify external effects. A late worker cannot overwrite an already recorded terminal receipt. Original terminal receipts cannot be edited.

Report archives are marked `generated` with command/implementation/operator lineage, not `external` independent outcomes. C6's raw-outcome checks therefore cannot treat them as corroborating world evidence. Capturing original bytes preserves what was reported without certifying its truth. No external connector is installed; arbitrary binary connector reports and independently observed effects need future contracts.

## 8. Actor-information qualification

`qualify_actor_view` uses C3's native read interface to check an active pinned actor and selected model refs. It checks C1 occurrence IDs, workspace, digest, origin class, lineage and receipt/commit knowledge time for evidence refs. An explicit shared-UTC clock-mapping assumption is required. No selected datum can be available before its referenced source/model was known; receipt cannot precede availability; perception requires preceding receipt; all selected times must be within the requested nonfuture cut.

The retained view contains only caller-supplied content and its attribution/uncertainty, plus actor refs and stated goals/frames/memory/policy. It appends no full canonical record, adjacent record, global history, analyst result, or automatically traversed relationship. Availability does not imply attention, receipt does not imply understanding, and an attributed perceived value is not measured psychology. Content-to-selector correctness, omissions and upstream information leakage remain review obligations; a dishonest caller can supply hidden knowledge in ordinary JSON. This API is not an information-security sandbox.

C3's global `actor_view` operation remains explicitly unavailable because its full visibility/perception policy is not installed. This C7 artifact is a narrow attributed mask, not a replacement claim. C5 does not yet execute actors from these masks. Unknown hormonal, cognitive or social causes stay unknown; a selected narrative does not identify the human system's causal structure.

## 9. Access review and curiosity handoff

Access review searches the current adopted policy for covering standing grants. It returns their IDs and expiry but never acquires data or expands them. Exact scope, target, unknown, hypothesis family and minimum useful evidence form the coalescing key; ID order is normalized without semantic rewriting. A materially changed request can have a different key. New request IDs retain separate audit records while linking to the same unresolved need; no notification is sent.

Configured local operators can retain a denial/defer interval. Unexpired denial/defer suppresses another missing-access suggestion for that exact need. A changed adopted policy with a valid covering grant takes precedence: an access disposition is not a grant revocation. To revoke actual permission the operator must adopt a new policy. Grant expiry makes a previous positive review stale; dispatch always rechecks current rights. Retrying an old review returns the historical answer, not a fresh grant check; use a new request for a current review.

C0 owns consolidated notification/daily budgets and C1 owns any future acquisition. C4 owns frontier ranking; C6 owns inquiry-yield evidence. Automatic scheduling, request delivery, source discovery, access to arbitrary resources, information-gain estimates and useful knowledge expansion remain open. These methods support that later loop without equating question count with intelligence.

## 10. C3 candidate policy/organization descriptions

`build_model_patch` accepts bounded `Put` proposals only, with no admission decisions, retired-record mutations, progress acknowledgement or operational grant. It adds reserved C7 attribution/meaning metadata and implementation lineage. `submit_model_update` stages the exact patch and reserves its receipt before calling C3's candidate-only facade. C3 owns the commit and all later admission. Retries preserve the original base/versions and exact patch; no automatic rebase or adoption occurs.

`change_kind` distinguishes represented policy, organization, explanation and context. The request explicitly has `boundary=modeled-world` and `basis=analyst-proposal`. It cannot certify that a forest manager, family or institution actually adopted a policy. A future evidence-backed domain-transition contract must preserve that separate operation and state carry-over semantics. Representing one is not permission to do it.

## 11. Integration and all-pair interface review

The original eight owners, 28 pairs and 56 directed dispositions are preserved in the [source review](evidence/c7-source-review.json). A required lane can be only partially implemented; inventory completeness is not contract acceptance.

| Pair / directed contracts | Concrete source subset | Explicit limits |
| --- | --- | --- |
| C0→C7 IF-07A; C7→C0 IF-07B | C0-only facade: action check, amendment proposal, authorized dispatch, access review, policy/status receipts. Trusted SDK/CLI separately exposes operator decisions. | C0 scheduling/authenticated identity, acquisition, notifications and complete resource orchestration remain open. |
| C7→C1 IF-13B; C1→C7 IF-13A | Exact-origin native selections, evidence metadata checks and dedicated generated-report ingestion/receipts. | No registry, arbitrary payload read, raw external outcome manufacture or external source acquisition privilege. |
| C7→C3 IF-18B; C3→C7 IF-18A | Revision/pinned model reads, existing bounded dependency/status ports and exact candidate-only policy/organization proposals. | Native actor-perception policy, delta subscriptions and complete refinement/dependency validity remain open. |
| C4/C5/C6→C7 | Prohibited, unchanged. | C0 carries attributed proposals; no direct actuation/adoption bypass. |
| C7→C4/C5/C6; C2↔C7 | Not needed, unchanged. | No new direct execution, reasoning, assessment or interpretation dependency. |

All eleven contract facets apply: **ownership** C7 policy/commands, C1 evidence, C3 model; **authority** named restricted ports and trusted operator boundary; **shape/version** strict 1.0 contracts/research grammar; **identity/scope** opaque workspace IDs, exact refs and distinct report/command occurrences; **time/order** UTC assumptions, pinned revisions/cursors, grant/decision expiry; **delivery/idempotency** original request fingerprints and single-use decisions; **commit/recovery** local durable intents, prepaid receipts, no cross-owner atomicity; **retention** append-only finite history with no deletion/export/restore promise; **resources** count/byte/item/deadline/disk/writer caps; **errors** typed denial/conflict/capacity/unavailable/integrity/unknown-commit outcomes; **feedback grounding** generated reports, model candidates, operator accounts and measured effects remain distinct.

Whole-system review: a model recommendation cannot grant its own capability; a captured report cannot corroborate itself through C6; an accepted model is not a real adoption; a completed read is not a successful intervention. Separate lazy stores avoid C1 waiting on C7, C3, C5 or an LLM. C7 holds no database transaction while invoking another owner. A full report store or failed C1 archive can block reconciliation; recovery requires restoring capacity/availability, not fabricated completion. C0 schedules retry and preserves this blockage in offered-work accounting. Shared host/clocks/SQLite remain common failure domains.

## 12. Resource and durability envelope

[AgencyProfile](../../src/edi/agency/config.py) defines finite defaults, proposed limits rather than measured capacity: 128 KiB request, 2 MiB document, 1 MiB result, 4 MiB page, 50,000 accounted rows, 1 GiB accounted artifact bytes, 15-second cooperative operation, 5-second SQLite writer wait, 256 MiB free-disk reserve. Policy ≤32 grants, each ≤32 IDs, tool ≤100 observations or ≤32 model records, actor mask ≤32 data, model patch ≤16 puts. These sizes require workload-specific qualification.

Each execution/report/model stage prepays one completion row and its original maximum document allowance. The allowance is stored with the parent; later configuration increases cannot exceed it. Logical quotas do not include exact physical SQLite indexes/WAL/temporary allocation. Disk failure can still prevent a prepaid receipt. Native owner calls can allocate up to their own configured bounds before C7 rejects an oversized returned result; there is no hard process-level RAM/time limit.

C7 uses a separate lazy SQLite FULL/WAL ledger with workspace/schema checks, policy CAS and indexed kind/scope/position selections. Single active unresolved command per workspace bounds admission across processes. Immutable requests/artifacts preserve retry outcomes. Local trusted file access is not hostile-tenant isolation. No latency/energy/throughput/token advantage, HA, unlimited scale, migration or complete application backup/restore is established. No model call is required for deterministic C7 operations; that does not make total EDI cost zero.

## 13. KISS, Five Whys, waterfall, MECE and failures

KISS: reuse existing Pydantic/SQLite/owner ports; one C7 ledger; two native internal adapters; no new framework, LLM, policy DSL, broker or service. A stateless allowlist alone loses policy history and uncertain command outcomes. A general agent/planner is unnecessary for permission enforcement and would expand the unqualified surface.

Five Whys: why separate proposal/adoption? Advice can be wrong → evidence/reasoning is not authority → permissions/standards must have an owner → changes need an explicit decision and version → original goals and evidence must survive. Why stage commands? Interruption loses acknowledgements → a retry could repeat work/effects → request identity alone cannot establish completion → durable intent precedes invocation → reconciliation, not optimism, resolves the gap. These are design rationales, not experimentally proven causal results.

Requirements waterfall and return path: source requirements → C7-R001–R016 → F70–F73/contracts/source → C7-V001–V024 → later pinned evidence → original acceptance authority. Currently the return path has source checks only. Deferred upstream obligations are named rather than silently passed.

MECE applies within explicit axes: domain versus EDI boundary; proposal versus adopted policy; available/received/perceived timing; authorization versus completion versus effect; change classes bootstrap/parameter/policy/goal; completed/failed/reported/abandoned receipts versus unresolved intent. Causes, actor goals, hypotheses and modalities overlap; they are not declared mutually exclusive or exhaustive.

| Failure/counterexample | Detection and containment | Unrun case |
| --- | --- | --- |
| LLM submits a grant as advice | Amendment is proposed only; operator decision absent from component facade. | C7-V003/V023 |
| Model record or actor view includes future knowledge | Pinned refs and explicit UTC availability cuts reject known violations; supplied content leakage remains unverified. | C7-V002/V004 |
| Policy changes between check and dispatch | Adoption hash/head CAS; old decision cannot start. | C7-V008 |
| Decision expires while waiting for SQLite | Time sampled after writer-lock acquisition and cooperative per-call checks. | C7-V009 |
| Another process consumes the same decision | Unique consumed-decision index and transactional intent admission. | C7-V010 |
| Worker dies after intent/tool but before receipt | Original status unresolved; no retry invokes tool; operator report/reconciliation required. | C7-V011/V012 |
| Late worker returns after reconciliation | Active-command/policy fence and immutable terminal receipt reject overwrite. | C7-V013 |
| C1 report committed but C7 receipt lost | Exact staged capture/idempotency key reused; original C1 receipt retained. | C7-V014 |
| Generated report returns as empirical evidence | Generated origin/lineage and report basis retained; no measured-effect assertion. | C7-V015 |
| Repeated missing-access requests annoy the user | Coalescing/cooldown/denial retained; notification left to C0, never sent here. | C7-V016/V017 |
| Storage fills or configuration changes after staging | Original prepaid completion allowance; physical disk failures remain explicit. | C7-V019/V020 |
| Candidate policy treated as domain adoption | C3 candidate-only interface and analyst-proposal boundary; no actual-effect operation. | C7-V018/V023 |

## 14. Source checks, usage and next work

Checks are limited to AST parsing, imports, CLI parser construction, schema generation, JSON/TOML parsing, new-document links, requirement/source/case references and unchanged lane dispositions. No Runtime/store, policy adoption, actor qualification, action check/dispatch, report capture, reconciliation, access review, model proposal, compiler/solver, example, test suite, gate validator, model call, simulation, training, benchmark or deployment was executed. Source review is the implementer's self-review, not independent validation.

[Examples](../../examples/agency/) are authored request templates with placeholders, not executed fixtures. The trusted local CLI provides `--agency-config`, `agency-propose-policy`, `agency-decide-policy`, `agency-policy`, `agency-check`, `agency-dispatch`, `agency-receipt`, `agency-actor-view`, `agency-access`, `agency-access-disposition`, `agency-archive-report`, `agency-reconcile`, `agency-build-patch`, `agency-submit`, artifact getters and `agency-query`. No template is automatically loaded and no default policy is installed by importing code or constructing the parser.

The first source pass now spans C0–C7, each partial and unqualified. The next development scope is a **C0 integrated workflow** connecting bounded observation → interpretation → model candidates/admission → reasoning handoff → analysis → assessment → authorized internal action/adoption, retaining explicit human/operator boundaries. Native model/provider binding, autonomous scheduling, actor simulation, complete original obligations and qualification remain separate open work. There is no C8 component implied and no benchmark or paid inference authorization from completing C7.
