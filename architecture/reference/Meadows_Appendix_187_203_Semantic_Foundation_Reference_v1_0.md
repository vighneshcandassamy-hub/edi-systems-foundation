# Meadows Appendix: semantic foundation reference for the integrated architecture

Version 1.0 | 20 October 2026 | Source scope: printed pages 187–203 inclusive

## 1. Purpose, authority and review status

This is a separate, source-anchored reference asset for the architecture developed from Chapters 1–7 of Donella H. Meadows, *Thinking in Systems*, edited by Diana Wright. It consolidates the appendix vocabulary, principles, traps, intervention positions, practical guidelines and nine illustrative model families. It does not reproduce the appendix or replace the book. Source meanings below are paraphrased; engineering contracts and qualifications are explicitly our interpretation.

Source: *Meadows-2008.-Thinking-in-Systems(3).pdf*, stable identity `libfile_b37e53e90794819197f19f233af940d2`, content `file_000000000a10821198286322dbd247fa`; 235 PDF pages. Printed page p maps to PDF page p+17 for this range. All 17 requested appendix pages were read. Graph-containing printed pages 197, 198, 199, 201, 202 and 203 were also inspected as rendered page images. Curves were not digitized and model dynamics were not run.

Architecture input: *Meadows_Chapters_1_2_3_4_5_6_7_Integrated_Architecture_Audit_v0_7.md*, internal v0.7, stable identity `libfile_7b9b477f82208191ab94058fbf22e04e`, content `file_0000000003ec8211987dd8b867e28011`, saved version 5. The selected attachment with an older v0.4 name failed to reach the workspace; this review used the successfully retrieved current saved seven-chapter item. That item was not modified by this task.

**Semantic authority policy:** preserve the supplied source meaning as historical/source evidence. Use the engineering contract when building or composing model records. Label extensions, assumptions, disagreements and unresolved source conventions. Do not silently rewrite Meadows to agree with our schema, or use a concise appendix sentence to erase qualifications developed in the chapters. If a later architecture changes a meaning, retain both versions and document the correspondence.

**Accepted scope:** a working semantic foundation and source-to-architecture allocation. **Open scope:** exact numerical reproduction where source conventions or graph values are incomplete. **Unqualified scope:** executable dynamics, empirical causation, prediction quality, intervention success, autonomous learning and runtime performance.

The appendix is reviewed here as **102 catalogue entries**: 18 glossary terms, 40 summary principles, 8 traps, 12 intervention positions, 15 guidelines and 9 model families. These counts are our catalogue organization, not 102 independent discoveries or primitives. The 32 engineering extension terms in section 4 are additional explanatory vocabulary. Twenty semantic requirements and 24 prospective cases support future use; **all 24 cases are PLANNED — NOT RUN**. They overlap earlier obligations and are not additions to the 192-case master catalogue unless explicitly incorporated in a later revision.

## 2. Source map and reading ledger

| Printed page | PDF page | Reviewed content |
| --- | --- | --- |
| 187 | 204 | Glossary: first twelve terms, from archetypes through reinforcing feedback. |
| 188 | 205 | Glossary: six remaining terms; Systems principles; first five stock/flow principles. |
| 189 | 206 | Two stock/buffer principles; six feedback principles; three dominance/delay principles; opening scenario principle. |
| 190 | 207 | Second scenario principle; constraints; resilience/organization/hierarchy; first seven surprise principles. |
| 191 | 208 | Bounded-rationality surprise principle; three model principles; policy resistance, commons and opening performance drift. |
| 192 | 209 | Performance drift, escalation, compounding advantage and opening burden-shifting trap. |
| 193 | 210 | Burden-shifting continuation, withdrawal/capability recovery, rule beating and wrong goal. |
| 194 | 211 | Twelve intervention positions and first eleven living-with-systems guidelines. |
| 195 | 212 | Four remaining guidelines; numerical-model introduction/converters; bathtub and opening coffee equations. |
| 196 | 213 | Coffee warming/cooling, bank compounding and opening thermostat state equation. |
| 197 | 214 | Thermostat parameters and graph-defined daily outside-temperature driver; opening population model. |
| 198 | 215 | Population rates and changing fertility; first fertility graph; opening capital heading. |
| 199 | 216 | Second fertility graph; capital accumulation/depreciation; opening inventory specification. |
| 200 | 217 | Inventory converters, delay variants and order-expression ambiguity; opening finite-resource model. |
| 201 | 218 | Finite-resource/capital equations and nonlinear curves; questionable figure-range label; opening renewable-resource heading. |
| 202 | 219 | Renewable-resource/capital equations; graph-defined price and renewal-rate description. |
| 203 | 220 | Renewal-rate and three yield curves; distinction between renewal coefficient and total flow. |

The appendix has six source sections: glossary (187–188); summary principles (188–191); trap summaries (191–193); intervention positions (194); living-with-systems guidelines (194–195); model equations and graphs (195–203). Source headings can share a page; the page ranges are not mutually exclusive.

## 3. Canonical source glossary with engineering meaning

AD identifiers below belong to this reference. The source glossary contains eighteen entries. Terms used in the chapters or added in our design are kept in section 4 rather than falsely described as additional appendix glossary entries.

| ID | Source term | Printed page | Source meaning, paraphrased | Operational meaning | Qualification | Architecture requirements |
| --- | --- | --- | --- | --- | --- | --- |
| AD01 | Archetypes | 187 | Recurring structural arrangements associated with characteristic behavior patterns. | A candidate pattern view over shared actors, stocks, rules and feedback paths. | A familiar pattern is a hypothesis; necessary paths and rival mechanisms must be inspected. | I7-R13, I7-R21, I7-R30 |
| AD02 | Balancing feedback loop | 187 | A return path that counteracts a change and tends to regulate a condition. | Specify the complete stock-to-rate return, reference if applicable, response, delay and capacity. | Balancing polarity alone does not prove stable convergence or beneficial outcomes. | I7-R04, I7-R19, I7-R36 |
| AD03 | Bounded rationality | 187 | Choices can be understandable locally while appearing unreasonable from a wider view. | Attribute available information, interpretation, memory, purposes and perceived options to each actor. | This does not mean every actor optimizes, lacks reason, or knows the analyst state. | I7-R10, I7-R15, I7-R41 |
| AD04 | Dynamic equilibrium | 187 | A stock remains constant while its incoming and outgoing flows balance. | Compare gross rates as well as the resulting level at the relevant temporal resolution. | Constant level is not zero throughput, zero risk, resilience or demonstrated stability. | I7-R02, I7-R03, I7-R12 |
| AD05 | Dynamics | 187 | The time-dependent behavior of a system or component. | Retain states, rates, events, variation, regimes and consequential organizational history. | A current snapshot cannot by itself identify a trajectory or its cause. | I7-R03, I7-R12, I7-R43 |
| AD06 | Feedback loop | 187 | A closed causal chain lets a stock influence a flow that changes that stock. | Record the ordered participating mechanisms, applicability, timing, shared supports and closure evidence. | A two-way software exchange, correlation or directed cycle in a diagram is not sufficient causal evidence. | I7-R04, I7-R09, I7-R11 |
| AD07 | Flow | 187 | Material or information entering or leaving an accumulation over time. | For numerical stock accounting, distinguish amount transferred from rate; declare time basis, endpoints and conversion. | Not every information message or organizational process changes a defined stock. | I7-R02, I7-R04, I7-R44 |
| AD08 | Hierarchy | 187 | Subsystems participate in an organized larger system. | Represent composition separately from authority, reporting, supply and cross-level coordination. | A hierarchy can coexist with overlapping memberships and network interfaces. | I7-R01, I7-R09, I7-R10 |
| AD09 | Limiting factor | 187 | A required input currently restricts system activity. | Specify the joint input requirements, actual availability, capacities and context-dependent active constraint. | The limiting input can change; complementary inputs and joint bottlenecks may matter together. | I7-R04, I7-R18, I7-R35 |
| AD10 | Linear relationship | 187 | A relationship has constant proportional response over the range being described. | Record variables, units, slope, domain and intercept convention. Distinguish strict linearity from an affine line. | A straight line over one range is not a universal law; mathematical additivity needs its stated assumptions. | I7-R13, I7-R16, I7-R32 |
| AD11 | Nonlinear relationship | 187 | Response is not proportional across the described range. | Represent applicable shape, thresholds, saturation, conditional rules and uncertainty. | Nonlinearity does not automatically imply chaos, unpredictability or a unique regime change. | I7-R04, I7-R16, I7-R32 |
| AD12 | Reinforcing feedback loop | 187 | A return path amplifies a change in its existing direction. | Specify the actual return mechanism, gain conditions, limits and competing paths. | Amplification may be useful or harmful; exact exponential behavior requires additional assumptions. | I7-R04, I7-R23, I7-R36 |
| AD13 | Resilience | 188 | A system can recover or restore functioning after perturbation. | Attribute functioning or regime, disturbance, recovery horizon, resources, alternatives and evidence. | Finite resilience is not equivalent to fixed equilibrium, high output or an unconditional scalar score. | I7-R06, I7-R07, I7-R36 |
| AD14 | Self-organization | 188 | A system can generate or alter its own organization, with learning or diversification among the source examples. | Specify actual generating, selecting and retaining processes, resources and state/history correspondence. | Observed structural change, useful adaptation, learning and analyst model revision are distinct claims. | I7-R08, I7-R14, I7-R39 |
| AD15 | Shifting dominance | 188 | Competing feedback paths change their relative influence over time. | Track interacting mechanisms, applicable states, limits and intervals of influence. | Changing behavior can occur without a changed graph; a topology change is a different hypothesis. | I7-R04, I7-R12, I7-R16 |
| AD16 | Stock | 188 | Material or information accumulated through system history. | Identify the accumulated subject, units, relevant state, input/output processes and initial/history conditions. | Not every state, capability, value or intensive variable is literally an accumulated conserved quantity. | I7-R02, I7-R03, I7-R33 |
| AD17 | Suboptimization | 188 | A subsystem pursues its goals at the expense of wider system goals. | Compare owned local purposes, shared constraints, distributed consequences and wider criteria. | There need not be an agreed global welfare function; wider and local priorities require attribution. | I7-R05, I7-R10, I7-R26, I7-R50 |
| AD18 | System | 188 | An organized, interconnected set of constituents produces characteristic functioning or behavior. | Specify constituents, relationships, mechanisms, selected view, external exchanges and function/purpose claims. | A named collection alone does not establish a functional system; purpose need not imply conscious intention. | I7-R01, I7-R05, I7-R09, I7-R17 |

