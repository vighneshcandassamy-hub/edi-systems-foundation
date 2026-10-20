# Verification plan, operating profiles and critical review

Version 0.1, 20 October 2026. Status: prospective implementation plan. No product case, inference experiment, capacity run or comparative benchmark was executed in this documentation task. Existing I7-T01–I7-T192 and AF-T01–AF-T24 remain PLANNED — NOT RUN. The new E01–E40 cases are engineering/integration case designs, not additional successful experiments.

## 1. Gate decision and limits

Architecture proposal: suitable for review and concrete contract development, with the ownership, alternatives, flowdown and bounded implementation path documented. This is a scoped self-review, not an independent scientific review. The machine review report may pass architecture consistency while contract, runtime and integration readiness remain pending.

Contract gate: pending typed schemas, semantic fixtures, source-native envelope compatibility mapping, exact dependency/checkpoint pins, restricted mechanism grammar and numerical/event support decisions for the first selected capability. Runtime and integrated intelligence gates: not run. No automatic implementation or deployment follows from a document pass.

The retained substrate blueprint's historical REVISE status is preserved. This package addresses its broad implementation allocation and authority questions but does not retroactively qualify its old contracts or product tests. Current source snapshots stay immutable; changes are prospective and recorded in the new design package.

## 2. Proposed development operating profile DEV1

These are proposed test/admission settings, not measurements or promises. A selected machine and dependency lock must be recorded before the first capacity run. Adjusting a profile requires a new version and rerun; it cannot be changed after seeing a result to turn failure into success.

| Dimension | Initial proposed setting | Interpretation |
| --- | --- | --- |
| Host | 8 CPU cores, 16 GiB available application/DB RAM, at least 100 GiB free workspace disk; hosted model adapter first. | Qualification fixture, not a statement of the current laptop's capability. Model serving hardware is separate. |
| Steady native workload | 50 records/s, mean payload 2 KiB, representative registered source count 100. | Native workload only; media distribution must be separately specified and cannot be averaged away. |
| Burst | Up to 1 MiB/s total native payload for 60 seconds within available spool; individual object up to 16 MiB, larger objects explicitly chunked. | Offered/admitted/rejected bytes and records reconciled, with actual latency and durable-ack semantics. |
| Initial run window | One focused integrated campaign, including a 1-hour steady offered-load segment and a 24-hour model-dependency-outage/replay design. | The latter can first be accelerated by deterministic replay; accelerated replay is not a 24-hour uptime result. |
| Payload/spool allocation | 12 GiB durable native-payload budget; separate 20 GiB DB/metadata and 16 GiB derived/trial budgets. | At 50 × 2 KiB/s, 24 hours is about 8.24 GiB payload; 25% reserve gives about 10.3 GiB. This arithmetic is a sizing estimate, not a compression or DB-size measurement. |
| Retention | 24-hour rolling input availability in this development profile, plus explicitly pinned campaign/forecast evidence until review. | Production identity history and longer retention require a separate measured capacity profile. No two-year byte retention is promised by DEV1. |
| Small-record capture target | p99 durable receipt below 250 ms at the steady workload, measured with the chosen durability profile. | Proposed acceptance target. Include queueing/storage barriers and offered failures; do not claim based on in-memory acknowledgement. |
| Bounded reads | Default 100 records, hard cap 1,000 records or 8 MiB per result; dependency expansion at most 2 hops and 500 referents by default. | Return continuation/truncation and the omitted frontier. Explicit larger jobs use another reservation/profile. |
| LLM reasoning | One concurrent model call; initial inquiry ceiling 32k submitted text-equivalent input tokens, 4k requested output tokens per call, 4 calls and a 120-second wall limit per inquiry. | Reasoning usage, hidden/provider-metered usage, media and retries also count. If provider-supported output includes reasoning, budget must include it. Unsupported limits lead to rejection/profile revision, not silent overrun. |
| Hypothesis search | At most 3 rivals per local expansion, 2 revision rounds before yielding, 16 queued frontier items per inquiry. | Yield/defer with rationale; do not discard the broader unknown frontier. These prevent runaway recursive work and are tunable profile settings. |
| Numeric analysis | Initial supported model at most 100 numeric state variables, 10,000 discrete events, 32 ensemble members and 60 CPU-seconds per job. | Native solver work counters and memory limits remain required; simulated horizon and output count are also explicitly bounded in each ScenarioSpec. |
| Financial ceiling | A per-run price manifest and owner-approved spend cap must be bound before paid inference. Documentation tasks use zero inference spend. | Token ceilings are not a complete dollar budget. Defer execution if the spend policy is absent. |
| Recovery | Local process crash and restart with no acknowledged local commit loss under supported storage; restore target within 15 minutes for the pinned small campaign. | Proposed recovery target. Single-host DEV1 has no production HA claim or protection against permanent host/disk loss beyond verified backup. |

