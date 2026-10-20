# C3 shared world-model substrate: first local implementation

Historical code 0.3.0 handoff: [C2 increment](C2_INTERPRETATION_RUNTIME.md), code 0.4.0, now consumes the prepared evidence/candidate subset and adds explicit returned C1 identity/workspace checks. This does not qualify C3 or close the remaining obligations below.

20 October 2026. Code version **0.3.0**. Input: `bd8b05d6c17114fe6747c18801399444838125a3`. Status: source implementation, **unqualified**. No product/qualification tests, inference, simulation or benchmark campaign ran. [ADR-004](../decisions/ADR-004-versioned-world-hosting.md) records the design decisions; [source review](evidence/c3-source-review.json) preserves open obligations.

## 1. Delivered boundary

C3 now hosts typed representations, versions, candidate/admission history and bounded model views. C0 opens C3 lazily and coordinates evidence progress. C1 remains the sole native evidence owner; C3 validates references through C1's read facade. C2 interpretation and C4 reasoning are still unavailable, so inputs are explicitly authored patches, not demonstrated discovery.

| Function | Source implementation | Limit |
| --- | --- | --- |
| F30 instantiate/compose | Nine typed families, stable IDs, nested/overlapping references, roles, interfaces, scope, alternatives and uncertainty | No domain ontology inference, automatic identity merge or abstraction qualification |
| F31 admit/revise | Candidate-only proposal ports; trusted local scoped decisions; optimistic base/record versions; immutable versions/commit log; request retries | Policy validates declared modeling-use conditions, not empirical truth; no remote identity provider |
| F32 scoped views | Exact revision reads, scope/family/state filters, explicit valid-time filtering and pinned pagination | No unrestricted graph query, timestamp-to-knowledge-revision lookup or actor perception policy |
| F33 projections/dependencies | Transactional head index and versioned reverse reference index; bounded dependency/dependent traversal; revision invalidation notice | No vector/graph engine, selective transitive revalidation worker, cache rebuild API or automatic evidence expiry propagation |

Historical SUB-C1/SUB-C2/SUB-C3 labels in the retained blueprint are INTERNAL substrate parts; they are not global C1/C2/C3. Their storage/admission duties map to current C3. Inquiry/execution/assessment map to C4/C5/C6. No additional component or service is created for each term.

## 2. Representation catalogue

| Family | Concrete structure fields |
| --- | --- |
| System view | Included/excluded members, external drivers/sinks, boundary, purpose, level, resolution, horizon and closure assumptions |
| Constituent | Parts, roles, condition and lifecycle |
| Stock | Typed quantity, initial basis, inflow/outflow references, bounds and reserve/access distinctions |
| Flow/process | Role-indexed participants and direction, optional rate, response, prerequisites, pending commitments, transformation/time basis and resource use |
| Information/influence link | Participants, direction, channel/meaning, availability/receipt/attention, distortion and unknown/hypothesized/reported causal status |
| Response relationship | Joint participants, mechanism description, parameters, domains, delays, capacities and explicitly nonexecuting status |
| Function/purpose/reference/criterion | Distinct function/purpose/goal/reference/criterion/constraint/inquiry role, attributed owner/basis, definition, horizon, conflicts, feasibility and normative scope |
| Feedback path | Ordered mechanism references, closure, conditional polarity, delays and applicability |
| History/conditional trajectory | Referents, source/forecast/simulation origin, initial history, supplied points/time/units/aggregation, driver assumptions, model/policy versions, run identity and horizon |

All representations also retain support/counterevidence, assumptions, method lineage, uncertainty, valid interval, scope, alternative group/links and generic properties. Missing qualitative/numerical material stays explicit or unspecified; a numeric stock is not required for everything. Quantity strings preserve declared precision; C3 does not silently convert units or numeric strings. These structural priors are declared; semantic neutrality is not claimed.

Ref carries an internal record ID and optional version. Before storage, an omitted version is resolved to the post-patch target; forward references within one patch can resolve to that new revision. Explicit historical references must exist. Self and multi-party/cyclic references are allowed and do not execute anything. A pinned reference is representation identity, not evidence of physical identity or causality.

