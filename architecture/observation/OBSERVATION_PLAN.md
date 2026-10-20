# EDI MVP observation plan

Version: 0.1. Date: 19 October 2026, Asia/Kolkata. Architecture baseline: observation v0.2. Architecture self-review: PASS for implementation planning. Concrete contract gate: pending. Runtime and integration qualification: NOT RUN. This document consolidates the discussion and reviewed design; it does not claim that the layer has been built.

## 1. Purpose and authoritative references

Build a continuously operating observation layer that receives heterogeneous source-native information, preserves acquired evidence and context, maintains revisable operational identity across years and modalities, and exposes bounded, addressable access to later EDI components.

The intended EDI mission is broader: observe with or without an external goal, develop endogenous representations and relationships under declared assumptions, investigate uncertainty, consolidate revisable knowledge, predict, transfer and interpret useful findings. Observe supplies evidence and operational attribution. It does not fulfill the later learning/intelligence capabilities by recording data.

Use this plan as the planning entry point. Keep detailed requirements in [REQUIREMENTS.json](REQUIREMENTS.json), their readable view in [REQUIREMENTS.md](REQUIREMENTS.md), allocation in [TRACEABILITY.md](TRACEABILITY.md), contracts in [COMPONENT_SPECS.md](COMPONENT_SPECS.md), rationale in [REVIEW.md](REVIEW.md), operating targets/checks in [VERIFICATION.md](VERIFICATION.md), and topology/envelope in [README.md](README.md). If they disagree, flag and resolve the conflict; do not silently choose the convenient version. The requirement catalogue remains the authority for IDs and requirement status. Update this plan when its selected decisions or gate status changes.

The reviewed repository baseline is `ceacd5cb5bab9bde76ed79c574ac5cf0124f3309` on `architecture/observation-review-20261019`, private PR #228. Inspect the current branch/PR/main before resuming; a chat summary or this revision pointer cannot prove the latest status. Preserve [v0.1](archive/OBSERVATION_DESIGN_v0_1.md) as history. v0.2 supersedes its twelve-field core and nine-responsibility deployment suggestion where they differ.

## 2. Fundamental distinctions retained from the discussion

- Receiving training information is observation too. Training adds a procedure for changing the model; observation alone does not distinguish EDI from an LLM.
- Acquiring a signal, decoding it, interpreting it and learning from it are separate activities that may run concurrently. The observation contract must remain useful before interpretation succeeds.
- Source-native means the bytes/values actually supplied. A received JPEG is already compressed relative to physical light; retaining it exactly does not recover unrecorded physical information.
- Semantic neutrality means no mandatory domain ontology, object vocabulary or causal explanation is inserted as established understanding. Sensors, sampling, coordinates, architecture and objectives still introduce assumptions.
- A reported statement, prediction, artwork or simulation is observed as received material. Its content is not automatically a verified fact about the world.

## 3. Requirements flowdown

Follow mission -> system requirement -> capability/layer requirement -> function -> component specification -> verification case -> evidence. Current allocation includes 16 system requirements, 27 observation requirements, six functions, four modules, 24 component specifications, 24 planned product cases and eight future-consumer obligations. Counts describe the reviewed baseline, not achieved capability; the catalogue supplies current details.

| Requirement group | Observation obligations | Reason |
| --- | --- | --- |
| OBS-R001–R002 | Continuous heterogeneous intake and native fidelity | Later questions may need distinctions omitted by preprocessing |
| OBS-R003–R005, R022 | Source/subject continuity, dated correction, uncertainty/conflict | One component can recur across sessions/modalities while names and attachments change |
| OBS-R006–R009 | Time/order, provenance, composition and unknown states | Mixed inputs must retain context without fabricated certainty |
| OBS-R010–R014 | Commit, retry, recovery, bounds and coverage | Acquired evidence must survive admitted failures and expose losses |
| OBS-R015–R019 | Measured latency/capacity, inference independence, bounded access, HA and expansion | Efficiency and scale need explicit workloads and fault models |
| OBS-R020–R027 | Retention/dependencies, schemas, controls, isolation, accounting, policy and view versions | Multi-year interpretation and replay require more than stored payloads |

This table groups obligations for reading; it is not an exclusive partition. Detailed links remain in TRACEABILITY.md.

## 4. Information coverage

