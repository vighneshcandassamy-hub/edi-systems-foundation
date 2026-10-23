# Native asset source identity correction

24 October 2026 IST. Source 0.10.10.dev0; C0 integrated-1.6.

The pinned 0.10.9 live teaching run acquired the register and capture notebook,
but later student drafts said those sources had not been read and proposed
another register acquisition. Inspection found that native asset document IDs
were retained in opaque C1 capture profiles, while C4 received excerpts with a
single generic broker origin. The compact teaching view omitted prior action
transcripts, so the source-ID-to-content association was not explicit in the
next prompt. This is a confirmed context-delivery omission; its causal share
in Qwen's repeated actions has not been isolated experimentally.

The smallest repair keeps the existing OriginSpec contract. A successfully
verified native asset now has a configured origin scoped to broker session and
requested document ID. Its descriptor exposes that ID to ordinary C4 evidence
reads. Repeated reads of one document share the source handle while retaining
distinct observation occurrences; different documents have different handles.
The descriptor expressly does not certify physical sameness or independence.
Payload bytes, hashes, source claims, teacher authority and C3 admission remain
unchanged. No new schema field, owner, source fetch or model call is introduced.

The C4 decision description points to the acquired evidence origins. Existing
public_outcomes deliberately remains a bounded list of direct world-call
receipts, not a complete asset acquisition log; its prior disclaimer is kept.
An additional acquisition-log schema was rejected because the existing origin
already carries the necessary identity without duplicated controller state.
C0 integrated-1.6 rejects older controller journals rather than rewriting old
captures, frozen cuts or pending provider jobs. The active Kaggle run remains
pinned to 0.10.9 and is not a live result for this correction.

## Requirements and review

Mission: retain useful evidence across inquiry steps. OBS-R003-R005/R022 require
source, occurrence and payload identity to stay distinct. DOWN-001-DOWN-008
allocate downstream evidence/provenance use; IMP-R09/R19/R23/R30 connect the
consumer obligations through IF-01A/B and IF-10A/B. C0 schedules, C7 authorizes,
C1 owns origin and immutable bytes, C4 reads context. The existing 8-owner,
28-pair, 56-directed-lane catalogue is reused; no no-link decision changes.
This is a scoped self-review using edi-component-review and
edi-interface-review; it is not independent validation.

| Interface facet | Scoped result |
| --- | --- |
| Ownership | C1 retains origins/occurrences; C0 retains schedule/phase identities; C4 retains decisions. |
| Authority | Existing C7 checks precede broker reads; a displayed ID grants no access or truth status. |
| Shape/version | Existing OriginSpec and EvidenceSlice; new native-asset adapter 1.1, C0 integrated-1.6 fence. |
| Identity/scope | Source key uses session/document digest; descriptor exposes requested ID; no physical merge. |
| Time/order | Existing receipt/commit/event-time unknowns and lineage are preserved. |
| Delivery/idempotency | Exact original acquisition IDs retain native/broker replay fencing; repeated new IDs are distinct occurrences. |
| Commit/recovery | Register origin after byte/digest reassembly succeeds; immutable registration is idempotent. Old journals are not migrated. |
| Retention | Existing C1 retain-only policy and checkpoint export; full bytes remain available for selected reads. |
| Resource limits | Existing 16 MiB asset and 300-call broker envelope; at most one extra origin per distinct asset, plus bounded descriptor text. Prompt token cost still enforced and not claimed improved. |
| Errors | Failed or mismatched asset reads do not gain a success origin; native conflicts/unsupported old controller states remain explicit. |
| Feedback/grounding | Both roles see the same source mapping; first assessments remain blind; duplicate reads are not independent confirmation. |

The alternative of copying all previous transcripts back into context was
rejected because it recreates the measured context-growth failure. Mandatory
source-selection sequences and domain-specific IDs are not encoded in runtime.
The source identity change does not prove that the model will use metadata
correctly. Capacity, ambiguous real-world identity and performance remain open.

## Verification and gate

One focused authored native case passed in the existing Windows Python 3.12
environment (unittest reported 4.370 seconds). It traverses the real in-process
broker handler, C1 capture, rendered student/teacher context, duplicate source
occurrences and C0/C4 reopen. It makes no LLM or network calls. See
[evidence](evidence/asset-source-identity-20261024/native-case.json) and
[component review](evidence/asset-source-identity-20261024/component-review.json).
Contract for this mapping: PASS, self-reviewed. Corrected-source live behavior,
autonomous transfer, neural training, comparative benefit and Meadows readiness:
not established. No additional neutral-model run is represented as completed.
