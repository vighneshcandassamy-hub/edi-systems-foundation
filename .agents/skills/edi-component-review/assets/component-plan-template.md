# COMPONENT_NAME plan

Version/date: VERSION. Status: proposed. Architecture gate: pending. Contract gate: pending. Runtime gate: not run. Integration gate: not run.

## Source of truth

Record repository, branch/commit, current requirement catalogue, supporting specs and prior versions. State what supersedes what. Record reviewer role and independence.

## Purpose and boundary

State intended capability, upstream guarantees, downstream consumer, inputs/outputs and non-goals. Separate required behavior, engineering assumptions and proposed mechanisms.

## Requirements and trace

Map mission -> system requirement -> capability/layer requirement -> function -> component specification -> verification -> evidence. Use stable IDs and explicit future allocations. Link the machine authority rather than duplicate it.

## Proposed architecture and alternatives

Show the smallest useful topology. Explain mandatory modules, fields, states, model dependencies and authority. Compare simpler and materially different alternatives. Link current primary-source research where applicable.

## Contracts and operating envelope

Specify types, identity/provenance, state transitions, versions, unknown/error behavior, resource budgets, latency/throughput, retention/recovery and deployment assumptions as applicable. Label unmeasured targets and unresolved choices.

## Critical review and decisions

Record KISS challenge, consequential Five Whys, requirements/verification cascade, scoped coverage partitions, rival hypotheses, failure modes, counterexamples and decision rationale. State findings, gate impact, correction and remaining uncertainty.

## Increment plan

| Increment | Deliverable | Entry condition | Acceptance/evidence | Status |
| --- | --- | --- | --- | --- |
| Contract | Concrete interfaces and fixtures | Architecture review pass | Scoped contract checks | pending |
| Minimal path | Smallest complete implementation | Concrete contract | Integrated component test | pending |
| Reliability/performance | Declared load and faults | Correct minimal path | Measured profile | not run |
| Consumer integration | One real consumer | Qualified component | Intended-use evaluation | not run |

## Verification and claims

Specify one focused integrated campaign, source/configuration/fixture pins, success/failure accounting and reporting. Distinguish documentation checks, runtime verification and scientific/competitive claims.

## Other skills and future revisions

Record contributing skill name/version, focused question, finding, affected requirement/decision, adopted change, check/evidence and updated gate. Preserve rejected alternatives and original failures. Reopen review when interfaces, assumptions, model/backend, workload, fault model or evidence materially changes.

## Next action

State the next concrete authorized action and any actual blocker.