Source bindings and compact identity lineage can outlive payload retention under an explicit identity-history policy. That supports long-gap continuity where stable identifiers/evidence exist; it does not recover evicted evidence or prove physical continuity. A future two-year identity test uses simulated time gaps and retained associations, followed by a real retention/recovery qualification if that duration is promised.

Worker priorities protect native capture first, then required assessment/admission, then interpretation and discretionary inquiry within configured reservations. No DB transaction waits for a model or external tool. Full disk or source overload produces explicit rejected/deferred work and coverage gaps rather than silent dropping. Requested per-call budgets cannot exceed remaining global reservations.

## 3. Later HA profile and scale triggers

HA1 is a design target, not the initial deployment: an eligible-request availability SLO of 99.9% over 30 days, RPO 0 for acknowledged commits under one declared fault-domain loss, and recovery/failover target within 15 minutes. These require tests against a named topology and exact failure model. They do not imply zero loss of observations that never reached EDI.

Candidate topology: app workers across failure domains; appropriately fenced DB failover with a synchronous durability configuration; object-byte replication whose acknowledgement matches the claimed DB/manifest level; independent backups and coherent restore points. Claiming only Postgres replication while evidence bytes remain on one lost disk fails the gate. Network partitions need a declared writer/quorum policy; conflicting writable primaries are prohibited.

For the SLO denominator, count all eligible offered requests within the profile, including rejection, timeout and silence detected by an external probe. Publish freshness and recoverability separately from availability. DB, blob and model service dependencies have different effects: native intake may continue without reasoning, but cannot promise durable acknowledgement without its required persistence path.

Scale additions require a discriminator: graph projection when bounded authoritative queries miss latency targets; additional worker/shards when queue growth exceeds the profile at fixed hardware; a broker when measured DB outbox pressure justifies it; a workflow service when state-machine complexity and fault handling justify its operational cost. Requalify semantics and complete cost after each change. Unbounded global graph expansion is never a valid scale plan.

## 4. One prospective integrated campaign

Start with one small unfamiliar connected system with observable quantities, a delayed process, a saturated resource, competing mechanisms, actor-specific information and a changed boundary/interface. Pin the environment, generator, source/known-at schedule, random seeds, allowed interventions, observation tools and success criteria before candidate exposure. Keep an evaluator-only ground truth and a genuinely held-out continuation. This establishes the capability path before broad benchmarks.

The campaign exercises capture → interpretation → versioned representation → alternative mechanism proposal → bounded test/simulation → sealed prediction → new observation → assessment → justified revision/finding. Include a source reconnection, duplicate delivery, false identity candidate, late correction, model timeout, process crash and unsupported numerical relation in the same fixture. Engineering cases may share this campaign; their passing scope must remain explicit.

Subsequent comparisons must include the same selected LLM with (a) no persistent history / long context as applicable, (b) strong conventional RAG, (c) temporal graph memory such as Graphiti when qualified, and (d) an explicit structured-model baseline where useful. Give comparators the same allowed observations, tools, simulation functions, task goals and total budget; do not disable their strongest legitimate tools. Architecture gains cannot be credited to a larger model, hidden observations or extra experiments.

Use matched quality/cost frontiers: task success and prediction scores at fixed budget, or total cost to a predefined quality. Count context assembly, tokens, media, tools, failed calls, retries, embeddings, storage, model hosting and wall time. Measure electrical energy only with an actual measurement boundary; token savings are not energy measurements. Report tradeoffs if one method is more accurate but slower or more expensive.

