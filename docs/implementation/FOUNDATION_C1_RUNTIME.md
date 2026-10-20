# Shared foundation and Observation C1: first implementation

Historical code 0.2.0 handoff: the subsequent [C3 increment](C3_WORLD_RUNTIME.md), code 0.3.0, implements the first world-hosting path while retaining this C1 scope/evidence record. C2 and C4-C7 remain unavailable. Earlier statements below describe the pinned first increment rather than newly qualifying C1.

20 October 2026. Code version 0.2.0. Source implementation, **unqualified**. Input architecture revision `0fd018e60373ca08551ebd7d57ac859dbc8b64fd`; [ADR-003](../decisions/ADR-003-local-observation-runtime.md) records the local backend binding. Structure-first direction is retained: no product tests, qualification, inference, training or benchmark campaign ran.

## 1. What is implemented

| Owner | Code | Delivered scope | Remaining scope |
| --- | --- | --- | --- |
| C0 | `src/edi/inquiry/runtime.py` | Composition, workspace/profile selection, C1 intake dispatch, bounded C1 admission and read-lane allocation | Persistent inquiry/jobs, leases/fences, reservations, scheduling and supported findings |
| C1 | `src/edi/observe/` | Source/epoch registry; native finite binary stream/file recording; one local transaction for chunks/metadata/retry result/replay log; status, bounded reads/replay, checkpoint, coverage and backup | Product qualification, network/live connectors, resumable uploads, retention/restore qualification, replicated backend and full F13 |
| C2-C7 | `interpret`, `world`, `reason`, `analyze`, `assess`, `agency` | Named owner modules, 24 function declarations, unavailable component/model/math ports | All processing implementations; calling a declared component raises component-unavailable |
| Shared | `src/edi/shared/` | Strict versioned value schemas, explicit errors/configuration, transport/proposal/value/growth records and replaceable dependency protocols | Full concrete world/admission/numerical grammar and future contract evolution |

The runtime capability list marks C0/C1 `implemented-unqualified`, with **partial scope** in their descriptions. It does not mean all eight functions are complete. No sixteen-service split is introduced for the reasoning subparts. No C4-C5 or C4-C7 execution bypass is introduced. C3 remains the sole future canonical admission owner.

Shared records include identity, known/unknown time, quantities, source-linked evidence, candidate assertions, commands/results, model patches/deltas, refinement bridges, knowledge requests and frontier snapshots. Proposal records are type shapes, not implementations of truth admission, unit checking, dependency maintenance, active curiosity or cross-scale conservation. No accepted-for-use assertion can be created through the current candidate-assertion type.

## 2. Requirement and function allocation

The original [OBS catalogue](../../architecture/observation/REQUIREMENTS.json), [implementation trace](TRACEABILITY.json) and [directed interface catalogue](INTERFACES.json) remain unchanged historical/proposed authorities. This table allocates this increment without changing their evidence statuses.

| Upstream obligations | Concrete mechanism | Functions | Status / future verification |
| --- | --- | --- | --- |
| OBS-R001, R002, R016 | Opaque binary streams and original file bytes; media type supplied, never guessed; no required model | F10/F11 | Implemented local finite-stream subset; heterogeneous fidelity cases not run |
| OBS-R003-R005, R022 | Stable workspace/namespace/native-source handle and immutable epoch descriptor; source/occurrence/content separate | F11 | Registered continuity only; subject association/correction C2/C3 pending |
| OBS-R006-R009 | Explicit unknown event/report time, receipt/commit times, source sequence, provenance/lineage and opaque profiles | F10/F11 | Recorded as supplied; no truth or causal inference; detailed temporal/compound cases pending |
| OBS-R010-R014 | Transaction, scoped retry key, hash/count checks, durable log, quotas and explicit errors | F11/F13 | Implemented source path; crash/retry/overload evidence not run; losses unknown unless supplied |
| OBS-R015-R019 | Local capacity profile, bounded pages/ranges, replaceable store port | F12/F13 | Bounds configured; latency, throughput, energy, HA and horizontal scaling unmeasured/unimplemented |
| OBS-R020-R027 | Retain-only policy, exact schema rejection, trusted local scope, origin classes, read-lane restrictions | F11-F13 | Partial; retention events, dependency-aware eviction, authentication/authorization service and minor-version compatibility pending |
| DOWN-001-DOWN-008 | Evidence reader, hashes/manifests, origin lookup, frozen replay cursor, explicit unknowns and C3 boundary | F12 | Consumer-facing contract subset only; downstream implementations/integration cases not run |
| IMP-R01-R03, R09, R19-R21, R23, R26, R30, R32 | Existing C1 lane allocation; typed SDK, no model admission/external access grants | F10-F13 | Partial implementation; source review is not case evidence |

