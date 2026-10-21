# Integrated workflow skeleton — design asset only

`integrated.template.json` is an authored 28-step coordination skeleton across C0–C7. **It has not been instantiated or executed.** It is not a complete runnable test manifest: exact native inputs, model binding, clock/correspondence policy, fixture IDs, revisions, resource profile and acceptance thresholds must be reviewed and frozen first under the [holistic test design](../../docs/implementation/INTEGRATED_TEST_DESIGN.md).

The skeleton shows real native handoffs: register sources; record/decode/host input; explicitly admit an authored model; create/export/import C4 work; host rivals; compile/run/seal; pause for later measured input; compare/review/retain a candidate revision/finding; review access; propose and separately adopt a policy; authorize an internal read; qualify an attributed actor mask; deliver the finding internally.

Every `$input` is a named **immutable external data value** supplied later. It is not a hidden simulated model output. Every `$step` selects an earlier committed native output with a bounded JSON pointer. Returned source/model JSON is copied literally and never recursively evaluated as another template. Native request IDs are generated deterministically when omitted.

`model-admission` and `policy-adoption` require the separate trusted-local `WorkflowOperatorInput` API and an explicitly enabled operator profile; ordinary model/data input cannot satisfy them. Never enable this SDK/CLI for untrusted callers merely because an operator label is present. Exact C3 and C7 revisions must match the recorded operator decisions; no automatic rebase or admission is implied.

Before any later run, freeze at least these native contracts:

- Source specifications and original setup account; source versus measured apparatus clearly distinguished.
- Complete consistent C3 model/IR and explicit modeling-use assumptions. Include model/participant versions and native stocks/flows together; do not assume an admission revision leaves versions unchanged.
- Inquiry/job/response bindings and context hashes. An unbound native job accepts authored proposals only; authored/imported work cannot be reported as native vLLM execution.
- Supported compile request, scenario/solver and prospective cases/rules with future targets and scoring criteria.
- Outcome capture must use C6's exact `measurement-v1` kind, correct source/epoch, `edi.measurement/1.0` JSON and clock/correspondence semantics. Preserve actual sensor-read times/jitter; never copy predicted values into outcomes or backdate samples.
- Fixed comparison cut, review/candidate/finding evidence references, distinct operator policy decision and scoped internal action.
- Required native result conditions: a successful function return is not sufficient when the native artifact says unsupported, failed or ineligible.

The suggested initial mechanism is small enough for an engineering handoff check only. The wider nonlinear, human, growth, uncertainty, recovery and comparison scenarios remain separately planned and may require missing adapters. No workflow, database, model, solver, test, example or benchmark has been run. See [source scope](../../docs/implementation/C0_INTEGRATED_WORKFLOW.md) and [native model/tool readiness](../../docs/implementation/INTEGRATION_READINESS.md).
