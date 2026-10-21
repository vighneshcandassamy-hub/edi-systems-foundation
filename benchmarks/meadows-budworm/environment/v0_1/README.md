# Two-database investigation environment

Version 0.1, 21 October 2026. **Operational development fixture; EDI/human comparison not run.**

The participant receives a mixed initial database, then requests further evidence from a second database through a broker. Useful observations and superficially related distractions use the same public schema and overlapping formats. Private evaluator labels and future outcomes live in a third, operator-only store.

## What is built

| Artifact | Contents | Participant access |
| --- | --- | --- |
| `fixture/initial/initial.sqlite.gz` | 30 initial items: sparse observations, convincing distractions, repeated bulletins and external context | Initial snapshot or public API |
| `fixture/investigation/investigation.sqlite.gz` | 129 requestable items, including longer histories and controlled assays | Broker responses only; do not mount the database in the participant runtime |
| `fixture/evaluator/evaluator.sqlite.gz` | Generator history, conditional relevance notes and five policy outcomes under identical future weather | Operator only |
| `fixture/participant/` | Initial SQLite, mission and public API client | Participant distribution |

The task is a constructed forest district with eight plots and 60 simulation years of evidence. A participant investigates recurrent foliage damage and protection spending, then chooses among five declared ten-year policies. Its forecast and policy outcome are scored by the operator after final submission. The objective and policy definitions are public; transition coefficients, relevance notes and future outcomes are private.

The real 32,895-record corpus is unchanged. Selected real records are included with their original identifiers as explicitly external context. Constructed observations are never represented as real New Brunswick, Maine or Canadian field measurements.

## Why the noise is superficially persuasive

- Same insect, trees, plots and years: biochemical and needle-assay channels have no structural effect in this constructed world. One historical biochemical series has an accidentally strong recent correlation with insect density. A requestable controlled contrast can challenge that apparent relationship.
- Same forest/insect language: a feeding study concerns a different moth species; another monitoring series comes from a separate forest district.
- Same management vocabulary: provincial nominal protection expenditure is not target-plot treatment intensity.
- Same canopy theme: all-species cover is not susceptible-host foliage stock.
- Same source repeated: bulletins re-present the same observations, with shared source-group identifiers.
- Same district name: an archive describes a replaced demonstration stand, not the current plots.

These are conditional distinctions. Sampling-method records are context, not biological forcing, but can still be valuable. Wrong-scope evidence can help a participant establish a boundary. Relevance classes are diagnostic notes, **not a scoring reward or a universal useful/noise truth**. No participant item contains those classes.

## Run locally

From this folder:

```bash
python restore_environment.py --environment fixture
python verify_environment.py --environment fixture
```

Choose a fresh token of at least 24 characters and set `EDI_BENCHMARK_TOKEN` in the operator and participant client environments. Keep tokens and run journals outside Git. Start one broker per participant/run:

```bash
python broker.py --environment fixture --run /tmp/edi-bug-tree-run --port 8765
```

The public client supports:

```bash
python client.py mission
python client.py initial --json '{"request_id":"brief-1","limit":20}'
python client.py catalogue --json '{"request_id":"search-1","query":"forest insect feeding"}'
```

Use an item ID returned by the catalogue to request evidence. The request must include `rationale` and `expected_observation`; `alternatives` can state competing explanations. The journal retains these fields alongside the response. Record pagination and original-asset byte ranges are supported. Unknown evidence stays unavailable; the broker does not invent answers or call a model.

Final submission contains a policy, next-year mean-density forecast under that policy, explanation, cited evidence IDs and uncertainties. It receives acknowledgement only. Further new acquisitions/submissions are then closed; an exact idempotent retry returns its original acknowledgement. The operator scores it separately:

```bash
python evaluate.py --environment fixture --run /tmp/edi-bug-tree-run
```

## Isolation and accounting

The broker opens only the two public evidence stores and its own audit journal. It never imports the world generator or opens evaluator files. There is no public SQL/file-path/evaluator/score endpoint. A bearer token is required and the server binds to loopback. The participant archive excludes the investigation database, evaluator, world source, labels and development reports.

This does **not** isolate a participant who has filesystem access to the operator repository or process environment. Actual blind runs require a participant process/container/account without those mounts or credentials. The local prototype has not been deployed or security-qualified for hostile multi-tenant use. Do not hand the complete repository or owner archive to the participant.

Logical acquisition events are idempotent. HTTP attempts separately record retries, denials, returned bytes and broker service time. Initial snapshot size is reported separately. Token use, participant reasoning time, model latency, hardware compute and energy are not measured by this broker.

## Verification and scientific limits

The focused scripted campaign verifies actual HTTP acquisition, rationale retention, source lineage, absent public relevance labels, future denial, forbidden paths, pagination, byte ranges, retry conflicts, durable response replay, final-submission closure and operator scoring. It verifies source/database hashes and frozen policy replay. It is an engineering fixture, not a reasoning-agent result.

The world includes fast insect change, slow host composition, foliage loss/recovery, bounded natural-control response, delayed natural-enemy adjustment, weather pulses and treatment decisions. Its coefficients and policy choices are **declared engineering assumptions**, not fitted ecological estimates or a faithful numerical reconstruction of Meadows' full account. Human institutions, industrial demand and all real ecological mechanisms are not modeled. No policy is forced to win; preserve the computed outcomes, including those that differ from an expected moral of the story.

One development world and five finite policies cannot establish general discovery, transfer, optimum control or EDI advantage. Independent unseen worlds, null/counterexample cases, richer stakeholder objectives, ecological validation, matched baselines and full resource accounting remain later qualification work.

See `PLAN.md`, `REQUIREMENTS.json`, `reports/COMPONENT_REVIEW.json` and `reports/INTERFACE_REVIEW.json` for the scoped review and evidence.