For persistent learning/transfer, separate reused genuine history, reset memory, unrelated history and conventional-memory history under unfamiliar shifted systems. Use opaque relabelings and new mechanisms/parameter regimes to reduce narrative recall. Frozen old forecasts are scored even when later knowledge improves. Do not train or tune on held-out outcomes, repeat until superiority, or claim learned discovery from imported pretrained facts alone.

## 5. Proposed cases and acceptance

All rows below are specified, not run. Positive and counterexample variants are paired where possible. `TRACEABILITY.json` links cases to implementation requirements and source obligations; the interface catalogue links active operations to cases.

| ID | Case / method | Prospective acceptance |
| --- | --- | --- |
| E01 | Mixed native capture and duplicate payloads. | Text, image, waveform, structured numeric and an unknown composite retain byte hashes, order and distinct genuine occurrences; replayed notification does not duplicate an occurrence. |
| E02 | Restart between byte staging and metadata commit. | No false durable receipt, no missing acknowledged artifact, detectable/recoverable orphan or incomplete manifest, and no repeated committed occurrence. |
| E03 | Long-gap identity and source epoch reset. | Stable binding survives a simulated two-year interval; replacement/reset is explicit; ambiguous physical continuity remains unknown rather than silently merged. |
| E04 | Cross-modal false association and reversal. | Similar text/image candidates do not force a merge; split/correction preserves sources and invalidates dependent views. |
| E05 | Event versus structure and source dependence. | Direct structural inspection and reported event are represented on independent role/basis axes; rephrased copies remain one source lineage. |
| E06 | Temporal semantics, late arrival and actor visibility. | Known-at cuts exclude later reports; gaps and uncertain time persist; actors cannot use analyst-only or future information. |
| E07 | Units, ordinal values and conversions. | Incompatible dimensional equations are rejected; allowed conversions retain meaning; ordinal/unknown values are not silently treated as numeric or zero. |
| E08 | Composition and overlapping system views. | Shared referent/resource appears once in accounting; query boundaries and external input closure remain explicit. |
| E09 | Multi-input nonlinear law. | One joint mechanism with domain/rivals is retained; unsupported independent edge coefficients are not substituted. |
| E10 | Stock-flow accounting and shared constraints. | Transfers balance under declared conversions/losses and capacity is consumed once; conflicting simultaneous demand is resolved by the declared rule. |
| E11 | Delays, backlog and state carry-over. | Same visible stock with different pending commitments gives the appropriately different forecast; topology change preserves relevant backlog. |
| E12 | Loop closure, sign and changing dominance. | Open paths are not labeled complete loops; sign is conditional; saturated or dormant mechanisms do not retain an unsupported fixed gain. |
| E13 | Scope/interpretation and stakeholder criteria. | Causal scope, interests, qualitative concerns, local/wider horizons and disagreements remain distinct; no compulsory global utility is invented. |
| E14 | Rival mechanism and non-identifiability. | Several structures fitting present data remain alternatives; the system proposes a distinguishing observation or reports non-identifiability. |
| E15 | Curiosity against noisy novelty. | Test selection favors feasible useful discrimination over uninformative random noise; heuristic utility is not presented as calibrated information gain. |
| E16 | System-of-systems boundary expansion. | Consequential interface frontier is exposed one supported link at a time; omitted drivers and duplicate accounting are detected; resource ceilings cause explicit defer/truncation. |
| E17 | Restricted compilation and unsupported laws. | Invalid operators/references/units or missing backend capability fail before execution; a qualitative unknown does not generate a precise fabricated trajectory. |
| E18 | Numerical refinement and discontinuity. | Solutions stabilize under declared step/tolerance refinement, balance diagnostics and threshold-event fixtures; unsupported delay/DAE semantics are explicit. |
| E19 | Hybrid event and shared clock. | Event ties, continuous advancement, resource contention and pending updates follow one pinned policy without double application. |
| E20 | Prospective forecast seal and outcome correspondence. | Original model/cut/forecast/scoring rule is immutable; new independent outcomes match quantities/units/time; edited forecasts cannot replace old ones. |
| E21 | Synthetic evidence echo through a full loop. | Generated, summarized, exported and reimported simulation artifacts remain generated and cannot become independent corroboration. |
| E22 | Calibration, missing outcomes and uncertainty. | Missing/censored data remain explicit; numeric scores are only computed for declared suitable quantities; coverage claims state dependence/stationarity assumptions. |
| E23 | Error diagnosis and controlled revision. | Numerical, source, semantic, driver, parameter, rule and topology explanations remain distinguishable; revision records rationale and affected dependencies. |
| E24 | Repair and finite shared support. | Repair uses the same resource authority as competing work, takes time and can fail; stable output with eroding restorative capacity remains visible. |
| E25 | Real reorganization versus model correction. | Membership/rewiring history, actual-world evidence and model reinterpretation have different operation types and preserve state. |
| E26 | Bounded actor response and failed execution. | Intention uses perceived options; realized effects obey actual modeled capacity; no automatic optimal response or goal success is assumed. |
| E27 | Eight traps, leverage and adverse transitions. | Trap labels require mechanism evidence/rivals; interventions specify direction, adoption, time/resources, carry-over and wider/adverse consequences. |
| E28 | Policy monitoring, authority and standard integrity. | Fixed response, amendment proposal, adoption and analyst revision stay separate; refusal/defer is possible; old criteria cannot be silently weakened. |
| E29 | Action dispatch and uncertain completion. | Unauthorized dispatch is denied; idempotent reconciliation prevents duplicate permitted effects; a receipt remains distinct from observed effect. |
| E30 | Proactive strategic finding. | A configured internal finding carries novel decision relevance, mechanism/evidence chain, uncertainty, horizon and test suggestion; duplicates are suppressed without masking a material update. |
| E31 | Selective acquisition and bias. | Selection/exposure/cost lineage is preserved; unvisited or unavailable evidence is not treated as absent or as confirmation. |
| E32 | Schema/embedding migration and stale projection. | Incompatible versions are rejected or explicitly migrated; old/current views do not silently mix; authoritative cutoff queries bypass or expose stale indexes. |
| E33 | Retention and restore. | Tombstones and unavailable refs propagate; acknowledged data and forecasts restore with their histories at a declared coherent point. |
| E34 | Queue saturation and model outage. | Native intake stays within the declared capacity/spool profile; bounded reasoning yields; overload and freshness lag remain visible and counted. |
| E35 | Lease fencing, duplicate/reorder and concurrent revision. | A stale worker or stale base revision cannot overwrite a newer commit; unknown completion is reconciled and outputs remain idempotent. |
| E36 | Matched persistent-learning comparison. | Same base model, observations/tools and accounting; include reset, unrelated and conventional-memory controls; report all pinned outcomes without a predetermined winner. |
| E37 | Failure to fit or transfer under regime shift. | New operating point/parameters/rules/topology/input/measurement are challenged separately; unsupported transfer is withheld and failures remain logged. |
| E38 | Whole-path resource accounting. | Offered/admitted/failing work, all token/media/tool/retry costs and wall time reconcile; unknown usage is not zero; energy claims require instrumentation. |
| E39 | HA fault-domain and partition profile. | Only under an implemented HA1 topology: eligible request, durability, fencing, byte/reference consistency and failover results satisfy the pinned SLO/RPO/RTO and fault conditions. |
| E40 | Provider/backend replacement. | Alternate provider or engine respects the same record/status/permission semantics; a version or quality change reopens qualification rather than silently inheriting results. |

