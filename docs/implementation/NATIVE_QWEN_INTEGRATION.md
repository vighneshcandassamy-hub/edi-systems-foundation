# Native Qwen integration checkpoint

22 October 2026. Development **0.9.2.dev0**, C4 implementation **edi-c4/0.5.2**, based on c6c5791301a3a9c9de1d2b28ed90d2958c74bf27.

**Source integration and 27 CPU regression checks are complete. Final-source live integration remains unverified.** Earlier native text/image calls were observed to complete; two autonomous controller trials failed. A third was launched, but Kaggle expired before its result and raw records were exported. This is not a completed autonomous test or forest benchmark.

## What changed

The loopback vLLM backend uses an ephemeral bearer header, exact server-side /tokenize admission, an explicit context window and actual prompt-usage reconciliation. Credentials are excluded from model context, C1 profiles and journals. NativeGateway records the original returned wire in C1 before content/usage validation. Count mismatch or unknown completion stays unresolved and does not silently cause another inference.

C4 now renders the selected native protocol questions that were previously omitted. Seven operation-specific argument shapes constrain generated JSON and are validated again by native code. For example, acquire-asset takes exactly a document_id; world-call takes a public operation and its body. This describes the API, without choosing an investigation sequence, source, hypothesis or solution. The model still chooses operations; C0/C7 retain dispatch and authority. The transport supplies identities, attribution and measured usage, and rejects conflicts.

A separate C0 resume defect could turn a completed task into yielded when completion occurred on the final allowed turn. The fix preserves durable terminal state. Its original failing test is retained.

The stricter validator requires fresh workspaces. Old malformed responses cannot be read through the new validated contract; original source snapshots are retained for reconstructing their reader. No ledger migration, repair or whole-application recovery is claimed.

## What was observed, and what remains available

[Observed checkpoint](evidence/native-qwen-20261022/OBSERVED_CHECKPOINT.json) explicitly separates terminal observations from retained primary evidence.

| Trial | Observed outcome | Input / output tokens |
| --- | --- | --- |
| Native numeric and image | Two native imports completed; completed calls reopened without new inference | 18,571 / 1,099 |
| Neutral C0 trial 1 | Failed: asset arguments had an extra operation/body wrapper | 26,731 / 1,913 |
| Neutral C0 trial 2 | Failed: world-call appeared where a public operation name was required | 8,536 / 694 |
| Neutral C0 trial 3 | Launched after strict grammar and terminal-state fixes; outcome unknown | Unknown |

The first diagnostic used authored CSV and a generated red-square/blue-circle image through C1/C2/C3/C4. Actual prompt counts matched preflight in the displayed results. The model supplied zero formal hypotheses and zero proposed C3 candidates. Semantic answer quality was not independently inspected. Those calls used earlier source, not the final operation grammar.

All neutral C0 trials shared the same mission, one instrument CSV and fixed four-turn/65,536-token/600-second limits. The model chose operations against a loopback fixture through C0/C7. Fixture corrections added native asset range/hash behavior; they did not change the mission or data. Its broker deduplication is in memory and does not qualify world restart recovery. C5/C6 and the teacher were not exercised.

Kaggle expired before export. Recovery showed only .virtual_documents in /kaggle/working, with no old result files, source or venv. Raw JSON, owner SQLite stores and server logs were lost. The observed numbers above are retained as a candid session account, **not replayable qualification evidence**. The third trial is not counted as success or failure. No subsequent inference was launched during recovery, and the replacement draft session was stopped.

## Configuration and limits

The attempted profile was Qwen/Qwen3-VL-8B-Instruct revision 0c351dd01ed87e9c1b53cbc748cba10e6187ff3b, vLLM 0.21.0, Transformers 4.57.6, two free Kaggle Tesla T4 GPUs, FP16/TP2, 16,384 context tokens and one image of at most 65,536 pixels. Numeric/image jobs reserved 12,288 input and 2,048 output tokens. The neutral loop reserved up to 4,096 output tokens. FlashInfer sampling was disabled after the earlier feasibility failure.

Native prompts consumed roughly 8–10K tokens in the displayed attempts. The previous 4K feasibility profile cannot serve these full requests. A 16K configuration does not establish performance at every boundary or qualify the forest's full image/resource profile. Total tokens including trial 3, complete elapsed/setup cost and energy remain unknown. No added paid service was used. No weight training occurred.

Only EDI source and authored neutral fixtures were transferred. Forest/evaluator material and account credentials were not included. Shared Kaggle user/process resources do not provide the hard isolation required by the forest plan.

## Retained checks and next gate

[CPU evidence](evidence/native-qwen-20261022/cpu-tests.json) pins the final source and tests. All **27 checks pass** on Windows Python 3.12 / Pydantic 2.12.5. They cover the existing 19 connection cases plus authentication, exact counting, context drift, usage mismatch/no duplicate inference, protocol rendering, role/window refusal, operation argument shapes/grammar and final-turn completion. Authored model transports do not qualify real inference. Initial 24-test evidence and the terminal-state first failure are preserved separately.

The generated [Kaggle notebook](../../examples/free-compute/edi-native-integration.ipynb) bundles final source without recorded outputs or credentials. It is a reproducible input, not an export of the lost session. The immediate next gate is to rerun the final-source numeric/image diagnostic, export and independently hash-verify its reports and raw state **before starting another trial**, then do the same for the neutral C0 investigation. Expired-session history cannot be reconstructed from source manifests alone.

C5/C6 feedback, full P1, hard isolation, the ChatGPT-plan teacher adapter, forest investigation and matched comparison remain open. Teacher plan availability from the separate feasibility check does not connect that account to EDI. Overall contract/integration readiness is **REVISE**, with live verification blocked by missing evidence.

## Review and sources

The EDI component-review and interface-review skills were applied as self-review, not independent review. Existing 28 owner pairs/56 lanes and 10 outer pairs/20 lanes retain their authority dispositions. The neutral instrument substitutes a diagnostic public WORLD endpoint; no direct model-to-world route is granted. Structural helper success establishes catalogue consistency only.

Version-specific primary references: vLLM [tokenization implementation](https://docs.vllm.ai/en/v0.21.0/api/vllm/entrypoints/serve/tokenize/serving/) and [structured outputs](https://docs.vllm.ai/en/v0.21.0/features/structured_outputs/). Live acceptance of the final strict grammar remains unverified.
