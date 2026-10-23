# Information-seeking controller repair - 23 October 2026

Version **0.10.7.dev0**. Scoped native regressions pass. **Autonomous readiness
remains REVISE; live verification and the Meadows diagnostic have not run.**

The latest real Qwen result remains the retained 0.10.5 failure: it yielded after
the mission without requesting information. This change repairs the executable
stopping contract and clarifies information-request justification; it does not
claim the model now investigates successfully.

| Change | Reason |
| --- | --- |
| Native progress and actual public receipt headers supplied by C0 | Separate what has happened from a model's proposed actions and a bounded evidence cut |
| Information need may justify an authorized request | Absence of readings is not an empirical finding that readings are inaccessible |
| Structured yield reason, unresolved needs, alternatives and resumption condition | Empty or unexamined stopping no longer silently satisfies the new decision contract |
| Explicit optional teacher availability | Unavailable critic requests receive native feedback; configured critic remains selective |
| New policy/version; older C0 journals require a fresh workspace | Preserve historical artifacts and dispatch identities |
| New mandatory launch preflight | Check actual serving grammar before live inference |

The assessment remains an attributed judgment. A model can deliberately stop
before gathering data; that outcome fails acquisition acceptance. No requirement
to try all sources, spend the budget, repeat a request, or invoke a teacher is added.

## Verification

[Nine native regressions](evidence/information-seeking-20261023/native-regressions.json)
pass using authored model outputs and the actual neutral HTTP handler invoked in
process. They check rejected empty yield and accounted correction; deliberate
stop and restart without redispatch; actual receipt/capacity metadata after
restart; invented stop alternatives; unavailable teacher feedback; selected
teacher critique/student revision; strict/legacy decoder requirements; closure
receipts; and failed public status preserved as failure. These are engineering
fixtures and are never supplied as an investigation script to a live model.

The wider baseline suite ran 31 tests: 21 passed; 10 errored because this host
blocks TCP loopback with WinError 10013. The unmodified result is retained under
[cpu-base](evidence/information-seeking-20261023/cpu-base/cpu-tests.json).
An earlier test invocation also hit the host's unwritable default temp location;
its raw result remains under cpu-initial. The task-scoped temp directory corrected
that environment setting. Neither run is reported as an all-tests pass.

The same nine regressions also pass on Python 3.12 and from the unpacked portable
launch bundle. The wheel builds and all 69 core Python files match source bytes.
The complete owner/outside matrices, component-review consistency and frozen
source/package integrity checks pass; see [final checks](evidence/information-seeking-20261023/final-checks.json).

Local jsonschema/xgrammar are unavailable. The launch package now embeds
check_information_seeking.py and its fixture tests and requires --grammar in the
pinned serving environment before model startup. This check fails closed on
missing dependencies or a decoder error. Network/model-service validation and
actual model input token counts remain to be measured there. No throughput,
latency, energy, cost, inference-quality or advantage result is claimed.

[Decision and tradeoffs](../decisions/ADR-013-information-seeking-and-stopping.md),
[trace](evidence/information-seeking-20261023/TRACEABILITY.json),
[component review](evidence/information-seeking-20261023/COMPONENT_REVIEW.json),
[owner matrix](evidence/information-seeking-20261023/OWNER_INTERFACE_REVIEW.json)
and [outside matrix](evidence/information-seeking-20261023/INTERFACE_REVIEW.json)
separate native contract checks from live capability. All reviews are self-review.
Historical broader gates remain unchanged.

## Next execution

Use a fresh directory/workspace and the same pinned Qwen weights, neutral
objective, resources, acceptance and budgets from the original protocol.
The launch preflight must pass before starting inference. Retain raw outputs,
all corrections, actual broker receipts, teacher usage/waits, complete token
accounting, fresh-process restart, all owner integrity and source hashes.
A considered yield without acquisition remains a failed autonomous diagnostic.
Do not start Meadows or claim readiness based on authored fixtures.
