# C0 integrated workflow and controlled capability demonstration

21 October 2026. Input: `945460a2458cf343633ccf2e49e5355e43d66cea`. Code increment 0.9.0. The owner initially requested integration and a capability demonstration, then explicitly directed: **do not test yet; design the test holistically and finalize integration first**. That latest instruction controls this increment. Runtime, demonstration, test, inference, simulation and qualification execution are deferred. Only source/artifact checks are in scope.

## Purpose, scope and prerequisites

Connect existing C1–C7 through C0 without changing their ownership or admitting recommendations automatically. C7's first source subset supports this handoff; full specification/security/runtime acceptance is not established by its earlier AST checks. C7 local operator identity remains a trusted configuration assumption. Existing actor dynamics, native inference, external actuation, retention and HA limitations remain open. The component-review and interface-review skills apply, with runtime results recorded separately from source review.

The [architecture](../../architecture/world-model/Meadows_EDI_Integrated_Architecture_v0_8.md), [component allocation](COMPONENTS.md), [contracts](CONTRACTS.md), [all-pair interface inventory](INTERFACES.json), [C7 specification](C7_AGENCY_RUNTIME.md) and [tools/math reference](ARCHITECTURE_TOOLS_AND_MATH_REFERENCE.md) govern the work. Existing snapshots, failures and planned-case catalogues remain unchanged.

## Requirements and acceptance before execution

| ID | Parent requirements | Function / obligation | Bounded acceptance |
| --- | --- | --- | --- |
| C0-W01 | IMP-R04, IMP-R19 | F00/F02 immutable workspace-scoped plan and inputs | Conflicting IDs reject; persisted plans/inputs survive reopening. |
| C0-W02 | IMP-R19, IMP-R23 | F02 finite typed native operation registry | No shell, arbitrary method, network, cross-owner SQL or executable template. |
| C0-W03 | IMP-R04, IMP-R19 | F02 references to earlier committed output and named external input | Missing input pauses before invocation; explicit bounded JSON selectors only. |
| C0-W04 | IMP-R19, IMP-R23 | F02 write-ahead step intent and exact native request identity | Interrupted step reports uncertain completion; no automatic replay on ordinary resume. |
| C0-W05 | IMP-R12, IMP-R23 | F02 operator steps separate from proposals | Operator admission/adoption require an explicit trusted-local workflow profile; model outputs cannot enable it. |
| C0-W06 | IMP-R19, IMP-R29 | F02 resource reservations, fencing, cancellation and bounded pages | Reserve completion before invocation; cancel cannot erase an unresolved step; stale workers cannot overwrite. |
| C0-W07 | IMP-R11, IMP-R12, IMP-R23 | F02 preserve C0-mediated C1–C7 lanes | All original 28 pairs/56 lane dispositions unchanged; no C4/C5/C6 direct action bypass. |
| C0-W08 | IMP-R07, IMP-R12, IMP-R23 | F03 internal findings delivery | Persist C6 finding hash, uncertainty and expiry as an internal artifact; no external message. |
| C0-W09 | IMP-R04, IMP-R11, IMP-R25 | F00/F01 controlled system demonstration | Distinguish a real local OS measurement, authored model/fixture, generated control and attributed reasoning. |
| C0-W10 | IMP-R19, IMP-R23 | F02 targeted fault and authority checks | Demonstrate duplicate/conflict handling, missing input, restart, generated-outcome rejection and denied external action. |
| C0-W11 | IMP-R07, IMP-R15, IMP-R33 | F00/F03 honest evidence and limits | Record original failures/configuration/workload/cost limits; no claim of autonomous discovery, full qualification or advantage over LLM. |

The demonstration must cover native C1 intake, C2 decoding/candidate submission, C3 hosting and explicit modeling-use decisions, C4 bounded questioning/export/import/rivals/frontier, C5 actual restricted numerical execution, C6 prospective registration and later outcome comparison/review/finding, C7 explicit policy/authorized internal read and C0 resume/delivery. A scripted response or authored model cannot be presented as autonomous native LLM discovery. Model assistance through this session, if used, must be attributed and its unmeasured inference cost retained as unknown.