### 3.1 Important semantic refinements

- **Flow versus rate:** preserve the source's broad entry while making numerical amount/time semantics explicit. A message can influence a response without being an inflow to a separately defined information stock.
- **Stock versus state:** a stock accumulates something. A variable needed for state, a capacity limit, an ordinal quality rating and a temperature proxy are not automatically the same type. Source models can legitimately use normalized proxies if their assumptions are declared.
- **Feedback versus connection:** a signal, reciprocal communication and a graph cycle do not establish the stock-dependent causal return required by a system-dynamics feedback claim.
- **Polarity versus outcome:** balancing/reinforcing describe directional return under stated conditions. They do not imply good/bad, stable/unstable, exactly exponential, or globally correct action.
- **Organization versus understanding:** structural change in the world, learning by an actor and revision by the analyst have different ownership and evidence. The glossary's broad self-organization entry does not collapse these distinctions.
- **Function versus intention:** observed system functioning may be attributed without inventing a conscious controller or shared goal.

## 4. Extended vocabulary used by the architecture

These are engineering distinctions and terms used beyond the eighteen-entry appendix glossary. The anchor column identifies their source context; the wording is ours. E identifiers do not assert that Meadows used a separate glossary definition for every term.

| Extension | Term | Working definition | Source anchor | Architecture requirements |
| --- | --- | --- | --- | --- |
| E01 | Element/constituent | A persistent participating referent; may itself have a system view. | System definition | I7-R01 |
| E02 | Interconnection/interface | A typed directed physical, informational or institutional relationship between specific participants. | System/feedback/hierarchy | I7-R09 |
| E03 | Composition/membership | Which constituents participate in a view or assembly, distinct from exchange or command. | Hierarchy | I7-R01, I7-R09 |
| E04 | Function | Observed or modeled contribution of an arrangement. | System definition | I7-R05 |
| E05 | Purpose | Intended or inferred outcome attributed to a subject, with evidence and scope. | System/suboptimization | I7-R05, I7-R40 |
| E06 | Goal/reference | A desired condition actually used by a response, with owner and update history. | Balancing loop | I7-R05, I7-R23 |
| E07 | Criterion/value | An attributed basis for judging outcomes, possibly qualitative or contested. | Guidelines5/7/14/15 | I7-R45, I7-R50 |
| E08 | Indicator/proxy | A selected measure used to stand for a broader outcome; correspondence must be checked. | Wrong-goal trap | I7-R26 |
| E09 | State variable | A quantity required to describe current conditions; may be accumulation, proxy or other state. | Stock/dynamics; model equations | I7-R02, I7-R03 |
| E10 | Rate versus interval amount | Rate has amount/time units; an interval transfer equals its appropriately integrated rate. | Flow and stock equations | I7-R02, I7-R44 |
| E11 | Converter/derived variable | A constant or calculation from other model elements; the appendix names this explicitly. | Model introductionp195 | I7-R02, I7-R04, I7-R44 |
| E12 | Parameter | A setting or coefficient for a particular mechanism, with units, scope and mutability. | Leverage12 | I7-R32 |
| E13 | Constraint/capacity | A feasibility condition or throughput bound; not automatically usable accumulated reserve. | Limiting factor/leverage11 | I7-R18, I7-R33 |
| E14 | Buffer | An accumulation used to absorb a mismatch, relative to actual flows and accessibility. | Stock principles/leverage11 | I7-R33 |
| E15 | Delay/memory | Retained causal timing or state; not every delay is an additional material stock. | Principles18–20 | I7-R03, I7-R19, I7-R35 |
| E16 | Initial condition/prehistory | Starting state plus prior history required by delayed mechanisms. | Model equations | I7-R03, I7-R14 |
| E17 | Boundary/closure | The selected view and treatment of omitted sources, sinks, exchanges and drivers. | Principle31 | I7-R17 |
| E18 | External driver | An input treated as given relative to a view; may be internal in another view. | Scenarios/constraints | I7-R17, I7-R19 |
| E19 | Event/pattern/regime | Occurrence, temporal characterization and operating context are different descriptive roles. | Dynamics/principle4 | I7-R11, I7-R43 |
| E20 | Mechanism/causal claim | An evidence-qualified account of how specified conditions generate effects. | Feedback/system | I7-R04, I7-R11 |
| E21 | Observation/report/inference | Measurement or inspection, source account and interpretive conclusion have distinct evidential status. | Mindsets and guidelines | I7-R11, I7-R53 |
| E22 | Model/scenario/prediction | A versioned account, chosen conditional configuration and its expected result are separate records. | Scenarios/testing | I7-R12, I7-R48 |
| E23 | Policy/intention/execution | Current response rule, attempted action and realized process effect are distinct. | Bounded rationality/guideline6 | I7-R15, I7-R46 |
| E24 | Policy review/adoption | Owned monitoring and proposed amendment differ from an authorized implemented change. | Guideline6/leverage5 | I7-R38, I7-R47 |
| E25 | Analyst revision | An update to the explanatory account, not automatically a change in the actual system. | Mindsets/guideline2 | I7-R08, I7-R48 |
| E26 | Repair/restoration/support | Restoring a damaged mechanism differs from temporary compensation and its enabling resources. | Resilience/burden trap | I7-R07, I7-R25 |
| E27 | Variation/selection/retention | Separate processes that may produce persistent new organization. | Self-organization | I7-R39 |
| E28 | Actor frame/analyst frame | Owned interpretive assumptions differ from those used by the modeler. | Bounded rationality/leverage2 | I7-R41, I7-R42 |
| E29 | Consequence incidence/responsibility | Who experiences effects differs from influence, authority, knowledge and normative attribution. | Commons/guideline9 | I7-R22, I7-R49 |
| E30 | Affected-party/evaluative scope | Who is affected differs from who is causally modeled and whose interests are considered. | Guidelines7/14 | I7-R50 |
| E31 | Uncertainty/alternative | An unresolved value, mechanism or claim and its rivals are retained with applicability. | Mindsets/guideline10 | I7-R11, I7-R48, I7-R54 |
| E32 | Meaning/measurement correspondence | Shared terms and numerical scales require referents, permissible operations, timing and domain mapping. | Linear/nonlinear; guidelines4/5/13 | I7-R44, I7-R45 |

### 4.1 Meanings that must not be merged

| Keep separate | Reason |
| --- | --- |
| Constituent / measured variable / role | A tree, its biomass and its role as host refer to different things. |
| Stock level / flow rate / capacity / usable reserve | They have different units and different histories. |
| Physical law / institutional rule / belief / criterion | Changing an institution or assumption does not repeal physical constraints or settle values. |
| Composition / information / transfer / authority | A part-of relation is not permission to control or proof of communication. |
| Dynamic equilibrium / stability / resilience | A steady level does not establish return after disturbance or ability to recover. |
| Actual / observed / reported / perceived / predicted | These are separately qualified accounts, not separate physical copies or interchangeable truth. |
| Event / temporal pattern / structural mechanism | An occurrence and its generating explanation are distinct; direct structural observations are possible. |
| Published / received / attended / understood / actionable | Information quantity does not itself supply effective feedback. |
| Policy / intended action / execution / consequence | A response rule and a desired outcome do not guarantee a feasible process effect. |
| Proposed / announced / adopted / implemented / observed effective | Each requires its own evidence and transition semantics. |
| Source definition / engineering extension / tested implementation | A semantic reference is not an implemented algorithm or performance result. |
| Causal inclusion / affected-party coverage / evaluative priority | Representing an effect does not prescribe how all parties must value it. |
| Regeneration coefficient / total regeneration / harvest | The renewable model multiplies the coefficient by the current stock. |
| Per-capita rate / total flow / net growth | Fertility, births and births-minus-deaths are different quantities. |
| Source ambiguity / documented interpretation / silent repair | Only an explicit named interpretation supports reproducible implementation. |

## 5. Forty source principles and their architectural use

The forty bullet principles on printed pages 188–191 are allocated individually. Paraphrases retain the source topic; qualifications explain how we will use them without turning heuristics into universal laws.

