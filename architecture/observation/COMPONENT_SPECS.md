# Observation component specifications

Version 0.2; proposed contracts, not implemented components. IDs OBS-C1 to OBS-C4 and their specification allocations are authoritative in REQUIREMENTS.json. This document explains execution, state and limits. The four modules do not require four servers.

## Shared contract

Input: source bytes or exact typed payload, acquisition descriptor, optional source occurrence/sequence information, declared metadata and capacity profile. Output: receipt state; committed observation reference/cursor at an explicit durability level; optional derived/identity records; query results with provenance and projection watermark.

Core fields and profile coverage are in README.md and the archived v0.1 catalogue. Data shapes remain native. Scalar batches keep per-sample time/missingness; a compound record may have several origins and subjects through its part manifest and assertions. A zero-byte valid payload is distinguishable from no acquired content.

Errors are structured and retryable or terminal: unsupported-profile, malformed-envelope, integrity-mismatch, incomplete-input, capacity-exceeded, scope-denied, source-unavailable, unknown-commit-outcome, storage-unavailable, worker-budget-exceeded and stale-projection. Error reporting does not imply source loss is fully measurable.

Reference lifecycle: registered -> receiving -> staged -> committed -> indexed. Decode and identity status evolve independently after commit. Payload availability may later change under retention events. Receipt/staged is not a durable acknowledgement. No read silently substitutes a current view for a requested historical one.

Required API families: register_origin, ingest/append_chunk/finalize, commit_status, subscribe(cursor), get_record, read_payload(range), read_part(selector), resolve_identity(valid_at,known_at,policy), append/retract_assertion, request_acquisition, coverage, export/restore. This specifies behavior, not a mandatory network protocol or SDK.

## OBS-C1: intake and source adapters

Specifications: OBS-C1-S01 through OBS-C1-S06.

**Purpose:** accept heterogeneous streams without mandatory interpretation and preserve delivery continuity.

- Inputs: push/pull/file/stream connectors, registered descriptor snapshots, admission limits, supported acquisition requests.
- Outputs: chunked receipts to C2, source/epoch registration records, explicit gap/fault/acquisition events, supported acknowledgement states returned to the caller.
- State: bounded pending spool, retry-stable keys, per-source epoch/counters, descriptor cache, capability/configuration snapshots. Durable spool entries identify unacknowledged work, not an alternative committed-observation log.
- Normal path: validate outer contract and budgets; assign/reuse occurrence key; record observer time; append bounded payload chunks; pass metadata to C2; release spool only after the required acknowledgement or explicit abandoned-delivery event.
- Identity: deterministic scoped producer/channel lookup and dated reported attachment references; unknown original producer is valid behind a known deliverer. Never perform neural re-identification synchronously.
- Acquisition requests: require supported capability, target/settings/duration/budget and request ID. Record requested versus actual behavior, denial and unavailable status. Requests do not add a curiosity or external action policy here.
- Backpressure: per-source fair queues and explicit configured quotas. Do not silently sample or weaken durability. Non-pausable sources generate known/unknown loss records; source hardware overflow cannot be perfectly reconstructed without source counters.
- Failure handling: network retry reuses occurrence identity; counter reset starts a new epoch; source silence updates coverage only according to known heartbeat/sampling expectations. Unknown gaps remain unknown.
- Bounds: configured max chunk, pending bytes, source count, open files, spool disk, parser preflight, request rate and source fairness. No globally unbounded in-memory queue.
- Verification: mixed input, origin recurrence, clocks, overload, request outcomes and scope separation. Exact case links are in TRACEABILITY.md.

## OBS-C2: evidence commit, retention and recovery

Specifications: OBS-C2-S01 through OBS-C2-S06.

**Purpose:** define what was durably accepted and retain addressable native evidence.

- Inputs: C1 receipts/chunks and versioned C3 origin/schema references; worker outputs with parent references; registry/assertion/correction events.
- Outputs: immutable committed record/manifest IDs, authoritative log offsets, durable acknowledgement and outbox entries, availability/retention events and aggregate metrics.
- State: metadata transactions; payload objects/chunks; pending/committed upload manifests; idempotency scope/key/result; log/outbox and consumer checkpoints. Origin/schema/assertion data have authoritative records here even when C3 exposes their APIs.
- Commit: payload integrity and backend durability barrier precede the metadata/outbox transaction. Commit pins all required descriptor/profile versions. Full object acquisition and partial acquisition are distinguishable; a source can commit explicitly acquired partial bytes without falsely declaring a complete file.
- Query/retry: unknown commit outcomes are resolved by idempotency status. Native source IDs are qualified by issuer/channel/epoch; content hashes only support payload deduplication. Preserve distinct byte-identical observation occurrences.
- Replay: acquisition-order cursors are authoritative. Source/phenomenon-time replay is a separately requested view that may be incomplete or partially ordered.
- Retention: prevent deletion of referenced pending/committed material until policy and reconciliation allow it. Metadata/dependency retention is independently configurable. A tombstone states eviction/deletion and lost access; it does not pretend future raw replay remains possible.
- Recovery: reconcile staged payloads, metadata/outbox records, spool and consumer offsets; tolerate repeated effects through idempotency. Kill-process, OS crash, disk-full, interrupted writes and restore are separate qualification scenarios.
- Local backend candidate: transactional SQLite on a supported local filesystem with WAL, synchronous FULL, busy timeouts and monitored checkpoints, plus durable chunked files. This is a proposed low-operations prototype, not an established benchmark choice or HA claim. Validate real filesystem barriers and directory/object persistence; SQLite settings alone cannot make a separate payload durable.
- Replicated backend: qualify metadata and payload replication, acknowledgement policy, leader election/fencing, exact failover eligibility, split-brain prevention and restoration. PostgreSQL is a candidate metadata component; it does not by itself solve payload replication, fencing or end-to-end RPO.
- Bounds: per-transaction metadata, chunk/object size, in-flight bytes, disk reserve, commit units/s, bandwidth, checkpoint lag and recovery work. Chunk a large artifact; do not load it into RAM. Refuse admission before disk reserve is exhausted where possible.