The broader 34 IMP requirements and 48 cases are not all satisfied by this increment. Observation O1/O2 have concrete schemas/source code now; their original contract/runtime acceptance gates remain open. O3/O4 are not run. Restore is limited to opening an offline backup as a new store path; no destructive restore endpoint is installed.

## 3. Data and persistence contract

An origin is scoped by workspace and `(namespace, native_source_id)`; each epoch has a separately immutable descriptor. Re-registering the same descriptor returns its original IDs. A changed descriptor with the same source/epoch conflicts; a new epoch reuses the registered source handle. A replacement requiring a distinct referent must use a distinct native source handle. Registration records a reported/configured binding, not proof of physical sameness. An authenticated binding requires an evidence reference, whose authenticity is not automatically checked by this local adapter.

One observation retains the eight earlier logical envelope fields: schema_ref, record_id, scope_id, kind, receipt_time, origin_ref, manifest_ref and profiles. Typed extensions carry the capture declaration, manifest, source_id, commit position and committed_at. `schema_version` is the implementation contract version. Scope is supplied by the database-bound profile rather than trusted from incoming payload bytes. Origin_class defaults to unknown; external/generated/simulation are supplied provenance declarations, not automatic independence certification.

Original content is a binary stream, including zero bytes. File encodings, numeric precision, masks, schemas, composite layouts, calibration, packet timing and selectors remain in original bytes and optional supplied profiles. The sample CSV preserves `0001.2300` and missing cells as bytes; it does not parse them into quantities. Unknown critical profiles are stored opaquely and remain unprocessed. No decoder, composition validator or recursive archive expansion runs at intake. A URL in a file is preserved text, not fetched content.

Storage tables: workspace/accounting row; source handles; epoch/origin snapshots; immutable observations/replay log; payload chunks; consumer checkpoints. Only C1 adapter code writes them. The observation log IS the outbox source: every committed occurrence has a commit position, even if no consumer is running. There is no separate asynchronous notification side effect to lose. A transaction commits all required metadata, chunks, accounting and log position or none. Chunk hashes and the aggregate SHA-256 are retained. Separate retry keys with identical bytes still commit separate occurrences; no cross-occurrence deduplication is attempted.

Local SQLite is configured for WAL and synchronous FULL. The acknowledgement label is `local-sqlite-full-unqualified`; it does not establish physical-disk barriers, replica persistence, HA, backup safety or RPO/RTO. committed_at is an observer timestamp prepared immediately before the commit call, not a hardware acknowledgement timestamp. First durable knowledge is represented by committed log membership; event/report time remains separate. No throughput/latency number is claimed.

## 4. Operations and recovery semantics

| Operation | State/authority | Result and failure semantics |
| --- | --- | --- |
| register_origin | C0/trusted local intake -> C1 | Persist immutable descriptor, or return existing; conflicts never overwrite history |
| ingest | Trusted finite stream/file -> C1 | Check metadata/bounds, origin, byte count/hash, and commit transaction; receipt only after COMMIT |
| commit_status | Read C1 by origin + retry key | committed with original ID/position, or not-found at that read; an in-progress caller may still commit later |
| get_record / get_origin | C1 read surface | Exact stored snapshot or not-found; no replacement by an inferred current interpretation |
| replay | C1 -> permitted downstream read lane | Acquisition/commit-position order, bounded records, fixed watermark and continuation cursor |
| read_payload | Permitted payload-read lane | Bounded byte range, verify every touched chunk; incomplete/corrupt range is integrity-mismatch |
| checkpoint | Trusted consumer/local control -> C1 | Durable monotonic progress, within committed history; must follow consumer's own durable effects |
| coverage | Local accounting | Committed count/bytes/origins/watermark; unknown upstream loss; no silent heartbeat inference |
| backup | Trusted local operator -> C1 adapter | SQLite online backup to an exclusively new path, including native chunks; failures can leave an incomplete destination |