| ID | Topic | Printed page | Source principle, paraphrased | Engineering interpretation / qualification | Architecture requirements | Prospective case |
| --- | --- | --- | --- | --- | --- | --- |
| AP01 | Systems | 188 | Organized wholes have properties that are not obtained by listing isolated parts. | Represent relations and generating mechanisms as well as constituents; emergence is not a separate force. | I7-R01, I7-R04, I7-R09 | AF-T01 |
| AP02 | Systems | 188 | Information carries many system interconnections. | Specify directed content, receipt, interpretation and use; not every dependence is informational. | I7-R09, I7-R15, I7-R37, I7-R53 | AF-T08 |
| AP03 | Systems | 188 | Function or purpose can be consequential even when less visible than components. | Keep attributed operating purpose, stated objective, reference, proxy and criterion distinct. | I7-R05, I7-R26, I7-R40 | AF-T16 |
| AP04 | Systems | 188 | Structure generates behavior, which appears as events through time. | Connect mechanisms, conditions and history; events and patterns do not identify a unique structure. | I7-R04, I7-R11, I7-R12, I7-R43 | AF-T02 |
| AP05 | Stocks/flows | 188 | Current stock retains the history of net flows. | Initialize relevant stocks and additional history such as queues, cohorts and pending effects. | I7-R02, I7-R03, I7-R14 | AF-T03 |
| AP06 | Stocks/flows | 188 | Excess inflow increases a stock. | Apply to compatible gross rates over the declared interval; distinguish derivative from sampled level. | I7-R02, I7-R04 | AF-T03 |
| AP07 | Stocks/flows | 188 | Excess outflow reduces a stock. | Retain removal destinations or loss conventions and actual feasibility limits. | I7-R02, I7-R04, I7-R18 | AF-T03 |
| AP08 | Stocks/flows | 188 | Equal incoming and outgoing rates leave a stock unchanged. | Inspect throughput and composition; endpoint equality alone can conceal intermediate variation. | I7-R02, I7-R03 | AF-T03 |
| AP09 | Stocks/flows | 188 | Reducing outflow can increase stock as increasing inflow can. | Compare alternative process changes, delays, costs and effects elsewhere. | I7-R02, I7-R12, I7-R31 | AF-T04 |
| AP10 | Stocks/flows | 189 | Accumulations can buffer disturbances and delay response. | Relate usable reserve to actual rates, accessibility and replenishment rather than capacity alone. | I7-R03, I7-R06, I7-R33 | AF-T09 |
| AP11 | Stocks/flows | 189 | Stocks can decouple the immediate timing of incoming and outgoing activity. | Represent buffering within finite bounds; rates remain connected through stock and other mechanisms. | I7-R02, I7-R04, I7-R33 | AF-T04 |
| AP12 | Feedback | 189 | Feedback returns stock-dependent influence through a flow to the stock. | Trace the complete ordered physical/rule/information path and its evidence. | I7-R04, I7-R09, I7-R36 | AF-T06 |
| AP13 | Feedback | 189 | Balancing loops support regulation and can resist change. | Specify reference, sign, timing, capacity and disturbance; do not equate balancing with assured stability. | I7-R04, I7-R19, I7-R36 | AF-T06 |
| AP14 | Feedback | 189 | Reinforcing paths can amplify growth or decline. | Exact exponential trajectories require the relevant proportional law and conditions, not the loop label alone. | I7-R04, I7-R16, I7-R36 | AF-T05 |
| AP15 | Feedback | 189 | A returning signal cannot change the past behavior that generated it. | Use availability and decision times; later feedback can affect subsequent action or history interpretation, not past physical effects. | I7-R03, I7-R15, I7-R19, I7-R48 | AF-T07 |
| AP16 | Feedback | 189 | A regulating reference/response must account for other stock-changing processes. | Check disturbances, external inflows/outflows and steady-state offset; desired stock need not be achieved. | I7-R04, I7-R05, I7-R36 | AF-T06 |
| AP17 | Feedback | 189 | Similar feedback organization can support analogous behavior. | Require domain roles, response laws, units, times and conditions before transferring parameters or conclusions. | I7-R13, I7-R16, I7-R44 | AF-T12 |
| AP18 | Dominance/delays | 189 | Changes in relative feedback influence can produce complex behavior. | Distinguish an operating-point change under fixed mechanisms from changed parameters, rules or topology. | I7-R04, I7-R12, I7-R16 | AF-T05 |
| AP19 | Dominance/delays | 189 | Delayed balancing can oscillate. | Check delay together with response intensity, other dynamics and capacity; delay alone is not a universal instability proof. | I7-R19, I7-R35, I7-R36 | AF-T07 |
| AP20 | Dominance/delays | 189 | Changing delay can materially change behavior. | Identify perception, decision, implementation and physical-completion stages separately. | I7-R03, I7-R19, I7-R35 | AF-T07 |
| AP21 | Scenarios/testing | 189 | Models can explore conditional futures and what-if questions. | Declare model version, initial/history state, drivers, interventions, horizon and analysis limitations. | I7-R11, I7-R12, I7-R31 | AF-T12 |
| AP22 | Scenarios/testing | 190 | Plausible response patterns matter when exact future drivers cannot be known. | Assess mechanism response and scenario relevance separately; this is not permission to ignore impossible inputs or assert actual forecasts. | I7-R12, I7-R13, I7-R31, I7-R54 | AF-T12 |
| AP23 | Constraints | 190 | Finite physical environments cannot support unlimited exponential growth. | Represent actual resource/source/sink/capacity closure and limiting feedback where relevant; do not force every decline into the same mechanism. | I7-R04, I7-R17, I7-R18 | AF-T04 |
| AP24 | Constraints | 190 | Nonrenewable resource use is limited by remaining stock. | Include depletion, access, quality, extraction rate and substitution assumptions. | I7-R02, I7-R04, I7-R18 | AF-T04 |
| AP25 | Constraints | 190 | Renewable resource use is constrained by renewal flows. | Renewal depends on resource condition and operating context; a renewable label is not guaranteed sustainability. | I7-R02, I7-R04, I7-R16, I7-R18 | AF-T23 |
| AP26 | Resilience/organization | 190 | Resilience has limits. | State disturbance type, magnitude, duration, functioning, shared supports and recovery conditions. | I7-R06, I7-R07, I7-R36 | AF-T09 |
| AP27 | Resilience/organization | 190 | Productivity and stability alone are insufficient management criteria. | Expose resilience, future capability and other relevant tradeoffs without prescribing a universal weighting. | I7-R05, I7-R06, I7-R25, I7-R50 | AF-T16 |
| AP28 | Resilience/organization | 190 | Some systems generate new organization and capabilities. | Specify generating/selection/retention mechanisms; novelty does not guarantee useful learning. | I7-R08, I7-R14, I7-R39 | AF-T10 |
| AP29 | Resilience/organization | 190 | The source links hierarchy with bottom-up development and service to lower levels. | Treat historical development as an empirical claim and service to lower layers as a design perspective; neither is a theorem about every hierarchy. | I7-R01, I7-R09, I7-R10, I7-R50 | AF-T11 |
| AP30 | Surprises | 190 | Many relationships are nonlinear. | Retain conditional domains, limits and unknown functional forms; do not invent a curve to fit a story. | I7-R04, I7-R16, I7-R32 | AF-T05 |
| AP31 | Surprises | 190 | Boundaries are selected within an interconnected world. | Record omissions, shared referents and external-input closure; widening analysis is not physical reorganization. | I7-R01, I7-R09, I7-R17 | AF-T01 |
| AP32 | Surprises | 190 | The currently scarce necessary input can dominate activity. | Represent complementary requirements, shared resources and evolving active constraints. | I7-R04, I7-R18 | AF-T04 |
| AP33 | Surprises | 190 | Systems with many inputs and outputs face multiple layers of limits. | Trace upstream/downstream conditions and common dependencies as bottlenecks shift. | I7-R04, I7-R09, I7-R18 | AF-T04 |
| AP34 | Surprises | 190 | Growth encounters limits. | Specify the finite environment and actual mechanism; growth in one metric need not imply the same bound for every abstract quantity. | I7-R04, I7-R17, I7-R18 | AF-T04 |
| AP35 | Surprises | 190 | Exponential growth can approach a limit rapidly. | Distinguish doubling time, remaining margin, feedback delay and uncertain thresholds. | I7-R03, I7-R16, I7-R19, I7-R35 | AF-T07 |
| AP36 | Surprises | 190 | Long delayed effects make anticipatory attention important. | Represent commitments and conditional forecasts without granting actors future knowledge. | I7-R03, I7-R15, I7-R19, I7-R51 | AF-T07 |
| AP37 | Surprises | 191 | Locally understandable decisions can fail to promote wider welfare. | Compare actor information, authority and local/wider consequences; do not assume irrationality or one agreed optimum. | I7-R10, I7-R15, I7-R26, I7-R50 | AF-T08 |
| AP38 | Mindsets/models | 191 | Knowledge of the world is mediated by models. | Expose claims, assumptions, definitions, source status and alternative explanations. | I7-R11, I7-R41, I7-R42, I7-R48 | AF-T18 |
| AP39 | Mindsets/models | 191 | Models can meaningfully correspond to the world. | Treat correspondence as a question for evidence and applicability, not automatic validation of a preferred account. | I7-R11, I7-R12, I7-R13, I7-R48 | AF-T12 |
| AP40 | Mindsets/models | 191 | Models remain incomplete descriptions of reality. | Preserve unknowns and scope limits while allowing justified provisional decisions. | I7-R11, I7-R12, I7-R42, I7-R54 | AF-T20 |

## 6. Eight traps and qualified opportunities

Each source trap and way-out suggestion is an analytical view over existing mechanisms. The recommendation column paraphrases source guidance. It is not a universally effective intervention or an empirical finding of this review.

| ID | Trap | Printed pages | Structural condition | Source opportunity, paraphrased | Required qualification | Architecture requirements |
| --- | --- | --- | --- | --- | --- | --- |
| AT01 | Policy resistance | 191 | Different actors correct toward incompatible conditions. | Seek participation, mutual accommodation or revised wider purposes. | Agreement/adoption is not guaranteed; preserve genuine conflicts and actual authority. | I7-R21, I7-R23, I7-R28 |
| AT02 | Tragedy of the commons | 191 | Private gains combine with distributed costs and weak resource-to-user feedback. | Strengthen understanding and consequence feedback; compare access governance or ownership arrangements. | Privatization and regulation are conditional options with distribution/enforcement effects. | I7-R21, I7-R22, I7-R28 |
| AT03 | Drift to low performance | 191–192 | Perceived past performance shifts the standard and weakens corrective pressure. | Protect standards or use better demonstrated performance to support higher aspiration. | Distinguish erosion from legitimate revision of an infeasible or contested standard. | I7-R23, I7-R26, I7-R52 |
| AT04 | Escalation | 192 | Reciprocal rival comparisons drive reinforcing attempts to surpass the other. | Avoid the race, interrupt participation, or negotiate countervailing arrangements. | A linear-looking rivalry diagram does not prove exact exponential escalation or feasible disarmament. | I7-R21, I7-R23, I7-R28 |
| AT05 | Success to the successful | 192 | Rewards provide means that improve future competitive success. | Compare diversification, concentration limits, reduced advantage or different reward conversion. | Actual conversion, entry, institutions and shared limits determine outcomes. | I7-R21, I7-R24, I7-R28 |
| AT06 | Shifting the burden to the intervenor | 192–193 | Relief or hidden symptoms combine with failure or erosion of original corrective capability. | Rebuild underlying capability; an intervenor should support self-maintenance and plan withdrawal. | Relief is not inherently addiction; withdrawing before recovery can cause harm. | I7-R21, I7-R25, I7-R28 |
| AT07 | Rule beating | 193 | Adaptation achieves apparent formal compliance while defeating the intended purpose. | Redesign rules and incentives toward their purpose and allow subsequent adaptation. | Compliance, motive and consequences need evidence; rule redesign may produce new strategies. | I7-R21, I7-R26, I7-R27, I7-R28 |
| AT08 | Seeking the wrong goal | 193 | Incomplete indicators or goals steer activity away from intended welfare. | Choose outcome-relevant purposes and indicators and distinguish effort from result. | No perfect proxy or universally agreed welfare measure follows from the recommendation. | I7-R21, I7-R26, I7-R40, I7-R50 |

All eight use AF-T13 and AF-T14 as prospective semantic checks. Preserve shared resources and mechanisms across simultaneous trap hypotheses. Never add the predicted benefits of several remedies without a joint scenario, transition account and distributional assessment.

## 7. Twelve intervention positions

All positions are on printed p. 194. The appendix labels the order by increasing effectiveness. Chapter 6's retained assessment qualifies this ordering as tentative and context-dependent. We preserve the appendix presentation as source evidence and use no fixed rank-to-efficacy score. The final position is operationalized here as revisability, not implemented enlightenment.