Support extensible structures: arbitrary bytes; exact scalars/arrays; events/sequences; trees/graphs; and nested compositions. Use modality profiles as access contracts, not an exhaustive closed vocabulary of things EDI must already recognize.

| Input family | Native material to preserve |
| --- | --- |
| Text, symbols, equations, code | Original encoding, spans, supplied syntax/layout |
| Numbers, tables, spreadsheets | Precision, types, formulas versus cached values, masks, keys and units as supplied |
| Pixels, photographs, artwork, scans | Original raster encoding, dimensions, channels, color/bit depth |
| Vector art, diagrams, maps, charts and graphs | Supplied layers, coordinates, paths, nodes/edges and source data; raster-only when that is what arrived |
| Audio, music, speech, environmental signals | Waveform, channels, sampling/codec and timing |
| Notes, MIDI, MusicXML and scores | Supplied symbolic events, voices, timing, controllers; score scans remain images until interpreted |
| Video, animation, screen and immersive material | Frames/packets, tracks, captions, timing, geometry and composition |
| Geometry and scientific arrays | Point clouds, CAD, meshes, volumes, spectra, fields, dimensions and reference frames |
| Physical/transduced measurements | Instrument-native readings, calibration, sensitivity, ranges and detection limits when known |
| Events, software/UI state, API/tool output | Epoch/sequence, snapshots versus changes, request/response and execution context |
| Documents, reports and supplied knowledge | Container/pages/embedded parts, author/reporter and declared generation method |
| Unknown, encrypted and compound material | Admitted bytes, completeness and access status, original container and per-part links |

A future format can be retained before a decoder exists. A URL alone is a reference until materialized. Available transducers and finite capacity bound physically capturable input. Do not claim understanding from storage or claim that unsupported/evicted material remains retrievable.

## 5. Identity over two years and across modalities

Distinguish deliverer, producer, channel, session/epoch, observed subject, functional position, artifact/revision and observation occurrence. Use generic opaque references with role metadata rather than require semantic object classes.

Persist identity/alias/assertion history independently of chat/model context. A binding records its endpoints/selectors, relation, valid interval, recorded-at, actor/method/version, supporting evidence, status and retraction/supersession. Confidence is optional with explicit meaning and calibration, not an invented universal probability.

For the owner's example, initial information about component E17 can be linked to later information after two years when supported scoped identifiers, dated attachment/provenance or recognition evidence establish continuity. A new producer can observe the same subject; the old producer can move to another subject. Similar appearance, simultaneous arrival, a reused station name or identical bytes alone do not establish sameness.

Support multiple subjects per record and region/span/part-specific bindings. Retain candidates and unresolved identity when evidence is insufficient. A replacement receives a new physical identity plus a dated position/replacement relation. Corrections preserve original occurrences and allow as-known-then and current-association queries. Avoid creating a purported physical entity merely because one packet arrived.

Learned cross-modal matching is optional asynchronous proposal work. No natural-data automatic acceptance algorithm or recognition accuracy has been qualified. Observation owns the operational ledger and declared association policy, not an unsupported promise to recognize every returning element.

## 6. Selected architecture

| Module | Responsibilities | Mandatory model inference |
| --- | --- | --- |
| OBS-C1 intake | Source adapters/registration, bounded spool, epochs, admission, supported acquisition controls | None |
| OBS-C2 evidence | Native chunks/manifests, authoritative commit/log/outbox, durable acknowledgement, retention/recovery | None |
| OBS-C3 attribution/access | Persistent identity/assertions, catalogue/schemas, bounded queries, watermarks, replay | None for registered identity and ordinary reads |
| OBS-C4 workers | Optional lazy decoding, selectors, features and matching proposals with separate budgets | Only if explicitly enabled for a justified job |

C1–C3 can share one core process initially. Isolate C4 resource consumption. Do not deploy a service per logical responsibility, a JSON envelope per pixel, or a synchronous model per observation.

Use one evidence commit authority: stage and qualify native payload durability; atomically commit its required metadata, manifest, idempotency result, log offset and outbox; then acknowledge the requested supported durable level. Reconcile failures and retry with stable occurrence identity. The spool holds unacknowledged delivery, not a competing committed history. Indexes and workers consume committed records independently and expose lag.

The local filesystem/object backend's actual barriers require qualification. SQLite FULL/WAL is a local candidate, not proof of end-to-end payload durability or HA. Replicated metadata, payload protection, fencing and correct failover eligibility must all satisfy the HA profile before its acknowledgement is offered.

