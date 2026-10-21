# Benchmark connection execution checkpoint

21 October 2026. Development increment: **0.9.1.dev0**, C4 operation-proposal contract increment **0.5.1**. Source baseline: EDI 0.9.0 at `879452b8332a318ca76af4f84589b676b031f253`. Benchmark/planning baseline: `27c437bbc54310dff0603d46f5dd3516d5e00730`. The owner has now explicitly authorized implementation and execution, superseding the historical defer-testing instruction. The original branch, historical evidence and frozen benchmark are preserved.

## Implemented source increment

| Owner | Connection | Scope |
| --- | --- | --- |
| C0 | `inquiry/benchmark.py` | Durable generic turn intents, C4-selected public requests, selected context, C2 decoding, candidate submission, optional C5 requests and selective teacher handoff. No prescribed forest investigation. |
| C0/shared | `shared/durable_io.py` | Namespaced tables within initialized owner stores; bounded prepaid call journals, immutable identities and atomic first-dispatch claim. No transaction around external calls. |
| C1 | `observe/benchmark.py` | Real authenticated HTTP broker, exact raw response recording, HTTP errors as evidence, paging/chunk identity, bounded native-asset reassembly and SHA-256 verification. |
| C4 | `reason/gateway.py` | Pinned job/context validation, exact token-counter requirement, actual acquired PNG/JPEG parts, raw model output capture, usage and unresolved-call handling. Local vLLM transport and GPT-6.1 Sol Responses API critic transport. |
| C4 | `Response.operation_proposals` | At most one typed data-only next-operation proposal. Teacher proposals/actions are rejected. C0 validates arguments through the existing native ports and C7 authority. |
| C7 | `agency/benchmark.py` and factory | Explicit trusted-operator standing simulated-session grant, exact endpoint/token/workspace/session binding, expiry and finite request count. Existing research-readonly policy remains unchanged; no model self-adoption. |

Original C0–C7 paths remain authoritative for evidence, representations, analysis and assessments. A new generic operation proposal is an integration contract extension. Old response fixtures omit it and remain valid; new schema consumers must pin the changed schema/implementation. C4 episode implementation identity changes to 0.5.1; use fresh workspaces. No migration of earlier 0.5.0 episodes is claimed. The default finite C4 cuts and exact token admission can reject large inputs; this is an explicit bound, not successful understanding. Recency/byte allocation is only a default presentation policy; selected context remains replaceable by EDI.

## Actual engineering evidence

`tests/test_benchmark_connection.py` exercises the real pinned world broker and native C1/C2/C3/C4/C7 source where indicated. Model transports in these CPU tests are authored wire fixtures, with explicit attribution and no claim that a real model ran. The image case checks exact image bytes in the message; it does not measure vision. The dynamic two-turn case checks C0→C4→C0 dispatch and retained evidence; it does not measure autonomous problem solving.

The initial run had three consequential failures: extension tables initialized before the native C4 database made the native schema guard reject it; gateway retries accidentally rendered later response history, changing the original fingerprint; and a cost assertion incorrectly expected a future measurement to be charged before advancement. Fixes initialize native owners first, freeze the job's earlier-response cut and preserve the world's actual delayed-charge semantics. Original failures are retained in the execution evidence. Acceptance is not weakened to claim a live model result.

The first Windows campaign also recorded twelve cleanup errors: the preserved broker relies on SQLite handle finalization and Windows refuses deleting open run files. The engineering test teardown now joins non-daemon HTTP workers and explicitly collects unreachable handles before deleting its disposable directory. It does not suppress cleanup errors or modify the frozen broker. This is a test-lifecycle repair, not a production handle-management qualification. A further regression check verifies that a bounded native image larger than the text-cut allowance remains whole rather than silently losing its image view.

