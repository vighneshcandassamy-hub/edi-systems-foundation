# ADR-002: a hybrid implementation with explicit model and evidence authority

Date: 20 October 2026. Status: proposed architecture for owner review. Supersedes no source snapshot or historical runtime qualification.

## Problem

The seven-chapter/appendix conceptual model and the owner-supplied overview do not specify which software should own state, which current AI techniques should propose or test relationships, or how integration will preserve evidence and timing. Selecting a model or a graph database alone cannot satisfy those contracts.

## Decision

Propose eight logical application owners in a modular Python codebase, a canonical transactional model/evidence authority with source-native artifacts, a replaceable pretrained reasoning/perception provider, and typed adapters for causal, statistical, quantitative and qualitative analysis. One owner admits model revisions; source evidence, generated trials, original forecasts and actual execution remain distinct. Use a finite operating profile and one prospective integrated capability path before broader comparisons.

Compare current hosted/open-weight models and mature frameworks in [the implementation tradeoffs](../implementation/TRADEOFFS.md). Prefer the simplest complete owner/contract implementation first; Neo4j, Graphiti, LangGraph, Temporal, learned latent dynamics and specialist solvers have explicit conditional adoption triggers rather than becoming mandatory infrastructure.

## Consequences

There is more integration work than one long-context prompt, but state, provenance, numerical semantics, uncertainty and revisions become inspectable. Model-only, conventional retrieval, temporal graph and structured-model alternatives remain legitimate strong controls. Nothing establishes superior intelligence, energy savings or arbitrary scale before matched measurements.

This package allocates requirements and proposes interfaces. It does not retroactively pass the retained substrate contracts, execute any of the existing scenarios, train a new model or authorize external actuation. Concrete schemas, numerical grammar, dependency pins, first fixture and profile are implementation entry conditions. The full [specification index](../implementation/README.md) and [verification plan](../implementation/VERIFICATION.md) define the scoped gates.
