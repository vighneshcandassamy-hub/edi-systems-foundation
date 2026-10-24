# Decision grounding repair

24 October 2026 IST. Source 0.10.11.dev0, C0 integrated-1.7, decision policy
`information-seeking/1.1`. This is an EDI engineering interpretation, not a
Meadows prescription or a neural training result.

## Evidence and diagnosis

The stopped corrected-source run is pinned to `3ffa1091c5e4e32237f49c0d9626aca53f622d36`.
Offline reconstruction reproduced the exact recorded messages and decoding
schema hashes for all nine completed student calls. The raw provider content
reconstructs the admitted Response with declared native defaults; all four
revised action proposals match the completed C0 dispatch requests. No new model
or broker call was made. The parser and controller did not substitute a stale
action. The failed revision genuinely repeated the complete capture notebook
while denying information present in its prompt. See the retained
[offline trace](evidence/asset-source-identity-20261024/offline-decision-trace.json).

That revision used 13,978 input / 274 output tokens and finished normally. Its
four selected excerpts total 1,913 characters; the schema field index alone
was 13,514 characters. This establishes prompt overhead and failure under that
prompt, not an isolated causal finding about attention or model capacity.

## Mission, requirements and mechanism

Mission: acquire relevant information, use actual results, preserve uncertainty
and deliver findings. IMP-R08/R09/R18/R19/R26/R32/R33 allocate bounded reasoning,
evidence use and inquiry through C0/C4 and C1/C4. Existing downstream provenance
obligations remain in force. C4 F40-F43 owns its decision workspace and proposal
validation; C0 schedules, C7 authorizes, C1 retains immutable observations and
C3 alone admits durable world-model changes. No new world representation family,
logical owner, external service or direct component lane is introduced.

The versioned decision contract adds an attributed `DecisionBasis` to student
responses under policy 1.1. It contains selected record IDs, current
understanding, information need, expected use of the chosen result, optional
repeat reason and optional feedback response. These are concise decision
justifications, not private reasoning traces or empirical support citations.
Each explanation is bounded to 1,024 characters and at most 16 distinct selected
record IDs are allowed. Empirical hypotheses still require complete EvidenceRef
citations. Generated explanations remain fallible.

Native C4 admission requires the basis, rejects record IDs outside the pinned
cut, requires a repeat reason when a requested native document is already
selected as a complete whole object, and requires an explicit response to the
critique at revision. It checks structure and referential conditions, not the
truth or quality of the explanation. A model can still rationalize a bad
choice. A reasoned reread and disagreement with a teacher remain allowed. No
action is automatically substituted and no source sequence is encoded.

The renderer supplies a derived acquired-source index, labels prior response
stages and removes duplicate inquiry selection/profile metadata. Full Context,
excerpts, reference lineage, limitations, unknowns, substantive prior response
content and all protocol questions remain. Under structured transport, a small
field guide replaces the complete schema index; the full native schema and
admission checks still enforce outputs. Teacher first assessment stays blind
and teacher output remains critique-only. Retained provisional lessons now show
bounded chosen actions with an explicit omission flag when too large; the full
outcome remains native. Neither source repetition nor teacher agreement counts
as independent evidence or proof of learning.

The counterfactual renderer on the saved failure reduces system characters
28,082 -> 16,593 and user characters 25,703 -> 23,995. The schema index shrinks
13,514 -> 765 characters. Exact Context and prior rationale/guidance are
unchanged. This is a character count, not serving token, latency or energy
measurement. See [view comparison](evidence/decision-grounding-20261024/prompt-view-comparison.json).

## Compatibility, failure and alternatives

C0 integrated-1.7 requires a fresh workspace; old C0 journals are not migrated.
New investigations default to policy 1.1. An explicit 1.0 policy remains available
for authored historical cases; it is not claimed to reproduce an old prompt
byte for byte under new source. Offline reopen reads the exact policy frozen in
C0 and never upgrades the saved run. Original live source and checkpoints are
preserved separately.

Malformed decisions use existing retained rejection/correction accounting.
Unknown provider completions are never resent automatically. Exact provider
chat tokenization, existing input/output limits, stage/job caps, C7 grant checks,
native journals, checkpoint export and operator stop remain in force. Missing
context and source failure remain explicit. The derived index covers only the
selected cut; omitted old sources are not declared nonexistent. Metadata-only
or partial selections do not trigger the complete-document repeat condition.
C4 checks do not establish physical identity, freshness or independence.

Simpler alternatives considered: more coaching alone repeated the observed
failure; prompt compaction alone does not verify decision references or make
feedback use reviewable. Automatic source ordering or banning all repeated reads
would impose a solution and prevent legitimate refreshes. Weight training and
model replacement remain separate options if the focused live result shows a
remaining need. This repair does not establish their necessity.

## Review and verification

One authored native five-turn mission exercises actual broker handling, C1
capture, C4 decisions/rejections, blind assessments, revision feedback, C0/C7
execution, final closure and no-redispatch reopen. Three deliberately defective
responses are retained and corrected before their proposed effects. It also
checks that an explicitly reasoned repeat can be admitted without executing it.
The native case passes on Windows Python 3.12; it executes no real model.
Serving grammar compilation is a Kaggle preflight obligation before inference.
See [native case](evidence/decision-grounding-20261024/native-case.json).

Scoped component and interface self-reviews cover the existing eight owners,
28 pairs and 56 lanes, including shared evidence/model dependencies and the
student-teacher-controller feedback cycle. No authority is broadened. Structural
review consistency and authored native execution are distinct from Qwen benefit.

Next: one fresh pinned Qwen engineering mission with the same fixed model and
resource profile. Complete through useful inquiry and a supported submission,
or stop on repeated nonprogress/explicit failure and preserve it. Do not change
this source mid-run or add repetitive teaching runs. Only demonstrated usable
engineering flow permits proceeding to the frozen Meadows comparison. No neural
weights, transfer, EDI advantage or benchmark readiness are established here.