Only typed Ref fields form indexed dependencies. Opaque dictionaries, strings, equations and points are retained without interpreting apparent embedded IDs or running code. No mechanism compiler, conservation checker, unit algebra, closure/polarity proof or stock-flow simulation is installed here; those obligations remain visible for later C5 integration. Whole-object source content remains in C1.

## 3. Changes and admission

WorldPatch specifies workspace, retry-stable request_id, expected whole-model base revision, proposer, reason, change kind and one bounded operation per representation. Change kinds distinguish state, parameter, organization, policy, goal, explanation and context; they describe MODEL amendments rather than authorize physical action. No automatic rebase occurs.

| Operation | Meaning |
| --- | --- |
| put | Create or replace a representation snapshot with expected_version=0 for a new ID, otherwise the exact previous version. Stable family cannot change under the same ID. A changed record becomes candidate unless an operator explicitly supplies admission. |
| decide | Append a new snapshot with candidate/accepted_for_use/rejected/withdrawn decision and rationale; the previous snapshot stays available. |
| retire | Append a retained retired snapshot; no evidence or version is deleted. |

Split/merge/rewire is expressed through bounded puts, new IDs/compositions, explicit lineage/properties and retirement of superseded views. There is no inferred physical merge or automatic migration of stocks/orders/pending state. Carry-over/loss semantics and specialized split/merge operators remain future work; a caller must explicitly retain the desired contents in its replacement record.

WorldAccess.propose_patch accepts only candidate puts, enforces the allocated proposer, and exposes no administrative commit method. Decisions use trusted local World.commit / CLI world-commit. The stored decision_authority distinguishes C3-candidate-policy from C3-local-operator. This is an SDK discipline inside a trusted process, not user authentication or protection against Python introspection.

Initial local-modeling-use/1.0 policy requires accepted_for_use to have linked support or explicit assumptions, a nonempty rationale, use_scope and remaining verification_obligation. It offers no empirical-truth class. Source reports, model derivations and assumptions retain their basis. Presence of support, schema validity, teacher agreement and plausible text cannot prove a mechanism. No scalar truth score is introduced. The local decision can still be scientifically wrong; qualification and stronger domain-specific policies are open.

Rejection/withdrawal/retirement history is retained. Withdrawal/retirement can proceed even if old raw evidence becomes unavailable. New puts and accepted-for-use decisions recheck their linked C1 evidence metadata. A decision never edits C1 or a previously sealed forecast.

## 4. Evidence and progress interface

For each support/counterevidence link, C3 uses the allocated IF-09 facade to inspect the immutable C1 record and checks workspace, exact manifest SHA-256, supplied origin_class/lineage and selector bounds. Supported selectors are whole-object and half-open bytes:start:end. Page/image/track/semantic selectors need future C2 validators; they are rejected as unsupported here rather than guessed.

This validates correspondence to C1's declaration and addressable byte bounds, not natural-world correctness or the integrity of every underlying payload byte. C3 cannot read payload bytes on IF-09. C1's payload reader checks touched chunk hashes; C2 will own decoding and exact semantic correspondence. An external-origin declaration is not independent evidence certification. No model inference is needed for this validation.

An optional consumed record declares consumer ID, expected prior C1 position, new position and selected occurrence IDs. Those IDs must be linked in this patch's validated evidence; an advance must end at a linked committed C1 occurrence. Selected IDs may skip records by explicit consumer selection; the cursor does not claim complete coverage or interpretation of skipped material.

In one C3 transaction, commit versions, dependencies, current-head index, original patch/fingerprint, revision notice/retry result and C3 consumer progress. Only afterward may C0 call acknowledge_world_progress to update C1's checkpoint. A crash before C3 commit retries; a crash after commit/before C1 acknowledgement resolves through C3 request status and durable progress. Repeating the same request returns its original revision; a changed patch or authority channel under that key conflicts. C1 and C3 do not share a transaction or database writer.

C3 is lazy: importing the application, listing source capabilities or using C1 recording does not open C3's database. Opening/using C3 can fail separately. C3 calls C1's bounded read facade while holding its own transaction; C1 does not call back into C3, avoiding a circular writer dependency. Both still share finite host resources. Native intake and C3 are not isolated from physical disk/host loss.

## 5. Versions, views and dependencies

