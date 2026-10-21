# C7 authored templates — not executed

These JSON files illustrate the [C7 contracts](../../docs/implementation/C7_AGENCY_RUNTIME.md). They are request templates, not successful tests, installed policies or verified fixtures. Replace every `REPLACE-...` value, including UTC dates and native IDs, before any later explicitly authorized runtime use. No example has been run.

1. A future C0/operator workflow registers an actually permitted source with C1. `report-origin.template.json` illustrates a separate generated-report source; it grants no access and is not an external connector.
2. `policy-proposal.template.json` proposes a bootstrap research policy at revision zero. It creates no grant until a separate authorized decision.
3. `adoption.template.json` illustrates that separate trusted-local operator decision. The configured operator label is not authentication; never expose this CLI/SDK to untrusted callers.
4. `action.template.json` requests a bounded native metadata read under the adopted revision and exact grant. Its allowed decision is not dispatch or an observed effect.
5. A later `DispatchRequest` names that decision and stable request/execution IDs. Original retry returns the same status. An interrupted command remains unresolved until explicit archived-report reconciliation; it is not automatically run again.

No shell/network/action tool, model call, paid resource, source acquisition, policy adoption, C3 submission or simulation is triggered by these files. External actuation remains unavailable in this code profile. C0 orchestration, native reasoning binding and all runtime/security/scientific qualification remain open.