## 7. Envelope and extensibility

Eight required logical fields: schema_ref, record_id, scope_id, kind, receipt_time, origin_ref, manifest_ref and profiles. The shared origin descriptor carries deliverer/producer/channel/epoch/adapter/configuration and explicit unknown origin. Conditional lineage retains record-specific inputs and transformations; it has not been removed for brevity.

Begin with time/order, exact values/layout, composition/selectors, quality/coverage and lineage/declared-origin profiles. Add sensor-specific calibration, coordinates or codecs only when applicable. Preserve unknown optional extensions; retain but do not interpret unknown critical profiles. Keep versioned descriptor dependencies as long as their retained data needs them.

The full v0.1 metadata catalogue and its keep/move/optional rationale are preserved in archive/REVIEW. It is a coverage checklist, not mandatory per-record verbosity. Cache shared descriptors, batch native samples while preserving times/masks, use binary/range transfer, and decode parts lazily. Eight fields are a logical simplification; benchmark whether actual encoding/cache overhead improves.

## 8. Review rationale and limits

Completed retrospective: KISS for every original field/group; consequential Five Whys; requirements waterfall with verification return path; scoped MECE axes; alternatives, rival hypotheses, failure modes and analytical capacity estimates. These methods justify and challenge decisions but are not empirical proof. The review was self-review by the proposing assistant, not independent scientific validation.

Retained decisions: native evidence plus derived views; persistent reversible identity; one commit authority; bounded asynchronous processing; source-specific optional metadata; explicit capacity/fault profiles. Deferred: a universal encoder, mandatory domain ontology, graph database, broker cluster, natural cross-modal auto-accept policy and unnecessary service splits.

Design risks still requiring evidence: false identity merges; missing or misreported sensor data; payload/metadata commit inconsistency; stale projections; parser amplification; descriptor/model drift; cold historical retrieval; overload; lost schema/calibration/key dependencies; replication/failover errors; and downstream token/cost effects.

## 9. Proposed operating targets

Targets are engineering proposals, not user-supplied numerical commitments or measured achievements. Freeze actual source mix, hardware/backend/configuration and fault model before qualification.

- P0 local reference: 4 CPU cores, 8 GiB host RAM, documented local SSD durability; up to 1,000 commit units/s AND 20 MiB/s aggregate; small units <=4 KiB and bulk chunks <=1 MiB. Small-unit durable-local acknowledgement target p95 <=50 ms and p99 <=100 ms under the specified read/worker mix.
- Bound core resident memory to 1 GiB and configured workers to 1 GiB extra. A 30-GiB spool with 25% reserve targets 15 minutes at 20 MiB/s; outages that destroy the spool are different failures.
- P0 process recovery target <=60 s with no acknowledged loss under its qualified intact-disk fault model. It is not a host-failover HA commitment. Total-loss backup/restore targets and dependencies are separately specified.
- P1 replicated proposal: 99.9% service target over rolling 30 days, p99 small-unit replicated acknowledgement <=250 ms in a pinned same-region topology, <=60 s failover and RPO 0 for records acknowledged at replicated level under one declared fault-domain loss. Backend/topology remain pending; do not silently downgrade acknowledgement during a partition.
- Require zero model calls/tokens on mandatory recording, registered-identity and ordinary replay paths. Count optional model work separately. Overall token, compute or energy advantage requires matched end-to-end measurements.
- Continuous 20 MiB/s produces about 1.65 TiB/day before replicas/indexes; retention is a major capacity choice. Qualify expansion under a fixed workload rather than promise literally unlimited scale.

## 10. Incremental execution plan

| Increment | Deliverable | Acceptance / evidence | Current status |
| --- | --- | --- | --- |
| O0 mission/design review | Consolidated requirements, rationale, architecture, component specs, future contracts | Coherent allocated design and passing document checks; explicit limits | Complete; architecture self-review PASS |
| O1 concrete contracts | Envelope/profile/origin/assertion schemas, APIs, errors, state machine, workload/backend choices and fixtures | Versioned examples validate; no ambiguous commit/identity ownership; scoped contract review | Pending |
| O2 smallest integrated path | Intake -> native durable commit -> registered identity -> bounded replay, with restore | Mixed recording survives exact-value, idempotency, clock/late-arrival, long-gap and replacement cases | Not implemented |
| O3 local qualification | Pinned P0 workload, recovery/overload/resource instrumentation and bounded worker path | Relevant OBS-V cases pass with complete failure/outcome accounting | Not run |
| O4 replicated qualification | Actual P1 metadata/payload topology and operational controls when deployment is authorized | Failover, partition/fencing, durability and observation-window evidence under declared faults | Not run; no deployment started |
| O5 consumer handoff | One downstream component consumes the qualified observation interface | DOWN-001–DOWN-008 respected and integration evidence recorded | Future |

