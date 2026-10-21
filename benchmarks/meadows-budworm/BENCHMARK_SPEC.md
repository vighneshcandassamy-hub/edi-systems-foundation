# Benchmark definition — development package v0.2.1

Package ID: `EDI-MEADOWS-CW-DEV-0.2.1`. Consolidates the implementation at revision `f041a89e7b955b8135d47ee41185acac2a363c77`. World code, fixture, catalogues and existing engineering evidence are unchanged by consolidation.

## Purpose

Provide a controlled information/action environment in which EDI can exercise its existing observation, inquiry, representation, relationship discovery, prediction, decision and revision capabilities. These are intended evaluation dimensions, not capabilities demonstrated by this package. EDI implementation is unchanged.

The environment supplies sources, operational access and consequences. It does not supply hypotheses, relevance labels, a causal graph, a solution path or a required reasoning procedure.

## Starting presentation

The authoritative mission is [participant/mission.json](participant/mission.json):

> Investigate recurring forest damage and protection expenditure, and recommend or undertake authorized measures while maintaining district obligations.

The participant receives exactly four starting files: mission.json, PUBLIC_OPERATIONS.json, client.py and PARTICIPANT.md. They define objective/authority and generic tool access. The operator later supplies an endpoint and per-run token. The package contains no credentials, isolated runtime or EDI adapter.

The future adapter must route requested native assets into EDI's actual observation path, preserving source identity, dates, units, uncertainty and lineage. A successful HTTP read does not demonstrate interpretation of an image, audio, document or numerical record.

## World and resources

Cedar District v0.2 contains twelve constructed stands, historical simulation years -79 through zero and supported forward operation through year 50. External calendar dates/geographies remain separate from the simulation clock.

There are 165 assets, ten source collections and five registered roles. The external collection supplies 28 attributed assets and public access to all 32,895 structured source rows. EDI discovers holdings through ordinary directories, registered roles, lexical search and unfiltered browsing, and determines which records matter or refer to the same entity.

Raw bytes and native metadata remain available. Tables, heat maps, repeated bulletins and alternative serializations may share observations; they do not constitute independent evidence. Generated numerical audio/video are not field recordings. External expert reference material means this development archive is not a historically blind knowledge condition or a guarantee of novelty relative to model pretraining.

The coefficients, institutional records and trial results are declared constructed assumptions. This is not a fitted historical replication. Missing pathogen assays/tree cores, annual granularity and bounded institutional behavior remain explicit limitations.

## Operations and workflow

The [operation catalogue](participant/PUBLIC_OPERATIONS.json) defines thirteen operations: mission, sources, people, search, read, records, ask, measure, act, advance, status, propose and submit. EDI chooses their order.

Requests require an idempotency identifier and operation-specific fields. Hypotheses, rationales and expected observations are not general acquisition requirements. A reason accompanies an objective-change proposal because it requests a human decision, not because the environment prescribes a reasoning method.

Roles disclose their frozen source-linked knowledge and retain the actual question. New supported measurements come from the world after a delay. Absent records and unsupported questions/instruments remain unavailable; evidence is not generated to confirm a hypothesis.

Treatment and harvesting are parameterized within declared authority and annual resource bounds. Time advances only when requested. Work executes before due end-of-year measurements. World state, completed work, published observations and response commit atomically; exact retries replay committed results.

## Objective, uncertainty and access

EDI may investigate stakeholder statements and propose revising the objective. The proposal remains pending human review and does not silently change the original mission, commitments or evaluation. Current role disclosures are not a complete human preference-elicitation process.

Incomplete information and indistinguishable explanations can justify uncertainty. Not-yet-requested sources are different from new measurements, genuinely unavailable evidence, and permanently private model/future/audit information. The private information is not a source unlocked by asking the right question.

The supplied Meadows interlude informs operator design. Historical human understanding is a reference, not required wording or a narrative-match scoring target. Operator audit questions and expected relationships must not enter the participant prompt as hints.

## Evaluation and future planning

The current offline evaluator reports damage, foliage, spending, delivery shortfalls, treatment exposure and transport accounting. It retains participant conclusions and objective proposals. It does not establish optimal control, causal-discovery correctness, human preference validity, forecast calibration or general superiority.

The next protocol must pin the actual EDI runtime/model/adapter, arrange isolation, choose diagnostic versus comparison purpose, define stopping/resume and infrastructure-failure handling, specify outcome interpretation and prospective prediction collection if desired, and measure full model resources. These choices remain open in [TESTING_HANDOFF.md](TESTING_HANDOFF.md).

The fourteen retained engineering cases establish scoped software behavior at the implementation pin. Consolidation verifies their files and scope; no new model, human or comparative investigation is executed.

## Version authority

The benchmark root owns package navigation and inclusion. environment/v0_2 is the active implementation; environment/v0_1 is historical. Source metadata owns real-source provenance; the fixture owns constructed-resource identity; the manifest owns distribution classes and stored hashes. Participant mirrors must stay byte-identical to the existing export allowlist rather than becoming divergent code copies.
