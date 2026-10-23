# ADR-014: Intensive teaching without changing neural weights

Date: 23 October 2026. Source 0.10.8.dev0; C0 integrated-1.4; C4 0.7.0.
Parent: e5dc7b6013a1503a5b87cc1b92dbe410e4e1da87.
The owner's current direction explicitly replaces student-selected-only teacher
use during this developmental teaching phase. Selective mode remains available.

## Execution and responsibility

Each intensive turn records four stages on one immutable acquired evidence cut:
teacher independent assessment, student draft, teacher critique and student
revision. The first teacher job is allocated before the student draft. A file
teacher request can remain pending while the student computes its draft; the
same inquiry may hold this specific pair of unresolved jobs. All other conflicting
pending work remains fenced. Model/admission/store writes are serialized. This
supports asynchronous teacher/student work; it does not claim simultaneous GPU
execution or an independent reviewer. The manual teacher's identity and usage
remain operator-declared and unverified.

First-assessment rendering excludes peer responses, peer hypothesis names and
peer rejection text. This also applies during correction/restart. Critique sees
both first assessments; the student revision sees the critique. Same world cut,
mission, access catalogue and general Meadows protocol are available to both.
The teacher has no broker execution port or hidden solution/evaluator access.
The student's initial draft is retained in C4 but is not dispatched or submitted
to C3. Only its final revision can become a C0-scheduled operation or C3 candidate.
A revised yield remains possible; teaching does not manufacture completion.

The teacher adds up to four conditional procedural-guidance statements during
critique. Other teacher stages and student outputs cannot author this field.
C0 captures the actual revised action, current receipt headers and acquired
result record IDs as a generated teaching-outcome artifact. C4 checks the native
inquiry/revision identities and keeps a bounded, immutable teaching episode.
It links original draft, independent assessment, critique, revision and outcome.
A tool receipt is execution evidence, not proof of a correct scientific lesson.
Every lesson therefore remains provisional. No automatic epistemic promotion,
world-model admission, neural-weight update or unsupported success label occurs.

Recent guidance can be reused in later inquiries in the same native workspace.
At most four whole lesson projections and 12 KiB are selected; overlong guidance
is omitted rather than truncating instructions or negations. Native IDs preserve
inspection paths. The C4 journal has a separate 32 MiB ceiling and reserves
512 KiB per retained episode. Existing owner quotas remain declared separately.
Cross-workspace guidance export/import has not been implemented or qualified.

Intensive mode always recalls these provisional lessons. A selective-mode run
may explicitly enable use_teaching_memory while disabling the teacher, allowing
reduced-assistance evaluation. The default selective baseline omits the history.
This is a configurable memory path, not demonstrated transfer or model learning.

## Failure, budgets and alternatives

Intensive mode requires a configured teacher and a fresh C0 journal. A missing
teacher response suspends the original turn; it never silently falls back to
unguided action. Reopen uses original jobs/requests. Unknown dispatched calls are
not resent. Unknown teacher usage consumes its full input/output reservation.
Existing one-correction-per-job, six-jobs/four-rounds-per-inquiry and global
budgets remain. A new intensive turn needs room to reserve four normal jobs
(65,536 policy units); corrections can consume remaining existing reservation.
Actual tokenization still gates all real student calls.

The six-question checklist provides inquiry discipline: supported evidence,
consequential uncertainty, alternatives/boundary, useful available action,
observed change and justified continuation/stop. All eleven Meadows protocol
axes are exposed during intensive practice. Neither catalogue prescribes a
particular source, solution or investigation order.

Selective-only escalation failed to help a student that stopped without asking.
Forced source sequences would change the task. Neural-weight training would be
a separate implementation/data/compute decision. Its necessity cannot be inferred
from the previous unguided failure or from authored fixture success. First obtain
a live assisted result; then assess retained guidance with reduced assistance.

## Evidence and limitations

Five native teaching checks exercise the full guided acquire/read/submit story,
blind/peer context separation, real file exchange with an independent pending
student draft, budget accounting, restart without redispatch, later-inquiry memory,
clean baseline omission and teacher outage. All model outputs in these checks are
authored. Nine selective checks are retained as compatibility coverage. Their
results cannot establish student reasoning improvement.

Live execution is blocked: Opera connector disconnected; the available Kaggle
browser is signed out. The execution environment briefly disconnected during
verification; persisted files and the five-case report were recovered intact.
No real student/teacher inference, training or Meadows evaluation ran here.
The updated launch package must pass native and serving grammar checks first.
Scientific and broader component gates remain REVISE. Review is by the implementer.
