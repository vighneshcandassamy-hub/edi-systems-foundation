# Observation coverage and limits

The database is organized for later requests for evidence, rather than a single prompt containing the final ecological explanation.

| Information family | Stored representation | Native or derived | Remaining limit |
| --- | --- | --- | --- |
| Numeric/count observations | Original CSV and workbook cells | Native | Sampling selection and source codes require care |
| Tables and nested records | XLSX, CSV, JSON, JSONL, XML | Native plus linked serializations | Duplicate representations are not extra evidence |
| Time series and sequences | Collection dates, weather days, annual summaries | Native dates plus derived aggregates | Different time scales and incomplete overlap |
| Spatial information | Native GeoJSON, coordinates, report maps | Native exports plus derived plots | No asserted cross-study physical-entity binding |
| Text/documents | Original HTML/PDF, extracted TXT, FTS text blocks | Native plus extraction | Narrative contains human interpretation |
| Images/photographs | Native PDF image stream, rendered map pages | Extracted or rendered from source report | No newly acquired stand-photo campaign |
| Plots and diagrams | Source report plots; generated PNG/SVG | Source publication plus derived | Source charts may encode prior analysis |
| Scientific arrays | NPZ with values, row IDs and validity mask | Derived from observed source values | No native hyperspectral/point-cloud arrays |
| Audio | WAV annual-mean sonification | Generated numerical encoding | No field audio, speech or acoustic ecology |
| Animation/video | GIF and MP4 annual-chart sequence | Generated numerical encoding | No native video observations or audio/video synchronization |
| Human decisions/purpose | Monitoring and treatment narrative in agency report; forest uses in species references | Published reference statements | No complete contemporaneous economic or decision logs |

The sixteen evidence formats are CSV, GeoJSON, GIF, HTML, JPEG, JSON, JSONL, MP4, NPZ, PDF, PNG, SVG, TXT, WAV, XLSX and XML. SQLite and compressed containers are storage formats, not additional observation modalities.

Six knowledge areas are indexed: population, forest, weather, management, space/time and methods. This metadata is a curator's retrieval aid, not a claim that EDI discovered an ontology. Existing environmental relationships and causal hypotheses are not stored as verified truth.

## Source cohorts

- NB L2 mapping: 2017-2025, 16,166 source rows, varying sites and annual effort.
- NB moth trapping: 1,565 source rows. Original date strings and sentinels retained.
- Natural Resources Canada research workbook: study cohorts from 1998-2022, multiple regions and four sheets. Row-order joins between sheets are not assumed.
- ECCC daily weather: 730 days, 2022-2023, climate identifier 8101605, station FREDERICTON CDA CS.
- Maine Forest Service: 2021 monitoring report issued March 2022, 16 pages; references, maps, images and management narrative.
- USDA Forest Service: balsam-fir and black-spruce species-reference pages.

Independent field audio/video, radar, point clouds, tree rings, hyperspectral data, matched predator histories and full historical management/economic evidence are absent. These gaps are recorded rather than filled with invented observations.

## Acquisition failures

Several NB report/policy pages and a Canadian catalogue metadata endpoint rejected direct acquisition. One endpoint returned a small HTML rejection with HTTP success; that payload was rejected as invalid JSON and is not evidence. These outcomes remain in the acquisition log. No web-search excerpt is substituted for a native downloaded source file.

## Prior-chat claims

The previous chat reported 23,743 structured records, 1,339 text blocks and 31 files in 14 formats. Those files could not be located. This release has independently computed counts, new byte hashes and verified storage. It makes no byte-identity or count-continuity claim against that unavailable database.
