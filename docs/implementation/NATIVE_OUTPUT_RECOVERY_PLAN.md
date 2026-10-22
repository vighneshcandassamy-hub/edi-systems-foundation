# Native output recovery and inquiry selection: next development gate

Proposed scope after the retained 22 October 2026 rerun. **Not implemented or qualified by this document.** Parent obligations: RP-R02, RP-R04, RP-R06 and RP-R10.

## Reproduced problem

The current C0 turn claims its journal entry, obtains a real C4 response, then calls native import. When semantic validation rejects the response, the turn remains pending. C4 still awaits import although the gateway has retained the provider answer and known usage. Original retry does not redispatch, which prevents duplicate effects, but there is no explicit terminal rejection/correction transition. The controller cannot simply continue.

The latest model output also chose no operation and treated the operation catalogue as the whole available world. Its test targeted API names rather than hypotheses. Removing the invalid annotation would still leave no information-seeking decision. Output validation and autonomous inquiry are separate acceptance obligations; this one trial does not identify whether model capability, request representation, context emphasis or controller design caused the passive behavior.

## Bounded implementation proposal

1. Trace a definite native rejection separately from provider timeout/unknown completion. C4 should retain the original raw C1 reference, immutable validation diagnostics, pinned cut and measured or conservatively reserved usage in an owned rejection receipt. It must never create missing hypotheses or repair evidence references silently.
2. Extend C0 coordination with an explicit rejection/correction-or-yield transition. The inference, validation and action-dispatch phases must be distinguishable, including crash recovery. A known invalid response must not masquerade as an unknown external action, and a truly unknown provider call must not be automatically retried.
3. If correction is allowed, allocate a distinct native job/attempt ID under the original turn's overall token/time/action budget. Supply only the original objective/cut, unaccepted output and machine validation diagnostics. At most one correction is the initial proposed limit; exhaustion yields durably. Original output and failure remain visible, and all call costs count.
4. Review the model-facing envelope for an intake decision. Compare the current full native schema with a compact typed operation interface that binds native IDs/provenance deterministically. Choose only after checking expressiveness and authority. Preserve all available operations and the model's choice; do not mandate sources/read/submit or supply a hypothesis.
5. Repeat the identical instrument mission/data and evaluate information acquisition plus the final report. An output with no next operation can be a legitimate explicit yield, but cannot be scored as solving this objective. A valid wire with no investigation also fails this gate.

A read-only partial-admission design is an alternative requiring a separate contract decision. It must not quietly discard invalid knowledge fields while labeling the whole response accepted. No such partial admission is implemented now.

## Required verification before live repetition

| Case | Required behavior | Status |
| --- | --- | --- |
| NR-V001 | Bad references retained; no proposed action dispatched; known usage charged | Planned |
| NR-V002 | Corrected response uses a distinct bounded job; original call is never replayed as new inference | Planned |
| NR-V003 | Provider-unknown outcome remains unresolved; no automatic correction dispatch | Planned |
| NR-V004 | Crash between rejection and correction reopens exactly once; no duplicated action | Planned |
| NR-V005 | Second invalid output or exhausted token/time budget yields with complete retained cost | Planned |
| NR-V006 | Authority/context/evidence violations cannot gain rights through correction | Planned |
| NR-V007 | Same live instrument case acquires data and submits a grounded, uncertainty-aware report | Planned |

C0 owns coordination, C4 owns reasoning-job/rejection state, C1 owns retained bytes, C3 owns knowledge admission and C7 keeps action authority. No cross-owner direct database mutation or new direct model/world route is proposed. C5/C6 and teacher adoption remain separate work. Update the existing 56-owner-lane/20-outer-lane review and source trace when implementing the changed states/ports.

Success is a native, observable workflow with retained failures and bounded recovery. It is not evidence of forest discovery or an EDI advantage over another system. Keep the frozen benchmark and original scientific acceptance criteria unchanged.
