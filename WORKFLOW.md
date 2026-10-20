# Development workflow

1. Read the state, source definitions and relevant component plan.
2. Choose one capability-level question. Trace requirements, functions, contracts and acceptance criteria before implementation.
3. Preserve the current source baseline and use a task branch for changes needing review.
4. Apply the relevant review skills, repair justified gaps and state the limits of the result.
5. Run targeted checks. Record document consistency, contract readiness, runtime integration and scientific evidence separately.
6. Commit a reviewed change, verify the authorized private remote, and record the returned commit and paths after upload.

User direction: develop capability by capability. Existing LLMs may be used for an initial iteration; semantic neutrality remains a longer-term aspiration rather than an automatically imposed gate. No earlier semantic-neutral runtime is imported or promoted by this snapshot.

Do not run inference or benchmarks merely to store this baseline. Keep the original 192 model scenarios and 24 reference-use scenarios marked planned until actual pinned executions provide evidence.