## Design

One C0 SQLite ledger stores immutable workflow plans, external inputs, resolved native step intents, step outcomes and a bounded internal finding. It is separate from seven owner databases and opens lazily. A finite operation registry invokes existing typed ports. Native request IDs are deterministically derived from workflow/step IDs when omitted. No operation mutates another owner's database directly.

Arguments may contain only two reference forms: `{"$step":"earlier-step-id","path":"/JSON/pointer"}` and `{"$input":"named-input","path":"/JSON/pointer"}`. The full referenced value is copied as data; there is no expression evaluation, attribute access, interpolation, arithmetic or arbitrary code. Steps are ordered, IDs unique, and references cannot select a future or uncommitted step. Named inputs are immutable and byte bounded. Missing input returns `waiting-input` before a durable invocation intent.

Ordinary resume never redispatches an unresolved step. Explicit reconciliation retry uses the original resolved arguments and native idempotency key, after the operator has established that a prior runner stopped. The next C0 attempt fences final admission; it cannot forcibly interrupt an owner call. C5/C7 still independently reject/reconcile uncertain commands. This is not a distributed exactly-once guarantee.

Operator C3 admission, C7 adoption/reconciliation/access disposition and C5 control are gated by an explicit trusted-local workflow profile, disabled by default. Their arguments must be a whole named operator-decision input, never a computed/model-output reference. Ordinary `supply` cannot create operator authority. A separate `supply_operator` API checks configured operator IDs and retains the exact decision; the native request's operator ID, where present, must match. These IDs are a trusted-local configuration, not authentication. The future demonstration may use this profile only in its isolated disposable workspace and must label these as authored test-operator decisions. Inputs and plans cannot turn the profile on. External actions remain unavailable in C7.

Steps can declare up to eight simple JSON-pointer equality conditions on the native result. A returned failed/unsupported result does not automatically satisfy downstream capability: the frozen plan must require its relevant status/criteria before forwarding it. Failure retains the native result plus diagnostic, while only completed steps are eligible as input to later operations. A valid native JSON `null` remains a retrievable result, distinct from an absent/unresolved step.

Status returns compact step metadata and hashes; explicit output selection reads one bounded artifact. References copy selected native data literally and do not reinterpret model/source JSON as another template. Attempt history retains unresolved/superseded attempts with unknown usage and has a bounded reader. Every explicitly reconciled retry prepays another finite attempt record. No C0 transaction stays open while invoking another owner.

[ADR-010](../decisions/ADR-010-bounded-integrated-workflow.md) records alternatives and KISS/Five Whys/waterfall/MECE rationale. [The source/interface review](evidence/integration-source-review.json) preserves a scoped REVISE verdict and all original lane dispositions.

## Native interface allocation

| Existing pair | Request/result source mapping | Remaining limits |
| --- | --- | --- |
| C0↔C1 | Origin registration, bounded JSON or exact decoded native-byte capture, receipts/coverage | No new physical/source acquisition, interpretation or independent-truth authority. |
| C0↔C2 | Typed interpretation/get/submission and native derivation/commit results | Native modalities only; imported meanings and associations remain fallible. |
| C0↔C3 | Candidate proposal, separate operator commit, bounded query/read/dependency/status and progress handoff | No model truth oracle; actor/refinement/projection semantics remain partial. |
| C0↔C4 | Inquiry/jobs/export/import/candidate submission/frontier/outbox/ranking and assessment selection | No native vLLM/teacher execution; exact context/model/assistance binding remains explicit. |
| C0↔C5 | Compile/run/status/get and separate operator control | Supported IR only; process termination and numerical validity are not supplied by the coordinator. |
| C0↔C6 | Seal/compare/review/finding/yield/submission and bounded reads | Original cuts/criteria retained; diagnosis/advantage remains unqualified. |
| C0↔C7 | Proposal/read/check/internal dispatch/receipt/access/mask/report/model submission plus separate operator adoption/reconciliation/disposition | No external actuation or grant from a recommendation; local identities remain unauthenticated. |