Do not start a reasoning benchmark or design all later layers merely because this plan exists. Deliver one complete authorized increment at a time. P0 qualification cannot close the deferred P1 requirement. No contract/schema/runtime gate is passed by the architecture verdict alone.

## 11. Verification record

Use one integrated mixed recording/replay campaign containing numerical channels, image/video, audio, symbolic/document material, native graph/diagram structure and a compound/unknown-profile case. Include source and subject replacement, deliberately ambiguous identities, clock/sequence reset, two-year-late arrival, duplicate delivery, crash boundaries, overload, retention/restore and view/schema change.

The 24 product cases OBS-V001–OBS-V024 are defined in REQUIREMENTS.json and VERIFICATION.md. All remain not_run. Deterministic fixture identity correctness does not establish natural-world matching accuracy; that needs held-out labeled evidence, false-merge/false-split/abstention reporting and a qualified acceptance policy. Advancing a synthetic clock does not prove two years of uptime.

Already executed: document graph/generated-view/relative-link checks and six rejected invalid-graph examples. They found and corrected a retry/recovery function allocation gap. These checks establish documentation consistency only; they do not verify EDI runtime behavior or comparative advantage.

The scoped [architecture review report](evidence/ARCHITECTURE_REVIEW.json) records the architecture PASS, reviewer independence, future gate blockers and NOT RUN product qualification. Its consistency check is separate from product verification.

## 12. Repeat the process across the MVP

Use [the EDI component-review skill](../../.agents/skills/edi-component-review/SKILL.md) for every new or materially revised EDI component architecture. Invoke it explicitly as `$edi-component-review`, or follow the repository AGENTS routing rule. This is a repository-scoped skill; do not assume it is installed globally in unrelated workspaces.

| Capability | Current design allocation |
| --- | --- |
| Observe/attribute | This plan and reviewed v0.2 baseline |
| Form representations | Future component review; consume observation guarantees and unknowns |
| Recognize uncertainty/surprise | Preserve observation uncertainty; future inference mechanisms |
| Form competing explanations | Future relationship/discovery component |
| Predict and explore what-if | Future prediction/simulation component |
| Investigate | Observation acquisition interface plus future inquiry policy |
| Test and revise | Operational association correction plus future belief revision |
| Consolidate persistent knowledge | Evidence interface plus future memory/consolidation component |
| Transfer | Future controlled transfer evaluation |
| Interpret/report/act | Future interpretation, proactive findings and action-policy components |

Reuse the review method, IDs and evidence distinctions. Do not impose Observe's topology, eight fields or zero-model intake rule on components whose purpose requires learned computation.

## 13. Future skill contributions and change control

Apply additional skills only to a specific question: interface correctness, data integrity, identity, distributed durability, performance or scientific qualification. Record skill name/version, input revision, finding, affected IDs, accepted/rejected change, verification consequence and resulting gate. Preserve prior conclusions so another review can disagree transparently.

Reopen review when requirements, source types, authority, identity policy, schema, backend/model version, workload, retention, fault model or observed failure materially changes. Repair justified in-scope gaps and rerun affected checks. Do not repeat whole-design reviews without new evidence or relax thresholds to obtain a pass.

Next action: complete O1 concrete contracts and fixtures, then implement O2. No inference comparison or paid deployment is authorized by this document.

## 14. Proposed substrate consumer integration

The [OBS/SUB integration plan](../integration/OBSERVATION_SUBSTRATE.md) allocates DOWN-001 through DOWN-008 and eleven proposed logical contract families. Native evidence enters SUB admission before representation commit; consumer progress follows durable substrate state/checkpoint consistency. Retention/tombstones are explicit; no external evidence pin endpoint is assumed. C4 request and progress/session bindings remain concrete-contract work. This integration proposal does not change the observation architecture review scope or qualify its O1 contracts/runtime cases.
