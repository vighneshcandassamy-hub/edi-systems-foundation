# Interlude evidence sufficiency and access audit

21 October 2026. Operator-only analysis of the current evidence corpus and constructed v0_1 development fixture, pinned to repository revision `6650dc94c4ea640e43fc52ccd42cfd93cad49c98`.

**Decision: not yet ready to test discovery of the full Meadows interlude.** Existing evidence supports narrower investigation in an explicitly constructed world. The complete historical/systemic account cannot currently be investigated through the participant interface. This is an environment finding, not an EDI failure.

This audit must stay outside participant materials. It identifies evidence gaps and intended scientific coverage for the operator; it is not a reading list, causal graph, suggested inquiry sequence or answer rubric to give EDI. No new hypotheses, mandatory reasoning steps or solution suggestions have been added to the participant interface.

## What was reviewed

- Meadows, *Thinking in Systems*, the complete interlude “Spruce Budworms, Firs, and Pesticides,” printed pages 92–94 (supplied PDF physical pages 109–111).
- The actual corpus coverage/gap declarations and database structure.
- The initial and investigation snapshots, mission, broker, builder, world transitions and evaluator implementation.
- Actual HTTP catalogue, record and asset retrieval in an isolated temporary copy of the two public stores. No evaluator database or labels were opened by the reachability probe.

No paid inference or human/EDI/LLM reasoning trial was run. Operator-selected queries test whether a route exists, not whether EDI discovers the right question.

## Distinguish kinds of withheld information

1. **Not initially supplied but obtainable:** existing reports, older observations and supported measurements. Their existence must be discoverable through ordinary browsing, source directories, native references or inquiry. No special phrase or answer-specific alias should be necessary.
2. **Not yet known in the world:** a new field measurement or experiment. Its result needs a supported operation, time, resources and a grounded observation process. The current broker does not provide these operations.
3. **Unavailable or unknowable from the available evidence:** absent historical records or observationally indistinguishable explanations. An honest uncertainty statement is appropriate; a better question cannot conjure nonexistent evidence.
4. **Permanently private evaluation information:** future trajectories, model coefficients, answer notes, labels and scoring internals. These are not additional sources to release when the participant asks the right question. Future observations can become public only through legitimate world progression in a future implementation.

The supplied book is an operator reference for scenario design. Giving its complete case explanation to the participant would change the task from discovery to using a published explanation. Historical methods and expertise may be admitted under a declared availability rule; model pretraining contamination remains an independent limitation.

## Results of actual access checks

- All **30 initial items** were returned through the initial endpoint.
- All **129 requestable items** were discoverable by paginating the public catalogue without a search phrase.
- All **129 requestable items** were fetched, with record pagination as needed and original-asset SHA-256 verification.
- The two snapshots and original real-source SQLite remained unchanged.
- Unknown evidence returned unavailable; future records were denied. These are correct boundaries, not missing-evidence recovery features.
- Requests without the mandated rationale/expected-observation template were rejected. This restriction conflicts with the owner's preferred unguided inquiry design and should be removed or made optional in a reviewed runtime change.
- Asking a person, commissioning a measurement, acting and clarifying the objective all returned unknown operation. The corresponding resources cannot currently be reached through a conversational question.

Search is keyword matching against titles/summaries with any-term matching. `natural enemies` returned 12 monitoring items, while `birds`, `parasites` and `spraying` returned zero. `treatment` returned 12 items. A broad `historical tree rings` query returned 36 matches without supplying actual tree-ring data. Thus a hit count is not proof of semantic coverage. Browsing avoids an exact-word dead end for existing records, but does not fill absent content or demonstrate EDI inquiry ability.

The **32,895-record source corpus is not fully exposed by the current scenario broker**. It serves two specific scenario databases. The builder copies six external source excerpts of 12 rows each into the investigation store, with three initial three-row excerpts drawn from those series. The full reference reports, species pages and original multimodal source archive are not thereby requestable through this broker. Owner-level CLI access to the full corpus is not an isolated participant access route.

## Interlude coverage review

The entries below are operator-side investigation dimensions. They do not prescribe how EDI must organize the evidence or require it to reproduce the book's terms.

| ID | Dimension in the interlude | Available initial/requestable evidence | Remaining limit |
| --- | --- | --- | --- |
| I01 | Long recurrence preceding modern management | Recent constructed series initially; 60 simulation years requestable | No native tree-ring record; the named older archive describes a replaced demonstration stand. It is not a valid pre-treatment baseline for the current plots. |
| I02 | Changing industrial use of tree species and changing definition of the problem | Owner-held species references; provincial spending proxy in the scenario | No participant route to the needed historical industrial/decision records; species-use references alone do not establish local motivation. |
| I03 | Repeated treatment and recurrent insect damage | Constructed larval, foliage and treatment histories, recent initially and older on request | Supports association and forecasting in this fixture; treatment is selected by insect density, so naive treated/untreated comparison is confounded. No live intervention comparison. |
| I04 | Natural-control observations | Aggregate natural-enemy index, initial and longer requested histories | Not separate bird, spider, parasitoid or disease measurements. Real corpus lacks matched histories. |
| I05 | Host preference and forest composition | Mature susceptible-host fraction; owner-held species text | No target-district comparative host-feeding observations or separate fir, spruce and birch cohorts. |
| I06 | Slow succession and recovery following disturbance | Foliage and mature-host histories | Aggregate proxies only; no explicit tree ages, mortality records or non-host replacement sequence. |
| I07 | Seasonal weather as trigger rather than complete explanation | Constructed weather anomaly history; regional real-weather excerpts | A scalar anomaly does not separately measure warm/dry spring conditions; real weather is not matched to scenario plots. |
| I08 | Natural-control saturation | Two requestable feeding-assay items, target and other species; enemy and insect histories | Target assay can support bounded consumption in the constructed case. Species scope matters; it is not a fitted reconstruction of historical biology. |
| I09 | Food depletion and outbreak termination | Foliage-dependent capacity in the model; insect/foliage history | Partial model support; no full mature-host death and multi-species recovery process. New measurements cannot be commissioned. |
| I10 | Treatment affecting natural enemies | No matched direct non-target treatment records | The current enemy transition has no direct spray term. Data generated by this model cannot establish this interlude pathway. |
| I11 | Management dependence and short/long-term tradeoffs | Constructed treatment records and fixed ten-year policy outcomes held privately | No operational continuation for the participant, no timber-supply commitments, and no local economic decision histories. Private future answers must not be released as substitute evidence. |
| I12 | Stakeholder purposes, expenditure concerns and disagreement | Public mathematical objective; aggregate provincial spending index | No stakeholder-question route, correspondence, preference clarification or objective-revision acceptance. Cannot test evidence-supported reframing adequately. |

