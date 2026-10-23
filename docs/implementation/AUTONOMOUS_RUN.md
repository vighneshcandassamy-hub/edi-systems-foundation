# Autonomous controller engineering investigation — 23 October 2026

Current source: **0.10.5.dev0**. The three engineering steps are complete, but
**autonomous investigation readiness is REVISE**: the student yielded without
acquiring information. Native execution/restart checks pass. **The first Meadows
diagnostic has not started.**

The authorized task is to inspect existing controller wiring, let the student
choose operations from an objective and access catalogue, then retain evidence
and verify fresh-process continuation. No live operation sequence, hypothesis,
pre-admitted analysis model or compulsory teacher cycle is supplied.

The original [protocol](evidence/autonomous-20261023/protocol.json) remains
unchanged. Its source-version statement describes the initial attempt;
[execution amendment](evidence/autonomous-20261023/execution-amendment.json)
records subsequent engineering repairs without changing acceptance or resources.
[ADR-012](../decisions/ADR-012-autonomous-controller-contract.md) gives the design
and native serialization corrections.

## Current live result

The final live run made one real student call:4,018 input and170 output tokens,
4,188 policy units, zero unknown usage and zero rejected outputs. The student
selected an explicit yield after seeing only the mission. Its rationale treated
missing readings in the selected context as preventing an information request.
It requested no source catalogue, document, interview, teacher review or final
submission. The0.10.5 generic access clarification did not resolve that behavior.

| Predeclared criterion | Actual result |
| --- | --- |
| Autonomous acquisition beyond bootstrap | Failed: only the mission reached the broker |
| Raw instrument data used in final submission | Failed: no instrument record acquired and no submission |
| Supported conclusion and uncertainty | Not demonstrated; abstention avoided invented measurements but did not satisfy the mission |
| Native fresh-process restart without redispatch | Passed: identical snapshot, zero new model/broker requests |
| Eight databases, retained failures, source/model pins | Passed: all integrity checks OK;76 exported source files verified; all69 core files equal source and wheel |

See [runtime results](evidence/autonomous-20261023/runtime-results.json),
[acceptance review](evidence/autonomous-20261023/ACCEPTANCE_REVIEW.json),
[native restart](evidence/autonomous-20261023/native-restart-audit.json) and
[build verification](evidence/autonomous-20261023/build-verification.json).
The owned model server and Kaggle session are stopped after evidence recovery.
No paid API or parameter training was used.

This separates corrected execution defects from the remaining student/protocol
information-seeking behavior. It does not establish a general inability or a
fundamental architecture failure. Next work is a scoped design review of native
information-seeking and stopping/escalation semantics before another domain
trial. Do not substitute an authored resource sequence or force a teacher merely
to make this acceptance pass.

## Repairs and verified engineering checks

- A controller inquiry explicitly requires one next-operation proposal or yield;
  proposal-only mode remains available. Teacher output remains critique-only.
- Structured decoding uses exact complete evidence references, including lineage.
  Native semantic validation remains decisive; model output is never repaired.
- Schema-aware providers send the full decoder separately and use a field index
  in the prompt. The original data cut, other control and validation are unchanged.
- The configured completion timeout is bounded30..900 seconds; this T4 profile
  uses600 seconds for a4,096-token output cap. Unknown dispatched work is not resent.
- C0 command identity and unresolved-call lookup use JSON-native proposals.
  Canonical JSON also converts nested native component results. Existing valid
  JSON canonical bytes/identities stay unchanged; arbitrary objects are rejected.
- All eight owners are constructed during preflight. This is not a business
  execution or qualification of each owner.

The controller/grammar regression checks complete references, missing lineage,
missing controller decision, legacy proposal-only output, an empty evidence cut,
actual xgrammar compilation and byte-identical data under transport compaction.
The [dispatch regression](evidence/autonomous-20261023/dispatch-regression.json)
uses an explicitly authored sequence and no inference. It exercises real native
C0/C1/C2/C4/C7, broker requests, invalid-asset feedback, source discovery, raw
reading, interpretation, submission, reopen without redispatch and unresolved
broker response handling. It is not autonomous model evidence.

All28 [CPU integration checks](evidence/autonomous-20261023/cpu-regression-0.10.5/cpu-tests.json)
pass. The first run retained two stale seven-operation catalogue expectations;
the catalogue already included component-call. Corrected checks also verify a
valid component call and the native DENIED result for direct world admission.
The intermediate fixture exception mismatch remains in cpu-regression-fixed.

## Retained attempts and failures

| Attempt | Observed result and retained limits |
| --- | --- |
| Initial0.10.1 | Yield after two rejected outputs; printed19,747 input/1,672 output tokens. Restart exit1. Original raw diagnostics/databases were lost after VM expiration; their cause is not inferred. |
| Retained0.10.1 repeat | Both native rejections identify an evidence reference outside the pinned selection: correct record/hash, omitted lineage. Both responses lacked a next operation.20,028 input/1,878 output tokens. Fresh snapshot identical; five existing stores pass integrity. Exit1 came from the harness expecting eight lazily opened stores, not native corruption. |
|0.10.2/0.10.3 diagnostic | Two outputs admitted, then the third job stopped before dispatch for prompt capacity. Removing duplicate schema allowed the same job/cut to resume. Twelve decisions were ultimately admitted, with129,708 input/4,475 output tokens and zero unknown usage. However, **none of the selected operations reached the connector**: a nested OperationProposal failed JSON serialization during C0 command hashing. Only bootstrap mission reached the broker. Operator stopped after a completed turn; native reopen and eight-store integrity passed. |
| First authored dispatch regression | Explicit proposal conversion reached the broker but exposed the same nested serialization issue in C2 result envelopes. Submission bookkeeping did not finish. The shared serializer repair then passed the complete regression. |

