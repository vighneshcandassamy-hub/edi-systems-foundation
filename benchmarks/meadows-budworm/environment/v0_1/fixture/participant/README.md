# Participant materials

You receive `initial.sqlite`, `mission.json` and `client.py`. All participants use the same evidence interface. The initial database is a mixed briefing; more observations can be requested. Scope, units, time and source relationships matter. No relevance labels are supplied.

This is a constructed development scenario. Separately attributed external records retain their real source identifiers and do not become measurements of the scenario's target plots. Simulation years are not calendar years.

Read `mission.json` for the task, objective, policy options and final-answer fields. The SQLite `items` table contains initial title, summary, source group, scope, serialized rows, format and original asset bytes/hash.

The operator supplies an evidence-broker URL and a participant token. Set the token in `EDI_BENCHMARK_TOKEN`; do not put it in a report or commit it. The client defaults to the local broker at port 8765.

```bash
python client.py mission
python client.py initial --json '{"request_id":"initial-1","limit":20}'
python client.py catalogue --json '{"request_id":"catalogue-1","query":"forest insect monitoring","limit":20}'
```

For evidence acquisition use `request` with a catalogue item ID, a unique `request_id`, a `rationale`, and an `expected_observation`. Optional `alternatives` can describe what you are trying to distinguish. Record reads support offset/limit; original assets support bounded byte ranges. Use the exact returned IDs, scope and source groups. An unavailable request does not generate new evidence.

When ready, `submit` a declared policy, forecast, explanation, evidence IDs and uncertainties. Submission is final: new inquiries and new answers close, while an exact retry remains idempotent. There is no outcome-feedback endpoint during the session.