E39 is outside DEV1 runtime scope and blocks any later HA claim. E36/E37 are later scientific/transfer assessment gates, not prerequisites for approving a document or a small contract fixture. No suite count may be reported as successful model reasoning merely because JSON references validate.

## 6. Applying the two real-world stories

**Budworm/forest:** preserve tree, insect, predator, climate, spraying, logging and market observations with temporal provenance. Propose rival mechanisms for outbreak timing and persistence, including food availability, predator saturation, climate triggers, insecticide effects and selection/reporting changes. Keep local ecological behavior and logging supply criteria separate. Fit/test supported submodels; examine delayed propagation through timber demand and management incentives. If observations cannot identify predation or spray effects, request discriminating observations and retain alternatives. Do not hardcode Meadows' narrative as the generated model's answer or equate story comprehension with discovery.

**Visible electric meters:** distinguish meter location, installation history, household traits, tariff, building configuration, weather, appliance mix, occupancy, actual attention and energy use. Compare feedback-mediated behavior with pre-existing household preference, placement selection and other confounding. A lower-consumption group alone cannot identify the effect of visibility or hormones. Where permitted, randomized visibility/display interventions, crossover designs or defensible natural experiments can discriminate; account for period effects and carry-over. Simulate several behavior laws and sensitivity ranges, retaining unknown psychological structure. A simulation that reproduces one-third lower use is not itself causal identification.