Replay cursors bind workspace, origin filter, last position and snapshot watermark. Concurrent later commits do not alter that snapshot. After exhausting it, a consumer can get `coverage().watermark` and construct a new ReplayCursor using its prior final `after` and the new watermark. No source-time order is implied; late records enter at their later commit position with original declared times. A saved checkpoint is a local cursor, not proof of downstream processing. Consumers must deduplicate by occurrence ID and persist their effects before advancing it. No atomic C1/C3 transaction is claimed.

Retry scope is `(workspace database, origin_ref, idempotency_key)`. The fingerprint combines the canonical capture declaration and payload SHA-256. Repeating exactly the same request returns the original receipt; changing metadata or bytes under the same key conflicts. Generated receipt/commit timestamps are excluded from the fingerprint. To recover a lost acknowledgement, query status first. Full retry validation rereads the finite input under the configured byte/chunk/deadline limits.

Before commit, an input/storage error rolls back provisional chunks and metadata. A failed commit acknowledgement reports unknown-commit-outcome and requires status resolution. Raw SQLite errors are structured storage-unavailable results; no hidden retry loop or silent downgrade. A not-found status is a point-in-time read, not cancellation of concurrent work. SQLite journal recovery is relied on but not crash-qualified here. Source loss before acquisition, partial streams without an expected length, and undetected source misreporting remain unknown.

## 5. Directed interfaces and authority

| Requesting owner | Prepared C1 read operations | Existing catalogue lanes | Remaining endpoint work |
| --- | --- | --- | --- |
| C0 | select records/origin, status, coverage | IF-01A/B | Acquisition connectors/standing grants and durable orchestration |
| C2 | select records/origin, payload range, returned coverage | IF-08A/B | Interpretation worker and durable consumer progress |
| C3 | select records/origin, status | IF-09A/B | Evidence admission validation; payload read denied on this lane |
| C4 | select records/origin, payload range, coverage | IF-10A/B | Reasoning/inquiry implementation |
| C5 | select records/origin, payload range | IF-11A/B | Analysis and source correspondence |
| C6 | select records/origin, payload range, coverage | IF-12A/B | Independent outcome comparison |
| C7 | select records/origin | IF-13A/B | Attributed ingest_report protocol; payload read denied on this lane |

`Runtime.reader_for(owner)` returns an operation-restricted read facade. It exposes no register, ingest, checkpoint, SQL or model-revision method. Unexpected operations are scope-denied. `Runtime.observation` is the TRUSTED LOCAL administrative SDK used by CLI; it is not granted to downstream owners. A caller-supplied owner string is not authentication. Process introspection is not a security boundary. Any future remote/multi-tenant API must bind caller authority outside this SDK.

All 28 pairs/56 directed lanes retain their design disposition; [source-review allocation](evidence/foundation-c1-source-review.json) identifies the 14 C1 directions prepared in part and the remaining 42 lanes as design-only. Prepared facades do not mean live C2-C7 endpoints. No new lane is introduced. C7 cannot ingest actions as independent external truth; the future ingest_report adapter must enforce its generated lineage. No shared graph, external tool loop, trained model or simulation feeds back into native evidence automatically.

## 6. Finite resource profile

Default local limits: 1 MiB storage/read chunks, 64 MiB per occurrence, 4,096 chunks per occurrence, 64 KiB serialized metadata per stored/request record, one million occurrences, 10,000 origin snapshots, 1,000 consumer cursors and 4 GiB retained payload bytes. SQLite metadata/indexes/WAL/backups are additional disk use. 256 MiB free-disk reserve is checked on new origin/payload writes. These defaults are engineering choices, not measured capacity targets.

At most four operations enter one ObservationService instance; excess calls fail immediately and retryably. SQLite serializes writers with a five-second lock timeout. No in-memory unbounded queue is created. Ingest checks a 30-second cooperative deadline and per-record quotas while reading chunks. Readers return at most 100 metadata records or a 4 MiB byte range per call; the SQLite page cache is configured to approximately 8 MiB per connection. Python/OS/cache overhead and metadata allocations mean these settings do not prove a total-RAM SLO.