Model revisions start at 0 (empty). Each committed patch gets the next integer revision; each changed representation's version equals that revision. Old versions remain immutable. get(record_id, revision=N) selects its latest version at or before N, including retired states for inspection. Knowledge-as-of is pinned by model revision; known_at is a local pre-commit timestamp, not a qualified hardware acknowledgement or a guarantee of monotonic wall clock.

Queries fix a revision and paginate lexically by stable record ID. Filters are applied AFTER selecting each record's latest version at that revision, preventing a retired/changed record's old matching version from being silently resurrected. Defaults return candidate/accepted-for-use records; inactive states can be requested explicitly. A cursor binds workspace, revision, query and after ID; changing its scope/filters/revision conflicts. No full history is copied to an LLM.

Valid-time scope is unknown, unbounded or a UTC interval [start,end). A valid_at query excludes unknown validity unless include_unknown_validity is explicitly enabled. Revision time and modeled valid time are separate. Simulated clocks, unavailable-history retention and complete timestamp-indexed bitemporal semantics remain future work; unknown intervals are never silently interpreted as timeless truth.

dependencies/dependents traverses typed references at a chosen revision with bounded depth/nodes/edges and cycle detection. It compares each pinned target version with the target visible at that revision, reporting current/changed/inactive/missing plus the visible admission state. "Current" means matching structural version, not empirical correctness. Retired/withdrawn/rejected targets are flagged inactive. Traversal follows visible versions and flags stale pins; it is not an implicit execution of the old pinned mechanism tree.

Reaching a depth, node, edge or frontier boundary reports complete=false with explicit truncation/boundary IDs. Even complete structural traversal cannot certify evidence independence, units, model validity or analysis eligibility. get results and query pages are marked not-certified; callers must inspect dependencies/evidence before use. Queries do not silently revoke historical admission decisions when a dependency changes.

Each WorldCommit is the durable revision/outbox notice, identifies changed_ids and invalidates prior-revision `world.current` views. changed_ids is NOT an exhaustive transitive invalidation list. A cache must key on the exact model revision or revalidate; no old global projection is declared current. The transactional head/reference indexes are local projections of append-only versions. No graph/vector cache or transitive maintenance worker is installed yet.

## 6. Eleven interface facets and all-pair assessment

Existing component registry stays eight owners, 28 pairs/56 directed lanes. C0-C3 and C1-C3 now have local source paths; C2/C4/C5/C6/C7 endpoints remain unavailable/prepared. [Structured allocation](evidence/c3-source-review.json) records every lane; no full-mesh or new C4-C5/C7 bypass is created.

| Facet | Concrete local contract |
| --- | --- |
| Ownership | C1 owns native evidence; C3 owns representations, admission, versions, indexes and its progress; C0 coordinates the separate handoff. |
| Authority | C0/C2/C4/C6/C7 may propose candidates; C5 reads/dependencies only; C1 supplies evidence responses but gets no world mutation port. Operator decisions are absent from component facades. |
| Shape/versions | Strict 1.0 records/discriminated operations/families; extra fields/unsupported selectors rejected; opaque bounded properties allowed. Unknown DB schema rejected; no migration applied. |
| Identity/scope | One cumulative model per workspace, stable internal IDs and pinned versions; scopes/views overlap rather than duplicate source entities automatically. |
| Time/order | Optimistic global base revision and expected object versions; revision-pinned knowledge reads and separate valid time; no source-time order invented. |
| Delivery/idempotency | Request fingerprint includes the exact admitted JSON snapshot and authority channel. Same retry returns original result; changed payload conflicts. |
| Commit/recovery | C3 mutation/progress/index/outbox state atomic; C1 checkpoint only afterward; unknown commit acknowledged explicitly and resolved by request ID. Recovery/restore cases unrun. |
| Retention | Retain-only versions; explicit rejection/withdrawal/retirement append history. No raw evidence pin/lease, eviction or retention tombstone API is assumed. |
| Resource limits | Finite operation/byte/ref/evidence/version/consumer/query/graph limits, bounded service slots, SQL work/time interruption and cooperative commit budget. |
| Errors | Scope-denied, malformed-envelope, unsupported-profile, not-found, conflict, integrity-mismatch, capacity, storage-unavailable and unknown-commit-outcome. No silent automatic rebase/promotion. |
| Feedback grounding | Origin/lineage must match C1 declarations; candidate proposals cannot accept themselves; no generated echo is automatically corroboration; no simulation or actor action executes here. |