These are development challenge families, not held-out proof of EDI. Truly unfamiliar continuations and alternate/no-effect mechanisms are needed to assess generalization.

## 7. Critical retrospective

| Review lens | Challenge | Resulting design decision |
| --- | --- | --- |
| First principles | Is a language explanation enough to reconstruct a world? | Separate evidence, represented mechanism, prediction and decision; retain unresolved structure. |
| KISS | Does each conceptual box need a service/model/database? | Eight logical owners in one application; one canonical transactional store, native artifacts and replaceable adapters; no service per Meadows term. |
| KISS | Must the MVP support every simulator and train a new neural model? | One supported quantitative backend plus honest qualitative/unsupported state first; specialist engines and learning are conditional. |
| Five Whys: persistence | Need continuity → sessions end → model context is finite → recoverable history is required → durable versioned state. | Persist evidence and admitted models outside the prompt; do not store all history in every call. This is rationale, not measured performance. |
| Five Whys: separate proposals | LLMs can be wrong → plausible mechanism can fit one event → alternatives can be observationally equivalent → new tests must discriminate → evidence admission must be independent of proposal generation. | C4 proposes, C5 tests models, C6 compares evidence, C3 admits; generated material stays tagged. |
| Five Whys: explicit time | Events arrive late → actors could not have known them → hindsight changes apparent decision quality → forecasts need an original cutoff → valid/known/commit times must be separate. | Pin knowledge cuts, actor-visible inputs and immutable original forecasts. |
| Requirements waterfall with return | Does every mechanism have a parent need and a verification case? | Trace mission/requirements/functions/contracts/cases both ways in machine-readable catalogues; case evidence returns to its original requirement. |
| MECE within axes | Are observation/inference, event/structure and current/past mutually exclusive categories? | Use independent role, basis, time, modeling-use and applicability axes; do not impose a false mutually exclusive ontology over modalities or causes. |
| Alternatives/counterexamples | Could ordinary memory or a strong LLM do as well? | Retain model-only, RAG, temporal-graph and structured-model controls with equal tools and accounting. Preference is not superiority. |
| Causal identifiability | Does every relationship become uniquely discoverable with more reasoning? | No. Preserve equivalence classes and unknowns; ask what extra observation/intervention would matter; allow non-identifiable output. |
| FMEA and capacity | Could correct modules still form a bad feedback loop? | Review shared dependencies, echo paths, temporal leaks, saturation, stale revisions and execution authority across the whole system. |

## 8. Failure modes and containment

The highest-risk trace was also inspected semantically: mission and audit/reproducibility needs → I7-R48 original expectations → IMP-R10/IMP-R26 → F60/F61 forecast sealing and independent comparison → C5-to-C6 forecast registration and C1-to-C6 outcome selection → E20/E21. The reverse return of an assessment is a recommendation, not a newly acquired observation. A simulation cannot pass this chain merely by being archived and re-read. The actor-time path (I7-R15/I7-R53 → IMP-R04/IMP-R11 → E06/E26) similarly keeps represented knowledge at decision time separate from later analyst knowledge. These are self-review judgments over proposed contracts; their runtime cases remain unrun.