All eleven interface facets are allocated: ownership stays native; authority uses fixed ports and separate operator inputs; shape/version uses strict 1.0 records; identity uses workspace/native request/artifact IDs and hashes; time/order uses immutable cuts/steps plus native clocks; delivery/idempotency keeps original resolved arguments/keys; commit/recovery uses prepaid local intents/receipts and explicit uncertainty; retention is finite without deletion/restore guarantees; resource limits bound plans/inputs/references/results/attempts/time; errors distinguish failed versus unknown completion; feedback grounding preserves generated/assisted/candidate material versus independently acquired outcomes. Native contract-specific behavior remains in each component guide, not replaced by this common coordination profile.

Whole-system loops remain conditional: C4 recommends through C0, C3 admits models, C5 produces trial results, C6 compares evidence and recommends revision, C7 separately authorizes operational change. Generated model/report echoes cannot acquire independent evidential status through C0. Shared host/clocks/storage and saturation remain common dependencies. Pair coverage alone does not prove semantic or runtime integration.

`observe-json` records the canonical serialization of a supplied structured value; it does not preserve that value's original transport whitespace or byte encoding. For exact source bytes, `observe-bytes` decodes a bounded validated base64 value and passes those bytes unchanged to C1. Media type, source/epoch, expected digest and origin/lineage remain explicit. This permits opaque/native media without pretending C2 understands every format. Base64 is a finite control-plane adapter, not an efficient unbounded media stream; large/chunked live acquisition needs the existing/future native C1 source adapters.

Default limits are 96 steps, 512 KiB plan, 256 KiB input, 4 MiB resolved arguments/result, 256 MiB accounted state, 10,000 accounted records, 30-second cooperative resume and 5-second writer wait. Each initial invocation prepays result capacity plus diagnostic headroom; this can limit how many worst-case steps fit under the default state budget. Admission still fails explicitly at quota rather than implying every maximal plan completes. Owner calls can allocate up to their own limits before C0 checks a result; no hard RAM/time isolation or HA is claimed. Runtime composition still initializes C1 first, so independent C0 status inspection during a C1 startup failure needs a future operational path.

## Controlled demonstration and frozen interpretation

Use a bounded local file as a measurable accumulator, with authored stock/flow laws and an instrumented local writer. Initial state and proposed rate are assumptions/configuration. Later raw file-size measurements come from the OS; they are not copied from C5 predictions. A deliberately changed write amount creates a discrepancy. This checks integration under a known controlled change; it does not discover an unknown real-world mechanism or represent all Meadows structures.

Measurements use a prespecified nominal sampling schedule; actual read time and scheduling jitter must be retained. The exact-match scalar measurement profile assumes the file state stays constant over each sampling window. Outcomes are acquired only after a post-commit future forecast confirmation. Input/output recording channels can differ while sharing the same apparatus; neither distinct IDs nor passing C6's local eligibility check establishes statistical/causal independence.

A generated measurement control uses explicit generated origin/lineage and must remain unscored. Allowed and refused C7 actions are separate assertions. The discrepancy can trigger attributed rivals, candidate revision, an access request and explicit operator-approved further inspection. Findings retain limits and are delivered only into C0's internal results.

## Verification and operating envelope

Future execution must follow the separate [holistic test design](INTEGRATED_TEST_DESIGN.md), retain first failures and freeze criteria/control splits before runs. Record Python/package/backend/source versions, wall time, CPU time when available, work/record counts and all failures. Inference tokens, session assistance cost, energy and hardware capacity remain unknown unless actually measured. No paid model/API, deployment, external notification, destructive operation or production source is needed for the initial local case. **No runtime or tests are run in this increment.**

Source integrity, runtime execution, model validity, useful learning and comparative superiority are separate conclusions. Results will be recorded after a later authorized execution; no demonstration result exists yet. Full C0–C7 qualification and native vLLM/large-model bindings remain open.
