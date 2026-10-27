# Comparison boundary - 27 October 2026

Scope: provider-free engineering preparation. The boundary passes 18 neutral checks on signed-in Kaggle Python 3.13.15. This is not a Cedar paired run, provider isolation qualification, financial budget enforcement or EDI superiority result. Completed Cedar episode cedar-sole-cd05b18d100b remains untouched.

## Implemented

examples/comparison/offline_runner.py adds an arm-local durable request/result channel, ordinary baseline notes and searchable raw history, an explicit native EDI session adapter, and a paired termination/evaluation fence. No provider SDK, model dispatch, credential handling, billing operation, network transport or automatic world launcher is present. invoke_paid_model always raises before any external action.

The operator supplies only an arm's authorized mission, public operation manual and public-call adapter. EDI requires a separately configured NEW native session under its own arm directory, matching model ID/revision and job token caps, with teacher/multi-stage work rejected. The current frozen helper's operator-declared assistant binding is not automatically replaced or promoted.

Requests persist exact serialized payloads with arm/request/cut identity. Reopening a pending request preserves its ID and reservation. Oversized requests stop without truncation. Responses retain original bounded bytes; oversize responses retain only size/digest, explicitly not the full bytes. Wrong-arm, duplicate, malformed, duplicate-key and nonfinite JSON responses cannot dispatch an action. A retained response whose application was interrupted blocks new exports until operator reconciliation. An action intent and prospective predictions commit before dispatch. Unknown dispatch outcomes block replay after reopen. One bounded validation correction is allowed. Failed public calls count and remain in history. Baseline notes are editable; raw receipts, rejected attempts and proposals remain accessible through literal search and byte-range reads. History search streams matches rather than assembling all result bodies in memory.

The budget is finite: 64 accepted decisions, 128 model request reservations, 12,288 input and 4,096 output policy tokens per request, 2,097,152 reserved policy tokens, 262,144 request bytes, 65,536 response bytes, 256 public calls and six hours per arm. Rejected requests consume model reservations. Expired pending exports and late responses are blocked. These are policy reservations, not actual token measurement or monetary limits; no tokenizer/provider cap is implemented here. Public receipts have a 4 MiB return bound checked after the trusted callback returns. This is not a streaming transport bound.

Evaluation is operator-only, requires both explicit terminal dispositions, preserves failures and retains the first result. Terminal dispositions are operator declarations, not independently attested world completion. There is no method feeding evaluator output to participants. Work is serial on a trusted host; SQLite files do not constitute process sandboxing or independent anti-tamper isolation.

## Requirements and endpoint contracts

R1: exclude cross-arm evidence and stale responses. R2: preserve a strong ordinary-memory baseline. R3: retain predictions before outcomes, receipts and failures. R4: bound calls, bytes and elapsed time; disclose unmeasured costs. R5: prevent unknown-outcome replay. R6: withhold evaluation until both arms terminate. R7: no paid inference or completed-run mutation. R8: establish model/input/world parity before a scientific launch.

Seven registered roles: C operator coordinator plus channels; B ordinary baseline; E native EDI adapter; Wb baseline public broker; We EDI public broker; M external model transport (unimplemented); V terminal evaluator. Wb and We are required separate future broker instances, not currently launched worlds. C's scheduling/lifecycle operations are operator orchestration, not an implemented unattended runner. Native C0-C7 internals remain unchanged; this is a scoped external boundary review, not a renewed claim that every existing internal lane passed.

Every unordered pair and both directed lanes are represented below (21 pairs, 42 lanes). R means required by the proposed deployment; P means prohibited. An R does not claim an endpoint has been implemented or runtime-qualified.

| Producer  consumer | C | B | E | Wb | We | M | V |
|---|---|---|---|---|---|---|---|
| C | - | R | R | R | R | R | R |
| B | R | - | P | R | P | P | P |
| E | R | P | - | P | R | P | P |
| Wb | R | R | P | - | P | P | R |
| We | R | P | R | P | - | P | R |
| M | R | P | P | P | P | - | P |
| V | R | P | P | R | R | P | - |

