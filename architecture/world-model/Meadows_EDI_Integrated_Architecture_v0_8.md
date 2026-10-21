# Integrated systems and EDI reasoning architecture: Meadows Chapters 1–7

Version 0.8 — 20 October 2026. Retained seven-chapter conceptual foundation plus explicit EDI reasoning and future-learning integration.

## Revision 0.8 engineering extension

The single diagram in section 3 now includes explicit reasoning control, a pretrained student served by vLLM, selective teacher guidance, model admission, exploration and a separate future training/checkpoint-adoption path. All original conceptual nodes and connections are retained. Section 53 distinguishes these engineering additions from Meadows-derived concepts and records the pretrained-versus-random-weight decision.

Initial neural weights remain fixed; evidence-linked world representations can evolve continuously. This update establishes structure before qualification/tests as requested. No new model training, runtime, benchmark or qualification was performed. Earlier numerical graph counts and review verdicts below refer to their historical v0.7 inputs; they do not qualify the new engineering extension.

## Basis, scope and status

This document integrates the retained Chapters 1–6 architecture and the Chapter 7 assessment into **one shared system description and one connected master diagram** in section 3. It retains nine representation families. Learning, meaning, qualitative concerns and responsibility are specifications over shared referents, rather than additional worlds or a physical module per practice.

Current integration inputs:

- *Meadows_Chapters_1_2_3_4_5_6_Integrated_Architecture_Audit_v0_6.md*, internal revision 0.6.1, stable identity `libfile_7b9b477f82208191ab94058fbf22e04e`, content `file_000000008dc08211884def62eecac463`, version 4. Its detailed assessments, contracts, 278 catalogue units, 42 requirements and 124 prospective cases are retained.
- *Meadows_Chapter_7_Living_in_Systems_Architecture_v0_1.md*, `libfile_563bbbb5751c8191a0551da7d061c149`, content `file_00000000c688821193d73ecb4d18db13`. Its fifteen practices, 68 catalogue units, 18 parent requirements and 60 prospective cases supply Chapter 7 material. Its separate extension graph is superseded here by the single cumulative master.

Underlying source: Donella H. Meadows, edited by Diana Wright, *Meadows-2008.-Thinking-in-Systems(3).pdf*, `file_000000000a10821198286322dbd247fa`. Requested body scope is printed pp. 11–72, 75–141 and 145–185, corresponding to PDF pp. 28–89, 92–158 and 162–202: **170 body pages**. Earlier chapter assessments are reused. All 20 Chapter 7 body pages were checked again as extracted text in this integration pass; a fresh rereading of all 170 pages or complete rendered-figure inspection is not claimed.

Meadows supplies concepts, examples and practices. The nine families, record schemas, interface contracts, formalizations, diagram, catalogue divisions and tests are our design synthesis. The **346 catalogue units** are our review granularity, not official primitives numbered by Meadows. Historical, philosophical and ethical claims remain attributed and qualified. In particular, conceptual scope does not provide an autonomous learning algorithm, a universally correct moral objective or complete knowledge of human psychology.

The cumulative namespace is now **I7-R01–I7-R54** and **I7-T01–I7-T192**. The first 42 requirements and 124 cases retain their meanings and numbers from I6; historical references in this working document are normalized to I7. Chapter 7 cases C7-T01–C7-T60 map in order to I7-T125–I7-T184. Eight additional composition cases are I7-T185–I7-T192. **All 192 model scenarios are PLANNED — NOT RUN.** Document checks concern consistency, coverage allocation and explicit interfaces, not successful model behavior or empirical causal truth.

Earlier retrospectives in sections 15, 21, 28 and 39–42 are retained review history. **Sections 49–52 are the authoritative seven-chapter review, canonical crosswalk, source scope and qualification record.** Sections 43–48 contain the detailed Chapter 7 integration. Sections 1–52 retain the book-first conceptual architecture and historical review scope. Section 53 separately records the new EDI engineering extension; no implementation, training, tests or benchmarking is performed by this revision.

## 1. The integrated definition

A system model is a revisable, evidence-linked description of interacting constituents whose organization and mechanisms generate conditional behavior over time. It represents both how functioning changes and how the organization supporting that functioning may persist, degrade, be repaired or develop.

It must answer fifteen connected questions:

1. What participates, and how is it organized across relevant levels?
2. What accumulates, and what processes change it?
3. What conditions, information, rules, limits and delays govern those processes?
4. What retained history and pending effects matter for future behavior?
5. Which purposes, references and criteria belong to which actors or system views?
6. How do the included systems exchange with each other and their surroundings?
7. Which mechanisms preserve or restore functioning under specified disturbances?
8. How can constituents, relationships or coordination arrangements change?
9. Which observations support the description, and which predictions or decisions are justified by it?
10. What can each relevant actor perceive, believe, attempt and actually affect, and how does that differ from the analyst’s knowledge?

11. Which interacting mechanisms sustain an unwanted outcome, and which feasible changes might interrupt them without obscuring costs, dependency, adaptation or wider consequences?

12. What can be changed, in which direction, by whom, through what adoption and implementation process, and with which conditional effects?
13. Which actor or analyst assumptions shape interpretation, goals and selection, and what evidence or context would warrant revising them?
14. How do available experience, expectations, review and authorized adoption change a policy, separately from ordinary action and analyst model revision?
15. Which qualitative concerns, affected parties, responsibilities and short/long consequences remain important even when measurement or agreement is incomplete?

No single constituent, relationship or behavior label answers all fifteen. The model must connect them without assuming every system has a controller, an agreed collective objective, a fixed equilibrium or a demonstrated self-organization mechanism.

## 2. What has evolved across the seven chapters

| Concern | Chapter 1 | Chapter 2 | Chapter 3 | Chapter 4 | Chapter 5 | Chapter 6 | Chapter 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Organization | Elements, connections and function/purpose | Coupled systems and conditional analogies | Hierarchy, stable assemblies and self-organization | Roles, perspectives and analytical boundary revision | Adaptive strategies, governance and rule-conditioned specialization | Intervention authority and separately attributed frames | Policy owners, reviewers, domain contributors and affected parties with distinct rights |
| Accumulation | Stocks, flows and balance | Regeneration, resource depletion and capacity | Buffers, repair resources and capability where accumulated | Wider sources, sinks and changing limits | Shared resource condition, opportunity and corrective-capacity histories | Capacity versus usable reserve, cohorts and retained history | Slow commitments and history; qualitative value is not automatically a numerical stock |
| Mechanism | Information, response and feedback | Joint nonlinear relationships and changing dominance | Restoration, repair and organization-producing processes | Intended action versus realized effect and applicability | Opposed goals, reward conversion, dependency, rule adaptation and proxy-target effects | Conditional leverage, adoption and explicit assumption dependence | Fixed-policy response, policy amendment and analyst revision as different mechanisms |
| Time | Events and behavior over time | Perception, response and delivery delays | Recovery and organizational development times | Pending commitments, relevant timescales and foresight | Goal drift, compounding advantage, erosion and intervention transitions | Delay relative to change, implementation and irreversible commitments | Nested fast/slow processes; physical time, monitoring cadence, planning and value weighting distinct |
| Purpose | Function and attributed purpose | References and outcome criteria | Local/wider conflict and autonomy | Bounded choice, incentives and satisficing | Purpose versus rule, indicator, compliance and actual outcome | Goals, selection and normative versus empirical assumptions | Qualitative concern, contested values and legitimate revision versus reference erosion |
| Interfaces | Material and information connections | Shared transfers and external drivers | Cross-level exchanges and common dependencies | Boundary closure and consequential visibility changes | Benefit/cost incidence, resource governance, adaptive feedback and concentration of influence | New versus tuned information paths, rule-writing authority and mediated frame change | Consequence feedback, semantic correspondence, directed information and policy-review authority |
| Behavior | Conditions and mechanisms generate histories | Several modes from one structure | Persistence, recovery and reorganization | Alternative explanations for events, patterns and regimes | Eight composable candidate traps and conditional ways out | Conditional intervention effects and interaction among targets | Mean versus variability, transients, surprise and preserved forecast errors |
| Assessment | Examine structure and behavior | Driver plausibility, response and wider causes | Hidden resilience and coordination tradeoffs | Evidence independence, uncertainty and model limits | Mechanism discrimination, adoption, transition, adaptation and wider outcomes | Leverage exceptions, influence versus desirability/feasibility and frame reconsideration | Inspectable learning, rival error explanations, affected-party coverage and bounded conclusions |

The evolution is not the addition of a physical module per property or trap. It is the ability to explain these properties through the same constituents, processes, relationships and evidence already used to explain ordinary behavior.

## 3. Overall architecture

The architecture has one shared system description, four retained complementary views, three Chapter 5 analytical views, explicit intervention/frame and Chapter 7 learning/meaning specifications, and a modeling/assessment workflow. These are conceptual divisions, not required software services or a fixed sequence of cognitive stages.

### 3.1 The shared system description

The core contains nine representation families:

1. System view.
2. Element or constituent.
3. Stock or accumulated quantity.
4. Flow or changing process.
5. Information or influence link.
6. Response relationship.
7. Function, purpose, reference and criterion.
8. Feedback path.
9. Behavior history and conditional trajectory.

Evidence, identity, temporal meaning, uncertainty and revision status apply across them. They are shared annotations rather than separate copies of each object.

### 3.2 Four views of that same description

| View | Main question | What it references |
| --- | --- | --- |
| Restoration and repair | What preserves or recovers functioning, and what supports those mechanisms? | Constituent condition, stocks, processes, response rules, feedback, dependencies and criteria. |
| Organization change | How can the system create, remove or alter organization? | Constituent membership, relationships, rules, generating processes, resources and structural history. |
| Hierarchy and interfaces | How do local systems participate, exchange and coordinate within wider systems? | Shared identities, composition, interactions, information, permissions, purposes and cross-level effects. |
| Actor perspective and action | What can a particular actor know, interpret, intend and realize? | Shared referents, channel availability, internal state, purposes, perceived options, policy and execution mechanisms. |

Chapter 5 adds three derived analytical views over the same referents: **archetype assessment**, **purpose–rule–indicator correspondence**, and **intervention comparison**. These preserve evidence, conditions and alternative explanations. They do not create another physical stock or force.

Chapter 6 additionally makes two cross-cutting specifications explicit: intervention target/direction/adoption and owned interpretive assumptions/revision. They refer to shared constituents, information, response, purpose and temporal records. Neither specification creates an extra physical primitive or universal belief-update algorithm.

Chapter 7 makes four cross-cutting records explicit: meaning/measurement correspondence; qualitative concern and coverage; expectation/error/learning decision; and versioned feedback-policy review. These reference the existing families and views. They separate represented actors' policy learning from analyst inquiry and actual adoption; they do not supply a general update algorithm or prescribe a universal ethical objective.

The views can reveal different consequences of the same mechanism. A central approval rule might coordinate scarce resources while delaying local repair. A new relationship might provide an alternative route while introducing a shared dependency. These are interactions to assess, not contradictions to remove by definition.

```mermaid
flowchart TB
    subgraph SCOPE["Inquiry and selected system view"]
        direction TB
        Q["Inquiry and model purpose"]
        B["Boundary, resolution and horizon"]
        CR["Stakeholder outcome criteria"]
        X["External drivers, sources and sinks"]
        BV["Boundary alternatives and interface closure"]
        B -.->|"Alternative view definitions"| BV
        BV -.->|"Assigns input ownership"| X
        BV -.->|"Qualified view definition"| MD
        Q -.->|"Selects"| B
        Q -.->|"Frames evaluation"| CR
        B -.->|"Declares omissions"| X
    end

    subgraph ORG["Organization across interacting levels — Chapters 1 and 3"]
        direction TB
        EL["Constituents and persistent identity"]
        CP["Composition, hierarchy and stable assemblies"]
        IF["Directed exchanges and interfaces"]
        CO["Coordination and local autonomy"]
        FU["Functions and attributed purposes"]
        IC["Information-channel change in examined system"]
        IC -->|"Changes a feedback interface"| IF
        EL -.->|"Participate in"| CP
        CP -.->|"Exposes dependencies"| IF
        CO -->|"Supports or restricts local work"| EL
        FU -.->|"Local and wider roles"| CO
    end

    subgraph DYN["Accumulation and conditional mechanisms — Chapters 1 and 2"]
        direction TB
        ST["Stocks, regeneration and buffers"]
        FL["Inflows, outflows and transformations"]
        RU["Joint response rules and nonlinear relations"]
        TM["History, delays and pending effects"]
        LM["Joint capacities and constraints"]
        NA["Nonlinear domains and response uncertainty"]
        NA -.->|"Qualifies applicability"| RU
        ST -->|"State-dependent availability"| LM
        ST -->|"Affects rates where specified"| RU
        RU -->|"Governs"| FL
        FL -->|"Changes accumulation"| ST
        TM -->|"Retained conditions"| RU
        LM -->|"Constrains"| FL
    end

    subgraph CONTROL["Information, decisions and feedback — Chapters 1–7"]
        direction TB
        SE["Sensing and information sources"]
        PE["Actor perception, interpretation and memory"]
        GR["Actor goals, incentives and references"]
        DE["Discrepancy or departure from a reference"]
        AC["Intended action under an owned policy"]
        AS["Actor access, receipt and timing"]
        KC["Known or perceived constraints"]
        OPT["Perceived options and satisficing rule"]
        EX["Realized execution and effects"]
        AS -->|"Delivered constraint information"| KC
        PE -->|"Interpreted choice possibilities"| OPT
        KC -->|"Actor-context input"| AC
        OPT -->|"Candidate choice rule"| AC
        AC -->|"Attempted action"| EX
        FB["Balancing and reinforcing feedback paths"]
        SE -->|"Delivered through declared channels"| AS
        AS -->|"Attention, filtering and delay"| PE
        PE -->|"Condition used in comparison"| DE
        GR -->|"Reference for comparison"| DE
        DE -->|"Corrective input where applicable"| AC
        PE -->|"Other available decision input"| AC
        GR -->|"Other objective where applicable"| AC
        FB -.->|"Describes closed paths"| AC
    end

    subgraph RESTORE["Restoration and mechanism repair — Chapter 3"]
        direction TB
        CD["Constituent and interface condition"]
        AP["Alternative restorative mechanisms"]
        RP["Maintenance and repair processes"]
        SD["Shared dependencies and repair support"]
        CD -->|"May trigger repair"| RP
        SD -->|"Enables or limits repair"| RP
        RP -->|"Restores capability if successful"| CD
        SD -->|"May disable several alternatives"| AP
    end

    subgraph DEVELOP["Real organizational development — Chapter 3"]
        direction TB
        VA["Variation and permitted experimentation"]
        GE["Organizing or adaptation process"]
        RT["Retention and stabilization conditions"]
        CH["Actual change of organization"]
        VA -->|"Possible alternatives"| GE
        GE -->|"Produces new arrangement"| CH
        RT -->|"Persistence or rejection"| CH
    end

    subgraph BEHAVIOR["Conditional behavior and functioning — Chapters 1–7"]
        direction TB
        TR["Conditional model trajectories"]
        EV["Derived events and state or rate samples"]
        PT["Derived patterns and operating regimes"]
        OU["Outcomes at local and wider levels"]
        TR -.->|"Occurrences within history"| EV
        TR -.->|"Temporal characterization"| PT
        TR -.->|"Consequences under criteria"| OU
    end

    subgraph KNOW["Evidence and model construction — analyst level"]
        direction TB
        OB["Actual-system observations and source reports"]
        RE["Retained observation and report records"]
        PV["Sources, temporal context and uncertainty"]
        HY["Alternative mechanism explanations"]
        MP["Pattern-to-domain role and rule mapping"]
        MD["Versioned system description"]
        OB -.->|"Recorded with source identity"| RE
        HY -.->|"Candidate analogy where relevant"| MP
        MP -.->|"Qualified pattern instantiation"| MD
        RE -.->|"Qualified by"| PV
        RE -.->|"Supports or challenges"| HY
        HY -.->|"Candidate or accepted for use"| MD
    end

    subgraph SCENARIO["Scenario specification and analysis — analyst level"]
        direction TB
        IN["Initial state and required prehistory"]
        DR["Assumed future drivers and disturbances"]
        IV["Intervention target, direction and proposed change"]
        TS["Structural-transition state and history mapping"]
        AN["Conditional simulation or qualitative analysis"]
        FO["Commitments and foresight comparisons"]
        IP["Proposed observation or feedback intervention"]
        FO -.->|"Conditional timing assumptions"| AN
        IP -.->|"Scenario change only"| IV
        TS -.->|"Carry-over and validity rules"| AN
        IN -.->|"Initializes"| AN
        DR -.->|"Defines conditions"| AN
        IV -.->|"Defines hypothetical change"| AN
    end

    subgraph ASSESS["Assessment and revision — analyst level"]
        direction TB
        CM["Compare predictions, evidence and outcomes"]
        RA["Persistence, recovery and tradeoffs"]
        AD["Consistency, execution, empirical and decision adequacy"]
        RV["Targeted model revision or further inquiry"]
        CM -.->|"Assesses under disturbances"| RA
        CM -.->|"Separates adequacy claims"| AD
        AD -.->|"Findings and unresolved questions"| RV
    end

    B -.->|"Scopes included constituents"| EL
    EL -.->|"Holds or participates in"| ST
    IF -->|"Carries exchanges"| FL
    IF -->|"Carries signals"| SE
    X -->|"Boundary inputs and conditions"| RU
    FU -.->|"Actor-specific purposes"| GR
    CO -->|"Communicated allocations and permissions"| AS
    CO -->|"Actual authorization or allocation"| EX
    PE -->|"Status and needs for coordination"| CO
    ST -->|"Condition available to sensing"| SE
    EX -->|"Realized process effect"| FL
    EX -->|"Realized policy effect where applicable"| RU
    FB -.->|"Shares stock and rate mechanisms"| RU
    TM -->|"Response timing, not extra knowledge"| AC
    FL -->|"Creates pending effects where relevant"| TM
    CD -->|"Enables or degrades sensing"| SE
    CD -->|"Enables or degrades response"| RU
    AP -->|"Provides a feasible alternative response"| RU
    LM -->|"Restricts restorative capacity"| RP
    LM -->|"Restricts feasible generation"| GE
    CO -->|"Permits or restricts experimentation"| VA
    PE -->|"May inform adaptation"| GE
    CH -->|"Adds, removes or regroups"| EL
    CH -->|"Changes interfaces"| IF
    CH -->|"Changes coordination"| CO
    CH -->|"May create restorative routes"| AP
    CH -->|"May change governing rules"| RU
    FL -->|"Evolution of accumulated conditions"| TR
    CH -->|"Changes subsequent behavior"| TR
    CP -.->|"Defines relevant levels"| OU
    MD -.->|"Describes organization"| EL
    MD -.->|"Specifies candidate mechanisms"| RU
    MD -.->|"Analyzed model version"| AN
    AN -.->|"Produces conditional predictions"| TR
    TR -.->|"Predicted trajectory comparison"| CM
    CH -.->|"Transition to specify"| TS
    RE -.->|"Observed comparison"| CM
    OU -.->|"Outcome coverage"| CM
    CR -.->|"Evaluation criteria"| CM
    PT -.->|"Functioning regime"| RA
    CD -.->|"Condition in the examined model"| RA
    RV -.->|"Corrects our description"| MD
    RV -.->|"Selects another scenario"| AN
    RV -.->|"Reconsiders scope when justified"| B
    LM -->|"Actual modeled feasibility"| EX
    CD -->|"Actuation condition"| EX
    TM -.->|"Pending state and timing"| FO
    CM -.->|"Review response applicability"| NA

    subgraph INCENTIVE["Rules, consequences and changing capability — Chapter 5"]
        direction TB
        BB["Benefit and burden incidence"]
        RW["Reward allocation and conversion"]
        OP["Future capability and access"]
        GV["Governing rules and enforcement"]
        IR["Indicators and apparent compliance"]
        GU["Reference updates and rival comparisons"]
        IT["Intervention and corrective capacity"]
    end

    subgraph PATTERNS["Conditional archetype views — Chapter 5"]
        direction TB
        PA["Policy resistance and commons"]
        PB["Goal drift and escalation"]
        PC["Compounding advantage and dependency"]
        PD["Rule beating and wrong goals"]
    end

    FL -.->|"Attribute gains and costs"| BB
    BB -.->|"Distribution and delayed burdens"| OU
    FL -.->|"Shared reward process role"| RW
    RW -->|"Funds or grants future means"| OP
    OP -->|"Actual capability or access"| EX
    OP -->|"Can influence governance"| GV
    GV -->|"Actual access and enforcement"| EX
    GV -->|"Communicated incentives and rules"| SE
    GV -.->|"Defines formal success"| IR
    FU -.->|"Attributed intent to compare"| IR
    EX -->|"Activity selected for measurement"| IR
    ST -->|"Outcomes selected for measurement"| IR
    IR -->|"Reported success or compliance"| SE
    PE -->|"Perceived performance and rival history"| GU
    GU -->|"Changes reference where specified"| GR
    IT -->|"Relief or substitution effect"| FL
    IT -->|"May strengthen or erode"| CD
    IT -->|"May change visible signals"| SE
    LM -->|"Finite support resources"| IT
    GV -->|"Support authorization"| IT
    CD -->|"Corrective capability informs need"| IT
    RP -->|"May rebuild capacity"| IT
    IT -->|"May build or displace repair"| RP
    CH -->|"Can change adopted rules"| GV
    CH -->|"Can change reference mechanism"| GU
    AS -->|"Delivered rules, not hidden knowledge"| OPT
    MD -.->|"Candidate shared mechanisms"| PA
    MD -.->|"Candidate shared mechanisms"| PB
    MD -.->|"Candidate shared mechanisms"| PC
    MD -.->|"Candidate shared mechanisms"| PD
    PA -.->|"Competing goals and shared-resource hypotheses"| AN
    PB -.->|"Reference-update hypotheses"| AN
    PC -.->|"Opportunity and capacity hypotheses"| AN
    PD -.->|"Purpose-rule-indicator hypotheses"| AN
    CM -.->|"Support, contradiction and rival explanation"| PA
    CM -.->|"Support, contradiction and rival explanation"| PB
    CM -.->|"Support, contradiction and rival explanation"| PC
    CM -.->|"Support, contradiction and rival explanation"| PD
    IV -.->|"Candidate rule change only"| GV
    IV -.->|"Candidate reference change only"| GU
    IV -.->|"Candidate support change only"| IT
    GV -.->|"Actual rule transition to specify"| TS
    GU -.->|"Reference memory to preserve"| TS
    RW -.->|"Opportunity distribution"| CM
    IR -.->|"Compare proxy and intended outcome"| CM
    GR -.->|"Attributed actor references"| PA
    ST -.->|"Shared state and resource condition"| PA
    BB -.->|"Private and shared incidence"| PA
    GV -.->|"Access and control hypotheses"| PA
    GU -.->|"Reference-update paths"| PB
    GR -.->|"Formal and relative references"| PB
    PE -.->|"Perceived performance and rival state"| PB
    RW -.->|"Reward feedback"| PC
    OP -.->|"Future competitive means"| PC
    IT -.->|"Relief and capacity effects"| PC
    CD -.->|"Original corrective condition"| PC
    GV -.->|"Rule and enforcement correspondence"| PD
    IR -.->|"Apparent compliance and proxy result"| PD
    AC -.->|"Adaptive strategy hypothesis"| PD
    OU -.->|"Actual intended-outcome comparison"| PD

    subgraph FRAMING["Interpretation and implementation — Chapter 6"]
        direction TB
        FR["Owned actor or community assumptions"]
        AA["Analyst assumptions and alternative frames"]
        ADP["Adoption and implementation process"]
    end
    subgraph LEVERAGE["Conditional intervention targets — Chapter 6"]
        direction TB
        LA["12 Parameters; 11 Buffers; 10 Physical structure"]
        LB["9 Delays; 8 Balancing; 7 Reinforcing"]
        LC["6 Information; 5 Rules; 4 Self-organization"]
        LD["3 Goals; 2 Paradigms; 1 Reconsidering frames"]
    end

    FR -->|"Shapes interpretation where specified"| PE
    FR -->|"Can shape owned goals"| GR
    AS -->|"Available experience for belief update"| FR
    MD -.->|"Evidence-qualified actor frame account"| FR
    AA -.->|"Assumptions of candidate description"| MD
    AA -.->|"Alternative framing hypotheses"| HY
    RE -.->|"Can challenge analytical assumptions"| AA
    RV -.->|"Reconsider assumptions without rewriting evidence"| AA
    IV -.->|"Proposal or scenario adoption only"| ADP
    EX -->|"Realized authorized implementation activity"| ADP
    GV -->|"Authority and enforceable permissions"| ADP
    LM -->|"Implementation resources and limits"| ADP
    ADP -->|"Produces adopted organizational change"| CH
    ADP -->|"Changes adopted rules where specified"| GV
    ADP -->|"Changes reference mechanism where specified"| GU
    ADP -->|"Implements information-channel change"| IC
    ADP -->|"Enables or restricts actual experiments"| VA
    ADP -->|"May influence individual or social uptake"| FR
    ADP -.->|"Transition and retained history"| TS
    IV -.->|"Candidate target correspondence"| LA
    IV -.->|"Candidate target correspondence"| LB
    IV -.->|"Candidate target correspondence"| LC
    IV -.->|"Candidate target correspondence"| LD
    LA -.->|"State, capacity and topology to specify"| AN
    LB -.->|"Timing and complete feedback paths"| AN
    LC -.->|"Channel, institution and generation changes"| AN
    LD -.->|"Purpose and framed-assumption alternatives"| AN
    ST -.->|"Reserve, capacity and cohort meanings"| LA
    RU -.->|"Values, domains and critical regimes"| LA
    TM -.->|"Stage-specific relative timing"| LB
    FB -.->|"Corrective versus driving mechanism"| LB
    IF -.->|"New versus tuned channel"| LC
    GV -.->|"Rule-writing authority and adaptation"| LC
    GE -.->|"Generation, selection and retention"| LC
    FU -.->|"Local and wider purpose"| LD
    FR -.->|"Owned beliefs and priorities"| LD
    AA -.->|"Revisable analyst frame"| LD
    CM -.->|"Influence, direction, feasibility and criteria"| IV

    subgraph PRACTICE["Meaning, learning and responsibility — Chapter 7"]
        direction TB
        PI["Current versioned response policy"]
        PM["Actor monitoring and policy review"]
        UP["Candidate policy amendment"]
        ER["Actor-owned expectations and error review"]
        EJ["Analyst expectation and error record"]
        ME["Meaning, scale and domain correspondence"]
        QV["Qualitative concerns and affected-party coverage"]
        RR["Influence, burden, authority and responsibility"]
    end

    PI -->|"Rule used at this decision time"| AC
    PE -->|"Available interpreted monitoring input"| PM
    PI -->|"Current policy and owned expectations"| ER
    PE -->|"Experienced evidence for comparison"| ER
    ER -->|"Discrepancy and rival error accounts"| PM
    GR -->|"Owned review criteria where applicable"| PM
    GV -->|"Review and amendment permissions"| PM
    LM -->|"Finite monitoring and review support"| PM
    PM -->|"May generate a specified revision"| UP
    UP -->|"Candidate submitted for adoption"| ADP
    ADP -->|"Authorized implemented policy version"| PI
    PI -.->|"Policy history and pending effects to preserve"| TS
    PM -.->|"Actual learning mechanism to describe"| MD
    MD -.->|"Candidate response-policy description"| PI
    TR -.->|"Preserves original conditional expectation"| EJ
    RE -.->|"Independent evidence for aligned comparison"| EJ
    EJ -.->|"Discrepancy and unresolved explanations"| CM
    RV -.->|"Records retention or revision rationale"| EJ
    ME -.->|"Defines variables and permissible operations"| MD
    ME -.->|"Aligns observations and predictions"| EJ
    ME -.->|"Declared message interpretation correspondence"| PE
    PV -.->|"Source wording, transformations and dependencies"| ME
    MP -.->|"Qualified cross-domain meanings"| ME
    B -.->|"Causal scope and horizon correspondence"| QV
    BB -.->|"Affected parties and distributed consequences"| QV
    QV -.->|"Attributed concerns and disputed priorities"| CR
    QV -.->|"Qualitative or measured outcome interpretation"| CM
    TM -.->|"Slow state and residual commitments"| QV
    EX -.->|"Decision influence to trace"| RR
    BB -.->|"Burden and benefit incidence"| RR
    GV -.->|"Decision and amendment authority"| RR
    OP -.->|"Actual capacity to respond"| RR
    RR -.->|"Candidate missing consequence feedback"| IP
    RR -.->|"Attributed responsibility and legitimacy questions"| QV
    GU -.->|"Reference history and revision rationale"| CM
    CD -.->|"Existing local capability before intervention"| QV
    ER -.->|"Owned expectation history in transitions"| TS
    AS -->|"Available experience for policy review"| ER
    SE -.->|"Measurement and reporting provenance"| PV

    subgraph EDIRUN["EDI reasoning execution - engineering extension"]
        direction TB
        subgraph EDICONTEXT["Context and control"]
            direction TB
            RCTX["Scoped world, evidence and unknowns"]
            RPRO["Versioned systems reasoning protocol"]
            RCTL["Inquiry and tool controller"]
        end
        subgraph EDIMODELS["Replaceable model assistance"]
            direction TB
            RSTU["Pretrained student served by vLLM"]
            RTEA["Selective pretrained teacher guidance"]
        end
        subgraph EDIPROPOSAL["Reasoning outputs"]
            direction TB
            RALT["Rival mechanisms and explicit unknowns"]
            RTEST["Discriminating inquiries and scenarios"]
            RPATCH["Typed interpretations and model patches"]
        end
        subgraph EDIEXPLORE["Exploration and retained experience"]
            direction TB
            RFRONT["Adjacent, internal and temporal frontier"]
            RACCESS["Access requests and standing grants"]
            REPIS["Attributed attempts, guidance and outcomes"]
        end
    end

    RADMIT["C3 model admission and revision authority"]

    subgraph EDITRAIN["Future parameter learning - separate from runtime"]
        direction TB
        TCUR["Curated training episodes"]
        TTRAIN["Explicit student parameter-training job"]
        TCKPT["Candidate model or adapter checkpoints"]
        TADOPT["C7 operational checkpoint adoption"]
    end

    Q -.->|"Defines an inquiry"| RCTL
    B -.->|"Scopes context and resolution"| RCTX
    CR -.->|"Declared evaluation criteria"| RCTX
    RE -.->|"Selected records with availability"| RCTX
    PV -.->|"Source and uncertainty qualification"| RCTX
    ME -.->|"Meaning and temporal correspondence"| RCTX
    MD -.->|"Pinned model and dependency view"| RCTX
    AA -.->|"Declared analytical assumptions"| RCTX
    RPRO -.->|"Selects relevant reasoning operations"| RCTL
    RCTL -.->|"Bounded student request"| RSTU
    RCTX -.->|"Current scoped context"| RSTU
    RCTX -.->|"Declared teacher context"| RTEA
    RPRO -.->|"Systems reasoning guidance"| RTEA
    RSTU -.->|"Selected attempt and difficulty"| RTEA
    RTEA -.->|"Attributed critique and correction"| RSTU
    RSTU -.->|"Candidate explanations"| RALT
    RALT -.->|"Rivals and missing alternatives"| HY
    RALT -.->|"Questions that could separate rivals"| RTEST
    RCTL -.->|"Selects feasible methods"| RTEST
    RTEST -.->|"Scenario initial-history questions"| IN
    RTEST -.->|"Driver alternatives"| DR
    RTEST -.->|"Hypothetical intervention proposals"| IV
    RTEST -.->|"Analysis request through C0"| AN
    AN -.->|"Results or unsupported status through C0"| RCTL
    RTEST -.->|"Unresolved evidence needs"| RFRONT
    RFRONT -.->|"Proposes wider or deeper scope"| B
    RFRONT -.->|"Specific missing information"| RACCESS
    RACCESS -.->|"Requests permitted acquisition via C0-C7-C1"| OB
    RCTL -.->|"Assembles proposed changes"| RPATCH
    RSTU -.->|"Proposed interpretations and edits"| RPATCH
    RPATCH -.->|"Proposal with base version and evidence"| RADMIT
    RADMIT -.->|"Retains status and justified revision"| MD
    CM -.->|"Discrepancies and rival explanations"| RCTL
    RV -.->|"Further inquiry or proposed revision"| RCTL
    RSTU -.->|"Attempts and explicit rationales"| REPIS
    RTEA -.->|"Generated teacher feedback"| REPIS
    RTEST -.->|"Inquiry-selection history"| REPIS
    EJ -.->|"Original forecast references"| REPIS
    CM -.->|"Outcome assessments with lineage"| REPIS
    REPIS -.->|"Future scoped dataset selection"| TCUR
    RPRO -.->|"Declared learning objectives"| TCUR
    TCUR -.->|"Future frozen training input"| TTRAIN
    TTRAIN -.->|"Future changed weights or adapters"| TCKPT
    TCKPT -.->|"Candidate submitted for adoption"| TADOPT
    TADOPT -.->|"Future explicit loading of adopted version"| RSTU

    classDef edireason fill:#e8f1ff,stroke:#225ea8,stroke-width:2px
    classDef editeacher fill:#e8f7ec,stroke:#237a3b,stroke-width:2px
    classDef edifuture fill:#f2f2f2,stroke:#666666,stroke-dasharray:6 4
    class RCTX,RPRO,RCTL,RSTU,RALT,RTEST,RPATCH,RFRONT,RACCESS,REPIS,RADMIT edireason
    class RTEA editeacher
    class TCUR,TTRAIN,TCKPT,TADOPT edifuture

```

Solid arrows name candidate processes or dependencies; dotted arrows name scope, specification, evidence or assessment relationships. The map describes possibilities the representation can express, not a claim that every system contains all links. Actual observations enter retained evidence through OB→RE; model trajectories have no route becoming independent observation evidence. Actor intentions use declared actor inputs, while actual modeled constraints apply at execution. The diagram is a relationship map, not a mandatory processing pipeline or software-service stack.


**Chapter 5 interpretation:** BB is consequence attribution over existing processes; RW, OP, GV, IR, GU and IT are explicit roles or relationships within the nine families, not seven new physical primitives. PA–PD are four compact groupings displaying all eight traps; they are analytical hypotheses, not mutually exclusive modules or extra forces. The exact names and paths appear in section 28.4. All new arrows retain the same legend: solid = named process/influence/dependency; dotted = definition, evidence, attribution or analysis. A proposed change remains scenario-only until adoption and occurrence have their own evidence. Governing rules reach actor choice through declared information channels; unknown actual enforcement can still restrict execution.

Pairwise direct links and indirect shared dependencies are assessed separately under section 28.3. Each actor, stock, response and reference node denotes a role that can have many separately owned instances. It is not one global actor with access to everybody's information. The map is a capability schema, not a claim that every relationship is active in every system. Arrows do not prescribe universal signs, strengths or laws. Actual relationships need the contracts below. Specialization and resilience are assessed through existing organization, functioning, criteria and scenario paths; no ninth trap is invented.


**Chapter 6 interpretation:** FR and AA are separate accounts: actors do not inherit analyst knowledge or its preferred framing. ADP denotes a specified adoption/implementation process, not instantaneous obedience to a proposed lever. In a scenario all affected state remains scenario-scoped; real-world adoption and effects require evidence. LA–LD display all twelve source positions as target views with overlapping membership, not a fixed effectiveness ranking or extra causal forces. Solid paths require their actual mechanisms, resources and timing; dotted paths specify or assess candidates. Preserving a reference to an old path is not evidence that it is active in a particular system.


**Chapter 7 interpretation:** AC is intended action; PI is the current versioned rule. PI→AC→EX is ordinary response. PE/AS→ER→PM→UP→ADP→PI describes a possible policy-review return path, conditional on a specified review mechanism, authority and implementation. TR/RE→EJ→CM→RV concerns analyst model review; it cannot silently amend an actor's policy. ME declares meanings and correspondence, rather than giving analyst labels causal power. QV and RR reference shared consequences, concerns and authority; neither computes universal moral worth or blame. The same actor may perform several roles, and a reviewer may itself be a subsystem. Unknown updater, belief, value or causal relationship remains explicitly unknown.

**Evidence-path qualification:** a diagram arrow shows a typed relation, not permission to copy information. SE→PV supplies measurement/reporting metadata; it does not convert a modeled signal into an independent source record. Source observations still enter through OB→RE. Policy-monitoring evidence is available only through declared actor channels, never through the analyst's scenario predictions. The purpose of the three review paths is separation of ownership and status, not a claim that there are only three kinds of learning in nature.

## 4. The nine integrated representation families

Attributes are included when relevant and supported. This is not a mandate to populate every possible field or manufacture precision. A field may be unknown, inapplicable or deliberately omitted with a reason.

### 4.1 System view

**Meaning:** an organized subject examined at a selected scope, resolution and horizon.

**Attributes:** persistent subject; inquiry purpose; constituents and memberships; internal interactions; related wider/finer views; external drivers and exchanges; omissions and source/sink assumptions; proposed functioning; applicable operating regime; relevant local and collective purposes; conditions of partial independence.

**Connections:** brings constituents, stocks, processes and mechanisms into scope; links to other views through shared referents and specified interfaces; provides context for resilience and organization-change claims.

**Integration rule:** boundary selection does not assert physical isolation. One constituent may participate in several views without being copied into independent worlds. A named group is not automatically a demonstrated functional system.

**Chapter 3 addition:** the view identifies what must continue functioning, under which disturbances, and how local and wider organization contribute. A viable cyclic regime is permitted; a fixed target is not required.

**Chapter 4 integration:** Question-specific scope now includes applicability, omitted consequences and comparison with related views. Expanding an analytical boundary does not itself change the real organization; section 18 defines input closure and identity rules.

**Chapter 5 integration:** Include stakeholders, distributional perspectives, resource/sink governance, alternative opportunities and horizons over which delayed dependency or exclusion would matter. Preserve omitted interfaces and unresolved purpose conflicts.

**Chapter 6 integration:** Record intervention question, horizon, affected stakeholders and alternative analyst frames. A changed analytical view is distinct from changed world organization; compare outcomes with an explicit correspondence.

**Chapter 7 integration:** Record behavior-grounded inquiry, causal scope, affected-party coverage and evaluative scope separately. Physical time, observation cadence, planning horizon and value weighting are different assumptions.

### 4.2 Element or constituent

**Meaning:** a participating physical, biological, organizational or intangible constituent; it can itself be a system in another view.

**Attributes:** identity and aliases; descriptive role; composition and memberships; relevant properties; condition; capacity, lifetime and replacement history where meaningful; maintenance needs; local responsibilities and permissions; known substitutability; supporting dependencies.

**Connections:** participates in processes, holds or is associated with accumulations, receives information, affects responses and may be maintained, repaired, replaced or regrouped.

**Integration rule:** distinguish the referent from variables describing it and from its current membership. A tree is not identical to its biomass value; a supplier is not identical to its available capacity. The same sensor referenced by several feedback paths remains one sensor with one condition.

**Chapter 3 addition:** record mechanisms that preserve constituent functioning, stable intermediate assemblies and consequences of their loss. Do not delete a constituent solely because ordinary observations show little activity.

**Chapter 4 integration:** For relevant actors, distinguish identity, role, internal condition, information access, perceived options and actual effect capacity. Known private beliefs are not inferred from a role label; section 16 specifies their evidential status.

**Chapter 5 integration:** Actor, user, regulator, recipient and intervenor are roles of shared constituents. Record access, authority, capability and relevant support dependencies; one entity can occupy several roles without duplication.

**Chapter 6 integration:** Specify frame holders, implementers, recipients and rule-writing authority as attributed roles. Different actors can share a constituent or institution without sharing all information, values or beliefs.

**Chapter 7 integration:** Attribute policy ownership, review roles, implementation rights, local knowledge and consequence exposure separately. A role label does not establish a private belief or normative responsibility.

### 4.3 Stock or accumulated quantity

**Meaning:** an accumulation whose present condition reflects an initial state and its changes over time.

**Attributes:** accumulated subject; unit or qualitative meaning; current/initial/unknown condition; applicable domain; incoming/outgoing processes; relevant history; regeneration and loss rules; depletion and recovery conditions; buffer role where applicable.

**Connections:** flows change the stock; the stock can influence rates, observations, references, decisions and restoration capacity.

**Integration rule:** constant level does not mean no exchange, and equal levels do not establish equal futures. Information or capability can be modeled as accumulated only when that meaning is defensible; not every desirable property is a stock.

**Chapter 3 addition:** inventory, stored energy, trained personnel or spare material can support restoration, but whether they do so depends on the associated mechanisms. A stock is not itself proof of resilience.

**Chapter 4 integration:** Represent consequential upstream, downstream and environmental accumulations. Actual, estimated, actor-perceived and scenario states remain distinct accounts of shared referents, not extra physical quantities.

**Chapter 5 integration:** Include resource condition, wealth, skill or corrective capacity only where a defensible accumulation and history exist. Formal standards or opportunity can instead be computed relations; do not turn every desirable property into a stock.

**Chapter 6 integration:** Distinguish installed capacity, usable reserve, quality/access and replenishment. Retain age/cohort distributions or other independent history where they affect future rates; equal totals need not imply equal futures.

**Chapter 7 integration:** Preserve slow commitments and histories. Qualitative importance or a numerical rating does not by itself establish an accumulation, cardinal scale or calibrated mechanism.

### 4.4 Flow or changing process

**Meaning:** a process that adds, removes, transfers or transforms an accumulation. Related non-accumulative changes may be described as processes without pretending they are material flows.

**Attributes:** identity; what changes; source/destination and affected roles; rate/time basis if quantitative; response rule; prerequisites; capacity; resources; conversions/losses; delay, completion and pending effects where relevant.

**Connections:** one transfer can affect several stocks; joint conditions can govern its rate. Maintenance or repair can change constituent condition; organization-changing processes can change membership or interfaces.

**Integration rule:** distinguish material transfer, information and organizational change. If unlike quantities are transformed, declare the conversion. Refer to a shared process once rather than counting its capacity independently in every feedback path.

**Chapter 3 addition:** compensation, restoration, repair and reorganization are explicit process roles. One process may serve several roles; they are not mutually exclusive physical substances.

**Chapter 4 integration:** Distinguish attempted action from realized process effects under actual modeled constraints. Specify joint requirements, multiple outputs, source/sink limits and pending effects; intended success does not instantiate a successful transfer.

**Chapter 5 integration:** Represent appropriation, regeneration, pollution loading/removal, reward conversion, capability maintenance/loss and external relief as actual processes when applicable. Share transfers and capacity across all archetype views.

**Chapter 6 integration:** Represent construction, replacement, adoption, enforcement and implementation as processes with resources and time. Proposed changes cannot create stock or erase pending work without accounting.

**Chapter 7 integration:** Monitoring, review, experimentation, adoption and support are process roles with resources and timing. Compare strengthening existing corrective capability with substitution and displacement.

### 4.5 Information or influence link

**Meaning:** a condition, observation, signal or direct dependence influencing a response.

**Attributes:** source and recipient; direction; informational versus direct physical dependence; exchanged meaning; observed/reported/perceived status; observation and availability time; filtering, delay, coverage, distortion and uncertainty; condition and interruption when relevant.

**Connections:** conveys stock conditions or other inputs to an actor, mechanism, reference calculation or coordination process.

**Integration rule:** an available signal need not be noticed or acted upon. A physical dependency need not involve a sensing actor. Do not infer a causal influence from correlation alone.

**Chapter 3 addition:** information routing can enable local self-maintenance or create delay and overload. Its adequacy depends on the receiving responsibility and response, not merely on information volume or hierarchy depth.

**Chapter 4 integration:** Distinguish channel availability, receipt, attention and belief. Actor policies use information or physical influences delivered through declared mechanisms; global model state is not an automatic choice aid. Visible feedback can itself be an intervention.

**Chapter 5 integration:** Identify who receives resource condition, rival performance, formal rules and proxy reports, with attention, availability time, distortion and ability to act. A measured indicator is not automatic proof of purpose achievement.

**Chapter 6 integration:** Distinguish adding a new recipient or feedback path from tuning an existing channel. Specify content, delivery, attention, interpretation, ability to act and possible adverse response; received experience may update a particular frame through a stated mechanism.

**Chapter 7 integration:** Separate condition, measurement, reporting, publication, availability, receipt, attention and interpretation. Preserve source wording and report dependencies; communication can alter behavior.

### 4.6 Response relationship

**Meaning:** the proposed mechanism relating relevant inputs to a rate, signal, decision or change. It may be a physical relation, institutional policy, actor response or organization-generating rule.

**Attributes:** joint inputs; output/effect; equation, conditional rule or unresolved explanation; parameters; reference dependence; domains and limits; temporal memory; activation and completion semantics; resources and permissions; alternatives and source support.

**Connections:** reads current and retained conditions; governs processes or derived quantities; may be shared across feedback paths; may itself depend on a functioning constituent or interface.

**Integration rule:** a named connection is not a specified mechanism. Nonlinear or conditional sensitivity must not be flattened into one permanently valid coefficient. Unknown generating mechanisms remain unknown.

**Chapter 3 addition:** represent fallback activation, repair and structural development only to the extent supported. A rule that generates more structure is not automatically a learning rule or a useful adaptation.

**Chapter 4 integration:** Record nonlinear operating domains and actor interpretation/choice rules separately from execution. Each instantiated rule declares its inputs and role; physical execution constraints are not an automatic input to every actor-choice instance. Fixed nonlinear response at a new operating point is distinct from a new rule or topology; unknown psychological mechanisms stay unresolved.

**Chapter 5 integration:** Specify reference updates, rival comparisons, resource-use choices, reward allocation/conversion, strategy adaptation and support effects where relevant. Preserve unknowns and alternative rules; the trap name supplies no law.

**Chapter 6 integration:** Retain critical parameter ranges, relative timing, local gain meaning and frame-dependent interpretation where justified. No nominal leverage rank supplies the response law or outcome.

**Chapter 7 integration:** A changing action under a fixed rule is distinct from a changed policy. A policy updater requires a specified or explicitly unknown mechanism; an elicited curve remains evidence-qualified.

### 4.7 Function, purpose, reference and evaluation criterion

Keep four roles distinct:

| Role | Meaning | Example |
| --- | --- | --- |
| Function | What an organization does or contributes. | Replenishment supports fulfillment. |
| Purpose | An intended or inferred outcome attributed to a subject. | A dealer seeks reliable local service. |
| Reference | A condition used by a response mechanism. | Desired inventory calculated from perceived sales. |
| Criterion | How an observer or stakeholder evaluates outcomes. | Service loss, recovery duration, resource use or distribution of shortages. |

**Attributes:** owner/subject; scope and level; stated/inferred basis; horizon; fixed or computed reference; conflicts; feasibility; significance for functioning; unresolved interpretations.

**Integration rule:** a target is not an achieved outcome. A stakeholder criterion is not automatically every constituent’s purpose. Several legitimate criteria may conflict without a single agreed collective optimum.

**Chapter 3 addition:** make local–collective conflicts and coordination’s supporting role assessable. The model can describe excessive control without assuming all control is harmful or all local action beneficial.

**Chapter 4 integration:** Attribute incentives, pressures, aspiration levels and criteria to their subjects and horizons. Satisficing is an optional specified mechanism, not a universal optimizer or a moral assessment of the actor.

**Chapter 5 integration:** Distinguish attributed purpose, intended outcome, formal rule, indicator, target, compliance and evaluation criterion. A reference can depend on perceived history or a rival; legitimate revision and contested welfare remain representable.

**Chapter 6 integration:** Keep local references, wider purposes, viability, selection criteria, empirical belief and normative priority distinct. Announced goals and adopted operating selection can diverge.

**Chapter 7 integration:** Retain qualitative concerns, affected interests, contested priorities and reference histories. Better proxy performance, lowered standards and legitimate goal revision are distinct.

### 4.8 Feedback path

**Meaning:** a closed chain through which a changed condition returns to affect that condition.

**Attributes:** ordered participating quantities and mechanisms; closure evidence; balancing/reinforcing/unknown interpretation; applicable conditions; shared paths; timing and capacity; restorative role if supported; prerequisites and common dependencies.

**Connections:** references existing processes and relationships. Feedback adds no separate force to their equations.

**Integration rule:** loop closure, material direction and polarity are different meanings. Open chains remain valid descriptions. Relative influence can change with context; more loops do not guarantee better functioning.

**Chapter 3 addition:** distinguish a path restoring a condition, a path repairing a mechanism, and a process creating a different restorative arrangement. They may share vulnerable resources; repair does not imply an infinite hierarchy of guaranteed repair mechanisms.

**Chapter 4 integration:** Review contextual influence, saturation, delay and cross-boundary return paths without inferring a loop from one positive edge or correlation. A scope change may reveal an existing path rather than create one.

**Chapter 5 integration:** Allow several balancing and reinforcing paths to share mechanisms. Test commons, resistance, drift, escalation, compounding advantage or dependency only under their necessary conditions. Loop polarity alone does not establish exact exponential behavior.

**Chapter 6 integration:** Compare corrective paths relative to disturbance and self-amplifying drivers relative to their limits. More correction, faster reaction or more disclosure is not assumed always helpful; new loops need complete return paths.

**Chapter 7 integration:** Trace ordinary feedback and monitoring-based amendment as separately owned paths. Return consequences to decision makers through actual channels; do not infer an ethical conclusion or good response from closure alone.

### 4.9 Behavior history and conditional trajectory

**Meaning:** how modeled or observed conditions unfold over an interval.

**Attributes:** variables and roles; units/time basis; initial condition and relevant history; driver schedule; policy and structural version; observation/scenario status; horizon; changes of regime; degradation, recovery, oscillation or depletion where relevant; uncertainty and applicability.

**Connections:** histories constrain descriptions; a model and scenario yield conditional expectations; comparisons assess both ordinary and disturbed functioning.

**Integration rule:** an event is not an entire pattern, and a pattern does not uniquely establish one mechanism. Similar trajectories can arise from different structures; one structure can generate several behaviors.

**Chapter 3 addition:** retain histories of mechanism condition and organizational development alongside output. This permits stable recent output and declining restoration capacity to coexist in the same description.

**Chapter 4 integration:** Compare histories of variability and changed operating regimes as well as averages. Predictions, actor forecasts and actual observations retain separate source/time status; evidence does not arise by relabeling generated samples.

**Chapter 5 integration:** Retain separate histories of actual and perceived performance, references, effort, costs, distribution, opportunity, capacity and wider outcomes. A smaller discrepancy, higher proxy or stable output is not automatically improvement.

**Chapter 6 integration:** Compare baseline and changed scenarios across applicable histories, conditions and criteria. Preserve distribution, transition, irreversibility and uncertainty; assessment can remain qualitative or unresolved.

**Chapter 7 integration:** Preserve mean, variability, extremes, aggregation, regime and timing. Keep original expectations beside independent observations and unresolved error causes; compare near and distant effects without claiming omniscience.

## 5. Shared evidence, identity and time

### 5.1 Evidence annotations

| Axis | Required distinction |
| --- | --- |
| Descriptive role | Event, state/rate sample, behavior pattern, structural relationship, mechanism or purpose claim. |
| Evidential basis | Directly measured/inspected, source-reported, inferred, assumed or unresolved. |
| Temporal meaning | When it applied, when it was observed/reported, and when information became available. |
| Modeling use | Retained evidence, candidate explanation, accepted-for-use description or conditional scenario output. |
| Applicability | System view, conditions, horizon, known exclusions and alternatives. |

These axes are independent. Structure may be inspected directly; an event report may be uncertain. Recording an interface removal as an event and revising the structural description from it does not create two independent observations. “Accepted for use” is not equivalent to proven truth.

### 5.2 Complete relevant temporal state

Preserve whatever retained information the chosen mechanisms need: physical accumulations, perceived estimates, pending orders or repairs, relevant histories, current policy, constituent condition and organizational configuration.

Not every delay needs another physical stock. A queue, retained time history or equivalent lag state can represent a delayed mechanism if its semantics are preserved. Equal visible stocks may have different futures because their pipelines, damaged mechanisms or organizational arrangements differ.

### 5.3 Identity and change

Preserve the identity of a constituent where evidence supports continuity, while allowing its state, role, membership and connections to change. Replacing a part need not erase organizational continuity; retaining a name does not prove it. Shared membership must not duplicate physical quantities, pending commitments or restoration capacity.

### 5.4 Chapter 7 shared record discipline

Meanings, qualitative concerns and learning decisions use the existing referent and provenance spine. Section 45 gives their minimum contracts. Preserve the original account, the interpretation, correction and version as distinct entries. A term's meaning cannot be changed after a forecast merely to erase a discrepancy. A qualitative statement can be usable without a numerical coefficient; a missing measurement is not a zero effect or a false claim of a known effect.

### 5.5 Temporal and epistemic ownership

An actor or reviewer uses its actually available inputs at the decision time. A later source report, analyst prediction or preferred frame cannot be inserted into its earlier knowledge. A policy version, forecast version, model version and observed history have separate identities. Changes preserve commitments and historical expectations. When observation itself changes the system, the corresponding information intervention has its own proposed/adopted/realized status.

## 6. The integrated mechanisms

### 6.1 Dynamics and constraints

For quantitative stocks:

\[
\frac{dx_i}{dt}=\sum_{j\in\mathrm{in}(i)}f_j-\sum_{k\in\mathrm{out}(i)}f_k.
\]

Rates can depend on current conditions, retained history, inputs, organization and policies:

\[
f_j(t)=g_j\big(x(t),m(t),u(t);G(t),\theta(t),\pi(t)\big).
\]

Here m is the relevant memory or pending state, u selected external inputs, G constituents and relationships, theta mechanism parameters and pi policies/references. This is our formalization, not notation prescribed by Meadows. Qualitative mechanisms remain legitimate without invented numbers.

Keep four constraint meanings separate:

- Real-system limits: resources, capacities, response times and feasible permissions.
- Scenario assumptions: selected future drivers, disruption duration or proposed policy.
- Modeling validity: units, initialization, numerical timing and applicability.
- Stakeholder requirements: wanted outcomes, including who should benefit.

### 6.2 Restoration, repair and meta-resilience

A complete restoration description identifies the retained function or regime, disturbance, sensing or direct trigger, response, capacity, delay, resources and outcome evidence. Alternative paths require examination of common dependencies and switching conditions.

Repair adds the damaged mechanism’s condition and a process that restores it. A repair process may itself require information, skilled work, materials or an operating interface. Those needs can remain explicit boundary assumptions when not modeled internally. The description must permit repair failure and delayed repair.

Resilience is then an assessed property of this arrangement under specified disturbances and criteria. It is not universally a scalar variable, a return to equilibrium, or an extra force added to the dynamics.

### 6.3 Self-organization and real structural transitions

An actual change can modify G, a rule, a parameter or a coordination arrangement. Describe the changed subject, circumstances, producing process, possible changes, resources/restrictions, retention and consequences.

Where a rule is known, one possible formal description is:

\[
G(t^+)=\Phi\big(G(t^-),x,m,u;\rho\big).
\]

Phi denotes the particular proposed generating process, not a universal self-organization algorithm. An observed structural change may be retained even when Phi is unresolved. A change is internal or externally imposed relative to the stated system view; the boundary matters to that distinction.

Increasing complexity, adding variation and useful learning are different claims. New organization can fail, consume resources, introduce fragility or support persistence. The architecture keeps those possibilities open.

### 6.4 Hierarchy, autonomy and coordination

Represent nested or overlapping membership, stable assemblies and cross-system relationships separately. A part-of relation is not a supply link, reporting line or right to control. Hierarchical composition can coexist with network interactions.

For local regulation, specify available information, responsibilities, maintenance needs and permitted responses. For wider coordination, specify the service provided, information used, resources allocated and restrictions imposed. Compare effects at the levels concerned.

Partial decomposability is conditional: state which local functions remain possible, for how long, and with which exchanges removed or retained. Recheck this when coupling changes. A formerly minor external dependency can become essential.

### 6.5 Response, policy amendment and explanatory revision

Ordinary action follows the current owned rule, interpreted inputs and actual execution constraints. A policy-review process may compare an owned expectation with received evidence and propose a changed rule, target or structure. It needs a trigger or cadence, updater, candidate alternatives, authority, resources and adoption; none is supplied by the word learning. Independently, an analyst may compare original predictions with evidence and revise an explanation, boundary or assumption. Revising that explanation need not change any actor's beliefs, permissions or policy.

Errors can reflect measurement, reporting, changed conditions, model inadequacy, implementation failure or several causes. Preserve rival explanations and discriminate where possible; failure to predict does not uniquely identify the correct repair. Useful simplification and partial prediction remain possible within stated domains. Neither a smaller step nor a more frequent update guarantees stability or improvement.

## 7. Interface and integration contracts

Every consequential interaction must have identifiable participants and meaning. This does not require a physical connection between every pair of systems.

| Interaction | Minimum contract | Integration check |
| --- | --- | --- |
| Flow ↔ affected stocks | Quantity, direction, rate/time basis and conversion if needed. | One transfer is accounted consistently at all affected stocks. |
| Information → response | Source meaning, availability, filtering and recipient use. | The response does not use information unavailable at its decision time. |
| Reference → response → process | Owner, calculation, feasibility and effect. | A computed target is not mistaken for achieved functioning. |
| Constituent/interface condition → process | What condition enables or restricts which mechanism. | A damaged mechanism cannot continue operating at assumed full capacity without an explanation. |
| Repair → mechanism condition | Required resources, initiation, delay and restored capability. | Repair competes consistently for resources and may fail or remain incomplete. |
| Organization change → membership/relationship | Actual transition, source process, time and affected roles. | A real change is distinguished from a correction to the model. |
| Local subsystem ↔ wider coordination | Separate information, allocation, permission and response directions. | Local maintenance and collective effects are both visible. |
| System view ↔ another view | Shared identities, exchanged quantities, timing and boundary assumptions. | No duplicated constituent, flow, resource or pending commitment. |
| Actor context → intention | Received information, internal state, perceived options and known permissions. | Hidden global feasibility does not silently remove choices or select a better intention. |
| Intention → realized process | Attempted response, actual modeled capacity, enforcement and physical effect. | Attempts may fail or differ from expectation; actual resource limits act on execution without granting knowledge. |
| Boundary revision → input closure | Former driver, new internal mechanism, shared state and output correspondence. | The same influence is not simultaneously counted as an independent driver and its internal explanation. |
| Measurement/feedback change → information channel | Proposed versus included status, recipients, timing and resulting exposure/effects. | A change to actor-visible feedback is not automatically passive or proven effective. |
| Response domain → assessment | Operating range, nonlinear features, unknowns and rival mechanisms. | A mode change does not uniquely identify the rule or justify unbounded extrapolation. |

For A→B and B→A, specify distinct content and mechanisms. A two-way exchange need not be symmetric in capacity, delay, authority or vulnerability. A one-way signal can close a feedback path only through other specified relationships; the word “bidirectional” alone establishes neither feedback nor mutual influence.

For a collection of components, review each pair for consequential direct exchanges, meaningful absence and indirect shared dependencies. Do not invent all-to-all links or infer absence from silence. Record unresolved interfaces where the evidence is insufficient.

**Master-map correspondence:** the same information, directed exchanges, common dependencies, maintenance and analyst-comparison paths are included in the single connected map in section 3. The surrounding contracts retain the detailed meanings.

This is an example topology, not a requirement that every system possess a central authority. It exposes both exchanges and a common vulnerability that a simple hierarchy tree would conceal.

## 8. One continuous worked model: inventory, restoration and coordination

### 8.1 Retained Chapter 2 candidate

One dealer holds inventory I in cars, receives deliveries A and makes sales S in cars/day. Requested demand D is external. Perceived sales P support desired inventory I-star and order rate O. Retain the selected parameters C=10 days coverage, W=5 days trailing perception, tau=3 days adjustment and L=5 days delivery delay:

\[
P(t)=\frac{1}{W}\int_{t-W}^{t}S(v)\,dv,\qquad I^*(t)=C P(t),
\]

\[
O(t)=\max\left(0,P(t)+\frac{I^*(t)-I(t)}{\tau}\right),\qquad A(t)=O(t-L),
\]

\[
\dot I=A-S.
\]

The declared fulfillment candidate uses lost sales, not backlog: S=D while I>0, and S=min(D,A) at I=0. Negative inventory is invalid. A numerical implementation needs a declared event/boundary procedure. W and tau must be positive; zero-delay/instant-response limits need separate definitions.

With pre-change demand d0>0, initialize I(0)=C d0 and the relevant sales/order prehistory to d0. This initializes perceived demand and the delivery pipeline, not just the visible stock.

These are our chosen candidate equations. The baseline retained an unresolved source discrepancy: the text uses a five-day averaging description while the Figure 33 caption refers to three days. The selected W does not resolve that discrepancy, and no exact curve reproduction is claimed.

### 8.2 Why Chapter 3 requires a changed supplier assumption

The original A=O(t-L) guarantees fulfillment after a delay. It can examine ordinary replenishment, but supplier failure is excluded by construction. A disruption model must replace that equation explicitly rather than silently retaining guaranteed deliveries.

For one illustrative extension, separate two delivery pipelines Q1 and Q2 and their dispatches U1 and U2. Let O1 and O2 be the orders routed to the respective arrangements:

\[
O_1+O_2=O,\qquad \dot Q_k=U_k-A_k,\qquad A=A_1+A_2.
\]

An order, dispatch and arrival are different events. The extension must specify how orders become dispatches, whether undelivered orders wait or are lost, how arrivals depend on transport and lead times, and how the pipelines are initialized. A queue or retained shipment history may be more appropriate than a simple first-order rate; the pipeline balance alone does not define the delivery law.

Represent supplier/route availability, dispatch capacity, outstanding commitments, switching rules and the dependencies shared by both routes. If these mechanisms are unresolved, this extension remains a conceptual candidate; it cannot generate a justified numerical trajectory yet.

### 8.3 Integrated restorative and organizational mechanisms

| Mechanism | Shared-core representation | What it explains |
| --- | --- | --- |
| Inventory buffer | Existing stock I, coupled to fulfillment. | Temporary service while arrivals are restricted. |
| Alternative supply | Another supplier/route, dispatch and arrival processes, plus routing response. | Substitution under stated capacity and timing. |
| Shared transport hub | One constituent/dependency referenced by both routes. | Why apparently separate routes may fail together. |
| Order-channel repair | Channel condition, repair process, required support and completion history. | Recovery of the original mechanism. |
| New supplier formation | Actual relationship transition and the process that produces it. | A possible organization-changing response. |
| Wider allocation | Shared supply constraints, local requests, allocation rule and permissions. | Coordination and local–collective effects. |

None is an independent “resilience object.” Their combined behavior supports or contradicts a resilience claim under a specified disturbance.

### 8.4 Adding another dealer without duplicating the supplier

With dealers a and b, retain separate inventories and local histories but one identity for each shared supplier and hub. If supplier k has dispatch capacity c-k in cars/day, the chosen model must respect:

\[
U_{k,a}+U_{k,b}\leq c_k.
\]

The allocation rule remains to be specified. Giving each dealer access to full c-k simultaneously would invent capacity. Local requests, supplier allocation, observed shortages and central permissions need not have the same timing.

An aggressive local ordering policy may protect one dealer while disadvantaging another; wider allocation may improve collective service while slowing some local adjustments. Those are conditional comparisons, not established outcomes or reasons to assume universal centralization.

### 8.5 Four changes that must remain distinct

1. More cars arrive: state changes within the arrangement.
2. A broken channel is repaired: a mechanism’s functioning is restored.
3. A dealer establishes a new supplier relationship: actual organization changes.
4. We discover a backup relationship that already existed: our description changes.

Same current inventory does not imply the same future: one dealer may have deliveries already dispatched, another may face an unrepaired channel, and another may have a functioning alternative. Recent sales alone cannot distinguish all these conditions.

### 8.6 Continuous scenario family

Retain Chapter 2’s demand step, perception-window and adjustment-time contrasts, equal-visible-stock/different-history comparison, and finite-supply/backlog alternatives. Add:

- Supply interruption with duration and affected mechanism specified.
- Buffer-only versus alternative-route arrangements under comparable conditions.
- Independent versus common-dependency alternatives.
- Delayed or unavailable repair support.
- Temporary compensation followed by withdrawal.
- Creation of a new relationship versus a pre-existing relationship discovered later.
- Local ordering versus wider allocation, including restrictions on local response.

Assess fulfillment, unmet demand, inventories, resource use, interruption/recovery and the distribution of consequences. Different criteria may disagree. No numerical scenario has been run or policy ranking established here.

## 9. Model definition, scenarios, assessment and revision

The actual system, the model describing it and a hypothetical experiment remain distinct.

| Modeling record | Meaning |
| --- | --- |
| Model definition | Selected views, constituent identities, mechanisms, parameters, history rules, organization, boundary and supporting evidence. |
| Scenario | Model version, starting state/history, external inputs, disturbances, proposed interventions, horizon and numerical settings where applicable. |
| Result | Conditional trajectories, organizational transitions, diagnostics, uncertainty and any invalid/truncated interval. |
| Assessment | Agreement with evidence, driver plausibility, response adequacy, wider causes, stakeholder outcomes and alternative explanations. |

**Master-map correspondence:** the same information, directed exchanges, common dependencies, maintenance and analyst-comparison paths are included in the single connected map in section 3. The surrounding contracts retain the detailed meanings.

Evidence can also support or challenge an individual mechanism directly; it need not enter only through a whole-trajectory comparison. This workflow does not establish a unique causal model merely because one candidate matches past behavior.

Revision can target a state estimate, retained history, parameter, policy/reference, mechanism, topology/composition, interface, membership or boundary. Every revision needs its subject, applicable time, source or assumption, previous interpretation and consequences for prior conclusions.

Keep separate:

- An actual-world change that the description records.
- New evidence correcting an earlier description.
- A rival explanation retained for comparison.
- A hypothetical intervention used in a scenario.

Neither updating a graph nor retaining a version history proves that the external system has reorganized or learned. Model uncertainty and real structural change can coexist.

## 10. Requirements and verification allocation

I7-R01–I7-R20 preserve the corresponding I4 requirement meanings; I7-T01–I7-T28 preserve the corresponding I4 scenario definitions. These are namespace mappings, not new empirical passes. All 16 Chapter 4 parent requirements are allocated below. A requirement describes what the representation must permit, including absent or unresolved mechanisms.

| Integrated requirement | Obligation | Earlier requirement parents | Chapter 3 allocation | Chapter 4 allocation | Integrated check |
| --- | --- | --- | --- | --- | --- |
| I7-R01 | Preserve identity, organization and overlapping views. | C1-R01/R02/R05; C2-R01/R05/R06 | C3-R07/R08/R10 | Retained prior obligation | I7-T01 |
| I7-R02 | Distinguish stocks, flows, information and response with coherent accounting. | C1-R03/R06/R07/R08; C2-R02/R07/R09 | C3-R02/R03 | C4-R06 | I7-T02/I7-T15 |
| I7-R03 | Preserve complete relevant temporal state. | C1-R06/R09/R13; C2-R04/R07 | C3-R02/R03/R05 | C4-R10 | I7-T03 |
| I7-R04 | Preserve conditional joint mechanisms, limits and shared resources. | C1-R07/R11/R13; C2-R02/R03/R05/R06/R09/R10 | C3-R02/R08 | C4-R06 | I7-T04/I7-T16 |
| I7-R05 | Distinguish purposes, references and criteria at relevant levels. | C1-R04/R12; C2-R02/R08/R12 | C3-R01/R11 | C4-R14, C4-R16 | I7-T05/I7-T27 |
| I7-R06 | Qualify resilience by functioning, regime, disturbance and horizon. | C1-R08/R13; C2-R01/R03/R11 | C3-R01/R04 | C4-R05 | I7-T06 |
| I7-R07 | Represent compensation, repair and restoration support without automatic success. | C1-R07/R11/R13; C2-R03/R05/R06/R10 | C3-R02/R03 | C4-R05 | I7-T07 |
| I7-R08 | Represent real organizational development separately from model revision. | C1-R02/R05/R14; C2-R06/R13 | C3-R05/R06 | Retained prior obligation | I7-T08 |
| I7-R09 | Preserve directed interfaces and conditional decomposability. | C1-R10/R11/R13; C2-R05/R06 | C3-R08/R09 | C4-R06 | I7-T09 |
| I7-R10 | Compare coordination and autonomy, including local–collective conflict. | C1-R04/R12; C2-R08/R12 | C3-R10/R11 | C4-R14, C4-R16 | I7-T10 |
| I7-R11 | Retain sources, alternatives, unknowns and distinction between event and structure. | C1-R14; C2-R04/R13 | C3-R12 | C4-R01, C4-R02, C4-R15 | I7-T11/I7-T26/I7-T28 |
| I7-R12 | Assess conditional behavior, wider causes and decision relevance separately. | C1-R13/R14; C2-R12/R13 | C3-R01/R04/R09/R11/R12 | C4-R01, C4-R02, C4-R03, C4-R05, C4-R16 | I7-T12/I7-T27/I7-T28 |
| I7-R13 | Qualify pattern reuse through domain roles, mechanism correspondence, units, timing and applicability. | C1-R13/R14; C2-R06/R13 | C3-R12 | Retained prior obligation | I7-T13 |
| I7-R14 | Preserve referent, quantity, history and commitment meaning across structural transitions. | C1-R05/R06/R07; C2-R07/R08/R13 | C3-R05/R06 | Retained prior obligation | I7-T14 |
| I7-R15 | Represent actor-specific information, interpretation and perceived options separately from intended action and realized effects. | C1-R04/R14; C2-R04/R07 | C3-R09/R11/R12 | C4-R12, C4-R13, C4-R14 | I7-T17/I7-T18/I7-T19 |
| I7-R16 | Qualify nonlinear response domains and distinguish operating-point, parameter, rule and topology explanations. | C1-R13/R14; C2-R10/R11/R13 | C3-R01/R12 | C4-R03, C4-R04, C4-R05 | I7-T21 |
| I7-R17 | Compare query-specific views with explicit boundary closure, shared identity and output correspondence. | C1-R10; C2-R05/R06 | C3-R07/R09 | C4-R06, C4-R07 | I7-T23/I7-T24 |
| I7-R18 | Represent joint, uncertain and evolving constraints with compatible quantities and shared resources. | C1-R07/R12; C2-R09/R10 | C3-R02/R08 | C4-R08, C4-R09 | I7-T22 |
| I7-R19 | Assess stage-specific delays, relevance and foresight under incomplete commitments and uncertain inputs. | C1-R09/R13; C2-R07/R08/R13 | C3-R02/R04 | C4-R10, C4-R11 | I7-T25 |
| I7-R20 | Distinguish passive records, proposed information interventions and changes in examined feedback channels. | C1-R03/R14; C2-R04/R08 | C3-R05/R09/R12 | C4-R15 | I7-T20 |

These rows allocate checks, not proof of implementation. The detailed parent catalogues remain applicable: C2-T01–C2-T32, C3-T01–C3-T27 and C4-T01–C4-T40. Several describe related scenarios and should not be summed as independent demonstrations.

## 11. Integrated acceptance scenarios

**All cases are planned, not executed.** These checks exercise the combined architecture rather than repeating the chapter summaries. A check can reveal missing information and need not produce a numeric answer.

| Test | Combined scenario | What must be assessable |
| --- | --- | --- |
| I7-T01 | Two dealers share a supplier, and one constituent appears in several views. | One referent and one shared capacity, with distinct local memberships and states. |
| I7-T02 | Add deliveries, sales and a repair consuming spare material. | Compatible accounting, explicit conversions, no conflation of information with physical transfer. |
| I7-T03 | Equal current inventory but different pipeline, perceived demand or repair progress. | Different conditional futures are possible without inventing a current inventory difference. |
| I7-T04 | Activate several fallback mechanisms using one limited resource. | Shared constraints and response delays restrict simultaneous operation. |
| I7-T05 | Local inventory targets improve while another dealer loses essential service. | Local references and criteria remain distinct from wider outcome assessment. |
| I7-T06 | Ordinary output remains constant as backup support degrades; also examine a functioning cyclic regime. | Constancy is not proof of resilience, and oscillation is not automatically failure. |
| I7-T07 | Damage an ordering interface, delay repair, then withdraw external compensation. | Separate continued operation, repair, temporary substitution and recovered internal functioning. |
| I7-T08 | Compare increased stock, repaired channel, a newly formed relationship and a newly discovered old relationship. | State, condition, actual organization and our knowledge change retain distinct meanings. |
| I7-T09 | Isolate a subsystem, interrupt assembly, then introduce a critical shared dependency. | Partial functioning, retained intermediates and the revised limits of decomposability. |
| I7-T10 | Compare local authority, wider allocation and approval of every response. | Coordination benefits, permission delays, maintenance needs and consequences at several levels. |
| I7-T11 | Supply uncertain event reports and competing mechanisms that fit a history. | Provenance, uncertainty, alternative explanations and unsupported causal claims remain visible. |
| I7-T12 | Compare demand/policy scenarios, supply disruption and possible new organization. | Driver plausibility, response adequacy, causes outside the boundary, criteria and applicability are assessed separately. |
| I7-T13 | Map population and capital to a shared pattern, then change one response to a delayed or nonlinear rule. | Record the extent and limits of correspondence; matching topology alone cannot authorize parameter or trajectory transfer. |
| I7-T14 | Retire or merge a stock-holding constituent while deliveries and repair are pending. | Preserve or explicitly account for quantities, referents, commitments and histories; unknown carry-over makes subsequent execution unresolved rather than silently resetting it. |
| I7-T15 | Compare zero exchange with equal nonzero inflow/outflow at the same stock level; compare inflow and outflow interventions. | Same net change does not imply identical turnover, resource dependence, costs or effects at connected stocks. |
| I7-T16 | Let a productive process consume finite supply and create waste with finite removal. | Both source and sink assumptions constrain the candidate; moving a cloud or renaming a resource does not make capacity unlimited. |
| I7-T17 | Give the analyst wider state knowledge than an actor’s delivered history. | Actor-specific information and internal interpretation are explicit; no future or analyst-only input silently enters the choice rule. |
| I7-T18 | Hold actor information, internal state, perceived options and policy fixed while varying a hidden execution constraint. | The hidden condition does not improve intention by oracle filtering; realized acceptance/effect may differ through specified mechanisms. |
| I7-T19 | Compare candidate satisficing, attention, role and incentive mechanisms under the same declared external conditions. | Private states remain qualified; actor replacement and role redesign are distinct comparisons, not preselected answers. |
| I7-T20 | Compare a hidden logger, a visible display, a proposed channel change and one actually included in the examined system. | Record data availability versus actor exposure, adoption time, possible response and separate outcome evidence. |
| I7-T21 | Move the operating point of a fixed nonlinear mechanism, then compare parameter, rule and topology alternatives. | Do not identify one change type from the trajectory alone; preserve domain, threshold and saturation uncertainty. |
| I7-T22 | Relieve one production constraint while skill, material or removal capacity changes. | State-dependent bottlenecks, simultaneous constraints, unknown inputs and source/sink units remain explicit; no universal minimum law is assumed. |
| I7-T23 | Internalize a formerly external demand or supply variable by expanding the view. | Replace or condition the old closure; do not add both accounts as independent contributions or duplicate shared quantities. |
| I7-T24 | Compare a wide and narrow view with different aggregation, then remove a consequential subsystem. | Define output correspondence and an omission closure; unknown replacement dynamics remain unresolved rather than disappearing. |
| I7-T25 | Compare fast information, delayed physical completion, pending commitments and a short threshold-crossing disturbance. | Relevance follows consequences, not duration alone; foresight remains conditional and does not use later outcomes as earlier information. |
| I7-T26 | Feed one observation through several reports or pass a prediction through another model. | Preserve source dependence and predicted status; repetition or citation count does not create independent confirmation. |
| I7-T27 | Examine the budworm/host/natural-control/management candidate across weather histories and stakeholder horizons. | Separate trigger and susceptibility, changing control strength, target/non-target effects and ecological versus industrial outcomes. |
| I7-T28 | Compare meter visibility, household selection, load/configuration and recording explanations. | Keep association, mediator hypotheses and causal claims distinct; the reported one-third contrast is not a calibrated effect. |

For a quantitative run, additionally specify the full equations and closures, units, initial and pending history, disturbance schedule, transition semantics, boundary handling, numerical settings and diagnostics. For empirical validation, obtain independent observations relevant to the claimed mechanisms and conditions. A structural diagram alone satisfies neither obligation.

## 12. Integration review and architecture decisions

| Decision | Rationale | What would justify revision |
| --- | --- | --- |
| Retain nine shared representation families. | The four chapters’ needs can be expressed through their constituents, processes, rules, purposes and histories. | A real case exposes a necessary meaning that cannot be represented coherently. |
| Treat restoration, organization, hierarchy and actor perspective through shared derived views. | Avoid duplicates and opaque explanatory labels. | Queries or mechanisms require a more explicit shared description, without losing traceability. |
| Keep functioning and resilience contextual. | Acceptable regimes and disturbance effects differ by subject, horizon and stakeholder. | Domain evidence supports a more precise criterion for a particular application. |
| Make organizational change explicit but permit unknown generators. | Actual development is different from both ordinary dynamics and improved observation. | Evidence identifies a specific generating rule or contradicts the proposed one. |
| Support hierarchical and network relationships together. | Membership, coordination and exchange are different relationships; overlap matters. | A particular domain supports a narrower representation for a particular purpose. |
| Assess shared dependencies before counting alternatives. | Apparent redundancy may share a failure mechanism or resource limit. | Evidence establishes meaningful independence under the disturbances examined. |
| Keep assessment and revision separate from external-world dynamics. | A better description is not automatically a changed world. | A specified intervention actually changes the system and its effects are observed. |

### Retained allocation of the Chapter 3 extension

All Chapter 3 foundation groups have an allocation in this unified model:

| Chapter 3 foundations | Integrated location |
| --- | --- |
| F01–F03: conditional functioning, caution and persistence | System view; evidence/applicability; I7-R06. |
| F04–F08: restoration paths, timing, redundancy, repair and new restorative organization | Feedback/process families; section 6.2–6.3; I7-R03/R07/R08. |
| F09–F12: dynamic regimes, hidden fragility, tradeoffs and internal capacity | Purpose/criteria and history families; I7-R05/R06/R07. |
| F13–F19: self-organization, diversity, variation, restrictions, generating rules and uncertainty | Response family and structural transitions; I7-R08/R11. |
| F20–F25: membership, local regulation, intermediates, coupling, information and partial decomposition | System/constituent/link families; interface contracts; I7-R01/R09. |
| F26–F29: cross-level causes, changing integration and coordination development/support | Wider/finer views, structural history and coordination; I7-R08/R09/R10/R12. |
| F30–F32: suboptimization, overcontrol and coordination–autonomy balance | Purpose/criteria, permissions and comparative scenarios; I7-R05/R10. |

### Preserved Chapter 1–2 obligations

Elements/interconnections/functions; stock–flow accumulation; balancing/reinforcing feedback; joint and conditional mechanisms; capacities and regeneration/depletion; relevant initial conditions and delay history; multiple purposes and references; external drivers and explicit boundaries; several possible behaviors; evidence, alternatives and uncertainty; scenario/result separation; and revision of specific claims all remain in the architecture.

The thermostat, population, industrial capital and renewable/nonrenewable-resource cases continue to use the same representation. Their actual equations and evidence remain domain-specific. Chapter 3 adds questions about restoration, development and coordination where relevant; it does not require every example to possess those capabilities or share one generative law.

### Four separate adequacy claims

1. **Descriptive consistency:** identities, relationships, meanings and temporal context fit together coherently.
2. **Execution correctness:** a calculation follows the specified mechanisms and numerical semantics.
3. **Empirical adequacy:** observations support the model under its claimed conditions.
4. **Decision adequacy:** outcome coverage, accuracy and uncertainty suit the decision.

This document defines the integrated architecture and prospective assessments. It does not establish the latter three claims for a real-world instance. It also does not establish a universally complete ontology, a universal law of self-organization, an optimal hierarchy or an implemented intelligence.

The consolidated baseline now represents systems whose conditional behavior emerges from organization and mechanisms, while allowing those mechanisms to be maintained, damaged, repaired and reorganized across interacting levels. The same model retains how we know those things and where our explanation remains incomplete.


## 13. Retained core integration contracts

These contracts originated in audit revision 0.3.1 and remain part of the four-chapter baseline. The core remains nine representation families. The following retained contracts resolve omissions or ambiguities found during the earlier review of 73 then-in-scope book pages and reviewing the chapter assessments, integrated specification and master diagram. They are modeling deductions from those foundations, not additional laws prescribed by Meadows.

### 13.1 Observation, prediction and scenario separation

A model trajectory can generate derived events, samples and patterns. These remain predictions or analytic consequences. The same record must not become external evidence merely by being retained, summarized or passed through another model. A prediction becomes assessable against an observation only through a separately identified observation/report and an explicit correspondence.

Record the referent/variable correspondence, quantity interpretation or conversion, temporal interval, aggregation and applicable conditions when comparing prediction with observation. Direct inspection can support structure without first inferring it from a behavior history. Conflicting or uncertain source observations remain distinguishable from competing model explanations.

Each scenario has its own state, history, organizational configuration, assumed drivers and result identity. Shared definitions and source observations can be referenced without duplicating evidence. A hypothetical action must not overwrite the accepted account of actual conditions or another scenario's pending effects. An intervention is recorded as actual only when there is evidence that it occurred; outcome claims require their own support.

### 13.2 Structural transitions must preserve state meaning

Allowing G to change is insufficient for an executable evolving model. Every consequential transition must declare:

1. Which referents persist, which constituents/relationships change, and when the change takes effect.
2. How affected stock values, constituent conditions, retained information, queues and pending commitments correspond before and after it.
3. Where material or other accounted quantities go when a holder, process or boundary changes; loss, conversion or exchange requires its own declared meaning. Informational quantities need not obey material conservation.
4. Which mechanism and parameter versions govern work already in progress and future work, including delay/filter history.
5. Which histories are preserved and how newly introduced state is initialized, without rewriting prior observations.
6. Which capacities, permissions and applicability assumptions change, and whether the resulting description remains executable.

One possible formalization extends the earlier organizational transition to an explicit mapping:

\[
(x^+,m^+,G^+,\theta^+,\pi^+)=\Psi(x^-,m^-,G^-,\theta^-,\pi^-;e).
\]

Here e is the specified transition occurrence or scenario intervention. Psi may map between differently organized descriptions; it must retain referent/quantity meaning. This is a model-state mapping, not permission to make material appear or disappear instantaneously in the real system. Continuous physical transfer or an event-scale approximation requires its declared accounting and temporal interpretation. Incompatible units or quantities cannot simply be summed when nodes merge.

If the mapping is unknown, retain the observed or hypothetical organizational change and identify where numerical execution becomes unresolved. Do not silently reset stocks, discard in-flight orders, replenish resources or claim recovery. A state-mapping correction in our description remains distinct from a real transition in the system.

### 13.3 References, discrepancies and feasible responses

For a goal-directed response, specify the reference owner, whether it is fixed or computed, the actual or perceived condition used, the comparison rule, and the feasible response. A discrepancy may be a signed quantitative difference, a departure from a range, a deadband predicate or a qualitative mismatch. It need not be a new stock or primitive.

For the common scalar convention e=r-y, r and y must have compatible meanings and units; record the sign and what corrective action it implies. An alternative convention is valid if consistently applied. Test behavior on both sides of the reference, including bounds and the case where ongoing losses require replacement as well as gap correction. Competing mechanisms may have different references.

Use direction-neutral variable identities. A loop correcting above and below a reference does not establish a material interface operating in both directions. Direct physical equilibration may be described by the relevant physical difference without inventing a sensing actor or conscious goal.

### 13.4 Gross exchange, net change and intervention alternatives

Retain gross inflows and outflows, their net balance and the accumulated stock separately. Zero net change can mean no exchange or substantial balanced exchange. Those arrangements can differ in resource dependence, effects at connected stocks and response to disruption.

When changing a stock is the objective, compare feasible changes to inflow, outflow and both where relevant. A lower depreciation or attrition rate can change accumulation without a higher inflow. Equal stock effects do not imply equal cost, beneficiaries, wider effects or attainable timing. These checks make explicit the Chapter 1 obligations already implicit in the stock/flow families.

### 13.5 Source, sink and renewal closure

For a consequential material or energy process, identify modeled inputs, outputs, transformations, accumulated waste and omitted exchanges. A boundary cloud is an assumption about scope, not an unlimited supply or disposal capacity. State whether a constraint is internally represented, treated as a declared external condition, or unresolved over the chosen horizon.

Distinguish finite stock drawdown, self-dependent regeneration and externally supplied replenishment. Renewal depends on its actual mechanism and supporting conditions. A sink with limited removal can accumulate a harmful quantity even while the productive stock looks healthy. Waste-absorption limits use the appropriate accumulation/removal direction; a resource analogy does not transfer units or calibrated parameters.

Distinguish physical remaining resource, physically attainable extraction, economic viability and renewable recovery. Moving to another source requires an identified added source and its dependencies; it does not create unlimited regional or global supply. Near depleted states, preserve unknown regeneration thresholds and recovery assumptions instead of automatically resetting a resource to health.

### 13.6 Typed composition and conditional decomposition

Part-of, participates-in, coordinates, supplies, informs and authorizes remain different relations. Overlapping social participation does not imply circular physical containment. Impose any domain-appropriate containment restrictions on that relation, rather than banning cycles from causal feedback or forcing all memberships into a single tree.

An aggregate stock can represent a total over components only with a declared correspondence and compatible quantities. Do not add an aggregate to its own constituents as if they were independent resources. Shared capacities and commitments remain shared across overlapping views.

To examine a subsystem in isolation, declare the interface conditions, duration and local functions being assessed. Recomposition must preserve the significant interactions and constraints. Stable subassemblies may preserve progress under interruption, but neither that fable nor dense local coupling guarantees that an isolated subsystem is self-sufficient.

### 13.7 Cross-domain pattern instantiation

A reusable pattern is a scoped model template, not a new universal kind of physical system. An instantiation needs:

- The source pattern and target domain, with a correspondence between roles and actual referents.
- Stock, flow, information, response, purpose and boundary roles; different appearances may support corresponding roles.
- Compatible governing relationships, units, time scales, parameter meanings and applicable domains.
- Initial conditions, relevant histories and omitted dependencies.
- The extent of the proposed analogy: topology, qualitative behavior or quantitatively equivalent dynamics.
- Domain-specific evidence and alternatives; parameters or causal claims are not transferred merely because diagrams resemble each other.

Population and capital can share a proportional growth/loss pattern under corresponding assumptions. A delayed inventory model is not dynamically equivalent to a delay-free model merely because the same foreground stock appears. A resemblance can remain a candidate explanation while its mechanism correspondence is unresolved.

## 14. Pattern allocation and model-development comparisons

This table checks that the full chapter range can be expressed by the integrated architecture, including examples not instantiated as a complete numerical model here. These are analytical specifications and proposed comparisons, not executed simulations or claims of exact figure reproduction.

| Pattern or example | Roles and mechanism correspondence | Comparison or limit to examine | Detailed parent checks |
| --- | --- | --- | --- |
| Bathtub, reservoir and linked forest/mill stocks | Accumulation, multiple flows, shared transfer, source/sink scope. | Balanced nonzero exchange versus inactivity; inflow versus outflow interventions; transfer conversions. | C1-R06–C1-R10; I7-T02/I7-T15. |
| Savings and proportional growth/decline | Stock S, net proportional rate r under declared constant-rate assumptions; dot S=rS. | Growth, decline and r=0; approximate doubling time only in its applicable proportional-growth regime. The rule of 70 is an approximation, not a universal reinforcing-loop law. | B32–B33; Z11–Z14. |
| Coffee equilibration and thermostat | Thermal condition, heat-transfer mechanisms, physical differences, reference and finite heating capacity where applicable. | Above/below reference; heating alone, cooling alone, combined response, ongoing loss and capacity breakdown. A physical quantitative model needs energy/heat-capacity conversion or declared normalized rates. | C2-T01–C2-T05. |
| Population and capital | Population births/deaths correspond conditionally to capital investment/depreciation, with explicit role and rule correspondence. | Per-capita versus total rates; service lifetime versus loss flow; changed driver schedules; no topology-only parameter transfer. For the simple rules dot P=(b-d)P and dot K=(alpha f-1/L)K, units and assumptions determine whether analogy is valid. | C2-T06–C2-T09; I7-T13. |
| Inventory with delays | Physical inventory, actual/perceived sales, computed reference, discrepancy, replacement and gap correction, order/delivery history. | One demand step can initiate repeated internally generated cycles; compare perception, corrective intensity and delivery delay separately. | C2-T10–C2-T15; section 8. |
| Nonrenewable resource and capital | Remaining resource R, productive capital K, extraction H, profit, investment and depreciation. | Dot R=-H over the chosen horizon; yield/cost change with resource state; operation can stop while R remains positive. Reserve/current-use ratio is not a dynamic lifetime forecast under growth. | C2-T16–C2-T20. |
| Renewable resource and capital | Dot R=g(R,conditions)-H for self-regeneration, or a separately defined external replenishment process; coupled capital and profitability. | Nonlinear total/per-capita regeneration meanings, yield and price; overshoot/adjustment, oscillation, collapse and conditional recovery. A technology improvement can change scarcity feedback without creating resource. | C2-T21–C2-T24/C2-T30. |
| Source and sink constraints | Resource supply or pollutant accumulation with finite removal/absorption. | Opposite accounting direction with explicit meaning, units and conditions; local substitution versus wider limits. | C2-T20/C2-T25/C2-T27; I7-T16. |
| Restoration and repair | Functional mechanisms, damage, alternatives, repair processes, supporting resources and timing. | Hidden capacity loss, shared dependencies, repair failure and withdrawal of compensation; dynamic functioning allowed. | C3-T01–C3-T12. |
| Self-organization and stable hierarchy | Actual generating processes, restrictions, retention, stable assemblies, local responses and wider coordination. | Real change versus model correction; preserved work under interruption; cross-level causes, suboptimization and excessive control. | C3-T13–C3-T27; I7-T08–I7-T10/I7-T14. |

The mathematical forms above are our simple illustrative formalizations, conditional on the stated relationships. They do not provide calibrated functions or prove universal behavior. The zoo remains a nonexhaustive pattern library; a system may combine patterns or require a different explanation.



## 15. Retained four-chapter retrospective: historical findings and disposition

This review read the current audited Chapters 1–3 specification, its master map and retrospective, and the Chapter 4 assessment. It reused the completed page-level reviews of Chapters 1–3 (73 pages) and Chapter 4 (25 pages), plus the Chapter 4 source-note check. Thus the source coverage is 98 body pages: printed 11–72 and 75–110. This is not a claim that all 98 pages or their image pixels were freshly reread in this particular integration pass.

The prior documents covered the main foundations, but a four-chapter integration pass could not be issued while Chapter 4 remained a separate proposal. The review identified these integration obligations:

| Finding | Risk or incomplete contract | Correction and allocation |
| --- | --- | --- |
| A4-01 — Incomplete cumulative integration | The current master specification and map covered Chapters 1–3; the Chapter 4 report explicitly remained a first extension. Presence of both documents did not establish their integration. | This cumulative version incorporates Chapter 4 into the shared families, master map, requirements, scenarios and coverage allocation. The earlier scoped documents remain historical inputs. |
| A4-02 — Intended choice versus realized feasibility | A modeled actor choosing from the actual globally feasible set could receive information it has not sensed. A policy might appear competent because hidden impossibilities were removed for it. | Section 16 separates actor-perceived options and intended action from realized execution under actual modeled constraints. Unknown global constraints do not silently improve choice. I7-R15; I7-T17–I7-T19. |
| A4-03 — Closure when a boundary changes | Expanding a view can retain an old independent input while also explaining it internally, count a shared stock twice, or compare outputs with incompatible meanings. | Section 18 specifies input ownership, replacement of boundary assumptions, shared referents and correspondence between views. I7-R17; I7-T23–I7-T24. |
| A4-04 — Observation can be an information intervention | A new visible meter or feedback channel can change behavior. Treating it as a passive data source could change the mechanism while attributing the result to an unchanged system. | Section 19 distinguishes passive records, proposed information changes and changes actually included in an examined system. Intervention timing, recipients, effects and evidence remain explicit. I7-R20; I7-T20/I7-T28. |

These are representation and integration corrections, not observed runtime failures. The source does not prescribe these formal contracts; they are deductions needed to represent its examples coherently. Earlier corrections remain: observation/prediction separation, explicit discrepancy, state/history carry-over, qualified analogy, gross/net accounting, source/sink closure and typed composition.

The review also retained four important qualifications rather than adding unnecessary primitives: a fixed nonlinear rule can change local sensitivity without a new topology; several constraints may bind; role context does not determine every individual’s behavior; and a reported association does not establish a causal effect. No additional core family was needed.

## 16. Actor perspective, information and intended action

An actor is a constituent with relevant internal processes, not a compulsory feature of every physical feedback mechanism. Where an actor matters, describe identity and role, information channels, internal condition/memory, attributed goals, incentives, pressures, known permissions, perceived options, decision rule and the process translating intent into effect. Every claim can be observed, reported, inferred, assumed or unresolved.

Keep these meanings separate:

| Description | Meaning |
| --- | --- |
| Analyst’s candidate system state | State in the examined model; knowing it in a simulation does not establish knowledge of the real state. |
| Actor channel availability | What a channel could expose, to whom and when. |
| Received or attended information | What actually reaches or is used by the actor according to evidence or the scenario. Availability alone does not establish attention. |
| Actor belief and perceived constraints | The actor’s modeled interpretation, estimates and assumed possibilities; these may be incomplete or mistaken. |
| Intended action | Choice or attempted response generated from the actor’s modeled internal condition and context. |
| Realized effect | What the world mechanisms actually allow or produce under the candidate’s physical and institutional constraints. |

For example, a dealer may intend to order from an apparently available supplier; the supplier may reject the order because capacity is unavailable. Removing that supplier from the actor’s perceived options before any modeled notice would leak hidden capacity information. Conversely, fatigue, injury or another physical condition can affect an actor’s decision process without deliberate awareness if that influence is explicitly part of the model. The contract prohibits unexplained oracle access, not legitimate physical influence.

One proposed formalization is:

\[
\hat z_i(t^+)=U_i(\hat z_i(t^-),\mathcal I_i(t);\eta_i),
\]

\[
a_i^{\mathrm{intent}}(t)=\pi_i\big(\hat z_i(t),g_i,c_i,\widehat{\mathcal A}_i(t)\big),
\]

\[
f(t)=F\big(x,m,u,a^{\mathrm{intent}};G,\theta,\text{actual modeled constraints}\big).
\]

I denotes information delivered through declared channels by the relevant time; eta describes the proposed attention/memory/interpretation process; A-hat is the actor’s perceived or known choice set. Internal states can include explicit non-informational influences. Intended action and realized process are separate. U, pi and F remain particular candidate mechanisms, not universal learning algorithms or psychological laws.

Record whether an actor is assumed to optimize, satisfice, follow a rule, retain a routine or use an unresolved decision mechanism. A satisficing model needs its proposed sufficiently acceptable conditions and stopping/revision behavior; it is not a label that supplies an algorithm. Source-era role examples do not license stereotypes or known private motives.

Forecasts available to an actor require their own source, issue/availability time, interpretation and error status. A later outcome or analyst-only scenario must not become an earlier actor input. Other actors’ plans and future choices can remain unknown. The same internal condition, information, perceived options and policy should not yield a better-informed intention merely because a hidden global variable changes, unless a specified influence or stochastic difference accounts for it.

## 17. Nonlinear applicability, constraints and delayed effects

Each relevant response retains its joint inputs, quantity meanings, rule/curve or unresolved explanation, parameters, domains, limits, history, timing and source support. Distinguish the following possible explanations of changed behavior:

1. A different operating point under the same nonlinear function.
2. A changed parameter, capacity or reference.
3. A changed policy or functional mechanism.
4. A changed organization or interface.
5. Different driver/history assumptions or an observational difference.

A changed curve shape or apparent regime does not uniquely select one of these. Compare rival explanations rather than automatically rewriting the graph. Saturation, thresholds and reversal are represented where supported; they are not presumed in every relationship. A local approximation needs an applicability range. Unknown thresholds do not become precise values simply to run a scenario.

Joint constraints distinguish inventory amounts, available supply rates, conversion requirements, productive capacity, skill/maintenance condition, removal/absorption, economic viability, permissions and actors’ perceptions of these. Their units and governing processes matter. Do not treat a resource stock as a supply rate without a declared extraction/dispatch mechanism.

Where a fixed-complement process is a justified candidate, q <= min(b-k/a-k) can bound production: b-k is input availability per time and a-k the required input per produced unit. Equality requires additional assumptions. This is not a universal model of substitution, quality or human organization. Several constraints can bind, and some inputs may be omitted or unknown.

Constraint change should be traced to existing state/process relationships. Production can consume material or removal capacity and contribute to training, maintenance or investment through specified mechanisms. A changing “limiting factor” is an assessment of those relationships, not another physical force or permission to count capacity twice.

Relieving or relocating a constraint does not establish perpetual physical growth in a finite supporting environment. A chosen policy bound, a physical feasibility limit and an actor’s belief about either remain different descriptions. Record unknown requirements and side effects rather than treating the current factor list as exhaustive.

A delay description records stage, meaning, duration/range, history, controllability and relevant timescale. Distinguish availability, perception, decision, response intensity, shipment, maturation, construction and effect manifestation. Foresight compares conditional schedules and existing commitments. Faster information does not complete construction, and faster correction can interact badly with other delays. The chapter’s multiply-by-three heuristic remains an assumption, not a calibration law. Short events can matter to a long inquiry if they cross a threshold; slow processes can matter to a short inquiry through its initial condition.

## 18. Question-specific boundaries and comparison between views

An expandable shared representation can support many related inquiries. For each view, retain the subject/question, horizon/resolution, included referents, external variables, source/sink assumptions, omissions and rationale, relevant exchanges and conditions requiring review. Scope is not determined solely by academic, political or organizational jurisdiction.

When expanding a view:

- Identify shared referents and quantities; do not create a second physical inventory, commitment or capacity merely because another subsystem becomes visible.
- State which formerly external input is now internally explained and by which mechanism. Remove or condition the old independent driver at that variable’s interface; do not add both as separate contributions unless they genuinely are distinct inputs.
- Preserve initial state and pending history, or declare missing correspondence. Boundary revision alone is not evidence that the actual system changed organization.
- Define transfers, conversions and multiple effects across the new interfaces. Recycling does not automatically return all discarded mass or recreate its original quality.

When reducing a view, replace omitted consequential influences with a declared closure, conditional input schedule or unresolved status. Simplification does not make omitted dynamics disappear. A missing closure may prevent quantitative prediction while leaving a useful qualitative comparison.

To compare narrow and wide views, define a correspondence for referent, variable meaning, units, aggregation and time window. Compare like quantities or explicitly project/aggregate them. A disagreement due to measuring different variables is not proof that one mechanism is wrong. Neither larger graph size nor smaller computational cost alone determines adequacy; assess effects on explanation, uncertainty and stakeholder conclusions.

## 19. Observation, feedback interventions and evidence independence

Passive retrieval of an existing record need not change the system. A visible display, disclosure, new measurement procedure, sampling action or altered communication channel may change what actors perceive or what processes occur. State which case is being modeled rather than assuming all observation is passive or all observation is an intervention.

For a consequential information intervention, retain proposed versus included/applied status, channel and recipients, start time, changed availability/visibility/interpretation assumptions, feasible subsequent responses and any direct physical effects. A proposed scenario changes only that scenario’s description. Actual adoption and outcomes require their own evidence.

Compare a hidden logger with an actor-visible display under otherwise declared comparable conditions. Their effect on records may be similar while their effect on actor behavior differs. If no recipient attends or can act, more recorded data need not change the outcome.

Actual reports, inferred mechanisms, assumed private states and predicted results retain separate status. Two summaries of the same observation are not two independent confirmations. Multiple cited sources may share data; independence or dependence must not be invented from citation count. Model output passed through another model remains model-derived unless independently observed.

The meter story remains a reported association with a proposed mediator chain and unresolved selection, load/configuration and recording alternatives. Its source note identifies an oral account at a 1973 conference. The reported one-third contrast is not installed as a causal parameter. The budworm account retains its compiled-source provenance and model-based explanation; neither story’s equations or causal findings are independently replicated here.

## 20. Worked integration across all four chapters

The inventory candidate in section 8 remains a declared model with a guaranteed-delivery baseline and a separate disruption extension. Chapter 4 adds four linked questions:

1. **Whose information drives ordering?** The dealer may receive sales/inventory reports but not a supplier’s true capacity or another dealer’s pending plans. Record the dealer’s estimates, perceived options, intended orders and actual dispatch acceptance separately.
2. **What lies behind the input and output clouds?** Revealing production, raw materials, consumer stocks or discard changes the analytical view. If demand is now explained from consumer conditions, it must not also remain an unrelated independent input at the same variable without an explicit reconciliation.
3. **Which limits and operating ranges matter?** Supplier capacity, transport, skills, administration, demand and removal may bind differently. A different mode can follow from the same conditional rules as state and relative response effects change.
4. **Does new information change the mechanism?** A visibility or sharing intervention can change the dealer’s perceived conditions or policy response. Its scenario timing and effects are explicit; installing a display does not directly create stock or repair transport.

The full path is therefore: organized participants and shared stocks → conditional processes and retained history → information available to particular actors → interpreted conditions and intended choices → realized effects under shared constraints → local and wider histories → comparison with independent observations and criteria. Repair and real organizational development can alter the mechanisms along that path; analyst revision changes the description. These relations operate together, not as a mandatory one-pass pipeline.

Two additional source cases check breadth:

- **Budworm:** host and insect stocks, natural-control limits, climate histories, management information and incentives, multiple intervention effects, succession and ecological/economic criteria fit the same core. Unknown response curves remain unknown; the story’s conclusion is not hardcoded into a simulator.
- **Meter visibility:** a channel’s exposure may affect attention, perceived use/cost, feasible action and later power use. The analyst can possess measurements unavailable to the household. Selection/configuration rivals remain represented, and cumulative energy accounting does not by itself specify household behavior.

These are specified reasoning paths and prospective comparisons, not numerical or empirical test results.

## 21. Retained Chapters 1–4 coverage and audit record

The four source assessments allocate 36 B, 42 Z, 32 F and 48 U foundation entries. All 158 have a destination below. These identifiers are our analytical catalogue, not an enumeration by Meadows or a mathematical proof of completeness. Chapter 4’s 16 parent requirements are also allocated to the cumulative requirements. Existing detailed chapter test catalogues remain references; their presence is not a runtime pass.

The audit preserves the source qualifications already recorded: the inventory averaging discrepancy, thermal units, conditional analogy, context-dependent loop influence, variable regeneration and recovery, resilience versus constancy, uncertain organizational generators, partial hierarchy decomposition, statistical-fit limits, fixed nonlinear rules versus structural change, realistic boundaries, delay heuristics and the evidential limits of historical stories.

Historical role-play and Stanford prison references and broad biological, economic or social examples are not treated as independently validated causal findings or calibration data. Neither a whole-system model nor better information guarantees that stakeholder criteria can all be satisfied.

**Retained v0.4 conceptual verdict (superseded for the cumulative scope by section 28.6):** after the integration corrections, suitable as the working Chapters 1–4 baseline. No unallocated foundation was found at the resolution of the reviewed catalogue and source assessments, and no tenth core representation family was needed. This is a review judgment with explicit scope, not an assertion that every future system or scientific mechanism is represented completely.

**Validation boundary:** document consistency, reference allocation and graph relationships can be checked here. Full numerical models, empirical predictions, actor psychology, causal identification, runtime speed, token consumption, availability and scalability are not qualified by those checks. All integrated scenarios remain planned. Exact figure geometry and numerical source-curve reproduction are not claimed.

The source ledger consists of Chapter 1 pp. 11–34 (24), Chapter 2 pp. 35–72 (38), Chapter 3 pp. 75–85 (11) and Chapter 4 pp. 86–110 (25). The first three chapters’ source review and audit were retained rather than falsely described as a new rereading. The new review focuses on their composition with the current Chapter 4 specification.


### 21.1 Foundation-to-architecture crosswalk

Section numbers below refer to this cumulative document. The prior audit’s historical finding codes are not reused as current empirical claims.

#### Chapter 1

| Foundation | Printed pages | Integrated sections |
| --- | --- | --- |
| B01 — System rather than collection | 11–13 | 4.1 |
| B02 — Physical and intangible elements | 12–13, 18 | 4.2 |
| B03 — Nested composition | 11–13, 15 | 4.1, 7, 13.6 |
| B04 — Collective and adaptive properties | 12 | 6.2–6.4 |
| B05 — Interconnection families | 11, 13–14 | 4.4–4.6, 7 |
| B06 — Unequal observability | 12–14 | 5.1 |
| B07 — Function and purpose | 11, 14–15 | 4.7 |
| B08 — Purpose inferred from operation | 14–15 | 4.7, 5.1 |
| B09 — Multiple and conflicting purposes | 15–16 | 4.7, 6.4 |
| B10 — Identity through replacement | 16 | 5.3 |
| B11 — Different targets of change | 16–17 | 9, 13.2 |
| B12 — Stocks | 17–18 | 4.3 |
| B13 — Stock as historical memory | 18 | 5.2 |
| B14 — Flows | 18–19 | 4.4 |
| B15 — Sources, sinks and scope | 18, 22 | 4.1, 13.5 |
| B16 — Multiple flows and coupled stocks | 18–19 | 4.4, 7 |
| B17 — Balance and accumulation | 20–22 | 6.1 |
| B18 — Dynamic equilibrium | 20–22 | 13.4 |
| B19 — Alternative ways to change a stock | 22 | 13.4 |
| B20 — Inertia and finite change | 17, 23 | 5.2, 6.1 |
| B21 — Buffering and flow decoupling | 23–24 | 4.3, 8 |
| B22 — Behavior-over-time description | 19–22 | 4.9 |
| B23 — Stock regulation and information | 14, 24–26 | 4.5–4.6 |
| B24 — Closed feedback path | 25–27 | 4.8 |
| B25 — Open chains are permitted | 27 | 4.8 |
| B26 — Distinct diagram meanings | 18, 26 | 7 |
| B27 — Reference, discrepancy and response | 26–29 | 13.3 |
| B28 — Balancing feedback | 27–30 | 4.8, 13.3 |
| B29 — Direction-neutral variable names | 28–29 | 13.3 |
| B30 — Hidden or omitted stock dependencies | 27–28 | 13.5 |
| B31 — Feedback failure and feasibility | 30 | 6.2, 7 |
| B32 — Reinforcing feedback | 30–33 | 4.8 |
| B33 — Compounding and time horizon | 31–33 | 14 |
| B34 — Reverse influence inquiry | 33–34 | 7 |
| B35 — Multiple and joint dependencies | 34 | 4.6, 4.8 |
| B36 — Conditional behavior repertoire | 20–22, 28–34 | 9, 14 |

#### Chapter 2

| Foundation | Printed pages | Integrated sections |
| --- | --- | --- |
| Z01 — Simplified pattern library | 35 | 14 |
| Z02 — Composed feedback | 36–42 | 4.8 |
| Z03 — Competing reference conditions | 36–38 | 13.3 |
| Z04 — Isolate before combining | 36–38 | 14 |
| Z05 — State-dependent loss | 37–38 | 4.6, 14 |
| Z06 — Continuing replacement requirement | 38–40 | 13.3 |
| Z07 — Reference versus attained state | 38–40 | 4.7 |
| Z08 — Feedback acts prospectively | 39 | 7, 13.1 |
| Z09 — Capacity and breakdown | 40–41 | 6.1 |
| Z10 — Time-varying dominance | 40–42, 44–45 | 4.8 |
| Z11 — Proportional growth and loss | 42–45 | 14 |
| Z12 — Changing relative rates | 44–47 | 4.6, 9 |
| Z13 — Conditional behavior repertoire | 45–47 | 4.9, 9 |
| Z14 — Assumptions are not observations | 42–48 | 5.1, 13.1 |
| Z15 — Three model-value questions | 45–48 | 9 |
| Z16 — Revisable exogenous boundary | 48 | 4.1, 9 |
| Z17 — Conditional structural analogy | 48–51 | 13.7 |
| Z18 — Lifetime and replacement | 49–50 | 4.2, 14 |
| Z19 — Coupled population and economy | 50–51 | 7, 14 |
| Z20 — Derived target | 51–53 | 8.1 |
| Z21 — Actual versus perceived rate | 52–55 | 5.2, 8.1 |
| Z22 — Three delay meanings | 52–54 | 5.2 |
| Z23 — Pipeline and hidden temporal state | 53–54 | 8.1, 13.2 |
| Z24 — Endogenous oscillation after a step | 52–55 | 8.6 |
| Z25 — Relative delays and corrective intensity | 55–57 | 8.6 |
| Z26 — Actor policy revision | 55–57 | 9, 13.2 |
| Z27 — Cross-system delay propagation | 58 | 7 |
| Z28 — Sources and sinks bound growth | 58–60 | 13.5 |
| Z29 — Coupled productive and resource stocks | 60–62 | 14 |
| Z30 — Physical remaining versus economically accessible | 61–62 | 14 |
| Z31 — Reserve-to-current-use is not a lifetime forecast | 61–64 | 14 |
| Z32 — Growth goals and stakeholder horizons | 63–64 | 4.7 |
| Z33 — Price and technology feedback | 64–66 | 14 |
| Z34 — Local versus wider limits | 65–66 | 13.5 |
| Z35 — Stock-limited versus renewal-flow-limited | 66–72 | 14 |
| Z36 — Different replenishment mechanisms | 66 | 14 |
| Z37 — Density-dependent regeneration | 66–67 | 14 |
| Z38 — Several nonlinear relationships interact | 67 | 4.6, 14 |
| Z39 — Overshoot and three outcomes | 68–72 | 14 |
| Z40 — Efficiency can weaken corrective feedback | 69–71 | 14 |
| Z41 — Recovery is conditional | 71 | 14 |
| Z42 — Threshold and feedback-speed interaction | 71–72 | 14 |

#### Chapter 3

| Foundation | Printed pages | Integrated sections |
| --- | --- | --- |
| F01 — Functioning is conditional | 75 | 4.1 |
| F02 — Preserve poorly understood contributors | 75 | 4.2 |
| F03 — Persistence in a variable environment | 76 | 6.2 |
| F04 — Multiple restorative feedback mechanisms | 76 | 4.8 |
| F05 — Different response times | 76 | 5.2 |
| F06 — Redundancy and substitution | 76 | 6.2 |
| F07 — Repair of restorative organization | 76 | 6.2 |
| F08 — Creation of new restorative organization | 76 | 6.3 |
| F09 — Resilience permits dynamic regimes | 77 | 4.1 |
| F10 — Current constancy can conceal fragility | 77–78 | 4.9 |
| F11 — Tradeoffs with productivity and immediate stability | 77–78 | 4.7 |
| F12 — Support the system’s own restorative capacity | 78 | 6.2 |
| F13 — Organization can be produced internally | 79 | 6.3, 13.2 |
| F14 — Heterogeneity and diversity | 79–80 | 6.3 |
| F15 — Freedom and experimentation | 80 | 6.3–6.4 |
| F16 — Suppression for short-term control | 79–80 | 6.4 |
| F17 — Simple rules can generate complex form | 80 | 6.3 |
| F18 — No established universal simple-rule explanation | 81 | 6.3, 12 |
| F19 — New structures create prediction limits | 80–81 | 9, 13.2 |
| F20 — Systems within systems | 82 | 13.6 |
| F21 — Local regulation with wider coordination | 82 | 6.4 |
| F22 — Stable intermediate assemblies | 82–83 | 4.2, 14 |
| F23 — Unequal coupling strengths | 83 | 6.4 |
| F24 — Information economy | 83 | 4.5 |
| F25 — Partial decomposability | 83 | 6.4 |
| F26 — Cross-level causes remain important | 83–84 | 4.1, 7 |
| F27 — Coupling changes over time | 84 | 5.3, 9 |
| F28 — New coordination can emerge | 84 | 6.3–6.4 |
| F29 — Coordination has a supporting role | 84–85 | 4.7, 6.4 |
| F30 — Suboptimization | 84–85 | 4.7, 6.4 |
| F31 — Excessive central control | 85 | 6.4, 7 |
| F32 — Coordination–autonomy balance | 85 | 6.4 |

#### Chapter 4

| Foundation | Printed pages | Integrated sections | Cumulative requirement allocation |
| --- | --- | --- | --- |
| U01 — Our descriptions, equations, databases and mental pictures are models rather than the world itself. | 86 | 5.1, 9, 15, 21 | I7-R11, I7-R12 |
| U02 — Models can be useful and congruent with experience while remaining incomplete. | 86–87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 |
| U03 — Reasoning can fail through inaccurate assumptions or invalid conclusions from otherwise accurate assumptions. | 87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 |
| U04 — Better systems understanding reduces some surprises without eliminating surprise. | 87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 |
| U05 — Events are occurrences at particular times and places, often the most visible system outputs. | 88 | 4.9, 9, 20 | I7-R11, I7-R12 |
| U06 — Behavior includes growth, stagnation, decline, oscillation, randomness and evolution; changing variability matters too. | 88 | 4.9, 9, 20 | I7-R11, I7-R12 |
| U07 — Interlocking stocks, flows and feedback make behaviors possible under different conditions. | 89 | 4.9, 9, 20 | I7-R11, I7-R12 |
| U08 — Systems inquiry moves repeatedly between behavior histories and candidate structure. | 89 | 4.9, 9, 20 | I7-R11, I7-R12 |
| U09 — Event-to-event explanations can miss the mechanisms generating repeated behavior. | 89 | 4.9, 9, 20 | I7-R11, I7-R12 |
| U10 — Past flow correlations may cease to hold after underlying structure or operating conditions change. | 90 | 4.6, 9, 17 | I7-R12, I7-R16 |
| U11 — Effects need not scale in proportion to a larger input or intervention. | 91 | 4.6, 17 | I7-R16 |
| U12 — Thresholds, saturation, weak-response ranges and reversals occur in the examples. | 91–92 | 4.6, 17 | I7-R16 |
| U13 — Nonlinearities alter relative loop effects and can change the resulting behavior mode. | 92, 94 | 4.6, 17 | I7-R16 |
| U14 — A weather episode can trigger an outbreak whose susceptibility developed over decades. | 93 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16 |
| U15 — Natural-control responses can reach capacity while the process being controlled continues increasing. | 94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16 |
| U16 — Host depletion, population decline and forest succession can form a long ecological cycle. | 93–94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16 |
| U17 — An intervention can suppress the target and simultaneously weaken control mechanisms or preserve susceptible conditions. | 94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16 |
| U18 — Ecological persistence and steady industrial supply can be different criteria. | 93–94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16 |
| U19 — Analytical boundaries divide a more interconnected reality. | 95 | 4.1, 4.4, 13.5, 18 | I7-R02, I7-R04, I7-R09, I7-R17 |
| U20 — Effects called secondary or unintended are still effects of the system. | 95 | 4.1, 4.4, 13.5, 18 | I7-R02, I7-R04, I7-R09, I7-R17 |
| U21 — Source/sink clouds hide potentially consequential stocks and processes. | 95–96 | 4.1, 4.4, 13.5, 18 | I7-R02, I7-R04, I7-R09, I7-R17 |
| U22 — Production, consumption, discard and recycling connect stocks, with employment, income and waste among the wider effects. | 96 | 4.1, 4.4, 13.5, 18 | I7-R02, I7-R04, I7-R09, I7-R17 |
| U23 — Appropriate boundary depends on the question, user and time horizon. | 96–97 | 4.1, 18 | I7-R17 |
| U24 — A birth/death view can omit consequential migration or disposal constraints. | 97 | 4.1, 18 | I7-R17 |
| U25 — Infrastructure, settlement and demand can respond to an intervention; effects cross geographic and institutional lines. | 97–98 | 4.1, 18 | I7-R17 |
| U26 — Excessively large models can obscure the answer with unnecessary detail. | 98 | 4.1, 18 | I7-R17 |
| U27 — Familiar boundaries can become rigid and should be reconsidered for a new problem. | 98–99 | 4.1, 18 | I7-R17 |
| U28 — Many inputs jointly produce many outputs, supported by wider social and ecological conditions. | 100–101 | 4.6, 17 | I7-R18 |
| U29 — An essential scarce input may limit functioning despite abundance elsewhere. | 101 | 4.6, 17 | I7-R18 |
| U30 — The identified factor set can be incomplete; adding an input can affect other supporting processes. | 101 | 4.6, 17 | I7-R18 |
| U31 — Relieving one bottleneck can move the constraint to production, skills or administrative capacity. | 102 | 6.1, 17 | I7-R18 |
| U32 — Growth changes the supporting environment and relative scarcity; the system and its limits coevolve. | 102 | 6.1, 17 | I7-R18 |
| U33 — Physical growth faces bounds; limits can be chosen or encountered through system response. | 102–103 | 6.1, 17 | I7-R18 |
| U34 — Perception, shipping, processing, maturation, construction and stock turnover have temporal effects. | 103–104 | 5.2, 17 | I7-R03, I7-R19 |
| U35 — Estimated duration is often too optimistic; the chapter offers an informal correction heuristic. | 103 | 5.2, 17 | I7-R03, I7-R19 |
| U36 — Delay relevance depends on the behavior timescale being investigated. | 104 | 5.2, 17 | I7-R03, I7-R19 |
| U37 — Delayed action can miss a target, while reacting too rapidly can amplify short-term variation. | 104–105 | 5.2, 17 | I7-R19 |
| U38 — Long lead times and effects not yet visible create a need for foresight. | 105 | 5.2, 17 | I7-R19 |
| U39 — Actors have incomplete, delayed and local information, including uncertainty about others’ actions. | 106 | 4.5, 16 | I7-R15 |
| U40 — Satisficing means seeking a sufficiently acceptable choice rather than an omniscient optimum. | 106 | 4.6, 16 | I7-R15 |
| U41 — Interpretation can be selective, affected by recency, risk perception, future discounting or prior mental models. | 107 | 4.6, 16 | I7-R15 |
| U42 — Roles bring particular information, incentives, goals, pressures and constraints. | 107–108 | 4.7, 6.4, 16 | I7-R05, I7-R10, I7-R15 |
| U43 — Locally reasonable choices can combine into unwanted wider outcomes. | 106–108 | 4.7, 6.4, 16 | I7-R05, I7-R10, I7-R15 |
| U44 — Replacing an individual may leave role-induced mechanisms substantially unchanged. | 108, 110 | 4.7, 6.4, 16 | I7-R05, I7-R10, I7-R15 |
| U45 — A wider perspective can reveal opportunities to redesign information and incentives. | 108 | 4.7, 6.4, 16 | I7-R05, I7-R10, I7-R15 |
| U46 — The electric-meter story links visible feedback with reported differences in use. | 109 | 7, 16, 19 | I7-R11, I7-R20 |
| U47 — Useful feedback must reach an appropriate recipient at a useful time and support an effective response. | 109 | 7, 16, 19 | I7-R11, I7-R20 |
| U48 — Whether local behavior supports wider functioning depends on information, incentives, goals, stresses and constraints. | 109–110 | 4.7, 9, 20 | I7-R05, I7-R10, I7-R12 |

### 21.2 Chapter 4 parent-requirement allocation

| Parent | Cumulative requirements |
| --- | --- |
| C4-R01 | I7-R11, I7-R12 |
| C4-R02 | I7-R11, I7-R12 |
| C4-R03 | I7-R12, I7-R16 |
| C4-R04 | I7-R16 |
| C4-R05 | I7-R06, I7-R07, I7-R12, I7-R16 |
| C4-R06 | I7-R02, I7-R04, I7-R09, I7-R17 |
| C4-R07 | I7-R17 |
| C4-R08 | I7-R18 |
| C4-R09 | I7-R18 |
| C4-R10 | I7-R03, I7-R19 |
| C4-R11 | I7-R19 |
| C4-R12 | I7-R15 |
| C4-R13 | I7-R15 |
| C4-R14 | I7-R05, I7-R10, I7-R15 |
| C4-R15 | I7-R11, I7-R20 |
| C4-R16 | I7-R05, I7-R10, I7-R12 |


## 22. Complete foundation catalogue

### 22.1 General foundations

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F01 | 111 | Nonlinearity, uncertain boundaries and other sources of surprise are common system properties | Preserve them where relevant; do not make linearity a prerequisite for representation |
| C5-F02 | 111–112 | Archetypes are recurring structures producing recognizable problematic patterns | Store patterns as conditional structural hypotheses, with several possible manifestations |
| C5-F03 | 112 | Blame, stronger pressure and marginal adjustment can leave the generating structure intact | Distinguish actor replacement or parameter increase from changing the causal organization |
| C5-F04 | 112 | Goals and feedback can be changed to avoid or escape traps | Represent proposed structural changes and their conditions, rather than storing only a recommended action name |

### 22.2 Policy resistance

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F05 | 112–113 | Persistent undesirable behavior can be maintained by balancing responses | A stable aggregate can conceal intense opposing activity |
| C5-F06 | 113 | Actors monitor relevant conditions against their own goals | Each actor needs its own information, reference, discrepancy and response |
| C5-F07 | 113 | Inconsistent subsystem goals can create counteracting efforts over shared conditions | Represent the shared affected state and the distinct influence paths |
| C5-F08 | 113–114 | More effort can provoke counter-effort and create a costly ratchet | Track effort, costs and response timing as well as the visible stock |
| C5-F09 | 114–115 | Overpowering resistance or removing ineffective pressure has different consequences | Assess continuing coercive capacity and withdrawal responses; do not assume either succeeds automatically |
| C5-F10 | 115–116 | Understanding constraints and finding broader compatible goals can redirect energy; harmony is not assured | Preserve stakeholder differences and unresolved conflicts even when exploring a shared purpose |

### 22.3 Tragedy of the commons

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F11 | 116–117 | The illustrated commons is limited, shared and erodable under excessive use | Distinguish a shared resource from the additional conditions needed for this trap |
| C5-F12 | 117–118 | Resource loss can reduce regeneration or accelerate further destruction | Represent nonlinear erosion and possible recovery limits explicitly |
| C5-F13 | 117–119 | Individual gains and collectively distributed costs weaken incentives to restrain use | Record benefit and burden incidence, not just total extraction |
| C5-F14 | 117–118 | Missing or delayed feedback permits user growth or use to outstrip support | Connect resource information to actual decision capability and timing |
| C5-F15 | 118 | Shared sinks can be overused as well as resource sources | Model pollutant loading, assimilation or remaining sink capacity with appropriate accounting |
| C5-F16 | 119 | Education, privatization and regulation act through different mechanisms | Compare changes in information, incidence, access and enforcement separately |
| C5-F17 | 119–120 | Some resources cannot feasibly be divided into private units | Record divisibility, spillovers and institutional feasibility rather than assuming privatization is always available |
| C5-F18 | 119–121 | Regulation depends on knowledge, interpretation, authority, enforcement and public purpose | Give governing actors bounded information and finite capacity; recognition of a limit does not itself enforce one |

### 22.4 Drift to low performance

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F19 | 122 | The initial regulation structure compares performance with a desired state | Keep the ordinary balancing loop visible |
| C5-F20 | 122 | Selective perception and memory can give bad performance disproportionate weight | Distinguish actual history, perceived history and the selection process |
| C5-F21 | 122 | A desired standard can fall with perceived performance | A reference may be an endogenous state or computed variable, rather than a fixed constant |
| C5-F22 | 122–123 | Lower standards reduce discrepancy and corrective effort, creating a reinforcing decline | Reduced error can reflect aspiration loss rather than improvement |
| C5-F23 | 123 | Fixed standards or learning from better achieved performance can interrupt or reverse drift | Make the reference-update rule an intervention target and examine feasibility |

### 22.5 Escalation

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F24 | 124 | Actors seek to surpass each other's perceived states | Link each reference to the perceived rival, not only to its own past state |
| C5-F25 | 124–125 | Reciprocal response closes a reinforcing loop | Record the complete cross-actor return path and perception effects |
| C5-F26 | 125 | Escalation can involve falling prices or rising noise, costs, arms or other variables | Define comparison direction; escalation does not mean every raw variable increases |
| C5-F27 | 124–125 | Competition can accelerate desirable achievement while also producing excess and wider costs | Assess benefit, burden and limits separately from loop polarity |
| C5-F28 | 125–126 | Reinforcing escalation can rapidly reach extremes and eventually encounter limits or collapse | Represent applicable response laws and constraints rather than forcing an endless exponential |
| C5-F29 | 125–126 | Refusal to compete or negotiated balancing mechanisms can interrupt the process | Test rival response, short-term exposure, agreement and implementation capacity |

### 22.6 Success to the successful

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F30 | 126–127 | Winning can confer resources, privileges or information that improve future competitive ability | Link current reward to future opportunity and performance |
| C5-F31 | 127 | A small or contingent advantage can compound, including from initially equal conditions | Preserve initial conditions and chance separately from intrinsic capability |
| C5-F32 | 127–129 | In a constrained shared environment, increasing appropriation can exclude others | Represent resource coupling, entry, survival and alternative opportunities |
| C5-F33 | 128–129 | Wealth, credit, education, land and opportunity can reinforce one another | Link distinct domains without collapsing their different units or mechanisms |
| C5-F34 | 129 | Diversification can create an alternative niche, but exclusion can obstruct it | Represent access and resources needed for diversification |
| C5-F35 | 129 | Concentrated power can weaken mechanisms intended to limit concentration | Allow governance rules and enforcement capacity to be influenced by participants |
| C5-F36 | 129–130 | Limits, redistribution, renewed opportunity or differently structured rewards can reduce compounding advantage | Compare allocation rules and their effects on participation, performance and distribution |

### 22.7 Shifting the burden to the intervenor

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F37 | 131–132 | A system already has, or lacks adequate, means of maintaining a desired condition | Represent the original corrective process and the underlying difficulty |
| C5-F38 | 132–133 | An intervention can change the condition, perception or both, without resolving the underlying difficulty | Distinguish actual relief from signal suppression and enduring repair |
| C5-F39 | 132–133 | Intervention effects may lapse, allowing the problem to reappear | Retain duration, repetition and pending effects |
| C5-F40 | 132–133 | Shifting responsibility can intentionally improve the system; an intervenor may be needed | Do not classify all assistance or specialization as addiction |
| C5-F41 | 133–135 | Destruction or neglect of self-maintaining capacity creates a reinforcing dependency loop | Make capacity erosion a mechanism to investigate, not an inference from repeated use alone |
| C5-F42 | 133 | Increasing need can strain the intervenor and reduce the recipient's control | Track both sides' capacities, commitments and vulnerability |
| C5-F43 | 134–135 | Removing an intervention can expose a deteriorated state; recovery has timing and transition costs | Compare capacity restoration and support changes over a sufficient horizon |
| C5-F44 | 134–135 | Ask why correction fails, remove obstacles and strengthen effective mechanisms | Represent repair of feedback and capability as alternatives to taking over the task |

### 22.8 Rule beating

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F45 | 136 | Apparent compliance can evade the intended purpose of a rule | Store formal rule, intended purpose, compliance evidence and outcome separately |
| C5-F46 | 136–137 | Actors adapt around thresholds, categories and allocation procedures | Allow changes in strategy and relevant organization; a fixed actor response can miss the mechanism |
| C5-F47 | 137 | Rules can induce behavior that is otherwise difficult to explain | Compare incentives with and without the rule while retaining plausible alternative explanations |
| C5-F48 | 137 | More rigid rules or enforcement can produce further distortion | Assess adaptation to the revised rule rather than freezing the response after intervention |
| C5-F49 | 137 | Evasion is feedback for revising, explaining or removing a rule and directing creativity toward its purpose | Give rule revision a justification and a causal pathway to a better outcome |

### 22.9 Seeking the wrong goal and sailboat interlude

| ID | Pages | Extracted foundation | Modeling consequence |
| --- | --- | --- | --- |
| C5-F50 | 138 | Goals define what counts as discrepancy, compliance and success | Represent the relationship between purpose, indicator, reference and corrective action |
| C5-F51 | 138–139 | Spending, activity or counted procedures can be mistaken for the outcome sought | Separate effort, throughput, stock, service and welfare claims |
| C5-F52 | 139–140 | An aggregate monetary flow omits important nonmarket, distributional and stock conditions | Do not treat a single aggregate as a complete account of system well-being |
| C5-F53 | 140 | Regular measurement of valued outcomes can redirect feedback toward them | Represent coverage, timing and behavioral consequences of outcome measurement |
| C5-F54 | 140–141 | Wrong-goal compliance differs from rule beating; both can coexist | Evaluate both independently and retain mixed explanations |
| C5-F55 | 141 | Rule-defined competitive categories can redirect design and use | Connect selection rules to accumulated design changes and lost alternative functions |
| C5-F56 | 141 | Extreme optimization for current rules can sacrifice resilience to changed rules or contexts | Examine performance outside the selected regime and the ability to adapt |



## 23. Detailed structural assessment of the eight traps

The following mechanism traces are qualitative causal explanations, not executable equations. Each needs contextual response laws, timing, capacity and evidence before a numerical trajectory can be inferred. A reinforcing path can weaken, saturate or be dominated by another path. A desirable or undesirable outcome is evaluated against attributed criteria; it is not determined by whether a loop is reinforcing or balancing.

### 23.1 Policy Resistance—Fixes that Fail, pp. 112–116

**What the chapter contributes.** A condition can remain nearly unchanged because actors continuously counteract one another. Each uses a bounded view and a goal to determine action. Effective movement toward one actor's goal can increase others' discrepancies and responses. Maintaining the unwanted state may consume considerable effort, and increasing pressure can increase counterpressure. The title here is Meadows' combined heading; this assessment does not silently introduce a separate ninth archetype called fixes that fail.

**Mechanism.** Shared condition changes; actor A perceives a gap from A's reference; A acts; the shared condition moves; actor B perceives a larger gap from B's different reference; B acts in another direction; the resulting condition prompts renewed action by A. The local loops can each be balancing while their interaction generates resistance and costly persistence. A policy-resistant state need not minimize total cost or satisfy any participant.

**Representation needed.** Specify the affected stock or state vector; each actor's perception, goals, constraints, response intensity and delay; which physical or institutional processes actually change the condition; and who pays for the effort. Different goals may concern different variables connected through the same system. Do not subtract unconverted quantities, such as money and safety, to create one universal discrepancy.

**Illustrations and their limits.** The chapter uses drug policy and contrasting population policies in Romania, Hungary and Sweden. In the latter accounts, coercion, material constraints and broader child welfare objectives lead to different responses. These demonstrate how an analyst might widen the explanation; they do not prove that one policy alone caused each historical result. The Hungary discussion explicitly notes that housing was only one constraint. Historical details remain attributed to the source and its references.

**Opportunity.** Examine whether ineffective pressure can be relaxed, whether participants' constraints can be addressed and whether a broader goal can be negotiated. The chapter acknowledges that goals cannot always be harmonized. A shared goal requires an actual agreement or change in incentives and authority; writing one into the analyst's model does not make actors adopt it.

**Questions before use.** Is the apparent resistance an active countermove or simply inertia, a delay, an unmodeled constraint or a weak intervention? Does each actor have the information attributed to it? Can one withdraw without unacceptable exposure? Will the proposed agreement retain support when conditions change? Continue to measure costs and stakeholder outcomes even if the focal stock barely moves.

### 23.2 The Tragedy of the Commons, pp. 116–121

**What the chapter contributes.** Shared use becomes troublesome in this archetype when private benefit is strong, damage is shared, corrective feedback is absent or slow, and use can exceed the support of a limited, erodable resource. A shared resource alone is insufficient evidence of a tragedy. The text also applies the analysis to shared sinks, where disposal benefits one party while others bear accumulating costs.

**Mechanism.** Users increase use or their number; aggregate removal exceeds regeneration; resource condition falls; beyond relevant conditions regeneration weakens or erosion increases; deterioration accelerates. Weak feedback to individual users fails to restrain the process in time. For a sink, loading can exceed assimilation, impair conditions and reduce future capacity. Source depletion and sink loading need different accounting signs.

**Representation needed.** Represent resource quantity, regenerative processes and ecological condition where distinct; access rights and users; desired and realized use; user benefits and external burdens; information delay; alternative livelihoods or substitutes; governance and enforcement. If soil condition has a slower history than grass biomass, it can require a separate stock. Do not create an extra stock merely because the word capacity appears: use a derived variable if it has no independent memory.

**Opportunity.** The chapter distinguishes education, privatization and regulation. Education changes understanding and social response; privatization attempts to bring benefits and costs to the same decision maker; regulation changes allowed access or its consequences. Monitoring, correct interpretation, authority, enforcement and the regulator's orientation to the community matter. Some resources cannot practically be divided into private units.

**Critical qualification.** These are the book's proposed families of response, not an exhaustive theorem about governance. Its discussion includes historical and politically charged analogies; those do not establish that a population or group is inherently a resource burden, or that every shared institution has the same ecology. Its ranking of governance options should remain a source claim. A model must test the actual institutions, spillovers, time horizons and possible cooperation. A private owner can face short horizons, incomplete information or off-site effects, so ownership must not be coded as automatic conservation.

**Questions before use.** Is the limit physical, regenerative, organizational or assumed? Are users independent, cooperating or governed already? Is damage erodable and reversible? Does information arrive before critical loss, and can users afford to respond? Does a restriction shift extraction or pollution beyond the chosen boundary? A quota without enforcement or viable alternatives may not change realized use.

### 23.3 Drift to Low Performance, pp. 121–123

**What the chapter contributes.** A reference can erode with perceived performance. Negative selection of experience reinforces the process: bad results become the expectation, good results are dismissed, and standards fall. A system may report a smaller gap while its actual performance deteriorates.

**Mechanism.** Performance falls or is perceived to fall; remembered or selected experience lowers the standard; the lower standard reduces corrective discrepancy; less effort supports performance; subsequent performance worsens. This reinforcing path can dominate the balancing loop that originally maintained the standard. Gradual change can obscure how far performance has moved from earlier conditions.

**Representation needed.** Keep actual performance history, perceived performance, remembered evidence, desired standard and corrective action distinct. Store how the reference is updated and who can change it. Give actual and perceived values a common meaning or an explicit conversion. A formal standard can remain fixed while an informal expectation drifts, so they should not automatically be the same variable.

**Opportunity.** Meadows suggests maintaining absolute standards or drawing standards from better actual performance. These alter the reference-update mechanism. The better-performance strategy uses the same capacity for reinforcing change in another direction; it does not demonstrate that improvement can continue without limits.

**Critical qualification.** The frog story is explicitly uncertain in the source and is not used here as biological evidence. A falling target is not necessarily pathological: capacity, safety constraints or a legitimate change in purpose can make revision reasonable. Best-ever results may be noisy, unrepeatable or achieved at hidden cost. Fixing an impossible standard may consume resources without restoring performance.

**Questions before use.** Did performance change, did measurement change, or did the standard change? Which memories are retained? Is the chosen reference feasible under current resources? What distinguishes adaptive revision from normalization of failure? Test these rival explanations before calling a declining series goal erosion.

### 23.4 Escalation, pp. 124–126

**What the chapter contributes.** The reference for one actor depends on surpassing the perceived state of another, who responds in the same way. Relative comparison makes the actors part of a cross-system reinforcing loop. Hostility and arms are examples, but the text also discusses price wars, advertising, conversation loudness and ostensibly beneficial competition.

**Mechanism.** A changes its state to get ahead; B observes or overestimates A; B raises its own competitive reference and acts; A observes B and increases its response. In a price war the raw prices may fall, so the comparison variable or desired direction must be defined explicitly. A one-sided increase is not evidence of this reciprocal loop.

**Representation needed.** Store each actor's actual condition, perceived rival condition, comparison criterion, margin or response rule, delay, implementation capacity, costs and relevant limits. Relative targets may be asymmetric. Some competitive acts are flows, not accumulated stocks; identify what accumulates rather than forcing every example into two stock boxes.

**Opportunity.** Avoid entering the loop; stop participating where feasible; or establish negotiated balancing controls. Unilateral reduction can expose an actor to short-term disadvantage, a qualification the chapter states. Negotiated controls require credible observation, authority or agreement, and capacity to sustain compliance.

**Critical qualification.** The chapter describes escalation as exponential. For our model, exact exponential growth is a hypothesis requiring compatible response laws, gains and time conditions. Loop polarity alone does not establish that functional form. Saturation, budgets, time delays, exhaustion or third parties can produce other behavior. Even competition toward an apparently good outcome can impose excessive wider costs.

**Questions before use.** Do actors actually use rival-relative references? Is perceived threat exaggerated? Does a common external disturbance explain both increases instead? Can de-escalation survive an asymmetric response? Would a negotiated cap redirect competition toward a less observable dimension?

### 23.5 Success to the Successful—Competitive Exclusion, pp. 126–130

**What the chapter contributes.** Success can change the means of succeeding next time. Income, assets, education, access and information are not just outcomes; they can become inputs to subsequent competition. The Monopoly and Christmas-light examples show how an initially small or contingent lead may compound. In constrained environments the process can deprive competitors of what they need to remain active.

**Mechanism.** Present advantage improves performance or allocation; reward increases resources or privileged access; these improve future competitive ability; future reward grows. A second path can reduce what remains for other participants, weakening their future ability. Equality of initial rules does not guarantee equal realized trajectories.

**Representation needed.** Store resource pools, allocation rules, participant capabilities, productivity differences, performance indicators, rewards and the mechanism converting rewards into future opportunity. Distinguish money, land, skill and information rather than adding them into one ungrounded advantage score. Include entry, exit, borrowing, inherited state and alternative niches when relevant. Random early results should remain distinguishable from measured capability.

**Opportunity.** The chapter discusses diversification, caps on concentration, renewed or equalized opportunity, redistribution and rewards that do not bias the next competition. A reset in a game is structurally simple; resetting real inherited conditions can involve costs, institutions and conflicting interests. Diversification needs access and resources. The text notes that dominant actors may block or acquire emerging alternatives, and that concentrated power can weaken antitrust administration.

**Critical qualification.** The chapter's strong competitive-exclusion and monopoly statements describe the mechanism under restrictive conditions. Do not encode inevitable monopoly or extinction for every competitive system. Resource heterogeneity, spatial variation, entry, innovation, cooperation, changing conditions and countervailing rules can alter the outcome. Market concentration alone does not identify this feedback, and a productive participant is not necessarily advantaged solely by prior reward.

**Questions before use.** Which reward actually improves subsequent chances? Is the environment constrained in the relevant way? What other causes explain performance differences? Does the proposed balancing policy survive influence by its beneficiaries or opponents? Evaluate total service, distribution and continued participation separately.

### 23.6 Shifting the Burden to the Intervenor—Addiction, pp. 131–135

**What the chapter contributes.** Outside intervention can relieve a symptom or alter its perception while leaving the underlying problem. Repetition becomes a destructive dependency loop when the original system's corrective capacity is actively damaged or neglected, increasing the need for intervention. The chapter explicitly says that shifting a burden can be beneficial and some systems need an intervenor.

**Mechanism.** A gap prompts external assistance; assistance improves the measured condition or suppresses the signal; less need is perceived or original correction is displaced; original capacity deteriorates; the underlying difficulty persists or worsens; more assistance is needed. If capacity does not erode, this particular destructive return path is absent, even if assistance is repeatedly used.

**Representation needed.** Identify the underlying condition, perceived condition, desired condition, original response process, its capacity, the intervention, the intervention's duration and actual effects, and any capacity damage or maintenance foregone. Represent recipient and intervenor separately. Record external support capacity, cost, dependency and alternatives. A perceived benefit is not the same quantity as repair of physical conditions.

**Opportunity.** Ask why original correction fails; remove obstacles; strengthen effective mechanisms. The chapter proposes rebuilding capability and addressing the underlying condition, with transition timing that avoids unnecessary disruption. Intervention may support restoration rather than displace it. Some beneficial specialization should remain supported rather than forced back into a supposed self-sufficient state.

**Critical qualification.** This is an abstract architecture analysis. The chapter's drug, medicine, vaccination and immunity examples are not independently verified clinical claims or instructions for withdrawing treatment. Its numerical efficacy language is not imported as a model parameter. The principle we retain is to investigate actual effects on capability and vulnerability, including beneficial protective interventions. A conceptual model does not determine an individual's medical or withdrawal decisions.

**Questions before use.** What evidence shows atrophy rather than greater underlying need? Is the intervention suppressing information, improving reality, or both? Is ongoing specialization efficient and dependable? Can capacity actually recover, on what timescale, and with what resources? What happens if support stops before recovery, or the intervenor reaches a limit?

### 23.7 Rule Beating, pp. 136–137

**What the chapter contributes.** A formal rule can induce adaptive behavior that appears compliant while defeating its purpose. The chapter's examples include end-of-year spending induced by next-year budget rules, threshold-sensitive land subdivision and substitution around a restricted product category. The relevant mechanism is adaptation to the rule, not the mere fact that an outcome is disappointing.

**Mechanism.** A rule defines categories, thresholds or rewards; actors perceive the consequences; they select or develop a strategy that improves their local position under the formal rule; recorded compliance looks acceptable while the underlying purpose is frustrated. Stricter rules can elicit further adaptation and distortion. A rule is part of the environment to which actors respond.

**Representation needed.** Keep rule text or formal condition, scope, issuer, version, effective dates, purpose, actor interpretation, response, compliance assessment and wider result distinct. Represent authority and permissions for changes. Inferred intent requires evidence; do not assign conscious deception to an actor merely because the result resembles avoidance. Adaptive behavior can also occur without deliberate rule evasion.

**Opportunity.** Treat avoidance as diagnostic feedback. Reconsider whether to revise, remove or explain the rule; investigate whether incentives and flexibility can direct adaptive capacity toward the purpose. The model should allow a response to the revised rule rather than preserving the old strategy indefinitely.

**Questions before use.** Was the actor compliant, noncompliant or only apparently compliant? Was the rule understood? Is the purpose itself contested? Would this behavior occur without the rule? Does a threshold shift change the mechanism or merely move the clustering point? Is enforcement addressing actual harm, or inducing a more costly form of avoidance?

### 23.8 Seeking the Wrong Goal, pp. 138–141

**What the chapter contributes.** An actor or organization can obey a goal faithfully and still produce an unwanted result if the indicator is an incomplete or misleading representation of the purpose. The chapter distinguishes effort from outcome and uses spending, counted procedures, test performance and GNP to illustrate measurement choices. A formal target influences discrepancies, action and the definition of success.

**Mechanism.** A purpose is operationalized by an indicator and target; the control or selection process produces more of what is rewarded; the indicator improves while important intended outcomes do not, or are damaged through other paths. Deception is unnecessary. The metric can be measured accurately and still be inadequate for the decision.

**Representation needed.** Give intended outcomes an attributed owner and scope; define indicators, measurement procedures, aggregation, units, exclusions and target values; record the claimed relationship between proxy and outcome, its evidence and domain. Keep effort, purchased activity, service delivered, durable stock and welfare distinct. Some valued outcomes may remain qualitative or incompletely measurable.

**Opportunity.** Define goals and reporting that better reflect the outcomes actually valued. Use several meaningful views where necessary, without assuming a universal welfare score. Changing a metric is an intervention that may alter behavior, not just a passive reporting improvement. A new indicator can itself become an incomplete proxy.

**Critical qualification.** The chapter's discussion of GNP is a critique of its use as a welfare goal, not a complete mathematical replacement for national accounts. Its examples do not establish that all throughput is harmful or every fall in economic activity is desirable. The architecture retains distribution, maintenance, stocks, services and external effects so that these claims can be examined rather than presumed.

**Questions before use.** Does the target measure an input or the intended result? Does correlation survive when the measure becomes a target? Who benefits and who is omitted? Can the actor satisfy the indicator while worsening a separately observed outcome? Rule beating and wrong-goal pursuit must remain independently assessable; the chapter explicitly permits both at once.

### 23.9 The sailboat interlude, p. 141

This interlude is a composition of mechanisms, not a ninth named trap. Racing classifications change incentives; designers specialize to win under those rules; later rule tightening prompts further specialization. The resulting design may perform exceptionally in the selected setting while losing other uses and resilience to a rule change. It connects Chapter 5 to Chapter 3's warning that immediate performance can come at the expense of adaptive capacity.

The representation needs the original and current purposes, rule versions, competitive evaluation, accumulated design changes, operating requirements and performance outside the selected regime. A design change must preserve or explicitly alter its existing state and commitments. A successful specialist is not inherently defective: the loss matters relative to the functions and future conditions stakeholders care about. Whether any actual yacht has the properties described requires evidence beyond this illustrative narrative.



## 24. Minimal mechanism contracts that the extension requires

### 24.1 Shared stock and process accounting

Retain the stock balance:

\[
\dot x_j=\sum_k f_{kj}^{\mathrm{in}}-\sum_l f_{jl}^{\mathrm{out}}.
\]

Transfers shared by actors or archetypes are counted once. Costs are not automatically physical losses from the focal stock. Money flows, energy use, skill learning and ecosystem effects need their own conversions and boundaries. Every quantified rate needs units and a time basis; a qualitative relation may remain qualitative.

For a renewable commons, a useful optional skeleton is:

\[
\dot R=\rho(R,K,\text{conditions})-\sum_i H_i,
\qquad H_i=\mathcal E_i(q_i,R,\text{equipment},\text{access}).
\]

Here R is the resource, K is ecological condition if it has independent dynamics, q is requested use and H is realized extraction. Regeneration and erosion laws are unresolved until specified. A sink can instead require pollutant accumulation, loading and assimilation. Do not subtract pollution from biomass without a declared physical conversion.

### 24.2 Benefit, burden and access correspondence

Represent a relationship from a process to its beneficiaries and burden bearers: recipient, type, amount or qualitative effect, timing, spatial extent, uncertainty and whether the actor perceives or internalizes it. An access right, an expected benefit, a realized gain and an ecological cost are distinct. They need not be reduced to money or added into one total.

This is essential to both commons and competitive advantage. A resource remains one shared stock even if several users describe it differently. Institutional allocation and actual removal must connect to that same referent. Benefits can influence choices through perceived incentives; unknown future damage cannot enter actor decisions by analyst omniscience.

### 24.3 Reference and comparison updates

A standard can be fixed, externally changed, or updated from perceived history. Distinguish these cases. If a changing reference has independent memory, represent its update and initial value. A possible numerical update is a lag toward a history-based reference, but neither a first-order lag nor its duration is mandated by the chapter.

In drift, inspect whether reference changes shrink the gap without better actual performance. In escalation, inspect whether one actor's reference depends on surpassing a rival's perceived condition. A common external driver is a rival explanation to reciprocal escalation. Neither structure requires an invented universal ambition variable.

### 24.4 Reward-to-opportunity conversion

Distinguish performance, recorded success, reward allocation and conversion into future means of competition. If a budget A is shared in one unit, allocations must satisfy its accounting constraint; heterogeneous resources require separate constraints. A cash reward can fund training through an explicit process, but cannot be added directly to a skill stock. A privilege can change permissions without being treated as physical material.

The feedback may run through multiple domains and time horizons. Record depreciation, learning delay, borrowing, entry and governance where relevant. Success need not entail a finite zero-sum competition; exclusion requires additional coupling and limitations.

### 24.5 Intervention and corrective capacity

Distinguish original capacity, ongoing effort, actual condition and external relief. Where capacity accumulates, an optional accounting form is:

\[
\dot C=\text{rebuilding and maintenance}-\text{wear, neglect and damage}.
\]

External support can affect either side of this equation, or neither. Dependency requires an evidenced pathway from support to diminished independent correction or deferred repair, and from that change to future need. Repetition alone supplies no such pathway. Also represent the intervenor's own capacity, resource use and commitments; external intervention is not an unlimited source cloud by default.

### 24.6 Purpose, rule, proxy and observed outcome

The purpose, rule, indicator, adaptive response and actual-outcome relationships are included in the single master map in section 3.

Rule beating asks how responses exploit or work around formal rules while frustrating an attributed purpose. Wrong-goal pursuit asks whether achieving the prescribed result serves that purpose in the first place. These questions are independent and can both apply. Formal compliance, apparent compliance, misunderstanding and actual noncompliance remain separate claims. A disputed purpose remains disputed rather than being resolved by the model's author.

### 24.7 Structural change and state carry-over

Retain the v0.4 transition contract:

\[
(x^+,m^+,G^+,\theta^+,\pi^+)=\Psi(x^-,m^-,G^-,\theta^-,\pi^-;e).
\]

When a rule, reference, access structure, capability or organization changes, identify the change and preserve existing quantities, histories and commitments unless a modeled process changes them. A tax, allocation redesign or new measurement does not erase old wealth, ecological damage, learned expectations or pending deliveries. A change in the analyst's interpretation is not the same event as a change in the world. Unknown carry-over blocks a claimed quantitative comparison until resolved or explicitly bracketed.



### 24.8 Archetype assessment record

| Field group | Minimum content and rationale |
| --- | --- |
| Identity and scope | Assessment ID, model version, actor set, boundary, variables, units or qualitative meanings, time horizon; prevents reuse outside the examined system |
| Proposed pattern | One or more trap candidates, structural conditions and applicability; permits mixed or unresolved diagnoses |
| Mechanism references | Existing stocks, processes, response rules, references and complete feedback paths; the label contributes no additional causal force |
| State and timing | Initial conditions, perception memory, delayed commitments, capacity and reference-update histories where relevant |
| Evidence | Source and location; direct versus reported versus inferred basis; support, contradiction, missing data, dependencies among reports |
| Alternatives | Other mechanisms compatible with the behavior, including non-trap explanations; no compulsory numerical probability |
| Distribution and criteria | Who gains, pays, controls, is exposed or omitted; purpose ownership and unresolved conflicts |
| Opportunity candidates | Exactly which link, rule, reference, allocation or capacity changes; who could adopt and implement it |
| Assessment limits | Unknown response laws, disputed purpose, infeasible change, unmodeled spillover, limited horizon and any execution blocker |
| Qualification status | Candidate, provisionally supported for a specified use, contradicted, or unresolved; retain revision history |

This record is deliberately relational. Detailed raw evidence stays in its existing record. Do not copy an entire subsystem into each trap assessment or attach a compulsory trap field to every observation.



## 25. Chapter 5 interface obligations and modeling practice

### 25.1 Interface contract for each relationship

Each interface needs a source, recipient, content or transferred quantity, meaning and units, direction, timing, condition of operation, capacity, access or authority, evidence and failure modes. Distinguish an actor's observation of a condition from the physical effect of that condition. Assess A-to-B and B-to-A independently: evidence of one does not imply the reverse. Bidirectional interaction consists of identifiable directional relationships; it need not have equal strength or delay.

| Pair or boundary | Forward relationship to examine | Reverse relationship to examine | Important failure or ambiguity |
| --- | --- | --- | --- |
| Actor and shared condition | Action changes processes affecting condition | Condition reaches actor through observation or physical effects | Analyst gives actor inaccessible knowledge; apparent resistance is a delay |
| User and common resource | Extraction or loading affects quantity or condition | Resource condition affects feasible use, benefit or perceived decisions | Actual scarcity constrains execution before user perceives it |
| Actor A and actor B | A's state or action informs B's reference and response | B's response informs A | A common cause is mistaken for mutual escalation |
| Reward and participant | Allocation funds capability, access or opportunity | Performance or influence affects future allocation | Rewards are counted twice or treated as proof of intrinsic merit |
| Intervenor and recipient | Relief, information or repair changes recipient | Need, payment, commitments or resistance affects intervenor | Unlimited external capacity; repeated help is mislabeled addiction |
| Rule issuer and governed actor | Rules change permissions, incentives and reporting | Adaptation, outcomes and political influence reach issuer | No adaptation after redesign; capture is omitted |
| Indicator and purpose | Metric is used as evidence for intended outcome | Revised understanding changes measurement or target | Proxy improvement is treated as welfare by definition |
| Narrow and wider system view | Processes impose effects across boundary | Wider constraints and responses return | Intervention merely exports the problem or duplicates an internalized driver |

This is a checklist of potentially consequential interfaces, not a requirement to connect every entity to every other entity. Record assessed absences and unknown links where they matter to a conclusion. Extend the boundary when a consequential return path is omitted; do not expand it without a question or stop condition.



### 25.2 How to use the architecture without oversimplifying the system

#### 25.2.1 Inquiry sequence

1. **Define the concern and whose criteria matter.** Identify the event or behavior, relevant horizons and affected groups. A stock being stable can be undesirable; a stock changing can be healthy. Preserve disputed purposes.
2. **Separate observation from interpretation.** Assemble histories, actual inspected structure, source reports and missing information. Record when information became available. Do not translate every sentence directly into a causal law.
3. **Construct candidate mechanisms.** Identify accumulations, process rates, decision rules, information, references, constraints and delays. Preserve unknowns. An explanatory narrative without the return paths is not yet an established feedback model.
4. **Assess archetypes conditionally.** Ask which necessary relationships are present, absent or unresolved. Allow several patterns or no current match. Look for a rival explanation that could produce similar behavior.
5. **Trace the wider interfaces.** Follow consequential transfers, incentives, delayed effects and governance responses. Expand the view only where needed to assess the question. Keep the boundary and omitted effects explicit.
6. **Specify an opportunity as a change.** Identify its target mechanism, adopter, permission, resources, timing, implementation process and transition. A better goal or rule in the analyst's notes is only a proposal.
7. **Compare conditional scenarios.** Retain the current configuration, proposed alternatives, adverse responses and uncertainties. Evaluate intended outcomes, burdens, capacity, distribution and resilience over suitable horizons.
8. **Revise when evidence warrants.** Predictions guide questions; new observations can support or contradict the model. An unsupported relationship stays open rather than becoming true through repetition or a persuasive diagram.

#### 25.2.2 Structural composition example

A shared renewable resource may be governed by a rule. One participant's early gains can fund more extraction equipment and influence over the rule. A regulator may respond to depletion with subsidies that suppress the visible hardship while reducing incentives to maintain local capability. A production target can encourage the wrong outcome, and participants may adapt around enforcement categories.

This would be several candidate mechanisms operating on shared referents, not five independent worlds. It is a constructed architecture example, not a claim that all such systems behave this way.

The constructed composition uses the common-resource, reward, governance, support and corrective-capacity paths already connected in the master map. It is an optional hypothesis, not a finding about every resource system.

The words can and may matter: each disputed path needs evidence or an explicit scenario assumption. This diagram does not establish the signs or strength of all composite loops. If relief builds capability, the dependency interpretation can fail. If access is effective, commons erosion may not occur. If gains are not reinvested or access is unconstrained by rivals, competitive exclusion may not follow.


### 25.3 Best practices derived from the chapter

| Practice | Rationale and application |
| --- | --- |
| Diagnose a mechanism before prescribing a remedy | A declining curve could reflect erosion, reference change, lost support, measurement or an external shock |
| Record local logic before judging the whole | Bounded information and roles can explain conduct without assuming stupidity or malice |
| Inspect what changes when a policy works initially | Success can provoke countermoves, change expectations or weaken another control path |
| Inspect who benefits and who bears delayed costs | Aggregate totals can conceal the incentive structure sustaining the problem |
| Track standards and measurement alongside performance | A smaller discrepancy or a better proxy may conceal deterioration |
| Inspect the next round of competition | Rewards can change opportunity, entry and influence rather than merely recognize past achievement |
| Assess original corrective capacity during assistance | Relief and capability restoration are different effects; beneficial support is possible |
| Model adaptation to a new rule | Responses after redesign need not resemble responses before it |
| Compare near-term relief with longer-term capacity | A favorable short run can conceal erosion, dependency, concentration or lost resilience |
| Treat ways out as conditional hypotheses | Adoption, trust, information, enforcement, feasibility and transition resources can determine whether they work |
| Retain non-trap explanations and disputed goals | The archetype catalogue is a tool for inquiry, not a compulsory classification of every system |
| Separate model quality from preferred policy | A technically consistent model can still rest on an unsupported mechanism or omit an important criterion |

These are modeling practices synthesized from the chapter. The book does not provide a software test framework or a complete empirical identification protocol in these pages.



## 26. Retained five-chapter requirement allocation

The first twenty requirements retain their full definitions and parent allocations in section 10. The following ten additions complete I7-R01–I7-R30. Legacy I4-R01–I4-R20 and I4-T01–I4-T28 map one-to-one to I5 identifiers with the same numbers. Chapter 5 parent identifiers remain intact for traceability.

| Requirement | Function | Obligation | Chapter 5 parents | Prospective cases |
| --- | --- | --- | --- | --- |
| I7-R21 | Conditional archetype assessment | Represent structural conditions, evidence, contradiction, missing paths, rivals and several simultaneous candidates; a label cannot establish cause. | C5-R01, C5-R02, C5-R16 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T61, I7-T62, I7-T67, I7-T68 |
| I7-R22 | Incidence and commons governance | Represent private/shared benefits and burdens, erodable resource or sink dynamics, access, user feedback and bounded governance. | C5-R03, C5-R04 | I7-T33, I7-T34, I7-T35, I7-T36 |
| I7-R23 | Endogenous references and relative competition | Separate actual/perceived histories, reference updates, corrective responses and reciprocal rival comparisons; no forced pathological or exponential outcome. | C5-R02, C5-R05, C5-R06 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| I7-R24 | Reward to future opportunity | Represent allocation, conversion, future means, shared constraints, entry, diversification and influence on countervailing rules. | C5-R07, C5-R08 | I7-T45, I7-T46, I7-T47, I7-T48 |
| I7-R25 | Intervention and corrective capacity | Distinguish relief, signal masking, original correction, capacity erosion/rebuilding, beneficial specialization and intervenor limits. | C5-R09, C5-R10 | I7-T49, I7-T50, I7-T51, I7-T52 |
| I7-R26 | Purpose, rule, indicator and outcome | Separate intended outcome, formal target, effort, proxy, compliance and actual consequence, including distribution and nonmarket effects. | C5-R11, C5-R12 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| I7-R27 | Adaptive rule responses | Allow actor strategies and governance to change after rule redesign; purpose, intent, compliance and noncompliance require their own evidence. | C5-R11 | I7-T53, I7-T54, I7-T55, I7-T56 |
| I7-R28 | Qualified opportunities and transitions | Specify target mechanism, adoption, authority, resources, timing, carry-over and adverse or wider responses for each proposed way out. | C5-R15 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| I7-R29 | Specialization and changed regimes | Evaluate selected performance, other relevant functions and adaptation to changed rules or operating conditions without condemning all specialization. | C5-R13 | I7-T65 |
| I7-R30 | Composed traps and shared referents | Preserve one accounting and identity per shared process or resource across patterns, with delayed interfaces and boundary closure. | C5-R14 | I7-T60, I7-T62, I7-T63, I7-T64 |

### 26.1 Chapter 5 parent-to-cumulative mapping

| Parent | Cumulative requirements |
| --- | --- |
| C5-R01 | I7-R21 |
| C5-R02 | I7-R21, I7-R23 |
| C5-R03 | I7-R22 |
| C5-R04 | I7-R22 |
| C5-R05 | I7-R23 |
| C5-R06 | I7-R23 |
| C5-R07 | I7-R24 |
| C5-R08 | I7-R24 |
| C5-R09 | I7-R25 |
| C5-R10 | I7-R25 |
| C5-R11 | I7-R26, I7-R27 |
| C5-R12 | I7-R26 |
| C5-R13 | I7-R29 |
| C5-R14 | I7-R30 |
| C5-R15 | I7-R28 |
| C5-R16 | I7-R21 |


## 27. Prospective modeling and testing scenarios

**Status for every case: PLANNED — NOT RUN. I7-T29–I7-T68 map, in order, to C5-T01–C5-T40. Together with section 11 this is a 68-case prospective catalogue, not 68 test results.** The expected checks below are conditional acceptance criteria for future instantiated models. They are not measured results and do not require the qualitative architecture to manufacture numerical parameters. Quantitative runs will need equations or executable rules, units, initial state, history, external conditions, numerical methods and explicit tolerances. Empirical validation will additionally need independent data and an appropriate causal design.

### 27.1 Policy resistance

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T29 | Apply pressure to a shared condition with two opposed actor references | Any countermove must follow the second actor's available information and response rule; the model need not guarantee full cancellation |
| I7-T30 | Increase opposing effort while the aggregate condition changes little | Report the two efforts and their costs separately; small net change must not erase substantial activity |
| I7-T31 | Compare pressure withdrawal with a negotiated broader goal | Withdrawal retains possible exposure; negotiation changes actual adopted rules only in the relevant scenario and can remain infeasible |
| I7-T32 | Produce apparent nonresponse through a slow process or hard constraint without an opposing actor | Preserve the non-resistance explanation; do not assert policy resistance from the trajectory alone |

### 27.2 Commons

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T33 | Vary use relative to regeneration and ecological erosion conditions | Resource accounting balances; deterioration and recovery depend on the specified laws, without compulsory collapse for shared ownership |
| I7-T34 | Deliver accurate resource information early or late, with or without user ability to respond | Information changes intended behavior only through a specified rule; scarcity can constrain realization before it is perceived |
| I7-T35 | Compare education, divided rights and enforced access limits | Each changes its own mechanism; enforcement, externalities and indivisibility remain visible rather than assuming a universally successful option |
| I7-T36 | Regulate a source while loading rises in a connected sink or neighboring resource | Wider effects remain accounted for; changing the boundary does not duplicate the old external closure |

### 27.3 Drift

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T37 | Hold actual performance history fixed while changing memory selection and reference updating | Show which differences arise from perception and standards; a falling gap cannot by itself establish improved performance |
| I7-T38 | Let a standard respond to selectively remembered poor results | Any downward feedback uses the explicit update and effort paths; reference change must not directly rewrite past performance |
| I7-T39 | Compare fixed and best-achieved standards under noise and limited capacity | Report feasibility, effort and actual outcomes; a higher reference is not guaranteed to yield indefinite improvement |
| I7-T40 | Revise a target legitimately after an external capacity change | Preserve adaptive revision as a rival explanation; a declining standard is not automatically classified as pathological drift |

### 27.4 Escalation

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T41 | Connect reciprocal rival-relative targets, then remove one return path | Any escalation attributed to reciprocity depends on the relevant path; other mechanisms can still produce growth after removal |
| I7-T42 | Compare a price war with rising competitive expenditure | Direction semantics are correct for each variable; decreasing price can coexist with increasing competitive intensity |
| I7-T43 | Vary perception error, delay, response gain, budgets and saturation | Behavior follows instantiated mechanisms and constraints; no unconditional exponential is imposed by the label |
| I7-T44 | Compare unilateral restraint, negotiated limits and a common external threat | Include short-term asymmetric exposure, agreement implementation and the alternative common-cause explanation |

### 27.5 Success to the successful

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T45 | Start with equal opportunities but an explicit early random advantage | Keep chance and capability distinct; any compounding requires the reward-to-future-opportunity path |
| I7-T46 | Break reward conversion or change depreciation while preserving prior success | Future advantage changes only through the specified mechanisms; prior success alone is no extra force |
| I7-T47 | Compare a constrained single niche with entry or an accessible alternative niche | Exclusion is conditional; resource conservation, actual entry costs and alternative access are respected |
| I7-T48 | Add a concentration limit, then allow influence on its enforcement | Governance can constrain concentration or be weakened through an explicit path; neither outcome is predetermined |

### 27.6 Shifting the burden

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T49 | Repeat support that maintains or strengthens original capacity | Do not infer the destructive dependency loop without erosion or a specified displacement of underlying repair |
| I7-T50 | Compare actual relief, signal masking and capacity-eroding assistance | Separate physical outcomes, perceptions and corrective capability; the mechanisms need not yield the same future need |
| I7-T51 | Compare early withdrawal, gradual transition and restored-capacity transition | Preserve state, recovery delay, resource requirements and possible short-term deterioration; support removal is not automatically beneficial |
| I7-T52 | Increase recipient need until intervenor capacity is constrained | Requested and realized support can diverge; the intervenor is finite and repeated need can also arise from a worsening external driver |

### 27.7 Rule beating

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T53 | Reward full budget use before a deadline | If wasteful activity emerges, connect it to the perceived allocation rule; distinguish spending, useful output and inferred intent |
| I7-T54 | Move a regulatory threshold while allowing alternative actor strategies | A shifted threshold can move adaptation; the model must not freeze behavior or equate clustering alone with deliberate evasion |
| I7-T55 | Compare stronger enforcement with a redesigned rule and with rule removal | Evaluate purpose achievement, wider costs and new strategies; more enforcement is not assumed always worse or always better |
| I7-T56 | Hold behavior constant across deliberate avoidance, misunderstanding and actual noncompliance accounts | Preserve the distinct evidence requirements; identical outputs cannot by themselves establish actor intent or compliance status |

### 27.8 Wrong goals

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T57 | Meet a spending or procedure target while a separately represented outcome stagnates | Report target success and outcome failure independently; faithful compliance can coexist with wrong-goal pursuit |
| I7-T58 | Improve an aggregate flow while distribution, maintenance or an environmental stock worsens | Preserve the omitted dimensions; the aggregate cannot define them away |
| I7-T59 | Add outcome reporting that becomes visible to decision makers | Distinguish passive measurement from feedback intervention and model any resulting behavior change |
| I7-T60 | Combine an incomplete target with adaptive avoidance around its rule | Allow both wrong-goal pursuit and rule beating on shared mechanisms, without double-counting actions or effects |

### 27.9 Composition, evidence and transition

| ID | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T61 | Supply the same behavior history to several structurally different candidate models | Keep rival explanations open unless discriminating evidence exists; a visually matching curve cannot settle the mechanism |
| I7-T62 | Compose commons use, reward advantage and policy resistance around one resource | Use common entity and transfer identities; labels add no extra causal terms and do not force each trap to become active |
| I7-T63 | Change allocation or governance after capabilities, damage and commitments have accumulated | Apply state/history carry-over; no instant reset of wealth, ecology, beliefs or pending obligations without an explicit process |
| I7-T64 | Improve a local result while adverse effects return later through another subsystem | Evaluate a sufficient horizon and wider interfaces; extending the view must replace or condition any duplicated external driver |
| I7-T65 | Optimize a design for one racing rule, then alter the rule or require another use | Compare in-regime performance, alternative function and adaptation; the model does not require every specialist to lose resilience |
| I7-T66 | Announce a better goal without adoption, then simulate actual adoption and enforcement | Keep the proposed, announced, adopted and realized changes distinguishable; words alone do not rewrite actor rules |
| I7-T67 | Repeat the same anecdote in multiple summaries, then add a model-generated matching story | Preserve shared provenance; repetition and prediction do not create independent evidence for the mechanism |
| I7-T68 | Leave response functions, welfare criteria or transition mapping unknown | Retain a useful qualitative representation while withholding an unsupported numerical ranking or confident causal verdict |

### 27.10 Test levels and limits

The first level is **representation consistency**: shared identities, correct units, stock balance, explicit information paths, separate actual/perceived values, declared rules and valid state carry-over. The second is **mechanism discrimination**: remove or vary a path and examine whether the claimed explanation still holds under its stated conditions. The third is **behavioral adequacy**: examine several histories and conditions, not a single fitted curve. The fourth is **intervention robustness**: vary delays, capacities, adoption and actor adaptation; inspect wider consequences and alternative criteria. The fifth is **empirical qualification**, requiring observations and causal evidence beyond this book assessment.

These levels should not be conflated. Passing a document check does not establish a mechanism in nature; reproducing a historical curve does not identify a unique structure; a successful simulation does not prove that actors will adopt a proposed policy.



## 28. Retained five-chapter retrospective and integration disposition

This review supersedes the four-chapter verdict in section 21 for the cumulative scope. It uses the current v0.4 architecture and current Chapter 5 source assessment, retaining the completed chapter source reviews rather than claiming a new page-by-page rereading of all 129 body pages. The underlying source scope is Chapter 1 pp. 11–34, Chapter 2 pp. 35–72, Chapter 3 pp. 75–85, Chapter 4 pp. 86–110 and Chapter 5 pp. 111–141. Chapter 5 notes on p. 206 were reviewed in its source assessment. Meadows' concepts are the source; the architecture, records, contracts and tests remain our synthesis.

### 28.1 Findings and repairs

| Finding | Prior gap or ambiguity | Integrated repair | Disposition |
| --- | --- | --- | --- |
| A5-01 | The cumulative document explicitly excluded Chapter 5, although a separate assessment existed | Integrate its 56 foundations, mechanisms, requirements, 40 prospective cases and 31-page ledger into this same cumulative artifact | Repaired conceptually |
| A5-02 | Splitting the displayed architecture obscured interactions among operation, repair, development and inquiry | Use one connected master graph; retain both physical/institutional dependencies and analytical relationships with explicit arrow meanings | Repaired in the representation |
| A5-03 | Generic actor goals did not visibly specify endogenous reference changes and rival-relative targets | Add reference-update relationships and persistent history where needed; distinguish formal standards, perceived performance and reference revision | Repaired conceptually; private-state mechanisms still require evidence |
| A5-04 | Shared limits did not alone explain commons incentives or unequal opportunity | Add benefit/burden incidence, access rules, reward allocation and conversion into future capability or opportunity | Repaired conceptually; no compulsory common utility or advantage score |
| A5-05 | Restoration language could conflate repeated help with destructive dependency | Connect intervention separately to actual conditions, perceived signals, original capacity and intervenor limits; retain capability-building and beneficial specialization alternatives | Repaired conceptually; repeated support alone is insufficient evidence |
| A5-06 | Purpose, target, compliance and actual welfare could be collapsed into one success claim | Explicitly separate intended outcome, formal rule, indicator, compliance, actor strategy and outcome correspondence | Repaired conceptually; contested purposes remain attributed |
| A5-07 | A trap label could be mistaken for a causal explanation or a separate subsystem | Archetypes are conditional analytical views referencing the same mechanisms; allow rival diagnoses, mixed patterns and no current match | Repaired by contract |
| A5-08 | A proposed way out could silently change actor policy, erase history or guarantee a favorable result | Link proposal, adoption, execution, transition mapping, actor adaptation and outcome evidence; evaluate adverse responses and wider effects | Repaired by contract; effectiveness remains untested |
| A5-09 | Four-chapter evolution table merged two columns; definition listed ten questions but referred to nine | Correct table structure, add the fifth-chapter column and extend the definition consistently | Repaired editorially |
| A5-10 | Pairwise interface review could miss indirect feedback through a shared dependency or an omitted system | Add a directed pair review method with explicit absences, unknowns and indirect-return checks; require boundary closure on expansion | Repaired as an assessment method; actual-world completeness cannot be inferred |

### 28.2 Critical questions applied to the integration

**First principles and KISS.** A trap is not a new physical substance. The nine shared families still suffice at the reviewed resolution. Add state only where independent memory is needed; use a relationship or derived value elsewhere. Store evidence once, refer to a shared transfer once, and assess different patterns over the same referents. The master map's additional roles are neither new software services nor extra causal forces.

**Five Whys.** Why did an intervention disappoint? Because some modeled response may counteract it. Why does that response occur? Because of a particular information path, incentive, rule, reference, resource condition or physical mechanism. Why does that relationship exist? Inspect its supporting institution, history, dependencies and evidence. Why does the proposed alternative help? Identify the changed return path and necessary adoption, capacity and timing. Why should we believe that account? Compare rival mechanisms and discriminating observations. Stop where evidence is missing; a fifth answer is not automatically the root cause, and several interacting causes may remain.

**MECE.** Use distinct meanings for event/state/rate/pattern/structure, actual/perceived, purpose/proxy, intent/realization and observation/prediction. Do not force archetypes into mutually exclusive categories: interacting traps are an expected possibility. Coverage concerns necessary distinctions and source allocation, rather than a claim that every possible phenomenon belongs to one and only one trap.

**Requirements flow-down.** Source foundation → representation/function → mechanism/interface contract → cumulative requirement → prospective scenario. Each step can be challenged by evidence. This is traceability, not an assumption that scientific inquiry proceeds once through a fixed waterfall.

**Boundary and temporal challenge.** Trace delayed and cross-level effects through specified interfaces. A larger graph is not automatically a better model. Retain the question, horizon, quantity correspondences and omitted-input closure. A local improvement can export harm or create later dependency; a transient decline can accompany useful recovery. Neither interpretation is hardcoded.

**Sensitivity and causal challenge.** Distinguish a changed operating point, parameter, rule, organization, external driver and observation process. A matching history cannot uniquely identify the mechanism. Vary relevant assumptions and consider omitted variables when an executable model is instantiated. This review has not performed those numerical or empirical sensitivity studies.

### 28.3 Directed interface review method

For n selected components or system views, review n(n−1) possible ordered direct relationships, where that finite component set is useful for the inquiry. This counts review questions, not required links. For each A→B record: included with a typed contract; supported absent under specified conditions; inapplicable at this resolution; or unresolved. Review B→A separately. Evidence of one direction does not establish the reverse. Include indirect paths and common dependencies even where no direct link exists.

For an included relation record participants, content or quantity, units/qualitative meaning, timing and delay, access/authority, capacity, governing mechanism, evidence, failure effects and relevant version. Distinguish material transfers, signals, incentives, permissions, containment and analytical correspondence. Bidirectional interfaces may have unequal delay, strength and authority.

| Critical interface set | Required integration check | Prospective cumulative checks |
| --- | --- | --- |
| Stocks ↔ processes ↔ shared constraints | Coherent units, gross versus net change, joint capacity and single transfer accounting | I7-T02, I7-T04, I7-T15, I7-T16, I7-T33 |
| World condition → delivered information → actor intent → actual execution | No analyst-only or future information enters intent; hidden constraints may change realization | I7-T17, I7-T18, I7-T19, I7-T34 |
| Local systems ↔ coordination and common dependencies | Different directions, partial autonomy, cross-level effects and common-mode failures | I7-T09, I7-T10, I7-T32, I7-T48 |
| Performance/perception ↔ references ↔ corrective effort | Distinguish real improvement, aspiration change and reciprocal comparison | I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T43 |
| User action ↔ common resource/sink ↔ governance | Resource dynamics, incidence, information, enforcement and spillovers remain separate | I7-T33, I7-T34, I7-T35, I7-T36 |
| Reward ↔ future opportunity ↔ performance ↔ governance | Trace actual conversions, finite shared resources, entry and influence on rules | I7-T45, I7-T46, I7-T47, I7-T48 |
| Intervention ↔ original correction ↔ intervenor resources | Do not infer erosion from repetition; include recovery timing and support capacity | I7-T49, I7-T50, I7-T51, I7-T52 |
| Purpose ↔ rule ↔ indicator ↔ adaptation ↔ outcome | Independent claims about intent, compliance and effectiveness; no automatic proxy-to-welfare identity | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| Real structural change ↔ state/history; model revision ↔ evidence | Preserve existing quantities and commitments; scenarios do not overwrite actual observations | I7-T08, I7-T14, I7-T35, I7-T63, I7-T66, I7-T67 |

This method cannot prove that every consequential real-world component has already been identified. Unknown interfaces remain explicit. An unresolved causal return path can restrict the conclusion without preventing useful partial representation.

### 28.4 Eight archetypes: complete mechanism allocation

| Archetype | Required path in the shared model | Important alternative or missing condition | Cumulative requirement and cases |
| --- | --- | --- | --- |
| Policy resistance | Different actor references → responses → shared condition → other actors' perceptions and countermoves | Delay, weak actuation or hard limits can also produce apparent nonresponse; a broader goal is not automatically adopted | I7-R21, I7-R23; I7-T29–I7-T32 |
| Tragedy of the commons | Private gains/shared costs → use → limited erodable resource or sink → weak/late decision feedback | Shared ownership alone is insufficient; existing cooperation or effective access control can prevent the loop | I7-R22; I7-T33–I7-T36 |
| Drift to low performance | Perceived history → lower reference → lower corrective discrepancy/effort → worse performance | Legitimate target revision, changed measurement and infeasible previous standards remain alternatives | I7-R23; I7-T37–I7-T40 |
| Escalation | Rival-relative reference → action → perceived rival state → reciprocal response | Common cause, one-way response, saturation and limits can change the behavior; exact exponential is not guaranteed | I7-R23; I7-T41–I7-T44 |
| Success to the successful | Reward → future capability/access → competitive performance → reward, with relevant shared limits | Entry, diversification, productive differences and non-zero-sum opportunities can alter exclusion | I7-R24; I7-T45–I7-T48 |
| Shifting the burden | Relief/masking → displaced or eroded correction → increased underlying need → further relief | Useful intervention, specialization, capability-building support and exogenous increases in need remain representable | I7-R25; I7-T49–I7-T52 |
| Rule beating | Formal rule → perceived incentive → adaptive strategy → apparent compliance and frustrated purpose | Misunderstanding, noncompliance or other causes need distinct evidence; intent is not inferred from appearance | I7-R26, I7-R27; I7-T53–I7-T56 |
| Seeking the wrong goal | Incomplete target/indicator → faithful response → proxy success without intended outcome | Accurate measurement can still be an inadequate target; can coexist with rule beating | I7-R26; I7-T57–I7-T60 |

The sailboat interlude additionally connects rule-conditioned selection, accumulated specialization, alternative functions and resilience to changed rules: I7-R29 and I7-T65. It is not counted as a ninth named trap.

### 28.5 Continuous five-chapter worked integration

Extend the inventory candidate in section 8 without replacing its existing referents. Suppliers, dealers, users, transport, repair personnel, material stocks and pending deliveries remain the same subjects across all views. Chapter 5 adds candidate mechanisms, each enabled only when specified:

1. Dealers and a central allocator can hold incompatible references for the same limited supply. Their countermoves can create policy resistance, but an unfulfilled order can instead result from ordinary capacity or delay.
2. If users appropriate a shared erodable source or impose waste on a shared sink, record private gains, distributed costs, regeneration/removal and decision feedback. Do not label an ordinary shared warehouse a tragedy without the relevant overuse and erosion mechanism.
3. Service standards can drift with perceived history, or competitive targets can follow rival performance. References need update rules and memory, not merely new target constants chosen by the analyst.
4. Successful dealers may receive allocation priority, investment or information that improves subsequent performance. Track how that advantage is acquired and converted; it is not an intrinsic property inferred from prior success.
5. Emergency supply may restore service while local ordering or repair capacity is maintained, improved or neglected. Repetition alone does not choose among those explanations. Finite support and recovery time matter.
6. A delivery-count target can reward easy shipments while neglecting essential service. A threshold or budget rule can induce adaptive avoidance. Rule beating and wrong-goal pursuit are assessed independently against attributed purposes.
7. A redesign changes particular rules, information, references, allocation or capability. Preserve inventories, damage, beliefs, supplier relationships and commitments. Model adoption and actor responses to the redesign rather than assuming immediate agreement.
8. Compare service, cost, distribution, resource condition, recovery and alternative functions over appropriate horizons. Keep observed histories, candidate explanations and scenario results separate.

This is an integrated conceptual exercise, not a historical finding or executed simulation. It demonstrates how the same core can host compositions without adding a module per story or hardcoding a desired conclusion.

### 28.6 Coverage and qualification verdict

The cumulative source catalogue now has 214 entries: B01–B36, Z01–Z42, F01–F32, U01–U48 and C5-F01–C5-F56. These are our review units, not 214 official primitives from the book. Their scope is 129 requested body pages, including all eight Chapter 5 traps and the sailboat interlude. Source notes and anecdote qualifications are retained. No new independent verification of the underlying historical, ecological, behavioral or clinical claims is asserted.

The cumulative requirements comprise I7-R01–I7-R30. The first 20 preserve the I4 meanings; the next 10 integrate Chapter 5. The cumulative scenario catalogue comprises I7-T01–I7-T68: 28 retained integrated cases plus 40 Chapter 5 cases. Legacy identifiers are explicitly mapped. These scenarios overlap in purpose and are not independent demonstrations. Every case remains **PLANNED — NOT RUN**.

**Retained v0.5 verdict, superseded for cumulative scope by section 39.6: accept as the then-working Chapters 1–5 baseline after the listed repairs.** No unallocated foundation or unresolved contradiction was found at the reviewed catalogue resolution, and no tenth core representation family was necessary. This is a bounded review judgment. It does not establish a universally complete world ontology, a unique causal explanation, or that unknown real-world mechanisms have all been found.

**Validation boundary:** consistency of identifiers, allocation, page scope and graph references can be checked in the document. Executable dynamics, empirical causal adequacy, predictive advantage, policy effectiveness, psychological mechanisms, AI intelligence, latency, energy, token economy, high availability and scalability remain unqualified by those checks. The representation is designed to retain those questions, not to declare them solved.


## 29. Retained five-chapter foundation traceability

This crosswalk contains 214 source-review units, with explicit cumulative requirement and prospective-case allocation. Sections 21 and 22 retain their labels, page references and substantive descriptions; sections 23–28 supply the Chapter 5 integration. A mapped case is an assessment opportunity, not a proof that the source proposition has been empirically confirmed.

| Foundation | Printed pages | Mechanism sections | Cumulative requirements | Prospective cases |
| --- | --- | --- | --- | --- |
| B01 | 11–13 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| B02 | 12–13, 18 | 4.2 | I7-R01 | I7-T01 |
| B03 | 11–13, 15 | 4.1, 7, 13.6 | I7-R01, I7-R09, I7-R17 | I7-T01, I7-T09, I7-T23, I7-T24 |
| B04 | 12 | 6.2–6.4 | I7-R06, I7-R07, I7-R09, I7-R10 | I7-T06, I7-T07, I7-T09, I7-T10 |
| B05 | 11, 13–14 | 4.4–4.6, 7 | I7-R02, I7-R04, I7-R09, I7-R16 | I7-T02, I7-T04, I7-T09, I7-T15, I7-T16, I7-T21 |
| B06 | 12–14 | 5.1 | I7-R11 | I7-T11, I7-T26, I7-T28 |
| B07 | 11, 14–15 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| B08 | 14–15 | 4.7, 5.1 | I7-R05, I7-R11 | I7-T05, I7-T11, I7-T26, I7-T27, I7-T28 |
| B09 | 15–16 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| B10 | 16 | 5.3 | I7-R01, I7-R14 | I7-T01, I7-T14 |
| B11 | 16–17 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| B12 | 17–18 | 4.3 | I7-R02, I7-R03 | I7-T02, I7-T03, I7-T15 |
| B13 | 18 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| B14 | 18–19 | 4.4 | I7-R02, I7-R04 | I7-T02, I7-T04, I7-T15, I7-T16 |
| B15 | 18, 22 | 4.1, 13.5 | I7-R01, I7-R17, I7-R18 | I7-T01, I7-T22, I7-T23, I7-T24 |
| B16 | 18–19 | 4.4, 7 | I7-R02, I7-R04, I7-R09 | I7-T02, I7-T04, I7-T09, I7-T15, I7-T16 |
| B17 | 20–22 | 6.1 | I7-R02, I7-R04, I7-R18 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T22 |
| B18 | 20–22 | 13.4 | I7-R02 | I7-T02, I7-T15 |
| B19 | 22 | 13.4 | I7-R02 | I7-T02, I7-T15 |
| B20 | 17, 23 | 5.2, 6.1 | I7-R02, I7-R03, I7-R04, I7-R18, I7-R19 | I7-T02, I7-T03, I7-T04, I7-T15, I7-T16, I7-T22, I7-T25 |
| B21 | 23–24 | 4.3, 8 | I7-R02, I7-R03, I7-R07 | I7-T02, I7-T03, I7-T07, I7-T15 |
| B22 | 19–22 | 4.9 | I7-R12 | I7-T12, I7-T27, I7-T28 |
| B23 | 14, 24–26 | 4.5–4.6 | I7-R04, I7-R15, I7-R16, I7-R20 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T20, I7-T21 |
| B24 | 25–27 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B25 | 27 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B26 | 18, 26 | 7 | I7-R09 | I7-T09 |
| B27 | 26–29 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| B28 | 27–30 | 4.8, 13.3 | I7-R04, I7-R05, I7-R12 | I7-T04, I7-T05, I7-T12, I7-T16, I7-T27, I7-T28 |
| B29 | 28–29 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| B30 | 27–28 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| B31 | 30 | 6.2, 7 | I7-R06, I7-R07, I7-R09 | I7-T06, I7-T07, I7-T09 |
| B32 | 30–33 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B33 | 31–33 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| B34 | 33–34 | 7 | I7-R09 | I7-T09 |
| B35 | 34 | 4.6, 4.8 | I7-R04, I7-R12, I7-R16 | I7-T04, I7-T12, I7-T16, I7-T21, I7-T27, I7-T28 |
| B36 | 20–22, 28–34 | 9, 14 | I7-R11, I7-R12, I7-R13 | I7-T11, I7-T12, I7-T13, I7-T26, I7-T27, I7-T28 |
| Z01 | 35 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z02 | 36–42 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| Z03 | 36–38 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| Z04 | 36–38 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z05 | 37–38 | 4.6, 14 | I7-R04, I7-R12, I7-R13, I7-R16 | I7-T04, I7-T12, I7-T13, I7-T16, I7-T21, I7-T27, I7-T28 |
| Z06 | 38–40 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| Z07 | 38–40 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| Z08 | 39 | 7, 13.1 | I7-R09, I7-R11 | I7-T09, I7-T11, I7-T26, I7-T28 |
| Z09 | 40–41 | 6.1 | I7-R02, I7-R04, I7-R18 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T22 |
| Z10 | 40–42, 44–45 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| Z11 | 42–45 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z12 | 44–47 | 4.6, 9 | I7-R04, I7-R11, I7-R12, I7-R16 | I7-T04, I7-T11, I7-T12, I7-T16, I7-T21, I7-T26, I7-T27, I7-T28 |
| Z13 | 45–47 | 4.9, 9 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| Z14 | 42–48 | 5.1, 13.1 | I7-R11 | I7-T11, I7-T26, I7-T28 |
| Z15 | 45–48 | 9 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| Z16 | 48 | 4.1, 9 | I7-R01, I7-R11, I7-R12, I7-R17 | I7-T01, I7-T11, I7-T12, I7-T23, I7-T24, I7-T26, I7-T27, I7-T28 |
| Z17 | 48–51 | 13.7 | I7-R13 | I7-T13 |
| Z18 | 49–50 | 4.2, 14 | I7-R01, I7-R12, I7-R13 | I7-T01, I7-T12, I7-T13, I7-T27, I7-T28 |
| Z19 | 50–51 | 7, 14 | I7-R09, I7-R12, I7-R13 | I7-T09, I7-T12, I7-T13, I7-T27, I7-T28 |
| Z20 | 51–53 | 8.1 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z21 | 52–55 | 5.2, 8.1 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z22 | 52–54 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z23 | 53–54 | 8.1, 13.2 | I7-R03, I7-R14, I7-R19 | I7-T03, I7-T14, I7-T25 |
| Z24 | 52–55 | 8.6 | I7-R12, I7-R19 | I7-T12, I7-T25, I7-T27, I7-T28 |
| Z25 | 55–57 | 8.6 | I7-R12, I7-R19 | I7-T12, I7-T25, I7-T27, I7-T28 |
| Z26 | 55–57 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| Z27 | 58 | 7 | I7-R09 | I7-T09 |
| Z28 | 58–60 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| Z29 | 60–62 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z30 | 61–62 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z31 | 61–64 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z32 | 63–64 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| Z33 | 64–66 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z34 | 65–66 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| Z35 | 66–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z36 | 66 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z37 | 66–67 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z38 | 67 | 4.6, 14 | I7-R04, I7-R12, I7-R13, I7-R16 | I7-T04, I7-T12, I7-T13, I7-T16, I7-T21, I7-T27, I7-T28 |
| Z39 | 68–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z40 | 69–71 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z41 | 71 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z42 | 71–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| F01 | 75 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| F02 | 75 | 4.2 | I7-R01 | I7-T01 |
| F03 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F04 | 76 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| F05 | 76 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| F06 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F07 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F08 | 76 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F09 | 77 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| F10 | 77–78 | 4.9 | I7-R12 | I7-T12, I7-T27, I7-T28 |
| F11 | 77–78 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| F12 | 78 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F13 | 79 | 6.3, 13.2 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F14 | 79–80 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F15 | 80 | 6.3–6.4 | I7-R08, I7-R09, I7-R10, I7-R14 | I7-T08, I7-T09, I7-T10, I7-T14 |
| F16 | 79–80 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F17 | 80 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F18 | 81 | 6.3, 12 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F19 | 80–81 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| F20 | 82 | 13.6 | I7-R01, I7-R09 | I7-T01, I7-T09 |
| F21 | 82 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F22 | 82–83 | 4.2, 14 | I7-R01, I7-R12, I7-R13 | I7-T01, I7-T12, I7-T13, I7-T27, I7-T28 |
| F23 | 83 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F24 | 83 | 4.5 | I7-R15, I7-R20 | I7-T17, I7-T18, I7-T19, I7-T20 |
| F25 | 83 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F26 | 83–84 | 4.1, 7 | I7-R01, I7-R09, I7-R17 | I7-T01, I7-T09, I7-T23, I7-T24 |
| F27 | 84 | 5.3, 9 | I7-R01, I7-R11, I7-R12, I7-R14 | I7-T01, I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| F28 | 84 | 6.3–6.4 | I7-R08, I7-R09, I7-R10, I7-R14 | I7-T08, I7-T09, I7-T10, I7-T14 |
| F29 | 84–85 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| F30 | 84–85 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| F31 | 85 | 6.4, 7 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F32 | 85 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| U01 | 86 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U02 | 86–87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U03 | 87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U04 | 87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U05 | 88 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U06 | 88 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U07 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U08 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U09 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U10 | 90 | 4.6, 9, 17 | I7-R04, I7-R11, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T11, I7-T12, I7-T16, I7-T21, I7-T22, I7-T25, I7-T26, I7-T27, I7-T28 |
| U11 | 91 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U12 | 91–92 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U13 | 92, 94 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U14 | 93 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U15 | 94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U16 | 93–94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U17 | 94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U18 | 93–94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U19 | 95 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U20 | 95 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U21 | 95–96 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U22 | 96 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U23 | 96–97 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U24 | 97 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U25 | 97–98 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U26 | 98 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U27 | 98–99 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U28 | 100–101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U29 | 101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U30 | 101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U31 | 102 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U32 | 102 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U33 | 102–103 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U34 | 103–104 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U35 | 103 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U36 | 104 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U37 | 104–105 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U38 | 105 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U39 | 106 | 4.5, 16 | I7-R15, I7-R20 | I7-T17, I7-T18, I7-T19, I7-T20 |
| U40 | 106 | 4.6, 16 | I7-R04, I7-R15, I7-R16 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T21 |
| U41 | 107 | 4.6, 16 | I7-R04, I7-R15, I7-R16 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T21 |
| U42 | 107–108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U43 | 106–108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U44 | 108, 110 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U45 | 108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U46 | 109 | 7, 16, 19 | I7-R09, I7-R15, I7-R20 | I7-T09, I7-T17, I7-T18, I7-T19, I7-T20 |
| U47 | 109 | 7, 16, 19 | I7-R09, I7-R15, I7-R20 | I7-T09, I7-T17, I7-T18, I7-T19, I7-T20 |
| U48 | 109–110 | 4.7, 9, 20 | I7-R05, I7-R11, I7-R12 | I7-T05, I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| C5-F01 | 111 | 22–28 | I7-R21 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F02 | 111–112 | 22–28 | I7-R21, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F03 | 112 | 22–28 | I7-R21 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F04 | 112 | 22–28 | I7-R28, I7-R30 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T60, I7-T62, I7-T63, I7-T64, I7-T66 |
| C5-F05 | 112–113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F06 | 113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F07 | 113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F08 | 113–114 | 22–28 | I7-R21, I7-R23, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F09 | 114–115 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F10 | 115–116 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F11 | 116–117 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F12 | 117–118 | 22–28 | I7-R22, I7-R30 | I7-T33, I7-T34, I7-T35, I7-T36, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F13 | 117–119 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F14 | 117–118 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F15 | 118 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F16 | 119 | 22–28 | I7-R22, I7-R28 | I7-T33, I7-T34, I7-T35, I7-T36, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F17 | 119–120 | 22–28 | I7-R21, I7-R22 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T33, I7-T34, I7-T35, I7-T36, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F18 | 119–121 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F19 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F20 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F21 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F22 | 122–123 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F23 | 123 | 22–28 | I7-R23, I7-R28 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T35, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F24 | 124 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F25 | 124–125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F26 | 125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F27 | 124–125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F28 | 125–126 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F29 | 125–126 | 22–28 | I7-R23, I7-R28 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T35, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F30 | 126–127 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F31 | 127 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F32 | 127–129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F33 | 128–129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F34 | 129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F35 | 129 | 22–28 | I7-R24, I7-R30 | I7-T45, I7-T46, I7-T47, I7-T48, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F36 | 129–130 | 22–28 | I7-R24, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T45, I7-T46, I7-T47, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F37 | 131–132 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F38 | 132–133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F39 | 132–133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F40 | 132–133 | 22–28 | I7-R21, I7-R25 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T49, I7-T50, I7-T51, I7-T52, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F41 | 133–135 | 22–28 | I7-R25, I7-R30 | I7-T49, I7-T50, I7-T51, I7-T52, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F42 | 133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F43 | 134–135 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F44 | 134–135 | 22–28 | I7-R25, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T49, I7-T50, I7-T51, I7-T52, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F45 | 136 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F46 | 136–137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F47 | 137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F48 | 137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F49 | 137 | 22–28 | I7-R26, I7-R27, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T63, I7-T64, I7-T66 |
| C5-F50 | 138 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F51 | 138–139 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F52 | 139–140 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F53 | 140 | 22–28 | I7-R26, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T63, I7-T64, I7-T66 |
| C5-F54 | 140–141 | 22–28 | I7-R21, I7-R26, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F55 | 141 | 22–28 | I7-R29 | I7-T65 |
| C5-F56 | 141 | 22–28 | I7-R28, I7-R29 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T65, I7-T66 |


## 30. Retained Chapter 5 page-by-page source coverage ledger

All page numbers in the first column are printed labels. PDF page number is printed page plus 17. The ledger records the contribution reviewed, not an assertion that every source sentence becomes a separate requirement.

| Printed | PDF | Relevant content and treatment |
| --- | --- | --- |
| 111 | 128 | Distinguishes ubiquitous complexity from recurring troublesome structural configurations; C5-F01–C5-F02 |
| 112 | 129 | Structural rather than blame-based response, opportunities, and opening policy-resistance account; C5-F02–C5-F05 |
| 113 | 130 | Actor goals, discrepancy responses, shared conditions, countermoves and intensification; C5-F06–C5-F08 |
| 114 | 131 | Romania narrative, coercive persistence and possible release of ineffective pressure; C5-F08–C5-F09; historical claims retained as source-reported |
| 115 | 132 | Hungary constraints, broader goal alignment and Sweden account; C5-F10; no single-cause identification assumed |
| 116 | 133 | Limits of goal harmonization, policy summary and opening commons example; C5-F10–C5-F11 |
| 117 | 134 | Erodable resource, weakened regeneration, users, private benefit and missing feedback; C5-F11–C5-F14 |
| 118 | 135 | Overuse sequence, renewable resources and shared pollution sinks; C5-F12–C5-F15 |
| 119 | 136 | Education, privatization and regulation; monitoring, incentives, enforcement and regulator limitations; C5-F16–C5-F18 |
| 120 | 137 | Indivisible resources and several institutional forms for governing access; C5-F17–C5-F18 |
| 121 | 138 | Commons summary, compliance/enforcement and opening drift example; C5-F18–C5-F19 |
| 122 | 139 | Actual versus perceived performance, negative memory, eroding targets and reinforcing decline; C5-F19–C5-F22 |
| 123 | 140 | Gradual normalization, uncertain frog analogy, fixed and better-performance standards; C5-F22–C5-F23 |
| 124 | 141 | Escalation from rival-relative goals and perception; possible desirable competition; C5-F24–C5-F27 |
| 125 | 142 | Price wars and other manifestations, wider costs, rapid growth and opening unilateral reduction; C5-F26–C5-F29 |
| 126 | 143 | Short-term exposure, negotiated balancing limits, escalation summary and next trap opening; C5-F28–C5-F30 |
| 127 | 144 | Reward improves future means of winning; game and contest examples; constrained niche exclusion; C5-F30–C5-F32 |
| 128 | 145 | Capital accumulation and linked education, credit and land mechanisms; C5-F32–C5-F33 |
| 129 | 146 | Opportunity feedbacks, diversification limits, antitrust influence and renewed opportunity; C5-F33–C5-F36 |
| 130 | 147 | Equalizing mechanisms, distribution and reward structures that do not compound the next round; C5-F36 |
| 131 | 148 | Burden-shifting examples and original stock-regulation structure; C5-F37 |
| 132 | 149 | Actual versus perceived relief, expiring interventions and beneficial burden shifting; C5-F38–C5-F40; health examples not adopted as clinical evidence |
| 133 | 150 | Need for some intervenors, original capacity atrophy, dependency, control loss and intervenor strain; C5-F40–C5-F42 |
| 134 | 151 | Pest and oil examples, withdrawal and rebuilding alternatives, capacity-supporting intervention; C5-F43–C5-F44 |
| 135 | 152 | Three diagnostic questions, dependency summary and restore-capability transition; C5-F41–C5-F44 |
| 136 | 153 | Rule beating, apparent compliance and responses to budget, category and threshold rules; C5-F45–C5-F46 |
| 137 | 154 | Purpose versus letter, adaptive distortion, rigid response and rule redesign; C5-F45–C5-F49 |
| 138 | 155 | Goals define success; spending, tests and procedure counts as possible inadequate indicators; C5-F50–C5-F51 |
| 139 | 156 | Effort versus outcome, GNP exclusions, distribution and throughput versus stocks; C5-F51–C5-F52 |
| 140 | 157 | Wider effects of throughput targets, outcome reporting, wrong-goal summary and distinction from rule beating; C5-F52–C5-F54 |
| 141 | 158 | Coexistence of wrong goals and rule beating; sailboat specialization and lost resilience; C5-F54–C5-F56 |

Chapter Five notes on printed p. 206 list references 1–17, including contemporary newspaper accounts, population-policy sources, Hardin, Kozol, Tims, Kennedy and Berry. Those references were identified in the notes, not independently reread or empirically verified here. The body was reviewed as extracted page text; complete rendered-page geometry and numerical reproduction of source figures are not claimed.



## 31. Retained five-chapter scope and document verification

| Chapter | Printed body pages | PDF pages | Body page count | Foundation count |
| --- | --- | --- | --- | --- |
| 1 — The Basics | 11–34 | 28–51 | 24 | 36 |
| 2 — A Brief Visit to the Systems Zoo | 35–72 | 52–89 | 38 | 42 |
| 3 — Why Systems Work So Well | 75–85 | 92–102 | 11 | 32 |
| 4 — Why Systems Surprise Us | 86–110 | 103–127 | 25 | 48 |
| 5 — System Traps and Opportunities | 111–141 | 128–158 | 31 | 56 |
| Total requested body scope | 11–72 and 75–141 | 28–89 and 92–158 | 129 | 214 |

The PDF mapping is printed page plus 17 for these body ranges. Prior chapter assessments and their source qualifications remain the source review trail; this integration pass did not freshly reread all body pages. The page counts exclude intervening unrequested pages and source notes.

Document verification checks identifiers, source allocation, table column consistency, graph node/edge references, connectedness and the absence of a prediction-to-independent-observation path. They are document checks, not model executions. The final review status is in section 28.6.

**Document check result, 20 October 2026:** passed the specified consistency and allocation checks. One master graph contains 67 concepts and 164 named relationships in a single connected component; all 56 concepts and 104 relationships from the prior master map are retained. All 214 foundation entries have cumulative requirement and prospective-case allocations. The 30 requirement and 68 scenario definitions have unique contiguous identifiers. Table columns, graph endpoints, subgraph delimiters, code fences and the retained Chapter 5 page ledger passed their checks. Graph counts describe representation detail, not scientific completeness. No model scenarios were executed.


## 32. Chapter 6 leverage mechanisms and source assessment

The numbers and descending order below are Meadows' presentation. They are useful prompts for looking beyond familiar parameter changes. They are not numerical estimates of impact or mutually exclusive classes.

| Source position | Leverage point | Main target in the shared representation | Necessary qualification |
| --- | --- | --- | --- |
| 12 | Numbers: constants and parameters | Values in response rules, standards, rates and policies | A parameter can be decisive when it changes loop gain, a goal, a threshold crossing or a regime |
| 11 | Buffers relative to their flows | Accumulated reserve, storage capacity, operating stock and supporting processes | More reserve can improve protection while increasing cost or reducing flexibility; capacity is not the same as a filled reserve |
| 10 | Stock-and-flow structures | Physical topology, transfers, bottlenecks, cohorts and durable infrastructure | Influence can be large even when rebuilding is slow, expensive or infeasible |
| 9 | Delays relative to change rates | Stage-specific information, decision, completion and effect histories | Faster is not universally better; some delays cannot be shortened, so change rates may need adjustment |
| 8 | Balancing feedback strength | Sensing, transmission, reference, actuation, capacity and restorative paths | Adequacy is relative to disturbances; idle reserves may be essential under unusual conditions |
| 7 | Reinforcing feedback gain | Self-amplifying response and opportunity relationships | Examine the driving mechanism and limits rather than relying only on stronger counterpressure |
| 6 | Information-flow structure | Who can receive which information, when and in what actionable form | More information can induce a race or be ignored; a new signal is not the same as tuning an existing channel |
| 5 | Rules | Permissions, incentives, sanctions, constraints and authority to change them | Formal adoption, interpretation, enforcement and adaptive responses are distinct |
| 4 | Self-organization | Generating processes, variation, experimentation, selection and retention | New organization needs sources, resources and conditions; novelty is not automatically useful |
| 3 | Goals | Local references, wider purposes and selection criteria | A different announced goal does not prove adoption or implementation; goals can conflict |
| 2 | Paradigms | Actor/community assumptions shaping meaning, purpose, rules and design | Distinguish empirical beliefs, normative commitments and analytical assumptions; avoid one universal cultural frame |
| 1 | Transcending paradigms | Capacity to expose, compare and revise interpretive frames | Our operational interpretation is revisability, not a claim to implement spiritual enlightenment or make all explanations equally valid |

One action can affect several positions. Changing a subsidy changes a number and may change a reinforcing mechanism, access, incentives and information. Changing a rule-writing institution affects more than a rule value. Classify what the action actually changes, with references to the mechanisms, rather than giving every action a single compulsory depth label.



### 32.1 Position 12 — Numbers, pp. 147–149

**Source mechanism.** Parameter adjustments change process magnitudes without necessarily changing the arrangement producing behavior. The chapter discusses taxes, spending, prices, standards and personnel replacements within the same institutional setting. Its critique is directed at attention to familiar adjustments while the broader information, rules and purposes remain intact. It explicitly acknowledges that numbers matter to affected individuals and in the short term.

**Important exception.** Some numerical changes alter higher-level mechanisms: an interest or birth rate changes reinforcing gain; a target changes what a balancing loop attempts to maintain. Near a relevant critical range, the numerical setting can be consequential. Therefore a parameter-change label is not grounds for discarding a candidate intervention.

**Representation.** Identify parameter owner, meaning, units, applicable rule and version, range, physical or institutional adjustability, rate of change, effective date and relevant thresholds. Separate the nominal setting, communicated setting and realized effect. Record uncertainty about the response curve. A proposed value may be unavailable because of physical limits or permissions.

**Development practice.** Compare both direction and magnitude around the actual operating condition; include a baseline and wider outcomes. Ask whether the change alters an ordinary rate, crosses a threshold, changes an actor's reference or affects loop dominance. Do not infer that the same percentage change has the same effect elsewhere.

**Critical qualification.** The rent example challenges the assumption that there must be one uniquely fair value. The architecture should permit acceptable ranges and several criteria, but it cannot derive universal fairness from that story. Similarly, the chapter's broad claims about macroeconomic policies are illustrations of its argument, not current empirical findings or calibrated response laws.

### 32.2 Position 11 — Buffers, pp. 149–150

**Source mechanism.** The stabilizing contribution of a reserve depends on its size relative to consequential flows. Money, inventory, breeding populations and chemical neutralization illustrate different mechanisms. The chapter also emphasizes cost, reduced responsiveness and physical difficulty of expansion.

**Representation.** Distinguish installed storage capacity, current usable stock, committed or inaccessible stock, replenishment and consumption processes, loss, quality and availability during the disturbance. Increasing a tank's capacity does not fill it. Two reserves with equal size can differ because one is inaccessible when a shared dependency fails.

Where quantities and assumptions justify it, stock divided by a relevant rate has units of time. This is an illustrative time-scale comparison, not a new universal resilience metric: average-rate coverage can conceal peaks, replenishment delays, spoilage and incompatible resources. Chemical buffering also requires its actual reaction mechanism, not a literal inventory analogy.

**Development practice.** Compare service continuity, capital and maintenance cost, response flexibility and recovery. Include both an interruption and changing demand. Test reserve sizing with its replenishment and dispatch limits, rather than assuming that a larger stock is always better. A business's lower inventory cost and a wider system's exposure can be different criteria.

**Critical qualification.** The chapter explains why buffers can be influential but difficult to change. That is a distinction between dynamic effect and intervention accessibility; it should not become a rule that low-ranked physical changes are unimportant.

### 32.3 Position 10 — Physical stock-and-flow structures, pp. 150–151

**Source mechanism.** Physical arrangement can determine congestion, losses, delays and operating limitations. The chapter contrasts redesign before construction with costly rebuilding later. It also includes inherited cohort histories, pollutant persistence and slow replacement of durable equipment.

**Representation.** Record topology, intersecting routes, capacity, conversion losses, bottlenecks, lifetimes, age/cohort composition, replacement pipelines and construction resources where consequential. Equal total installed stock does not establish equal future replacement or service if ages differ. A routing parameter and a new physical connection are different changes even when their observed effects resemble each other.

**Development practice.** Compare alternative design, retrofit, operating strategy and demand/change-rate adjustments. Keep work-in-progress, service interruptions, capacity during construction and eventual retirement explicit. A scenario must carry existing quantities and commitments into the changed topology; it cannot teleport material, reset pollution or instantly replace a fleet.

**Critical qualification.** The chapter uses strong language about rebuilding poorly arranged systems. Our architecture retains rebuilding as one candidate along with operating and demand changes, then examines what each can accomplish. Physical influence can be large while a particular alteration remains unavailable within the chosen horizon. Source-era estimates of energy savings and turnover durations are not imported as universal present-day parameters.

### 32.4 Position 9 — Delays, pp. 151–152

**Source mechanism.** Delayed information or delayed response can produce overshoot and oscillation. Importance depends on delay relative to changing conditions and response dynamics. The chapter warns about both overly rapid reactions and overlong delays, especially where an irreversible threshold can be crossed before correction arrives.

**Representation.** Identify each delay stage: availability, attention, estimation, decision, order, transport, construction, maturation, completion and effect. Record distribution or qualitative range, controllability, relevant history and pending commitments. Do not use one global latency number. Shorter sensing delay does not shorten construction or biological maturation.

**Development practice.** Vary the relevant delay together with corrective intensity and the rate of disturbance or growth. Compare acting faster with reducing the speed of the process being controlled, preserving a reserve or using foresight. Include prior orders and projects, so repeated reactions do not ignore work already under way. Unknown delay distributions can remain explicit rather than being assigned arbitrary constants.

**Critical qualification.** Oscillation is conditional on the full dynamics, not a universal consequence of delay. Shortening a delay is not inherently destabilizing or stabilizing. The chapter's financial-market and central-planning claims remain illustrations to investigate, not universal institutional laws. A fixed physical delay can reduce the feasibility of following rapidly changing demand without establishing that no useful coordination is possible.

### 32.5 Position 8 — Balancing feedback, pp. 153–155

**Source mechanism.** Corrective ability is a property of the entire path: relevant reference, monitoring, signaling, response and feasible corrective flows. Its adequacy is relative to the disturbance. Multiple mechanisms can provide protection under different conditions, including rarely activated emergency mechanisms. Removing them can leave normal output unchanged while narrowing survivable conditions.

**Representation.** Link sensing accuracy and timing, channel availability, response rule, actuator condition, resources, authority, capacity and maintenance. Reuse the original process identities rather than adding a separate corrective force for the loop label. Record dormant modes and common dependencies of backup paths. Disturbance magnitude, duration and affected mechanisms belong to the assessment context.

**Development practice.** Test normal and uncommon conditions; disable individual links and shared supports; compare added capacity with improved information, maintenance or changed disturbance exposure. Examine possible delay-induced side effects of stronger correction. A loop's strength need not be one numeric gain in a nonlinear or heterogeneous system.

**Wider-system point.** The chapter connects market signals, externalized costs, information, government and influence over governance. A locally corrective arrangement can be weakened by a wider information or authority structure. Its named institutional examples are not substitutes for specifying the actual channels and powers in the system being modeled.

**Critical qualification.** The thermostat passage is schematic. A quantitative thermal model needs energy balance and heat-capacity meaning; temperature must not be treated as conserved heat. Unused backup capacity is neither automatically waste nor automatically sufficient protection. Its contribution depends on feasibility under the examined disturbance.

### 32.6 Position 7 — Reinforcing gain, pp. 155–156

**Source mechanism.** Self-amplification can generate growth, erosion and concentration. The chapter argues that reducing a troublesome driving mechanism may be more effective than strengthening compensatory correction indefinitely. In its examples, slowing a driving process can give delayed adaptation time to work.

**Representation.** Identify the return path, self-multiplying relationship, resources, nonlinear range, competing loops, relevant history and limits. A numerical gain needs a defined local or dynamic meaning. A reinforcing label alone supplies neither an exact exponential law nor the eventual outcome. A loop can support desirable learning or recovery, so reducing gain is assessed against attributed outcomes.

**Development practice.** Compare modifying the driving path with strengthening compensation; vary both separately and jointly. Examine whether an intervention actually weakens the path or shifts it elsewhere. The success-to-the-successful example additionally requires tracking how influence can change countervailing governance, potentially turning an intended restraint into further support for concentration.

**Critical qualification.** Unbounded physical growth cannot be assumed, but the specific stopping process must be represented rather than prescribed by the label. The nuclear illustration is a loose analogy, not a reactor-physics model; its statements about neutron energy, criticality and failure modes are not adopted as technical laws. No neutronics or clinical model is inferred from the chapter's examples.

### 32.7 Position 6 — Information-flow structure, pp. 156–157

**Source mechanism.** Creating or restoring a missing information relationship can close a new feedback path. This differs from tuning speed or intensity in an already connected path. The recipient, content and compelling consequences matter. The chapter warns that telling aquifer users about depletion could accelerate extraction instead of restraining it.

**Representation.** Specify variable meaning, producer, recipient, availability and receipt time, visibility, attention, interpretation, credibility and feasible response. Distinguish a resource-population signal from market price, which can rise as scarcity increases and intensify incentives to extract. Make institutional cost or accountability changes explicit; changing a water tariff is not merely sending a message.

**Development practice.** Compare an existing hidden record, a visible display, a new recipient, alternative content and a recipient unable or unwilling to act. Include a plausible adverse response, such as faster appropriation. Trace whether the new path actually closes a return to the condition being observed. More records in the analyst's database do not automatically inform actors.

**Critical qualification.** The chapter repeats the meter story as a 30 percent contrast, whereas the earlier account described roughly one-third less use. Neither formulation becomes a calibrated causal effect. Selection, configuration and reporting alternatives remain open. The provocative accountability hypotheticals illustrate consequence incidence; they are not adopted as literal intervention recommendations.

### 32.8 Position 5 — Rules, pp. 158–159

**Source mechanism.** Rules shape access, incentives, permissible responses and the process by which rules themselves can be changed. Power over rule setting is therefore distinct from compliance with an existing rule. The chapter uses contracts, constitutions, education arrangements and trade institutions to broaden this inquiry.

**Representation.** Separate physical law, institutional rule, informal norm, perceived restriction and analyst assumption. Physical constraints cannot be repealed by a policy proposal. For an institutional rule, specify issuer, jurisdiction, affected actors, interpretation, enforcement, sanctions/incentives, effective version, amendment procedure and who controls that procedure. Authority can be contested or uncertain.

**Development practice.** Compare changes in a rule's value, its form, enforcement, membership and amendment authority. Allow actors to adapt to the change, including rule beating and concentration of influence. Record the path from formal adoption to actual execution. A rule that exists on paper but is unenforced can differ from the rule actors perceive.

**Critical qualification.** The chapter's assessments of political and trade systems are source interpretations. They do not establish known motives or a single uncontested purpose for every organization. Rule-setting power must be supported or explicitly assumed for the scenario. Wider effects and legitimacy are attributed criteria, not truths created by a formal compliance test.

### 32.9 Position 4 — Self-organization, pp. 159–161

**Source mechanism.** A system may generate new structures, responses or rules. The chapter emphasizes variation-bearing material, processes that generate alternatives, experimentation, selection and retention. Biological, scientific, technological and cultural examples illustrate different sources and selection environments.

**Representation.** Extend the existing organization-change contract with the source of alternatives, access to retained repertoires, generation process, experimentation resources, selection criteria and who controls them, retention or rejection, costs, timing and state/history carry-over. Scientific knowledge and DNA are not interchangeable numeric stocks. Their roles may correspond without their units, rules or evidence being transferable.

**Development practice.** Compare preserved versus lost repertoires, different experimentation permissions, selection environments and retention procedures. Track unsuccessful variation and harmful novelty as well as successful adaptation. Test whether a proposed new structure was actually generated or merely inserted by the analyst. Technology must not appear costlessly at a predetermined improvement rate unless that is a declared external assumption.

**Critical qualification.** Self-organization can contribute to resilience but does not guarantee survival under almost any condition. Useful variation, available resources and compatible conditions matter. Encouraging diversity is not a proof that every experiment is valuable or that all constraints should disappear. The chapter's broad evolutionary claims are not a complete biological theory.

### 32.10 Position 3 — Goals, pp. 161–162

**Source mechanism.** Purposes can shape which structures, information and innovations are selected. Local loop references and wider organizational purposes are different levels. The chapter also qualifies the claim that changing personnel is shallow: a person with actual authority to change purpose can alter more than the identity of the officeholder.

**Representation.** Attribute each purpose, reference and selection criterion to its owner and scope. Distinguish a viability constraint, stated mission, inferred operating purpose, formal target and actual selection behavior. Goals can conflict across levels, be incomplete, change over time or be unknown. Do not infer a universal drive for expansion from an organization or species label.

**Development practice.** Compare a new statement with changed resource allocation, incentives, selection and execution. Hold a technology constant while varying its adopted purpose and deployment context. Evaluate several stakeholder criteria and time horizons rather than assuming all actors accept the new goal. A change of leader matters through a supported authority and adoption path.

**Critical qualification.** Historical leadership stories and generalizations about corporations or living populations remain source interpretations. They do not license teleological claims about every biological process or known private motivations. A better-sounding goal is not automatically feasible, adopted or consistent with the desired wider outcome.

### 32.11 Position 2 — Paradigms, pp. 162–164

**Source mechanism.** Shared assumptions about reality, value and legitimacy can shape goals, rules, measurement and physical arrangements. Such assumptions can be unstated because participants treat them as obvious. The chapter contrasts possible rapid individual change with social resistance and describes anomalies, alternative accounts, public influence and system modeling as possible contributors to change.

**Representation.** A proposed frame record contains its attributed holder or community, scope and time, categories and boundary assumptions, empirical beliefs, normative priorities, legitimacy assumptions, relationships it influences, evidence and alternatives. Shared belief is a hypothesis requiring evidence; do not give every member of a population an identical frame. Separate the analyst's assumptions from modeled actors' beliefs.

**Development practice.** Compare candidate frames against the same retained evidence, with clear differences in empirical predictions and normative evaluation. Trace how changed interpretation could alter choices, institutions or design through adoption and implementation. Include persistence of existing infrastructure and beliefs. A reframing in our model does not retroactively alter actual observations or instantly rebuild the world.

**Critical qualification.** A paradigm label must not become an unexplained cause of everything. Some constraints remain physical regardless of belief. A frame can be useful for one question and misleading for another; its empirical claims can be contradicted. The chapter does not supply a universal mathematical model of belief formation or social diffusion.

### 32.12 Position 1 — Transcending paradigms, pp. 164–165

**Source contribution.** Meadows argues for flexibility about one's deepest worldview and recognition that any paradigm is limited. This passage is philosophical and includes spiritual language; it is not a specified cognitive algorithm, a scientific result that every belief is equally false, or a claim our architecture can implement enlightenment.

**Operational interpretation proposed here.** Expose the assumptions a model depends on; preserve alternative frames; identify where they yield different explanations or evaluations; revise, bracket or decline a conclusion when evidence is insufficient. A system can act provisionally while retaining uncertainty. It need not choose one frame for all future tasks or remain indefinitely indecisive.

**Representation.** Record candidate frame versions, the question for which each is used, evidence compatibility, unresolved normative disagreement, consequences of the choice, revision triggers and any working decision. Distinguish an actor's ability to reconsider from the analyst's ability to write several scenarios. Storing alternatives does not itself demonstrate that either can revise its governing assumptions.

**Development practice.** Present anomalies that distinguish a parameter error from a frame limitation, compare plausible rival frames, check whether conclusions survive, and record why a working frame is retained. Do not select a frame merely because it yields the preferred answer. Some differences concern values rather than competing factual predictions; more observations alone may not resolve them.



## 33. Key records and component specifications

### 33.1 Intervention specification

| Field group | Required meaning |
| --- | --- |
| Identity and version | Proposal/scenario identity, baseline model, target referents and effective time |
| Question and criteria | Problem, desired consequences, owners, scope, horizon and unresolved stakeholder disagreement |
| Target and change | Exact parameter, stock/capacity, topology, timing, response path, information, rule, generating process, goal or frame affected; multiple categories allowed |
| Direction and rationale | Increase/decrease/replace/add/remove or qualitative change, mechanism path and why the proposed direction might help |
| Conditions | Applicable operating range, initial and retained history, external drivers, constraints, critical unknowns and alternative mechanisms |
| Agency and adoption | Who proposes, authorizes, interprets, adopts and implements; opposition, coordination and enforcement where relevant |
| Resources and timing | Required capacity, cost categories, delays, commitments and possible transition disruption |
| State/history transition | Persistent referents, quantities, cohorts, pipeline work, beliefs, rule versions and initialization of genuinely new state |
| Evidence and status | Source basis, assumed versus observed adoption, inferred mechanism, scenario output, contradictory evidence and revision history |
| Consequences | Direct, delayed, distributional and cross-system effects; actual outcome versus proxy and effect versus desirability |
| Reassessment | Monitoring, feasible stopping/revision conditions and reversibility or residual commitments where appropriate |

The record can be sparse when the proposal is qualitative; unknowns are explicit. There is no compulsory numerical leverage score and no assertion that every intervention can be reversed. A change in representation is not an adopted intervention.

### 33.2 Interpretive-frame specification

| Field group | Required meaning |
| --- | --- |
| Attribution | Analyst, actor, subgroup or community; evidence for membership and shared assumptions; no automatic homogeneity |
| Contents | Empirical beliefs, categories, boundaries, priorities, legitimacy assumptions and meanings kept distinguishable |
| Scope and time | Context, applicability, effective period, version and relevant memory |
| Dependents | Which interpretation, purpose, indicator, rule, choice or design relationship uses which assumption |
| Evidence status | Observed expression, source report, inferred belief, scenario assumption, contradiction or unresolved status |
| Alternatives | Rival frames, disagreements, domain limitations and potentially discriminating observations |
| Revision pathway | Proposed anomaly/experience, interpretation, social or individual update process, adoption and persistence; may remain unknown |
| Consequences | Different factual predictions, normative evaluations, decisions and distribution of effects |

Changes in frame contents do not directly create a physical resource. An empirical claim and an ethical preference have different assessment needs. A frame should be decomposed into consequential assumptions when a global label obscures the explanation.

### 33.3 Conditional analysis specification

A useful optional formalization retains the parent model's structure:

\[
\dot x=f(x,m,u;G,\theta,\pi),
\qquad
(x^+,m^+,G^+,\theta^+,\pi^+)=\Psi(x^-,m^-,G^-,\theta^-,\pi^-;e).
\]

Here x denotes accumulated state, m relevant history and pending effects, u declared external conditions, G organization, theta mechanism parameters and pi policies/references. An intervention may affect several arguments. An interpretive frame can influence particular actor interpretation or policy mechanisms where specified; it is not added as an unexplained scalar controlling the whole equation.

A proposed effect can be compared as:

\[
\Delta Y(H\mid M,\omega)=Y_{\mathrm{change}}(H\mid M,\omega)-Y_{\mathrm{baseline}}(H\mid M,\omega),
\]

where M is the candidate model, omega the declared initial history and conditions, H the horizon, and Y a defined compatible outcome. This is a conditional model comparison, not an identified real causal effect. If outcomes are qualitative, incomparable or vector-valued, retain the corresponding comparison rather than forcing subtraction or a total score. Compare plausible alternative M and omega; a result can remain unresolved.

Numerical sensitivity is not a universal leverage ranking. The scale of a parameter, nonlinearity, constraints and transition can change what a derivative means. Near a discontinuity or change of structure a local derivative may be insufficient or undefined. Unit-incompatible outcomes must not be summed to construct an attractive ratio.



## 34. Interface and integration requirements

Assess each consequential direction independently, including cases in which a link is absent, inapplicable or unresolved. Bidirectional exchange does not require equal strength, delay or authority. Indirect effects and common dependencies can matter even when no direct link exists.

| Interface | Contract | Failure to prevent |
| --- | --- | --- |
| Proposal → target mechanism | Named referent, version, exact change, direction, conditions | A leverage category stands in for the actual change |
| Physical arrangement ↔ stock/process state | Quantity meaning, capacity, conversions, location, cohorts, construction and carry-over | More capacity silently creates stock or material teleports after redesign |
| Delay ↔ response ↔ disturbance | Stage, history, duration, timing and applicable rates | Faster sensing is mistaken for faster physical completion |
| Corrective loop ↔ support and disturbance | Full path, backup dependencies, available resources and disturbance conditions | Apparently idle protection is removed without assessing unusual conditions |
| Information → actor interpretation → intent | Recipient, delivery, attention, meaning, memory and feasible perceived options | Analyst knowledge or future outcomes leak into actor choice |
| Intent → realization | Actual resource, physical and institutional constraints | Announced or desired success is recorded as realized effect |
| Rule ↔ rule-setting authority ↔ adaptive response | Issuer, scope, amendments, enforcement, perceived incentive and strategy changes | A rule's text is treated as full compliance or as unchangeable physics |
| Repertoire ↔ experimentation ↔ selection | Alternative source, resources, permissions, selection criteria and retention | Useful novelty appears for free or every variation is retained |
| Frame → goals/rules/information interpretation | Attributed assumption, dependent relationship and evidence | A homogeneous paradigm becomes a universal causal shortcut |
| Anomaly → frame reconsideration | Independent evidence, competing interpretations and explicit update or unresolved pathway | Any inconvenient observation is dismissed by changing the frame arbitrarily |
| Scenario → predicted consequences ↔ observations | Baseline, outcome correspondence, units, time, scope and independent record | Matching model output is recycled as independent confirmation |
| Local intervention ↔ wider systems | Shared referents, exchanged quantities, delayed effects and boundary closure | Harm is exported or an internalized driver is counted twice |


The parent integration boundary is now closed through sections 37–42: the sixteen Chapter 6 parent requirements and all 64 foundation units have cumulative allocations. No source statement or position number is converted into an automatic policy ranking.


## 35. Best practices for modeling and intervention inquiry

| Practice | Application |
| --- | --- |
| Start with the question and attributed outcomes | A large effect is not automatically a desirable result; preserve distribution and disagreement |
| Locate the complete affected path | Identify sensing, interpretation, response, physical execution, resources and return effects |
| Check direction before intensity | The chapter's opening warning concerns pushing an influential point the wrong way |
| Separate influence from access | A physical bottleneck can be decisive but unavailable to change within the horizon |
| Compare categories without treating rank as evidence | A parameter near a threshold can matter more than an inaccessible paradigm proposal |
| Use relevant relative scales | Buffer versus flow; delay versus change; correction versus disturbance; selection versus retention |
| Preserve normal and dormant mechanisms | Ordinary performance may not expose lost emergency capability |
| Model implementation and transition | Announcements, adoption, enforcement, capacity and realized effects are different stages |
| Consider adverse actor adaptation | Information can accelerate competition; rules can induce avoidance; power can reshape constraints |
| Include preserved and lost future options | Diversity, knowledge, capabilities and existing infrastructure affect later adaptation |
| Expose assumptions and their owners | Distinguish physical conditions, analyst assumptions, empirical beliefs and normative priorities |
| Allow conditional decisions and unresolved conclusions | Model incompleteness need not imply either certainty or permanent inaction |

The chapter does not present a software testing protocol. The requirements and scenarios below operationalize these practices for model development; they are our proposal, not tests claimed to have been performed by Meadows.


### 35.1 Continuous example across all twelve positions

Use the parent inventory-and-service system, retaining the same dealer, supplier, users, inventory, capacity, information channels and pending orders. The objective is not predetermined maximization of stock; the inquiry might concern reliable service with acceptable cost, distribution and resource use.

- **12:** vary an order correction parameter or reorder threshold, preserving its units, delay and feasible range.
- **11:** vary usable reserve or storage capacity separately, including replenishment and carrying cost.
- **10:** compare an actual transport route or supplier topology change, with construction and shared constraints.
- **9:** distinguish sales-estimation delay, ordering delay and physical delivery time; compare slower correction or demand variation with faster information.
- **8:** restore a damaged ordering link or a rarely used backup, checking shared dependencies under disruption.
- **7:** examine a reinforcing priority rule through which high prior sales yield more allocation and future sales; distinguish it from genuine productivity differences.
- **6:** deliver relevant stock or supplier information to a previously uninformed participant; include attention and possible overreaction.
- **5:** change allocation rules, penalties or amendment authority and allow participants to adapt.
- **4:** support experiments with new suppliers or repair routines, using existing knowledge, resources, selection and retention.
- **3:** compare maximizing shipment count with reliable essential service, changing actual incentives and selection where adopted.
- **2:** compare the assumption that efficiency means minimum local stock with one that values wider continuity and distributed reserve; retain actual accounting and evidence in both.
- **1:** identify where neither frame explains an anomaly, retain alternatives, and revise the working account without rewriting observations.

These are twelve views of possible changes to the same system. Several may be combined, and some may be infeasible or irrelevant. Combining them requires a joint scenario and explicit interactions; isolated predicted benefits cannot simply be added.




## 36. Source foundation catalogue

The 64 entries below are our source-review units, not 64 official primitives stated by Meadows. Their formulation records a source proposition and its proposed representation consequence. Broader claims and illustrations retain the qualifications in section 3.

| Foundation | Printed pages | Source contribution | Proposed modeling consequence |
| --- | --- | --- | --- |
| C6-F01 | 145–146 | An influential intervention point can be pushed in a harmful direction. | Specify direction and the complete claimed pathway; do not infer benefit from influence. |
| C6-F02 | 146–147 | The list is an invitation to broader thought, not a formula for locating leverage. | Use categories as inquiry prompts, with evidence and rival explanations. |
| C6-F03 | 147 | Coupled stocks and flows can produce dynamics difficult to infer from isolated parts. | Retain joint constraints, boundaries and multiple interacting paths. |
| C6-F04 | 145–147 | Understanding and changing system structure are related but distinct inquiries. | Separate explanation, intervention hypothesis, adoption and observed effects. |
| C6-F05 | 147–148 | Constants and parameters adjust processes within an existing arrangement. | Identify the exact value, role, units and governing mechanism. |
| C6-F06 | 147 | Some settings are physically fixed or change only at a limited rate. | Record adjustability, authority and implementation timing. |
| C6-F07 | 148 | Replacing personnel can leave the same information, rules and goals intact. | Represent changes in roles and mechanisms rather than inferring structural change from a new name. |
| C6-F08 | 148 | Parameter changes can matter to individuals and in the short term without removing a wider pattern. | Assess distribution, horizon and aggregate behavior separately. |
| C6-F09 | 149 | Critical settings can alter loop gain or goals and be consequential exceptions to low parameter leverage. | Inspect domains, thresholds, references and changed dominance. |
| C6-F10 | 149–150 | Buffer effects depend on stock size relative to relevant flows. | Distinguish reserve, rate and time-scale comparisons. |
| C6-F11 | 150 | Buffers can protect against variability and interruption. | Connect reserve access to actual functioning and replenishment. |
| C6-F12 | 150 | Large buffers can impose cost and inflexibility. | Compare continuity, resource use and response to changing demand. |
| C6-F13 | 150 | Physical buffer capacity can be difficult to change. | Separate potential influence, construction feasibility and current usable stock. |
| C6-F14 | 150 | Physical arrangement and points of intersection shape system operation. | Represent topology, shared routes, losses and bottlenecks. |
| C6-F15 | 151 | Rebuilding infrastructure can be slow, expensive or unavailable. | Include transition capacity, existing commitments and implementation resources. |
| C6-F16 | 151 | Cohorts, pollutant persistence and durable equipment retain consequential history. | Preserve age structure, lifetime and replacement or removal processes where relevant. |
| C6-F17 | 151 | Design-stage choices and effective use of inherited constraints can differ from later rebuilding. | Compare design, retrofit and operating options under explicit horizons. |
| C6-F18 | 151–152 | Information and response delays can affect oscillation and target tracking. | Keep different delay stages and full response dynamics distinct. |
| C6-F19 | 152 | Delay relevance depends on the rate of change being controlled. | Use relative time scales rather than one universal latency target. |
| C6-F20 | 152 | Both overlong delay and overly jumpy response can cause trouble under appropriate dynamics. | Test delay, response intensity and operating conditions jointly. |
| C6-F21 | 152 | A delayed correction can arrive after an irreversible threshold is crossed. | Represent danger conditions, pending effects and recovery limits. |
| C6-F22 | 152 | Where delays are hard to shorten, reducing driving change may let adaptation catch up. | Compare feasible change rates with shortening information or completion delays. |
| C6-F23 | 153 | Balancing response depends on monitoring, signaling, a reference and a feasible response mechanism. | Specify complete paths and actual resource conditions. |
| C6-F24 | 153 | Several corrective mechanisms can support different disturbance conditions. | Represent modes, alternatives and activation conditions. |
| C6-F25 | 153 | Rarely used emergency mechanisms can be crucial despite no ordinary visible contribution. | Assess unusual conditions before removing dormant capacity. |
| C6-F26 | 153–154 | Corrective strength depends on combined links and must be assessed relative to the impact. | Trace sensing, timing, actuation, shared support and disturbance magnitude. |
| C6-F27 | 154–155 | Wider information, governance and externalized costs can weaken local correction. | Include relevant institutional feedback and cross-level dependencies. |
| C6-F28 | 155 | Reinforcing paths can amplify growth, erosion and concentration. | Identify the return path and conditional response law. |
| C6-F29 | 155–156 | Reducing a driving reinforcing mechanism can be preferable to ever stronger compensation. | Compare changes to driving and corrective paths separately and together. |
| C6-F30 | 156 | Slower driving change can give delayed adaptive processes time to operate. | Retain the time horizon, residual disturbances and delayed response. |
| C6-F31 | 156 | Influence over government can weaken countervailing controls on compounding advantage. | Represent the pathway changing governance, not only a fixed tax or allocation setting. |
| C6-F32 | 156–157 | A new information connection can establish feedback that previously did not reach a recipient. | Distinguish adding a path from tuning an existing path. |
| C6-F33 | 157 | A scarcity-related price need not convey population or resource condition in a corrective way. | Preserve signal meaning and the recipient response mechanism. |
| C6-F34 | 157 | Useful feedback must reach an appropriate place in an actionable form. | Specify receipt, attention, interpretation and feasible responses. |
| C6-F35 | 157 | Information about depletion can induce faster appropriation rather than restraint. | Include plausible adverse behavioral responses. |
| C6-F36 | 157 | Accountability and who experiences consequences affect missing feedback and its acceptability. | Separate disclosure, cost incidence, permissions and political adoption. |
| C6-F37 | 158 | Rules shape permissions, incentives and degrees of freedom. | Represent scope, enforcement and interpretation. |
| C6-F38 | 158 | Physical laws, formal rules and informal agreements have different meanings. | Institutional redesign must not overwrite physical constraints. |
| C6-F39 | 158 | Authority to make, interpret or change rules is consequential. | Identify amendment procedures, power and affected participants. |
| C6-F40 | 158–159 | Rule arrangements can exclude feedback and favor reinforcing concentration. | Trace participation, access, influence and adaptation. |
| C6-F41 | 159 | Self-organization can add or alter structure, feedback and rules. | Represent actual generating processes and state/history carry-over. |
| C6-F42 | 159 | Complex structures can arise from particular relatively simple generating rules. | Specify the rule and conditions; complexity alone does not identify it. |
| C6-F43 | 160 | Variation-bearing repertoires, generation, experimentation, selection and retention support adaptation. | Identify the separate mechanisms and resources. |
| C6-F44 | 160 | Biological, scientific and cultural diversity preserve potential future alternatives. | Represent loss or restricted access to consequential repertoires without requiring a universal diversity score. |
| C6-F45 | 160–161 | Suppression of variation and experimentation can narrow future adaptation. | Compare permission and selection conditions, including costs and failed novelty. |
| C6-F46 | 161 | Wider goals can direct physical organization, information, rules and selection of novelty. | Trace purpose through actual choices and institutions. |
| C6-F47 | 161 | Local reference settings and wider system purposes are different levels. | Attribute owner, scope, conflict and evaluation criteria. |
| C6-F48 | 161–162 | A viability rule, stated purpose and inferred operating purpose need not be identical. | Keep attribution and evidence distinct from a label. |
| C6-F49 | 162 | A person with effective authority can change more than personnel by changing adopted goals. | Represent authority, adoption and implementation rather than an automatic leader effect. |
| C6-F50 | 162–163 | Shared assumptions can shape perceived fairness, meaning, goals and arrangements. | Use attributed, contextual frame claims rather than universal cultural constants. |
| C6-F51 | 163 | Deep assumptions can be unstated and differ across communities. | Preserve inference status, disagreement and alternatives. |
| C6-F52 | 163 | Interpretive assumptions can influence institutional and physical arrangements. | Require an explicit mediated pathway to actual change. |
| C6-F53 | 163–164 | Individual belief change and social paradigm change can have very different timing and resistance. | Represent uptake, persistence, heterogeneity and unknown update processes. |
| C6-F54 | 164 | Anomalies, alternative accounts, visible influence and system modeling can contribute to reconsideration. | Treat each as a possible mechanism rather than an assured conversion procedure. |
| C6-F55 | 164 | The chapter advocates recognizing the limitations of any paradigm. | Expose assumptions and domain limits without declaring all factual claims equally valid. |
| C6-F56 | 164 | Flexibility between paradigms is distinguished from merely adopting a new one. | Keep capacity for reconsideration separate from storing a replacement frame. |
| C6-F57 | 164–165 | The account of transcending paradigms includes philosophical and spiritual claims. | Attribute those claims; the operational proposal is revisability, not implemented enlightenment. |
| C6-F58 | 164–165 | Purposes and action can remain possible without certainty in a final worldview. | Allow qualified working decisions while retaining evidence and unresolved alternatives. |
| C6-F59 | 165 | The leverage order is tentative and exceptions can move categories. | Do not derive fixed efficacy scores from list position. |
| C6-F60 | 165 | Influential changes can encounter substantial resistance. | Represent adoption and implementation separately from potential effect. |
| C6-F61 | 165 | Knowing a target and a direction does not make it accessible. | Retain feasibility, authority, resources and horizon. |
| C6-F62 | 146–147, 165 | There is no quick universal recipe for mastery of system intervention. | Withhold unsupported rankings and acknowledge unresolved mechanisms. |
| C6-F63 | 147, 165 | Generalization about complex systems requires qualification. | Keep source examples, assumptions and domain correspondence visible. |
| C6-F64 | 165 | The closing emphasizes responsiveness and humility rather than forceful control alone. | Interpret as a prompt for monitoring and revisability, not a prescribed algorithm. |




## 37. Retained six-chapter record — Six-chapter cumulative requirement allocation

I7-R01–I7-R30 preserve the earlier thirty meanings in sections 10 and 26; I7-R31–I7-R42 below add or strengthen the Chapter 6 obligations. Legacy I5-R01–I5-R30 map one-to-one to the same-number I6 requirements, and I5-T01–I5-T68 to the same-number cumulative cases. Chapter 6 C6-T01–C6-T48 map in order to I7-T69–I7-T116. The extra I7-T117–I7-T124 are prospective composition cases, not new observations.

| Requirement | Function | Obligation | Chapter 6 parents | Prospective cases |
| --- | --- | --- | --- | --- |
| I7-R31 | Qualified intervention and leverage inquiry | Record target, direction, baseline, adoption, criteria, resources, timing and uncertainty. Categories overlap and list order does not determine effect or preference. | C6-R01, C6-R14, C6-R15, C6-R16 | I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| I7-R32 | Parameter meaning and critical ranges | Preserve units, applicable rule, adjustability, operating range, threshold uncertainty and exceptions to shallow-parameter intuition. | C6-R02 | I7-T69, I7-T70, I7-T71, I7-T105, I7-T120 |
| I7-R33 | Buffers and usable capacity | Separate installed capacity, usable reserve, access, replenishment, relevant flow scale, cost and flexibility. | C6-R03 | I7-T72, I7-T73, I7-T74, I7-T117 |
| I7-R34 | Physical arrangement and cohort history | Specify topology, shared bottlenecks, construction, age/lifetime history, replacement and carry-over. | C6-R04 | I7-T75, I7-T76, I7-T77, I7-T109, I7-T117 |
| I7-R35 | Relative timing and feasible correction | Represent stage-specific delay, response intensity, driving rate, pending effects and irreversible conditions without a universal fastest-is-best rule. | C6-R05 | I7-T78, I7-T79, I7-T80, I7-T120 |
| I7-R36 | Corrective and driving mechanisms | Compare disturbance-relative balancing ability and conditional reinforcing gain, including dormant/common dependencies, limits and useful reinforcing processes. | C6-R06, C6-R07 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| I7-R37 | Information topology and adverse response | Distinguish hidden recording, new paths, tuned channels, resource versus price signals, received meaning and possible harmful action. | C6-R08 | I7-T87, I7-T88, I7-T89, I7-T121, I7-T123 |
| I7-R38 | Rules and authority over rules | Separate physical law, institutional rule, norm, belief, interpretation, enforcement and amendment authority; allow adaptation. | C6-R09 | I7-T90, I7-T91, I7-T92, I7-T119, I7-T122 |
| I7-R39 | Resource-supported generation and selection | Specify repertoire access, variation, experiment resources, selection, retention and actual structural change. | C6-R10 | I7-T93, I7-T94, I7-T95, I7-T119 |
| I7-R40 | Purpose, selection and adoption | Distinguish viability, local reference, attributed wider purpose, stated mission and actual selection; goal changes need a mediated adoption path. | C6-R11 | I7-T96, I7-T97, I7-T98, I7-T119, I7-T122 |
| I7-R41 | Owned interpretive assumptions | Keep actor/community frames separate from analyst assumptions and physics; retain heterogeneity, timing, evidence and mediated change. | C6-R12 | I7-T99, I7-T100, I7-T101, I7-T118, I7-T122, I7-T123 |
| I7-R42 | Reconsideration without evidence loss | Expose assumptions, compare empirical and normative differences, retain revision triggers and permit qualified decisions without asserting enlightenment or automatic cognitive flexibility. | C6-R13 | I7-T102, I7-T103, I7-T104, I7-T118, I7-T123, I7-T124 |

### 37.1 Chapter 6 parent-to-cumulative mapping

| Parent | Cumulative requirements |
| --- | --- |
| C6-R01 | I7-R31 |
| C6-R02 | I7-R32 |
| C6-R03 | I7-R33 |
| C6-R04 | I7-R34 |
| C6-R05 | I7-R35 |
| C6-R06 | I7-R36 |
| C6-R07 | I7-R36 |
| C6-R08 | I7-R37 |
| C6-R09 | I7-R38 |
| C6-R10 | I7-R39 |
| C6-R11 | I7-R40 |
| C6-R12 | I7-R41 |
| C6-R13 | I7-R42 |
| C6-R14 | I7-R14, I7-R28, I7-R31 |
| C6-R15 | I7-R11, I7-R12, I7-R31 |
| C6-R16 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31 |


## 38. Retained six-chapter record — Prospective modeling and testing scenarios

**Every case is PLANNED — NOT RUN.** The 48 cases here continue the retained 68-case catalogue; they are I7-T69–I7-T116. Their definitions retain the original Chapter 6 meanings. These are future checks on instantiated models, not results, tests copied from the book or evidence that the architecture already discovers leverage. The first 36 cases allocate three checks to each source position, proceeding from 12 to 1. The final 12 Chapter 6 cases address cross-cutting integration. The positions may overlap in a real intervention.

| Case | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T69 | Change the same parameter above and below its current value. | Keep units, conditions and horizon fixed where appropriate; effects follow the candidate response, not assumed linear symmetry. |
| I7-T70 | Vary a numerical setting near a supported threshold and far from it. | Allow a low-ranked numerical change to alter a regime; unknown thresholds remain unknown rather than calibrated to force the result. |
| I7-T71 | Replace an officeholder while keeping rules, information and authority fixed, then change actual authority. | Separate identity change from the supported mechanism through which a different person can affect goals or rules. |
| I7-T72 | Increase storage capacity without adding usable inventory. | No physical reserve appears until an explicit replenishment process adds it. |
| I7-T73 | Compare equal stocks with different flow rates, access limits and replenishment delays. | Report different protection where the specified dynamics justify it; equal stock alone does not imply equal resilience. |
| I7-T74 | Compare larger reserve during disruption and during a shift in demand. | Retain carrying cost, losses, flexibility and service criteria rather than forcing larger to be universally better. |
| I7-T75 | Compare route reconfiguration with construction of a genuinely new connection. | Distinguish operating-rule changes from physical topology and construction resources. |
| I7-T76 | Start two equipment populations with equal total capacity but different age profiles. | Retain different replacement commitments and subsequent service where lifetime mechanisms imply them. |
| I7-T77 | Retrofit while deliveries and construction are already pending. | Preserve material, initial state, service during transition and commitments; do not reset the system. |
| I7-T78 | Change information delay while holding physical completion delay fixed. | The changed signal does not make already ordered goods arrive earlier without a separate mechanism. |
| I7-T79 | Vary delay, corrective intensity and disturbance speed jointly. | Dynamics may differ; shorter delay is not universally beneficial or harmful. |
| I7-T80 | Compare faster correction with slowing the driving process near an irreversible threshold. | Account for existing commitments and threshold uncertainty; no action is granted foresight of later outcomes. |
| I7-T81 | Apply disturbances of different magnitudes and durations to the same corrective loop. | Adequacy remains relative to the disturbance and actual available capacity. |
| I7-T82 | Remove a rarely used backup, then damage a normal path and a shared support. | Ordinary unchanged output cannot certify unchanged resilience; alternative paths must respect common dependencies. |
| I7-T83 | Improve monitoring while actuation or authorization remains constrained. | A more accurate signal does not automatically create a larger corrective flow. |
| I7-T84 | Compare reducing a self-amplifying driver with adding compensatory correction. | Results follow the stated mechanisms, delays and limits; no universal winner is imposed. |
| I7-T85 | Let compounding advantage influence a countervailing rule. | Specify the governance influence pathway rather than silently changing enforcement in favor of the intended narrative. |
| I7-T86 | Apply gain reduction to a useful recovery or learning mechanism and to harmful erosion. | Evaluate attributed outcomes separately from reinforcing polarity. |
| I7-T87 | Compare a hidden logger, a new recipient and a faster pre-existing channel. | Adding a feedback path, tuning a path and merely collecting analyst data remain different interventions. |
| I7-T88 | Disclose declining aquifer condition under alternative actor response rules. | Permit restraint, no response or accelerated pumping where mechanisms support them; disclosure is not hardcoded as conservation. |
| I7-T89 | Compare a resource-population signal, a scarcity price and a changed tariff. | Keep signal meaning, incentive redesign and adoption explicit; do not treat all three as identical information. |
| I7-T90 | Propose an institutional change that conflicts with a physical constraint. | Changing a rule cannot repeal the candidate physical accounting or capacity constraint. |
| I7-T91 | Change a formal rule but leave interpretation or enforcement incomplete. | Formal adoption, perceived rule and realized compliance can diverge. |
| I7-T92 | Change authority to amend a rule and allow participants to adapt. | Represent who can change the rule, opposition and new strategies without fixed actor responses. |
| I7-T93 | Allow generation of a new supplier or repair arrangement. | New organization needs a specified generating pathway, resources and carry-over, rather than analyst insertion presented as discovery. |
| I7-T94 | Remove a relevant repertoire or restrict experimentation. | Assess the resulting alternatives under the declared inquiry; loss need not change immediate output. |
| I7-T95 | Hold generated alternatives fixed while varying selection and retention criteria. | Different retained organization can follow; all novelty is not automatically useful or costless. |
| I7-T96 | Announce a new mission without changing adopted incentives or allocation. | Do not rewrite actual operating goals or outcomes merely from the announcement. |
| I7-T97 | Use the same technology under two adopted purposes. | Keep physical constraints fixed and trace differences through deployment, selection and implementation. |
| I7-T98 | Change a local reference while retaining a conflicting wider purpose. | Preserve scope, owner and local versus collective outcome disagreement. |
| I7-T99 | Apply two candidate frames to the same retained evidence. | Record which differences concern factual prediction and which concern normative evaluation; neither frame can rewrite the evidence. |
| I7-T100 | Introduce a frame change first to one actor and then through a proposed social uptake process. | Do not assume instantaneous homogeneous belief across a community; timing and evidence remain explicit. |
| I7-T101 | Attribute a design change to a paradigm without a mediated adoption process. | Keep the causal explanation unresolved until choice, institution, resources and implementation are specified. |
| I7-T102 | Present an anomaly compatible with parameter error, missing mechanism or a frame limitation. | Compare these alternatives without automatically declaring a paradigm shift. |
| I7-T103 | Compare several frames while retaining a qualified working decision. | Reconsideration does not require either fixed certainty or indefinite paralysis. |
| I7-T104 | Store several alternative frames without any revision mechanism. | Do not claim demonstrated flexibility merely because alternatives are listed. |
| I7-T105 | Compare a critical parameter change with an inaccessible higher-position proposal. | List position cannot determine the preferred action; consider effect, access, cost, horizon and evidence separately. |
| I7-T106 | Classify one subsidy or target change under several source positions. | Reference all affected mechanisms without counting its physical effect more than once. |
| I7-T107 | Reverse the direction of an influential change. | Permit adverse effects; locating a sensitive target is not proof of beneficial direction. |
| I7-T108 | Propose an effective change lacking authority, resources or social adoption. | Separate modeled potential from feasible implementation and retain the failure or unresolved status. |
| I7-T109 | Change topology, frame, reference or rule with existing memories and commitments. | Apply state/history correspondence; physical resources and past observations cannot disappear. |
| I7-T110 | Combine two candidate interventions evaluated separately. | Use a joint scenario; predicted benefits need not be additive and interactions may reverse rankings. |
| I7-T111 | Reuse the meter, growth or housing example as a domain analogy. | Retain source provenance, rival explanations and domain correspondence; no anecdotal effect becomes an automatic calibrated law. |
| I7-T112 | Leave important response curves, uptake rates or criteria unknown. | Permit a useful qualitative model while withholding an unsupported numerical leverage score. |
| I7-T113 | Obtain a large aggregate improvement with adverse distribution or a disputed goal. | Report incompatible criteria separately; do not call the change universally beneficial. |
| I7-T114 | Obtain new observations inconsistent with a previously preferred intervention explanation. | Retain observations and revise the relevant hypothesis, assumptions or decision with a stated rationale. |
| I7-T115 | Internalize a wider source or governance process while several interventions share it. | Replace the former external closure where appropriate and count shared quantities and effects once. |
| I7-T116 | Pass scenario output through summaries and model revisions. | Predictions remain model-derived; repetition does not produce independent observational confirmation. |


### 38.1 What an eventual execution needs

For quantitative scenarios specify the equations or executable rules, variable meanings and units, initial values, cohorts and prehistory, pending commitments, driver schedules, parameter/structural versions, adoption and transition processes, boundary closures, numerical settings and diagnostics. An uncertainty or range must have an interpretation; not every unknown can be assigned a defensible probability. Compare plausible mechanisms and conditions rather than fitting one favorable trajectory.

For empirical evaluation obtain independent observations relevant to the stated mechanisms and adoption conditions. Prediction-versus-observation correspondence needs compatible quantities, timing and aggregation. Matching a curve does not uniquely identify the intervention mechanism. A simulated counterfactual is conditional on its model, rather than a measured causal effect by itself.

For decision assessment retain stakeholder criteria, cost categories, implementation feasibility, timing, residual risk, distribution and irreversible commitments. If no common criterion or reliable ranking is justified, report that outcome. A document check cannot establish better decisions, AI reasoning, predictive advantage, token efficiency or runtime resilience.



### 38.2 Additional six-chapter composition cases

All eight additional cases are PLANNED — NOT RUN. They test the seams among chapters and supplement rather than replace source-level cases.

| Case | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T117 | Compare buffer capacity, actual reserve and a changed institutional belief about sufficiency. | A declared belief or larger vessel cannot create inventory. Preserve replenishment, accounting, available information and actual implementation. |
| I7-T118 | Explain a changed history using parameter, mechanism, driver, observation and frame alternatives. | Keep shared observations fixed, identify discriminating consequences and retain unknown explanations rather than forcing structural or paradigm change. |
| I7-T119 | Change rule-writing authority, selection criteria and information access in a resource-allocation system. | Trace local goals, counter-effort, compounding opportunity, experiment resources and actual adoption on shared referents; do not assume goal harmony. |
| I7-T120 | Compare a parameter near a critical regime with a slower, inaccessible higher-position intervention. | Evaluate direction, horizon, retained commitments, authority and affected outcomes; nominal leverage rank cannot determine a recommendation. |
| I7-T121 | Disclose depletion while rewards favor extraction and external support maintains local performance. | Permit a race, shifting advantage, loss or rebuilding of correction, delayed ecological effects and conflict between proxy and wider criteria under specified mechanisms. |
| I7-T122 | Announce a new mission or paradigm while actor information, rules and adoption remain unchanged. | Do not grant new knowledge, silently update behavior or record implementation. Compare a separately specified actual uptake process. |
| I7-T123 | Reuse meter and budworm accounts under rival analytical frames and intervention scenarios. | Keep source dependence, reported effect estimates, missing mechanisms and prediction status intact. A frame or model output does not independently confirm the source story. |
| I7-T124 | Face conflicting stakeholder values, incomplete evidence and a hard physical constraint. | Distinguish empirical uncertainty from normative disagreement, retain physical feasibility, document a qualified working decision or unresolved ranking, and preserve revision conditions. |


## 39. Retained six-chapter record — Six-chapter retrospective and integration disposition

This review combines the current five-chapter baseline, internal v0.5.1, and the Chapter 6 source assessment. It checks source allocation, representation meanings, mechanism composition, directed interfaces and prospective verification. The completed source reviews are retained; this pass does not claim a new page-by-page rereading of all 150 body pages or independent replication of their examples. Source scope is printed pp. 11–72, 75–141 and 145–165. Chapter 7 and later material remain outside scope.

### 39.1 Findings, rationale and disposition

| Finding | Integration issue | Repair and rationale | Status |
| --- | --- | --- | --- |
| A6-01 | Chapter 6 was a standalone extension, not part of the cumulative baseline | Integrate all 64 source-review units, twelve leverage positions, component records, interfaces and 48 proposed cases into the same shared model | Repaired conceptually |
| A6-02 | Paradigm language could mix the analyst's assumptions with actors' beliefs | Represent separately owned actor/community frames and analyst framing; retain scope, evidence, heterogeneity and dependent relationships | Repaired by representation contract |
| A6-03 | A candidate intervention could appear to change an actual rule, goal or belief directly | Add adoption and implementation as a declared process with actors, authority, resources, timing and status; a scenario changes its own model state | Repaired by integration contract |
| A6-04 | Depth on the leverage list could be mistaken for effectiveness or a policy ranking | Preserve conditional mechanism, direction, horizon, feasibility, costs, stakeholder criteria and exceptions; use no fixed rank-to-benefit score | Repaired by assessment contract |
| A6-05 | Buffer size, physical arrangement and delay language could hide different state meanings | Distinguish capacity from usable reserve; retain age/cohort composition, replacement, stage-specific delays and existing commitments | Repaired across the core families |
| A6-06 | A more powerful response or more information could be assumed always beneficial | Compare corrective and driving paths, disturbance-relative capacity, timing, recipient interpretation and adverse adaptation | Repaired in mechanisms and cases |
| A6-07 | New organization could be assumed to supply useful innovation automatically | Require repertoire access, generation, experiment resources, selection criteria, retention and actual state/history transition | Repaired across organization and purpose contracts |
| A6-08 | Reconsidering paradigms could become an untestable intelligence claim or unconstrained relativism | Operationalize exposing, comparing and revising assumptions; distinguish empirical claims from values and permit qualified working decisions | Repaired as an explicit design interpretation |
| A6-09 | An expanded diagram could be mistaken for a different model per chapter | Preserve shared referents and all earlier master relationships, with one connected graph and no separate chapter executor | Repaired in the master map |
| A6-10 | Earlier findings and verdicts could appear current after scope expansion | Mark the five-chapter review as retained history and make this section and section 42 authoritative for the six-chapter scope | Repaired editorially |

These statuses mean the conceptual specification was amended. They do not mean a physical mechanism, belief-update process, intervention or simulation has passed empirical testing.

### 39.2 Core semantic and temporal invariants

1. **Referents and accounting:** one actual constituent, transfer, shared capacity or commitment can participate in many views. Do not duplicate it when adding a trap, leverage category or wider boundary. Units, conversion, source and sink conditions remain explicit.
2. **Complete relevant history:** equal present totals need not imply equal futures. Preserve pending deliveries, maintenance progress, cohorts, learned expectations, rule versions and other history required by the proposed dynamics. Capacity expansion alone does not replenish a stock.
3. **Conditional mechanisms:** topology, polarity and a story do not determine a unique trajectory. Parameters, functional forms, domains, initial history, external conditions and competing mechanisms matter. Qualitative or unresolved rules are legitimate.
4. **Owned knowledge:** analyst state, actor-received information, actor interpretation, intended action and actual execution remain distinct. Private beliefs and shared frames require attribution and evidence; later observations cannot become earlier knowledge.
5. **Change status:** proposal, announcement, adoption, implemented change, actual consequence and observed evidence remain distinct. Structural or policy changes preserve state through a defined mapping. A new belief or target is not an instantaneous source of material or capability.
6. **Outcome meaning:** effort, activity, proxy, compliance, service, stock condition and welfare are not synonyms. Goals can conflict across actors and horizons. Improvement must identify the criterion and affected parties.
7. **Evidence independence:** source reports, inferred explanations, assumptions and scenario predictions retain separate status. Repetition, a second model or frame comparison does not create independent confirmation.
8. **Boundary correspondence:** expanding a view can reveal the cause of an old external driver; replace or condition the former closure at that interface. A revised analytical boundary is not itself actual physical reorganization.
9. **Interpretive limits:** an empirical claim can face contrary evidence even when framed differently. Normative disagreement may remain after additional observation. A frame is neither a law of physics nor an unexplained controller of everything.

These invariants are compatible with ordinary physical systems that have no sensing actor, stated purpose or demonstrated self-organization. The model must permit meaningful absences rather than manufacturing every depicted role in every instance.

### 39.3 Directed integration review

The review considers consequential A→B and B→A relationships separately, plus indirect return paths and common dependencies. A supported absence, an inapplicable link and an unknown link are different. The finite pairwise review is a way to organize questions; it does not require all-to-all physical connections or establish that all real-world components have been found.

| Interface | Required correspondence | Failure or uncertainty examined | Cumulative scenarios |
| --- | --- | --- | --- |
| Physical stocks ↔ processes ↔ supporting environment | Quantity, unit, shared transfer, capacity, regeneration, removal and boundary closure | Duplicate resource, invented reserve, missing sink or hidden bottleneck | I7-T02, I7-T04, I7-T16, I7-T72, I7-T75, I7-T115, I7-T117 |
| State/history ↔ sensing ↔ actor interpretation ↔ intent ↔ execution | Available information, attention, time, owned memory, perceived options and actual limits | Oracle knowledge, ignored commitment, improved intention from a hidden constraint | I7-T03, I7-T17, I7-T18, I7-T78, I7-T79, I7-T118 |
| Corrective paths ↔ shared supports ↔ disturbance | Mode, strength, timing, resources and common dependency | Stable ordinary output hides lost backup capability; stronger correction destabilizes another path | I7-T06, I7-T07, I7-T82, I7-T83, I7-T84, I7-T121 |
| Reward/access ↔ governance ↔ local or wider goals | Allocation, future capability, rule-writing power, incentives and constraints | Concentration changes the institution intended to restrain it | I7-T45, I7-T48, I7-T85, I7-T87, I7-T92, I7-T119 |
| Information disclosure ↔ incentives ↔ shared resource | Content, recipient, interpretation, ability, costs and realized use | A new signal creates a race rather than restraint | I7-T34, I7-T36, I7-T88, I7-T89, I7-T121 |
| Repertoire ↔ generation ↔ selection ↔ retention ↔ actual structure | Source, resources, experiment, criterion and carry-over | Useful novelty is inserted, alternatives are lost or selection defeats the stated purpose | I7-T65, I7-T93, I7-T94, I7-T95, I7-T119 |
| Actor frame ↔ information and goals ↔ adopted rules | Holder, assumption, dependent relationship, available experience and mediated adoption | Homogeneous belief, instantaneous social change or world change by mere declaration | I7-T96, I7-T99, I7-T100, I7-T101, I7-T122 |
| Analyst frame ↔ evidence ↔ candidate models ↔ assessment | Preserved source records, different assumptions, empirical prediction and normative evaluation | Preferred answers choose the frame; observations are rewritten; uncertainty becomes paralysis | I7-T102, I7-T103, I7-T104, I7-T111, I7-T112, I7-T123, I7-T124 |
| Intervention proposal ↔ adoption ↔ implementation ↔ transition | Implementer, authority, resources, timing, affected mechanism, status and retained state | Leverage rank replaces feasibility or two interventions' benefits are added without a joint scenario | I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T120 |
| Predictions ↔ independent observations and criteria | Referent, units, aggregation, time, conditions and provenance | Model-derived output is treated as new evidence or proxy success defines welfare | I7-T26, I7-T58, I7-T67, I7-T113, I7-T114, I7-T116, I7-T123 |

The rows are review allocations, not experiments or evidence that every proposed causal path is present in nature.

### 39.4 All twelve leverage positions in the integrated model

| Position | Existing roles and additional contract | Primary cumulative requirement | Representative prospective cases |
| --- | --- | --- | --- |
| 12 — Parameters | Response values, ranges, references and critical regimes | I7-R32 | I7-T69–I7-T71, I7-T105, I7-T120 |
| 11 — Buffers | Stock, usable reserve, capacity, replenishment and access | I7-R33 | I7-T72–I7-T74, I7-T117 |
| 10 — Physical structure | Constituents, topology, processes, cohorts, construction and carry-over | I7-R34 | I7-T75–I7-T77, I7-T109 |
| 9 — Delays | Stage-specific history, response timing, commitments and change rates | I7-R35 | I7-T78–I7-T80, I7-T120 |
| 8 — Balancing paths | Complete correction, dormant alternatives, capacity and disturbance | I7-R36 | I7-T81–I7-T83, I7-T121 |
| 7 — Reinforcing paths | Conditional driving mechanism, gain, limits and countervailing paths | I7-R36 | I7-T84–I7-T86, I7-T121 |
| 6 — Information | New versus tuned channels, actual receipt, meaning and adverse response | I7-R37 | I7-T87–I7-T89, I7-T121 |
| 5 — Rules | Institutional constraint, perceived rule, enforcement and amendment authority | I7-R38 | I7-T90–I7-T92, I7-T119 |
| 4 — Self-organization | Repertoire, variation, experimentation, selection, retention and resources | I7-R39 | I7-T93–I7-T95, I7-T119 |
| 3 — Goals | Local reference, attributed wider purpose, selection and adoption | I7-R40 | I7-T96–I7-T98, I7-T122 |
| 2 — Paradigms | Owned actor/community assumptions distinct from analyst framing and physics | I7-R41 | I7-T99–I7-T101, I7-T118, I7-T122 |
| 1 — Reconsidering paradigms | Explicit assumptions, alternatives, evidence, revision and qualified decision | I7-R42 | I7-T102–I7-T104, I7-T123–I7-T124 |

The order is retained as Meadows' tentative presentation, not used as an efficacy score. The twelve positions overlap, and a candidate may affect several. The architecture's operational treatment of the final position is an interpretation about revisability, not a claim to implement spiritual enlightenment.

### 39.5 KISS, first principles and retrospective method

**KISS:** keep nine shared representation families. Frame and intervention records are cross-cutting specifications referencing those families. Give a reserve, belief memory, cohort or capability separate state only when that state carries consequential independent history. Do not create a solver, universal gain, welfare score or world copy per chapter, trap or leverage position.

**Five Whys:** trace a disappointing result through the actual changed mechanism, actor response, enabling institution or physical condition, and supporting evidence. A fifth question does not guarantee a root cause. Consider multiple paths and stop with explicit unknowns where evidence is insufficient. Apply the same scrutiny to a proposed remedy's claimed beneficial direction.

**MECE:** maintain distinct meanings for physical/institutional, actual/perceived, capacity/reserve, cause/trigger, purpose/proxy, intent/realization, empirical/normative and observation/prediction. Do not force interacting traps or leverage categories into mutually exclusive bins. Their overlap is part of the system to explain.

**Requirements flow-down:** foundations → roles/functions → mechanism and interface contracts → cumulative requirements → prospective cases. The chain is traceability, not a one-pass waterfall claim about discovery. Any level can be revised when assumptions or evidence change.

**Sensitivity and alternatives:** compare operating point, parameter, rule, topology, history, drivers, information and frame explanations. Examine interacting interventions and changed horizons or stakeholders. These are specified assessments; this review has not executed numerical sensitivity analysis or identified empirical causal effects.

### 39.6 Historical six-chapter conceptual verdict

**Accept as the working Chapters 1–6 conceptual baseline after the listed repairs.** At the resolution of the retained source catalogue and chapter assessments, no unallocated foundation or unresolved semantic contradiction was found. All eight Chapter 5 traps, all twelve Chapter 6 positions, resilience, self-organization, hierarchy, nonlinear behavior, boundary revision, delays, bounded actor knowledge and evidence limitations have explicit allocations in one shared model.

Coverage is 278 catalogued source-review units over 150 requested body pages. These are our review units, not official primitives numbered by Meadows. Requirements comprise I7-R01–I7-R42. Scenarios comprise I7-T01–I7-T124: 68 retained integrated cases, 48 Chapter 6 cases and eight additional composition checks. Every scenario remains **PLANNED — NOT RUN**. The cases are not independent demonstrations and should not be counted as successful model executions.

This judgment does not prove a universally complete ontology, an exhaustive model of the world, a unique causal explanation or absence of unknown interfaces. A source anecdote remains a source report; a proposed mechanism, private mental state or paradigm remains evidence-qualified. The chapter source assessments are retained rather than falsely described as a new reading of all pages.

**Remaining qualification:** executable dynamics, empirical causal identification, prediction quality, intervention effectiveness, social adoption, actor psychology and implemented frame revision have not been established by document review. Runtime speed, energy, token use, availability, scalability and intelligence advantage are also unqualified. A complete-looking diagram and a consistent crosswalk do not establish those results.


## 40. Retained six-chapter record — Complete six-chapter foundation traceability

All 278 catalogued units have cumulative requirement and prospective-case allocation. The labels, source pages and detailed meanings are retained in sections 21–23, 32 and 36. Allocation specifies what a representation or future case should examine; it does not establish empirical confirmation.

| Foundation | Printed pages | Mechanism sections | Cumulative requirements | Prospective cases |
| --- | --- | --- | --- | --- |
| B01 | 11–13 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| B02 | 12–13, 18 | 4.2 | I7-R01 | I7-T01 |
| B03 | 11–13, 15 | 4.1, 7, 13.6 | I7-R01, I7-R09, I7-R17 | I7-T01, I7-T09, I7-T23, I7-T24 |
| B04 | 12 | 6.2–6.4 | I7-R06, I7-R07, I7-R09, I7-R10 | I7-T06, I7-T07, I7-T09, I7-T10 |
| B05 | 11, 13–14 | 4.4–4.6, 7 | I7-R02, I7-R04, I7-R09, I7-R16 | I7-T02, I7-T04, I7-T09, I7-T15, I7-T16, I7-T21 |
| B06 | 12–14 | 5.1 | I7-R11 | I7-T11, I7-T26, I7-T28 |
| B07 | 11, 14–15 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| B08 | 14–15 | 4.7, 5.1 | I7-R05, I7-R11 | I7-T05, I7-T11, I7-T26, I7-T27, I7-T28 |
| B09 | 15–16 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| B10 | 16 | 5.3 | I7-R01, I7-R14 | I7-T01, I7-T14 |
| B11 | 16–17 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| B12 | 17–18 | 4.3 | I7-R02, I7-R03 | I7-T02, I7-T03, I7-T15 |
| B13 | 18 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| B14 | 18–19 | 4.4 | I7-R02, I7-R04 | I7-T02, I7-T04, I7-T15, I7-T16 |
| B15 | 18, 22 | 4.1, 13.5 | I7-R01, I7-R17, I7-R18 | I7-T01, I7-T22, I7-T23, I7-T24 |
| B16 | 18–19 | 4.4, 7 | I7-R02, I7-R04, I7-R09 | I7-T02, I7-T04, I7-T09, I7-T15, I7-T16 |
| B17 | 20–22 | 6.1 | I7-R02, I7-R04, I7-R18 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T22 |
| B18 | 20–22 | 13.4 | I7-R02 | I7-T02, I7-T15 |
| B19 | 22 | 13.4 | I7-R02 | I7-T02, I7-T15 |
| B20 | 17, 23 | 5.2, 6.1 | I7-R02, I7-R03, I7-R04, I7-R18, I7-R19 | I7-T02, I7-T03, I7-T04, I7-T15, I7-T16, I7-T22, I7-T25 |
| B21 | 23–24 | 4.3, 8 | I7-R02, I7-R03, I7-R07 | I7-T02, I7-T03, I7-T07, I7-T15 |
| B22 | 19–22 | 4.9 | I7-R12 | I7-T12, I7-T27, I7-T28 |
| B23 | 14, 24–26 | 4.5–4.6 | I7-R04, I7-R15, I7-R16, I7-R20 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T20, I7-T21 |
| B24 | 25–27 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B25 | 27 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B26 | 18, 26 | 7 | I7-R09 | I7-T09 |
| B27 | 26–29 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| B28 | 27–30 | 4.8, 13.3 | I7-R04, I7-R05, I7-R12 | I7-T04, I7-T05, I7-T12, I7-T16, I7-T27, I7-T28 |
| B29 | 28–29 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| B30 | 27–28 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| B31 | 30 | 6.2, 7 | I7-R06, I7-R07, I7-R09 | I7-T06, I7-T07, I7-T09 |
| B32 | 30–33 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B33 | 31–33 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| B34 | 33–34 | 7 | I7-R09 | I7-T09 |
| B35 | 34 | 4.6, 4.8 | I7-R04, I7-R12, I7-R16 | I7-T04, I7-T12, I7-T16, I7-T21, I7-T27, I7-T28 |
| B36 | 20–22, 28–34 | 9, 14 | I7-R11, I7-R12, I7-R13 | I7-T11, I7-T12, I7-T13, I7-T26, I7-T27, I7-T28 |
| Z01 | 35 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z02 | 36–42 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| Z03 | 36–38 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| Z04 | 36–38 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z05 | 37–38 | 4.6, 14 | I7-R04, I7-R12, I7-R13, I7-R16 | I7-T04, I7-T12, I7-T13, I7-T16, I7-T21, I7-T27, I7-T28 |
| Z06 | 38–40 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| Z07 | 38–40 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| Z08 | 39 | 7, 13.1 | I7-R09, I7-R11 | I7-T09, I7-T11, I7-T26, I7-T28 |
| Z09 | 40–41 | 6.1 | I7-R02, I7-R04, I7-R18 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T22 |
| Z10 | 40–42, 44–45 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| Z11 | 42–45 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z12 | 44–47 | 4.6, 9 | I7-R04, I7-R11, I7-R12, I7-R16 | I7-T04, I7-T11, I7-T12, I7-T16, I7-T21, I7-T26, I7-T27, I7-T28 |
| Z13 | 45–47 | 4.9, 9 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| Z14 | 42–48 | 5.1, 13.1 | I7-R11 | I7-T11, I7-T26, I7-T28 |
| Z15 | 45–48 | 9 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| Z16 | 48 | 4.1, 9 | I7-R01, I7-R11, I7-R12, I7-R17 | I7-T01, I7-T11, I7-T12, I7-T23, I7-T24, I7-T26, I7-T27, I7-T28 |
| Z17 | 48–51 | 13.7 | I7-R13 | I7-T13 |
| Z18 | 49–50 | 4.2, 14 | I7-R01, I7-R12, I7-R13 | I7-T01, I7-T12, I7-T13, I7-T27, I7-T28 |
| Z19 | 50–51 | 7, 14 | I7-R09, I7-R12, I7-R13 | I7-T09, I7-T12, I7-T13, I7-T27, I7-T28 |
| Z20 | 51–53 | 8.1 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z21 | 52–55 | 5.2, 8.1 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z22 | 52–54 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z23 | 53–54 | 8.1, 13.2 | I7-R03, I7-R14, I7-R19 | I7-T03, I7-T14, I7-T25 |
| Z24 | 52–55 | 8.6 | I7-R12, I7-R19 | I7-T12, I7-T25, I7-T27, I7-T28 |
| Z25 | 55–57 | 8.6 | I7-R12, I7-R19 | I7-T12, I7-T25, I7-T27, I7-T28 |
| Z26 | 55–57 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| Z27 | 58 | 7 | I7-R09 | I7-T09 |
| Z28 | 58–60 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| Z29 | 60–62 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z30 | 61–62 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z31 | 61–64 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z32 | 63–64 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| Z33 | 64–66 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z34 | 65–66 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| Z35 | 66–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z36 | 66 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z37 | 66–67 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z38 | 67 | 4.6, 14 | I7-R04, I7-R12, I7-R13, I7-R16 | I7-T04, I7-T12, I7-T13, I7-T16, I7-T21, I7-T27, I7-T28 |
| Z39 | 68–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z40 | 69–71 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z41 | 71 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z42 | 71–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| F01 | 75 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| F02 | 75 | 4.2 | I7-R01 | I7-T01 |
| F03 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F04 | 76 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| F05 | 76 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| F06 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F07 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F08 | 76 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F09 | 77 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| F10 | 77–78 | 4.9 | I7-R12 | I7-T12, I7-T27, I7-T28 |
| F11 | 77–78 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| F12 | 78 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F13 | 79 | 6.3, 13.2 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F14 | 79–80 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F15 | 80 | 6.3–6.4 | I7-R08, I7-R09, I7-R10, I7-R14 | I7-T08, I7-T09, I7-T10, I7-T14 |
| F16 | 79–80 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F17 | 80 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F18 | 81 | 6.3, 12 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F19 | 80–81 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| F20 | 82 | 13.6 | I7-R01, I7-R09 | I7-T01, I7-T09 |
| F21 | 82 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F22 | 82–83 | 4.2, 14 | I7-R01, I7-R12, I7-R13 | I7-T01, I7-T12, I7-T13, I7-T27, I7-T28 |
| F23 | 83 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F24 | 83 | 4.5 | I7-R15, I7-R20 | I7-T17, I7-T18, I7-T19, I7-T20 |
| F25 | 83 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F26 | 83–84 | 4.1, 7 | I7-R01, I7-R09, I7-R17 | I7-T01, I7-T09, I7-T23, I7-T24 |
| F27 | 84 | 5.3, 9 | I7-R01, I7-R11, I7-R12, I7-R14 | I7-T01, I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| F28 | 84 | 6.3–6.4 | I7-R08, I7-R09, I7-R10, I7-R14 | I7-T08, I7-T09, I7-T10, I7-T14 |
| F29 | 84–85 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| F30 | 84–85 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| F31 | 85 | 6.4, 7 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F32 | 85 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| U01 | 86 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U02 | 86–87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U03 | 87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U04 | 87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U05 | 88 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U06 | 88 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U07 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U08 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U09 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U10 | 90 | 4.6, 9, 17 | I7-R04, I7-R11, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T11, I7-T12, I7-T16, I7-T21, I7-T22, I7-T25, I7-T26, I7-T27, I7-T28 |
| U11 | 91 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U12 | 91–92 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U13 | 92, 94 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U14 | 93 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U15 | 94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U16 | 93–94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U17 | 94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U18 | 93–94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U19 | 95 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U20 | 95 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U21 | 95–96 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U22 | 96 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U23 | 96–97 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U24 | 97 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U25 | 97–98 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U26 | 98 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U27 | 98–99 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U28 | 100–101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U29 | 101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U30 | 101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U31 | 102 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U32 | 102 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U33 | 102–103 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U34 | 103–104 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U35 | 103 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U36 | 104 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U37 | 104–105 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U38 | 105 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U39 | 106 | 4.5, 16 | I7-R15, I7-R20 | I7-T17, I7-T18, I7-T19, I7-T20 |
| U40 | 106 | 4.6, 16 | I7-R04, I7-R15, I7-R16 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T21 |
| U41 | 107 | 4.6, 16 | I7-R04, I7-R15, I7-R16 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T21 |
| U42 | 107–108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U43 | 106–108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U44 | 108, 110 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U45 | 108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U46 | 109 | 7, 16, 19 | I7-R09, I7-R15, I7-R20 | I7-T09, I7-T17, I7-T18, I7-T19, I7-T20 |
| U47 | 109 | 7, 16, 19 | I7-R09, I7-R15, I7-R20 | I7-T09, I7-T17, I7-T18, I7-T19, I7-T20 |
| U48 | 109–110 | 4.7, 9, 20 | I7-R05, I7-R11, I7-R12 | I7-T05, I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| C5-F01 | 111 | 22–28 | I7-R21 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F02 | 111–112 | 22–28 | I7-R21, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F03 | 112 | 22–28 | I7-R21 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F04 | 112 | 22–28 | I7-R28, I7-R30 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T60, I7-T62, I7-T63, I7-T64, I7-T66 |
| C5-F05 | 112–113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F06 | 113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F07 | 113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F08 | 113–114 | 22–28 | I7-R21, I7-R23, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F09 | 114–115 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F10 | 115–116 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F11 | 116–117 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F12 | 117–118 | 22–28 | I7-R22, I7-R30 | I7-T33, I7-T34, I7-T35, I7-T36, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F13 | 117–119 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F14 | 117–118 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F15 | 118 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F16 | 119 | 22–28 | I7-R22, I7-R28 | I7-T33, I7-T34, I7-T35, I7-T36, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F17 | 119–120 | 22–28 | I7-R21, I7-R22 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T33, I7-T34, I7-T35, I7-T36, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F18 | 119–121 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F19 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F20 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F21 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F22 | 122–123 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F23 | 123 | 22–28 | I7-R23, I7-R28 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T35, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F24 | 124 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F25 | 124–125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F26 | 125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F27 | 124–125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F28 | 125–126 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F29 | 125–126 | 22–28 | I7-R23, I7-R28 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T35, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F30 | 126–127 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F31 | 127 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F32 | 127–129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F33 | 128–129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F34 | 129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F35 | 129 | 22–28 | I7-R24, I7-R30 | I7-T45, I7-T46, I7-T47, I7-T48, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F36 | 129–130 | 22–28 | I7-R24, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T45, I7-T46, I7-T47, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F37 | 131–132 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F38 | 132–133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F39 | 132–133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F40 | 132–133 | 22–28 | I7-R21, I7-R25 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T49, I7-T50, I7-T51, I7-T52, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F41 | 133–135 | 22–28 | I7-R25, I7-R30 | I7-T49, I7-T50, I7-T51, I7-T52, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F42 | 133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F43 | 134–135 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F44 | 134–135 | 22–28 | I7-R25, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T49, I7-T50, I7-T51, I7-T52, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F45 | 136 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F46 | 136–137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F47 | 137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F48 | 137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F49 | 137 | 22–28 | I7-R26, I7-R27, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T63, I7-T64, I7-T66 |
| C5-F50 | 138 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F51 | 138–139 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F52 | 139–140 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F53 | 140 | 22–28 | I7-R26, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T63, I7-T64, I7-T66 |
| C5-F54 | 140–141 | 22–28 | I7-R21, I7-R26, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F55 | 141 | 22–28 | I7-R29 | I7-T65 |
| C5-F56 | 141 | 22–28 | I7-R28, I7-R29 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T65, I7-T66 |
| C6-F01 | 145–146 | 4, 32–39 | I7-R31 | I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F02 | 146–147 | 4, 32–39 | I7-R11, I7-R12, I7-R31 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F03 | 147 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F04 | 145–147 | 4, 32–39 | I7-R14, I7-R28, I7-R31 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F05 | 147–148 | 4, 32–39 | I7-R32 | I7-T69, I7-T70, I7-T71, I7-T105, I7-T120 |
| C6-F06 | 147 | 4, 32–39 | I7-R32 | I7-T69, I7-T70, I7-T71, I7-T105, I7-T120 |
| C6-F07 | 148 | 4, 32–39 | I7-R32 | I7-T69, I7-T70, I7-T71, I7-T105, I7-T120 |
| C6-F08 | 148 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R32 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T69, I7-T70, I7-T71, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F09 | 149 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R32 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T69, I7-T70, I7-T71, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F10 | 149–150 | 4, 32–39 | I7-R33 | I7-T72, I7-T73, I7-T74, I7-T117 |
| C6-F11 | 150 | 4, 32–39 | I7-R33 | I7-T72, I7-T73, I7-T74, I7-T117 |
| C6-F12 | 150 | 4, 32–39 | I7-R33 | I7-T72, I7-T73, I7-T74, I7-T117 |
| C6-F13 | 150 | 4, 32–39 | I7-R33 | I7-T72, I7-T73, I7-T74, I7-T117 |
| C6-F14 | 150 | 4, 32–39 | I7-R34 | I7-T75, I7-T76, I7-T77, I7-T109, I7-T117 |
| C6-F15 | 151 | 4, 32–39 | I7-R34 | I7-T75, I7-T76, I7-T77, I7-T109, I7-T117 |
| C6-F16 | 151 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R34 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T75, I7-T76, I7-T77, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T117, I7-T120, I7-T124 |
| C6-F17 | 151 | 4, 32–39 | I7-R34 | I7-T75, I7-T76, I7-T77, I7-T109, I7-T117 |
| C6-F18 | 151–152 | 4, 32–39 | I7-R35 | I7-T78, I7-T79, I7-T80, I7-T120 |
| C6-F19 | 152 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R35 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T78, I7-T79, I7-T80, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F20 | 152 | 4, 32–39 | I7-R35 | I7-T78, I7-T79, I7-T80, I7-T120 |
| C6-F21 | 152 | 4, 32–39 | I7-R35 | I7-T78, I7-T79, I7-T80, I7-T120 |
| C6-F22 | 152 | 4, 32–39 | I7-R35 | I7-T78, I7-T79, I7-T80, I7-T120 |
| C6-F23 | 153 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F24 | 153 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F25 | 153 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F26 | 153–154 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R36 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T121, I7-T124 |
| C6-F27 | 154–155 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F28 | 155 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F29 | 155–156 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F30 | 156 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F31 | 156 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F32 | 156–157 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R37 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T87, I7-T88, I7-T89, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T121, I7-T123, I7-T124 |
| C6-F33 | 157 | 4, 32–39 | I7-R37 | I7-T87, I7-T88, I7-T89, I7-T121, I7-T123 |
| C6-F34 | 157 | 4, 32–39 | I7-R37 | I7-T87, I7-T88, I7-T89, I7-T121, I7-T123 |
| C6-F35 | 157 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R37 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T87, I7-T88, I7-T89, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T121, I7-T123, I7-T124 |
| C6-F36 | 157 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R37 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T87, I7-T88, I7-T89, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T121, I7-T123, I7-T124 |
| C6-F37 | 158 | 4, 32–39 | I7-R38 | I7-T90, I7-T91, I7-T92, I7-T119, I7-T122 |
| C6-F38 | 158 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R38 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T90, I7-T91, I7-T92, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T119, I7-T120, I7-T122, I7-T124 |
| C6-F39 | 158 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R38 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T90, I7-T91, I7-T92, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T119, I7-T120, I7-T122, I7-T124 |
| C6-F40 | 158–159 | 4, 32–39 | I7-R38 | I7-T90, I7-T91, I7-T92, I7-T119, I7-T122 |
| C6-F41 | 159 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R39 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T93, I7-T94, I7-T95, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T119, I7-T120, I7-T124 |
| C6-F42 | 159 | 4, 32–39 | I7-R39 | I7-T93, I7-T94, I7-T95, I7-T119 |
| C6-F43 | 160 | 4, 32–39 | I7-R39 | I7-T93, I7-T94, I7-T95, I7-T119 |
| C6-F44 | 160 | 4, 32–39 | I7-R39 | I7-T93, I7-T94, I7-T95, I7-T119 |
| C6-F45 | 160–161 | 4, 32–39 | I7-R39 | I7-T93, I7-T94, I7-T95, I7-T119 |
| C6-F46 | 161 | 4, 32–39 | I7-R40 | I7-T96, I7-T97, I7-T98, I7-T119, I7-T122 |
| C6-F47 | 161 | 4, 32–39 | I7-R40 | I7-T96, I7-T97, I7-T98, I7-T119, I7-T122 |
| C6-F48 | 161–162 | 4, 32–39 | I7-R40 | I7-T96, I7-T97, I7-T98, I7-T119, I7-T122 |
| C6-F49 | 162 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R40 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T96, I7-T97, I7-T98, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T119, I7-T120, I7-T122, I7-T124 |
| C6-F50 | 162–163 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R41 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T99, I7-T100, I7-T101, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T122, I7-T123, I7-T124 |
| C6-F51 | 163 | 4, 32–39 | I7-R41 | I7-T99, I7-T100, I7-T101, I7-T118, I7-T122, I7-T123 |
| C6-F52 | 163 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R41 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T99, I7-T100, I7-T101, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T122, I7-T123, I7-T124 |
| C6-F53 | 163–164 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R41 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T99, I7-T100, I7-T101, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T122, I7-T123, I7-T124 |
| C6-F54 | 164 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R41 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T99, I7-T100, I7-T101, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T122, I7-T123, I7-T124 |
| C6-F55 | 164 | 4, 32–39 | I7-R42 | I7-T102, I7-T103, I7-T104, I7-T118, I7-T123, I7-T124 |
| C6-F56 | 164 | 4, 32–39 | I7-R42 | I7-T102, I7-T103, I7-T104, I7-T118, I7-T123, I7-T124 |
| C6-F57 | 164–165 | 4, 32–39 | I7-R42 | I7-T102, I7-T103, I7-T104, I7-T118, I7-T123, I7-T124 |
| C6-F58 | 164–165 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R42 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T102, I7-T103, I7-T104, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T123, I7-T124 |
| C6-F59 | 165 | 4, 32–39 | I7-R11, I7-R12, I7-R31 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F60 | 165 | 4, 32–39 | I7-R14, I7-R28, I7-R31 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F61 | 165 | 4, 32–39 | I7-R14, I7-R28, I7-R31 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F62 | 146–147, 165 | 4, 32–39 | I7-R11, I7-R12, I7-R31 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F63 | 147, 165 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31 | I7-T01, I7-T02, I7-T11, I7-T12, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T27, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F64 | 165 | 4, 32–39 | I7-R14, I7-R28, I7-R31 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |


## 41. Retained six-chapter record — Chapter 6 page ledger and complete source scope

Printed page labels map to PDF page plus 17. Each row records the material reviewed and its treatment; it does not claim that every source sentence is a separate architectural requirement.

| Printed | PDF | Reviewed content and architectural treatment |
| --- | --- | --- |
| 145 | 162 | Opening intervention question, leverage and wrong-direction warning; distinguish influence from desirable change |
| 146 | 163 | World and urban model examples, counterintuitive direction and absence of easy formulas; retain domain/source qualification |
| 147 | 164 | Tentative-list warning, coupled accounts and opening numerical parameters; no universal ranking |
| 148 | 165 | Parameter focus, personnel versus arrangement, short-term and individual importance; preserve scope and distribution |
| 149 | 166 | Critical-parameter exception, fairness-range anecdote and opening buffer comparison; permit exceptions and plural acceptable values |
| 150 | 167 | Buffer mechanisms, cost, flexibility and physical accessibility; topology and bottleneck examples |
| 151 | 168 | Rebuilding, cohorts, persistence, replacement and delay examples; carry inherited physical/temporal state |
| 152 | 169 | Relative delays, overreaction, irreversible thresholds and slowing driving change; avoid universal fastest-is-best rule |
| 153 | 170 | Complete balancing path, dormant emergency mechanisms and combined corrective capacity |
| 154 | 171 | Signals, externalized costs, governance influence and correction relative to disturbance; retain actual channels and capacities |
| 155 | 172 | Corrective-support examples and reinforcing paths; treat biological and nuclear illustrations as schematic, not technical laws |
| 156 | 173 | Reducing drivers, adaptation time, concentrated advantage and opening information-flow discussion |
| 157 | 174 | New feedback paths, population versus price signals, adverse disclosure and accountability; content and incentives differ |
| 158 | 175 | Rules, physical versus institutional constraints, amendment power and trade-system interpretation |
| 159 | 176 | Concentration consequences and self-organization through new structures, loops and rules; no costless technology assumption |
| 160 | 177 | Repertoires, variation, experimentation, selection, retention and diversity; conditional future potential |
| 161 | 178 | Suppressed diversity, local versus wider goals and purpose directing selection; avoid universal expansion motives |
| 162 | 179 | Authority and goal change; opening paradigm/fairness account; preserve mediated adoption and attribution |
| 163 | 180 | Unstated assumptions, differing frames and arrangements; distinguish interpretation, values and physical constraints |
| 164 | 181 | Individual versus social change, anomalies, modeling and philosophical transcendence; operationalize revisability cautiously |
| 165 | 182 | Philosophical continuation, tentative order, exceptions, resistance, accessibility and humility; no guaranteed recipe |

Chapter Six notes on pp. 206–207 identify eight references or acknowledgments: a newspaper account of IBM; Forrester's *World Dynamics* and *Urban Dynamics*; the rent-story acknowledgment; Dennis Meadows on commodity cycles; Galbraith; Emerson; and Kuhn. The note entries were reviewed; those underlying works were not independently reread or their findings replicated. The body was reviewed as extracted page text. Complete rendered-page geometry and numerical reconstruction of source figures are not claimed.



### 41.1 Complete requested body scope

| Chapter | Printed pages | PDF pages | Body pages | Catalogue units |
| --- | --- | --- | --- | --- |
| 1 — The Basics | 11–34 | 28–51 | 24 | 36 |
| 2 — A Brief Visit to the Systems Zoo | 35–72 | 52–89 | 38 | 42 |
| 3 — Why Systems Work So Well | 75–85 | 92–102 | 11 | 32 |
| 4 — Why Systems Surprise Us | 86–110 | 103–127 | 25 | 48 |
| 5 — System Traps and Opportunities | 111–141 | 128–158 | 31 | 56 |
| 6 — Leverage Points | 145–165 | 162–182 | 21 | 64 |
| Total | 11–72; 75–141; 145–165 | 28–89; 92–158; 162–182 | 150 | 278 |

The intervening unrequested pages and source notes are excluded from the body count. Prior source assessments and provenance remain part of the review trail. Rendered-page pixel coverage and numerical figure reproduction are not asserted.

## 42. Retained six-chapter record — Verification and qualification record

The checks for this cumulative document cover identifier uniqueness, canonical foundation allocation, legacy mapping, requirement-to-case allocation, valid parent references, table structure, one connected master graph, defined graph endpoints, preservation of prior master relationships, source-page offsets and no directed prediction-to-independent-source-record path. They do not execute the modeled dynamics, identify empirical mechanisms, validate paradigms or establish policy effectiveness. The conceptual verdict and its limits are in section 39.6.

**Document-check result, 20 October 2026: passed the specified consistency checks.** The single master diagram has 74 concepts and 202 named connections in one connected component, retaining all 67 concepts and 164 named connections of the prior master. All 278 source-review units have requirement and prospective-case allocations. The 42 requirement definitions and 124 scenario definitions have unique contiguous identifiers; the original 68 and Chapter 6's 48 scenario meanings are preserved. Graph endpoints, subgraph delimiters, table columns, fences, Chapter 6 page offsets and all twelve leverage-position allocations passed their checks. No directed path takes predicted trajectories into independent source-observation records. Counts describe the specification, not scientific completeness or successful model execution.


## 43. Chapter 7 integration: disciplined learning and participation

The opening (pp. 166–170) distinguishes understanding from implementation and asks unresolved questions about attention, values, cultural framing, fear of change and perceived agency. It advocates responsive participation rather than complete prediction and control. These questions are not solved psychological mechanisms. We interpret the warning as a limit on omniscience, not a proof that every nonlinear system defeats every bounded forecast or controller. The list is acknowledged by the source as incomplete.

The three process distinctions are integrated into sections 3–6, rather than placed only in an appendix. Important unmeasured concerns are retained, but ethical attribution, measurement and causation remain different questions. Chapter 7 practices are not fifteen physical components or a universal learning algorithm.

### 43.1 Fifteen source practices and their integrated roles

| Source practice | Printed pages | Role in the proposed extension |
| --- | --- | --- |
| Get the Beat of the System | 170–172 | Establish observed histories, timing, variability, strengths and alternative behavior before privileging a remedy |
| Expose Your Mental Models to the Light of Day | 172 | Make assumptions, mechanisms, unknowns and rivals inspectable and challengeable |
| Honor, Respect, and Distribute Information | 173 | Preserve meaning, provenance, accuracy, timeliness and appropriate receipt |
| Use Language with Care and Enrich It with Systems Concepts | 174–175 | Define referents and variable meanings; distinguish labels, claims and actual communication effects |
| Pay Attention to What Is Important, Not Just What Is Quantifiable | 175–177 | Retain qualitative concerns, attributed values and uncertainty instead of equating absence of a number with absence of an effect |
| Make Feedback Policies for Feedback Systems | 177–178 | Separate state-dependent response from monitoring-based revision of the response mechanism |
| Go for the Good of the Whole | 178 | Assess local and wider consequences with explicit boundaries and stakeholder criteria |
| Listen to the Wisdom of the System | 178–179 | Identify existing self-maintenance and support useful capability rather than automatically replacing it |
| Locate Responsibility in the System | 179–180 | Trace decision influence, consequence incidence, feedback, authority and capacity to respond |
| Stay Humble—Stay a Learner | 180–181 | Record expectations, errors, uncertainty, experiments and justified revisions |
| Celebrate Complexity | 181–182 | Permit transients, nonlinearity, diversity and reorganization without forcing uniformity or equilibrium |
| Expand Time Horizons | 182–183 | Evaluate short and long effects together, including coupling among different time scales |
| Defy the Disciplines | 183 | Integrate problem-relevant domain accounts through explicit meaning and mechanism correspondence |
| Expand the Boundary of Caring | 184 | Distinguish who is causally included, who is affected and whose interests count in evaluation |
| Don't Erode the Goal of Goodness | 184–185 | Distinguish actual improvement from lowered standards and selectively weighted experience; preserve the understanding–implementation gap |

The practices overlap deliberately. Information quality affects history, learning, accountability and values. Longer horizons affect the apparent merits of a policy. A shared glossary can expose incompatible assumptions across disciplines. These relationships should be integrated, not separated into independent world copies.

### 43.2 Detailed source assessment

#### 43.2.1 Get the Beat of the System, pp. 170–172

**Source contribution.** Observe behavior and learn its history before intervening. The chapter contrasts remembered narratives with time graphs, a change in average conditions with a change in variability, and multiple-variable histories with a static problem label. It also asks what is working and which other behavior modes are possible. A problem should not simply be defined as the absence of a favorite solution.

**Representation.** Retain variables, units or qualitative meanings, event/state/rate/pattern distinctions, observation times, temporal coverage, reporting and aggregation. A history of rainfall may show greater extremes without a falling mean. Incomplete memory, a missing period or changed measurement must remain visible. Histories of different variables need compatible timing and aggregation before their co-variation is assessed.

**Mechanism inquiry.** Histories can suggest connections and challenge easy narratives, but co-variation does not establish causation. Lack of a simple plotted association also does not prove no delayed, conditional or confounded mechanism exists. The New Hampshire growth/tax example remains a source account, not a universal economic law.

**Development practice.** Separate the observed concern, stakeholder interpretation, candidate cause and proposed remedy. Compare levels, changes, variability, timing and possible regime transitions. Allow direct structural inspection as well; history-first is a useful practice, not a rule that evidence about known physical structure must be ignored. Observation itself may affect the system, so its procedure and visibility can matter.

#### 43.2.2 Expose Your Mental Models to the Light of Day, p. 172

**Source contribution.** Expressing a model with diagrams, equations, words or other explicit forms makes assumptions and inconsistencies inspectable. Invite challenge, collect alternative explanations and revise or discard unsupported accounts. A model is not the world, and attachment to a preferred explanation can obstruct learning.

**Representation.** Give claims and mechanisms identifiable versions, sources, scope, dependencies, unknowns, contradictory evidence and rival explanations. Record what a reviewer challenged and which claim changed. The retained source observations do not change merely because a hypothesis is revised. Qualitative models are legitimate; explicitness is not synonymous with numerical execution.

**Development practice.** Check whether the same referent, rate or assumption changes meaning between discussions. Require declared conversions and time windows. Assess whether a mechanism is absent, contradicted or simply unsupported. Preserve a useful hypothesis at an appropriate provisional status rather than promoting it because it is the only one currently available.

**Qualification.** The source's invitation to consider many models does not require equal confidence in every imaginable story. Candidates can differ in logical consistency, physical feasibility and evidential support. Exposing a model improves its challengeability; it does not prove completeness or truth.

#### 43.2.3 Honor, Respect, and Distribute Information, p. 173

**Source contribution.** Missing, late, biased or inaccurate information can undermine feedback. Producers and intermediaries influence what reaches decision makers. The chapter's Toxic Release Inventory account links public reporting with a reported reduction in emissions, explicitly qualifying the reduction as at least reported and presumed also real.

**Representation.** Separate physical condition, measurement, report, publication, receipt, attention and subsequent response. Preserve reporting scope, definition, source, availability time, possible bias and corrections. A published record is not proof that every intended recipient saw, trusted or understood it. Information distribution is a directed relationship, not an indiscriminate broadcast assumption.

**Development practice.** Test delays, filtering, inaccurate measurements and missing recipients. Inspect whether apparent improvement follows actual changed processes, a reporting change or other factors. Monitoring and its publication can affect behavior and therefore belong to the intervention model where consequential.

**Qualification.** The source's historical percentages and policy account are not a calibrated causal effect here. Its ethical appeal to information integrity is not a theorem that more disclosure always helps; Chapter 6's adverse-information cases still apply. A model can record a restricted or unavailable channel without fabricating its content.

#### 43.2.4 Use Language with Care and Enrich It with Systems Concepts, pp. 174–175

**Source contribution.** Language and measurement categories influence perception and action. Concrete, meaningful terms help preserve information, while euphemisms and empty abstractions can conceal effects. A richer systems vocabulary can make overlooked mechanisms discussable.

**Representation.** Each consequential term needs a referent or construct, context, definition, unit or qualitative meaning, aggregation, temporal meaning and uncertainty. Preserve source wording separately from an analyst's normalized label. Identical words can have different meanings across domains; different terms can refer to the same subject. Identity binding needs evidence rather than spelling alone.

**Mechanism distinction.** Renaming a node in the analyst's diagram need not alter anyone's behavior. Changing a message, indicator or institutional category received by actors can alter interpretation and choices through a modeled pathway. Do not give a new label magical causal power or assume that common vocabulary establishes common purpose.

**Qualification.** The quoted language theories and cultural examples are source perspectives, not proof that nonverbal thought is impossible or language wholly determines perception. The architecture supports multiple modalities and qualitative representations without claiming semantic neutrality or a universal vocabulary. A glossary should clarify the question, not replace evidence with more terminology.

#### 43.2.5 Pay Attention to What Is Important, Not Just What Is Quantifiable, pp. 175–177

**Source contribution.** Easily counted activity can displace important qualitative outcomes. The chapter describes including prejudice and its proposed relationship with performance through elicited judgments, rather than omitting it because measurement is difficult. It argues for attending to quality and values even when a convenient metric is unavailable.

**Representation.** Retain a concern's meaning, affected parties, attributed importance, observations or testimony, proposed mechanisms and uncertainties. It may be descriptive, ordinal, interval-scaled or unmeasured; these are different measurement claims. An elicited curve is a source-qualified hypothesis, not direct observation of a universal causal law.

**Development practice.** Compare a model excluding a consequential concern with one that includes it qualitatively or under declared measurement assumptions. Where numbers are used, document the scale and transformation of response functions, thresholds and uncertainty. Changing the numeric labels of an ordinal scale cannot license arbitrary cardinal arithmetic. Do not assume equal importance or force all values into money or a total welfare score.

**Qualification.** The particular prejudice–performance curve is not supplied or independently reproduced here. The source's broad statements about measuring values are interpreted as a warning against incomplete proxies, not a denial that specific aspects of well-being or fairness can sometimes be operationalized. Including a concern does not establish its magnitude, mechanism or normative priority.

#### 43.2.6 Make Feedback Policies for Feedback Systems, pp. 177–178

**Source contribution.** Policies can change their response with system conditions. Under uncertainty, monitoring and review can also change the policy or feedback structure itself. The Carter examples are proposals the text says were not adopted. The Montreal Protocol account illustrates monitoring and subsequent revision of targets and coverage.

**Three processes must remain distinct.** A fixed rule can generate changing action from changing observations. A monitoring-and-review arrangement can propose or implement changes to that rule. Separately, an analyst can revise the model used to explain either process. These are neither the same mechanism nor automatic evidence of general intelligence.

**Representation.** A feedback policy needs inputs available to its owner, response rule, reference, constraints, delay, authority and version. Its revision arrangement additionally needs monitoring variables, expected consequences, review timing, discrepancy or other trigger, candidate changes, decision authority, resources, adoption and carry-over. More monitoring does not itself supply a valid update rule.

**Development practice.** Compare static and state-dependent policies, then separately enable policy revision. Account for stale/noisy signals, delayed physical effects, existing commitments and changed conditions. A poorly designed adaptive policy can chase noise, select the wrong proxy or destabilize another loop. The source's preference for feedback policy is not a universal claim that every variable rule outperforms every fixed rule.

#### 43.2.7 Go for the Good of the Whole, p. 178

**Source contribution.** Local optimization can damage wider functioning. Hierarchy is presented as supporting lower-level functioning rather than serving the apex alone. The chapter broadens attention to system properties and questions optimization of an activity whose purpose is itself misguided.

**Representation.** Keep the inquiry boundary, causal exchanges, stakeholders, local purposes, wider criteria and omitted consequences explicit. A local output, an aggregate total and its distribution are different assessments. Resilience, diversity, growth, stability and sustainability can conflict; the source's list is not a directive to maximize all simultaneously.

**Development practice.** Assess neighboring subsystems, shared resources, delayed dependencies and changed constraints. Ask whether the objective is useful before fine-tuning its achievement. Include both benefits of coordination and costs of excessive control. Widen a view when consequential interfaces justify it, then update its external-input closure.

**Qualification.** There is no automatically known global welfare function. A wider model can remain partial and contested. The phrase whole system supplies neither a natural final boundary nor authority to overrule every local concern. Larger graph size alone is not evidence of better understanding.

#### 43.2.8 Listen to the Wisdom of the System, pp. 178–179

**Source contribution.** Identify and support functioning self-maintenance before replacing it. The Guatemala market story contrasts imported solutions with attention to existing enterprise and locally identified obstacles.

**Representation.** Record existing corrective paths, working practices, local knowledge, access constraints, dependencies and condition. Distinguish capability, current output and externally supplied relief. A supporting intervention can strengthen local capacity or displace it; repeated help alone does not decide which occurred.

**Development practice.** Ask what already works, what obstructs it, which support it needs and which other parties depend on it. Compare removal, substitution, obstacle reduction and capability building. Track operating performance, recovery and future dependence over relevant horizons. Preserve observations from the people using the mechanism with their source status.

**Qualification.** Existing arrangements are not automatically wise, fair or sufficient. The source anecdote does not establish that outside investment is generally inferior to local finance or training. Its role is to challenge a presumed remedy and motivate discriminating local inquiry.

#### 43.2.9 Locate Responsibility in the System, pp. 179–180

**Source contribution.** In analysis, seek mechanisms that generate behavior rather than assigning everything to triggering events. In design, the chapter advocates returning consequences to decision makers quickly and compellingly. It discusses separated thermal-control decisions and several provocative accountability hypotheticals.

**Representation.** Distinguish causal influence, decision authority, information receipt, consequence incidence, capacity to respond and normative responsibility. A person may bear a consequence without having caused or controlled it. A decision maker can receive feedback but lack the resources or authority to act. Different directed relationships need their own contracts.

**Development practice.** Trace decision → actual process → consequences → perceived feedback → feasible response. Compare direct and mediated control, distribution of burdens, delays and local/wider criteria. A more local decision can improve responsiveness or create externalities; centralization and decentralization are conditional alternatives, not automatic verdicts.

**Qualification.** The medical-cost, warfare and reproductive examples are source ethical hypotheticals, not policy recommendations adopted by this architecture. Do not infer moral or legal blame from a causal graph. Exposure to consequences can be unjust or counterproductive; legitimacy and affected-party perspectives remain explicit.

#### 43.2.10 Stay Humble—Stay a Learner, pp. 180–181

**Source contribution.** Do not bluff or freeze when knowledge is incomplete. Learn through experience, monitored experiments, admission of error and willingness to change course. Uncertainty and failures should be communicable rather than hidden behind confidence.

**Representation.** Record what was expected, under which model and conditions, what was actually observed, the discrepancy, candidate explanations and the resulting update or unresolved status. Distinguish prediction error, measurement error, implementation failure, a changed driver and a changed mechanism. Error detection alone does not identify which account to revise.

**Development practice.** Define the question a proposed experiment could discriminate, the information it is expected to supply, implementation needs, monitoring timing and review conditions. Preserve the original forecast and observations after revision. Record why a policy is retained as well as why it changes. Small steps can still cross thresholds or accumulate harm; their scale is not a universal guarantee of benign effects.

**Qualification.** Trial and error is a practice, not a specified reinforcement-learning algorithm or proof that all useful learning requires intervention. Observation, inspection, testimony and analysis can also contribute. The source's confidence in openness improving trust remains a claim to investigate, not a guaranteed social effect.

#### 43.2.11 Celebrate Complexity, pp. 181–182

**Source contribution.** Transients, nonlinearity, diversity, self-organization and changing form are characteristic possibilities of the world. The chapter challenges a preference for neat equilibrium, uniformity and certainty, and includes an attributed land ethic.

**Representation.** Permit transient and cyclic regimes, heterogeneity, nonlinear response, multiple modes, changing coupling and actual reorganization. Retain the conditions under which a simpler approximation is useful. A heterogeneous system may contain temporarily simple or stable relations; complexity does not require every possible link to be active.

**Development practice.** Compare an approximation with the mechanisms it omits under the chosen question and horizon. Examine whether diversity provides alternatives or introduces dependencies and costs. Avoid deleting unusual states simply because the most familiar operating regime does not use them.

**Qualification.** Celebrating complexity is not a command to maximize graph size, disorder or model detail. The land ethic is an attributed evaluative perspective, not a scientific response law or a universally agreed objective. Keep description, usefulness and ethical preference distinct.

#### 43.2.12 Expand Time Horizons, pp. 182–183

**Source contribution.** Current action can have immediate and long-delayed consequences; present conditions can embody old commitments. Fast and slow processes can be coupled, with changing relative influence. The chapter calls for attention to both the next step and the distant future.

**Representation.** Separate physical time, observation cadence, planning horizon, stakeholder horizon, lifetime, lag and any discounting assumption. Preserve residual obligations and delayed effects beyond a convenient evaluation endpoint. A fast threshold crossing can matter to a long inquiry, while old slow processes can determine a short inquiry's initial condition.

**Development practice.** Compare short and long windows, peak versus averaged behavior, transition versus eventual outcome and alternative value-weighting assumptions. Keep important long-term outcomes visible even where their uncertainty is larger. Extending the horizon does not erase urgent current needs.

**Qualification.** The critique of interest and discounting is a normative and strategic argument, not a theorem that every discount rate is wrong. A longer horizon is not automatically an accurate forecast or a universally better decision. Historical cultural claims remain attributed rather than assigned to every community member.

#### 43.2.13 Defy the Disciplines, p. 183

**Source contribution.** Follow the problem across disciplinary boundaries and learn from other perspectives without treating jargon or professional identity as the boundary of the real system. Merely assembling specialists does not ensure integration.

**Representation.** Map domain terms to shared referents, quantity meanings, units, scales, boundaries, assumptions and proposed mechanisms. Retain disagreement and provenance. Identify where accounts concern the same process, a different aggregation or incompatible claims. A role analogy is not permission to transfer coefficients or causal findings.

**Development practice.** Start with a shared question and inspect points of interaction. Reconcile conversions, time windows and evidence dependencies before composing equations or conclusions. Seek missing knowledge where the model crosses into another field. Domain labels alone establish neither expertise nor error.

**Qualification.** Interdisciplinary openness is not a reason to treat every explanation as equally supported. A persuasive narrative with more disciplines can still be physically inconsistent, empirically weak or unnecessary for the question. The architecture should support useful integration and explicit unresolved differences.

#### 43.2.14 Expand the Boundary of Caring, p. 184

**Source contribution.** The chapter extends concern beyond immediate beneficiaries, emphasizing interdependence among people and ecological systems. It combines ethical reasons with practical arguments about linked functioning.

**Representation.** Distinguish the analytical boundary, causal reach, affected-party coverage and evaluative scope. An entity can be represented causally but excluded from the stated objective; an omitted party may still be affected. Record whose interests, times and outcomes are considered, by whom and with what disagreement.

**Development practice.** Trace distributed and delayed benefits, burdens, dependence and vulnerability. Ask which parties or ecological conditions disappear under aggregation and whether a local improvement shifts costs elsewhere. A proposed wider criterion can change a decision even when the physical dynamics remain the same.

**Qualification.** Systems relationships can reveal consequences but do not by themselves derive one compulsory moral weighting. The source's broad interdependence statements are not proof that every local failure immediately prevents every other success. Preserve causal timescales, degree of coupling and ethical attribution rather than using moral language as a substitute for a mechanism.

#### 43.2.15 Don't Erode the Goal of Goodness, pp. 184–185

**Source contribution.** The chapter applies drift to low performance to moral expectations: selective emphasis on bad examples can lower standards, reduce the gap and weaken action. It closes by returning to the difference between understanding and implementation, acknowledging the limits of analysis alone.

**Representation.** Keep observed conduct, selected reports, interpretation, normative reference, discrepancy and corrective action distinct. Record standard ownership, meaning, history and revision process. A shrinking discrepancy can result from lower aspiration instead of better outcomes. Moral standards and their conflicts are attributed, not presumed universally agreed.

**Development practice.** Preserve the full available evidence and examine selection bias; do not manufacture equal counts of good and bad reports. Compare genuine improvement, reference erosion, changed measurement and legitimate deliberative revision. Retain a reasoned standard while allowing transparent challenge to its meaning and applicability.

**Qualification.** The cultural diagnosis and quoted moral judgments are source perspectives, not calibrated population facts. The architecture does not prove an innate moral faculty or implement goodness by adding a scalar objective. It can expose standards, choices and effects; adoption and conduct require their own mechanisms and evidence.


## 44. Chapter 7 foundation catalogue

These 68 source-review units extend the retained 278. Their design implications are our synthesis; allocation to cumulative contracts is in section 50.

| Foundation | Printed pages | Source contribution | Proposed modeling consequence |
| --- | --- | --- | --- |
| C7-F01 | 166–169 | Systems understanding is not a key to unrestricted exact prediction and control. | Specify conditional prediction, applicability and limits rather than omniscience. |
| C7-F02 | 167 | Understanding a remedy and implementing it are different accomplishments. | Keep explanation, recommendation, adoption and actual effect distinct. |
| C7-F03 | 168–169 | People can resist, ignore or interpret the same information differently. | Specify receipt, attention, interpretation and unknown psychological mechanisms. |
| C7-F04 | 168–169 | Values, fear, culture and perceived power affect proposed change. | Attribute relevant beliefs and constraints; do not assume rational agreement from a model conclusion. |
| C7-F05 | 169–170 | Responsive participation can use feedback and learn from surprise. | Represent conditional action, monitoring and revisability without promising control of every outcome. |
| C7-F06 | 170 | The practice list is incomplete and not unique to systems thinking. | Use it as source guidance, not an exhaustive algorithm or ontology. |
| C7-F07 | 170–171 | Observe behavior and learn system history before privileging intervention. | Retain measured histories and testimony with their different evidential status. |
| C7-F08 | 171 | A change in variability can be confused with a change in average level. | Distinguish level, rate, variance/extremes, aggregation and measurement coverage. |
| C7-F09 | 171 | Histories of several variables can challenge causal stories and suggest connections. | Compare aligned variables while withholding causal identification from co-variation alone. |
| C7-F10 | 171–172 | Define the problem from behavior, not from the absence of a favorite remedy. | Separate observed concern, candidate explanation and proposed action. |
| C7-F11 | 172 | Explicit diagrams, equations or other representations expose assumptions and inconsistencies. | Use versioned, inspectable claims with coherent meanings and accounting. |
| C7-F12 | 172 | Models may be expressed in words, lists or pictures as well as mathematics. | Allow useful qualitative descriptions without invented numerical precision. |
| C7-F13 | 172 | Challenge and alternative models support flexibility. | Retain rival explanations, unknowns and differences in evidential support. |
| C7-F14 | 172 | Unsupported models should be corrected or rejected using evidence. | Preserve observations and original claims while recording revision rationale. |
| C7-F15 | 173 | Biased, missing, inaccurate or delayed information can undermine response. | Separate source condition, measurement, delivery, interpretation and action. |
| C7-F16 | 173 | The emissions example distinguishes reported reduction from presumed physical reduction. | Retain reporting scope, measurement alternatives and unverified causal status. |
| C7-F17 | 173 | Information producers and intermediaries can filter and channel what others receive. | Model directed access, transformations, timing and control over channels. |
| C7-F18 | 173 | Publication can change behavior and is itself consequential. | Distinguish passive retention from actor-visible reporting intervention. |
| C7-F19 | 174 | Language and categories can structure perceived possibilities and action. | Specify a mediated interpretation pathway rather than causal power from a label alone. |
| C7-F20 | 174–175 | Concrete, meaningful and truthful terms preserve informative communication. | Define referent, construct, scope, quantity meaning and source wording. |
| C7-F21 | 175 | Systems vocabulary can make complexity discussable. | Support precise terms without treating jargon as demonstrated understanding. |
| C7-F22 | 174–175 | Measurement and communication arrangements are not neutral by default. | Compare analyst renaming with changes in messages or categories actually received by actors. |
| C7-F23 | 175–176 | Easy quantification does not determine importance. | Retain consequential qualitative concerns and attributed priority. |
| C7-F24 | 176 | The source includes elicited relationships for difficult-to-measure constructs. | Distinguish testimony and assumed response curves from calibrated observations. |
| C7-F25 | 176 | A numerical scale can be conventional without removing the proposed phenomenon. | Specify measurement level and compatible transformations; do not infer cardinal precision from ordinal labels. |
| C7-F26 | 176–177 | Qualities and values warrant attention even without a convenient measurement. | Keep qualitative criteria, disagreement and uncertainty visible. |
| C7-F27 | 177 | Feedback policies can change their response with observed conditions. | Represent available inputs, policy rule, reference, constraints and time. |
| C7-F28 | 177–178 | Meta-feedback can alter, correct or expand a feedback policy. | Specify policy review separately from state-dependent action under a fixed rule. |
| C7-F29 | 177–178 | Monitoring and reconvened review can revise targets and coverage. | Record observation, trigger, authority, adopted version and retained commitments. |
| C7-F30 | 177 | The Carter examples are proposals reported as not adopted. | A described policy is not evidence of actual implementation or its effect. |
| C7-F31 | 178 | Optimizing a subsystem can neglect the wider system. | Evaluate cross-system effects, shared constraints and distribution. |
| C7-F32 | 178 | Hierarchy is presented as serving lower-level functioning. | Attribute coordination purposes and examine effects on local capability. |
| C7-F33 | 178 | Multiple system properties matter beyond easily measured output. | Retain distinct criteria and possible tradeoffs rather than maximizing every property simultaneously. |
| C7-F34 | 178 | The activity and objective themselves may need scrutiny before optimization. | Question purpose and proxy before tuning a response. |
| C7-F35 | 178 | Existing self-maintenance should be identified and supported. | Represent corrective paths and their condition before substitution. |
| C7-F36 | 178–179 | Useful capability and knowledge can reside locally. | Keep local participants, practices and information as potential evidence. |
| C7-F37 | 178–179 | Consulting existing participants can reveal obstacles missed by imported solutions. | Retain testimony, alternatives and source-qualified interpretations. |
| C7-F38 | 179 | Removing obstacles or strengthening capability can differ from external takeover. | Compare support, substitution and capacity effects without presuming one universal winner. |
| C7-F39 | 179 | Behavior arises from system mechanisms as well as external triggers. | Distinguish generating structure, trigger, susceptibility and boundary drivers. |
| C7-F40 | 179 | Intrinsic responsibility returns consequences to decision makers in an effective form. | Trace decision, effect, incidence, perception and feasible response. |
| C7-F41 | 179 | Mediated control can introduce delay and overcorrection. | Compare actual authority, local information, response timing and wider effects. |
| C7-F42 | 179–180 | Accountability examples connect decision influence with consequence exposure. | Keep causal role, burden, agency and normative responsibility distinct. |
| C7-F43 | 180 | Incomplete knowledge calls for learning rather than bluffing or freezing. | Allow explicit uncertainty and provisional action. |
| C7-F44 | 180 | Small steps, monitoring and course correction are advocated. | Specify discriminating inquiry and revision while retaining threshold and cumulative effects. |
| C7-F45 | 180–181 | Admitting error enables learning. | Preserve original expectations, observations, discrepancy and alternative error explanations. |
| C7-F46 | 181 | Sharing uncertainty and failure is part of the source practice. | Make review and correction inspectable without asserting guaranteed trust or improvement. |
| C7-F47 | 181 | Transient behavior need not be a defect relative to a fixed equilibrium. | Allow functioning regimes and history-dependent change. |
| C7-F48 | 181–182 | Nonlinearity, self-organization and changing form are relevant possibilities. | Preserve applicability, thresholds and actual organizing mechanisms. |
| C7-F49 | 181–182 | Diversity and uniformity both occur in systems. | Represent heterogeneity and conditional simplification rather than compulsory complexity. |
| C7-F50 | 182 | The land ethic is an attributed moral perspective. | Separate ethical criteria from descriptive dynamics and universal claims. |
| C7-F51 | 182 | Short evaluation horizons and discounting can hide distant consequences. | Expose planning horizon and value-weighting assumptions. |
| C7-F52 | 183 | Present state can embody actions and commitments initiated long ago. | Preserve relevant slow state, prehistory and pending effects. |
| C7-F53 | 183 | Fast and slow processes interact with changing relative influence. | Assess multiple time scales and consequences of aggregation. |
| C7-F54 | 183 | Both immediate conditions and distant effects need attention. | Do not equate a longer horizon with ignoring urgent current needs or knowing the future. |
| C7-F55 | 183 | Real system questions cross disciplinary boundaries. | Follow relevant interfaces beyond institutional or academic categories. |
| C7-F56 | 183 | Jargon and narrow lenses can obstruct integration. | Map referents, units, scales, assumptions and mechanisms explicitly. |
| C7-F57 | 183 | A shared problem and willingness to learn support meaningful integration. | Record the question, contribution, disagreement and evidence rather than merely assembling accounts. |
| C7-F58 | 183 | No single professional lens supplies the whole explanation. | Retain scope limitations without treating all explanations as equally supported. |
| C7-F59 | 184 | The chapter advocates widening ethical concern as well as analysis. | Record whose interests count, for which decision and horizon. |
| C7-F60 | 184 | Linked people and ecological conditions create practical interdependencies. | Trace actual degree, timing and direction of coupled effects. |
| C7-F61 | 184 | Local success can depend on conditions experienced by other parties. | Preserve distributed consequences and omitted stakeholders. |
| C7-F62 | 184 | Ethical and practical reasons are combined in the source argument. | Distinguish causal inclusion, affected-party coverage and normative weighting. |
| C7-F63 | 184 | Selective emphasis on bad examples can lower moral expectations. | Preserve reporting/selection mechanisms and reference history. |
| C7-F64 | 184 | Lower standards shrink discrepancy and weaken corrective action. | Distinguish reference erosion from actual performance improvement. |
| C7-F65 | 185 | The proposed response is to avoid biased weighting and maintain standards. | Retain attributed ideals without manufacturing balanced evidence or forbidding reasoned revision. |
| C7-F66 | 184–185 | Normative goals can themselves be subject to drift. | Record standard ownership, conflicts, revision rationale and actual conduct. |
| C7-F67 | 185 | Systems thinking alone does not bridge understanding and implementation. | Do not claim that an explicit model guarantees adoption, learning or moral behavior. |
| C7-F68 | 170, 185 | The chapter frames practice as involving judgment and values beyond calculation alone. | Keep evaluative choices and implementation limits explicit rather than claiming an automatic moral algorithm. |



## 45. Integrated meaning, concern, error and policy records

### 45.1 Meaning, history and evidence record

| Field group | Required meaning |
| --- | --- |
| Referent and construct | Persistent subject, variable role, source term, normalized term and definition; distinguish synonyms from shared identity claims |
| Measurement meaning | Unit or qualitative scale, permissible operations, calibration or elicitation status and uncertainty |
| Temporal meaning | Occurrence, observation, reporting, availability and aggregation times; cadence, gaps, changed definitions and coverage |
| Provenance | Observation/report source, dependencies among reports, transformations, corrections and conflict |
| Applicability | Context, domain, operating range, known exclusions and unresolved interpretation |
| Comparison correspondence | Referents, quantities, units, scale transformations, aggregation and time alignment across sources, models or disciplines |

Data integrity does not require accepting every source as accurate. Preserve the original account and any correction, then qualify the claim. A model variable's definition must not silently change to make a prediction look right. A qualitative report remains usable even when cardinal arithmetic is unjustified.

### 45.2 Qualitative concern and coverage record

| Field group | Required meaning |
| --- | --- |
| Concern and holder | What matters, to whom, at which system level and over what horizon |
| Evidence and proposed effects | Observations, testimony, mechanism hypotheses, uncertainty and alternatives; value attribution distinct from empirical belief |
| Assessment form | Narrative, category, ordinal assessment, interval/ratio measurement or unresolved construct; proposed conversions are explicit |
| Evaluation role | Desired outcome, constraint, warning, disputed priority or other criterion; no compulsory aggregate welfare score |
| Coverage | Causally represented subjects, affected parties, evaluated parties, omitted consequences and rationale |
| Reference history | Original and current standards, ownership, change procedure and evidence for improvement or erosion |

An important concern is not assigned zero impact because no reliable coefficient exists. Conversely, importance alone does not prove a causal effect. Ethical inclusion, measurement and causal representation are different questions.

### 45.3 Expectation, error and learning-decision record

| Field group | Required meaning |
| --- | --- |
| Context and owner | Analyst or represented actor; decision question, information actually available and applicable authority |
| Original expectation | Hypothesis/model/policy version, conditions, expected outcome or qualitative implication, time and stated uncertainty |
| New evidence | Independent observation or source report with correspondence to the expectation; not recycled prediction |
| Discrepancy | What differed, including missing observation, noisy measurement, implementation failure, changed conditions or unexplained behavior |
| Alternatives | Competing error explanations and potentially discriminating observations; retain unresolved causes |
| Review decision | Retain, revise, reject, investigate or defer; specify the affected claim, rule, boundary or criterion and rationale |
| Adoption and consequences | Proposal versus implemented update, authority, resources, time, state/history carry-over and later outcome evidence |
| Audit trail | Preserve original expectation, observation, update and changed version without rewriting the past |

The record makes learning inspectable. Its existence does not demonstrate that the system can generate explanations, choose useful experiments or update competently. Those are separate capabilities to instantiate and test.

### 45.4 Feedback-policy and policy-revision contract

A possible formal distinction is:

\[
a_i^{\mathrm{intent}}(t)=\pi_i^{v}(z_i(t),g_i(t)),\qquad
f(t)=F(x(t),m(t),u(t),a^{\mathrm{intent}}(t);G,\theta).
\]

Here z_i denotes the actor's available interpreted information and relevant internal condition. A fixed policy version v can produce varying actions. Actual effects f remain constrained by the specified world mechanisms and shared resources.

A separate proposed review process can produce:

\[
\widetilde\pi_i^{v+1}=U_i(\pi_i^v,\mathcal E_i,\mathcal C_i),
\]

where E_i is evidence available to the reviewer and C_i its declared review criteria and constraints. U_i is a particular candidate mechanism, not an algorithm supplied by the chapter. Proposal is not adoption; an implementation process must determine whether and when the new version is used. An unknown U_i remains unknown. The analyst's model revision is another separate process.

Specify monitoring variables, meaning, cadence, completeness and recipients; policy expectations; review time or trigger; changes the reviewer may propose; amendment authority; practical resources; adoption; and carry-over of old commitments. A new ordering policy does not cancel in-flight orders by default. More frequent review is not inherently more useful, and a changing policy is not inherently better.

## 46. Detailed directed integration review

The core contracts in section 7 and retained reviews in sections 24, 28.3, 34 and 39.3 remain binding. This table checks both directions where meaningful and declares when a return direction needs a distinct mechanism. The existence of A→B does not imply B→A, symmetry, equal delay or a closed feedback loop.

| Forward direction | Forward contract | Return direction or question | Return contract / integration risk | Prospective cases |
| --- | --- | --- | --- | --- |
| History → explanation | Evidence on mean, variability, timing, regime and measured structure | Explanation → inquiry requests | Explicit rival hypotheses and discriminating observations; no rewritten source | I7-T125–I7-T130, I7-T191 |
| Source/report → recipient | Meaning, transformation, availability, receipt and attention | Recipient → information channel | Questions or requests only if a return path is specified; no broadcast assumption | I7-T131–I7-T136, I7-T177 |
| Domain account → shared description | Referents, units, scales, aggregation, times and assumptions | Shared description → domain review | Identify contradictions and missing knowledge; never silently overwrite a specialist source | I7-T161–I7-T163, I7-T187 |
| Current policy → action/execution | Versioned rule and available input; shared actual constraints | Outcome → ordinary response | Sensing, receipt and interpreted state, distinct from policy amendment | I7-T140–I7-T142, I7-T172 |
| Monitoring → policy review | Owned expectations, received observations, discrepancy and unresolved error causes | Policy review → monitoring | Changed sampling or questions are proposals requiring authority/resources if consequential | I7-T142, I7-T172–I7-T173, I7-T185 |
| Review proposal → adoption | Allowed changes, decision rights, resources, opposition and timing | Adoption → review/current policy | Implemented version or refusal/deferral with preserved history; no instant obedience | I7-T170–I7-T173, I7-T178, I7-T185 |
| Analyst model → prediction | Version, conditions, declared uncertainty and horizon | Evidence comparison → model revision | Retain original expectation and alternative causes; no automatic actor-policy change | I7-T152–I7-T154, I7-T173–I7-T176, I7-T191 |
| Qualitative concern → evaluation | Meaning, holder, measurement level, uncertain effects and omitted parties | Evaluation → concern review | Disagreement, further inquiry or reasoned criterion revision; not manufactured precision | I7-T137–I7-T139, I7-T179, I7-T187 |
| Decision → consequences | Actual influence and timing; distributed burden/benefit incidence | Consequences → decision maker | Real receipt, interpretation, authority and capacity; no inference of blame from exposure | I7-T149–I7-T151, I7-T186, I7-T190 |
| External support → local correction | Shared resources, replacement or assistance, condition and recovery | Local capability → support decision | Existing practice and testimony via received information; support can build or displace | I7-T146–I7-T148, I7-T188, I7-T192 |
| View expansion → causal closure | Shared referents; replace/condition formerly external inputs | Consequences → evaluative coverage | Affected parties may extend beyond modeled boundary; inclusion does not settle moral weighting | I7-T164–I7-T166, I7-T180, I7-T186 |
| Reference update → action/evaluation | Owner, old/new meaning, evidence and legitimate revision procedure | Outcome/report → reference update | Selection bias, erosion and actual improvement separated | I7-T167–I7-T169, I7-T181, I7-T188 |
| Fast processes → slow commitments | Coupled rates, thresholds and actual pending effects | Slow state → current response | Inherited capacity, cohorts and obligations; explicit evaluation endpoint and weighting | I7-T158–I7-T160, I7-T178, I7-T189 |
| Ordinary response ↔ review ↔ model revision | Shared sensors, resources and identity without shared omniscience | Indirect/common dependency review | A failed sensor or depleted support can affect several loops; successful local output is insufficient | I7-T185, I7-T191, I7-T192 |

### 46.1 Pairwise completeness and meaningful absences

The retrospective reviewed each unordered pair among twelve conceptual groups: scope/criteria; organization/interfaces; physical dynamics; actor information/action; restoration/support; real organizational change; governance/adoption; frames/meaning; evidence; scenario analysis; analyst assessment; and policy review. That is **66 pairs and 132 directional questions**, including within-group ownership and common dependencies separately. These are schema review positions, not 132 discovered physical connections. The pair ledger below records both directional dispositions and the contract that governs them.

Included means a typed relationship is available in the schema, not that it is active in every instance. Indirect means existing intermediary paths suffice; no new direct arrow is warranted. Instance-specific means the schema requires a decision with evidence; it is not an asserted absence. Prohibited means the proposed shortcut would violate ownership, evidence or change-status invariants.

| Pair | First → second | Second → first | Key restriction |
| --- | --- | --- | --- |
| Scope/criteria ↔ Organization/interfaces | Select included constituents and levels | Expose consequential omitted memberships/interfaces | A view change is not physical reorganization |
| Scope/criteria ↔ Physical dynamics | Declare boundary inputs, quantities and relevant horizons | Expose coupled sources/sinks and physical limits | Replace or condition formerly external driver closure |
| Scope/criteria ↔ Actor information/action | Attribute inquiry perspectives and actor-specific criteria | Expose differing local goals, access and intended actions | Analyst criteria do not become actor goals automatically |
| Scope/criteria ↔ Restoration/support | Define functioning and disturbances used to assess recovery | Expose local capability and common support dependencies | No universal resilience score or fixed equilibrium |
| Scope/criteria ↔ Real organization change | Scope relevant organization changes and transition criteria | Expose changed memberships/coupling requiring another view | Real change and analyst boundary revision stay separate |
| Scope/criteria ↔ Governance/adoption | Specify intervention question, criteria and affected interests | Identify jurisdiction, authority and practical adoption limits | The inquiry does not grant amendment rights |
| Scope/criteria ↔ Frames/meaning | Declare analyst frames, terms and evaluative assumptions | Reveal alternative interpretations and contested boundaries | Actor/community framing separately attributed |
| Scope/criteria ↔ Evidence | Specify evidence questions, history and coverage needed | Challenge scope through missing or conflicting source accounts | Omissions remain explicit; no completeness claim from graph size |
| Scope/criteria ↔ Scenario analysis | Select question, horizon, criteria and boundary closure | Reveal scenario sensitivity and consequential omitted effects | Scenario-selected conditions are not observed facts |
| Scope/criteria ↔ Analyst assessment | Supply criteria and adequacy question | Recommend justified scope/criterion reconsideration | Evaluation disagreement need not disappear with more data |
| Scope/criteria ↔ Policy review | Describe owner-specific review scope and horizons | Expose the reviewers actual decision domain and blind spots | Analyst scope does not supply actor monitoring knowledge |
| Organization/interfaces ↔ Physical dynamics | Interfaces carry shared transfers and signals | Rates, stock conditions and limits affect operating capability | Composition does not duplicate stock or shared flow capacity |
| Organization/interfaces ↔ Actor information/action | Channels, roles and coordination shape received information and execution | Actor work may alter interfaces through realized processes | Part-of membership does not imply knowledge or command |
| Organization/interfaces ↔ Restoration/support | Constituent/interface condition enables restoration and repair | Repair may restore shared condition and local functioning | Common support failure can defeat several alternatives |
| Organization/interfaces ↔ Real organization change | Existing organization constrains permitted generation/retention | Actual transition changes memberships, interfaces and coordination | Preserve identity and retained state across the change |
| Organization/interfaces ↔ Governance/adoption | Institutions expose actual jurisdiction and communication routes | Adopted rules can change permissions or organization | Formal announcement is not effective implementation |
| Organization/interfaces ↔ Frames/meaning | Describe terms and attributed roles in their context | Owned interpretation may affect structure only through action/adoption | Analyst renaming alone creates no physical or social change |
| Organization/interfaces ↔ Evidence | Actual organization can be inspected/reported through observation | Evidence supports or challenges its versioned description | Reports are not the constituents they describe |
| Organization/interfaces ↔ Scenario analysis | Describe topology and boundary correspondence for scenarios | Analyze hypothetical topology/organization transitions | A simulated new interface is not a built connection |
| Organization/interfaces ↔ Analyst assessment | Supply dependencies and organization claims for assessment | Revise the description or propose an intervention | Assessment changes actual organization only through adoption |
| Organization/interfaces ↔ Policy review | Channels, roles and reviewer location constrain monitoring | Adopted review output may change a shared interface | A review role is not automatically a new centralized controller |
| Physical dynamics ↔ Actor information/action | Conditions reach actors through sensing; actual limits constrain execution | Realized actions affect shared rates or conditions | Hidden physical limits must not oracle-filter perceived options |
| Physical dynamics ↔ Restoration/support | Material/resources and disturbances constrain repair | Repair changes condition and may consume shared stocks | Gross transfers and repair competition count once |
| Physical dynamics ↔ Real organization change | Stocks, capacity and pending state constrain generation | Actual new structure changes subsequent physical mechanisms | No conservation reset, free capacity or erased commitment |
| Physical dynamics ↔ Governance/adoption | Resources and physical laws limit implementation | Realized enforcement/implementation may change process access | An institution cannot repeal physical accounting |
| Physical dynamics ↔ Frames/meaning | Observed conditions may inform an owned frame via sensing | Meaning shapes actual action through interpretation and mediation | Beliefs do not directly create material or change physical laws |
| Physical dynamics ↔ Evidence | Measured/inspected conditions produce source observations | Evidence revises the physical model description | Writing a record alone does not alter the physical quantity |
| Physical dynamics ↔ Scenario analysis | Specify candidate laws, state and conditional external drivers | Compute or reason about hypothetical trajectories | Prediction is not independent evidence of the actual process |
| Physical dynamics ↔ Analyst assessment | Supply accounting, mechanisms and conditions to assess | Identify model inadequacy or proposed corrective change | A consistency finding is not empirical causal identification |
| Physical dynamics ↔ Policy review | Physical effects may reach monitoring through declared channels | Adopted policy changes realized action and later physical effects | No policy update cancels in-flight physical effects by default |
| Actor information/action ↔ Restoration/support | Received condition can initiate finite repair or support | Recovered sensing/actuation alters feasible response | Need, knowledge, authorization and ability are different |
| Actor information/action ↔ Real organization change | Actual choices may initiate variation or organizational action | Changed organization affects information, options and execution | Permission to try is not retained useful innovation |
| Actor information/action ↔ Governance/adoption | Actor proposals, compliance and influence affect governance where specified | Communicated rules shape choice; actual enforcement shapes realization | Unknown enforcement affects realization without prior actor knowledge |
| Actor information/action ↔ Frames/meaning | Available experience may alter owned interpretation through a specified process | Owned frame influences interpreted possibilities and goals | No automatic convergence of heterogeneous beliefs |
| Actor information/action ↔ Evidence | Observed/reported actions and testimony become qualified sources | Analyst records affect an actor only if actually communicated | Private beliefs are not known from role or behavior alone |
| Actor information/action ↔ Scenario analysis | Describe owned policy, information and action mechanism in scenario | Hypothetical outcomes compare alternate policies | A modeled actor may not use the analyst future trajectory |
| Actor information/action ↔ Analyst assessment | Supply action/outcome/knowledge claims for evaluation | Propose investigation or change, not command the actor | Empirical and normative actor evaluation remain distinct |
| Actor information/action ↔ Policy review | Provide actually received experience and current policy version | Review may propose an amendment; adoption changes current rule | Ordinary changed action alone is not policy revision |
| Restoration/support ↔ Real organization change | Existing support/capability can enable or constrain novelty | Retained new arrangement can add or remove restorative paths | Novelty may consume support and create shared fragility |
| Restoration/support ↔ Governance/adoption | Repair need and capability inform proposals via channels | Governance authorizes support or changes its allocation | External relief can build, displace or leave capability unchanged |
| Restoration/support ↔ Frames/meaning | Local practices/testimony inform attributed understanding | Received framing may shape support choices through action | Existing practice is neither automatically wise nor obsolete |
| Restoration/support ↔ Evidence | Condition, recovery and local knowledge produce qualified observations | Evidence supports/challenges restorative claims | Unchanged normal output does not demonstrate retained backup capacity |
| Restoration/support ↔ Scenario analysis | Specify restoration paths, shared supports and disturbances | Analyze hypothetical support, substitution or loss | Independence of alternative routes must be examined |
| Restoration/support ↔ Analyst assessment | Supply persistence/recovery/condition and tradeoffs | Identify hidden fragility or propose support changes | Local output and wider resilience may diverge |
| Restoration/support ↔ Policy review | Repair and review may share staff, sensors or other resources | Adopted amendment changes support demands or allocation | A working controller can coexist with degraded review capability |
| Real organization change ↔ Governance/adoption | Actual reorganization can change jurisdiction or rule mechanisms | Authority and adopted rules permit/restrict generation | Rule-making change needs evidence and transition history |
| Real organization change ↔ Frames/meaning | Experienced new arrangements may inform owned frames | Interpretation can influence selection/adoption through actual actors | Cultural uptake and individual belief change have different mechanisms |
| Real organization change ↔ Evidence | Actual changes become observations with time/provenance | Evidence revises the description of structural history | Model revision is not itself actual self-organization |
| Real organization change ↔ Scenario analysis | Specify permitted transition, resources and carry-over | Analyze hypothetical organization and later trajectories | Do not insert useful novelty then call it discovered |
| Real organization change ↔ Analyst assessment | Supply actual change/selection claims and outcomes | Assess usefulness or revise explanation, not alter the past | Greater complexity is not proof of useful learning |
| Real organization change ↔ Policy review | Changed organization can alter a review process and its access | Authorized amendment can trigger actual structural change | Retain reviewer ownership and commitments after reorganization |
| Governance/adoption ↔ Frames/meaning | Communicated rules and actual adoption can influence owned interpretation | Attributed frames may shape rule proposals/goals via actors | Analyst assumptions are not institutional law |
| Governance/adoption ↔ Evidence | Adoption/enforcement create observable records and outcomes | Evidence may inform governance only via an actual communication path | A policy document proves neither compliance nor effect |
| Governance/adoption ↔ Scenario analysis | Supply authority, resource and implementation assumptions | Compare hypothetical intervention/transition alternatives | Scenario feasibility assumptions do not establish actual adoption |
| Governance/adoption ↔ Analyst assessment | Supply status, jurisdiction, incentives and implementation claims | Assess feasibility/desirability and propose changes | Leverage strength is distinct from authority or legitimacy |
| Governance/adoption ↔ Policy review | Authorize review, amendment and finite implementation | Submit candidate change; adoption returns version/status | Review may defer, reject, fail or be overridden |
| Frames/meaning ↔ Evidence | Definitions qualify source interpretation and correspondence | Source accounts challenge assumptions; corrections preserve originals | Neither preferred wording nor a changed frame erases evidence |
| Frames/meaning ↔ Scenario analysis | Specify meanings, units, scales and alternate frames | Expose sensitivities or incompatibilities across accounts | Ordinal relabeling cannot license cardinal operations |
| Frames/meaning ↔ Analyst assessment | Make empirical/normative assumptions and variable meanings inspectable | Challenge meanings or assumptions with reasoned versioned revision | Do not select a frame solely to obtain a preferred answer |
| Frames/meaning ↔ Policy review | Owned interpretation and criteria qualify review inputs | Available experience may revise beliefs through a specified/unknown updater | A reviewer does not inherit analyst semantic certainty |
| Evidence ↔ Scenario analysis | Independent records inform initial history and model assumptions | Predictions define expectations/comparison queries, not new source records | Prohibited: recycle prediction as independent observation |
| Evidence ↔ Analyst assessment | Independent observations support aligned comparison | Request inquiry or record a correction without altering the original | Repeated summaries of one source are not independent confirmation |
| Evidence ↔ Policy review | Analyst evidence reaches a reviewer only through declared delivery | Observed review/adoption can become new source records | Separate analyst archive from the reviewers available information |
| Scenario analysis ↔ Analyst assessment | Conditional trajectories and assumptions support assessment | Choose alternatives, discriminate or revise the analysis | Comparing scenarios is not an executed intervention |
| Scenario analysis ↔ Policy review | A received analysis may inform a real reviewer via a communication path | Review/adoption assumptions define hypothetical policy changes | No direct scenario control over an actual policy |
| Analyst assessment ↔ Policy review | Proposed recommendations need actual delivery and adoption | Observed review outcomes can inform analyst model evaluation | Analyst revision and actual policy amendment remain separate |

This finite group review cannot prove discovery of every component or interface in a real system. An instantiated model must resolve actual endpoints, payloads, units/scales, direction, timing, capacity, authority, evidence and uncertainty. A supported absence, inapplicable link and unresolved link require different recorded dispositions. Indirect routes and common dependencies must be checked even when neither direct direction is active. The pair ledger is a design audit, not a generated all-to-all causal network.

### 46.2 KISS disposition

No new universal optimizer, morality engine, domain-specific world copy or learning service is required. The added records refer to existing constituents, processes, policy, evidence and criteria. Diagram nodes denote roles and views rather than database tables or mandatory software services. A review process becomes executable only when its actual mechanism is specified. Unknowns do not force fabricated precision or block every useful qualitative inference.

## 47. Seven-chapter requirement allocation

The existing 42 definitions in sections 10, 26 and 37 retain their meanings under I7. Twelve explicit obligations below strengthen Chapter 7 integration. Additional allocations of existing requirements are shown separately so there is only one canonical definition per requirement. Chapter 7's eighteen parent requirements remain source-assessment identifiers, not eighteen mandatory software components.

| Requirement | Function | Obligation | Prospective cases |
| --- | --- | --- | --- |
| I7-R43 | Behavior-grounded inquiry | Preserve level, rate, variability, extremes, aggregation, timing and remedy-independent problem framing. | I7-T125, I7-T126, I7-T127 |
| I7-R44 | Meaning and cross-domain correspondence | Define source terms, referents, constructs, scales, aggregation and time; reconcile domain accounts without treating relabeling as a causal intervention. | I7-T134, I7-T135, I7-T136, I7-T161, I7-T162, I7-T163, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T187 |
| I7-R45 | Qualitative concerns and measurement discipline | Retain attributed importance, uncertain mechanisms and legitimate qualitative assessment; ordinal labels do not license cardinal arithmetic or invented calibration. | I7-T137, I7-T138, I7-T139, I7-T187 |
| I7-R46 | Owned versioned policy response | Identify policy owner, available input, rule/version, reference, timing and actual execution constraints. Changing action alone is not policy learning. | I7-T140, I7-T141, I7-T172, I7-T185 |
| I7-R47 | Monitoring, review and adopted amendment | Specify monitoring, owned expectations, trigger/cadence, update mechanism or unknown, allowed proposal, authority, resources and adoption with state/history carry-over. | I7-T142, I7-T171, I7-T172, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T185, I7-T192 |
| I7-R48 | Inspectable expectations and error inquiry | Preserve original forecasts, independent evidence, correspondence, discrepancy, rival causes and rationale for retention, revision, rejection or further inquiry. | I7-T128, I7-T129, I7-T130, I7-T152, I7-T153, I7-T154, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T185, I7-T191 |
| I7-R49 | Responsibility and consequence feedback | Separate causal influence, burden incidence, knowledge, decision rights, capacity and normative attribution; feedback alone neither assigns blame nor ensures correction. | I7-T149, I7-T150, I7-T151, I7-T190 |
| I7-R50 | Affected-party and evaluative coverage | Keep causal scope, affected parties and whose interests count distinct. Attribute qualitative priorities, disagreements and omitted distributed effects without a compulsory global utility. | I7-T143, I7-T144, I7-T145, I7-T164, I7-T165, I7-T166, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T186 |
| I7-R51 | Nested time scales and horizons | Separate physical timing, cadence, planning horizon and value weighting. Retain slow state, fast thresholds and residual obligations beyond the reporting endpoint. | I7-T158, I7-T159, I7-T160, I7-T189 |
| I7-R52 | Reference integrity and reasoned change | Preserve observed conduct, report selection, original/current standard and revision rationale. Distinguish improvement, erosion and legitimate deliberative revision. | I7-T167, I7-T168, I7-T169, I7-T188 |
| I7-R53 | Information integrity and actor-visible change | Preserve source, measurement/reporting status, transformations, availability, receipt and interpretation. Published or reported improvement is not automatically verified physical improvement. | I7-T131, I7-T132, I7-T133, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T188, I7-T190 |
| I7-R54 | Bounded practice and implementation | Expose assumptions, useful existing capability, justified simplification and unresolved mechanisms; allow provisional decisions without claiming omniscience, automatic adoption or a competent universal learner. | I7-T128, I7-T129, I7-T130, I7-T146, I7-T147, I7-T148, I7-T155, I7-T156, I7-T157, I7-T170, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T188, I7-T191, I7-T192 |

### 47.1 Strengthened inherited allocations

| Inherited obligation reference | Additional prospective cases |
| --- | --- |
| Existing I7-R01 | I7-T134, I7-T135, I7-T136, I7-T161, I7-T162, I7-T163, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T186 |
| Existing I7-R02 | I7-T128, I7-T129, I7-T130, I7-T134, I7-T135, I7-T136, I7-T161, I7-T162, I7-T163, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T187, I7-T192 |
| Existing I7-R03 | I7-T125, I7-T126, I7-T127, I7-T158, I7-T159, I7-T160, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T189 |
| Existing I7-R04 | I7-T140, I7-T141, I7-T155, I7-T156, I7-T157, I7-T172 |
| Existing I7-R05 | I7-T137, I7-T138, I7-T139, I7-T143, I7-T144, I7-T145, I7-T149, I7-T150, I7-T151, I7-T164, I7-T165, I7-T166, I7-T167, I7-T168, I7-T169 |
| Existing I7-R06 | I7-T146, I7-T147, I7-T148, I7-T155, I7-T156, I7-T157 |
| Existing I7-R07 | I7-T146, I7-T147, I7-T148, I7-T192 |
| Existing I7-R08 | I7-T142, I7-T155, I7-T156, I7-T157, I7-T172, I7-T173, I7-T178 |
| Existing I7-R09 | I7-T143, I7-T144, I7-T145, I7-T149, I7-T150, I7-T151, I7-T161, I7-T162, I7-T163, I7-T192 |
| Existing I7-R10 | I7-T143, I7-T144, I7-T145, I7-T146, I7-T147, I7-T148, I7-T164, I7-T165, I7-T166 |
| Existing I7-R11 | I7-T125, I7-T126, I7-T127, I7-T128, I7-T129, I7-T130, I7-T131, I7-T132, I7-T133, I7-T134, I7-T135, I7-T136, I7-T137, I7-T138, I7-T139, I7-T152, I7-T153, I7-T154, I7-T161, I7-T162, I7-T163, I7-T167, I7-T168, I7-T169, I7-T170, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T191 |
| Existing I7-R12 | I7-T125, I7-T126, I7-T127, I7-T128, I7-T129, I7-T130, I7-T137, I7-T138, I7-T139, I7-T152, I7-T153, I7-T154, I7-T155, I7-T156, I7-T157, I7-T158, I7-T159, I7-T160, I7-T164, I7-T165, I7-T166, I7-T170, I7-T171, I7-T179, I7-T184, I7-T191 |
| Existing I7-R13 | I7-T128, I7-T129, I7-T130, I7-T134, I7-T135, I7-T136, I7-T161, I7-T162, I7-T163, I7-T187 |
| Existing I7-R14 | I7-T142, I7-T152, I7-T153, I7-T154, I7-T158, I7-T159, I7-T160, I7-T171, I7-T172, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T189 |
| Existing I7-R15 | I7-T131, I7-T132, I7-T133, I7-T134, I7-T135, I7-T136, I7-T140, I7-T141, I7-T149, I7-T150, I7-T151, I7-T170, I7-T171, I7-T172, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T185, I7-T190 |
| Existing I7-R16 | I7-T125, I7-T126, I7-T127, I7-T155, I7-T156, I7-T157, I7-T189, I7-T191 |
| Existing I7-R17 | I7-T134, I7-T135, I7-T136, I7-T143, I7-T144, I7-T145, I7-T161, I7-T162, I7-T163, I7-T164, I7-T165, I7-T166, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T186 |
| Existing I7-R19 | I7-T125, I7-T126, I7-T127, I7-T140, I7-T141, I7-T142, I7-T158, I7-T159, I7-T160, I7-T172, I7-T173, I7-T178 |
| Existing I7-R20 | I7-T131, I7-T132, I7-T133, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| Existing I7-R22 | I7-T149, I7-T150, I7-T151, I7-T164, I7-T165, I7-T166, I7-T186, I7-T190 |
| Existing I7-R23 | I7-T167, I7-T168, I7-T169, I7-T188 |
| Existing I7-R25 | I7-T146, I7-T147, I7-T148, I7-T188 |
| Existing I7-R26 | I7-T137, I7-T138, I7-T139, I7-T143, I7-T144, I7-T145, I7-T149, I7-T150, I7-T151, I7-T164, I7-T165, I7-T166, I7-T167, I7-T168, I7-T169, I7-T188 |
| Existing I7-R27 | I7-T140, I7-T141, I7-T172 |
| Existing I7-R28 | I7-T142, I7-T152, I7-T153, I7-T154, I7-T170, I7-T171, I7-T172, I7-T173, I7-T178, I7-T179, I7-T184, I7-T185 |
| Existing I7-R29 | I7-T155, I7-T156, I7-T157 |
| Existing I7-R30 | I7-T143, I7-T144, I7-T145, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T192 |
| Existing I7-R31 | I7-T140, I7-T141, I7-T142, I7-T152, I7-T153, I7-T154, I7-T170, I7-T171, I7-T172, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T189 |
| Existing I7-R34 | I7-T158, I7-T159, I7-T160 |
| Existing I7-R35 | I7-T140, I7-T141, I7-T158, I7-T159, I7-T160, I7-T172, I7-T189 |
| Existing I7-R36 | I7-T140, I7-T141, I7-T146, I7-T147, I7-T148, I7-T172, I7-T192 |
| Existing I7-R37 | I7-T131, I7-T132, I7-T133, I7-T149, I7-T150, I7-T151, I7-T190 |
| Existing I7-R38 | I7-T142, I7-T149, I7-T150, I7-T151, I7-T172, I7-T173, I7-T178, I7-T190 |
| Existing I7-R40 | I7-T137, I7-T138, I7-T139, I7-T142, I7-T164, I7-T165, I7-T166, I7-T167, I7-T168, I7-T169, I7-T172, I7-T173, I7-T178 |
| Existing I7-R41 | I7-T167, I7-T168, I7-T169, I7-T170, I7-T171, I7-T179, I7-T184 |
| Existing I7-R42 | I7-T128, I7-T129, I7-T130, I7-T152, I7-T153, I7-T154, I7-T170, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184, I7-T191 |

### 47.2 Chapter 7 parent correspondence

| Chapter 7 parent | Cumulative requirements | Retained parent obligation | Cases |
| --- | --- | --- | --- |
| C7-R01 | I7-R11, I7-R12, I7-R15, I7-R28, I7-R31, I7-R41, I7-R42, I7-R54 | Separate conditional understanding, available knowledge, adoption and conduct; retain uncertainty without asserting impossibility of all prediction or control. | I7-T170, I7-T171, I7-T179, I7-T184 |
| C7-R02 | I7-R03, I7-R11, I7-R12, I7-R16, I7-R19, I7-R43 | Preserve timing, levels, variability, coverage and remedy-independent problem statements. | I7-T125, I7-T126, I7-T127 |
| C7-R03 | I7-R02, I7-R11, I7-R12, I7-R13, I7-R42, I7-R48, I7-R54 | Expose consistent assumptions, alternatives, unknowns and evidence-qualified revision in quantitative or qualitative form. | I7-T128, I7-T129, I7-T130 |
| C7-R04 | I7-R11, I7-R15, I7-R20, I7-R37, I7-R53 | Distinguish condition, measurement, report, publication, receipt, interpretation and physical effect. | I7-T131, I7-T132, I7-T133 |
| C7-R05 | I7-R01, I7-R02, I7-R11, I7-R13, I7-R15, I7-R17, I7-R44 | Define referents, constructs, scales and temporal meaning; distinguish analyst relabeling from actor-visible communication effects. | I7-T134, I7-T135, I7-T136 |
| C7-R06 | I7-R05, I7-R11, I7-R12, I7-R26, I7-R40, I7-R45 | Retain qualitative importance, attribution and proposed effects without false cardinal precision or mandatory aggregation. | I7-T137, I7-T138, I7-T139 |
| C7-R07 | I7-R04, I7-R15, I7-R19, I7-R27, I7-R31, I7-R35, I7-R36, I7-R46 | Specify available input, versioned response, actual constraints and timing; changing action does not imply policy learning. | I7-T140, I7-T141, I7-T172 |
| C7-R08 | I7-R08, I7-R14, I7-R19, I7-R28, I7-R31, I7-R38, I7-R40, I7-R47 | Specify review, expectations, authority, proposal, adoption and commitment carry-over separately from model revision. | I7-T142, I7-T172, I7-T173, I7-T178 |
| C7-R09 | I7-R05, I7-R09, I7-R10, I7-R17, I7-R26, I7-R30, I7-R50 | Evaluate wider consequences and distribution with explicit boundary and purpose; do not presume an agreed global utility. | I7-T143, I7-T144, I7-T145 |
| C7-R10 | I7-R06, I7-R07, I7-R10, I7-R25, I7-R36, I7-R54 | Identify current local functioning and support dependencies; compare capability building, displacement and substitution. | I7-T146, I7-T147, I7-T148 |
| C7-R11 | I7-R05, I7-R09, I7-R15, I7-R22, I7-R26, I7-R37, I7-R38, I7-R49 | Separate trigger, mechanism, influence, exposure, authority, ability and normative responsibility. | I7-T149, I7-T150, I7-T151 |
| C7-R12 | I7-R11, I7-R12, I7-R14, I7-R28, I7-R31, I7-R42, I7-R48 | Preserve expectations and observations, classify unresolved discrepancies and justify retention, revision or further inquiry. | I7-T152, I7-T153, I7-T154 |
| C7-R13 | I7-R04, I7-R06, I7-R08, I7-R12, I7-R16, I7-R29, I7-R54 | Permit transients, heterogeneity and changing modes while supporting justified simplification and attributed evaluation. | I7-T155, I7-T156, I7-T157 |
| C7-R14 | I7-R03, I7-R12, I7-R14, I7-R19, I7-R34, I7-R35, I7-R51 | Preserve slow state, fast events, residual obligations and explicit horizon or discount assumptions. | I7-T158, I7-T159, I7-T160 |
| C7-R15 | I7-R01, I7-R02, I7-R09, I7-R11, I7-R13, I7-R17, I7-R44 | Compose accounts through shared referents, units, mechanisms and evidence; retain substantive disagreement. | I7-T161, I7-T162, I7-T163 |
| C7-R16 | I7-R05, I7-R10, I7-R12, I7-R17, I7-R22, I7-R26, I7-R40, I7-R50 | Distinguish causal scope, affected parties and evaluated interests with attributed priorities and uncertainty. | I7-T164, I7-T165, I7-T166 |
| C7-R17 | I7-R05, I7-R11, I7-R23, I7-R26, I7-R40, I7-R41, I7-R52 | Keep conduct, selected reports, reference history and corrective action separate; distinguish improvement, erosion and legitimate revision. | I7-T167, I7-T168, I7-T169 |
| C7-R18 | I7-R01, I7-R02, I7-R03, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | Preserve independent evidence, shared identity, definitions, commitments and explicit unknowns across learning and evaluation. | I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |

## 48. Cumulative prospective scenarios: Chapter 7 and composition

**All cases are PLANNED — NOT RUN.** C7-T01–C7-T60 map to I7-T125–I7-T184, preserving scenario and acceptance wording. Three cases per source practice form the first 45 Chapter 7 cases; fifteen further cases test cross-cutting issues. I7-T185–I7-T192 add cumulative composition checks. These are future acceptance criteria for instantiated models, not executed intelligence, causal findings or test protocols specified by Meadows.

| Case | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T125 | Hold a history mean approximately fixed while increasing variability or extremes. | Keep the distinction visible; do not diagnose a falling average from more severe low observations alone. |
| I7-T126 | Compare recalled timing with timestamped records containing gaps or changed aggregation. | Preserve source status, coverage and temporal correspondence; neither account becomes complete by assumption. |
| I7-T127 | Define an observed shortage, then compare several explanations and remedies. | The problem record does not encode the favorite solution as the only possible cause or objective. |
| I7-T128 | Use inconsistent meanings for a stock or rate in two parts of a candidate model. | Expose the inconsistency or require an explicit conversion; do not silently reconcile it to fit a result. |
| I7-T129 | Offer a diagram, a qualitative rule and an executable equation for the same proposed mechanism. | Compare their claimed correspondence and missing details; explicitness alone is not evidence of truth. |
| I7-T130 | Supply conflicting evidence for a preferred account and a credible rival. | Retain the conflict, original hypothesis and support status; revision must not overwrite the observation. |
| I7-T131 | Delay, filter or corrupt a signal reaching one actor while the analyst retains the full record. | Actor choice uses only its modeled available information and internal condition. |
| I7-T132 | Report declining emissions under changed reporting coverage or definitions. | Separate reported and actual quantities and retain rival explanations; the source percentage is not an automatic causal coefficient. |
| I7-T133 | Publish previously hidden information to a recipient who may ignore it or respond adversely. | Distinguish retention, publication, receipt and action; more disclosure is not hardcoded as improvement. |
| I7-T134 | Use the same term for different constructs and different terms for the same candidate subject. | Require scope and identity evidence; spelling alone neither merges nor separates real referents. |
| I7-T135 | Compose accounts of rate, stock and throughput with incompatible units or time windows. | Expose the mismatch and declare conversions or unresolved status. |
| I7-T136 | Rename an analyst variable, then separately change an actor-visible message or institutional category. | Only the latter can affect behavior through a specified receipt and interpretation path. |
| I7-T137 | Compare omission of an important qualitative concern with explicit qualitative inclusion. | Lack of a reliable number is not treated as zero importance or proof of no possible effect. |
| I7-T138 | Replace a qualitative or ordinal scale with arbitrary numerical labels. | Do not infer equal intervals or numerical causal precision without a justified measurement and response interpretation. |
| I7-T139 | Elicit a nonlinear response from participants under differing experiences. | Retain source, uncertainty and disagreement; elicitation alone does not calibrate a universal law. |
| I7-T140 | Hold a policy version fixed while its action changes with observed state. | Classify this as state-dependent response, not evidence that the policy revised itself. |
| I7-T141 | Compare static and state-dependent response under noisy and delayed conditions. | Results depend on the specified rules and capacities; feedback adaptation is not assumed always better. |
| I7-T142 | Enable monitoring and formal review that can amend targets or coverage. | Require a review mechanism, authority, proposal/adoption distinction and preservation of existing commitments. |
| I7-T143 | Improve local shipment output while another user loses essential service through a shared constraint. | Preserve distribution and wider effects rather than defining local proxy improvement as global benefit. |
| I7-T144 | Widen the model to include a previously external supplier or environmental process. | Preserve shared identity and replace or condition the old external closure at the affected interface. |
| I7-T145 | Optimize an indicator for an activity whose purpose is contested. | Expose the purpose/criterion question and retain stakeholder disagreement. |
| I7-T146 | Substitute external service for an existing local corrective practice. | Track actual performance and whether local capability is maintained, improved or eroded. |
| I7-T147 | Consult local participants who identify an obstacle omitted by an imported proposal. | Retain testimony and compare alternatives; local status alone does not establish a correct causal diagnosis. |
| I7-T148 | Compare obstacle removal, capability building and outside investment. | Specify their mechanisms, resources, timing and distribution without assuming a universal preferred option. |
| I7-T149 | Compare an external trigger with differing internal susceptibility or corrective capacity. | Preserve both contributions; a visible event does not erase the generating structure or all external causes. |
| I7-T150 | Return consequences directly to a decision maker, then through a delayed intermediary. | Trace receipt, interpretation, authority and feasible response; direct exposure alone does not ensure improvement. |
| I7-T151 | Let one party suffer effects it did not choose and cannot control. | Keep consequence incidence, causal influence and normative responsibility distinct; do not infer blame from harm. |
| I7-T152 | Record a forecast, later contradictory evidence and an unresolved causal discrepancy. | Preserve the forecast and evidence and retain competing explanations rather than bluffing a diagnosis. |
| I7-T153 | Take a small action near a threshold or repeat small actions that accumulate. | Monitoring and small scale do not erase irreversible or cumulative effects. |
| I7-T154 | Review an error and choose to retain a policy pending more evidence. | A documented justified retention is possible; learning is not measured solely by how often the rule changes. |
| I7-T155 | Represent a functioning oscillation or long transient. | Do not equate departure from fixed equilibrium with failure without an attributed functioning criterion. |
| I7-T156 | Compare a simple approximation with a heterogeneous nonlinear model over several conditions. | State applicability and meaningful omissions; graph size alone does not establish quality. |
| I7-T157 | Remove rarely active diversity or alternative mechanisms. | Assess changed conditions and dependencies, while permitting irrelevant detail to be omitted with a rationale. |
| I7-T158 | End an evaluation before a delayed cost or obligation appears. | Retain the residual effect and report horizon dependence rather than treating it as nonexistent. |
| I7-T159 | Couple a fast threshold-crossing process with slow recovery or accumulated commitments. | Preserve relevant initial history and avoid averaging away the consequential event. |
| I7-T160 | Compare a near-term urgent need with distant consequences under different weighting assumptions. | Keep empirical outcomes and normative time weights separate; no horizon is assumed universally decisive. |
| I7-T161 | Combine economic, ecological and behavioral accounts that share a resource. | Map referents, rates, meanings and evidence dependencies; do not duplicate the resource or shared capacity. |
| I7-T162 | Use similar topology in different domains with different timing and response laws. | Topology does not authorize coefficient transfer or quantitative dynamic equivalence. |
| I7-T163 | Retain incompatible expert accounts after terminology is reconciled. | Document the substantive disagreement and needed evidence instead of forcing superficial consensus. |
| I7-T164 | Include an affected party in causal dynamics but omit it from the objective. | Expose the distinction between analytical inclusion and ethical evaluation. |
| I7-T165 | Improve a local outcome while exporting burden to another group or ecological subsystem. | Trace direction, magnitude or qualitative meaning, timing and the omitted-party consequence. |
| I7-T166 | Agree on a predicted consequence but disagree on its ethical weight. | Preserve normative disagreement; more observations alone are not assumed to select the value. |
| I7-T167 | Reduce a discrepancy by lowering the performance or moral standard. | Report reference change separately from actual outcome improvement. |
| I7-T168 | Feed selectively emphasized bad examples into a reference update. | Retain the selection mechanism and actual source history; do not manufacture equal good/bad frequencies. |
| I7-T169 | Revise a contested or infeasible standard through an explicit deliberative process. | Allow legitimate revision as an alternative to pathological drift, with owner, rationale and affected interests. |
| I7-T170 | Explain a potentially helpful intervention without actual adoption. | Do not record its expected effect as implemented behavior; keep the understanding–implementation gap visible. |
| I7-T171 | Let an actor receive and believe a report but lack resources or authority. | Separate information uptake from ability to act and actual outcome. |
| I7-T172 | Update a feedback response from monitored results while the physical effect remains delayed. | Include pending actions, review cadence and noise; repeated revision need not improve performance. |
| I7-T173 | Revise an analyst model while leaving the actor policy unchanged, then revise the actor policy in another scenario. | Keep the two changes, their state histories and evidence obligations separate. |
| I7-T174 | Use one source account through several summaries and disciplines. | Retain dependency and avoid counting the repeated account as independent confirmation. |
| I7-T175 | Pass scenario predictions through a learning record or an explanatory model. | They remain model-derived until compared with independently identified observations. |
| I7-T176 | Change a variable definition or measurement procedure after an apparent prediction error. | Retain the old definition and an explicit correspondence; the error cannot be silently erased. |
| I7-T177 | Combine an actor-visible monitoring intervention with an ostensibly passive evaluation. | Represent effects of observation/publication where relevant; do not assume the measurement procedure is causally inert. |
| I7-T178 | Amend a policy while deliveries, restoration work or obligations are pending. | Preserve quantities, commitments, version semantics and carry-over instead of restarting the scenario. |
| I7-T179 | Leave a policy-update rule, qualitative relation or shared value unknown. | Retain a useful partial representation without claiming an executable learner or invented welfare coefficient. |
| I7-T180 | Expand causal scope, stakeholder concern and horizon in different combinations. | Record which boundary changed and why; widening one does not automatically widen the others or improve the decision. |
| I7-T181 | Make local metrics look stable while supportive capability erodes and a normative standard drifts. | Retain interacting mechanisms and distinct outcomes; a favorable proxy cannot hide all deteriorating state. |
| I7-T182 | Attribute private motives or a shared cultural belief from role labels alone. | Keep source basis, heterogeneity and unresolved attribution; no stereotype supplies a decision law. |
| I7-T183 | Exercise a model against new operating conditions after earlier favorable performance. | Reassess domain and competing mechanisms; earlier fit is not universal validity. |
| I7-T184 | Retain important uncertainty while choosing a provisional action or deferring an unsupported conclusion. | Record criteria, limitations and revision triggers; neither false certainty nor perpetual paralysis is compulsory. |

### 48.1 Additional seven-chapter composition cases

| Case | Scenario | Prospective acceptance check |
| --- | --- | --- |
| I7-T185 | Enable ordinary response, policy review and analyst revision separately under delayed noisy observations. | Each process changes only its declared owned state; a review proposal may be refused, and no analyst revision silently changes the actor policy. |
| I7-T186 | Widen a supply-and-service view to affected neighbors while keeping a narrower evaluative preference. | Causal closure replaces the old driver where appropriate; affected-party coverage and normative priority remain separately recorded, with no duplicate resource or compulsory moral weighting. |
| I7-T187 | Merge an ecological ordinal condition report, a monetary market account and a qualitative account of local capability. | Shared referents, unit/scale operations, time alignment and disagreements are explicit; missing coefficients remain unknown and labels cannot manufacture a calibrated relationship. |
| I7-T188 | Service meets a lowered target while support displaces local repair and adverse reports are filtered. | Separate actual service, selected reports, reference erosion, legitimate revision and future corrective condition; apparent short-run compliance cannot certify system improvement. |
| I7-T189 | Run a small monitored intervention while slow damage and an in-flight commitment approach a nonlinear threshold. | A small step may still trigger irreversible effects; monitoring delay, relevant retained state, alternative lever/adoption times and outcomes beyond the endpoint remain visible. |
| I7-T190 | Give a decision maker faster consequence reports while restricting amendment authority and revealing a common resource decline. | Receipt is distinct from ability, legitimacy and responsibility; permit adverse appropriation or no response under declared rules without oracle knowledge or automatic moral blame. |
| I7-T191 | Two rival mechanisms predict the same ordinary history, then disagree after a new independently observed regime. | Preserve old forecasts and observations, inspect measurement/implementation/driver alternatives and justify only the revision supported by evidence; do not force a unique explanation or credit recycled predictions. |
| I7-T192 | Two subsystems share a sensor and finite repair/review staff; one adaptive policy diverts that support. | Count shared support once, represent common monitoring failure and delayed cross-system consequences, and distinguish stable local output from degraded corrective and learning capability. |

## 49. Critical seven-chapter retrospective and verdict

### 49.1 Findings and repairs

| Finding | Issue questioned | Disposition and rationale |
| --- | --- | --- |
| A7-01 | A separate Chapter 7 extension did not establish cumulative coverage | Merge all fifteen practices into the existing core, one master graph, contracts and source-to-case traceability. Retain all earlier concepts and named connections. |
| A7-02 | Policy, intention and learning were insufficiently separated | Make the current rule/version explicit; separate ordinary response, owned policy review, amendment proposal, actual adoption and analyst explanatory revision. |
| A7-03 | More data or an update box could be mistaken for competent learning | Specify received evidence, original expectation, timing, trigger, updater/unknown, authority and resources. Retain rival error causes and deferred or refused changes. |
| A7-04 | Shared language and qualitative ratings could manufacture precision | Add meaning, scale and domain-correspondence contracts; keep source wording and unknowns. Renaming an analyst label does not change actor behavior. |
| A7-05 | Important qualitative concerns and caring could collapse into a universal utility | Record causal scope, affected-party coverage and evaluative scope separately, including disagreement and unmeasured concerns. Importance is not evidence of causal magnitude. |
| A7-06 | Responsibility could conflate being harmed, causing harm and having control | Separate influence, incidence, knowledge, authority, capacity and normative attribution. Trace consequence feedback without automatically deriving blame or good action. |
| A7-07 | Learning could erase inconvenient evidence or rewrite definitions | Preserve original forecasts, source observations, definitions and revision history. Independent source roots remain protected from prediction recycling. |
| A7-08 | Long horizons and small experiments could be assumed intrinsically safe or correct | Keep fast/slow coupling, residual obligations, thresholds, uncertainty and weighting explicit; compare current needs and later effects without assuming universal superiority. |
| A7-09 | Whole-system improvement could hide displacement or lowered aspirations | Track existing repair/support capacity, local/wider outcomes, report selection and standard history. Distinguish reference erosion from genuine improvement and legitimate revision. |
| A7-10 | Diagram arrows could be read as universal mechanisms or direct intervention rights | Retain typed solid/dotted relations and scenario/adoption status. Add pairwise direction review and explicit ownership contracts; do not create all-to-all actual links. |
| A7-11 | A complete-looking catalogue could overstate scientific qualification | Separate conceptual source coverage from executable dynamics, causal identification, policy efficacy and intelligence. Mark every model scenario as unrun. |
| A7-12 | Historical verdicts and an evolution table could misstate current scope | Mark older audits as retained history; validate the exact eight-column evolution header and current 170-page scope rather than checking column consistency alone. |

All repairs are **conceptual specification changes**. Their existence does not establish successful execution or discovery. The following review asks whether the integrated contracts fit together; it does not validate an unspecified implementation.

### 49.2 Coverage across all seven chapters

| Chapter | Integrated foundations / mechanisms | Main cumulative anchors | Review result |
| --- | --- | --- | --- |
| 1 — Basics | Elements, interconnections, function/purpose; stock accounting, flows, information, balancing/reinforcing paths, delay and behavior | Sections 3–7, 13; B01–B36 | Retained and linked to policy/meaning/evidence contracts |
| 2 — Systems Zoo | Conditional behavior modes, coupled loops, shifting dominance, renewable/nonrenewable resources, capacities, overshoot and depletion | Sections 6, 8–14, 17; Z01–Z42 | Retained; no unique trajectory inferred from topology alone |
| 3 — Why Systems Work So Well | Resilience, repair, alternatives/shared dependencies, actual self-organization, hierarchy and local/wider functioning | Sections 3–7, 13–14; F01–F32 | Retained; local capability now feeds review and wider evaluation |
| 4 — Why Systems Surprise Us | Events/patterns/structure, nonlinear applicability, boundary limits, changing constraints, delays and bounded rationality | Sections 16–20; U01–U48 | Retained; available knowledge remains actor-owned |
| 5 — System Traps and Opportunities | Policy resistance, commons, low-performance drift, escalation, success to successful, burden shifting/addiction, rule beating and wrong goals | Sections 22–31; C5-F01–C5-F56 | All eight retained as composable conditional hypotheses; opportunities require actual adoption |
| 6 — Leverage Points | Twelve tentative positions from parameters to reconsidering paradigms, with target, direction, critical regimes and feasibility | Sections 32–41; C6-F01–C6-F64 | All twelve retained; no rank-based efficacy or automatic frame conversion |
| 7 — Living in a World of Systems | Fifteen practices; bounded inquiry, meanings, qualitative concerns, feedback-policy amendment, responsibility, learning and caring | Sections 43–48; C7-F01–C7-F68 | Integrated into core and one master graph, with unknown mechanisms preserved |

### 49.3 First-principles, Five Whys, MECE and dependency review

**First principles:** a representation must distinguish what exists, what changes, what governs change, what is observed, what is inferred, what is valued and what has actually been adopted. No additional causal force follows from naming a feedback loop, archetype, paradigm or learning process. Relevance to the inquiry determines detail; uncertainty is preserved rather than filled with a convenient law.

**Five Whys, applied to a bad outcome:** why did the outcome differ? Check the realized process. Why that process? Inspect available resources, rule and delayed commitments. Why that rule or intended action? Inspect received information, references, incentives and authority. Why were those arrangements retained? Inspect review, adoption, selection and supporting history. Why accept this explanation? Examine independent evidence, alternatives and discriminating observations. Branch whenever several mechanisms fit; the fifth answer is not automatically a root cause. The same questioning applies to a proposed remedy and its assumed beneficial direction.

**MECE where defensible:** keep referent/variable, stock/rate/capacity, actual/perceived, intent/realization, proposal/adoption, observation/prediction, ordinal/cardinal, empirical/normative, causal scope/evaluative coverage and response/policy revision/model revision distinct. Do not force overlapping mechanisms, system memberships, archetypes, leverage positions or practices into mutually exclusive boxes. Their overlap is represented through shared referents.

**Dependency and waterfall review:** trace source concept → requirement → family or view → directed contract → scenario → qualification claim; trace an unexpected result back through that chain. This is a traceability sequence, not a claim that development or discovery must follow a one-pass waterfall. Revise earlier assumptions when later evidence warrants it. The canonical crosswalk and parent mapping expose the route; they do not prove the chosen interpretation is uniquely correct.

**KISS:** retain nine families and reuse identity, time, evidence, criteria and transition contracts. Add a state only if it retains consequential independent history. Add a node to distinguish an important role, not to imply a service or separate world. Do not demand equations for every concern, a universal score or a direct link for every pair. Explicit unknowns and qualitative models are preferable to decorative precision.

### 49.4 End-to-end integration walkthrough

Use the retained inventory-and-service example. Begin with observed service, inventory, demand, delay and loss histories and direct structural evidence. Separate increasing variability from a lower mean; define the concern without presupposing another supplier. Map units, sources, reporting changes and qualitative accounts of essential needs.

Construct rival explanations using shared stocks, pending deliveries, capacities and response rules. Describe each actor's received information, current ordering policy and intended action; actual shared constraints govern fulfillment. A fixed ordering rule may react to a shortage without learning. A separate reviewer may compare an owned expectation with later received evidence, consider measurement error or changed demand, and propose an amended rule. Authority, resources, opposition and implementation decide whether the version changes. Old orders and commitments persist through a defined transition.

Compare local service, neighboring users, supplier capacity, waste, burdens, existing local repair and later resilience. Keep qualitative interests and disagreement visible. Widen causal closure consistently where a former external driver is modeled internally. Changing the evaluative scope need not change physical structure. Check apparent improvement against report selection and reference history rather than only the proxy target.

Independently, the analyst preserves the original forecast, compares it with source evidence and revises the explanatory model if justified. That revision does not itself teach or command the represented actor. An observed discrepancy may leave several causes unresolved. The account is coherent across all seven chapters without adding another physical stock per practice, but no dynamics or empirical result were executed in this walkthrough.

### 49.5 Acceptance verdict and remaining limits

**Accept as a robust working conceptual baseline for the requested first seven chapters, after the repairs above.** At the granularity of the retained source assessments, all 346 catalogue units have requirement and prospective-case allocations; all eight traps, twelve leverage positions and fifteen final-chapter practices are represented. No unresolved contradiction was identified among the reviewed accounting, identity, knowledge-ownership, change-status, scale, temporal and evidence contracts. This is an assessed design judgment, not a proof of exhaustive sentence-level extraction or absence of unknown interfaces.

Do not equate this acceptance with a complete model of reality or qualified intelligence. The book is a foundation for asking and testing system questions; it does not specify all domain laws, hidden human mechanisms, causal identification procedures, experiment selection or a universally competent updater. An actual model still requires domain evidence, explicit dynamics where needed, executable checks, out-of-sample discrimination and intervention/transition evaluation. Empirical causal truth, predictive quality, policy effectiveness, autonomous discovery and social adoption remain unestablished. Speed, tokens, energy, availability and arbitrary scaling have not been measured.

**All 192 model scenarios remain PLANNED — NOT RUN.** Successful document checks establish that the specified representation and traceability are internally organized; they are not successful model executions. The next development decision can use this baseline without another compulsory expansion of the diagram, while keeping these qualification boundaries visible.

## 50. Canonical complete seven-chapter foundation traceability

The 346 rows below are the current cumulative allocation. Earlier crosswalks are retained history and are not extra unique foundations. Detailed meanings remain in the chapter catalogues; every row links the source foundation to integrated requirements and prospective checks. Allocation is a review claim, not empirical confirmation.

| Foundation | Printed pages | Mechanism sections / parent obligations | Cumulative requirements | Prospective cases |
| --- | --- | --- | --- | --- |
| B01 | 11–13 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| B02 | 12–13, 18 | 4.2 | I7-R01 | I7-T01 |
| B03 | 11–13, 15 | 4.1, 7, 13.6 | I7-R01, I7-R09, I7-R17 | I7-T01, I7-T09, I7-T23, I7-T24 |
| B04 | 12 | 6.2–6.4 | I7-R06, I7-R07, I7-R09, I7-R10 | I7-T06, I7-T07, I7-T09, I7-T10 |
| B05 | 11, 13–14 | 4.4–4.6, 7 | I7-R02, I7-R04, I7-R09, I7-R16 | I7-T02, I7-T04, I7-T09, I7-T15, I7-T16, I7-T21 |
| B06 | 12–14 | 5.1 | I7-R11 | I7-T11, I7-T26, I7-T28 |
| B07 | 11, 14–15 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| B08 | 14–15 | 4.7, 5.1 | I7-R05, I7-R11 | I7-T05, I7-T11, I7-T26, I7-T27, I7-T28 |
| B09 | 15–16 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| B10 | 16 | 5.3 | I7-R01, I7-R14 | I7-T01, I7-T14 |
| B11 | 16–17 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| B12 | 17–18 | 4.3 | I7-R02, I7-R03 | I7-T02, I7-T03, I7-T15 |
| B13 | 18 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| B14 | 18–19 | 4.4 | I7-R02, I7-R04 | I7-T02, I7-T04, I7-T15, I7-T16 |
| B15 | 18, 22 | 4.1, 13.5 | I7-R01, I7-R17, I7-R18 | I7-T01, I7-T22, I7-T23, I7-T24 |
| B16 | 18–19 | 4.4, 7 | I7-R02, I7-R04, I7-R09 | I7-T02, I7-T04, I7-T09, I7-T15, I7-T16 |
| B17 | 20–22 | 6.1 | I7-R02, I7-R04, I7-R18 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T22 |
| B18 | 20–22 | 13.4 | I7-R02 | I7-T02, I7-T15 |
| B19 | 22 | 13.4 | I7-R02 | I7-T02, I7-T15 |
| B20 | 17, 23 | 5.2, 6.1 | I7-R02, I7-R03, I7-R04, I7-R18, I7-R19 | I7-T02, I7-T03, I7-T04, I7-T15, I7-T16, I7-T22, I7-T25 |
| B21 | 23–24 | 4.3, 8 | I7-R02, I7-R03, I7-R07 | I7-T02, I7-T03, I7-T07, I7-T15 |
| B22 | 19–22 | 4.9 | I7-R12 | I7-T12, I7-T27, I7-T28 |
| B23 | 14, 24–26 | 4.5–4.6 | I7-R04, I7-R15, I7-R16, I7-R20 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T20, I7-T21 |
| B24 | 25–27 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B25 | 27 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B26 | 18, 26 | 7 | I7-R09 | I7-T09 |
| B27 | 26–29 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| B28 | 27–30 | 4.8, 13.3 | I7-R04, I7-R05, I7-R12 | I7-T04, I7-T05, I7-T12, I7-T16, I7-T27, I7-T28 |
| B29 | 28–29 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| B30 | 27–28 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| B31 | 30 | 6.2, 7 | I7-R06, I7-R07, I7-R09 | I7-T06, I7-T07, I7-T09 |
| B32 | 30–33 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| B33 | 31–33 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| B34 | 33–34 | 7 | I7-R09 | I7-T09 |
| B35 | 34 | 4.6, 4.8 | I7-R04, I7-R12, I7-R16 | I7-T04, I7-T12, I7-T16, I7-T21, I7-T27, I7-T28 |
| B36 | 20–22, 28–34 | 9, 14 | I7-R11, I7-R12, I7-R13 | I7-T11, I7-T12, I7-T13, I7-T26, I7-T27, I7-T28 |
| Z01 | 35 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z02 | 36–42 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| Z03 | 36–38 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| Z04 | 36–38 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z05 | 37–38 | 4.6, 14 | I7-R04, I7-R12, I7-R13, I7-R16 | I7-T04, I7-T12, I7-T13, I7-T16, I7-T21, I7-T27, I7-T28 |
| Z06 | 38–40 | 13.3 | I7-R05 | I7-T05, I7-T27 |
| Z07 | 38–40 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| Z08 | 39 | 7, 13.1 | I7-R09, I7-R11 | I7-T09, I7-T11, I7-T26, I7-T28 |
| Z09 | 40–41 | 6.1 | I7-R02, I7-R04, I7-R18 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T22 |
| Z10 | 40–42, 44–45 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| Z11 | 42–45 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z12 | 44–47 | 4.6, 9 | I7-R04, I7-R11, I7-R12, I7-R16 | I7-T04, I7-T11, I7-T12, I7-T16, I7-T21, I7-T26, I7-T27, I7-T28 |
| Z13 | 45–47 | 4.9, 9 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| Z14 | 42–48 | 5.1, 13.1 | I7-R11 | I7-T11, I7-T26, I7-T28 |
| Z15 | 45–48 | 9 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| Z16 | 48 | 4.1, 9 | I7-R01, I7-R11, I7-R12, I7-R17 | I7-T01, I7-T11, I7-T12, I7-T23, I7-T24, I7-T26, I7-T27, I7-T28 |
| Z17 | 48–51 | 13.7 | I7-R13 | I7-T13 |
| Z18 | 49–50 | 4.2, 14 | I7-R01, I7-R12, I7-R13 | I7-T01, I7-T12, I7-T13, I7-T27, I7-T28 |
| Z19 | 50–51 | 7, 14 | I7-R09, I7-R12, I7-R13 | I7-T09, I7-T12, I7-T13, I7-T27, I7-T28 |
| Z20 | 51–53 | 8.1 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z21 | 52–55 | 5.2, 8.1 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z22 | 52–54 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| Z23 | 53–54 | 8.1, 13.2 | I7-R03, I7-R14, I7-R19 | I7-T03, I7-T14, I7-T25 |
| Z24 | 52–55 | 8.6 | I7-R12, I7-R19 | I7-T12, I7-T25, I7-T27, I7-T28 |
| Z25 | 55–57 | 8.6 | I7-R12, I7-R19 | I7-T12, I7-T25, I7-T27, I7-T28 |
| Z26 | 55–57 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| Z27 | 58 | 7 | I7-R09 | I7-T09 |
| Z28 | 58–60 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| Z29 | 60–62 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z30 | 61–62 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z31 | 61–64 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z32 | 63–64 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| Z33 | 64–66 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z34 | 65–66 | 13.5 | I7-R17, I7-R18 | I7-T22, I7-T23, I7-T24 |
| Z35 | 66–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z36 | 66 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z37 | 66–67 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z38 | 67 | 4.6, 14 | I7-R04, I7-R12, I7-R13, I7-R16 | I7-T04, I7-T12, I7-T13, I7-T16, I7-T21, I7-T27, I7-T28 |
| Z39 | 68–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z40 | 69–71 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z41 | 71 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| Z42 | 71–72 | 14 | I7-R12, I7-R13 | I7-T12, I7-T13, I7-T27, I7-T28 |
| F01 | 75 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| F02 | 75 | 4.2 | I7-R01 | I7-T01 |
| F03 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F04 | 76 | 4.8 | I7-R04, I7-R12 | I7-T04, I7-T12, I7-T16, I7-T27, I7-T28 |
| F05 | 76 | 5.2 | I7-R03, I7-R19 | I7-T03, I7-T25 |
| F06 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F07 | 76 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F08 | 76 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F09 | 77 | 4.1 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| F10 | 77–78 | 4.9 | I7-R12 | I7-T12, I7-T27, I7-T28 |
| F11 | 77–78 | 4.7 | I7-R05 | I7-T05, I7-T27 |
| F12 | 78 | 6.2 | I7-R06, I7-R07 | I7-T06, I7-T07 |
| F13 | 79 | 6.3, 13.2 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F14 | 79–80 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F15 | 80 | 6.3–6.4 | I7-R08, I7-R09, I7-R10, I7-R14 | I7-T08, I7-T09, I7-T10, I7-T14 |
| F16 | 79–80 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F17 | 80 | 6.3 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F18 | 81 | 6.3, 12 | I7-R08, I7-R14 | I7-T08, I7-T14 |
| F19 | 80–81 | 9, 13.2 | I7-R11, I7-R12, I7-R14 | I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| F20 | 82 | 13.6 | I7-R01, I7-R09 | I7-T01, I7-T09 |
| F21 | 82 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F22 | 82–83 | 4.2, 14 | I7-R01, I7-R12, I7-R13 | I7-T01, I7-T12, I7-T13, I7-T27, I7-T28 |
| F23 | 83 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F24 | 83 | 4.5 | I7-R15, I7-R20 | I7-T17, I7-T18, I7-T19, I7-T20 |
| F25 | 83 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F26 | 83–84 | 4.1, 7 | I7-R01, I7-R09, I7-R17 | I7-T01, I7-T09, I7-T23, I7-T24 |
| F27 | 84 | 5.3, 9 | I7-R01, I7-R11, I7-R12, I7-R14 | I7-T01, I7-T11, I7-T12, I7-T14, I7-T26, I7-T27, I7-T28 |
| F28 | 84 | 6.3–6.4 | I7-R08, I7-R09, I7-R10, I7-R14 | I7-T08, I7-T09, I7-T10, I7-T14 |
| F29 | 84–85 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| F30 | 84–85 | 4.7, 6.4 | I7-R05, I7-R09, I7-R10 | I7-T05, I7-T09, I7-T10, I7-T27 |
| F31 | 85 | 6.4, 7 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| F32 | 85 | 6.4 | I7-R09, I7-R10 | I7-T09, I7-T10 |
| U01 | 86 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U02 | 86–87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U03 | 87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U04 | 87 | 5.1, 9, 15, 21 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U05 | 88 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U06 | 88 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U07 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U08 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U09 | 89 | 4.9, 9, 20 | I7-R11, I7-R12 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| U10 | 90 | 4.6, 9, 17 | I7-R04, I7-R11, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T11, I7-T12, I7-T16, I7-T21, I7-T22, I7-T25, I7-T26, I7-T27, I7-T28 |
| U11 | 91 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U12 | 91–92 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U13 | 92, 94 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U14 | 93 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U15 | 94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U16 | 93–94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U17 | 94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U18 | 93–94 | 6.2, 17, 20 | I7-R06, I7-R07, I7-R12, I7-R16, I7-R18, I7-R19 | I7-T06, I7-T07, I7-T12, I7-T21, I7-T22, I7-T25, I7-T27, I7-T28 |
| U19 | 95 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U20 | 95 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U21 | 95–96 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U22 | 96 | 4.1, 4.4, 13.5, 18 | I7-R01, I7-R02, I7-R04, I7-R17, I7-R18 | I7-T01, I7-T02, I7-T04, I7-T15, I7-T16, I7-T22, I7-T23, I7-T24 |
| U23 | 96–97 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U24 | 97 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U25 | 97–98 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U26 | 98 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U27 | 98–99 | 4.1, 18 | I7-R01, I7-R17 | I7-T01, I7-T23, I7-T24 |
| U28 | 100–101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U29 | 101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U30 | 101 | 4.6, 17 | I7-R04, I7-R16, I7-R18, I7-R19 | I7-T04, I7-T16, I7-T21, I7-T22, I7-T25 |
| U31 | 102 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U32 | 102 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U33 | 102–103 | 6.1, 17 | I7-R02, I7-R04, I7-R16, I7-R18, I7-R19 | I7-T02, I7-T04, I7-T15, I7-T16, I7-T21, I7-T22, I7-T25 |
| U34 | 103–104 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U35 | 103 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U36 | 104 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U37 | 104–105 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U38 | 105 | 5.2, 17 | I7-R03, I7-R16, I7-R18, I7-R19 | I7-T03, I7-T21, I7-T22, I7-T25 |
| U39 | 106 | 4.5, 16 | I7-R15, I7-R20 | I7-T17, I7-T18, I7-T19, I7-T20 |
| U40 | 106 | 4.6, 16 | I7-R04, I7-R15, I7-R16 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T21 |
| U41 | 107 | 4.6, 16 | I7-R04, I7-R15, I7-R16 | I7-T04, I7-T16, I7-T17, I7-T18, I7-T19, I7-T21 |
| U42 | 107–108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U43 | 106–108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U44 | 108, 110 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U45 | 108 | 4.7, 6.4, 16 | I7-R05, I7-R09, I7-R10, I7-R15 | I7-T05, I7-T09, I7-T10, I7-T17, I7-T18, I7-T19, I7-T27 |
| U46 | 109 | 7, 16, 19 | I7-R09, I7-R15, I7-R20 | I7-T09, I7-T17, I7-T18, I7-T19, I7-T20 |
| U47 | 109 | 7, 16, 19 | I7-R09, I7-R15, I7-R20 | I7-T09, I7-T17, I7-T18, I7-T19, I7-T20 |
| U48 | 109–110 | 4.7, 9, 20 | I7-R05, I7-R11, I7-R12 | I7-T05, I7-T11, I7-T12, I7-T26, I7-T27, I7-T28 |
| C5-F01 | 111 | 22–28 | I7-R21 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F02 | 111–112 | 22–28 | I7-R21, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F03 | 112 | 22–28 | I7-R21 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F04 | 112 | 22–28 | I7-R28, I7-R30 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T60, I7-T62, I7-T63, I7-T64, I7-T66 |
| C5-F05 | 112–113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F06 | 113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F07 | 113 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F08 | 113–114 | 22–28 | I7-R21, I7-R23, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F09 | 114–115 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F10 | 115–116 | 22–28 | I7-R21, I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F11 | 116–117 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F12 | 117–118 | 22–28 | I7-R22, I7-R30 | I7-T33, I7-T34, I7-T35, I7-T36, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F13 | 117–119 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F14 | 117–118 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F15 | 118 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F16 | 119 | 22–28 | I7-R22, I7-R28 | I7-T33, I7-T34, I7-T35, I7-T36, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F17 | 119–120 | 22–28 | I7-R21, I7-R22 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T33, I7-T34, I7-T35, I7-T36, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F18 | 119–121 | 22–28 | I7-R22 | I7-T33, I7-T34, I7-T35, I7-T36 |
| C5-F19 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F20 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F21 | 122 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F22 | 122–123 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F23 | 123 | 22–28 | I7-R23, I7-R28 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T35, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F24 | 124 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F25 | 124–125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F26 | 125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F27 | 124–125 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F28 | 125–126 | 22–28 | I7-R23 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44 |
| C5-F29 | 125–126 | 22–28 | I7-R23, I7-R28 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T35, I7-T37, I7-T38, I7-T39, I7-T40, I7-T41, I7-T42, I7-T43, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F30 | 126–127 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F31 | 127 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F32 | 127–129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F33 | 128–129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F34 | 129 | 22–28 | I7-R24 | I7-T45, I7-T46, I7-T47, I7-T48 |
| C5-F35 | 129 | 22–28 | I7-R24, I7-R30 | I7-T45, I7-T46, I7-T47, I7-T48, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F36 | 129–130 | 22–28 | I7-R24, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T45, I7-T46, I7-T47, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F37 | 131–132 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F38 | 132–133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F39 | 132–133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F40 | 132–133 | 22–28 | I7-R21, I7-R25 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T49, I7-T50, I7-T51, I7-T52, I7-T61, I7-T62, I7-T67, I7-T68 |
| C5-F41 | 133–135 | 22–28 | I7-R25, I7-R30 | I7-T49, I7-T50, I7-T51, I7-T52, I7-T60, I7-T62, I7-T63, I7-T64 |
| C5-F42 | 133 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F43 | 134–135 | 22–28 | I7-R25 | I7-T49, I7-T50, I7-T51, I7-T52 |
| C5-F44 | 134–135 | 22–28 | I7-R25, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T49, I7-T50, I7-T51, I7-T52, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66 |
| C5-F45 | 136 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F46 | 136–137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F47 | 137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F48 | 137 | 22–28 | I7-R26, I7-R27 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F49 | 137 | 22–28 | I7-R26, I7-R27, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T63, I7-T64, I7-T66 |
| C5-F50 | 138 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F51 | 138–139 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F52 | 139–140 | 22–28 | I7-R26 | I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60 |
| C5-F53 | 140 | 22–28 | I7-R26, I7-R28 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T63, I7-T64, I7-T66 |
| C5-F54 | 140–141 | 22–28 | I7-R21, I7-R26, I7-R30 | I7-T29, I7-T30, I7-T31, I7-T32, I7-T53, I7-T54, I7-T55, I7-T56, I7-T57, I7-T58, I7-T59, I7-T60, I7-T61, I7-T62, I7-T63, I7-T64, I7-T67, I7-T68 |
| C5-F55 | 141 | 22–28 | I7-R29 | I7-T65 |
| C5-F56 | 141 | 22–28 | I7-R28, I7-R29 | I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T65, I7-T66 |
| C6-F01 | 145–146 | 4, 32–39 | I7-R31 | I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F02 | 146–147 | 4, 32–39 | I7-R11, I7-R12, I7-R31 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F03 | 147 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F04 | 145–147 | 4, 32–39 | I7-R14, I7-R28, I7-R31 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F05 | 147–148 | 4, 32–39 | I7-R32 | I7-T69, I7-T70, I7-T71, I7-T105, I7-T120 |
| C6-F06 | 147 | 4, 32–39 | I7-R32 | I7-T69, I7-T70, I7-T71, I7-T105, I7-T120 |
| C6-F07 | 148 | 4, 32–39 | I7-R32 | I7-T69, I7-T70, I7-T71, I7-T105, I7-T120 |
| C6-F08 | 148 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R32 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T69, I7-T70, I7-T71, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F09 | 149 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R32 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T69, I7-T70, I7-T71, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F10 | 149–150 | 4, 32–39 | I7-R33 | I7-T72, I7-T73, I7-T74, I7-T117 |
| C6-F11 | 150 | 4, 32–39 | I7-R33 | I7-T72, I7-T73, I7-T74, I7-T117 |
| C6-F12 | 150 | 4, 32–39 | I7-R33 | I7-T72, I7-T73, I7-T74, I7-T117 |
| C6-F13 | 150 | 4, 32–39 | I7-R33 | I7-T72, I7-T73, I7-T74, I7-T117 |
| C6-F14 | 150 | 4, 32–39 | I7-R34 | I7-T75, I7-T76, I7-T77, I7-T109, I7-T117 |
| C6-F15 | 151 | 4, 32–39 | I7-R34 | I7-T75, I7-T76, I7-T77, I7-T109, I7-T117 |
| C6-F16 | 151 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R34 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T75, I7-T76, I7-T77, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T117, I7-T120, I7-T124 |
| C6-F17 | 151 | 4, 32–39 | I7-R34 | I7-T75, I7-T76, I7-T77, I7-T109, I7-T117 |
| C6-F18 | 151–152 | 4, 32–39 | I7-R35 | I7-T78, I7-T79, I7-T80, I7-T120 |
| C6-F19 | 152 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R35 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T78, I7-T79, I7-T80, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F20 | 152 | 4, 32–39 | I7-R35 | I7-T78, I7-T79, I7-T80, I7-T120 |
| C6-F21 | 152 | 4, 32–39 | I7-R35 | I7-T78, I7-T79, I7-T80, I7-T120 |
| C6-F22 | 152 | 4, 32–39 | I7-R35 | I7-T78, I7-T79, I7-T80, I7-T120 |
| C6-F23 | 153 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F24 | 153 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F25 | 153 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F26 | 153–154 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R36 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T121, I7-T124 |
| C6-F27 | 154–155 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F28 | 155 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F29 | 155–156 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F30 | 156 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F31 | 156 | 4, 32–39 | I7-R36 | I7-T81, I7-T82, I7-T83, I7-T84, I7-T85, I7-T86, I7-T121 |
| C6-F32 | 156–157 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R37 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T87, I7-T88, I7-T89, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T121, I7-T123, I7-T124 |
| C6-F33 | 157 | 4, 32–39 | I7-R37 | I7-T87, I7-T88, I7-T89, I7-T121, I7-T123 |
| C6-F34 | 157 | 4, 32–39 | I7-R37 | I7-T87, I7-T88, I7-T89, I7-T121, I7-T123 |
| C6-F35 | 157 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R37 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T87, I7-T88, I7-T89, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T121, I7-T123, I7-T124 |
| C6-F36 | 157 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R37 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T87, I7-T88, I7-T89, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T121, I7-T123, I7-T124 |
| C6-F37 | 158 | 4, 32–39 | I7-R38 | I7-T90, I7-T91, I7-T92, I7-T119, I7-T122 |
| C6-F38 | 158 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R38 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T90, I7-T91, I7-T92, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T119, I7-T120, I7-T122, I7-T124 |
| C6-F39 | 158 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R38 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T90, I7-T91, I7-T92, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T119, I7-T120, I7-T122, I7-T124 |
| C6-F40 | 158–159 | 4, 32–39 | I7-R38 | I7-T90, I7-T91, I7-T92, I7-T119, I7-T122 |
| C6-F41 | 159 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R39 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T93, I7-T94, I7-T95, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T119, I7-T120, I7-T124 |
| C6-F42 | 159 | 4, 32–39 | I7-R39 | I7-T93, I7-T94, I7-T95, I7-T119 |
| C6-F43 | 160 | 4, 32–39 | I7-R39 | I7-T93, I7-T94, I7-T95, I7-T119 |
| C6-F44 | 160 | 4, 32–39 | I7-R39 | I7-T93, I7-T94, I7-T95, I7-T119 |
| C6-F45 | 160–161 | 4, 32–39 | I7-R39 | I7-T93, I7-T94, I7-T95, I7-T119 |
| C6-F46 | 161 | 4, 32–39 | I7-R40 | I7-T96, I7-T97, I7-T98, I7-T119, I7-T122 |
| C6-F47 | 161 | 4, 32–39 | I7-R40 | I7-T96, I7-T97, I7-T98, I7-T119, I7-T122 |
| C6-F48 | 161–162 | 4, 32–39 | I7-R40 | I7-T96, I7-T97, I7-T98, I7-T119, I7-T122 |
| C6-F49 | 162 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R40 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T96, I7-T97, I7-T98, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T119, I7-T120, I7-T122, I7-T124 |
| C6-F50 | 162–163 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R41 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T99, I7-T100, I7-T101, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T122, I7-T123, I7-T124 |
| C6-F51 | 163 | 4, 32–39 | I7-R41 | I7-T99, I7-T100, I7-T101, I7-T118, I7-T122, I7-T123 |
| C6-F52 | 163 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R41 | I7-T01, I7-T02, I7-T11, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T99, I7-T100, I7-T101, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T122, I7-T123, I7-T124 |
| C6-F53 | 163–164 | 4, 32–39 | I7-R14, I7-R28, I7-R31, I7-R41 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T99, I7-T100, I7-T101, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T122, I7-T123, I7-T124 |
| C6-F54 | 164 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R41 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T99, I7-T100, I7-T101, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T122, I7-T123, I7-T124 |
| C6-F55 | 164 | 4, 32–39 | I7-R42 | I7-T102, I7-T103, I7-T104, I7-T118, I7-T123, I7-T124 |
| C6-F56 | 164 | 4, 32–39 | I7-R42 | I7-T102, I7-T103, I7-T104, I7-T118, I7-T123, I7-T124 |
| C6-F57 | 164–165 | 4, 32–39 | I7-R42 | I7-T102, I7-T103, I7-T104, I7-T118, I7-T123, I7-T124 |
| C6-F58 | 164–165 | 4, 32–39 | I7-R11, I7-R12, I7-R31, I7-R42 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T102, I7-T103, I7-T104, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T118, I7-T120, I7-T123, I7-T124 |
| C6-F59 | 165 | 4, 32–39 | I7-R11, I7-R12, I7-R31 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F60 | 165 | 4, 32–39 | I7-R14, I7-R28, I7-R31 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F61 | 165 | 4, 32–39 | I7-R14, I7-R28, I7-R31 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F62 | 146–147, 165 | 4, 32–39 | I7-R11, I7-R12, I7-R31 | I7-T11, I7-T12, I7-T26, I7-T27, I7-T28, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F63 | 147, 165 | 4, 32–39 | I7-R01, I7-R02, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31 | I7-T01, I7-T02, I7-T11, I7-T12, I7-T14, I7-T15, I7-T17, I7-T18, I7-T19, I7-T20, I7-T23, I7-T24, I7-T26, I7-T27, I7-T28, I7-T60, I7-T62, I7-T63, I7-T64, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C6-F64 | 165 | 4, 32–39 | I7-R14, I7-R28, I7-R31 | I7-T14, I7-T35, I7-T39, I7-T44, I7-T48, I7-T51, I7-T55, I7-T59, I7-T63, I7-T64, I7-T66, I7-T105, I7-T106, I7-T107, I7-T108, I7-T109, I7-T110, I7-T111, I7-T112, I7-T113, I7-T114, I7-T115, I7-T116, I7-T120, I7-T124 |
| C7-F01 | 166–169 | 43–46; C7-R01, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R20, I7-R28, I7-R30, I7-R31, I7-R41, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T170, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F02 | 167 | 43–46; C7-R01 | I7-R11, I7-R12, I7-R15, I7-R28, I7-R31, I7-R41, I7-R42, I7-R54 | I7-T170, I7-T171, I7-T179, I7-T184 |
| C7-F03 | 168–169 | 43–46; C7-R01 | I7-R11, I7-R12, I7-R15, I7-R28, I7-R31, I7-R41, I7-R42, I7-R54 | I7-T170, I7-T171, I7-T179, I7-T184 |
| C7-F04 | 168–169 | 43–46; C7-R01 | I7-R11, I7-R12, I7-R15, I7-R28, I7-R31, I7-R41, I7-R42, I7-R54 | I7-T170, I7-T171, I7-T179, I7-T184 |
| C7-F05 | 169–170 | 43–46; C7-R01 | I7-R11, I7-R12, I7-R15, I7-R28, I7-R31, I7-R41, I7-R42, I7-R54 | I7-T170, I7-T171, I7-T179, I7-T184 |
| C7-F06 | 170 | 43–46; C7-R01, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R20, I7-R28, I7-R30, I7-R31, I7-R41, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T170, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F07 | 170–171 | 43–46; C7-R02 | I7-R03, I7-R11, I7-R12, I7-R16, I7-R19, I7-R43 | I7-T125, I7-T126, I7-T127 |
| C7-F08 | 171 | 43–46; C7-R02 | I7-R03, I7-R11, I7-R12, I7-R16, I7-R19, I7-R43 | I7-T125, I7-T126, I7-T127 |
| C7-F09 | 171 | 43–46; C7-R02 | I7-R03, I7-R11, I7-R12, I7-R16, I7-R19, I7-R43 | I7-T125, I7-T126, I7-T127 |
| C7-F10 | 171–172 | 43–46; C7-R02 | I7-R03, I7-R11, I7-R12, I7-R16, I7-R19, I7-R43 | I7-T125, I7-T126, I7-T127 |
| C7-F11 | 172 | 43–46; C7-R03 | I7-R02, I7-R11, I7-R12, I7-R13, I7-R42, I7-R48, I7-R54 | I7-T128, I7-T129, I7-T130 |
| C7-F12 | 172 | 43–46; C7-R03 | I7-R02, I7-R11, I7-R12, I7-R13, I7-R42, I7-R48, I7-R54 | I7-T128, I7-T129, I7-T130 |
| C7-F13 | 172 | 43–46; C7-R03 | I7-R02, I7-R11, I7-R12, I7-R13, I7-R42, I7-R48, I7-R54 | I7-T128, I7-T129, I7-T130 |
| C7-F14 | 172 | 43–46; C7-R03, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R11, I7-R12, I7-R13, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T128, I7-T129, I7-T130, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F15 | 173 | 43–46; C7-R04, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R11, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R37, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T131, I7-T132, I7-T133, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F16 | 173 | 43–46; C7-R04 | I7-R11, I7-R15, I7-R20, I7-R37, I7-R53 | I7-T131, I7-T132, I7-T133 |
| C7-F17 | 173 | 43–46; C7-R04 | I7-R11, I7-R15, I7-R20, I7-R37, I7-R53 | I7-T131, I7-T132, I7-T133 |
| C7-F18 | 173 | 43–46; C7-R04 | I7-R11, I7-R15, I7-R20, I7-R37, I7-R53 | I7-T131, I7-T132, I7-T133 |
| C7-F19 | 174 | 43–46; C7-R05 | I7-R01, I7-R02, I7-R11, I7-R13, I7-R15, I7-R17, I7-R44 | I7-T134, I7-T135, I7-T136 |
| C7-F20 | 174–175 | 43–46; C7-R05 | I7-R01, I7-R02, I7-R11, I7-R13, I7-R15, I7-R17, I7-R44 | I7-T134, I7-T135, I7-T136 |
| C7-F21 | 175 | 43–46; C7-R05 | I7-R01, I7-R02, I7-R11, I7-R13, I7-R15, I7-R17, I7-R44 | I7-T134, I7-T135, I7-T136 |
| C7-F22 | 174–175 | 43–46; C7-R05, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R11, I7-R13, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T134, I7-T135, I7-T136, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F23 | 175–176 | 43–46; C7-R06 | I7-R05, I7-R11, I7-R12, I7-R26, I7-R40, I7-R45 | I7-T137, I7-T138, I7-T139 |
| C7-F24 | 176 | 43–46; C7-R06 | I7-R05, I7-R11, I7-R12, I7-R26, I7-R40, I7-R45 | I7-T137, I7-T138, I7-T139 |
| C7-F25 | 176 | 43–46; C7-R06, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R05, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R20, I7-R26, I7-R30, I7-R31, I7-R40, I7-R42, I7-R44, I7-R45, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T137, I7-T138, I7-T139, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F26 | 176–177 | 43–46; C7-R06 | I7-R05, I7-R11, I7-R12, I7-R26, I7-R40, I7-R45 | I7-T137, I7-T138, I7-T139 |
| C7-F27 | 177 | 43–46; C7-R07 | I7-R04, I7-R15, I7-R19, I7-R27, I7-R31, I7-R35, I7-R36, I7-R46 | I7-T140, I7-T141, I7-T172 |
| C7-F28 | 177–178 | 43–46; C7-R08 | I7-R08, I7-R14, I7-R19, I7-R28, I7-R31, I7-R38, I7-R40, I7-R47 | I7-T142, I7-T172, I7-T173, I7-T178 |
| C7-F29 | 177–178 | 43–46; C7-R08, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R08, I7-R11, I7-R14, I7-R15, I7-R17, I7-R19, I7-R20, I7-R28, I7-R30, I7-R31, I7-R38, I7-R40, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T142, I7-T171, I7-T172, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F30 | 177 | 43–46; C7-R07, C7-R08 | I7-R04, I7-R08, I7-R14, I7-R15, I7-R19, I7-R27, I7-R28, I7-R31, I7-R35, I7-R36, I7-R38, I7-R40, I7-R46, I7-R47 | I7-T140, I7-T141, I7-T142, I7-T172, I7-T173, I7-T178 |
| C7-F31 | 178 | 43–46; C7-R09 | I7-R05, I7-R09, I7-R10, I7-R17, I7-R26, I7-R30, I7-R50 | I7-T143, I7-T144, I7-T145 |
| C7-F32 | 178 | 43–46; C7-R09 | I7-R05, I7-R09, I7-R10, I7-R17, I7-R26, I7-R30, I7-R50 | I7-T143, I7-T144, I7-T145 |
| C7-F33 | 178 | 43–46; C7-R09 | I7-R05, I7-R09, I7-R10, I7-R17, I7-R26, I7-R30, I7-R50 | I7-T143, I7-T144, I7-T145 |
| C7-F34 | 178 | 43–46; C7-R09 | I7-R05, I7-R09, I7-R10, I7-R17, I7-R26, I7-R30, I7-R50 | I7-T143, I7-T144, I7-T145 |
| C7-F35 | 178 | 43–46; C7-R10 | I7-R06, I7-R07, I7-R10, I7-R25, I7-R36, I7-R54 | I7-T146, I7-T147, I7-T148 |
| C7-F36 | 178–179 | 43–46; C7-R10 | I7-R06, I7-R07, I7-R10, I7-R25, I7-R36, I7-R54 | I7-T146, I7-T147, I7-T148 |
| C7-F37 | 178–179 | 43–46; C7-R10 | I7-R06, I7-R07, I7-R10, I7-R25, I7-R36, I7-R54 | I7-T146, I7-T147, I7-T148 |
| C7-F38 | 179 | 43–46; C7-R10 | I7-R06, I7-R07, I7-R10, I7-R25, I7-R36, I7-R54 | I7-T146, I7-T147, I7-T148 |
| C7-F39 | 179 | 43–46; C7-R11 | I7-R05, I7-R09, I7-R15, I7-R22, I7-R26, I7-R37, I7-R38, I7-R49 | I7-T149, I7-T150, I7-T151 |
| C7-F40 | 179 | 43–46; C7-R11 | I7-R05, I7-R09, I7-R15, I7-R22, I7-R26, I7-R37, I7-R38, I7-R49 | I7-T149, I7-T150, I7-T151 |
| C7-F41 | 179 | 43–46; C7-R11 | I7-R05, I7-R09, I7-R15, I7-R22, I7-R26, I7-R37, I7-R38, I7-R49 | I7-T149, I7-T150, I7-T151 |
| C7-F42 | 179–180 | 43–46; C7-R11 | I7-R05, I7-R09, I7-R15, I7-R22, I7-R26, I7-R37, I7-R38, I7-R49 | I7-T149, I7-T150, I7-T151 |
| C7-F43 | 180 | 43–46; C7-R12 | I7-R11, I7-R12, I7-R14, I7-R28, I7-R31, I7-R42, I7-R48 | I7-T152, I7-T153, I7-T154 |
| C7-F44 | 180 | 43–46; C7-R12 | I7-R11, I7-R12, I7-R14, I7-R28, I7-R31, I7-R42, I7-R48 | I7-T152, I7-T153, I7-T154 |
| C7-F45 | 180–181 | 43–46; C7-R12, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R20, I7-R28, I7-R30, I7-R31, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T152, I7-T153, I7-T154, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F46 | 181 | 43–46; C7-R12 | I7-R11, I7-R12, I7-R14, I7-R28, I7-R31, I7-R42, I7-R48 | I7-T152, I7-T153, I7-T154 |
| C7-F47 | 181 | 43–46; C7-R13 | I7-R04, I7-R06, I7-R08, I7-R12, I7-R16, I7-R29, I7-R54 | I7-T155, I7-T156, I7-T157 |
| C7-F48 | 181–182 | 43–46; C7-R13 | I7-R04, I7-R06, I7-R08, I7-R12, I7-R16, I7-R29, I7-R54 | I7-T155, I7-T156, I7-T157 |
| C7-F49 | 181–182 | 43–46; C7-R13 | I7-R04, I7-R06, I7-R08, I7-R12, I7-R16, I7-R29, I7-R54 | I7-T155, I7-T156, I7-T157 |
| C7-F50 | 182 | 43–46; C7-R13 | I7-R04, I7-R06, I7-R08, I7-R12, I7-R16, I7-R29, I7-R54 | I7-T155, I7-T156, I7-T157 |
| C7-F51 | 182 | 43–46; C7-R14 | I7-R03, I7-R12, I7-R14, I7-R19, I7-R34, I7-R35, I7-R51 | I7-T158, I7-T159, I7-T160 |
| C7-F52 | 183 | 43–46; C7-R14, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R19, I7-R20, I7-R30, I7-R31, I7-R34, I7-R35, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R51, I7-R53, I7-R54 | I7-T158, I7-T159, I7-T160, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F53 | 183 | 43–46; C7-R14 | I7-R03, I7-R12, I7-R14, I7-R19, I7-R34, I7-R35, I7-R51 | I7-T158, I7-T159, I7-T160 |
| C7-F54 | 183 | 43–46; C7-R14 | I7-R03, I7-R12, I7-R14, I7-R19, I7-R34, I7-R35, I7-R51 | I7-T158, I7-T159, I7-T160 |
| C7-F55 | 183 | 43–46; C7-R15 | I7-R01, I7-R02, I7-R09, I7-R11, I7-R13, I7-R17, I7-R44 | I7-T161, I7-T162, I7-T163 |
| C7-F56 | 183 | 43–46; C7-R15 | I7-R01, I7-R02, I7-R09, I7-R11, I7-R13, I7-R17, I7-R44 | I7-T161, I7-T162, I7-T163 |
| C7-F57 | 183 | 43–46; C7-R15 | I7-R01, I7-R02, I7-R09, I7-R11, I7-R13, I7-R17, I7-R44 | I7-T161, I7-T162, I7-T163 |
| C7-F58 | 183 | 43–46; C7-R15, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R09, I7-R11, I7-R13, I7-R14, I7-R15, I7-R17, I7-R20, I7-R30, I7-R31, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T161, I7-T162, I7-T163, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F59 | 184 | 43–46; C7-R16 | I7-R05, I7-R10, I7-R12, I7-R17, I7-R22, I7-R26, I7-R40, I7-R50 | I7-T164, I7-T165, I7-T166 |
| C7-F60 | 184 | 43–46; C7-R16 | I7-R05, I7-R10, I7-R12, I7-R17, I7-R22, I7-R26, I7-R40, I7-R50 | I7-T164, I7-T165, I7-T166 |
| C7-F61 | 184 | 43–46; C7-R16 | I7-R05, I7-R10, I7-R12, I7-R17, I7-R22, I7-R26, I7-R40, I7-R50 | I7-T164, I7-T165, I7-T166 |
| C7-F62 | 184 | 43–46; C7-R16, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R05, I7-R10, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R20, I7-R22, I7-R26, I7-R30, I7-R31, I7-R40, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R53, I7-R54 | I7-T164, I7-T165, I7-T166, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F63 | 184 | 43–46; C7-R17 | I7-R05, I7-R11, I7-R23, I7-R26, I7-R40, I7-R41, I7-R52 | I7-T167, I7-T168, I7-T169 |
| C7-F64 | 184 | 43–46; C7-R17 | I7-R05, I7-R11, I7-R23, I7-R26, I7-R40, I7-R41, I7-R52 | I7-T167, I7-T168, I7-T169 |
| C7-F65 | 185 | 43–46; C7-R17 | I7-R05, I7-R11, I7-R23, I7-R26, I7-R40, I7-R41, I7-R52 | I7-T167, I7-T168, I7-T169 |
| C7-F66 | 184–185 | 43–46; C7-R17 | I7-R05, I7-R11, I7-R23, I7-R26, I7-R40, I7-R41, I7-R52 | I7-T167, I7-T168, I7-T169 |
| C7-F67 | 185 | 43–46; C7-R01, C7-R17, C7-R18 | I7-R01, I7-R02, I7-R03, I7-R05, I7-R11, I7-R12, I7-R14, I7-R15, I7-R17, I7-R20, I7-R23, I7-R26, I7-R28, I7-R30, I7-R31, I7-R40, I7-R41, I7-R42, I7-R44, I7-R47, I7-R48, I7-R50, I7-R52, I7-R53, I7-R54 | I7-T167, I7-T168, I7-T169, I7-T170, I7-T171, I7-T173, I7-T174, I7-T175, I7-T176, I7-T177, I7-T178, I7-T179, I7-T180, I7-T181, I7-T182, I7-T183, I7-T184 |
| C7-F68 | 170, 185 | 43–46; C7-R01 | I7-R11, I7-R12, I7-R15, I7-R28, I7-R31, I7-R41, I7-R42, I7-R54 | I7-T170, I7-T171, I7-T179, I7-T184 |


## 51. Chapter 7 page coverage and complete body scope

Printed page plus 17 gives the PDF page for this range. These rows identify the material reviewed, not a claim that every sentence is a separate software requirement.

| Printed | PDF | Reviewed content and architectural treatment |
| --- | --- | --- |
| 166 | 183 | Opening warning about prediction/control and exaggerated expectations; preserve bounded claims |
| 167 | 184 | Understanding versus implementation, analysts' own difficulties, unanswered human questions and limits of mechanistic insight |
| 168 | 185 | Resistance to information, values, fear of change and incomplete control; model uptake and agency as unresolved where appropriate |
| 169 | 186 | Questions about selective interpretation, culture and powerlessness; responsive design and learning despite uncertainty |
| 170 | 187 | Participation, feedback, values, incomplete practice list and opening history-first guidance |
| 171 | 188 | Time graphs, memory, mean versus variability, co-variation, strengths and behavior-based problem definition |
| 172 | 189 | Avoid favorite-solution framing; expose assumptions, qualitative models, alternatives, challenge and evidence-based correction |
| 173 | 190 | Information integrity, directed distribution, reported emissions example and power over channels; reported versus actual outcome |
| 174 | 191 | Language, perception, institutional categories, ambiguity and measurement effects; source theories remain qualified |
| 175 | 192 | Meaningful concrete terms, systems vocabulary and opening concern about privileging what is countable |
| 176 | 193 | Qualitative constructs, elicited scale/curve example and concern for quality; no invented calibration |
| 177 | 194 | Values beyond convenient metrics; proposed Carter policies, state-dependent response and meta-feedback |
| 178 | 195 | Monitoring/review example, whole-system criteria and existing local self-maintenance |
| 179 | 196 | Local capability story, internal responsibility, trigger versus structure, decision/consequence feedback and delayed central control |
| 180 | 197 | Accountability hypotheticals, implementation limits, learning, monitored action and willingness to change course |
| 181 | 198 | Error-embracing, communicated uncertainty and transients/nonlinearity; source trust claims remain conditional |
| 182 | 199 | Diversity and attributed land ethic; long horizons and critique of short-term weighting |
| 183 | 200 | Coupled fast/slow processes, attention to near and far effects, disciplinary boundaries and real integration |
| 184 | 201 | Ethical coverage and interdependence; selective reports, lowered expectations and moral-reference drift |
| 185 | 202 | Source moral perspective, proposed resistance to drift and final acknowledgment that analysis alone cannot implement conduct |

Chapter Seven notes on printed p. 207 identify twelve references or acknowledgments: Chesterton; Senge; Abelson on chemical-industry changes; Kofman on language/accounting; Berry; the Roberts oral account; Hardin; two Michael references; Leopold; Boulding; and Krutch. The note entries were reviewed. Their underlying works and numerical or historical claims were not independently reread, verified or replicated. All body pages were reviewed as extracted page text; complete rendered-page geometry or numerical source-figure reproduction is not claimed.

### 51.1 Complete requested body scope

| Chapter | Printed pages | PDF pages | Body pages | Catalogue units |
| --- | --- | --- | --- | --- |
| 1 — The Basics | 11–34 | 28–51 | 24 | 36 |
| 2 — Systems Zoo | 35–72 | 52–89 | 38 | 42 |
| 3 — Why Systems Work So Well | 75–85 | 92–102 | 11 | 32 |
| 4 — Why Systems Surprise Us | 86–110 | 103–127 | 25 | 48 |
| 5 — Traps and Opportunities | 111–141 | 128–158 | 31 | 56 |
| 6 — Leverage Points | 145–165 | 162–182 | 21 | 64 |
| 7 — Living in a World of Systems | 166–185 | 183–202 | 20 | 68 |
| Total | 11–72; 75–141; 145–185 | 28–89; 92–158; 162–202 | 170 | 346 |

Intervening unrequested pages and the source notes are excluded from the body count. Chapter 7's 20 body pages were checked again as extracted text in this pass; earlier six-chapter assessments are retained. Neither complete rendered-page inspection nor numerical reproduction of the book's figures is asserted.

## 52. Verification and qualification record

The consistency checks verify current metadata, exact chapter columns, one canonical requirement definition per identifier, case preservation and allocation, canonical source allocation, parent correspondence, table structure, source-page offsets, one connected master graph, defined endpoints, retained prior concepts/connections and no directed prediction-to-independent-record path. The 66-pair ledger and semantic walkthrough are a design review, not model execution. The scope of acceptance is section 49.5.

**Document-check result, 20 October 2026: passed the specified consistency checks.** The single master diagram has 82 concepts and 241 named directed connections in one connected component. It retains all 74 concepts and 202 named connections of the six-chapter master; the intended-action label was clarified when the current policy became explicit. All 346 canonical source-review units have valid requirement and prospective-case allocations. The 54 requirement definitions and 192 scenario definitions are unique and contiguous. The original 124 and Chapter 7's 60 case wordings are retained under the declared namespace correspondence; eight further cases test cumulative composition. All eighteen Chapter 7 parent obligations are allocated. The exact eight-column evolution table, fifteen Chapter 7 practice sections, twelve leverage positions, table/fence structure and Chapter 7 printed-to-PDF page offsets pass their checks. The ledger records 66 conceptual pairs and 132 separate directional review questions. No directed graph path leads from predicted trajectories into the independent source-observation roots. These are structural/textual checks and a conceptual contract review; full Mermaid renderer execution and model dynamics were not tested. Every model scenario remains **PLANNED — NOT RUN**. Counts describe the specification and its traceability, not scientific completeness, learning competence or successful policy intervention.


## 53. Explicit EDI reasoning and the model starting point

The evolved graph contains 98 nodes and 286 named connections. The retained conceptual portion contains 82 nodes and 241 connections. New displays are internal responsibilities and dependency roles, not sixteen new software components.

# Explicit systems reasoning and the pretrained student decision

Design revision 0.4, 20 October 2026. Input implementation revision: `783a4509461ee3cf66d5580f92b7e6988dcddaaa`. Status: structural design extension; not implemented, trained, tested or qualified. The owner requested the integrated structure before qualification/tests. Historical v0.3 checker reports remain historical and do not assess this extension.

The full integrated diagram in section 3 evolves the detailed seven-chapter master, retaining its 82 conceptual nodes and 241 named connections. It makes reasoning execution, student/teacher assistance and future parameter learning explicit. The original compact owner-supplied compact overview retained in the implementation repository and imported v0.7 master remain preserved source snapshots. This extension is EDI engineering synthesis rather than a claim that Meadows specifies neural learning algorithms.

## 1. Decision: pretrained, fixed weights initially

| Starting point | What it contains | Initial EDI decision |
| --- | --- | --- |
| Randomly initialized model | Architecture and tokenizer choices; no acquired language/world/reasoning capabilities in the weights. | Do not use as the main first-iteration student. Teacher supervision would also need to establish general capabilities. |
| Pretrained base model | Learned language/statistical/world representations from pretraining; not necessarily adapted to instructions or EDI tool use. | Keep as an alternative for a later deliberate training study; a base model is not a prior-free model. |
| Pretrained instruction/reasoning model | General acquired capabilities plus post-training behavior suited to instructions, reasoning or tool use. | Preferred initial student, using a compatible open-weight checkpoint if local operation and future parameter training are intended. |
| Pretrained student with EDI-specific parameter adaptation | The prior capabilities plus subsequent learning from selected systems-reasoning episodes. | Preserve a separate future path; no weight updates are enabled by this diagram. |

Initial configuration: pretrained student served by vLLM, fixed student weights, versioned systems-reasoning protocol and selective teacher assistance. The teacher also uses a fixed identified pretrained version. Actual model/checkpoint selection depends on available compute, supported vLLM architecture, license and capabilities; this design does not install or bind one.

Three update mechanisms must stay distinct:

1. World-model learning changes evidence-linked representations, mechanisms, uncertainty, identity and history in C3.
2. Context/protocol changes affect the instructions and information used for a particular inference without changing neural weights. Material protocol/policy changes are versioned, with adoption authority recorded.
3. Parameter learning changes student weights or adapters through an explicit training job and adopted checkpoint. That path is future/dormant initially.

The first two permit a changing persistent world while neural weights remain fixed. No claim is made that a prompt removes pretrained priors or replaces the model's internal reasoning algorithm. Meadows-inspired operations shape how EDI uses the model and, later, the behaviors training could target.

## 2. Explicit reasoning operations

The shared protocol selects relevant operations rather than requiring every question to traverse every step:

- Separate source reports, observed events, temporal patterns, structures, mechanisms and assumptions.
- Establish referents, meaning, units, time, sampling and relevant available history.
- Trace stocks/flows, joint constraints, feedback closure, delays and pending effects where applicable.
- Inspect nonlinear domains, saturation, thresholds, heterogeneity and changes of operating regime.
- Distinguish actor information, perception, incentives, intent and actual effects from EDI's own operational policy.
- Construct rival mechanisms and preserve unclassified observations, missing alternatives and insufficient evidence.
- Form conditional predictions and feasible discriminating inquiries using supported tools.
- Expand adjacent interfaces, refine internal structure or change resolution when relevant to the inquiry.
- Compare available evidence and consequences, diagnose discrepancies and propose retain/revise/reject/investigate decisions.

Five Whys and What If are available question patterns, not fixed recursion depths or substitutes for evidence. An unanswered why becomes an attributed unknown or acquisition request; it is not filled with a plausible biological or social mechanism.

## 3. New displayed parts and existing owners

These are internal responsibilities and external dependency roles, not sixteen new software components. Existing eight logical owners and 32 functions are retained.

| Diagram node | Responsibility | Authority / allocation |
| --- | --- | --- |
| RCTX | Bounded reasoning context, model cut, evidence selectors, scope and unknowns. | C4 F40/F41 workspace derived from C1/C3 reads; not another world store. |
| RPRO | Versioned systems reasoning protocol. | C4 reasoning implementation under C7-owned adopted operational policy; C0 enforces resource limits. |
| RCTL | Inquiry and tool controller. | C4 F40-F43; submits scheduling/tool requests through C0. It does not acquire new component powers. |
| RSTU | Pretrained student served by vLLM. | Replaceable inference dependency called through the owning adapter; fixed weights initially. |
| RTEA | Selective pretrained teacher guidance. | C4-owned teacher-adapter interaction, separately attributed; no model-state admission authority. |
| RALT | Rival mechanisms and explicit unknowns. | C4 F40/F41 proposals; represented in existing C3 hypothesis/model records after admission. |
| RTEST | Discriminating inquiries and supported scenarios. | C4 F42 designs; C0 schedules, C5 executes supported analysis. |
| RPATCH | Typed interpretations and model-change proposals. | C4/C2 proposal responsibilities through existing C3 ports, with base version and evidence. |
| RADMIT | Evidence-qualified model admission and revision. | C3 F31 only. Validates references, type/semantic/authority rules and retains contested status where appropriate. |
| RFRONT | Adjacent, internal and temporal exploration frontier. | C4 F43 proposes; C0 owns scheduling/budgets and outward delivery. |
| RACCESS | Missing access requests and standing-grant reuse. | C0/C7/C1 existing request, rights and acquisition responsibilities. No C4 direct execution bypass. |
| REPIS | Attributed student attempts, teacher feedback and outcome references. | C4 retains inquiry workspace/episode metadata; C1 preserves generated payloads with generated lineage; C6 owns assessment records. |
| TCUR | Future curated training episodes. | C6 assessment/selection recommendations and C0-controlled dataset job metadata; not automatic training acceptance. |
| TTRAIN | Future student parameter training. | Separately configured training dependency invoked by C0; no trainer or model weights installed here. |
| TCKPT | Candidate model/adapter checkpoints. | C0 operational artifact/version metadata; actual weights in a configured artifact backend, never in the Git repository. |
| TADOPT | Explicit operational checkpoint adoption. | C7 F73 under configured authority; candidate status is not adopted status. No automatic live weight mutation. |

Interpretation and other functions can benefit from model assistance without routing every record through the teacher. Existing direct model adapters inside C2 may handle interpretation; cross-owner reasoning requests follow existing C0-mediated orchestration where no direct lane exists. No new C2-C4, C4-C5 or C4-C7 bypass is implied.

## 4. Interface and arrow semantics

The original diagram remains a conceptual relationship map. Its old edges are preserved, including specification edges about model revision. The added edges expose responsibilities and request/result relationships; they are not direct new APIs between every visual box.

| Relationship | Integration rule |
| --- | --- |
| C0 -> C4 and C4 -> C0 | Existing IF-04A/B: scoped inquiry, budgets, candidate patch/test/frontier/access proposals and status. |
| C1 -> C4 and C4 -> C1 | Existing IF-10A/B: record selection/payload ranges/coverage; generated teacher text remains generated evidence lineage. |
| C3 -> C4 and C4 -> C3 | Existing IF-15A/B: temporal snapshots, dependency validity and candidate patches. C3 admission remains the durable mutation boundary. |
| C4 -> C6 and C6 -> C4 | Existing IF-19A/B: assessment queries/results and inquiry-yield review; neither actor silently changes old forecasts. |
| Reasoning controller -> analysis -> controller | Requests are scheduled through C0 using existing C0-C5 contracts; results return through that workflow. There is no new direct C4-C5 lane. |
| Reasoning frontier -> access -> acquisition | Proposals reach C0; C7 handles required authority and C1 performs allowed acquisition. A request/grant is not an observation. |
| Student <-> teacher | Two directions: submitted attempt/context versus attributed critique/correction. Same named evidence cut unless an explicitly labeled pedagogic context is used. No teacher consensus becomes independent world evidence. |
| Episode -> training -> checkpoint -> serving | Future, explicit operational path. Frozen data/model/protocol provenance and authorized adoption are required. Recording an episode never causes weight training by itself. |

The conceptual actor policy nodes PI/PM/ADP describe actors inside the investigated system. TADOPT instead concerns the operational student model used by EDI. These are distinct state domains.

All 28 existing component pairs and 56 directed lanes retain their prior statuses. The displayed extension uses existing operation families; concrete model-service/trainer schemas and a future deployment topology remain unspecified. A newly independently operated service or changed lane needs its own later interface design before implementation.

## 5. Teacher guidance, training and budgets

The initial teacher gives explicit model-building critique, corrective examples, candidate edits and questions. It can be consulted for novel structures, unresolved ambiguity, consequential changes or a student escalation. Teacher and student consume one task's configured budgets; they do not receive independent unlimited recursion. Capture and known deterministic operations remain usable while teacher reasoning is pending or unavailable.

Textual feedback, supervised distillation, log-probability distillation and on-policy optimization are separate options. A hosted teacher's text output does not establish access to hidden reasoning, weights or arbitrary student-token log probabilities. Compatible scoring/tokenization/training interfaces and permitted use must be bound before a particular distillation method is chosen.

Teacher critique is fallible. It can be retained, challenged or deferred alongside student alternatives. The future learning path should preserve observation-supported mechanisms and successful alternatives instead of rewarding stylistic agreement with the teacher. No qualification, model comparison, training or benchmark is performed at this stage.

## 6. Structural status and provenance

This is an unqualified design extension following the owner's structure-first direction. Existing historical checker results apply to their pinned versions only. No new PASS verdict, tested integration, learned systems intelligence, speed or availability is asserted. Book snapshots remain byte-preserved in the repository; this v0.8 integrated master preserves all earlier chapters and historical reviews while adding this implementation extension.

Primary references consulted on 20 October 2026:

- vLLM project: https://vllm.ai/ — inference/serving role, separate from student learning.
- Thinking Machines, On-Policy Distillation: https://thinkingmachines.ai/blog/on-policy-distillation/ — pretrained capability stages and teacher supervision of student-generated trajectories.
- Model Distillation recipes: https://tinker-docs.thinkingmachines.ai/cookbook/recipes/distillation/ — an example of separately configured inference/training infrastructure, not a selected mandatory provider.
- Reward-Gated On-Policy Distillation: https://arxiv.org/abs/2607.04037 — a research example of gating fallible teacher supervision.
- Rethinking On-Policy Self-Distillation: https://arxiv.org/abs/2607.05184 — task-specific findings about privileged-context training; no universal EDI result inferred.
- On-Policy Distillation Inherits the Teacher in VLMs: https://arxiv.org/abs/2610.20989 — task-specific transfer of teacher failure modes; not an EDI benchmark.

This supplements the 84-entry v0.3 research register rather than silently rewriting its audited inventory. Model provenance, protocol versions, adoption authority and the distinction between accepted world state and model parameters belong in the code structure from the beginning.