The original text-only foundation validator also rejected the combined tree's legitimate binary benchmark assets and local virtual environment. `scripts/verify_baseline.py` now excludes only explicit local-environment/work directories and approves benchmark binary bytes only after checking the exact frozen package manifest/verifier hashes and running all package checks. Restored aliases must match their original source hashes. Text credential scanning and disallowed weight/key payload checks remain. A negative control confirms an unlisted binary is still rejected. The frozen v0.2.1 verifier itself uses OS-dependent `str(relative_path)` inventory identifiers; on Windows the combined validator supplies a Path view with POSIX presentation, leaving the verifier and dataset bytes unchanged. Use the combined validator there. Both the initial failure and passing/negative-control evidence are retained.

Run in a fresh disposable environment:

```sh
python -m venv .venv
.venv/bin/python -m pip install pydantic==2.12.5
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
PYTHONPATH=src .venv/bin/python -m edi.inquiry.benchmark_preflight --output work/host-preflight.json
```

On Windows use Python 3.12 and `.venv-benchmark\Scripts\python.exe`; set `PYTHONPATH=src`. Preflight returns code 2 when live prerequisites are absent. It never prints credential values. Record actual source/test hashes and preserve failures. No credentials, local SQLite databases or weights belong in Git.

## Live execution remains blocked

The connected Windows host has RTX 2060 6144 MiB VRAM, about 15.4 GiB RAM, Python 3.12 available, no Docker command and no installed WSL distribution. No OpenAI API key was present in the checked process environment. The cloud scratch environment also lacks GPU, Docker and vLLM. These observations are not a claim that no compatible host exists elsewhere.

The full-precision Qwen3-VL-8B-Instruct/vLLM profile has not been loaded, downgraded, quantized or replaced. Exact checkpoint/tokenizer/processor/container pins, a real token counter and real neutral inference remain required. A six-GB GPU is below the plan's provisional 48-GB preparation allowance. No OS distribution, Docker installation, model download, paid GPU or paid inference was started to bypass this condition.

The saved first diagnostic pilot is student-only. For the subsequently discussed teacher-assisted configuration, the teacher transport is GPT-6.1 Sol (`gpt-6.1-sol`), selective critique only, with the same evidence cut and no tools/extra world access. It is source implemented but not connected or tested against the live API. It changes context/representations, not Qwen weights. Credentials, exact provider settings, tokenizer/count admission and total-cost accounting must be bound before execution.

An offline `--network none` pod cannot call the remote teacher directly. The teacher-assisted deployment therefore additionally needs a narrowly scoped outbound gateway (for example a Unix-socket proxy outside the offline pod, with credentials confined to that gateway), its own reviewed isolation/retention contract and actual negative probes. This network boundary is **not implemented or qualified** in this increment. Do not broaden the model container's egress or reuse this chat as an unlogged teacher. The first student-only image-inclusive pilot still requires the three-container isolation tests.

C6's empirical forecast guard is not bypassed. C4 predictions remain original, unscored expectations of a constructed world. Exact constructed-clock/measurement eligibility, P1 full eight-owner demonstration, whole-application restore and live image/model/teacher/isolated-container cases remain open. Existing code and engineering checks do not establish those capabilities.

## Next execution prerequisites

1. An authorized compatible Linux GPU/container host, with frozen model artifacts and actual neutral token/image/inference fit verification.
2. A securely configured GPT-6.1 Sol credential and restricted teacher gateway if enabling that arm.
3. Concrete C6 constructed-world correspondence (or explicitly scoped unscored diagnostic), complete neutral P1 evidence, isolated deployment checks and full resource accounting.
4. Then freeze a new run manifest and start the original unguided Cedar case with empty case memory. Preserve incomplete/failed runs; perform private offline outcome review only after closure.

Contract self-review remains REVISE; live runtime/integration/scientific qualification is BLOCKED/NOT RUN. Only scoped CPU engineering claims supported by actual reports may be marked passed.


## Subsequent free-compute feasibility — 22 October 2026

[The free-compute checkpoint](FREE_COMPUTE_SETUP.md) supersedes the earlier assumption that paid GPU access and a separately funded API key are necessary for a neutral model check. Actual Qwen text/image inference on free Kaggle T4 x2 and GPT-6.1 Sol access through the owner's Plus plan succeeded. The scoped 4096-token student profile and plan-access probe are not a live EDI benchmark connection; all remaining integration, full-budget, isolation and scientific gates above retain their stated status.
