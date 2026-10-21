# Open investigation world v0.2

**Executable constructed development world. EDI/human reasoning and comparative tests have not run.** This version implements the owner's unguided inquiry scope, preserving the real-source corpus and v0_1 baseline.

The starting material is an objective, authority and generic operations. Participants choose what to read, ask, measure and do. No mandatory hypothesis or expected-observation template, causal-map handoff, relevance classes, question sequence or fixed policy menu is provided.

## Contents

- Twelve constructed stands and 80 years of historical records, including host species, age, foliage, insect/enemy observations, weather and treatment.
- Ten source collections and five source-linked institutional roles.
- 165 archive assets across 16 formats, comprising constructed records and all 28 attributed original-corpus assets. Existing audio/video remain derived numerical representations, not new field recordings. Heat maps share lineage with their underlying samples.
- The full 32,895 original structured rows are accessible through the same public interface, not just chosen excerpts. Their real dates/geographies remain external context. External assets are hash-checked references to the preserved original files, not duplicate binary copies in the new archive.
- Scheduled measurements, treatment/harvest, annual time progression, costs, bounded role inquiry, objective proposals, open final reports and offline outcome accounting.
- One atomic SQLite transaction for world state, job completion, observation publication and committed response. Exact retries and restart recovery do not duplicate interventions.

The ecology now contains direct method-dependent treatment effects on enemy abundance as well as indirect prey-mediated effects; saturation, host/foliage change and mortality are explicit. These are declared engineering assumptions. This is not a quantitative reconstruction of historical New Brunswick and no policy has been tuned to win.

## Restore and run

The compressed archive is stored as fixture/archive.sqlite.gz; the broker restores it with hash verification when needed. The original source corpus must also be restored using ../../scripts/restore.py from this directory. The build uses Pillow for heat maps; runtime and verification use only the Python standard library.

From this directory, set a fresh EDI_BENCHMARK_TOKEN of at least 24 characters, keep the run folder outside Git, and run:

```bash
python broker.py --environment fixture --corpus ../../database/evidence.sqlite --run /tmp/edi-world-run --port 8766
```

The correct corpus relative path from v0_2 is **../../database/evidence.sqlite** (environment/v0_2 -> benchmark root). Verification uses an absolute resolved equivalent.

In another shell, use client.py as documented in PARTICIPANT.md. Create a participant package with:

```bash
python export_participant.py --out /tmp/EDI_World_v02_Participant.zip
python verify.py
python evaluate.py --run /tmp/edi-world-run
```

The export contains exactly the client, mission, operations and participant instructions. It excludes the archive, private world code/state, operator audit, logs and review reports. An actual blind participant still needs separate filesystem/process credentials and permitted network routing; an archive allowlist alone does not establish isolation. Do not mount this owner repository into the participant.

## Workflow and boundaries

The API permits inquiry, work and observation in any supported order; it does not orchestrate EDI's reasoning. Search is full stored text/metadata lexical matching with unfiltered browsing available. Ask discloses a role's frozen source-linked statement, records the actual question and returns explicit limitations; arbitrary conversational expertise is not implemented. The operator should not supply answer-dependent follow-up hints.

Measurements execute after work in their due year and sample the resulting state. Enclosure trials in the archive concern specified fixed conditions, not universal field efficacy. Interventions are simulated, not external actions. Objective proposals remain pending human review; no real person is messaged and no preference is silently adopted.

Year zero archive observations describe the end of that year's transition. Subsequent measurements describe the end of their due year, with event/availability year in each result. Historical observations use declared sampling error; generated observations include their error bound. World evolution is deterministic by seed/place/year. It does not consume a global random stream when a participant asks additional questions.

Native images remain images on read. CSV records can be examined as text; the API does not put a normalized answer table alongside every image. All original assets retain byte hashes. External source explanations may contain expert interpretations; availability in this development archive means this is not a historically blind knowledge condition. A historical-cutoff comparison needs a separately frozen corpus.

## Limits and remaining work

This supports a scripted real-world-style investigation workflow, not a demonstrated EDI problem-solving ability. No human pilot, ecological calibration, historical resource equivalence, unseen-world generalization, adversarial multi-tenant isolation or matched LLM comparison is established. Role inquiry is bounded record disclosure; sampling is annual, not arbitrary continuous-time field science. Native pathogen assays/tree cores and rich visual field campaigns remain unavailable and are disclosed.

Offline evaluation reports outcome dimensions and costs; it does not claim optimum control or score agreement with Meadows. Prospective causal understanding, objective quality and complete model token/compute/energy costs require an EDI integration/evaluation protocol. The broker measures only transport attempts, bytes and service time.

See PLAN.md, PUBLIC_OPERATIONS.json, REQUIREMENTS.json and reports/ for contracts, scientific limits and actual engineering evidence. The initial exploratory build had no historical interventions because its insect dynamics stayed below the trigger; that failed workload check was retained outside the release and the declared growth assumption revised before freezing this fixture. This was a scenario-exercisability correction, not ecological fitting or policy optimization.
