# Development corrections

This log records engineering corrections, not scientific benchmark results.

- The first fixture had 28 initial and 116 requestable items and passed its HTTP engineering checks.
- Same-species/same-plot biochemical and needle-assay distractions plus a controlled biochemical contrast were then added. The fixture became 30 initial and 129 requestable items. An old initial-count assertion still expected 28; it failed and was updated to the new explicit inventory. No access-control, integrity or scoring acceptance was weakened.
- Review found that the audit stored a request hash but not the actual rationale/expected observation. The journal was changed to retain the full pre-acquisition request, and the verification now checks exact recovery of rationale, alternatives and expected observation. Older incompatible journals are rejected with an instruction to preserve them and use a new run directory.
- HTTP retries and denied attempts are recorded separately from idempotent logical acquisitions so transport cost is not hidden or double-counted as new evidence.
- Normalized branch-density values now explicitly state their 75 cm equivalent basis; raw branch-length method context must not silently change the reported density denominator.

All final check outcomes refer to the final pinned code and fixture. No EDI/human inference run occurred during these corrections.
