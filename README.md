# EDI Systems Foundation

The Meadows-based system-of-systems architecture baseline for the next EDI iteration.

**Version:** 0.1.0-architecture. **Status:** conceptual architecture and requirements baseline. Runtime implementation, learning performance and empirical qualification remain open.

This repository brings together the integrated seven-chapter architecture, the appendix semantic reference, retained observation/substrate plans and their review workflows. It preserves source meanings, engineering interpretations, unknowns and evidence status separately.

## Current architecture and saved references

- [Saved asset index](docs/ASSET_INDEX.md) — current architecture, references, requirements, interfaces and skills; pinned GitHub storage audit.
- [Full integrated architecture v0.8](architecture/world-model/Meadows_EDI_Integrated_Architecture_v0_8.md) and [integrated diagram](docs/implementation/INTEGRATED_REASONING_DIAGRAM.md).
- [Consolidated architecture, tools and mathematics reference v1.0](docs/implementation/ARCHITECTURE_TOOLS_AND_MATH_REFERENCE.md).

Latest design/reference additions are stored on `architecture/implementation-tradeoffs-20261020` through [draft PR #1](https://github.com/vighneshcandassamy-hub/edi-systems-foundation/pull/1). Main retains the earlier foundation until that proposal is merged. This is structure/specification work; runtime, training and qualification remain open.

## Foundation and supporting documents

1. [Preserved conceptual foundation v0.7](architecture/world-model/Meadows_Chapters_1_2_3_4_5_6_7_Integrated_Architecture_Audit_v0_7.md) — nine representation families; one master diagram; 54 cumulative requirements; 192 prospective scenarios.
2. [Semantic foundation](architecture/reference/Meadows_Appendix_187_203_Semantic_Foundation_Reference_v1_0.md) — appendix pages 187–203; 18 glossary terms, 40 principles, eight traps, twelve intervention positions, fifteen guidelines and nine model families.
3. [Architecture precedence](architecture/README.md) — how current foundations relate to retained component plans.
4. [Project state](STATE.md), [development roadmap](docs/ROADMAP.md) and [baseline decision](docs/decisions/ADR-001-foundation-baseline.md).
5. [Component review skill](.agents/skills/edi-component-review/SKILL.md) and [interface review skill](.agents/skills/edi-interface-review/SKILL.md).
6. [Implementation architecture and technique assessment](docs/implementation/README.md) — current model/framework tradeoffs, component specifications, requirements flowdown, proposed interfaces and prospective verification profiles, documented before runtime development.

## Retained component plans

- [Observation](architecture/observation/OBSERVATION_PLAN.md) and [component specifications](architecture/observation/COMPONENT_SPECS.md).
- [Substrate plan](architecture/substrate/SUBSTRATE_PLAN.md) and [blueprint](architecture/substrate/SUBSTRATE_BLUEPRINT.md).
- [Observation–substrate interfaces](architecture/integration/OBSERVATION_SUBSTRATE.md).

These plans retain their original evidence and assumptions. Reconcile them against the current architecture and semantic reference before implementation. Their previous document-check results do not qualify a new runtime or settle every later semantic decision.

## Verify this snapshot

```sh
python scripts/verify_baseline.py
```

This checks preserved-file hashes, canonical source allocations, requirement/case identifiers, the master graph, key reference counts and credential-pattern exclusion. It does not run the 192 architecture scenarios or the 24 reference-use scenarios. Those catalogues overlap and must not be presented as 216 independent tests.

## Provenance and ownership

Intended private GitHub destination: `vighneshcandassamy-hub/edi-systems-foundation`.
The previous research repository is [edi-lab](https://github.com/vighneshcandassamy-hub/edi-lab). It remains the source for earlier implementations, experiments and their original limitations.

[Import manifest](evidence/import_manifest.json) records exact file hashes and source identity. The source book is an external reference; this snapshot contains the architecture's analysis and paraphrased appendix reference. No model weights or inference credentials are required.
