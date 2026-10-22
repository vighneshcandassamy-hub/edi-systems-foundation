# Controlled engineering integration run — 22 October 2026

**Result: the scheduled C0–C7 engineering walkthrough completed, including real
student inference, imported teacher critique, student revision, numerical analysis,
assessment, authority checks, internal delivery and normal process restart.**

Implementation: **0.10.1.dev0**, based on source commit
`0935ce5b9e6d1f66fbb6f8f8566afefddcfd05a8`. The executed 69 source files match
the final repository files and built wheel byte for byte; exact hashes are in
[build-verification.json](evidence/engineering-20261022/build-verification.json).
The original 0.10.0 startup failure and subsequent harness failure are retained.

The run uses `IntegratedApplication` to compose the actual owners, scoped broker
connection and model ports. An authored harness schedules native C0 Workflow
handoffs to exercise the existing components. The autonomous `Investigation.step`
controller was not exercised. No Meadows problem-solving result, independent
scientific validation, general learning advantage or complete architecture
qualification follows from this walkthrough.

## What executed

| Component or path | Observed result | Native evidence |
| --- | --- | --- |
| C0 composition | Application starts after the C0/C7 facade repair; neutral loopback broker status is captured | Source repair, workflow outputs and raw archive |
| C1 | Original controlled file readings retained with exact bytes, origin and hash | `input-record.json` |
| C2 → C3 | JSON decoding completed; native derivation candidates submitted | `interpret.json`, `interpret-submit.json` |
| C3 | Authored model admitted explicitly by the local operator; original and corrected version pins retained | `model-admission.json`, `model-pin-repair.json` |
| C4 student | Real Qwen initial response admitted against the original cut | `student-initial-receipt.json` |
| C4 teacher → student | Original cut and actual attempt exported; critique imported and retained; a second real Qwen response admitted | `teacher-interaction.json`, `verified-summary.json` and raw archives |
| C5 | Typed model compiled as supported; numerical run completed | `compile.json`, `numerical-run.json` |
| C6 | Native local-prospective seal confirmed; OS measurement scored; review, candidate submission and finding retained | `forecast.json`, `compare.json`, `native-restart-audit.json` |
| C7 | Explicit policy adoption, authorized internal read and external-action denial completed; actor mask retained | `authorized-read.json`, `external-denial.json`, raw archive |
| C6 → C4 | Native assessment read returned through the existing reasoning port | `c4-assessment-read.json` |
| C0 delivery | Finding delivered to the internal workflow result, with `external_message_sent=false` | `delivery.json` |
| Recovery | Fresh process replay preserved completed outputs, the C4 episode and original failed inquiry; eight databases passed integrity checks | `restart-complete.json`, `native-restart-audit.json` |

Artifacts in this table are under
[evidence/engineering-20261022](evidence/engineering-20261022/verified-summary.json).
Full native owner stores, workflow records, logs and source snapshots are retained
in the separately hashed archives listed in
[archive-inventory.json](evidence/engineering-20261022/archive-inventory.json).

## Repairs and preserved failures

1. **Dependency conflict:** vLLM 0.21.0's Numba dependency requires NumPy below 2.5;
   C5 requires NumPy 2.5.3 / SciPy 1.17.0. Serving and numerical execution now use
   separate Python environments, communicating through loopback HTTP. Both
   installed successfully; package freezes are retained.
2. **Fresh-session setup:** `/kaggle/temp` did not exist. Setup now creates its
   owned parent directory. An earlier free session expired during a pause; its
   native execution state is unknown because no native checkpoint was exported.
   No result from that session is counted. The completed attempt used foreground
   notebook monitoring and immediate exports.
3. **Source defect:** `IntegratedApplication` requested `benchmark_authority` through
   `AgencyAccess`, but only `Agency` implemented it. The C0-only facade now forwards
   that existing operation. It remains outside the model-accessible operation
   catalogue. No model call occurred before this failure. Its complete archive is
   preserved as `failure-c7-facade`.
4. **Harness configuration:** C0 and C7 now explicitly name the same engineering
   operator. The harness originally requested 4,096 evidence bytes from a 459-byte
   payload. C4 correctly rejected that range before inference. The corrected
   inquiry uses the actual manifest length; the failed original workflow remains
   failed and is checked during restart. Its archive is `failure-c4-cut`.
5. **Native version pins:** the authored opaque IR assumed version `1`; the actual
   C3 records were version `2` after prior interpretation submission. Before
   compilation, an explicit operator correction retained the original model and
   pinned the same equation to the native versions. The corrected response record
   is version `3`; stock and flow remain version `2`. Subsequent analysis, review
   and actor reads use actual selected versions. Future fresh harness runs derive
   initial IR pins from the post-patch revision.

