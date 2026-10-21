# Meadows budworm evidence database

Version **0.1.0**, built 21 October 2026. Status: **database built; model benchmark not run**.

This folder stores a recoverable, heterogeneous evidence corpus for the Meadows budworm systems case. It is a new reconstruction from primary sources. The database reported in EDI MVP 7 was unavailable, so this release does not claim to recover that database or reproduce its inventory.

## What is actually included

- **32,895 structured records:** 16,166 NB larval-survey rows; 1,565 NB moth-trap rows; 14,434 rows from four Natural Resources Canada research-workbook sheets; 730 daily weather observations at Fredericton CDA CS.
- **150 searchable text blocks**, primarily reference documents and sampling descriptions.
- **28 evidence files in 16 formats**, spanning seven source groups. Eleven are native downloads and seventeen are extractions or derived representations.
- SQLite database, original source snapshots, source/licence notes, file hashes, lineage, explicit evidence gaps, storage checks and read-only retrieval utilities.

Records are not automatically independent observations. The research workbook includes both samples and publisher aggregate sheets. The CSV and GeoJSON survey exports are two views of the same 16,166 observations; the spatial export is not imported as a second set of records.

## Folder layout

| Folder | Contents |
| --- | --- |
| `database/` | Compressed SQLite snapshot and schema |
| `data/raw/` | Original downloaded source bytes, sometimes stored losslessly as `.gz` |
| `data/derived/` | Extracted text/images, linked serializations, charts, arrays and derived media |
| `metadata/` | Inventory, sources, acquisition outcomes, hashes, lineage and validation |
| `docs/` | Coverage, source limitations and corpus read/write contract |
| `scripts/` | Build, restore, integrity verification and read-only evidence requests |

Future benchmark task definitions, protocol and results can be added under this same folder. No evaluator or EDI runtime is added by this release.

## Open and verify

From this folder, using Python 3.10 or newer:

```bash
python scripts/restore.py
python scripts/verify.py
python scripts/query.py inventory --area population
python scripts/query.py records --series nb_l2 --year 2024 --limit 5
python scripts/query.py --include-reference text budworm --limit 3
python scripts/query.py gaps
```

`restore.py` checks SHA-256 before restoring each gzip-compressed file. It refuses to overwrite an existing file with different contents. SQLite opens read-only in `query.py`. Restoring, querying and verifying require only the Python standard library and SQLite FTS5/JSON support.

For rebuilding the database from the unchanged downloaded files, `scripts/build_corpus.py` uses NumPy, Matplotlib, Pillow, PyMuPDF, openpyxl and the `ffmpeg` executable. Its `--downloads` input is a directory of source snapshots and `download-log.json`, not an instruction to fetch new evidence silently. Source request URLs and failed acquisition outcomes are recorded in `metadata/acquisition_log.json`.

## Evidence discipline

Original numbers, nulls, sampling codes and source flags are retained. In particular, 164 negative moth-count codes are preserved and must not be interpreted as negative biological counts. The weather station is regional context; it has not been matched to every survey plot. Source coordinates and chronology are available for later, justified matching.

Each file and record has a stable content/selector identity. Lineage links alternate exports and transformations to their sources. A shared evidence group does not establish that two different studies measured the same physical tree, plot or insect.

Published explanations, species references, methods and report narratives are marked `reference`. The CLI excludes those files unless `--include-reference` is supplied. This convenience filter is **not** a security or benchmark contamination boundary: the owner has the complete database. A future blind benchmark must enforce its own withheld-evidence policy.

The animation, video and audio are explicitly generated from existing numerical data. They are useful ingestion fixtures, not field recordings, genuine ecological video or additional evidence. Format variety does not demonstrate model capability.

Matched predator/pathogen histories, longitudinal stand age and foliage, complete treatment histories, economic decision logs and several native observation modalities remain missing. See `docs/COVERAGE.md` and the `evidence_gaps` database table. This is a seed evidence database, not a complete causal account or a qualified standard benchmark.

Source attribution and licence status are recorded per source. Keep this archive private; public redistribution of source material with unverified terms requires a separate review.