| ID | Position | Source name | Operational target | Architecture requirements |
| --- | --- | --- | --- | --- |
| AL12 | 12 | Numbers | Parameters, constants and settings | I7-R31, I7-R32 |
| AL11 | 11 | Buffers | Usable stabilizing stocks relative to relevant flows | I7-R31, I7-R33 |
| AL10 | 10 | Stock-and-flow structures | Physical arrangement, nodes and intersections | I7-R31, I7-R34 |
| AL09 | 9 | Delays | Timing relative to rates of change | I7-R31, I7-R35 |
| AL08 | 8 | Balancing feedback loops | Corrective ability relative to the impact | I7-R31, I7-R36 |
| AL07 | 7 | Reinforcing feedback loops | Gain of the driving return paths | I7-R31, I7-R36 |
| AL06 | 6 | Information flows | Who receives which information, when and in what usable form | I7-R31, I7-R37 |
| AL05 | 5 | Rules | Incentives, sanctions, constraints, enforcement and amendment authority | I7-R31, I7-R38 |
| AL04 | 4 | Self-organization | Power and processes for generating and retaining changed structure | I7-R31, I7-R39 |
| AL03 | 3 | Goals | Attributed purpose and selection of outcomes | I7-R31, I7-R40 |
| AL02 | 2 | Paradigms | Owned assumptions underlying interpretation and arrangements | I7-R31, I7-R41 |
| AL01 | 1 | Transcending paradigms | Operational interpretation: reconsider assumptions while preserving evidence and qualified action | I7-R31, I7-R42 |

Each candidate must state: target and direction; reference model/scenario; mechanism; implementer; authority; resources; timing; adoption status; state/history carry-over; criteria; affected parties; adverse alternatives; uncertainty. Changing a parameter near a threshold can matter greatly. A nominally deep change can be inaccessible or unsupported. AF-T14 is the common prospective check.

## 8. Fifteen guidelines as modeling and review obligations

The appendix condenses the final chapter's practical guidance. Its normative recommendations are attributed; no universal ethical algorithm, optimal updater or compulsory total welfare score is inferred from them.

| ID | Guideline, shortened | Printed page | Architectural obligation | Architecture requirements | Prospective case |
| --- | --- | --- | --- | --- | --- |
| AG01 | Get the beat of the system | 194 | Start from behavior, variability, history and direct structural evidence rather than a presumed remedy. | I7-R43 | AF-T02 |
| AG02 | Expose mental models | 194 | Make meanings, mechanisms, assumptions, alternatives and uncertainty inspectable. | I7-R11, I7-R42, I7-R48 | AF-T18 |
| AG03 | Honor, respect and distribute information | 194 | Preserve provenance, timing, reporting status, directed receipt and interpretation. | I7-R37, I7-R53 | AF-T08 |
| AG04 | Use language carefully and enrich systems concepts | 194 | Define referents, constructs, units and domain correspondence; distinguish labels from actual communication effects. | I7-R44 | AF-T15 |
| AG05 | Attend to importance beyond quantification | 194 | Retain qualitative concerns without assigning zero effect or fabricated cardinal precision. | I7-R45, I7-R50 | AF-T16 |
| AG06 | Make feedback policies | 194 | Separate response under a current rule from monitoring-based amendment and explanatory revision. | I7-R46, I7-R47, I7-R48 | AF-T17 |
| AG07 | Consider the good of the whole | 194 | Assess local/wider consequences, distributed burdens and contested criteria. | I7-R10, I7-R26, I7-R50 | AF-T11 |
| AG08 | Listen to existing system capability | 194 | Inspect useful local maintenance before substitution; compare support with displacement. | I7-R07, I7-R25, I7-R54 | AF-T09 |
| AG09 | Locate responsibility | 194 | Trace decisions, effects, incidence, received feedback, authority and capacity separately. | I7-R49 | AF-T11 |
| AG10 | Stay humble and keep learning | 194 | Preserve expectations, independent observations, errors, rivals and justified changes. | I7-R42, I7-R48, I7-R54 | AF-T18 |
| AG11 | Celebrate complexity | 194 | Permit transients, diversity, nonlinearity and changed organization while retaining useful simplification. | I7-R08, I7-R16, I7-R54 | AF-T05 |
| AG12 | Expand time horizons | 195 | Consider immediate needs, slow state, delayed effects and residual obligations with explicit weighting assumptions. | I7-R03, I7-R19, I7-R51 | AF-T07 |
| AG13 | Cross disciplinary boundaries | 195 | Integrate shared referents, units, time windows, mechanisms and evidence dependencies rather than merging jargon. | I7-R13, I7-R44 | AF-T15 |
| AG14 | Expand the boundary of caring | 195 | Distinguish causal inclusion, affected-party coverage and evaluative scope. | I7-R50 | AF-T16 |
| AG15 | Protect the goal of goodness | 195 | Keep conduct, report selection and normative reference history separate; preserve reasoned revision. | I7-R52 | AF-T16 |

## 9. Nine illustrative model families: implementation reference

The source introduces its equations as models used for Chapters 1–2 and explains that converters can be constants or calculations. The catalogue below preserves equation structure and key source settings in compact notation. These are model descriptions, not runnable code, digitized lookup data or validated domain laws. Where evaluation time, units, graph values or solver behavior are incomplete, exact reproduction remains open.

### AM01. Bathtub

**Source:** printed pp. 195; source figures 5–7. **Role:** Water balance and a changed inflow.

**Source settings:** 50 gal; minutes; dt=1 min; 10 min; outflow=5 gal/min; inflow switches from 0 to 5 gal/min in the stated source windows.

**Compact equation structure:** `X_next=X_previous+(inflow-outflow)*dt.`

**Qualification and execution boundary:** Endpoint labels 0–5 and 6–10 require an explicit interval/event convention. Keep gross rates, units and nonnegative domain; do not treat endpoint naming as a unique software scheduler.

**Allocation:** I7-R02, I7-R03; prospective AF-T03.

### AM02. Coffee cooling and warming

**Source:** printed pp. 195–196; source figures 10–11. **Role:** Balancing response under several initial states.

**Source settings:** Room=18 C; minutes; dt=1 min; 8 min; cooling starts at 100/80/60 C, warming at 0/5/10 C; discrepancy multiplier=0.10.

**Compact equation structure:** `T_next=T_previous+0.10*(T_room-T_previous)*dt under a declared per-minute coefficient convention.`

**Qualification and execution boundary:** Temperature is a source-labeled stock/state proxy, not conserved thermal energy. Specify effective heat capacity and transfer assumptions for a physical energy model. The coefficient needs time units when dt varies.

**Allocation:** I7-R02, I7-R04, I7-R16; prospective AF-T19.

### AM03. Bank account

**Source:** printed pp. 196; source figures 12–13. **Role:** Reinforcing proportional growth.

**Source settings:** Initial balance=100 dollars; years; dt=1 year; 12 years; annual rates 0.02/0.04/0.06/0.08/0.10.

**Compact equation structure:** `B_next=B_previous+(B_previous*r)*dt.`

**Qualification and execution boundary:** Annual discrete compounding and exact continuous growth are different conventions. Preserve rate/time semantics and do not transfer this response law to every reinforcing loop.

**Allocation:** I7-R02, I7-R04, I7-R13; prospective AF-T24.

### AM04. Thermostat

**Source:** printed pp. 196–197; source figures 14–20. **Role:** Constrained balancing response against heat exchange.

**Source settings:** Initial room=10 C for warming or 18 C for cooling; hours; dt=1 hour; runs of 8/24 hours; target=18 C; furnace response=min(max(target-T,0),5); leakage multiplier=0.10 or 0.30.

**Compact equation structure:** `T_next=T_previous+[H-L]*dt; L=k*(T-T_out). The daily outside-temperature graph spans roughly 10 C to -5 C.`

**Qualification and execution boundary:** Declare temperature-rate normalization and possible negative exchange. The daily driver is graph-defined, not an inferred exact sine. Desired temperature can differ from equilibrium because loss persists; capacity and time step matter.

**Allocation:** I7-R04, I7-R16, I7-R19, I7-R36; prospective AF-T06.

### AM05. Population

**Source:** printed pp. 197–199; source figures 21–26. **Role:** Competing births and deaths with changing fertility.

**Source settings:** Initial=6.6 billion people; years; dt=1 year; 100 years. Figure 22 b=.021/d=.009; Figure 23 b=.021/d=.030; Figure 24 b declines from .021 to .009 with d=.009; Figure 26 b dips toward .009 then rises toward .030 with d=.009.

**Compact equation structure:** `P_next=P_previous+[b(t)*P_previous-d(t)*P_previous]*dt.`

**Qualification and execution boundary:** Time-varying fertility paths are graph-defined. These are schematic aggregate rates, not identified demographic mechanisms, universal forecasts or cohort models.

**Allocation:** I7-R02, I7-R04, I7-R13, I7-R16; prospective AF-T24.

### AM06. Capital

**Source:** printed pp. 198–199; source figures 27–28. **Role:** Investment versus depreciation and lifetime effects.

**Source settings:** Initial capital=100 source units; years; dt=1 year; 50 years; lifetimes 10/15/20 years; investment fraction=.20; output-per-capital=1/3.

**Compact equation structure:** `K_next=K_previous+[s*a*K_previous-K_previous/L]*dt.`

**Qualification and execution boundary:** Specify output/capital conversion and annual rate units. A lifetime parameter is not equivalent to a full cohort replacement distribution. The source constants are illustrative, not transferable industrial data.

**Allocation:** I7-R02, I7-R04, I7-R34; prospective AF-T19.

### AM07. Business inventory

**Source:** printed pp. 199–200; source figures 29–36. **Role:** Stock regulation with perception, adjustment and delivery delays.

**Source settings:** Initial inventory=200 cars; days; dt=1 day; 100 days. Demand=20 then 22 cars/day at the source windows. Initial deliveries=20; later arrivals reference past orders. Figure 32 delays=5/3/5 days; Figure 34=2/3/5; Figure 35=5/2/5; Figure 36=5/6/5; Figure 30 lists zero delays.

**Compact equation structure:** `Stock balance; desired inventory=10*perceived sales. Source Figure 32 order expression adds perceived sales to discrepancy; Figures 34–36 divide discrepancy by response delay.`

**Qualification and execution boundary:** Sales is printed as min(stock,demand), relying on a one-day numerical convention. Averaged/smoothed does not identify a unique kernel. The listed Figure 32 response delay is absent from its printed order expression. Zero-delay mode must not divide by zero. Initialization, dispatch/arrival ordering and lost sales/backlog need explicit variants.

