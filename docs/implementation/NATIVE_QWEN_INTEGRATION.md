# Native Qwen integration: retained rerun

22 October 2026. Development **0.9.4.dev0**, native C4 implementation **edi-c4/0.5.2**. Input revision f7f25cde7f5434e71ff2e1677802ef50b50f6591.

**Numeric/image integration passes its scoped live checks. The autonomous investigation failed. Overall integration remains incomplete.** All 28 Windows CPU checks pass. Each of this rerun's four trials was exported and hash-verified before another trial. The Kaggle session is off.

## Actual results

| Trial | Source | Outcome | Input / output tokens |
| --- | --- | --- | --- |
| Initial rerun | 0.9.2.dev0 | Server rejected unsupported propertyNames grammar | Unknown / unknown |
| Serving compatibility repair | 0.9.3.dev0 | Response returned; native owner rejected invalid rival-hypothesis references | 9,541 / 872 |
| Numeric and image diagnostic | 0.9.4.dev0 | Two accepted native imports; exact prompt counts; completed-call reopening without new inference | 19,416 / 1,287 |
| Autonomous C0 instrument trial | Same 0.9.4.dev0 | Native owner rejected a test targeting undeclared hypotheses; no selected operation or final report | 8,728 / 475 |

[Results and export inventory](evidence/native-qwen-rerun-20261022/RESULTS.json), [CPU evidence](evidence/native-qwen-rerun-20261022/cpu-tests.json), [native success](evidence/native-qwen-rerun-20261022/native-success/edi-native-result.json) and [controller failure](evidence/native-qwen-rerun-20261022/controller-failure/edi-native-loop3-result.json) retain distinct outcomes.

The accepted numeric answer describes +4 increments from 8 and limits causal/generalization claims. The accepted image answer identifies a red square on the left and a blue circle on the right. These descriptions were checked against the authored CSV/PIL fixture. Each case produced one formal C4 candidate hypothesis; neither produced a C3 representation candidate. This establishes two bounded native interpretation/inference handoffs, not causal discovery or full architecture acceptance.

The autonomous trial retrieved its original mission during bootstrap. The model then supplied zero hypotheses, zero operation proposals and one test whose discriminates array contained public API names: mission, read, sources and submit. Those are not hypothesis IDs. C4 rejected it before C0 dispatched anything selected by the model. No instrument data was read and no report was submitted. Even if that invalid test were removed, the original response requested no next operation; the controller would yield. This is therefore also a failure to demonstrate information seeking, not merely a serialization defect.

## Repairs that were tested

The existing authenticated loopback transport, exact /tokenize admission, actual prompt-usage reconciliation, selected native protocol questions, C1 original-wire recording and no duplicate inference controls remain in use. All native acceptance, evidence/reference and authority checks remain enforced.

The initial server failure exposed propertyNames in three native analysis-map schemas. The serving envelope now defers only the known 1–256-character map-key bound to native validation; unexpected new key constraints fail explicitly. Values, operation shapes and other schema constraints remain. XGrammar is pinned as the serving backend. It warns that oneOf may be approximated during decoding; complete native validation remains authoritative. The regression check confirms invalid native map keys are still rejected. [Native schema](evidence/native-qwen-rerun-20261022/native-generation-schema.json) and [serving schema](evidence/native-qwen-rerun-20261022/serving-schema.json) preserve the distinction.

After the second failure, generic ID-reference semantics were exposed in control metadata: rivals/discriminates reference declared hypothesis IDs, and evidence references must match the pinned context. No domain hypothesis, operation sequence or answer was supplied. NativeGateway adapter/lineage is now 1.2. The prior C0 final-turn completion fix is retained. Fresh workspaces were used; no old ledger was modified into a success.

Worker examples now accept a separate diagnostic output directory and correctly report the 2,048-token native or 4,096-token controller output reservation. This changes output organization and metadata, not the mission, data or inference limits.

## Preserved evidence and practical limits

All **48 exported files**, four raw state archives and **17 SQLite database copies** passed hash/archive or database integrity checks. The successful native and failed controller source manifests each matched all 70 transferred source files. Earlier source is pinned at the parent commit; the 0.9.3 changed files were reconstructed and checked against their exported hashes. Each trial has its own receipt, manifest and verification. These are implementer checks, not independent scientific review.

Raw state ZIPs and extracted copies are on the desktop under C:\Users\csscs\Documents\Codex\2026-10-22\edi-free-setup\native-rerun-evidence\, in stage1 through stage4. Each folder contains edi-native-state.zip. Selected JSON, exact responses, logs, source pins and manifests are stored in this repository; raw databases, model weights and credentials are excluded.

The previous expired-session observations remain separately recorded in [the historical checkpoint](evidence/native-qwen-20261022/OBSERVED_CHECKPOINT.json). Their lost raw records have not been recovered; the current files are new executions. An initial CPU grammar probe only wrapped a schema and did not validate it; the later actual validator results and successful live run are retained separately.

The model remains Qwen/Qwen3-VL-8B-Instruct revision 0c351dd01ed87e9c1b53cbc748cba10e6187ff3b, vLLM 0.21.0, Transformers 4.57.6, FP16/TP2 on two free Kaggle T4 GPUs, 16,384 context tokens, one image of at most 65,536 pixels and fixed weights. Native jobs reserve 12,288 input and 2,048 output tokens; C0 reserves 4,096 output tokens and keeps four turns / 65,536 total tokens / 600 seconds. The serving request timeout remains 120 seconds. No paid fallback or teacher was used.

Known measured calls across all trials consumed 37,685 input and 2,634 output tokens; first-attempt returned usage is unknown. Rejected work is included where measured. Setup, complete aggregate elapsed cost and energy remain unqualified. Shared Kaggle user/process resources are not hard isolation. Completed-call reopening and SQLite integrity do not establish whole-application or broker restart recovery.

## Next development gate

[Native output recovery and inquiry plan](NATIVE_OUTPUT_RECOVERY_PLAN.md) records the concrete gap: a known rejected response leaves C0's turn pending and C4 awaiting import, without an explicit bounded correction/yield path. The model's failure to request information must also be investigated. The plan preserves original outputs and does not delete invalid scientific fields to manufacture success.

The next gate remains the same unguided instrument workflow: independently acquire information, submit a grounded report, account for failures/corrections and reopen durable state. A valid wire format alone cannot pass it. Full P1, C5/C6, hard isolation, teacher integration, forest investigation and matched comparison remain open. No superiority, transfer, latency or energy advantage is established.

The component/interface reviews remain REVISE and self-authored. Existing owner and outer lane inventories retain their authority dispositions; structural helper success is catalogue consistency only. The frozen forest package is unchanged.

## Reproduction and sources

[Generated notebook](../../examples/free-compute/edi-native-integration.ipynb) bundles exact source without outputs or credentials. Run each launch once, monitor only thereafter, and export/hash-verify each trial before starting the next. Original invalid jobs are not silently retried. The notebook is a prepared input, not a saved live-session export.

Primary implementation references: vLLM [structured outputs](https://docs.vllm.ai/en/v0.21.0/features/structured_outputs/), [XGrammar validation](https://docs.vllm.ai/en/v0.21.0/api/vllm/v1/structured_output/backend_xgrammar/) and [Guidance validation](https://docs.vllm.ai/en/v0.21.0/api/vllm/v1/structured_output/backend_guidance/). Actual errors, package inventories and outcomes are in the retained evidence.
