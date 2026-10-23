# ADR-012: Autonomous controller response and transport contracts

Date: 23 October 2026. Parent: 68111c370042b465a262f6210c25da6915c8f535.
Status: implemented in 0.10.5.dev0; runtime outcome is recorded separately.

## Observed problem and causes

The retained 0.10.1 repeat copied the correct record ID, selector and hash but
omitted nonempty evidence lineage. Native admission correctly rejected both
outputs. Both were also reasoning-only replies, leaving C0 without a next
operation. See the retained-repeat native audit; the original expired attempt's
raw databases remain unavailable and its precise cause is not inferred.

The 0.10.2 run admitted two model-selected operations, then stopped before its
third provider dispatch because the rendered prompt exceeded the 12,288 input
cap. The system message repeated a 28,430-character response definition graph
already sent through structured decoding. Eight native databases passed integrity
checks. This was a bounded transport/context failure, not evidence corruption.

## Decision and authority

A native InquiryRequest explicitly chooses proposal or controller-turn mode.
Proposal remains the default. A student controller turn must propose exactly one
operation or explicit yield. This fixes the executable handoff without choosing
an operation, forcing a teacher, imposing a hypothesis or supplying domain clues.
Teacher output remains fallible critique only. C0 schedules, C7 authorizes, C1
retains raw evidence and C3 retains representation admission authority.

The serving grammar restricts evidence addresses to exact complete references in
the pinned cut, including lineage. Native semantic validation remains decisive;
no output is silently corrected. The C0 identity changes to integrated-1.1 and
requires a fresh workspace for older journals; C4 implementation becomes0.6.1,
while historical0.6.0 episodes remain readable.

For schema-aware native providers, the prompt carries a response field index
instead of duplicating the full schema. The exact full schema still travels in
response_format and native admission remains unchanged. Other prompt control,
all evidence, inquiry and prior outputs remain byte-identical under the focused
regression check. Generic/manual exchange retains its full prompt schema.
The pending job had no recorded inference dispatch; only its transport rendering
is repaired before resume. Its original evidence cut and limits are preserved.
Initial and repaired source manifests and the first raw checkpoint are retained.
The existing origin identity remains stable; exact prompt/schema hashes in the
per-job journal and versioned source manifests identify the changed rendering.

The configured completion timeout is bounded30..900 seconds (default120). This
T4 profile uses600 seconds for a4,096-token cap, based on observed slow generation;
unknown dispatched work still must not be resent. All eight owners are opened
before the run; constructor preflight does not perform their business operations.

## Alternatives and limits

Weakening lineage checks or filling model citations after generation would hide
an invalid reference; rejected. An authored resource sequence or forced teacher
would invalidate autonomous selection; rejected. Increasing context or token
limits would add resource cost before eliminating duplicate protocol content;
not selected. The bounded native context still may need explicit selection as
knowledge grows; this repair does not promise unlimited history.

This is an engineering diagnostic with fixed pretrained priors, synthetic raw
resources, finite budgets and a normal process restart. It does not qualify
scientific reasoning, all component cases, hard OS isolation, crash recovery,
parameter learning, transfer or superiority. The frozen Meadows tree is unchanged.

## Verification and return path

CI-R01/CI-R02/CI-R04 and the predeclared autonomous criteria trace through the
native InquiryRequest, C0 Investigation, C4 admission and NativeGateway. Focused
fixtures check valid complete references, invalid omitted lineage, missing
controller decision, legacy proposal-only output, an empty cut, actual xgrammar
compilation and byte-identical data under transport compaction. Runtime results,
all failures, source/wheel equality and restart are reported in
[AUTONOMOUS_RUN.md](../implementation/AUTONOMOUS_RUN.md). Self-review is not
independent review; broader original gates remain REVISE.

## Subsequent native dispatch finding and correction

The exported0.10.3 archive exposed a more specific failure than the live progress
counter: all twelve accepted asset proposals failed during command hashing,
before broker dispatch, because canonical JSON converted only a top-level native
record. A proposal nested in a digest list remained a Python object. The prior
interpretation as primarily student error recovery is withdrawn; that judgment
was confounded by the code failure. See retained-serialization-failure.json.

The first dispatch regression then reached the broker but found the same defect
in C2 results nested inside an attributed envelope, preventing later closure
bookkeeping. Both original failures are preserved. In0.10.4, command identities
explicitly use proposal.model_dump(mode="json"), and canonical JSON applies the
same native conversion recursively via the JSON encoder. Already-valid JSON
values retain byte-identical canonicalization. Unsupported arbitrary objects
and nonfinite numbers still fail; no fallback stringification is permitted.
No persisted valid command/evidence identities are rewritten.

The authored native dispatch regression now proves an invalid asset reaches the
broker and returns its native error, then sources/read/C2/submission complete.
It also verifies native reopen without redispatch and UNKNOWN_COMMIT for a broker
response loss. Its fixed authored operation order is regression evidence only,
not autonomous reasoning. A fresh live run uses unchanged objective/resources,
predeclared acceptance and model pin. The packager runs this regression and the
controller/grammar regression before starting inference.

## Generic information-access clarification

The first repaired0.10.4 live run completed one real call without rejection or
execution exception and yielded. Its rationale explicitly treated absence of
readings in the selected cut as preventing any supported next operation, even
though access operations were available. Native restart was identical and all
eight stores passed integrity checks; acquisition/submission acceptance failed.
This is preserved in retained-premature-yield.json and is distinct from the
older serialization failure.

Version0.10.5 clarifies only the generic action contract: an authorized request
for information does not require already having the missing observations.
Missing selected evidence does not establish unavailability in the accessible
world. Empirical claims still require evidence; the student chooses whether and
how to inquire and may yield for a justified stop. The clarification names no
resource ID, public operation, hypothesis, solution or investigation sequence.
It is a post-observation protocol repair, not an unchanged-engine scientific
qualification. The original case and acceptance remain unchanged.