The SDK accepts trusted finite **blocking** binary streams honoring read(size); it cannot interrupt arbitrary blocking read implementations, database/fsync calls or OS I/O. The deadline is cooperative, not hard real-time. Continuous input currently means repeated bounded occurrences/segments; no daemon, fair multi-source spool, nonpausable sensor handling or network backpressure protocol is implemented. Registry/consumer/record/payload limits and disk failures are explicit refusal, not sampling/eviction. Multi-process callers have separate admission semaphores and share SQLite writer contention. Backup has a five-minute cooperative progress deadline and checks free-disk reserve; its full copy cost is outside the low-latency intake path. CLI configuration/spec/cursor files are trusted local operator inputs; no hostile-input preparse sandbox is supplied.

Schema `1.0` is exact and extra outer fields are rejected. Future optional data must use bounded profile namespaces. Unknown future outer major/minor versions are not accepted yet. DB schema user_version=1 rejects unknown versions and nonempty unrecognized databases; migration tooling remains open. Local quotas may be changed in configuration, but raising them does not qualify a larger workload.

## 7. Local use

From the repository, create an isolated environment and install the package when desired:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m edi --config examples/observation/local-profile.json register-origin examples/observation/origin.json
```

Copy `capture.template.json` to `.local/capture.json`, replace origin_ref with the registration result, then:

```powershell
.venv\Scripts\python -m edi --config examples/observation/local-profile.json ingest .local/capture.json examples/observation/native.csv
.venv\Scripts\python -m edi --config examples/observation/local-profile.json replay --limit 10
.venv\Scripts\python -m edi --config examples/observation/local-profile.json coverage
```

Use `get RECORD_ID`, `origin ORIGIN_REF`, `status ORIGIN_REF RETRY_KEY`, `read RECORD_ID NEW_OUTPUT_FILE --offset 0 --length 4096`, `checkpoint CONSUMER --position N` and `backup NEW_DATABASE_PATH` for the other operations. Control/results are JSON; payloads are written as bytes to an exclusively new file. Save a returned cursor object, not the entire page, for `replay --cursor CURSOR_JSON`. All commands must use the same workspace/database profile. Backups can be opened as a new database path with the same workspace after ensuring the backup finished and no process is writing it. Do not copy only an active SQLite main file while ignoring its WAL.

The examples are handoff assets, not executed test evidence. No dependency installation was performed in this development turn; the existing Pydantic installation was used only for imports.

## 8. Retrospective and evidence

KISS: one package, one native byte path, one commit authority, one transactional store and one replay/outbox log. No parser/model/broker/graph service is mandatory. Five Whys: long-gap continuity requires persisted handles; reliable retry requires separate delivery/content identities; reconstructable evidence requires original bytes; honest receipts require atomic required state; finite resources require admission/refusal. These are design rationales, not experimental causal findings.

MECE axes remain separate: source identity, occurrence identity, content hash; supplied event/report versus observer receipt/commit times; evidence origin versus completeness versus interpretation state. Generated evidence is not an independent observation merely because it passed C1. Requirements cascade into the table above; future case results must trace back up rather than be inferred from source code existence.

Self-review repaired an initially overbroad downstream reader by restricting operations per existing C1 lane. The schema retains source/epoch history; no semantic identity merge occurs. Payload range reads verify chunk integrity. The adapter avoids a separate-file commit gap. Remaining risks include real disk/barrier behavior, blocking inputs, one-writer contention, source misattribution, future retention semantics, schema evolution and downstream commit ordering. Each remains an open qualification/integration obligation.

Executed: Python AST syntax parsing, application imports and CLI parser construction only; the runtime was not instantiated. Environment: Python 3.14.0 / SQLite 3.50.4 / Pydantic 2.12.5. No recording/replay example, product test, crash/recovery case, performance benchmark, model inference, training or scientific comparison ran. Historical checks are unchanged and do not qualify this source implementation. No architecture/contract/runtime/integration PASS is issued for this increment.

Next component: implement the minimal C3 hosting/admission/versioned-read skeleton against EvidenceAccess, then C2 derivation, before C4 reasoning. Qualification can be resumed separately under the owner's chosen sequence; its deferred status must remain visible.
