# CUDA launch dependency correction, 28 October2026

Self-review addendum to QWEN_LOCAL_INTERFACE_REVIEW_20261028.json. Existing8 components,56 directed lanes and participant contracts are unchanged. External dependency inventory gains a compiler-only search directory linking the actual loaded NVIDIA driver. No additional driver install, model, data or evaluator authority is introduced.

- ownership: Kaggle owns installed CUDA driver; launch cell owns private per-container symlink and receipt. Entry/server inherit environment only.
- authority: read loaded driver map and driver version; create one private link/probe; no system-directory mutation or source/participant override.
- shape_versions: existing131-file source archive fd9dddda55f6963b1578d757f3e8765a49ab55acb1a15b094c72cca17b695dfe unchanged; actual driver version/hash retained, vLLM0.21.0/model revision/decoding/context remain pinned.
- identity_scope: actual libcuda.so mapping must be unique, existent and outside stubs. Unversioned linker name resolves only to that driver; UUID scopes private directory to fresh container.
- time_order: compilation and real driver API validation precede installs and model startup; native participant admissions remain unchanged.
- delivery_idempotency: failures terminate batch; no retry within run. Historical Versions1-3 remain preserved; source source-directory/single-launch guards unchanged.
- commit_recovery: original source hashes checked; new preflight receipt persists compile status before load and qualification status after driver API check. No failed episode is resumed.
- retention: compiler receipt in working outputs; temporary link only for container lifetime; actual failed runs remain saved Kaggle versions. No credential retained.
- resource_limits: one shared-library compilation60sec; no new model requests or larger benchmark allowances. Same per-arm budgets.
- errors: missing/ambiguous/stub driver, compiler failure, or driver API error stop before expensive setup. Version2 exposed missing ldconfig cache entry; Version3 exposed missing temp parent. Both repaired explicitly, not hidden.
- feedback_grounding: compiler receipts establish deployment linking only. They cannot prove Qwen competence, an ecological outcome or EDI advantage. No case answers enter model input.

Version4 actual preflight reports real driver /usr/local/nvidia/lib64/libcuda.so.580.178.04 and CUDA API version13000, compiler link/load PASS. Remaining serving/schema/vision/runtime and science gates remain pending. Full58 software tests previously passed; original server startup failed missing-lcuda. No independent review or bundled-checker pass claimed (skill checker resource remains unavailable). No GitHub publication claimed.