Only the C7 facade forwarding and package version changed in the existing engine.
Other corrections concern execution environments and the engineering harness.
The 40 imported foundation artifacts and frozen Meadows package are preserved.
The package tree remains `9f2e070d1df5ff5d5638d0536e4104920b5a9184`.

## Actual teacher–student interaction

The initial student called the observed sequence “deterministic” and described a
test as requiring no additional data. The imported critique challenged both
claims, emphasized authored labels versus elapsed time, source dependence and
the incomplete dependency cut, and requested genuinely discriminating observations.

The real revision changed its headline claim to a finite ordered pattern of
8, 12 and 16 bytes with four-byte increments per authored label. It retained a
distinct hypothesis ID and the original evidence cut. **Uptake was partial:** its
test still claimed that no additional data or tools were required and remained
underspecified. Neither response supplied a C3 candidate or operation proposal.
This demonstrates transport and revision, not reliable test planning, autonomous
information seeking or a measured reasoning advantage.

The teacher was the current ChatGPT assistant, using explicit file exchange.
Identity and usage are operator-declared, and the reviewer knew the engineering
implementation. There was no authenticated paid teacher API, blinded review or
weight update. Teacher usage remains unknown.

## Numerical and assessment result

The harness-authored model is `dB/dt = 4`, with initial state eight bytes and a
five-second horizon. C5 predicted **28 bytes**. The separate OS stat acquisition
reported **32 bytes**. C6 scored absolute error **4**, squared error **16**, and
`within_declared_limit=false`, then retained an attributed review candidate without
admitting it as truth or an operational policy.

The native seal was acknowledged at `18:14:54.176255 UTC`; the registered target
was `18:15:22.863216 UTC`, approximately 28.687 seconds later. The actual read was
0.250195 seconds after the nominal epoch. The file's size and modification time
were unchanged across the recorded brackets. That constant-window mapping is an
explicit assumption, not an exact acquisition timestamp or external clock proof.

The harness deliberately created and knew the 32-byte fixture before sealing.
This exercises prospective registration, measurement selection, scoring and
candidate retention. It does not establish blind forecasting or scientific
independence. Separate origin IDs do not remove the common host and harness.

## Resources, persistence and scope

| Measure | Completed attempt |
| --- | --- |
| Student | Qwen/Qwen3-VL-8B-Instruct, fixed revision `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` |
| Serving | vLLM 0.21.0, Transformers 4.57.6; two free Kaggle T4 GPUs; loopback only |
| Initial student usage | 9,481 input / 742 output tokens |
| Revised student usage | 11,115 input / 981 output tokens |
| Known student total | 20,596 input / 1,723 output tokens |
| Teacher | One explicit import; actual usage unknown |
| Accounting policy total | 38,703 token units, including the teacher's full 16,384-unit reservation; this is not measured total teacher usage |
| Additional paid inference | $0; no paid fallback |
| Energy / comparative efficiency | Not measured |
| Restart | Zero new model calls; retained native artifacts verified |
| Final archive | 472,735 bytes; SHA-256 `f9542a975fea6090fc4aa37839eedce98bafc5f6a252f1390188020d86cab2d4` |

The earlier expired session's compute and any native calls remain unknown.
Normal restart was tested inside Kaggle. Exported SQLite copies were independently
opened and integrity-checked on Windows; cross-host runtime resume, crash recovery,
hard isolation, broad modality coverage and the original conceptual acceptance
suite remain unqualified. The model server and Kaggle session were stopped after
verified export.

The eight exported engineering databases are available on the authorized desktop:

```text
C:\Users\csscs\Documents\Codex\2026-10-22\edi-free-setup\engineering-evidence-20261022\final\extracted\
```

`owners.sqlite3` holds observations; the `.interpret`, `.world`, `.reason`,
`.analyze`, `.assess`, `.agency` and `.workflows` SQLite files hold their respective
owner state. These are finite engineering-run stores. Raw archives, credentials and operational teacher exchanges
are excluded from Git; reviewed synthetic evidence and reproducible source are saved.

The documentation checker also incorrectly rejected valid directory links by
requiring every Markdown target to be a file. It now checks target existence;
missing paths still fail. The original failed check is retained alongside the
passing release checks. This change does not alter engine execution.

The self-review distinguishes this runtime pass from the broader original
contract reviews, which remain REVISE. The next development question is how the
autonomous controller selects and executes information-seeking work in the
controlled world, including the observed weaknesses in test planning.