| Mode / consequence | Detection | Containment and verification |
| --- | --- | --- |
| False physical-identity merge contaminates relationships. | Contradictory identifiers/time or negative evidence; dependency audit. | Reversible association, original-source retention and descendant invalidation; E03/E04/E23. |
| Model consensus or simulation becomes false corroboration. | Origin/common-source/derivation checks through full lineage. | Separate namespaces, independent outcome requirement, sealed forecasts; E05/E20/E21. |
| Hindsight leaks into actor decisions or forecasts. | Known-at cut and actor-mask checks. | Snapshot reads and separate clocks, reject unavailable-at-t input; E06/E20/E26. |
| Numerical artifact looks like a nonlinear regime change. | Tolerance/step refinement, balance checks, discontinuity/solver diagnostics. | Unsupported status, alternate method or qualified range; E17/E18/E19/E37. |
| Shared constraints or commitments counted twice. | Joint transfer ledger and resource invariants. | One referent/transfer authority across views, state carry-over; E08/E10/E11/E24. |
| Recursive inquiry saturates intake and memory. | Offered-work/backlog/spool and budget telemetry. | Bounded queues, reservations, yield/defer and protected intake; E15/E16/E34/E38. |
| Blob/DB mismatch or stale worker loses acknowledged state. | Manifest/hash/commit reconciliation and fencing errors. | Staged-commit protocol, idempotent recovery and coherent restore; E02/E33/E35. |
| Proposed policy/action bypasses legitimate authority. | Owner/policy/version and tool capability checks. | Separate proposal/adoption/dispatch/effect, research-mode denial; E28/E29. |
| Selection-driven learning misses disconfirming evidence. | Exposure/frontier/history and holdout diagnostics. | Rival tests, null mechanisms, unvisited-frontier reporting; E14/E31/E36. |
| Provider/library/license drift invalidates a prior claim. | Pin manifest, capability check and changed source/license review. | Rebind/requalify rather than inherit a pass; E32/E40. |

Severity is qualitative: evidence/authority/identity contamination is gate-blocking; measured probabilities and risk priority numbers are not available. The finite profile and fault model bound the claim.

## 9. Open implementation choices and exit criteria

| Item | Default recommendation | Must be resolved before |
| --- | --- | --- |
| Exact provider snapshot, access and price manifest | Sol first hosted; Qwen local path conditional. | Any model execution or claimed reproducibility/cost. |
| Python/package/OS compatibility, licensing and lock | Compatible isolated Python environment; Postgres/SQLAlchemy/Pydantic family; no assumption that Windows 3.14 supports all ML engines. | Concrete adapter contract and build. |
| Restricted mechanism grammar and numerical semantics | Small typed arithmetic/lookup/stock-flow subset, one SciPy backend. | C5 contract PASS. |
| Identity threshold/policy and calibration data | Stable explicit binding before probabilistic link; retain ambiguity. | Any automatic referent association claim. |
| Source-native envelope compatibility and complete JSON schemas | Map retained contracts into the new ports without silently deleting identity/time/availability semantics. | Cross-component contract PASS. |
| First use case, hardware and operating profile | One connected unfamiliar system and DEV1. | Runtime/capacity qualification. |
| Paid spend and external action policy | Absent/disabled in this documentation task. | Paid inference or external actuation, respectively. |
| Statistical/causal backend assumptions | Choose per question; no universal causal discovery algorithm. | Any numerical causal/uncertainty claim. |
| HA topology and actual restore/failover evidence | Later HA1, separate from single-host development. | Any production-availability/durability claim. |

These are bounded adoption conditions, not missing state owners or implicit magic components. A source/licensing assertion is restricted to the retrieved primary notice; exact software licenses and version compatibility are checked at dependency binding.

## 10. Capability-by-capability implementation order

1. Freeze a concrete record/identity/time contract and one source/meaning fixture; exercise it without inference.
2. Implement the smallest source-native capture → source-linked claim → versioned nine-family host path; include unsupported and ambiguous inputs.
3. Add one reasoning provider that proposes alternatives and tests, with no direct world-model writes.
4. Add one supported quantitative/qualitative analysis path with sealed prediction and genuinely later outcome comparison.
5. Add controlled revision, evidence-backed proactive findings and bounded cross-system exploration.
6. Integrate actor/policy/adoption semantics needed by the selected use case; keep actual actuation separately gated.
7. Run the one integrated campaign, then the matched comparison/transfer controls and qualified operational profiles.

Each increment must preserve the same evidence, identity, time, authority and cost spine. Do not implement all optional frameworks first. The next concrete development artifact is a typed contracts/fixtures package for the selected first capability, after the owner reviews this documented proposal.