**Allocation:** I7-R02, I7-R03, I7-R14, I7-R19, I7-R44; prospective AF-T21.

### AM08. Reproducible capital limited by a nonrenewable resource

**Source:** printed pp. 200–201; source figures 37–41. **Role:** Coupled depletion, yield, extraction, profit and investment.

**Source settings:** Resource initially 1000; Figure 39 compares1000/2000/4000. Capital initially 5; years; dt=1 year; 100 years; lifetime 20. Growth goals compare 6/8/10/12 percent; source contains a questionable figure-range label.

**Compact equation structure:** `R_next=R_previous-E*dt; E=K*y(R); K_next=K_previous+[min(profit,growth_goal)-K/20]*dt; profit=p*E-0.10*K.`

**Qualification and execution boundary:** Price/yield and yield/resource are graph-defined. Investment can become negative under the printed min rule; do not silently clip or double-count disinvestment/depreciation. Extraction feasibility and money/capital conversion need declared semantics.

**Allocation:** I7-R02, I7-R04, I7-R16, I7-R18; prospective AF-T19.

### AM09. Reproducible capital limited by a renewable resource

**Source:** printed pp. 201–203; source figures 42–45. **Role:** Coupled renewal, harvest, yield and economic response.

**Source settings:** Resource initially 1000; capital 5; years; dt=1 year; 100 years; capital lifetime 20; growth goal=.10*K. Profit=p*harvest-K, unlike the preceding .10*K cost term.

**Compact equation structure:** `R_next=R_previous+[R*r(R)-K*y(R)]*dt; K_next=K_previous+[min(profit,growth_goal)-K/20]*dt.`

**Qualification and execution boundary:** The displayed regeneration-rate curve has units per time; total regeneration multiplies it by R. Its peak is not automatically the peak of total regeneration. Three yield curves and the price curve require tabulation/interpolation for exact replication; no automatic recovery from R=0 is supplied.

**Allocation:** I7-R02, I7-R04, I7-R16, I7-R18; prospective AF-T23.

### 9.1 Numerical model contract

Before claiming execution or source reproduction, record variable identity and role, unit/scale, initial stock and required prehistory, rate law, time origin/unit, dt, integration method, update ordering, event inclusion, interpolation or smoothing kernel, zero-delay mode, capacities, nonnegative or other domains, external driver data, conversion conventions and comparison target. A curve shown on a graph is a source-defined relationship, not a supplied exact lookup table.

Distinguish three targets: (1) demonstrate a qualitative source mechanism, (2) implement an explicitly named engineering variant, and (3) reproduce a particular source figure. The third requires stronger evidence and numerical conventions. No one target establishes empirical accuracy in a real ecosystem.

## 10. Reconciliation findings and unresolved source questions

| Finding | Issue | Printed/source anchor | Disposition and rationale | Status |
| --- | --- | --- | --- | --- |
| AS01 | Glossary stock/flow meaning versus broad process roles | 187–188 | Keep stock accounting, non-accumulative process, information influence and intensive proxy distinct. No new core family is necessary. | Semantic distinction adopted; implementation remains model-specific. |
| AS02 | Converters and numerical conventions were not prominent in the architecture summary | 195–203 | Treat constants/derived variables as typed roles within existing response/quantity records. Make dt, scheduler and boundary rules explicit in numerical model specifications. | Reference clarification; existing I7-R02/R03/R44 obligations support it. |
| AS03 | Existing inventory candidate is not a literal appendix implementation | 199–200 | Current section8.1 chooses a trailing average, continuous stock boundary law and adjustment division. The appendix says averaged/smoothed, uses one-day stock-limited sales, and prints Figure 32 orders without the listed response-delay divisor. Preserve both accounts. | Exact reproduction open; current candidate remains explicitly a design choice. |
| AS04 | Figure 32 order formula and delay block do not fully align | 200 | The printed expression adds sales rate and inventory discrepancy without an explicit adjustment time; the same page lists response delay 3 days. Do not infer the intended correction from the desired plot. | Open source-convention question; named alternative implementations may be compared later. |
| AS05 | No-delay inventory mode cannot be obtained by dividing by zero | 200 | Figure 30 lists zero perception/response/delivery delays. Define its algebraic/immediate-response mode separately from positive-delay equations. | Required implementation distinction; no simulator repaired or run here. |
| AS06 | Temperature is labeled a stock but is an intensive state proxy | 195–197 | Preserve source labeling and normalized equations; distinguish physical thermal energy and effective heat-capacity/transfer conversion in an engineering model. | Semantic qualification adopted; physical calibration remains outside scope. |
| AS07 | Rate dimensions and discrete step assumptions are implicit | 195–203 | Interpret discrepancy multipliers as per-time response coefficients under declared units; retain amount versus rate, dt and compounding/sampling conventions. | Required numerical contract; no exact-step output certified. |
| AS08 | Graph-defined inputs and nonlinear relationships lack numerical tables | 197–199, 201–203 | Daily temperature, fertility histories, resource/yield, price/yield and renewal/yield curves need data/interpolation for exact replication. Visual shape and approximate range are source evidence only. | Exact figure reproduction open; six graph pages visually checked. |
| AS09 | Renewal-rate peak and maximum total renewal are different | 202–203 | Source uses total regeneration R*r(R). Do not equate the roughly 0.5 peak of r with the peak of R*r, an absolute harvest capacity, or recovery from zero. | Semantic distinction adopted; precise yield/sustainability thresholds uncomputed. |
| AS10 | A finite-resource model has a questionable figure-range label and possible negative investment | 201 | The text prints Figures 30–40 for a growth-goal setting in the resource model. Preserve the label as a source issue. min(profit,goal) can be negative; specify disinvestment, depreciation and domains before execution. | Open interpretation; no silent typo correction or clipping. |
| AS11 | Fixed-stock balance is not equivalent to stable or resilient functioning | 187–190 | Retain gross throughput, composition and hidden damage; test disturbances and alternative modes before a resilience claim. | Existing architecture distinction confirmed. |
| AS12 | Concise appendix heuristics are stronger than safe universal engineering claims | 189–194 | Qualify balancing stability, reinforcing exponentials, renewable sustainability, historical hierarchy claims, scenario realism and leverage ordering using source context and declared assumptions. | Working interpretation adopted; no source wording silently replaced. |
| AS13 | Broad self-organization wording could conflate three change processes | 188, 194–195 | Keep actual structural generation, actor policy learning and analyst explanatory revision distinct, with available evidence and admission authority. | Existing Chapter7 integration confirmed. |
| AS14 | Information accumulation could be treated as universally conserved material | 187–188 | Define the information quantity and update/copy/forgetting semantics. Copying does not prove physical identity, truth, novelty or independent confirmation. | Semantic rule adopted; concrete identity/learning capability untested. |
| AS15 | Selected attachment breadcrumb was stale and its upload failed | Input handling | Resolve the saved item by its stable identity and pin current version5. This reference does not claim use of the missing attached bytes. | Current architecture retrieved; separate reference created. |

The stock-buffer meaning, owned knowledge, nonlinear applicability, boundary closure, state/history carry-over, source independence, local/wider criteria and adoption distinctions remain compatible with the nine-family architecture. The appendix strengthens its semantic and executable-model contracts; it does not justify adding another physical layer for each glossary word or replacing the core with a list of traps.

## 11. Finalized core fundamental contracts

The following are working engineering contracts for using the source foundation. AF-R identifiers belong to this reference; I7-R references link to the pinned cumulative architecture. Source anchors point to entries in this file, not a claim of independent empirical evidence.

| Requirement | Contract | Obligation | Source anchors | Architecture requirements | Prospective cases |
| --- | --- | --- | --- | --- | --- |
| AF-R01 | Preserve shared identity and scope | One referent can participate in multiple views; no duplicate stock, resource or commitment. | AD18; AP31; AP33 | I7-R01, I7-R09, I7-R17 | AF-T01 |
| AF-R02 | Separate descriptive role and evidence status | Event, state, pattern, structure and mechanism are independent of measured, reported, inferred or assumed status. | AD05; AP04; AP38 | I7-R11, I7-R43 | AF-T02 |
| AF-R03 | Use explicit accumulation and gross-flow accounting | Declare units, conversion, initial state and interval; constant level does not mean zero flows. | AD04; AD07; AD16; AP05–AP09 | I7-R02, I7-R03 | AF-T03, AF-T22 |
| AF-R04 | Preserve joint constraints and resource closure | Include relevant sources/sinks, renewal, complementary inputs, shared capacities and changes in limiting conditions. | AD09; AP23–AP25; AP32–AP35 | I7-R04, I7-R17, I7-R18 | AF-T04 |
| AF-R05 | Qualify mechanism form and applicability | Linear, nonlinear, threshold and regime claims need domain and source status; topology alone supplies no trajectory. | AD10–AD12; AD15; AP17–AP18; AP30 | I7-R04, I7-R13, I7-R16, I7-R32 | AF-T05 |
| AF-R06 | Require complete feedback and actual feasibility | Trace stock-to-rate return, reference, disturbances, timing, support and actuation; polarity does not certify stability. | AD02; AD06; AP12–AP16 | I7-R04, I7-R19, I7-R36 | AF-T06 |
| AF-R07 | Respect causal time, delay and commitments | Later evidence cannot affect earlier action; retain pending effects, physical timing, relevant history and horizons. | AP14; AP19–AP20; AP35–AP36; AG12 | I7-R03, I7-R14, I7-R19, I7-R35, I7-R51 | AF-T07 |
| AF-R08 | Keep actor knowledge owned and bounded | Available data, receipt, attention, interpretation, policy, intention and realized effect remain distinct. | AD03; AP02; AP37; AG03 | I7-R15, I7-R37, I7-R41, I7-R53 | AF-T08 |
| AF-R09 | Qualify resilience and repair | Specify disturbance, function/regime, horizon, dependencies, support and finite recovery ability. | AD13; AP10; AP26–AP27; AG08 | I7-R06, I7-R07, I7-R25, I7-R36 | AF-T09 |
| AF-R10 | Separate actual organization change from learning claims and model revision | Describe generating/selection/retention process and carry-over; novelty alone is not useful intelligence. | AD14; AP28; AL04 | I7-R08, I7-R14, I7-R39 | AF-T10 |
| AF-R11 | Keep hierarchy, authority, local goals and wider effects separate | Composition is not a command relation; compare autonomy, coordination, consequence incidence and ability to respond. | AD08; AD17; AP29; AG07; AG09 | I7-R09, I7-R10, I7-R49, I7-R50 | AF-T11 |
| AF-R12 | Treat scenarios as conditional and test several adequacy questions | Preserve model version, initial history, driver assumptions, interventions, uncertainty and alternative explanations. | AP21–AP22; AP39; AM01–AM09 | I7-R11, I7-R12, I7-R13, I7-R31 | AF-T12 |
| AF-R13 | Use archetypes as conditional diagnostic views | Require actual mechanism evidence and allow overlapping trap assessments over shared referents. | AD01; AT01–AT08 | I7-R21, I7-R30 | AF-T13 |
| AF-R14 | Require explicit intervention and adoption contracts | Record target/direction, authority, resources, timing, transition and criteria; list rank does not determine benefit. | AT01–AT08; AL12–AL01 | I7-R28, I7-R31, I7-R38, I7-R40 | AF-T14 |
| AF-R15 | Control meanings, derived variables and domain correspondence | Define variable role, unit/scale, operations, source term, aggregation and time; renaming does not create a mechanism. | AD07; AD10–AD11; AG04; AG13; AM01–AM09 | I7-R02, I7-R13, I7-R44 | AF-T15, AF-T22 |
| AF-R16 | Retain qualitative values and distinct purpose/reference/proxy/outcome | Attribute concerns and scope; do not manufacture cardinal arithmetic, a global welfare function or automatic moral facts. | AD17–AD18; AT08; AG05; AG07; AG14–AG15 | I7-R05, I7-R26, I7-R40, I7-R45, I7-R50, I7-R52 | AF-T16 |
| AF-R17 | Distinguish response, policy amendment and explanatory revision | Each process has its own owner, evidence, state, updater or unknown, and adoption authority. | AD03; AD14; AG06; AG10 | I7-R08, I7-R15, I7-R46, I7-R47, I7-R48 | AF-T17 |
| AF-R18 | Preserve original evidence and expectations across revision | No recycled prediction becomes independent evidence; retain source dependencies, corrections, old forecasts and unresolved discrepancies. | AP38–AP40; AG02; AG03; AG10 | I7-R11, I7-R42, I7-R48, I7-R53 | AF-T18 |
| AF-R19 | Declare executable numerical conventions and source ambiguities | Time step, scheduling, solver, kernel, prehistory, lookup curves, conversion and boundary treatment must be explicit. | AM01–AM09 | I7-R02, I7-R03, I7-R13, I7-R14, I7-R44 | AF-T19, AF-T21, AF-T23, AF-T24 |
| AF-R20 | Use this asset as a versioned semantic reference | Source meanings, engineering extensions, open reproduction questions and runtime claims have separate status. | AP38–AP40; AG10; section 1 authority policy | I7-R11, I7-R42, I7-R44, I7-R54 | AF-T20 |

