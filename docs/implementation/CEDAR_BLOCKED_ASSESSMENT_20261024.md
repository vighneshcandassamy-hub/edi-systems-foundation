# Cedar blocked-run assessment — 24 October 2026 IST

The first actual teacher-assisted Cedar run failed to advance beyond four completed cycles. The fifth inquiry was blocked before provider dispatch: the exact rendered input measured **18,107 tokens**, exceeding the frozen **16,384-token** input cap by **1,723**. A full 4,096-token output reservation would require 22,203 tokens, beyond the configured 20,480-token model window. Raising the input cap alone is therefore insufficient.

This is a confirmed context-capacity integration failure, separate from the subsequent loss of browser access. The downloaded checkpoint is 1,327,341 bytes, SHA256 `53d2c145d033e9fcfe0d775efd1bf5fc647be00e221b67104abe46308e45ac34`. ZIP CRC and all eight EDI stores plus the Cedar broker database passed integrity checks. Native state is waiting-model, turn 4, job `10052b6d-88f2-4323-aba4-b38117bde51f`. There is no provider-journal row for this blocked job. No terminal receipt or final submission exists in this export. GPU shutdown remains unverified.

## Observed student structure and behavior

Each admitted decision has evidence record pointers, current understanding, an information need, expected use, optional repeat justification and a revision feedback response, followed by one operation proposal. These are generated justifications, not verified access to private internal reasoning.

| Cycle | Draft and revision | Assessment |
| --- | --- | --- |
| 0 | Internal mission UUID treated as a public document ID. Revised prose said it would browse, but the actual action repeated the invalid acquisition and failed. | Rationale-to-action inconsistency; provider wire and admitted operation agree, so no parser substitution. |
| 1 | Draft repeated the same UUID error. Concrete protocol coaching led to an actual sources request. | Local feedback uptake; sources call succeeded. |
| 2 | Draft confused the sources-response UUID with a public asset ID. Revision used forest search with an empty query and limit 5. | Discovery succeeded after concrete namespace coaching. |
| 3 | Draft used a valid damage-keyword search. Revision read birch observation sheets from years -39 to -30. | A real public document was selected. The prose still said it retained search while the action changed to read, and expected expenditure/intervention utility not established by the listing. |

Three first revisions omitted required feedback_response and were rejected; bounded corrected revisions were admitted. The resulting student-call count is **11**, not eight. All 11 calls completed and reported **106,988 input / 5,118 output tokens**. Eight teacher responses completed. Unknown teacher usage was charged full reservation, giving **275,946 policy units**. These units do not measure dollars, energy or teacher tokens. No weights changed.

Public successful operations were mission, sources, search and read. The failed native asset acquisition remains preserved separately. No public intervention, measurement commission, time advance or submit occurred. The admitted responses contain zero formal hypotheses, tests or C3 candidates. This run did not establish the ecological explanation, expenditure relationship, intervention effectiveness, learning transfer or advantage over an LLM baseline.

## Why document acquisition exposed the capacity problem

The read response is 10,840 bytes. C0 selected its first 8,192 bytes. That prefix contains a **5,804-character encoded asset**, followed by only part of the readable CSV; the body field begins at byte 5,892. The earlier suspicion that no readable CSV was selected was incorrect: a partial body is present. The full raw response remains retained.

The selection is explicitly bytes:0:8192. Its completeness field concerns the requested selection; it must not be interpreted as a whole-document read. Acquiring a file did not imply that all rows reached reasoning. No student response to this new cut occurred because token preflight failed. Consequently no interpretation of those rows can be attributed to Qwen.

The gateway's exact token check prevented an oversized provider request. C0 caught the error as model availability and retained waiting-model, even though this capacity error is nonretryable for the unchanged frozen job. The error cannot be repaired by replaying teacher feedback, retrying the same job or restoring browser access alone.

## Required engineering correction before a separate revised run

1. Budget the complete serialized prompt with the pinned tokenizer before freezing a cut, including access descriptions, protocol, selected evidence, teaching memory and revision overhead. Reserve output and model-window capacity. If a single indispensable item cannot fit, return an explicit capacity disposition.
2. Preserve the raw public response and provenance. Present source-linked readable content or an explicit typed interpretation, with ranges and omissions; do not spend text context on a duplicate encoded asset. Validate decoded bytes and never turn a generated summary into independent evidence.
3. Bound retained teaching memory and offer explicit context selection. Preserve the omitted original records for subsequent retrieval. No silent loss of mission constraints, no hidden answers or fabricated scientific observations.
4. Give deterministic capacity failure its correct operational disposition. Preserve the original job/cut and raw failure; a changed cut/configuration needs a distinct recorded identity rather than an invisible retry.
5. Correct response-schema guidance so every revision explicitly supplies decision_basis.feedback_response. Continue checking action grounding against actual operation arguments rather than counting compliant prose as successful uptake.

These are proposed repairs, not implemented or validated by this assessment. The live frozen source, benchmark, weights and limits have not been modified. The current failed run should be preserved and its owned compute stopped. A future revised run must keep this failure in the comparison history.

See [machine-readable assessment](evidence/cedar-blocked-20261024/assessment.json) and the [prospective protocol](CEDAR_ASSESSMENT_PROTOCOL.md). Official hidden-world evaluation was not invoked on this nonterminal checkpoint.
