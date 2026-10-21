# Free model feasibility checkpoint

22 October 2026. Existing EDI source remains 0.9.1.dev0. This is an external model feasibility result, not an EDI integration or Meadows benchmark result.

## Actual results

- OpenAI: a real GPT-6.1 Sol request completed through documented Sign in with ChatGPT plan usage on the owner's existing Plus account. Usage: 16 input, 6 output, 22 total tokens. No API key or paid fallback was used. This verifies availability for this account at this time; it is not unlimited access.
- Student: Qwen/Qwen3-VL-8B-Instruct revision 0c351dd01ed87e9c1b53cbc748cba10e6187ff3b completed two real authenticated loopback HTTP requests through vLLM on Kaggle's GPU T4 x2 allocation.
- Arithmetic answer: 2. Image answer: Left: Red square / Right: Blue circle. Usage was 24 total tokens for text and 67 for image.
- Profile: FP16, tensor parallelism 2, context 4096, one image capped at 65536 pixels, maximum 32 output tokens per request, temperature 0 and seed 17. This is a small diagnostic, not qualification of the proposed 16384-token/two-image benchmark profile.
- Installed model environment: Python 3.13.15, vLLM 0.21.0, PyTorch 2.11.0+cu130 and Transformers 4.57.6. GPU driver: 580.178.04. Each T4 reported 15360 MiB. Full package and checkpoint-file hashes are retained in the evidence.
- The probe stopped its server after the requests; a subsequent GPU snapshot reported 0 MiB allocated on both GPUs. The Kaggle draft session was then stopped after evidence export; the editor confirmed Session stopped and Draft Session off. No student weight training, EDI investigation, Cedar submission or comparative benchmark occurred.

## Preserved failures and limits

The initial environment creation with ensurepip failed; installation through system pip's --python option into the separate environment succeeded. The first model startup failed during FlashInfer sampler JIT/Ninja compilation. The same revision and FP16 layout passed after setting VLLM_USE_FLASHINFER_SAMPLER=0. The reusable example uses this native sampler configuration from the start and does not fabricate another failed attempt.

Kaggle's Python sitecustomize emitted a missing-wrapt warning; imports and both requests nevertheless completed. vLLM shutdown emitted shared-memory resource-tracker warnings. These are retained in the original logs and do not establish production lifecycle/recovery qualification.

Kaggle's editor showed a failed draft-save condition during the run. All 14 exported files were independently transferred to the owner's desktop and their SHA-256 hashes verified. The reusable notebook here is generated from saved source; it is not represented as a byte-identical download of the failed-save draft. Raw logs remain in the desktop evidence directory recorded in EXPORT_MANIFEST.json; selected exact JSON reports, package pins and raw-log hashes are included in Git. No credentials, browser sessions or model weights are included.

## Reuse

Import [the feasibility notebook](../../examples/free-compute/edi-free-vllm-feasibility.ipynb) into a private Kaggle notebook, select the free GPU T4 x2 allocation, enable internet for setup and run the cells in order. The launch cell starts one background probe. Repeat only the monitor cell while it runs. The probe freezes the revision above, verifies downloaded file hashes, uses offline artifact loading for its loopback server, sends the two neutral requests and stops that server. Preserve /kaggle/working reports before ending the VM. The environment and checkpoint cache are temporary; this is session-based compute subject to account quota, not permanent hosting.

The first recorded notebook is https://www.kaggle.com/code/vigini/notebook0dfd4a0f88/edit. The source and evidence in this repository are the durable checkpoint.

OpenAI plan sign-in and encrypted credentials stay on the owner's Windows machine, outside this repository and outside Kaggle. The credential is not a conventional API key. A production EDI adapter still needs the documented streaming request/refresh/limit contract and restricted teacher connection; the existing API-key backend has not been converted by this diagnostic.

## Remaining EDI work

The model feasibility result removes the need to assume a paid GPU rental or a separately funded OpenAI API key for these basic checks. It does not bind the live EDI deployment. Native C4 token/processor admission, the full input/image budget, C6 constructed-world eligibility, neutral P1 eight-owner execution, deployment isolation, teacher egress/retention and whole-application recovery remain open. The first saved Cedar pilot is student-only. The full benchmark has not started.

## Evidence

[Evidence folder](evidence/free-compute-20261022/) contains the actual request responses, checkpoint hash manifest, package pins, first failed-start report, final successful profile and OpenAI plan-access summary. EXPORT_MANIFEST.json distinguishes files included in Git from the 14 original local exports. These are engineering availability/perception checks only; they do not establish autonomous discovery, scientific validity or an advantage of EDI over an LLM.