### 11.1 Minimal common record contract

| Field group | Required meaning when relevant |
| --- | --- |
| Identity and scope | Stable referent, record/claim identity, role, system view, aliases and unresolved continuity; source occurrence differs from payload equality. |
| Meaning and shape | Source term, working definition, quantity or qualitative construct, unit/scale, aggregation, permissible operations and schema/model version. |
| Relationship | Producer/source, consumer/recipient, direction, affected process/state, mechanism, timing, capacity and any authority. |
| Temporal context | Occurrence/valid time, observation/report time, availability/decision time, model version, prehistory and pending effects; unknown times remain unknown. |
| Evidence and status | Source account, transformations, dependencies, measurement/inference/assumption/prediction status, uncertainty, rivals and applicability. |
| Ownership and change | Who owns the descriptive/model state; who can propose or admit a revision; previous meaning, rationale, compatibility and retained history. |
| Evaluation | Owned purpose/reference, proxy versus outcome, criteria, horizon, affected parties, qualitative concern and unresolved value disagreement. |
| Execution extension | For an executable model only: solver/dt, update/event rules, kernels/lookup data, constraints, failure behavior and sufficient initial state. |

This is a conceptual record contract, not an exhaustive transport envelope or a mandatory database schema. It does not promise infinite retention, global identifiers supplied by nature, automatic source matching or semantics-free input. Fields can be unknown or inapplicable with a reason. Concrete software admission, retry, recovery, retention and cost contracts require later endpoint design.

### 11.2 Mapping to the nine retained families

| Family | Appendix anchors | Semantic contribution |
| --- | --- | --- |
| System view | AD18; AP31; AG07; AG12–AG14 | Question-specific boundaries, horizons, related systems and distinct evaluative coverage. |
| Constituent | AD08; AD18; AP01; AT01–AT08 | Persistent participants, memberships, roles, dependencies and local/wider perspectives. |
| Stock | AD04; AD16; AP05–AP11; AM01–AM09 | Accumulation, gross balance, history, usable buffers, state proxies and domains. |
| Flow/process | AD07; AP05–AP12; AM01–AM09 | Typed material/information transfers and broader changes with explicit units and prerequisites. |
| Information/influence | AD03; AD06; AP02; AG03–AG04 | Directed content, availability, interpretation and evidence/communication distinctions. |
| Response relationship | AD09–AD12; AD15; AM01–AM09 | Joint conditions, derived variables, linear/nonlinear laws, active constraints and numerical conventions. |
| Function/purpose/reference/criterion | AD17–AD18; AT08; AL03; AG05/07/14/15 | Attributed function and goals, proxy correspondence, qualitative concern and normative scope. |
| Feedback path | AD02; AD06; AD12; AP12–AP20 | Complete stock-rate return, polarity, dominance, timing, actuation and shared support. |
| Behavior history/trajectory | AD05; AP04; AP18–AP22; AG01; AM01–AM09 | Events, patterns, scenario-conditioned modes, independent evidence and applicable comparisons. |

### 11.3 Interfaces and integration: semantic review scope

This task creates a reference asset; it does not add deployable EDI components, ports, state writers or authority to act. Consequently a runtime component-pair matrix and interface-checker pass would be inapplicable and misleading here. The interface-review checklist was used as a design aid for meaning, identity, timing, ownership, versions and evidence grounding. No full EDI interface qualification is claimed.

For later implementation, distinguish source/book evidence → semantic reference (paraphrase and interpretation), semantic reference → model specification (definitions and constraints), model result → source comparison (prediction remains generated), and review proposal → admitted model revision (controlled change). Reverse requests for clarification or correction are separate operations; a reference does not gain authority to mutate source evidence or an actor's world. Check all actual component pairs and both directions when concrete endpoints exist.

| Semantic interface | Meaning and direction | Prohibited shortcut / unresolved boundary |
| --- | --- | --- |
| Source → glossary/reference | Retain page, source wording context, paraphrase and interpreted contract as different records. | Engineering clarification must not masquerade as the literal source definition. |
| Reference → model specification | Supply controlled definitions, units/scales, constraints and open numerical questions. | A source citation does not supply missing mechanism, curve data or calibration. |
| Model specification → analysis | Specify version, conditions, initial/history state and numerical or qualitative method. | A diagram or glossary entry cannot become an executable law without an actual rule. |
| Analysis → evidence comparison | Preserve original prediction and compare to independently sourced records under defined correspondence. | Generated outcomes and repeated summaries cannot become independent source observations. |
| Review → admitted revision | State affected meaning/mechanism, owner, rationale, compatibility and retained history. | A corrected explanation does not automatically change the actual system or the source. |
| Actor information → policy review | Use actually received information and owned criteria with an explicit or unresolved updater. | An actor does not inherit analyst knowledge or implementation authority from shared vocabulary. |
| Proposed intervention → adoption | Target, direction, permissions, resources, timing and transition are separate. | Recommendation, formal approval, implementation and observed efficacy remain distinct. |

Shared source dependence, mixed time scales, reporting selection and multiple model views remain whole-system review concerns. Equivalent JSON types or matched names do not establish semantic compatibility. Concrete delivery, recovery, retention and resource limits remain endpoint-specific and unqualified by this document.

## 12. Prospective semantic and modeling cases

**Every case is PLANNED — NOT RUN.** These are author-designed checks for using the reference, not results, experiments quoted from Meadows or independent additions to the master 192-case catalogue. AF-T22 and AF-T24 additionally support AF-R03/AF-R15/AF-R19; AF-T23 supports AF-R04/AF-R19. AF-T21 addresses the named inventory reproduction blocker.

| Case | Scenario | Prospective acceptance check |
| --- | --- | --- |
| AF-T01 | Reference one supplier from two system views. | Shared identity, capacity and commitments count once; boundary assumptions remain explicit. |
| AF-T02 | Receive an uncertain report of a structural change and a measured event. | Descriptive role and evidential status are independently classified; no double confirmation is invented. |
| AF-T03 | Compare a steady stock with high throughput and a steady stock with zero throughput. | Stock-level equality does not merge gross flow, resource demand or constituent turnover. |
| AF-T04 | Move a bottleneck between complementary resources while widening a source boundary. | Feasible joint rates and shared capacity remain consistent; the old external driver is replaced or conditioned. |
| AF-T05 | Change a nonlinear operating point without changing topology, then change topology separately. | Competing explanations remain distinguishable; reinforcing polarity does not force exact exponential output. |
| AF-T06 | Add a nominal balancing path with delay or insufficient actuation. | Closure is explicit but stable target achievement is not assumed; external losses and support constraints remain visible. |
| AF-T07 | Deliver feedback after an action has created an irreversible pending effect. | The past effect remains; later knowledge affects later decisions and cannot erase the original history. |
| AF-T08 | Give the modeler a hidden constraint that the actor has not received. | Actual execution may be constrained; perceived options and intended action gain no oracle information. |
| AF-T09 | Keep ordinary output stable while a shared backup/repair support fails. | Resilience is assessed under specified disturbances and future condition, not certified from recent output alone. |
| AF-T10 | Observe a new relationship, discover an old relationship, and revise a description. | Actual reorganization, new knowledge and useful learning remain separate with retained identity/state. |
| AF-T11 | Return consequences to someone who lacks amendment authority. | Consequence exposure, knowledge, influence, capacity and normative responsibility are separate; good correction is not guaranteed. |
| AF-T12 | Fit two different structures to the same past history and vary future drivers. | Past fit does not uniquely identify cause; scenario applicability, mechanism response and decision criteria are evaluated separately. |
| AF-T13 | Assign two overlapping trap hypotheses to the same processes. | Shared stocks/rules are not duplicated; necessary mechanism evidence and rivals remain inspectable. |
| AF-T14 | Propose a nominally deep leverage change that has no implementer or resources. | Potential influence, direction, preference and actual adoption stay separate; rank supplies no efficacy score. |
| AF-T15 | Combine accounts with different units, identical words or differing ordinal scales. | Referent/quantity/time correspondence and valid operations are explicit; labels do not establish identity or cardinal precision. |
| AF-T16 | Improve an indicator by lowering its standard while excluding an affected party. | Outcome, proxy, reference revision, qualitative concern and evaluative coverage remain distinct and attributed. |
| AF-T17 | Enable fixed-policy response, owned policy review and analyst model revision independently. | Each changes only its own declared state; proposed updates may remain unadopted or unresolved. |
| AF-T18 | Store one forecast in several summaries and later correct its definition. | No independent evidence is created; original forecast, source account, definition and correction lineage remain recoverable. |
| AF-T19 | Implement a source model with omitted units, lookup tables or ambiguous update ordering. | Mark reproduction incomplete; do not hide a repaired equation or guessed curve under exact-source status. |
| AF-T20 | Use the semantic reference with an architecture revision that changes a term. | Record version, compatibility decision, affected requirements and unresolved mismatch; historical source meaning is preserved. |
| AF-T21 | Compare the appendix Figure 32 inventory expression with its listed response delay and the existing candidate. | Keep source expression and candidate separate; choose a named interpretation only with rationale and no exact-replication claim. |
| AF-T22 | Copy an information report, forget it at one recipient, and retain it at another. | Information state/count and provenance are explicit; no universal material conservation or independent-confirmation assumption is imposed. |
| AF-T23 | Compare the resource-dependent regeneration-rate curve with total regeneration flow. | Use G(R)=R*r(R) under the source formulation; do not infer identical maxima, sustainable yield or recovery from zero without evidence. |
| AF-T24 | Change dt, compounding convention or sales scheduling in a numerical model. | Rate units and discretization are explicit; solver sensitivity and changed assumptions cannot be represented as physical discovery. |

