# C2 interpretation and correspondence: first local implementation

20 October 2026 UTC. Code **0.4.0**. Input source revision `c43b8d5942b154e7849226208dd82f9d7736ca91`. Status: partial source implementation, **unqualified**. [ADR-005](../decisions/ADR-005-attributed-interpretation.md), [runtime trace](C2_RUNTIME_TRACE.json) and [source review](evidence/c2-source-review.json) record scope and remaining work.

## 1. C3 prerequisite assessment

The owner requested C2 if C3 meets the aligned specification. **Complete C3 requirement satisfaction has NOT been established.** The sixteen SUB obligations and C3 contract/runtime/integration gates remain open as recorded in [C3_WORLD_RUNTIME.md](C3_WORLD_RUNTIME.md). This increment proceeds against the already specified local IF-09/14 interface subset under the earlier structure-first/no-qualification direction; it does not turn that subset into full C3 acceptance.

Manually reviewed C3's strict candidate puts, proposer restrictions, reference/version validation, scoped evidence hashes/provenance/selectors, atomic commits and idempotent request results against C2's intended use. Added explicit checks that returned C1 metadata has the requested workspace AND occurrence ID, rather than relying only on the local adapter's implicit contract. C2 applies the same checks. C3 still alone admits model state; C2 cannot call administrative decisions. No Runtime/store or integrated example was instantiated/executed to qualify this assessment.

## 2. Component functions

| Function | Delivered source behavior | Remaining work |
| --- | --- | --- |
| F20 decode | Bounded C1 range reads; exact source references; UTF-8 text, ordered/lexical JSON, CSV strings, PNG IHDR metadata and supported WAV header metadata | Rich document/image/audio/video/graph/music/array parsers, OCR and semantic perception; broader codecs and parser process isolation |
| F21 identity/meaning | Orthogonal authored role/basis annotations, exact byte-quote checks, declared quantities and limited SI dimensions; registered-source/content comparisons; explicit referent/part/replacement hypotheses | Learned linking, calibrated physical recognition, semantic term resolution and qualified continuity decisions |
| F22 retrieval features | Versioned native lexical/container statistics alongside decoder/input/artifact identity | Embeddings, search indexes and similarity calibration; current statistics are not semantic embeddings |
| F23 attributed candidates | Immutable C2 derivations; reviewable C3 patch builder and candidate-only submission/retry receipts | Full interpretation-to-domain mechanisms, C3 stronger admission/availability policy and live C4/C5/C6 consumers |

The same InterpretRequest supports decode, annotation and derive_features flag through one pipeline; these are not separate services. C2 does not infer a mechanism or classify a sentence merely because its decoder succeeded. C0 supplies any authored/context references. Existing model/student/teacher choices and fixed-weight direction are unchanged; no neural model or inference adapter is invoked here.

## 3. Input and exact decoding

Inputs identify C1 occurrence IDs, explicit decoder/auto selection, optional absolute byte ranges and CSV delimiter. Workspace is checked against the configured owner store. Decoder auto selection uses SUPPLIED media type, not an inferred true identity. Unknown media defaults to opaque reference-only output. Explicit decoder choice is retained. UTF-8 is the only installed text encoding; declared incompatible native-layout encoding/delimiter conflicts and unknown critical profiles prevent decoding.

The source range is read in bounded chunks. C1 verifies touched chunks. C2 records selected-range SHA-256 and compares the aggregate to the C1 manifest when the whole acquired object is selected. For a partial byte range, it does not claim to have verified unread whole-object bytes. EvidenceRef retains the original C1 manifest hash, origin_class and lineage with whole-object or bytes:start:end selector. Source event/report/clock/sequence, receipt and commit times are retained separately from C2 created_at.

| Decoder | Result semantics |
| --- | --- |
| text-utf8 | Strict decoded text; no replacement characters, guessed encoding or semantic classification |
| json | Typed tree: objects are ordered entry lists preserving duplicate keys; number nodes retain original lexemes, distinct from numeric-looking strings; arrays/booleans/null remain typed. Raw whitespace/escapes remain accessible in C1. Depth/node preflight and postparse bounds apply; nonstandard constants and invalid decoded Unicode are rejected. |
| csv | Ordered rows/cells stay strings, including exact decoded numeric spellings and empty cells. No header, dtype, zero-fill or ordinal arithmetic is assumed. Parsed cell paths are not falsely identified as raw byte spans. |
| png-metadata | Validate PNG signature, IHDR shape/values and IHDR CRC; retain width/height/bit depth/color/interlace. No pixel decoding, later-chunk validation, artwork recognition or image meaning is claimed. |
| wav-metadata | Python wave's supported header metadata: channels, width, sample rate, declared frames and compression. Samples are not interpreted or verified as a complete waveform. |
| opaque | Native evidence reference only, with explicit unknown/unprocessed status and no payload read |