The matrix is also recorded in `INTERLUDE_COVERAGE.json`, with example existing item IDs and dispositions. Existing items can be useful in ways not anticipated here; there is no useful/noise classification reward.

## Structural discrepancy requiring correction before a full interlude claim

The book's treatment account includes a direct non-target natural-enemy pathway. In current `world.py`, next-step enemy abundance depends on the existing enemy/insect state, but not on spray intensity. The audit held state and weather constant and compared no spray with full spray: next-step enemies were **0.51 in both cases**. Prey can produce indirect later changes, which is a different pathway.

This should not be repaired by writing a fictional report claiming a treatment effect while leaving the world unchanged. Either declare this a deliberately different world and evaluate accordingly, or implement a scientifically scoped alternative world with explicit, evidenced or declared treatment mechanisms and consistent observations. Preserve the current fixture as a baseline. Do not tune parameters to make a particular policy win.

## Acceptance standard for the next environment

Every substantial conclusion we intend to assess needs at least one legitimate evidential route, or a declared reason it remains unresolved. That route can begin with broad browsing and extend through naturally available sources; it need not appear in the initial brief. An operator may audit those routes privately without revealing them to EDI.

Check separately:

- **Existence:** does the source actually contain the observation or testimony?
- **Discovery:** can a participant discover the source through an ordinary public operation?
- **Acquisition:** can its contents be obtained, including raw assets, with known operational limits?
- **Compatibility:** are place, time, units, identity and treatment conditions sufficiently established, or explicitly uncertain?
- **Discrimination:** can the observations distinguish competing explanations, or only support association?
- **Independence:** are repeated reports and derived modalities traced to their shared source?
- **Uncertainty:** are absent evidence, conflicting accounts and unsupported operations distinguished?
- **Non-interference:** are evaluator notes, future truth and operator audit absent from participant access?

A retrieval pass establishes only the first access steps for the inspected item. It does not establish causal identification, historical fidelity or an EDI ability.

## Prioritized corrections and additions

1. Register source-level participant access to the broader archive, subject to chronological and contamination rules. Support broad browsing and native-content search, with ordinary provenance. Do not create a curated list of sources that reveal each intended causal relationship.
2. Acquire real records for the missing historical, forestry, treatment and human dimensions. Retain honest gaps if the records cannot be obtained. Constructed supplements must be labeled and separated from historical observations.
3. Specify a new world version that either faithfully scopes the interlude mechanisms or explicitly tests alternative mechanisms. Include the relevant timescales and human commitments before assessing long-term consequences or objective reframing.
4. Add neutral inquiry and measurement operations with bounded source/person knowledge, operational delays and explicit unavailable responses. General query handling must not manufacture confirming evidence or expose answer notes.
5. Make reasoning templates optional and allow supported interventions/proposals beyond the five fixed policy choices. These are material interface changes needing their own component/interface review and runtime checks.
6. Repeat the access and evidence audit, then run an isolated EDI development participant. Record its actual questions and responses without operator hints. Assess its predictive commitments and conclusions, including justified uncertainty; do not require the operator's preferred question sequence.

## Scope of this change and readiness

Only an operator audit, a reproducible diagnostic script and checkpoint are added. Existing world equations, participant material, broker behavior and source observations are preserved. Existing component-pair and contract inventories are unchanged; this review identifies unimplemented required future paths rather than claiming those paths exist.

| Gate | Decision |
| --- | --- |
| Existing public item retrieval | Verified for this fixture through actual HTTP |
| Broad source-archive participant access | Incomplete |
| Full interlude evidence sufficiency | Blocked by listed gaps |
| New inquiry/action/clarification operations | Not implemented |
| Full interlude world fidelity | Not established; a material structural discrepancy identified |
| EDI autonomous question selection and conclusions | Not run |
| EDI comparative advantage | Not run |

This is a scoped self-review, not independent ecological validation. Follow-on interface work uses the repository's EDI interface-review skill; no new intelligence or integration gate passes from this audit.

## Reproduce the access audit

From the benchmark folder:

```bash
python environment/v0_1/audit_reachability.py --out operator-audit/REACHABILITY.json
```

Python standard library only. The script restores the two public snapshots into a temporary directory, starts a loopback broker with a temporary secret, retrieves records/assets, probes existing and missing operations, runs a fixed-state world diagnostic and cleans up. No secret, evaluator label, private future trajectory or run-specific participant trace is stored in the report.

Source reference: Donella H. Meadows (2008), *Thinking in Systems*, printed pages 92–94, supplied `Meadows-2008.-Thinking-in-Systems(3).pdf`. The interlude is treated as a narrative reference for this audit, not as quantitative calibration or a demonstration of a final universally successful historical intervention.
