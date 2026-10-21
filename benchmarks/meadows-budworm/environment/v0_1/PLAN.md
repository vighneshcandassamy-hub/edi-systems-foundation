# Environment component plan

Scope: implement the owner's two-database investigation design and superficially related distractions. Baseline corpus commit: 489454450b11102ac590900f9c3962a8ee39acb5. Corpus SHA-256: 49856811262c175efe99c31635e098e56312bdbca98a4ec1f58fab12794e5bd5. This is an additive test harness, not a modification of the EDI observation/substrate architecture or its nine representation families.

## Allocation and authority

The evidence package owns immutable received/constructed observations. The broker owns admission, request/response idempotency, final-submission closure and the audit journal. The participant owns its hypotheses, representations, memory and answer. The operator evaluator owns hidden development labels and outcome scoring. The builder is an offline maintainer utility, not a runtime participant service. Real source APIs and SQLite/Python are external dependencies.

The machine trace is `REQUIREMENTS.json`. Engineering evidence is in `fixture/reports/VALIDATION.json`; interface/component reports are in `reports/`. No EDI consumer has been connected.

## Design decisions

1. Preserve the original corpus. It lacks matched predator and management histories, so causal ground truth cannot be invented and passed off as historical fact. A declared constructed case provides known internal transitions; real excerpts remain external context.
2. Use two participant-facing stores. A single downloadable database with a visibility flag would expose requestable evidence and private answers to a filesystem-capable agent. The participant gets only its initial snapshot and broker responses. The third store belongs exclusively to the operator.
3. Make noise semantically close. Wrong scope, species, denominator and duplicate lineage demand evidence assessment. Same-plot biochemical noise additionally challenges reliance on recent correlation. Its interpretation is limited to the declared constructed world.
4. Keep policy outcome, not classification agreement, primary. A participant may use contextual evidence in a way the curator did not anticipate. Private labels diagnose resource use; they never directly reward accepting/rejecting a card.
5. Keep requests and observed evidence separate from hypotheses. Rationale, alternatives and expected observations are supplied before response delivery and retained in the journal. Evidence is frozen before the session; the broker cannot manufacture confirmation.
6. Keep runtime small: Python standard library, SQLite, one loopback HTTP broker per session, a separate offline scorer. No LLM framework, embedding model, paid inference, public deployment or source refresh is required.

## Contracts

Public items have opaque IDs, title/summary, source group, scope, measurement units/clock, format, original-asset hash and measured rows. There is no usefulness, class, causal-role or hidden-state field. Format is not a class label; the same serializers cover multiple classes. Source identity and physical-entity identity are separate. External field records retain their own IDs and dates; simulation years never become calendar dates.

`initial` and `catalogue` are bounded/paginated. Search uses public text and optional district scope only; it never reads evaluator classes. `request` requires a prior rationale and expected observation, supports optional alternatives and bounded row/asset reads, rejects future selectors and unsupported fields, and records an immutable response per request ID. A conflicting reused ID fails. An unknown item fails without synthetic fallback.

`submit` accepts only declared policy options, bounded finite forecasts, explanation and admitted evidence references. It commits one final answer and gives no reward feedback. Retrying a committed request/answer is idempotent. Restart recovery of committed responses is verified. Crash during an arbitrary filesystem or power failure and concurrent hostile workloads are not qualified.

The evaluator reads only a final run journal and its frozen private outcome store. It reports policy loss, regret against five declared options, forecast error, acquisition diagnostics and HTTP byte/attempt accounting. Relevance classes are not rewards. The participant cannot query the evaluator.

## Failure modes and limits

| Failure | Containment / status |
| --- | --- |
| Generated data mistaken for field evidence | Origin and scope declared in each item; real corpus unchanged |
| Surface correlation mistaken for cause | Longer histories and controlled contrasts available; no curator-class reward |
| Duplicate report mistaken for independent evidence | Shared source-group identity retained |
| Arbitrary SQL/path or hidden future requested | Strict operation/field allowlists, read-only stores and no private endpoint; checked |
| Retry causes duplicate admission or overwritten explanation | Content-bound request IDs; conflicting replay rejected; checked |
| Restart loses committed evidence/answer | Durable SQLite journal; exact committed response replay checked |
| Invalid or oversized query | Typed selectors, input/body/read limits and explicit errors; checked |
| Investigation quality judged by a predetermined narrative | Scores use declared outcomes; no expected mechanism prose answer |
| Participant reads owner filesystem / generator | Requires an externally isolated participant runtime; local HTTP alone does not solve this |
| One-world shortcut or policy bias | Development fixture only; general qualification blocked pending independent varied worlds and baselines |

## Gates

Architecture/contract: self-reviewed within this bounded harness. Runtime: only the scripted storage/HTTP/submit/score path can pass its declared checks. EDI integration, human inquiry, autonomous discovery, difficulty, biological fidelity and comparative advantage remain untested. Do not promote review-helper consistency into scientific evidence.

Contributing workflows: repository `edi-component-review` and `edi-interface-review` as pinned on the baseline. Their findings led to physical participant/evaluator separation, durable pre-acquisition request content, separate logical/transport accounting, and explicit unqualified isolation/consumer obligations.

Next consumer work: connect an isolated human or machine participant through the public client, first as a development run. A frozen comparative benchmark and additional worlds require their own protocol.