Unsupported media/limits and decode failures are explicit artifact outcomes. Source bytes remain unchanged in C1. Partial/unknown acquisition completeness is a warning; a complete DERIVATION means its requested installed transforms completed, not that the source was complete, truthful or understood holistically. Metadata-only is distinct from decoded content. No recursive archive expansion, URL fetching, pickle/code execution or decompression of PNG pixels occurs.

## 4. Meaning, roles, quantities and association

ClaimAnnotation retains statement, optional original UTF-8 quote with absolute source byte bounds, descriptive roles, role rationale, evidential basis/rationale, proposed referents, quantity, expected unit, meaning and attribution. Roles include event/state_sample/rate_sample/pattern/structure/mechanism/purpose/unclassified. Basis independently distinguishes measured_or_inspected/reported/inferred/assumed/unknown. These labels are AUTHOR declarations, not an executed truth or semantic classifier. Multiple tags are compatible when their rationale explains them.

Exact quote validation only proves the supplied nonempty bytes match the selected original range. It does not verify the paraphrase, causal interpretation or truth of the statement. A derived JSON path/CSV cell is not accepted as an invented C1 byte address. Physical/spatial/media selectors need future validators.

Operator-supplied annotations stay attributed. Imported assistance additionally requires producer, model/checkpoint, prompt version, tool-schema version, configuration and lineage references. This preserves DECLARED versions; no external authentication or model-quality certification is performed. No external assistance call or cost is assumed measured by this local pass. Semantic neutrality/removal of pretrained priors is not claimed.

The limited-si/1.0 checker accepts declared symbols 1, m, kg, s, A, K, mol, cd, Hz, N, Pa, J, W, mm, cm, km, g and ms. Restricted * and / expressions and signed integer powers within -8..8 produce dimensional vectors and scale descriptors. This is a small explicit format/unit prior; it does not infer the intended meaning of a source symbol. No parentheses, affine Celsius/Fahrenheit, arbitrary prefixes, compound natural-language units or general unit algebra are supported. Pint remains a future wider adapter.

Known cardinal annotations require a supported finite numeric scalar and compare declared dimensions when an expected unit is supplied. Unsupported/missing units remain unsupported/unknown. Incompatible dimensions or invalid cardinal values block world submission, while the failed/partial interpretation remains inspectable. Values are not converted or averaged; missing does not become zero, and ordinal/categorical scales do not undergo arithmetic.

Automatic association proposals only compare registered C1 source_id and whole-payload manifest hash. same_source, same_payload and occurrence identity stay distinct. Hash equality does not establish a physical referent or a second independent witness. Reported handles can span epochs but are not natural-world recognition. Explicit mentions_same_entity, possible_same_physical_referent, part_of and replacement_of proposals retain evidence, unknown direction, alternatives/contradictions and method attribution. No uncertain-link transitive closure, automatic equivalence class or destructive merge is installed.

## 5. Persistent derivations and source accounting

C2 owns a separate SQLite store with immutable derivations, request fingerprints, durable staged submission patches and final receipts. Default path is the C1 sibling `<stem>.interpret.sqlite3`. C0 opens it lazily; ordinary C1 recording and capability listing do not initialize C2/C3 storage. Decoding/storage does not open C3; only explicit submission requests its candidate port. All three configured database paths must differ and workspaces must match.

The retry fingerprint covers the canonical request, full declared C2 profile, decoder implementation version, code/Python/Pydantic/SQLite versions and current CSV field limit. Full profile/runtime snapshots are retained in the derivation, not merely hashed. Repeating the same request returns the original outcome, including failed/partial outcomes; changing request/config/version under that ID conflicts. A new derivation is required for an intentionally changed interpretation. Concurrent attempts may do duplicate compute, but the store admits only one result for the same fingerprint. There is no durable job lease/singleflight engine yet; process-global parser mutation by unrelated code is not sandboxed.

Each derivation retains original request, source references, decoder/version, selected hash and verification scope, structured output, warnings/errors, annotations, native associations, derived-content hash and scoped usage. Native features carry `edi.native-features/1.0`; lexical counts/header values do not create semantic similarity or unit/identity truth. Features and derived content are not rewritten into C1 as independent observations.

Usage records bytes read, derived-content JSON bytes and elapsed transform time BEFORE artifact commit. It includes requested C1 reads, excludes original acquisition, C2 commit latency, C3 submission and upstream imported assistance costs. Model calls/tokens are zero for this implemented deterministic pass only. This is not complete task cost/energy measurement or an efficiency benchmark; complete instrumentation remains open.

## 6. C3 candidate integration and recovery

