# Existing-component integration handoff

This page preserves the 0.10.0 source-only handoff. Subsequent 0.10.1 execution, source defect and repairs are recorded in [ENGINEERING_RUN.md](ENGINEERING_RUN.md). Wider original qualifications remain open.

22 October 2026. Source baseline 9b275da82e69cd0b77b7d63525067721017a165c;
implementation 0.10.0.dev0 / edi-c4/0.6.0. The owner directed completion of the
existing component wiring before testing. This increment builds those paths.
It does not execute a workflow, store operation, model call, simulation, product
test or benchmark. Earlier results remain at their original revisions.

## Scope and architecture reference

The integrated seven-chapter architecture and appendix, v0.8 engineering
extension, REASONING_INTEGRATION.md, COMPONENTS.md and the individual C1-C7
implementation guides govern this work. Fixed pretrained weights, selective
fallible teacher critique, C3-owned model admission and C7-owned operational
authority are retained. Future parameter training remains dormant, as specified.
No new representation family, domain hypothesis, forest explanation, prescribed
investigation sequence or scientific acceptance threshold is introduced.

Reviewing the source found a distinction hidden by the earlier status reports:
Runtime composed eight owners and Workflow exposed many native methods, but
Investigation reached only seven operation classes. Its analysis results were
stored only in C0 state and did not enter the next inference context. Teacher
job scaffolding existed, but the available $0 application had no usable teacher
transport. A returned semantic rejection left C4/C0 pending. These are wiring
and lifecycle gaps, not evidence of a fundamental failure of EDI's approach.

## Connections now present in source

| Owner / role | Connected native path | Return / persistence path |
| --- | --- | --- |
| C0 | IntegratedApplication composes Runtime, scoped broker authority, student gateway, teacher exchange and Investigation. CLI loads one application profile. | Original turn/phase identities, deadline, bounded correction and conservative token accounting. |
| C1 | Existing BrokerConnector capture and asset acquisition; C0 metadata replay/coverage; selected bytes reach C4. | Exact source bytes stay in C1. Generated component/model/teacher artifacts remain generated. |
| C2 | Existing interpret, get-derivation and candidate submission operations. Model annotations receive actual C4 assistance attribution. | Derivations/results enter subsequent bounded context; submitted IDs can be selected in C3. |
| C3 | Existing revision-pinned reads, query and dependency views; C2/C4/C6/C7 candidate submission paths. | Candidate IDs survive continuation and can be queried later. Existing operator admission remains a separate trusted-local API. |
| C4 | Explicit native inference-port binding, student jobs, same-cut selective teacher jobs, revised student jobs and explicit returned-output rejection receipts. | Accepted responses and generated teacher critique persist in C4/C1; a bounded memory artifact reaches the next turn. |
| C5 | Existing compile, run, get-run and get-compiled APIs through C0. | Native artifacts return to the reasoning context, including explicit unsupported/error outcomes. |
| C6 | Existing seal, compare, revision review, finding, inquiry-yield, candidate submission and read APIs. | Attributed assessment results/advice return through C0; prospective/eligibility checks stay in C6. |
| C7 | Existing policy proposal/read, action check/internal dispatch, receipt, access review, actor mask, report and candidate-model submission APIs. | Results return through C0. Existing operator adoption, access disposition and reconciliation remain separately controlled. |
| Student | NativeGateway + pinned loopback VllmBackend; explicit exact token preflight. | Raw generated wire retained before native content admission; completed calls are not new inference attempts. |
| Teacher | TeacherExchangeGateway exports the original cut/attempt, retains imported critique and resumes a student revision job. | Explicit waiting input. Operator-declared identity/usage; generated assistance, no direct world/model/adoption authority. |

`src/edi/inquiry/operations.py` is a finite catalogue over existing ports. A
`component-call` proposal names one native operation and its arguments; C0 supplies
workspace and request identities. `describe-operation` exposes the relevant native
argument schema on demand, avoiding every schema in every model prompt.
`observation-records` pages the already permitted C0 read-only C1 metadata port;
actual bytes reach reasoning through explicit selected context. C0 acknowledges receipt of C4 outbox proposals separately from executing them. The model still
chooses the operation and evidence. The original public world operations and
legacy analysis envelopes remain available.