## 13. Reference-use procedure and version control

1. Begin with a question and observed/directly inspected evidence; record source context and temporal availability.
2. Select glossary meanings and explicit engineering distinctions. Bind terms to actual referents and units/scales, not spelling alone.
3. Allocate proposed structure to the existing nine families and identify its source principles, assumptions, unknowns and relevant requirements.
4. Specify directed relations, shared constraints, available actor knowledge, delays and initial/history conditions.
5. Retain rival mechanisms and choose qualitative analysis, a named engineering model, or source-figure reproduction as the intended task.
6. For numerical work, resolve or explicitly bracket the section 10 ambiguities; document every changed convention rather than silently repairing it.
7. Compare conditional consequences across relevant time scales, affected parties and criteria. Preserve original expectations and independent evidence.
8. Admit a revision only with its owner, rationale, compatibility and carry-over. Revisit related conclusions and interfaces when meaning changes.

Use version 1.0 as the semantic working baseline for architecture discussion. A future extension may add a term while retaining these source meanings and qualifications. New findings can revise the engineering interpretation; finalizing vocabulary does not close inquiry about reality or settle source ambiguities by decree.

## 14. Validation record and final disposition

**Document consistency result: passed the specified checks.** All 17 printed pages have an exact printed/PDF ledger. The 18 glossary labels were found in the source; the 40 principle bullets were independently counted in the source text. The six source catalogues contain 102 uniquely allocated entries. All 102 have valid cumulative architecture requirements, reference contracts and prospective checks. References resolve against the pinned architecture catalogue of 54 requirement definitions; only relevant ones are used in this reference. Twenty reference requirements and 24 prospective cases have unique contiguous identifiers, and every case has a requirement allocation. The 32 extension definitions are explicitly labeled engineering vocabulary. Tables, section sequence, model-family definitions and named source questions pass structural checks. Source and architecture hashes are recorded privately; the architecture input is unchanged. Six graph-containing pages were visually reviewed. These are source/semantic/document checks, not dynamic model execution. All 24 model-use cases remain **PLANNED — NOT RUN**, and exact numerical reproduction is unqualified.

**Disposition:** accept as the separate, source-anchored semantic foundation for the current Chapters 1–7 conceptual architecture. It confirms the nine-family organization while making converters, quantitative execution conventions, source-versus-engineering status and the listed ambiguities explicit. Exact source-model reproduction is not accepted where unresolved conventions or missing graph data remain. No model execution, empirical causal identification, policy effectiveness, intelligence advantage, throughput, token/energy efficiency or high availability has been established.

### References

- Donella H. Meadows, edited by Diana Wright, *Thinking in Systems*, supplied 2008 edition, Appendix, printed pp.187–203 (PDF 204–220). Source provenance is pinned in section 1.
- *Meadows_Chapters_1_2_3_4_5_6_7_Integrated_Architecture_Audit_v0_7.md*, current saved version 5, internal v0.7. In particular: section4 shared families, section5 evidence/identity/time, section8 candidate inventory model, section45 cross-cutting records, section46 directed integration and section49 conceptual verdict.

This reference paraphrases and analyzes the supplied work. It is not a reproduction of the appendix or a substitute for the source. All formal notation, contracts, crosswalks and prospective tests are our synthesis unless explicitly identified as source equation structure.

## 15. Complete source-entry allocation

All 102 source entries are allocated below. Multiple links express shared obligations; they do not make entries independent evidence or add physical modules. The source definitions/principles and explicit qualification remain authoritative over a shortened crosswalk label.

