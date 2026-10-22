# Controlled engineering integration walkthrough

`complete_run.py` exercises existing C0–C7 owner contracts through the configured
`IntegratedApplication`. The schedule, initial model, comparison target and C6
review are authored. Student responses come from the real configured Qwen server;
teacher critique is imported explicitly from the current assistant session after
exporting the actual original cut. This is not an autonomous discovery result or
a Meadows benchmark result.

Use a fresh private run directory. Preserve the emitted protocol and exact source
manifest before observations. `initial` runs intake/interpretation/model admission
and student inference, then exports a teacher request and waits. Export and verify
that checkpoint before importing feedback. `finish` imports the critique, requests
a real student revision, and performs numerical, assessment, authority and delivery
handoffs. `restart` opens the eight owner stores in a new process, replays completed
workflows without redispatch and checks retained outputs and SQLite integrity.

The server supervisor keeps ephemeral credentials in memory/environment, exposes
vLLM and the neutral broker only on loopback, and accepts explicit local command
files. No paid API, public tunnel, model training, forest resources or evaluator
is used. Serving and numerical environments are separate: vLLM 0.21.0's Numba
dependency requires NumPy below 2.5, while C5 pins NumPy 2.5.3 / SciPy 1.17.0.

The measured outcome is a controlled 32-byte file, held constant across a future
nominal epoch and bracketed by actual OS stat reads. Actual acquisition times,
metadata and jitter are retained. Distinct source IDs do not establish scientific
independence. The authored 8+4t forecast intentionally differs from this fixture;
the resulting error exercises assessment and candidate retention, not diagnosis.
Normal process restart is not crash/fault-injection qualification.

Consult the dated implementation evidence report for actual outcomes. Presence of
these scripts alone is not a successful run. Optional student candidates are
submitted only if genuinely returned; authored C6 candidates are labeled separately.

Prepare a standalone fresh-session cell without executing a model:

```text
python examples/engineering/prepare_kaggle_run.py --output PATH_OUTSIDE_REPO.py
```

Use the generated cell in the authorized private Kaggle notebook with T4 ×2 and
internet access. It creates the owned temporary parent, installs separate pinned
environments, verifies the source bundle and keeps the notebook busy until the
initial checkpoint or a retained failure. Export and verify the checkpoint.
Review the newly exported teacher request; place its critique content in
`/kaggle/working/edi-engineering-20261022/teacher-feedback.json`, then create a
`command-finish-1.json` file there containing `{"stage":"finish","attempt":1}`.
The supervisor imports feedback through the native gateway and runs `finish`.

After that phase, run `complete_run.py restart` in the compute environment with
`PYTHONPATH=/kaggle/temp/edi-engineering-source/src`. No serving credentials are
needed for restart. Inspect native results and export consistent SQLite backups
before creating `command-stop.json` containing `{"stage":"stop"}`. Stop the owned
Kaggle session after hash/CRC verification. The supervisor has a finite 90-minute
command window; this is not an unattended hosting service or cross-session
reconnection guarantee. Failed native workspaces require explicit continuation.

The current completed execution, original failures, partial teacher uptake and
scope are documented in [ENGINEERING_RUN.md](../../docs/implementation/ENGINEERING_RUN.md).