C2 has proposal/dependency/status operations under IF-14; a free-standing full-world read is not granted just because snapshot results are mentioned. C0 can provide selected interpretation context until that contract evolves. C7's global EDI model read is not a modeled actor's perception. actor_view raises unavailable until visibility policy exists; it never substitutes the global snapshot.

## 7. Capacity and availability profile

Default C3 limits: 1 MiB patch, 64 operations, 64 KiB per stored version, 128 typed references per record, 256 evidence-validation items per patch including selected consumed IDs, one million stored versions, 1 GiB serialized version/patch/result bytes, 1,000 progress consumers and four concurrent service operations. Extra physical database/index/reference/WAL overhead is not included in the JSON byte quota. A 256 MiB free-disk reserve is checked before new commits.

Reads return at most 100 records. Dependency traversal permits at most 256 expanded nodes, 1,024 returned edges and depth 8. SQL connections set an approximately 8 MiB page cache, a five-second writer wait and a progress handler capped at approximately one million VM steps/two seconds between checks. The overall Python commit path also checks a ten-second cooperative deadline. SQL interruption returns a capacity error; very short statements may finish before a callback, and blocking I/O/COMMIT cannot be made hard real-time by these callbacks.

This is a serialized-writer, single-host SQLite profile with local-sqlite-full-unqualified receipts. C1 and C3 may contend for host resources even though stores/locks are separate. There is no replicated storage, HA, demonstrated tail latency, production throughput, unlimited scale, total-RAM guarantee or PostgreSQL compatibility result. No new dependency/model/tool service was installed. Schema generation is a reference artifact, not qualification.

C1 backup includes C1 only. C3 currently has no online backup/restore endpoint; qualified whole-application backup, consistent multi-store restore and migration are open. A stopped/checkpointed C3 store can be copied by a local operator, but this is not tested restoration evidence and does not justify copying an active main file without its journal.

## 8. Requirement allocation and remaining work

The original [SUB catalogue](../../architecture/substrate/REQUIREMENTS.json) and [implementation trace](TRACEABILITY.json) remain unchanged historical/proposed authorities. The following is this increment's allocation, not a blanket requirement pass. All SUB-V001-SUB-V022 and relevant E cases remain unrun.

| Requirements | Current code contribution | Remaining work |
| --- | --- | --- |
| SUB-R001 | Nine-family addressable structures, exact supplied properties, source links and unknowns | Mixed-format consumer demonstration and native selector validation |
| SUB-R002 | Stable IDs, immutable versions, pinned refs, retirement/revision history | Qualified identity split/correction and automatic affected-region revalidation |
| SUB-R003 | Participant roles, distinct direction/causal status/polarity/closure and n-ary structures | Mechanism consistency/causal interpretation checks |
| SUB-R004 | Stored qualitative/nonlinear mechanism/domain/delay/constraint descriptions | Restricted executable C5 grammar, conservation and numerical semantics |
| SUB-R005 | Valid-time scope, knowledge revisions, retained history/pending references | Simulation clocks, supported delay execution and leak-free prediction cases |
| SUB-R006 | Shared references, nested/overlapping systems and scoped reads | Validated refinement bridges/aggregation loss accounting |
| SUB-R007 | Explicit uncertainty, rival groups/refs, candidate/rejected states | Actual inquiry and calibrated evidence-based discrimination |
| SUB-R008 | C1 hash/provenance correspondence, method lineage and source/derivation basis | Authenticity/independence assessment and C2 decoder/model lineage |
| SUB-R009 | Versioned scope/boundary/context amendments | Autonomous context/regime discovery and response validity assessment |
| SUB-R010 | Bounded inspectable candidate/dependency data | C4 frontier, selection/stopping policy and active access requests |
| SUB-R011 | Proposal/decision/trial distinction, optimistic versions and explicit authority | C5 isolated trials and C7 actual adoption; stronger remote authorization |
| SUB-R012 | Put/retire/compose rewiring with prior versions intact | Dedicated split/merge, continuity carry-over/loss and generative rules |
| SUB-R013 | Distinct purpose/goal/criterion/constraint roles and attributed owner | Criterion adoption/threshold governance and outcome assessment |
| SUB-R014 | Finite quotas, admission/refusal and bounded reads/traversal | Complete end-to-end usage accounting, fairness and workload measurements |
| SUB-R015 | Append-only local transactions and retain-only history | Qualified backup/restore/retention/compression/failover and larger backend |
| SUB-R016 | Pinned structures/history, assumptions, source refs and conditional trajectory data | Prospective C5/C6 predictions, sealed outcomes and controlled comparisons |

