# Interface and system checklist

For each contract specify these eleven facets. Reuse a profile only when it truly applies; override operation-specific behavior. A reference to an authoritative document is acceptable; a generic assurance is not.

| Facet | Questions |
| --- | --- |
| ownership | Who produces, admits, commits and retains each state? What does the consumer own? |
| authority | Which reads, proposals, mutations and external actions are permitted? Which are denied? |
| shape_versions | Native shape, selectors, required/optional/unknown fields, units, schema/model compatibility, migration and unsupported extensions? |
| identity_scope | Scope, occurrence versus payload identity, source epochs, association versus physical identity, alias/correction lineage? |
| time_order | Valid/event/receipt/commit/knowledge/model times, clock uncertainty, ordering, watermarks, gaps and late corrections? |
| delivery_idempotency | Request/occurrence IDs, duplicate/reorder/loss/retry rules, unknown completion, cancellation and reconnection? |
| commit_recovery | Staged versus durable receipt, atomicity boundary, applied IDs/checkpoints, restart, stale/conflicting writers and repair? |
| retention | Availability horizon, tombstones, reference lifetime, evidence eviction, derived-state consequences and export/restore? |
| resource_limits | Admission, bytes/items/work/time/tokens/cost, concurrency, partial reads, queue growth and overload/fairness? |
| errors | Unknown/unavailable/unsupported/denied/conflict/timeout/cancelled/partial outcomes, retryability and error attribution? |
| feedback_grounding | Shared evidence/dependencies, selection history, generated echoes, model assistance and actual versus simulated outcomes? |

Inspect every directed lane, including justified no-links. A one-way signal may need a separate query or status lane. Distinguish transport acknowledgements from accepted mutations and independently observed effects. Never infer causal influence from software direction.

For the system, inspect:

- Indirect paths and shared store/model/clock dependencies that bypass apparent boundaries.
- Multi-party interactions and strongly connected groups, not just two-way pairs.
- Feedback gain/sign, delay, retries, self-confirmation, attention/selection bias and competing authority.
- Backpressure cycles, circular waits, saturation, bounded work and failure isolation.
- Crash during each handoff, committed cursor consistency, stale state and recovery ownership.
- Cross-version schema/embedding spaces, migrations and replay compatibility.
- Complete path cost, including model context, derivation, retries, failed work and storage.
- Source/action authority outside the component registry, and denied or impossible requests.

Use KISS and Five Whys to justify each connection and each retained state. Use failure modes and counterexamples to check the design. Keep requirements flowdown and verification return links. Treat coverage axes separately; modalities and functions need not be mutually exclusive.

Architecture review can establish a coherent proposal with declared assumptions; it cannot demonstrate measured throughput, high availability, source identity, learning or superiority. Concrete contracts, runtime tests and controlled learning evidence are separate gates.
