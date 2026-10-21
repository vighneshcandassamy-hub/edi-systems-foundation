# Handoff for the next test-planning conversation

Consolidation ends with an organized development package. No test starts automatically, no model has been selected and no EDI runtime is modified or connected here.

| Decision | Information needed |
| --- | --- |
| Actual EDI runtime | Repository/path, revision, entry point and observation/action interfaces |
| Model and execution location | Available model, compute context and supported native modalities |
| First test purpose | Unguided integration diagnostic, human pilot or frozen comparison; distinct claims |
| Adapter | Tool exposure, asset decoding, provenance handling, retry/session semantics |
| Isolation | Allowed files, account/container, broker route and blocked owner/evaluator access |
| Initial presentation | Pinned mission and generic access; changes versioned equally across comparison arms |
| Resource accounting | All model/helper tokens, wall time, compute/energy where measurable and transport metrics |
| Stop/resume/failure policy | Practical limits, checkpointing, non-progress handling and infrastructure versus reasoning failures |
| Outcome interpretation | Dimensions of interest, uncertainty/objective review and prospective forecasts if desired |
| Comparison, if requested | Matched model/tools/authority, competent baselines, instances, resources and uncertainty analysis |

These are planning inputs, not an investigation sequence for EDI. Do not insert operator audit topics, expected feedback loops or suggested hypotheses into its prompt to make it succeed.

## Available material

- [Definition](BENCHMARK_SPEC.md), [readiness](READINESS.md) and [participant starting files](participant/).
- [Operations](environment/v0_2/PUBLIC_OPERATIONS.json), [resources](environment/v0_2/RESOURCE_CATALOGUE.json) and [operator commands](environment/v0_2/README.md).
- [Implementation pin](environment/v0_2/reports/BUILD_PIN.json), [existing validation](environment/v0_2/reports/VALIDATION.json) and [requirements](environment/v0_2/REQUIREMENTS.json).
- [Operator-only interlude audit](operator-audit/README.md) for environment review, not participant coaching.

When a run is later configured, retain package/world/model/adapter revisions, initial prompt, tools/source access, run identity, start/stop/resume events, actual requests/responses, acquired assets/lineage, participant reports, resource measurements and analysis limits. Preserve failures and pending human decisions. Keep secrets and private session databases outside Git.

No success threshold, inference budget or model advantage is invented in this handoff. The existing outcome vector is available; a complete reasoning/comparison protocol remains to be designed.
