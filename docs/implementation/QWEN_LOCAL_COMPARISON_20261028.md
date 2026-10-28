# Local Qwen paired Cedar runner - runtime qualification pending
28 October 2026

The owner authorized Qwen alone versus the same Qwen connected to the real EDI runtime, executing on Kaggle. No paid provider, model API credential, billing change, training or model-weight update is part of this implementation.

## Implemented source

- local_qwen_adapter.py: explicit loopback transport, fixed Qwen3-VL-8B-Instruct revision0c351dd01ed87e9c1b53cbc748cba10e6187ff3b, temperature0/seed17, image hash checks, server-side token counts, constrained native/ordinary proposals, durable raw outputs/usage/timings and no retries after uncertain dispatch.
- qwen_run.py: launch evidence checks, separately initialized matched worlds, count BOTH first requests before either generation, alternating serial arms, genuine native EDI proposal imports, private evaluation after both terminal, participant reports and official outcome vector.
- qwen_kaggle_entry.py / qwen_fetch_snapshot.py / qwen_worker.py: fixed two-T4 configuration, pinned serving/compute environments, weight/tokenizer hashes, boundary tests, two domain-neutral real model smoke calls, one fresh actual pair, bounded cleanup and retained failure records.
- test_local_qwen_adapter.py:19 new boundary test definitions. Existing39 boundary/mocked-provider/report tests are also scheduled on Kaggle.
- reason/reasoner_exchange.py: optional count-only initialization port; prospective measured tokens retained separately from128-token conservative identity headroom. Actual pending requests are counted again before generation.
- cedar_pair.py: optional initialization binding for that count port before the first native step. Existing callers default to their prior unmeasured path.

The EDI reasoning role retains a legacy internal student field name. There is one Qwen reasoner and teacher disabled; no student/teacher reasoning or training is introduced.

## Scope and status

Source AST parsing passes for the changed Python files. This only checks syntax. No unit tests, schema/vision/tokenizer qualification, server start, weight download, Qwen inference, Cedar episode or private evaluation has executed for this new source.

The prior58 planned test definitions are not58 passed tests. Earlier39 passes belong to the previous qualified source; the new counter port requires fresh qualification. This source is not ready-for-benchmark evidence.

Current blocker: browser tools expose navigation/read only. CUA/repl click/edit/execute control is unavailable; the connected desktop-control device was offline. The workspace connection also briefly disconnected and later returned. User authorization is sufficient. No alternative execution route is authorized or used.

## Fairness and evidence controls

Both arms use identical weight/tokenizer files, decoding configuration, input/output caps, generation-call reservations and public operation access. Ordinary baseline notes/history are retained. The EDI arm uses the actual native observation/interpretation/reasoning/agency/workflow path; directory/status-only static artifacts are not substituted.

Previous Cedar solutions, participant reports, successful action sequences and private evaluator output are excluded from model requests. Generic identifier/schema engineering guidance is shared. No task-specific fine-tuning occurs. Case familiarity from model pretraining cannot be ruled out.

A single fixed server accepts stateless current-arm messages; prefix caching is disabled. It does not offer model-directed filesystem/code tools. The trusted operator can inspect both worlds for initial parity and final evaluation; this is not independently certified hostile-host isolation.

Native serving schema is reused from the existing EDI implementation. Full native validation is unchanged. The baseline has ordinary public operations and notes/history operations. Extra EDI framework overhead remains part of the measured treatment.

## Finite bounds

Each arm:64 decisions,128 model exchanges including corrections,12288 input/4096 output tokens,2097152 reserved policy tokens,256 public calls and six-hour admission horizon. Native preview adds128 declared headroom tokens to its measured prospective count; actual packet tokenization must still fit before generation. No silent truncation or cap extension.

The entry bounds installs, downloads and serving startup separately, caps the actual child process and terminates the local server in finally. HTTP generation has a finite900-second timeout. A pending call can reach the end of its admission horizon; late native responses remain subject to native rejection. This is not an exact GPU-quota guarantee. Kaggle quota/accelerator/internet access has not been verified for a fresh run.

Valid serving usage is retained for failed proposals as well as successful proposals. Unknown usage remains unknown; policy reservations are separate. Transport-plus-validation wall time is not pure GPU compute time. Energy is unmeasured. Two neutral smoke calls are retained separately from the scientific arm ledgers.

On token/schema/transport/budget failure, preserve the actual failure and stop. No automatic second trial, old-run restart, model swap, fallback provider or operator-authored replacement decision.

## Pending acceptance evidence

1. Kaggle source/hash verification and all boundary tests, including the modified native count port.
2. Exact installed versions, actual GPU inventory, weight/tokenizer hashes and local serving receipt.
3. Actual neutral JSON/identity/usage smoke receipts; required image/schema behavior remains subject to the real supplied packets.
4. Both initial actual prompts within caps; later growth can still terminate an arm.
5. Live acquisition of ecological observations by native EDI, retained hypotheses/tests/candidates where actually produced, updates after genuine observations and genuine terminal dispositions.
6. Official vector and verbatim accepted participant reports only after both terminate. Missing reports remain missing. One pair cannot establish general superiority/significance.

## Self-review

See QWEN_LOCAL_INTERFACE_REVIEW_20261028.json. All56 directed lanes among8 logical components are enumerated; active lanes have eleven-facet profiles and planned cases. This is manual source/contract review, not independent review. The skill's checker source could not be retrieved during the environment interruption; no checker pass is claimed. Runtime/integration/scientific gates remain blocked.

Official serving references:
- https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
- https://docs.vllm.ai/en/latest/configuration/env_vars/
- https://github.com/vllm-project/vllm/blob/main/docs/usage/security.md
Loopback binding is intentional: vLLM key authentication does not cover every auxiliary path. No endpoint is exposed beyond127.0.0.1.
