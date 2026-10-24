# Cedar reasoning assessment protocol

24 October 2026, Asia/Calcutta. Prospective analysis for the owner-requested detailed Meadows assessment. Runtime source stays `3d23e23663680cfcd1816df25fc8fa5135ae4ff6` (0.10.12.dev0); input bundle SHA256 `b6c121c4e7309545840791d8968b990500a680c6e1855fdaca133547a4865a73`. No model result is reported here. The upload is still blocked by automatic approval review.

The question is what reasoning structure the student actually develops, how its reported rationale connects to acquired evidence and actions, and what the result suggests optimizing. Preserve the first run before changing prompts, weights, memory, tools or the benchmark. Execution bounds and completion definition remain those in [the recorded live plan](evidence/teaching-recovery-20261024/live-plan.json); these analysis dimensions do not add preliminary practice runs or change the frozen case.

## Evidence for the report

Use the downloaded and verified native checkpoint, source/input manifest, raw C1 model and public-broker records, C4 episode/job/rejection records, actual C0 dispatch requests and outcomes, teacher feedback imports, provisional teaching-memory entries and the broker's actual terminal receipt. The official outcome vector is inspected after controller termination and is never provided as coaching material. Preserve missing, partial, truncated and unavailable records explicitly. Record archive digest, source/model revisions, assistance, resource bounds and start/stop timestamps with the result.

Analyze concise reported justifications and observable decisions. An explanation written by a model is fallible evidence of what it reported, rather than proof of the computation that produced the choice. An analyst reconstruction must be labelled and must cite the recorded statements/actions it combines.

## Decision-by-decision reconstruction

For every inquiry, retain a row with:

1. Acquired evidence available in the exact pinned cut: record/source IDs, selectors, coverage, byte hashes and limitations. Distinguish information already selected, acquired but omitted, publicly accessible but unacquired, and unavailable/unsupported.
2. Student draft: DecisionBasis.understanding, information_need, expected_use, selected evidence_record_ids, rationale_summary, limitation and the exact proposed operation. Retain malformed/rejected raw content and native diagnostic rather than reconstructing an accepted response that did not exist.
3. Independent teacher assessment, followed separately by critique. Check that the independent request withheld the current draft and that advice introduced no private state, future results or new observations.
4. Student revision: exact operation and changed claims; feedback_response and any explicit disagreement; native admission result and any correction. Identify whether the change is attributable in the record to critique, a native diagnostic, new source evidence, or remains unclear.
5. Actual execution and response: compare admitted revision with C0 dispatch; link public result or error and new observations. A proposed test is not an executed experiment; a dispatch receipt is not a successful scientific finding.
6. Next inquiry and retention: check whether the returned information changes the next reported understanding/action and whether the actual outcome and provisional lesson are retained. A repeated statement or stored lesson alone does not demonstrate learning or transfer.

Do not judge usefulness solely from eloquence, a filled checklist or teacher agreement. A correct uncertainty statement, evidence-based disagreement or justified stop can be informative. Repeated activity without a concrete information gain should remain visible.

## Assessment dimensions

| Dimension | Questions to assess | Native records |
| --- | --- | --- |
| Problem framing | Does it preserve the mission, obligations, system boundary, relevant horizon and distinction between observations and assumptions? Does it revise the boundary when evidence warrants it? | Inquiry request, DecisionBasis, rationale, final report |
| Evidence use | Does the actual selected content support its claims? Does it distinguish sources, occurrences, derived copies, missing ranges, conflicting reports and source independence? | Context evidence/limitations, full EvidenceRef lineage, raw public records |
| Relationship structure | Which constituents and directed relationships does it identify? Are they observed, reported or hypothesized? Are accumulation, rates, constraints and delays justified with coherent units and scope? | Hypotheses, candidate records, admitted C3 records if present, reported rationale |
| Feedback and dynamics | Does a claimed feedback loop contain a complete return path with supported directions, conditions and delays? Are thresholds, saturation and alternative explanations evidenced or merely named? | Hypotheses, assumptions/confounders, analysis outputs if actually invoked |
| Inquiry and tests | Does each action address a stated uncertainty? What alternative outcomes could discriminate rivals? Was the action available, feasible and actually executed? | InquiryTest, expected_use, proposals, C0/C7/broker receipts |
| Revision and teaching | What specifically changed after critique or diagnostic? Does the revised action address the defect? Does the next turn use the new result, or repeat the same unsupported request? | Draft/rejection, teacher independent/critique, revision, subsequent cut and action |
| Forecasts and interventions | Are expectations recorded before outcomes, with conditions, observable channel and horizon? Are interventions distinguished from recommendations, and causal effects from correlation? | Prediction, actual measurement/action/advance records, after-closure outcome report |
| Final synthesis | Does the final report connect findings, mechanisms, recommendations and uncertainty to acquired evidence? Does it disclose unresolved needs, validity limits and the difference between observed and conditional conclusions? | Student final submission, actual HTTP 200 closure, acquired evidence and terminal ledger |

Use descriptive judgments: demonstrated in this record, partially supported, unsupported/contradicted, or not demonstrated/not assessable. Include the evidence and reason for each judgment. Do not invent a numerical composite score or a Meadows answer-matching threshold.

## Reported structure versus native representations

Count and inspect separately: formal C4 hypotheses and rivals, proposed InquiryTest records, candidates submitted to C3, representations actually admitted by C3, C5 analyses actually run, C6 assessments actually produced, C7-authorized effects, and explanation-only relationships in prose. If a category is empty, report zero or absent. Do not infer a fully instantiated world model from a fluent paragraph. A diagram may summarize supported recorded relationships, with analyst-derived edges marked separately from native records.

## Terminal result and resources

Report completed submission, yielded/blocked investigation or unresolved execution exactly as recorded. A submission receipt establishes closure only; assess report quality independently. Keep infrastructure, orchestration/admission and reasoning-quality failures distinct, allowing mixed causes where evidence supports them.

Record all actual model calls, rejected/correction calls, teacher stages and waits, known input/output tokens, unknown teacher usage, policy-unit charging, elapsed time, broker attempts/results, bytes and available compute metadata. Token counts do not measure energy or money. Report energy as unmeasured unless an actual measurement exists. Report resource reservations separately from known consumption and allocated teacher jobs separately from imported responses.

## Deliverable and optimization decisions

The final assessment should give the execution outcome first, then the strongest supported findings, the student's resulting relationship structure, a concise account of its final rationale and uncertainty, representative decision/critique/revision examples, unresolved failures and resource use. Link evidence by immutable record/job/request identities and artifact hashes.

Only after preserving that result, propose targeted changes. Examples of diagnostic categories are: available evidence ignored; needed evidence omitted by context selection; source identity confused; unsupported causal inference; poorly discriminating inquiry; critique acknowledged without an action change; valid revision blocked by orchestration; or resource/export limits. Each proposed optimization needs a concrete observed failure, affected owner/path, expected behavioral change and a relevant verification case. Do not prescribe more training simply because a run fails, or promote successful software execution to general intelligence, transfer or competitive advantage. A matched comparison and additional systems would be separate work.