The12-turn diagnostic initially appeared to be student non-progress from live
counters. Raw feedback corrected that diagnosis to a pre-connector code failure.
It cannot isolate student error recovery or establish a fundamental architecture
failure. The model did repeatedly choose the mission observation ID as a document
ID; that attempt cannot isolate its response to proper native connector feedback.
The subsequent0.10.4 clean-yield result is preserved in
[retained-premature-yield.json](evidence/autonomous-20261023/retained-premature-yield.json):
3,958 input/182 output tokens, no rejection or tool dispatch, identical native
restart and eight-store integrity.0.10.5 clarified generic access without naming
a resource or operation; the current failed acquisition outcome remains visible.

Evidence: [first retained output](evidence/autonomous-20261023/attempt1-retained-output.json),
[retained repeat](evidence/autonomous-20261023/retained-repeat-native-audit.json),
[pre-transport checkpoint](evidence/autonomous-20261023/fixed-native-audit.json),
[serialization failure](evidence/autonomous-20261023/retained-serialization-failure.json)
and [first dispatch regression failure](evidence/autonomous-20261023/dispatch-regression-first-failure.json).
Original raw state remains separate from the corrections.

## Configuration and review scope

Student: Qwen/Qwen3-VL-8B-Instruct, revision
0c351dd01ed87e9c1b53cbc748cba10e6187ff3b, fixed weights, vLLM0.21.0,
Transformers4.57.6, temperature0, seed17, T4x2, FP16/TP2,16,384 context.
Serving and numerical environments remain separate. Exact package freezes,
model-file hashes and hardware inventory accompany each raw checkpoint.
The student has no benchmark evaluator or Meadows solution files.

The authored neutral world has three separately accessible documents and one
requested interview. It contains no measured future sample or independent
experiment. Limits remain24 turns,393,216 policy units, one-hour controller
deadline,64 public requests and one correction per job; input/output job caps
remain12,288/4,096. Teacher review is optional and model-selected, with manual
current-assistant file exchange and operator-declared identity/unknown usage.
No paid API, parameter training, comparison or scientific result is introduced.

All28 owner pairs/56 directed lanes and10 outside-role pairs/20 lanes retain
their dispositions. The [owner matrix](evidence/autonomous-20261023/OWNER_INTERFACE_REVIEW.json)
and [outside-role matrix](evidence/autonomous-20261023/INTERFACE_REVIEW.json)
record the eleven-facet delta, shared serializer dependency and feedback risks.
The [scoped trace](evidence/autonomous-20261023/TRACEABILITY.json) links existing
CI obligations to the new cases. Review is implementer self-review.
Original broader component/interface obligations remain REVISE. Normal native
reopen does not qualify crash recovery, model-service restart, hard OS isolation,
scientific intelligence, transfer, teacher advantage or superiority.

## Where the databases are saved

The frozen benchmark information database is
[benchmarks/meadows-budworm/database/evidence.sqlite.gz](../../benchmarks/meadows-budworm/database/evidence.sqlite.gz).
Git retains the compressed database; the local runtime uses its decompressed
evidence.sqlite copy.
These investigation runs have separate owner databases; they are not the
benchmark information corpus.

The verified12-turn raw checkpoint and all eight owner databases are on the
operator laptop under:

```text
C:\Users\csscs\Documents\Codex\2026-10-22\edi-free-setup\autonomous-final-evidence-20261023\edi-autonomous-fixed-20261023\
  edi-native-state.zip
  extracted\owners.sqlite3
  extracted\owners.world.sqlite3
  extracted\owners.interpret.sqlite3
  extracted\owners.reason.sqlite3
  extracted\owners.analyze.sqlite3
  extracted\owners.assess.sqlite3
  extracted\owners.agency.sqlite3
  extracted\owners.workflows.sqlite3
```

Its archive SHA-256 is
1b537e8f8c93b4ac471ea4a1a6d3625c98807c46be795f72a63278f4df2dddbd.
Notebooks, SQLite files, archives, weights and operational exchanges stay outside
Git; curated synthetic evidence and verification hashes are retained here.
The [recovery CLI](../../examples/autonomous/recover_checkpoint.py) verifies exact
snapshot hashes, ZIP CRC and safe extraction without executing the notebook.
Use --checkpoint-sha256 when a notebook retains several snapshots for one run.


The final0.10.5 raw checkpoint is saved separately on the operator laptop:

```text
C:\Users\csscs\Documents\Codex\2026-10-22\edi-free-setup\autonomous-access-contract-evidence-20261023\edi-autonomous-access-contract-20261023\
  edi-native-state.zip
  DOWNLOAD_VERIFIED.json
  NATIVE_AUDIT.json
  extracted\owners*.sqlite3
```

The exact final archive and notebook SHA-256 values are in build-verification.json.
All eight individual database names are the same as in the preceding listing.
The complete notebook is retained outside Git with both final snapshots and
shutdown evidence. Transport verification was followed by separate local
read-only SQLite checks and source/wheel byte comparison.

[Scoped component gate](evidence/autonomous-20261023/COMPONENT_REVIEW.json): integration REVISE. Contract/native regression evidence is scoped and self-reviewed; the original broader matrices remain REVISE.
