# Integrated application configuration

This guide configures the existing C0-C7 application and autonomous controller. The scheduled 0.10.1 execution is recorded in [ENGINEERING_RUN.md](../../docs/implementation/ENGINEERING_RUN.md); the autonomous controller remains unqualified. The loopback BrokerConnector supplies public-world access. Serving and pinned C5 execution require separate environments under the recorded dependency versions.

1. Prepare a fresh workspace and an operator-issued SimulationGrant for the
   intended public-world broker. The broker, student service and EDI application
   must share the explicitly configured host/loopback environment. The existing
   frozen forest package is not changed or automatically launched.
2. Copy application.template.json outside Git. Replace every REPLACE value,
   including the actual granted session/mission/token hashes and time interval.
   Supply only named broker/student secrets in the environment. Never commit
   actual secrets, session state, model weights or teacher exchange files.
3. Configure the declared teacher identity/version. File exchange supports the
   existing subscription/manual workflow without an inference API. Its identity
   and usage remain operator-declared, not provider-verified. File transport is
   not automatic ChatGPT serving and does not update weights. A separate paid
   teacher transport is neither required nor enabled by this configuration.
4. `edi integration-config PATH` validates configuration only; it does not create
   Runtime, stores, a broker session, model job or model request.
5. After the separate testing stage is authorized and prerequisites are running,
   `edi integration-step PATH` performs/resumes one controller turn. No fixed
   sources/read/submit sequence or domain explanation is supplied. The model can
   choose public operations, acquired context, component reads/requests, selective
   teacher critique or yield. A fresh application process resumes the original
   journals; an unknown provider completion is never silently resent.
6. If the result is waiting-teacher, use the exported request with the declared
   teacher. It contains the original cut, student attempt, selected images and
   critique rules. Save only the feedback fields shown below, then run
   `edi integration-teacher-import PATH JOB_ID FEEDBACK.json` and resume with
   `edi integration-step PATH`. The next student job receives the retained critique.

Feedback envelope (content is supplied by the teacher, not by this repository):

```json
{
  "rationale_summary": "REPLACE_WITH_TEACHER_CRITIQUE",
  "limitation": "REPLACE_WITH_TEACHER_LIMITATIONS",
  "feedback_disposition": "retained-for-review"
}
```

Optional `usage` has nullable integer `input_tokens`/`output_tokens`. Missing
counts are unknown; C0 charges the corresponding full reservations. This is not
an exact measured subscription-token cost. Rejected feedback is retained as a
rejection, never silently edited into valid scientific content.

Existing C3 operator admission and C7 policy adoption use the separate native
trusted-local Workflow/CLI APIs. The reasoning model cannot call them. Candidate
learning, analysis, assessment advice and authorized operational adoption remain
different states. Numerical execution still requires the original supported
operator grammar and declared numerical dependencies. General delay, hybrid,
actor dynamics or future weight training are not implemented by this wiring.

No commands in this example have been run as an integrated/model test for this
source increment. Build checks and future runtime verification are separate.