The all-pair review retains eight owners, 28 pairs and 56 directed dispositions.
There is no new C4-C5 or C4-C7 bypass. The external inventory retains five roles
and 20 directed lanes. The teacher request/result lanes now describe file exchange
instead of implying an enabled paid provider. Wider historical obligations are
not promoted by this source handoff.

## Student and teacher lifecycle

A student job uses a pinned evidence/model cut. If it requests teacher review,
C4 creates a teacher job against the same cut, with the student's retained attempt.
The teacher export includes selected images where supported. No model is invoked
by exporting. A local operator imports the teacher's content using the CLI; C1
retains the raw generated bytes, C4 validates critique authority, and C0 requests
another student job. Revised candidates are submitted through the same C3
candidate-only port as initial candidates. A teacher cannot submit hypotheses,
operation requests, accepted model changes or operational decisions directly.

This supplies a connected **manual teacher transport** for the $0 configuration.
It is not an automatic ChatGPT subscription API. Teacher model/version/usage and adherence to the exported cut are
operator-declared; authentication, outside information exclusion and exact provider measurement are not claimed.
Missing usage charges the corresponding full reservation. The existing separate
OpenAITeacherBackend source is not enabled by the application or this work.
No paid call, credential entry or weight update occurs.

## Failure and continuation contract

Definite returned output that fails shape or semantic checks has retained raw
C1 bytes, diagnostics, original job/cut and usage in a C4 rejection record. It
cannot trigger its proposed operation. At most one correction job for a rejected
attempt is permitted by the initial profile; each is a distinct native job under
one inquiry's bounded rounds/jobs/tokens and the original persisted deadline.
Both rejected output excerpts and diagnostics are supplied as unaccepted generated
material. No hypothesis/reference is invented and no scientific field is silently
removed to obtain admission. Exhaustion yields and preserves failures/costs.

Unknown provider completion, prompt-usage mismatch and storage uncertainty are
separate states. They do not authorize a new inference or scientific correction.
The provider journal remains authoritative for whether a call was dispatched.
A failed preflight before any recorded dispatch returns waiting-model and retains
the original pending native job; restoring the dependency can resume that job.
C0's local phase resume uses original native request identities; broker duplicate
handling and native command receipts remain their existing owners' responsibilities.
A process-local lock is not hard multi-process isolation or an HA claim.

Known denied/unsupported/invalid tool requests return attributed error artifacts
for another model decision. Component outputs and bounded reasoning memory enter
C1 as generated material; they cannot become independent corroboration by passing
through another owner. A context slice can truncate large native artifacts, with
range/size retained; complete artifacts remain accessible by native IDs/read APIs.
All available records need not fit one inference. No retention or cost guarantee
beyond the selected finite local profiles is implied.

## Configuration, build and readiness

Use [examples/integration](../../examples/integration/README.md) for the configuration
and manual-teacher commands. ApplicationProfile validates owner workspace/path
separation and model binding correspondence before opening Runtime. Configured
paths resolve relative to the application file. Secret values come only from named
environment variables and are absent from configuration/journals. The application,
broker and vLLM must share the explicitly configured loopback environment. This
work neither launches them nor exposes a public tunnel.

Use fresh integration workspaces. Historical 0.9.x episodes/journals are preserved;
this source version does not migrate or resume them as new-version episodes.
The C4 contract version changes to make that boundary explicit.

Build verification is AST/import/CLI construction, generated contract/reference
consistency, source-to-operation inventory and review/trace consistency only.
The checker never constructs Runtime, opens stores, performs model calls or runs
product cases. Source hashes and generated contracts are retained in
[evidence/component-connections-20261022](evidence/component-connections-20261022/source-checks.json).
All new runtime cases are planned and unrun, as directed. The previous 28-check
and model results apply to 0.9.4 only; none is carried forward as a new-version pass.

The existing components implement subsets of the full conceptual architecture.
Connecting them does not add missing delay/hybrid/actor solvers, general perception,
physical actuators, authenticated multi-user authority, hard process isolation,
HA or a trainer. Those are pre-existing implementation limits, not disconnected
ports fixed by a different diagram. C5/C6 retain their original supported-model,
forecast timing and independent-outcome restrictions. A simulated world does not
become an independently observed physical outcome through this wiring.

Next stage: review this concrete source handoff, then separately execute integration
verification and debug observed defects. No model trial or forest benchmark is
started by this change.