The old substrate architecture REVISE status remains preserved; this source increment does not close its native learning/execution questions. C1's open connector/retention/HA/qualification obligations remain open as well.

## 9. Usage assets

After installing the local package as described in [the foundation guide](FOUNDATION_C1_RUNTIME.md), use the same observation workspace/database profile. The default C3 database is the sibling `<C1 stem>.world.sqlite3`; --world-config accepts an explicit matching WorldProfile JSON. C1 and C3 database paths must differ.

For a new forest-demo workspace, the supplied authored examples show a three-step progression:

```powershell
.venv\Scripts\python -m edi --config examples/observation/local-profile.json world-propose examples/world/candidate-patch.json
.venv\Scripts\python -m edi --config examples/observation/local-profile.json world-commit examples/world/admission-patch.json
.venv\Scripts\python -m edi --config examples/observation/local-profile.json world-propose examples/world/response-patch.json
.venv\Scripts\python -m edi --config examples/observation/local-profile.json world-query --query examples/world/query.json
.venv\Scripts\python -m edi --config examples/observation/local-profile.json world-get forest-view --revision 1
.venv\Scripts\python -m edi --config examples/observation/local-profile.json world-dependencies forest-view --depth 2
```

These are authored examples and were NOT executed. They demonstrate hypothetical representation intent, not budworm discovery. Literal base revisions assume an initially empty model and that preceding commits succeed. For an existing model, get world-head, inspect expected object versions and author a new patch/request ID. Do not change a previously committed request's content under its old key.

Use `world-status REQUEST_ID`, `world-progress CONSUMER` and `world-ack CONSUMER` for recovery/progress. Save only the returned next_cursor object for world-query --cursor. Administrative world-commit is for the trusted local operator; future components use Runtime.world_for(owner).propose_patch instead.

For a C1-linked input, copy [the evidence patch template](../../examples/world/evidence-patch.template.json) and replace the C1 ID, exact hash, origin_class/lineage, actual selected commit position, expected prior consumer position and current world base revision. The hash placeholder intentionally is not a valid filled-in EvidenceRef. Source material stays in C1; this patch does not decode it. Commit C3 progress first, then world-ack if desired. The template is separate from the three-step empty-world example.

Schema reference assets generated directly from code: [WorldPatch](../../schemas/world-patch.schema.json), [WorldQuery](../../schemas/world-query.schema.json) and [WorldCursor](../../schemas/world-cursor.schema.json). They describe shapes, not an empirical admission or execution standard.

## 10. Retrospective and checks

KISS: nine data families share one representation/operation pipeline, owner, transaction store and read facade. Five Whys ties lasting knowledge to identities, corrections to immutable versions, reliable revision to expected versions, defensible use to attributed evidence/assumptions and continued observation to independent C1 availability. These are design rationales, not measured intelligence. MECE separates identity/version, valid/knowledge time, direction/causal status, admission/truth and stored/executed change.

Source review addressed: an initially eager C3 initializer would have coupled C1 availability to C3; it is now lazy. Withdrawing old claims must not require missing raw evidence; only new puts/promotions revalidate evidence. Graph depth/node/edge frontiers are reported incomplete, not global certificates. Admission is kept off component proposal facades. Mutable nested input JSON is copied into one canonical admitted snapshot so its retry fingerprint and stored contents agree.

Executed checks: Python AST parsing, application imports, CLI parser construction and authored TOML/JSON parsing; JSON schemas generated from source. No Runtime/store was instantiated; no example, recording/replay, patch commit, fault/recovery, integrated product case, test suite, benchmark, inference or training was run. Self-review is not independent. No architecture/contract/runtime/integration PASS is issued. Publication integrity is checked separately with Git content hashes.

Next component is C2 interpretation, using C1 native bytes and proposing attributed candidate structures to C3. Broader C3 obligations stay tracked rather than being declared finished by this increment.
