Teacher exchange persistence: use `teacher_handoff.show_handoff(out, source)`
at each pause, and `import_feedback(out, source, exact_job_id, feedback)` for
operator feedback. Each import waits at most 180 seconds for a native pause and
embeds the ZIP checkpoint in saved notebook output. Download that notebook;
`recover_checkpoint.py` verifies the recorded digest before extraction. An
expired VM or authority grant is not automatically resumable. A timeout does
not establish cross-owner quiescence and must not trigger blind replay.

Current source: **0.10.9.dev0**, C0 integrated-1.5. Intensive prompts keep raw
observations and bounded provisional lessons; full generated artifacts remain
available through explicit native context selection. The successor engineering
profile uses a 20,480 model window, 16,384 input cap, 4,096 output allowance and
786,432 total policy units. A fresh workspace is required. The first actual 0.10.8
teaching cycle and its later prompt-cap failure are preserved in the
[context repair](../../docs/implementation/INTENSIVE_CONTEXT_REPAIR.md).

The following launch and historical descriptions retain their original scope.

Intensive mode (0.10.8.dev0): add `--teaching-mode intensive` when building a
fresh launch cell. The teacher first assesses the same cut independently, then
critiques the student draft; the student revises before execution. Two teacher
file exchanges per normal turn are expected. Unknown usage is fully reserved.
The extra teaching preflight must pass before model startup. No live result is
implied. See [teaching protocol](../../docs/implementation/INTENSIVE_TEACHING.md).

Current source is 0.10.7.dev0. New runs require a fresh workspace and typed
information-seeking/stopping decisions. The launch package runs the additional
information-seeking regression and actual xgrammar preflight before model startup.
No new live result is implied. Use --source-revision VERIFIED_FULL_SHA when local
Git metadata is unavailable; per-file content hashes remain authoritative.

# Autonomous controller engineering run

This runner calls the existing `IntegratedApplication.step()` entry point. It
supplies the original objective and access catalogue through a neutral broker.
Qwen chooses subsequent operations. There is no scheduled component sequence,
pre-admitted analysis model, suggested hypothesis or forced teacher turn.

The authored world contains a raw register, capture notebook, unrelated service
bulletin and an interview available only through a request. It does not contain
an empirical experiment or a measured next sample. This is an engineering check
of information seeking, uncertainty handling and durable continuation.

Prepare the standalone cell outside the repository:

```text
python examples/autonomous/prepare_kaggle_run.py --output PATH_OUTSIDE_REPO.py
```

Use the authorized private Kaggle notebook with free T4 x2. The cell bundles only
all69 engine files, five run/checkpoint/reopen scripts and two native regression scripts, installs the already used separate
serving/numerical environments, verifies source hashes and starts the pinned
Qwen model. It does not include the Meadows package or evaluator files.

`server.py` exposes vLLM and the authored broker on loopback. Credentials exist
only in memory and child environments. `run.py turn` advances one actual native
controller turn in a fresh process; prior native state is compared before the
next turn. The process supervisor schedules continuation, not operation choice.
Every returned turn and all native stores remain available for export.

If the student selects teacher-review, export and verify the checkpoint before
reviewing its exact exported request. Place critique content in the owned run
folder as `teacher-feedback.json`, then create a unique `command-*.json` containing
`{"stage":"import-teacher"}`. Teacher identity is operator-declared and usage is
unknown unless supplied; there is no paid teacher API. Critique must respect the
original cut. Do not add evidence or tell the student which resource to request.

A terminal result triggers a separate `run.py restart` process. It checks native
snapshot equivalence, unchanged inference/broker counters and all eight SQLite
integrity checks. This is normal restart, not crash or unknown-provider recovery.
After consistent SQLite backup/export and hash verification, create a unique
command file containing `{"stage":"stop"}`, then stop the Kaggle session.

The supervisor has a finite 90-minute lifetime; the controller separately retains
24-turn, 393,216 policy-token and one-hour ceilings. These are engineering resource
limits, not a scientific benchmark budget or autonomous hosting guarantee.
The predeclared acceptance criteria are in
[protocol.json](../../docs/implementation/evidence/autonomous-20261023/protocol.json).
Presence of these files does not establish that the run passed.

The current packager accepts --run-directory to select a fresh owned directory. Its finally block emits a consistent native checkpoint automatically, including rejection/restart failure. The ZIP is embedded in notebook HTML output; Download Notebook preserves the payload for offline recovery. Download and verify it promptly. Original snapshots and failures must remain separate. Detailed restart differences and database integrity results are retained before an equality assertion.


The retained source0.10.5 ran both native regressions before model startup. The
controller contract check includes actual xgrammar compilation and preserves
proposal-only/teacher semantics. The authored dispatch check reaches the real
broker and C2, closure, reopen and unknown-completion guard. Its fixed operation
sequence is only a regression fixture and is never supplied to the live student.

Complete citation addresses and a controller decision are native requirements.
The schema-aware gateway keeps a field index in the prompt while retaining the
full structured decoder and native admission. Information access is authorized
by the catalogue/grant; a request does not require already knowing the missing
measurements. No domain-specific investigation order is encoded.

Recover a particular saved snapshot without executing the notebook:

```text
python examples/autonomous/recover_checkpoint.py --notebook PRIVATE.ipynb --output PRIVATE_OUTPUT --checkpoint-sha256 EXACT_SNAPSHOT_DIGEST
```

Keep distinct snapshots in distinct private output folders. Verify native source,
SQLite integrity and controller status separately from transport/CRC success.
For an operator-stopped case, offline_restart.py can reopen native controller
state with dispatch-forbidden ports against an explicitly saved restart baseline.
That checks native reopen only; it does not restart model/broker services or
qualify crash recovery. Never fabricate an endogenous yield after an operator stop.
