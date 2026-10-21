# Corpus contract and review scope

## Requirements

| ID | Obligation | Verification |
| --- | --- | --- |
| R01 | Retain original evidence and content hashes | Inventory hash checks against actual bytes |
| R02 | Preserve native values, unknowns, sentinels and selectors | Database payloads, source issue log and negative-code check |
| R03 | Retain heterogeneous formats and hierarchy | File inventory and workbook/page selectors |
| R04 | Preserve lineage and avoid double-counted exports | CSV/GeoJSON numeric/geometry parity and acyclic lineage |
| R05 | Separate observation files and published reference explanations | Read-only CLI inventory/text filter checks |
| R06 | Support durable recovery and bounded evidence requests | Gzip byte roundtrip, temporary-directory restore, row pagination and byte-range retrieval |

The immutable source bytes are the authority for received evidence. SQLite is the searchable index and retains source-row payloads. The maintainer alone admits a new version. CLI reads cannot write corrections into the evidence database. Corrections require a new recorded import, preserving the earlier snapshot through Git history.

Identity is occurrence/selector identity within a content-hashed source file. Native plot IDs remain source-scoped. Cross-format views share lineage; cross-study physical identity is not inferred from similar names or coordinates. Row numbers include header rows, workbook sheet selectors include exact sheet names and PDF selectors use 1-based physical page numbers.

Source event times retain their precision and clock context. Weather LOCAL_DATE is a local daily label, not a measured UTC midnight. Per-file acquisition is recorded to date precision; exact receipt timestamps were not captured. Archive build time is separate.

Readers request inventory, bounded records, text or byte ranges. Results expose IDs, selectors, source group, offsets and explicit has_more where relevant. Unknown IDs and denied reference access fail explicitly. SQL parameters are bound, the database opens read-only, row limits are at most 200 and byte ranges at most 65,536 bytes. The convenience reference filter cannot prevent an owner with filesystem access from reading the full corpus.

Builds use a staged local database and are published only after integrity verification. Restore writes a temporary file, verifies its hash and atomically replaces the missing destination. Repeated restores are idempotent, while conflicting existing bytes stop the operation. Git and the downloadable archive preserve a pinned version. Network refreshes must become a new corpus version rather than silently changing source files.

Source APIs, clocks, open-data distribution terms and scientific extraction libraries are external dependencies. Failed sources and partial coverage are recorded. No inference API, external action authority or learned feedback loop is implemented. Derived charts/audio/video return to the corpus with the same evidence lineage; they are never admitted as independent confirmations.

Review gates: storage contract and scoped storage checks can pass. EDI ingestion integration, autonomous inquiry, causal discovery, prediction, efficiency and comparative advantage remain **NOT RUN**. Source explanations and the familiar Meadows case cannot by themselves support blind novelty claims.