CB/E: arm-local exports, explicit imports and terminal declarations (R1-R6). BWb and EWe: selected public operations and native public receipts only; broker credentials stay operator-owned (R1,R3,R5). CWb/We: fresh lifecycle, pinned mission/manual and equivalent initial-state attestations (R7,R8; not implemented). CM: exact authorized request and routed model proposal with common model/settings and verified usage (R1,R4,R8; unimplemented). CV: evaluate only after both terminal, preserve first outcome including failures (R6). VWb/We: post-terminal private evaluation reads/results, never participant input (R6). All P lanes prevent direct cross-arm sharing, direct model access to world/private evaluator, and evaluator feedback into reasoning. A read request and its return are separate directed operations.

Eleven review facets applied to the active contracts: purpose/requirement; producer and consumer port; authority; schema/native values; identity/version; evidence provenance; temporal validity/order; resource accounting; failure/recovery; admission/mutation owner; verification evidence. Runtime checks cover the channel and baseline fixtures, not all required deployment contracts. Supplemental skill checklist/template reads failed; bundled interface_matrix checker was unavailable and was not run. This is a self-review, not independent review.

Durable authorities are channel DB for model exchange, baseline DB for notes/history/action intent, native owners for EDI admission, each future broker for world state, and pair DB for declared terminals/first evaluation. Private world state and source code do not enter participant requests. One host/operator remains a shared dependency capable of contamination. Model provider hidden state is outside this boundary's authority.

Feedback risks reviewed: generated notes returning as supposed evidence; action retry after a lost receipt; duplicate/stale model import; private evaluation leakage; shared broker/store state; prompt/history saturation; wall-clock expiry; and selective removal of failures. Neutral checks address the first operational paths. Unknown usage remains unknown. Fresh scientific variants, multimodal public-evidence rendering parity, common prediction-scoring opportunities and actual runtime/world equivalence remain unresolved.

## Actual verification

First immutable source archive: 15 checks passed on Kaggle in 2.667 s. Static review then added late-response/expiry rejection, strict JSON checks, streaming history search and additional adapter checks. Second separate archive: 18 checks passed in 2.482 s, with a ResourceWarning from a connection opened before rejecting changed configuration. Closed that handle before raising, then ran the same 18 checks in a third separate archive: all passed in 2.690 s with no ResourceWarning. All three runs and source hashes are retained; the earlier warnings were not erased. No failed runtime check was relabeled. Local work was source writing, AST parsing and packaging only. All product execution/tests occurred on Kaggle through CUA. No model or Cedar episode ran.

Final runner SHA256 f1072d3477459a91e8d61e8ae8760b49211a4bad8469cf3536616972bc08cd0a. Test SHA256 4b2a533e5b344b66abfbc453717abbcad03717ad1eddff9d03eaeb9d0713e1b2. See evidence/comparison-boundary-20261027/kaggle-results.json and kaggle-test-output.txt. UI readbacks are retained evidence, not raw provider response bytes or a trusted independent evaluator signature.

Kaggle preparation notebook https://www.kaggle.com/code/vigini/edi-controlled-comparison-preparation-20261026/edit saved Version 4, Quick Save WITH OUTPUTS, named Neutral boundary - final 18 checks - no models. Version3 retains the earlier two source runs. Draft session explicitly stopped after saving. No secrets added. Prior paused version remains historical.

Gates: neutral channel/baseline fixture checks PASS within this scope; architecture/contracts REVISE because complete deployed adapters/parity are absent; native EDI/Cedar paired integration BLOCKED; provider context/model/usage qualification BLOCKED; financial gate NOT IMPLEMENTED and paid route DISABLED; scientific comparison NOT STARTED. This code must not be described as a fully connected or benchmark-ready comparison runner.

Next concrete engineering task is a provider-specific isolated transport and budget gate paired with the existing native EDI boundary and a public-only baseline broker adapter. Before any live comparison, qualify identical Cedar initial conditions and public multimodal access, common model/settings, request caps and usage, complete five-year reports and all paired outcomes. A provider change or paid calls need explicit authorization; do not send the owner back to project-memory setup or silently substitute another model.

