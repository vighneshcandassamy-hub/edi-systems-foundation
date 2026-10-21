# EDI Systems Foundation — checkpoint

Date: 20 October 2026. Version: 0.1.0-architecture.

## What is stored

- Integrated Meadows Chapters 1–7 conceptual architecture, internal v0.7, saved source version 5.
- Appendix pages 187–203 semantic reference, v1.0.
- Retained observation, substrate and integration planning snapshots with their original evidence.
- Existing component-review and interface-review skills and bundled helpers.
- Import hashes, a local consistency checker and the initial repository decision.

## Evidence status

The conceptual documents have consistency/traceability reviews. The master architecture contains nine representation families, 346 catalogue units, 54 requirements and 192 prospective scenarios. Its master graph has 82 nodes and 241 named connections. The appendix reference allocates 102 source entries, 20 working requirements and 24 prospective reference-use cases. All model scenarios remain PLANNED — NOT RUN. Earlier retained checks are historical and do not establish a new runtime.

## Current scope

This task stores and organizes the new baseline. It does not implement an intelligence, migrate the earlier runtime, run experiments or establish superiority, throughput, cost, energy, availability or arbitrary scalability.

## Remote status

The private repository [vighneshcandassamy-hub/edi-systems-foundation](https://github.com/vighneshcandassamy-hub/edi-systems-foundation) is created and populated on `main`. Baseline commit: `059f302abd277756639d858c44f89db0fd324daa`. All 53 remote file blob hashes were verified against the prepared snapshot; its Git tree is `31b1d285f61d3fc8e6527cee1ee5cdb662dbb905`, identical to local snapshot `1ca0fdc8c286eaf09f5b50b0c1aa0e8bafcdb57a`. Remote history was initialized through the authenticated GitHub connection, so the remote commit ID differs from the portable snapshot while the baseline file tree is identical. The subsequent checkpoint records this verified upload and makes the documentation checker explicitly read UTF-8 on Windows as well as Linux. Documentation/import/graph checks pass; no model scenarios were executed.

## Next development step

Review the retained observation and substrate contracts against the current seven-chapter architecture and semantic reference. Select one capability and an explicit implementation gate with the owner before developing a runtime.

## Benchmark storage checkpoint — 21 October 2026

The stable folder is `benchmarks/meadows-budworm/`. Its README documents the intended evidence/database/metadata/documentation/evaluation/results organization. The import-status record explicitly marks the original database as missing and not uploaded. Historical EDI MVP 7 counts are retained as unverified conversation reports. No database, evidence payload, runtime or benchmark result is added by this checkpoint. Next action: recover the original database/archive, verify its inventory and integrity, and record checksums before importing it.

## Reconstructed benchmark database — 21 October 2026

The prior-chat database was unavailable. This commit replaces the pending import with a new primary-source reconstruction under `benchmarks/meadows-budworm/`, version 0.1.0: 32,895 structured records, 150 searchable text blocks and 28 evidence files across 16 formats and seven source groups. Eleven files are native downloads; seventeen are extracted or derived. Alternate CSV/GeoJSON exports share lineage and are not counted as separate observation sets.

The actual SQLite snapshot is stored losslessly as `database/evidence.sqlite.gz`. Original source bytes, hashes, lineage, explicit gaps and bounded read-only retrieval scripts are included. `scripts/restore.py` restores compressed files using the Python standard library. Source explanations remain references and generated audio/video remain derived encodings.

Actual storage checks passed: content hashes, SQLite integrity/foreign keys, FTS inventory, CSV/GeoJSON row and geometry parity, reference filtering, row pagination, byte-range requests, and restore/verification from a freshly extracted archive. The self-reviewed interface inventory covers three components, three pairs, six directed lanes and four implemented storage/read contracts. EDI integration and model benchmarks remain NOT RUN.

Archive: `EDI_Meadows_Benchmark_Database_v0_1_0.zip`; SHA-256 `f34ec3ee283729e8089ddfb75c3b04c146d85f5a12724f47b38ce4d0857c4f8a`. SQLite SHA-256: `49856811262c175efe99c31635e098e56312bdbca98a4ec1f58fab12794e5bd5`.

Next requested scope: add other benchmark materials in this stable folder. Missing matched ecological/management histories and native modality gaps remain explicit. This seed corpus is not a qualified standard benchmark or complete causal account.