SubmissionRequest identifies an immutable derivation, retry-stable world request ID, base revision and optional consumed evidence progress. build_patch returns a concrete reviewable WorldPatch without opening/writing C3. It creates stable new IDs derived from the derivation for source-report histories, attributed claim histories and information-link association candidates, reusing the existing nine families. Decoded data stays in C2; C3 receives compact source/derivation/hash/feature/provenance references, not every cell/text byte copied into the world.

Role tags describe the CLAIM. A history record describing a reported structure is not automatically a canonical structural mechanism. C4 may later propose an actual domain mechanism with the evidence and remaining rivals. Simulation source origin remains simulation where mapped, and source provenance is never relabeled as independent new evidence.

submit uses only the C2 WorldAccess.propose_patch port: proposer=C2, candidate puts, expected_version=0 for stable new artifact IDs, no admission/rejection/retirement, no administrative C3 commit and no implicit rebase. C3 validates support, exact source identity/provenance, refs, limits and base revision. Existing-ID or stale-base conflicts are returned for explicit review; no facts/criteria are silently replaced.

Failed derivations or incomplete operation errors cannot submit. Partial format coverage can submit explicit opaque/unsupported/failure metadata alongside valid results when the overall operation completed without an unresolved top-level error; this never means those artifacts were understood. Incompatible cardinal annotations block submission. Batches beyond 64 initial C3 operations are explicitly rejected; use a smaller derivation.

Before calling C3, C2 durably stages the exact candidate patch with its submission fingerprint. A retry reuses this patch even if a later mapper would produce different content; it does not silently reconstruct/rebase the old request. After C3 commits, C2 attaches the returned final receipt locally. If C3 committed but C2 receipt persistence fails, the result is unknown-commit-outcome FOR THE C2 RECEIPT with the known C3 request/revision in the message. Retrying the identical submission reaches C3's idempotent original result before stale-base/evidence checks and can repair the local receipt. The two stores are not atomic. C3 status remains independently inspectable through C0. Protocol/DB incompatibility after a future upgrade still needs explicit migration; staging is not universal upgrade compatibility.

Optional consumed evidence is carried into C3's existing atomic model/progress commit; C2 does not mutate C1 checkpoints. C0 may invoke world-ack after durable C3 progress. No automatic streaming daemon, scheduler, autonomous crawl or exactly-once external action is implied.

## 7. Interfaces and eleven-facet contract

Only IF-02A/B (C0/C2 control/results), IF-08A/B (C1 evidence/range reads) and IF-14A/B (C3 candidates/results) are allocated. All eight owners, 28 pairs and 56 directed dispositions remain; C2-C4 has no new direct link. C3 exposes C2 dependency/proposal/status but no free-standing global world query. C0 may pass selected authored referent context until that contract evolves. [Source-review lane inventory](evidence/c2-source-review.json) retains every pair/direction.

| Facet | Implementation contract |
| --- | --- |
| Ownership | C1 native records; C2 immutable derived data/submission receipts; C3 canonical versions/admission; C0 scope and handoff. |
| Authority | Read-only C1 access and candidate-only C3 proposal; no source mutation, self-admission, action execution or direct C4 call. Local SDK identity labels are not a remote authentication boundary. |
| Shape/versions | Strict 1.0 requests/annotations/results, exact decoder/feature/checker IDs, generated JSON schemas; unsupported outer versions and critical profiles are explicit. No DB migration is inferred. |
| Identity/scope | Validate returned C1 workspace/record IDs, preserve source/epoch/occurrence/content/ref distinctions; association candidates never auto-merge physical subjects. |
| Time/order | Preserve source times and observer receipt/commit/derivation time; explicit C3 base revision. No artificial chronology from text order or source silence. |
| Delivery/idempotency | Stable request/config fingerprints and distinct world submission identity; original outcomes reused; changed requests conflict. |
| Commit/recovery | C2 derivation precedes optional C3 candidate commit; C2 receipt follows it; lost acknowledgement reconciled by exact retry. C1 progress only after C3 progress via C0. |
| Retention | Retain-only local derived history with finite quota; raw material remains subject to C1 availability. No pin/lease, eviction, backup/restore or automatic retraction cascade is installed. |
| Resource limits | Finite inputs, request/output/storage, parse depth/nodes/cells, association count, read chunks, local concurrency and cooperative deadline. No unbounded worker queue. |
| Errors | Unsupported/opaque/failed/partial are explicit; source integrity, invalid quote, dimensional mismatch, stale world revision and unknown commit are not hidden as success. |
| Feedback grounding | Exact input/assistance lineage; no derivation or imported statement becomes another independent observation. No semantic/truth classifier is implied by a parsed format. |

## 8. Finite local profile

