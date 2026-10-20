# EDI component architecture work

Inherit the repository-root AGENTS.md and preserve its account, source-freeze and disclosure rules.

For every new or materially revised EDI MVP layer/component design, read and apply `.agents/skills/edi-component-review/SKILL.md` from the repository root. Use the component's current planning document and requirements authority. For Observe, start with `architecture/observation/OBSERVATION_PLAN.md`.

Trace mission, requirements, capabilities, functions, component specifications, verification and evidence. Repair justified in-scope gaps, then reassess the requested gate. Keep the implementation small and the evidence status explicit. Do not impose observation-specific modules, fields or model budgets on other components.

Preserve earlier plans, decisions and failed results. Record architecture approval separately from concrete contracts, runtime qualification and integrated/scientific claims. A skill run or structural check is not proof that a component works. Invoke additional skills for a specific gap and record the affected requirement/decision and resulting evidence.

Update the component plan and root checkpoint after material work. This routing rule adds no authorization for inference benchmarks, paid deployment or public disclosure.

For every new or changed component boundary, port, data/control path, schema, identity/learning path, shared dependency or deployment boundary, apply `.agents/skills/edi-interface-review/SKILL.md`. Review every component pair in both directed lanes, plus indirect/shared-dependency and system feedback paths. Keep internal-part matrices separate. Review all pairs; implement only justified connections. For the current OBS/SUB proposal, start at `architecture/integration/OBSERVATION_SUBSTRATE.md`.