| Source entry | Printed pages | Architecture requirements | Working reference contracts | Prospective checks |
| --- | --- | --- | --- | --- |
| AD01 | 187 | I7-R13, I7-R21, I7-R30 | AF-R12, AF-R13 | AF-T12, AF-T13 |
| AD02 | 187 | I7-R04, I7-R19, I7-R36 | AF-R04, AF-R06, AF-R07 | AF-T04, AF-T06, AF-T07 |
| AD03 | 187 | I7-R10, I7-R15, I7-R41 | AF-R08, AF-R11 | AF-T08, AF-T11 |
| AD04 | 187 | I7-R02, I7-R03, I7-R12 | AF-R03, AF-R07, AF-R12 | AF-T03, AF-T07, AF-T12, AF-T22 |
| AD05 | 187 | I7-R03, I7-R12, I7-R43 | AF-R02, AF-R07, AF-R12 | AF-T02, AF-T07, AF-T12 |
| AD06 | 187 | I7-R04, I7-R09, I7-R11 | AF-R04, AF-R11, AF-R18 | AF-T04, AF-T11, AF-T18 |
| AD07 | 187 | I7-R02, I7-R04, I7-R44 | AF-R03, AF-R04, AF-R15 | AF-T03, AF-T04, AF-T15, AF-T22 |
| AD08 | 187 | I7-R01, I7-R09, I7-R10 | AF-R01, AF-R11 | AF-T01, AF-T11 |
| AD09 | 187 | I7-R04, I7-R18, I7-R35 | AF-R04, AF-R07 | AF-T04, AF-T07 |
| AD10 | 187 | I7-R13, I7-R16, I7-R32 | AF-R05, AF-R12 | AF-T05, AF-T12 |
| AD11 | 187 | I7-R04, I7-R16, I7-R32 | AF-R04, AF-R05 | AF-T04, AF-T05 |
| AD12 | 187 | I7-R04, I7-R23, I7-R36 | AF-R04, AF-R06 | AF-T04, AF-T06 |
| AD13 | 188 | I7-R06, I7-R07, I7-R36 | AF-R06, AF-R09 | AF-T06, AF-T09 |
| AD14 | 188 | I7-R08, I7-R14, I7-R39 | AF-R10 | AF-T10 |
| AD15 | 188 | I7-R04, I7-R12, I7-R16 | AF-R04, AF-R05, AF-R12 | AF-T04, AF-T05, AF-T12 |
| AD16 | 188 | I7-R02, I7-R03, I7-R33 | AF-R03, AF-R07, AF-R09 | AF-T03, AF-T07, AF-T09, AF-T22 |
| AD17 | 188 | I7-R05, I7-R10, I7-R26, I7-R50 | AF-R11, AF-R16 | AF-T11, AF-T16 |
| AD18 | 188 | I7-R01, I7-R05, I7-R09, I7-R17 | AF-R01, AF-R11, AF-R16 | AF-T01, AF-T11, AF-T16 |
| AP01 | 188 | I7-R01, I7-R04, I7-R09 | AF-R01, AF-R04, AF-R11 | AF-T01, AF-T04, AF-T11 |
| AP02 | 188 | I7-R09, I7-R15, I7-R37, I7-R53 | AF-R08, AF-R11, AF-R18 | AF-T08, AF-T11, AF-T18 |
| AP03 | 188 | I7-R05, I7-R26, I7-R40 | AF-R16 | AF-T16 |
| AP04 | 188 | I7-R04, I7-R11, I7-R12, I7-R43 | AF-R02, AF-R04, AF-R12, AF-R18 | AF-T02, AF-T04, AF-T12, AF-T18 |
| AP05 | 188 | I7-R02, I7-R03, I7-R14 | AF-R03, AF-R07, AF-R10 | AF-T03, AF-T07, AF-T10, AF-T22 |
| AP06 | 188 | I7-R02, I7-R04 | AF-R03, AF-R04 | AF-T03, AF-T04, AF-T22 |
| AP07 | 188 | I7-R02, I7-R04, I7-R18 | AF-R03, AF-R04 | AF-T03, AF-T04, AF-T22 |
| AP08 | 188 | I7-R02, I7-R03 | AF-R03, AF-R07 | AF-T03, AF-T07, AF-T22 |
| AP09 | 188 | I7-R02, I7-R12, I7-R31 | AF-R03, AF-R12, AF-R14 | AF-T03, AF-T12, AF-T14, AF-T22 |
| AP10 | 189 | I7-R03, I7-R06, I7-R33 | AF-R07, AF-R09 | AF-T07, AF-T09 |
| AP11 | 189 | I7-R02, I7-R04, I7-R33 | AF-R03, AF-R04, AF-R09 | AF-T03, AF-T04, AF-T09, AF-T22 |
| AP12 | 189 | I7-R04, I7-R09, I7-R36 | AF-R04, AF-R06, AF-R11 | AF-T04, AF-T06, AF-T11 |
| AP13 | 189 | I7-R04, I7-R19, I7-R36 | AF-R04, AF-R06, AF-R07 | AF-T04, AF-T06, AF-T07 |
| AP14 | 189 | I7-R04, I7-R16, I7-R36 | AF-R04, AF-R05, AF-R06 | AF-T04, AF-T05, AF-T06 |
| AP15 | 189 | I7-R03, I7-R15, I7-R19, I7-R48 | AF-R07, AF-R08, AF-R18 | AF-T07, AF-T08, AF-T18 |
| AP16 | 189 | I7-R04, I7-R05, I7-R36 | AF-R04, AF-R06, AF-R16 | AF-T04, AF-T06, AF-T16 |
| AP17 | 189 | I7-R13, I7-R16, I7-R44 | AF-R05, AF-R12, AF-R15 | AF-T05, AF-T12, AF-T15, AF-T22 |
| AP18 | 189 | I7-R04, I7-R12, I7-R16 | AF-R04, AF-R05, AF-R12 | AF-T04, AF-T05, AF-T12 |
| AP19 | 189 | I7-R19, I7-R35, I7-R36 | AF-R06, AF-R07 | AF-T06, AF-T07 |
| AP20 | 189 | I7-R03, I7-R19, I7-R35 | AF-R07 | AF-T07 |
| AP21 | 189 | I7-R11, I7-R12, I7-R31 | AF-R12, AF-R14, AF-R18 | AF-T12, AF-T14, AF-T18 |
| AP22 | 190 | I7-R12, I7-R13, I7-R31, I7-R54 | AF-R12, AF-R14, AF-R20 | AF-T12, AF-T14, AF-T20 |
| AP23 | 190 | I7-R04, I7-R17, I7-R18 | AF-R01, AF-R04 | AF-T01, AF-T04 |
| AP24 | 190 | I7-R02, I7-R04, I7-R18 | AF-R03, AF-R04 | AF-T03, AF-T04, AF-T22 |
| AP25 | 190 | I7-R02, I7-R04, I7-R16, I7-R18 | AF-R03, AF-R04, AF-R05 | AF-T03, AF-T04, AF-T05, AF-T22 |
| AP26 | 190 | I7-R06, I7-R07, I7-R36 | AF-R06, AF-R09 | AF-T06, AF-T09 |
| AP27 | 190 | I7-R05, I7-R06, I7-R25, I7-R50 | AF-R09, AF-R16 | AF-T09, AF-T16 |
| AP28 | 190 | I7-R08, I7-R14, I7-R39 | AF-R10 | AF-T10 |
| AP29 | 190 | I7-R01, I7-R09, I7-R10, I7-R50 | AF-R01, AF-R11, AF-R16 | AF-T01, AF-T11, AF-T16 |
| AP30 | 190 | I7-R04, I7-R16, I7-R32 | AF-R04, AF-R05 | AF-T04, AF-T05 |
| AP31 | 190 | I7-R01, I7-R09, I7-R17 | AF-R01, AF-R11 | AF-T01, AF-T11 |
| AP32 | 190 | I7-R04, I7-R18 | AF-R04 | AF-T04 |
| AP33 | 190 | I7-R04, I7-R09, I7-R18 | AF-R04, AF-R11 | AF-T04, AF-T11 |
| AP34 | 190 | I7-R04, I7-R17, I7-R18 | AF-R01, AF-R04 | AF-T01, AF-T04 |
| AP35 | 190 | I7-R03, I7-R16, I7-R19, I7-R35 | AF-R05, AF-R07 | AF-T05, AF-T07 |
| AP36 | 190 | I7-R03, I7-R15, I7-R19, I7-R51 | AF-R07, AF-R08 | AF-T07, AF-T08 |
| AP37 | 191 | I7-R10, I7-R15, I7-R26, I7-R50 | AF-R08, AF-R11, AF-R16 | AF-T08, AF-T11, AF-T16 |
| AP38 | 191 | I7-R11, I7-R41, I7-R42, I7-R48 | AF-R08, AF-R18 | AF-T08, AF-T18 |
| AP39 | 191 | I7-R11, I7-R12, I7-R13, I7-R48 | AF-R12, AF-R18 | AF-T12, AF-T18 |
| AP40 | 191 | I7-R11, I7-R12, I7-R42, I7-R54 | AF-R12, AF-R18, AF-R20 | AF-T12, AF-T18, AF-T20 |
| AT01 | 191 | I7-R21, I7-R23, I7-R28 | AF-R06, AF-R13, AF-R14 | AF-T06, AF-T13, AF-T14 |
| AT02 | 191 | I7-R21, I7-R22, I7-R28 | AF-R11, AF-R13, AF-R14 | AF-T11, AF-T13, AF-T14 |
| AT03 | 191–192 | I7-R23, I7-R26, I7-R52 | AF-R06, AF-R16 | AF-T06, AF-T16 |
| AT04 | 192 | I7-R21, I7-R23, I7-R28 | AF-R06, AF-R13, AF-R14 | AF-T06, AF-T13, AF-T14 |
| AT05 | 192 | I7-R21, I7-R24, I7-R28 | AF-R13, AF-R14 | AF-T13, AF-T14 |
| AT06 | 192–193 | I7-R21, I7-R25, I7-R28 | AF-R09, AF-R13, AF-R14 | AF-T09, AF-T13, AF-T14 |
| AT07 | 193 | I7-R21, I7-R26, I7-R27, I7-R28 | AF-R13, AF-R14, AF-R16 | AF-T13, AF-T14, AF-T16 |
| AT08 | 193 | I7-R21, I7-R26, I7-R40, I7-R50 | AF-R13, AF-R16 | AF-T13, AF-T16 |
| AL12 | 194 | I7-R31, I7-R32 | AF-R05, AF-R14 | AF-T05, AF-T14 |
| AL11 | 194 | I7-R31, I7-R33 | AF-R09, AF-R14 | AF-T09, AF-T14 |
| AL10 | 194 | I7-R31, I7-R34 | AF-R14, AF-R19 | AF-T14, AF-T19, AF-T21, AF-T23, AF-T24 |
| AL09 | 194 | I7-R31, I7-R35 | AF-R07, AF-R14 | AF-T07, AF-T14 |
| AL08 | 194 | I7-R31, I7-R36 | AF-R06, AF-R14 | AF-T06, AF-T14 |
| AL07 | 194 | I7-R31, I7-R36 | AF-R06, AF-R14 | AF-T06, AF-T14 |
| AL06 | 194 | I7-R31, I7-R37 | AF-R08, AF-R14 | AF-T08, AF-T14 |
| AL05 | 194 | I7-R31, I7-R38 | AF-R14 | AF-T14 |
| AL04 | 194 | I7-R31, I7-R39 | AF-R10, AF-R14 | AF-T10, AF-T14 |
| AL03 | 194 | I7-R31, I7-R40 | AF-R14, AF-R16 | AF-T14, AF-T16 |
| AL02 | 194 | I7-R31, I7-R41 | AF-R08, AF-R14 | AF-T08, AF-T14 |
| AL01 | 194 | I7-R31, I7-R42 | AF-R14, AF-R18 | AF-T14, AF-T18 |
| AG01 | 194 | I7-R43 | AF-R02 | AF-T02 |
| AG02 | 194 | I7-R11, I7-R42, I7-R48 | AF-R18 | AF-T18 |
| AG03 | 194 | I7-R37, I7-R53 | AF-R08, AF-R18 | AF-T08, AF-T18 |
| AG04 | 194 | I7-R44 | AF-R15 | AF-T15, AF-T22 |
| AG05 | 194 | I7-R45, I7-R50 | AF-R16 | AF-T16 |
| AG06 | 194 | I7-R46, I7-R47, I7-R48 | AF-R17, AF-R18 | AF-T17, AF-T18 |
| AG07 | 194 | I7-R10, I7-R26, I7-R50 | AF-R11, AF-R16 | AF-T11, AF-T16 |
| AG08 | 194 | I7-R07, I7-R25, I7-R54 | AF-R09, AF-R20 | AF-T09, AF-T20 |
| AG09 | 194 | I7-R49 | AF-R11 | AF-T11 |
| AG10 | 194 | I7-R42, I7-R48, I7-R54 | AF-R18, AF-R20 | AF-T18, AF-T20 |
| AG11 | 194 | I7-R08, I7-R16, I7-R54 | AF-R05, AF-R10, AF-R20 | AF-T05, AF-T10, AF-T20 |
| AG12 | 195 | I7-R03, I7-R19, I7-R51 | AF-R07 | AF-T07 |
| AG13 | 195 | I7-R13, I7-R44 | AF-R12, AF-R15 | AF-T12, AF-T15, AF-T22 |
| AG14 | 195 | I7-R50 | AF-R16 | AF-T16 |
| AG15 | 195 | I7-R52 | AF-R16 | AF-T16 |
| AM01 | 195 | I7-R02, I7-R03 | AF-R03, AF-R07, AF-R19 | AF-T03, AF-T07, AF-T19, AF-T22 |
| AM02 | 195–196 | I7-R02, I7-R04, I7-R16 | AF-R03, AF-R04, AF-R05, AF-R19 | AF-T03, AF-T04, AF-T05, AF-T19, AF-T22 |
| AM03 | 196 | I7-R02, I7-R04, I7-R13 | AF-R03, AF-R04, AF-R12, AF-R19 | AF-T03, AF-T04, AF-T12, AF-T19, AF-T22 |
| AM04 | 196–197 | I7-R04, I7-R16, I7-R19, I7-R36 | AF-R04, AF-R05, AF-R06, AF-R07, AF-R19 | AF-T04, AF-T05, AF-T06, AF-T07, AF-T19 |
| AM05 | 197–199 | I7-R02, I7-R04, I7-R13, I7-R16 | AF-R03, AF-R04, AF-R05, AF-R12, AF-R19 | AF-T03, AF-T04, AF-T05, AF-T12, AF-T19, AF-T22 |
| AM06 | 198–199 | I7-R02, I7-R04, I7-R34 | AF-R03, AF-R04, AF-R19 | AF-T03, AF-T04, AF-T19, AF-T21, AF-T22, AF-T23, AF-T24 |
| AM07 | 199–200 | I7-R02, I7-R03, I7-R14, I7-R19, I7-R44 | AF-R03, AF-R07, AF-R10, AF-R15, AF-R19 | AF-T03, AF-T07, AF-T10, AF-T15, AF-T19, AF-T22 |
| AM08 | 200–201 | I7-R02, I7-R04, I7-R16, I7-R18 | AF-R03, AF-R04, AF-R05, AF-R19 | AF-T03, AF-T04, AF-T05, AF-T19, AF-T22 |
| AM09 | 201–203 | I7-R02, I7-R04, I7-R16, I7-R18 | AF-R03, AF-R04, AF-R05, AF-R19 | AF-T03, AF-T04, AF-T05, AF-T19, AF-T22 |