Defaults: up to eight input selections, 16 claim annotations and 16 explicit associations per request; 128 KiB serialized request; 8 MiB aggregate bytes read; 262,144 decoded text characters per input; JSON depth 32/nodes 4,096; CSV rows 4,096/cells 16,384; 32 native association proposals; 64 KiB C1 read chunks. CSV uses Python's bounded default field parser and explicit delimiter; a field-limit rejection is surfaced rather than changing a process-global setting.

Decoded-artifact content is conservatively limited to half the 4 MiB stored-derivation maximum, leaving room for request/annotations/usage. Budget excess fails explicitly rather than silently truncating complete data. Retention allows at most 100,000 derivations and 100,000 staged/final submission records within a 1 GiB serialized-data quota counting staged patches and final receipts, plus database/index/WAL overhead. A 256 MiB free-disk reserve is checked before writes. Two local service operations may run concurrently; excess admission is retryably rejected. SQLite writer timeout is five seconds.

The transform deadline is a ten-second COOPERATIVE check; Python parsers, blocking C1/SQLite/fsync calls and OS memory allocation are not hard real-time or process-isolated. Request/config/control files are trusted local inputs. Resource settings do not prove total RAM, latency, energy, security, availability or unlimited scalability. Backup/restore, untrusted-parser sandboxing, fair durable scheduling, complete usage, schema migration and replicated deployment remain open.

## 9. Examples and schema assets

[Request template](../../examples/interpret/request.template.json) uses an actual C1 occurrence ID. [Annotated text template](../../examples/interpret/annotated-text.template.json) shows role/basis attribution. [Lexical JSON source](../../examples/interpret/lexical-source.json) deliberately contains duplicate keys and numeric spelling distinctions; it is a SOURCE fixture, not a configuration object. [Submission template](../../examples/interpret/submission.template.json) requires the returned derivation ID and current C3 base revision.

After installing the package as described in [the C1 guide](FOUNDATION_C1_RUNTIME.md), copy/fill the templates under .local and use the same workspace/database profile:

```powershell
.venv\Scripts\python -m edi --config examples/observation/local-profile.json interpret .local/interpret-request.json
.venv\Scripts\python -m edi --config examples/observation/local-profile.json derivation DERIVATION_ID
.venv\Scripts\python -m edi --config examples/observation/local-profile.json world-head
.venv\Scripts\python -m edi --config examples/observation/local-profile.json interpret-build-patch .local/interpret-submission.json
.venv\Scripts\python -m edi --config examples/observation/local-profile.json interpret-submit .local/interpret-submission.json
```

These commands/examples were NOT executed as product cases. Use new request IDs for changed requests/config and preserve the exact old submission for recovery retries. --interpret-config accepts an optional InterpretationProfile JSON. C3 progress/ack is optional and explicit; no background consumer is started.

Generated shape references: [InterpretRequest](../../schemas/interpret-request.schema.json), [SubmissionRequest](../../schemas/interpret-submission.schema.json), [Derivation](../../schemas/derivation.schema.json). Schema generation documents source shape; it is not proof that an example or runtime qualifies.

## 10. Requirements and retrospective

[C2_RUNTIME_TRACE.json](C2_RUNTIME_TRACE.json) cascades existing IMP/DOWN obligations -> twelve scoped C2 requirements -> F20-F23/source components -> thirteen future cases. All cases remain not_run; original catalogues/case counts/evidence are unchanged. Broader C2 interpretation, entity matching, perception, unit arithmetic, temporal correspondence, search and consumer obligations remain partial.

KISS: one typed pipeline/store, standard parsers, no mandatory inference/broker/graph/embedding. Five Whys: future reasoning needs accessible structure; useful structure needs meaning/provenance distinctions; correction needs immutable derivations; stable retries need exact input/config identity; independent observation requires preventing generated echoes. These are design rationales, not empirical intelligence claims. MECE keeps modality, descriptive role, evidential basis, parse state, identity relation and admission as separate axes.

Self-review repaired explicit C1 returned identity/scope checks in C3/C2, decoder exception normalization, invalid Unicode handling, immutable retry snapshots, empty quote rejection, numeric/dimension checks and hash accounting after an output-budget failure. C1/C2/C3 use lazy separate stores to avoid parser/model/store failure becoming an unavoidable intake dependency. Limits and raw-source access remain explicit.

Checks performed: source AST parsing, application imports, CLI parser construction, authored TOML/JSON parsing and new-document links; schemas generated from source. No Runtime/store was instantiated, no decoder/example/patch/recovery/product case or test suite ran, and no model inference, training, simulation, benchmark or deployment occurred. Source self-review is not independent. No C3 or C2 full acceptance, runtime/integration PASS, measured speed/efficiency or intelligence advantage is established.

Next architectural owner is C4 reasoning, while C1-C3 outstanding requirements/qualification remain tracked. Selecting a model/provider/hardware or running an inference job is a separate binding; no credential or paid-model action is implied by this increment.