## OBS-C3: identity, catalogue, read and replay

Specifications: OBS-C3-S01 through OBS-C3-S06.

**Purpose:** expose historical attribution and efficient access without changing acquired evidence.

- Inputs: committed C2 records, identity/alias/assertion decisions, source/profile registrations and bounded queries.
- Outputs: origin and subject associations with evidence/status, native/derived data references, paginated range results, export bundles, replay subscriptions and projection watermarks.
- State: generic entity-role registry; versioned aliases; valid-time and recorded-time assertions; schema/configuration descriptors; source/time/identity indexes. Indexes are rebuildable; authoritative registry/assertion data are durable C2 records.
- Two-year continuity: persistent subject/source reference and dated attachment evidence survive sessions. When only a new name or similar descriptor is supplied, return a candidate/unresolved result rather than force continuity. A new physical component at an old functional position receives a new physical reference.
- Assertion contract: ID, scoped endpoint references and selectors, relation/schema, valid interval or explicit unknown, recorded-at, basis/actor/method/version, evidence, state and supersession/retraction. Score meaning/calibration only when available.
- Conflict behavior: inferred candidates cannot merge accepted sets. Accepted operational links are policy-scoped and reversible. Disputed bridges disable dependent equivalence shortcuts until a versioned decision resolves them. Preserve source claims even when rejected by an operational policy. Do not silently follow global transitive same-as chains.
- Read consistency: return commit cursor plus index watermark. Exact committed-record access remains possible while projections lag. Identity resolution states known_at/valid_at/policy. A bounded rebuild can return stale/unresolved status, never invented current certainty.
- Efficient access: source/time range indexes and bounded pages; cursor rather than full-history serialization; typed/binary range reads; only requested regions/parts. Descriptor/fingerprint search is bounded by candidate count, time and scope and is not required for intake.
- Schema evolution: immutable core/profile versions, compatibility rules, unknown-extension preservation and archived descriptors. Physical table migrations are versioned operations with rollback/restore plans; no mutation of historical meanings.
- Bounds: page bytes, query time, open cursors, candidate count, assertion fanout, active rebuild work and per-scope service quotas. Return continuation/limit status when truncated. A small token budget must not silently delete contradictory evidence; return references and truncation status.

## OBS-C4: optional bounded derivation workers

Specifications: OBS-C4-S01 through OBS-C4-S06.

**Purpose:** make retained material easier to access while isolating variable-cost work.

- Inputs: committed source selectors and a versioned requested procedure/model plus resource budget.
- Outputs: decoded structures, selectors, features or association proposals, all as new records committed through C2. Worker failure remains a processing event; original intake remains usable.
- State: versioned jobs, leased work, retry limits, procedure/model identities and input digests; optional descriptor indexes with separate versions. Worker effects are idempotent on job/input/procedure identity, not on payload alone.
- Parsing: lazy extraction with depth/member-count/decompressed-byte/CPU/time limits. Preserve original container and supplied composition; don't eagerly expand every archive, document or video.
- Association: propose operational source/subject correspondence with explicit basis and alternatives. No automated promotion policy for natural cross-modal identity is qualified by this design. An external or future recognizer can submit assertions through the same contract.
- Model changes: new model/weights/preprocessing means a new derived view. Do not compare incompatible feature vectors silently. Regeneration is admitted against a budget and retains old lineage.
- Cost: no mandatory LLM invocation. Enabled feature/model workers expose actual inference/compute cost separately; do not report them as zero-cost observation.
- Isolation: worker CPU/RAM/disk/job queues are capped; excessive lag rejects/defers derived work while C1/C2 remain within their configured capacity. No network service per decoder is required.

## Cross-component invariants

1. No accepted durable acknowledgement points to unavailable required native payload under the declared fault model.
2. No received evidence is rewritten by a decoder or identity correction.
3. No provisional match silently becomes a physical identity fact.
4. No clock reset or source rename silently becomes physical continuity.
5. No unbounded query, queue, identity candidate scan or recursive extraction.
6. No zero-token claim includes optional model work unless it truly performed no model inference.
7. No local deployment is described as HA, and no replication claim omits its payload store/fault model.
8. No target or not-run verification is reported as a measured capability.
