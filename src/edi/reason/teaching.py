"""C4-owned, bounded, provisional teaching episodes; no neural-weight updates."""
import json

from edi.shared.durable_io import CallJournal, canonical, digest
from edi.shared.errors import EDIError, ErrorCode


class TeachingMemory:
    def __init__(self, profile, evidence):
        self.profile, self.evidence = profile, evidence
        self.journal = CallJournal(profile.database, 'teaching_memory_c4',
            max_calls=4096, max_bytes=32*1024**2)

    def retain(self, episode, record_id):
        if episode.request.teaching_mode != 'intensive':
            raise EDIError(ErrorCode.DENIED, 'only an intensive episode can produce teaching memory')
        by_job = {j.job_id:j for j in episode.jobs}
        critique = [r for r in episode.responses if by_job[r.job_id].teaching_stage=='critique']
        drafts = [r for r in episode.responses if by_job[r.job_id].teaching_stage=='draft']
        revisions = [r for r in episode.responses if by_job[r.job_id].teaching_stage=='revision']
        if not critique or not drafts or not revisions:
            raise EDIError(ErrorCode.INCOMPLETE, 'teaching memory requires completed draft, critique and revision')
        source = self.evidence.get_record(record_id)
        if (source.scope_id != self.profile.workspace_id or source.capture.origin_class != 'generated'
                or source.capture.kind != 'component-result' or 'teaching-outcome' not in source.capture.lineage):
            raise EDIError(ErrorCode.INTEGRITY, 'teaching outcome must be an attributed C0 artifact in this workspace')
        if source.manifest.byte_count > 262144:
            raise EDIError(ErrorCode.CAPACITY, 'teaching outcome exceeds retained artifact limit')
        envelope = json.loads(self.evidence.read_payload(record_id, length=source.manifest.byte_count))
        data = envelope.get('result', {})
        if (envelope.get('operation') != 'teaching-outcome' or data.get('inquiry_id') != episode.request.inquiry_id
                or data.get('student_response_id') != revisions[-1].response_id
                or data.get('chosen_operation') != revisions[-1].operation_proposals[0].model_dump(mode='json')):
            raise EDIError(ErrorCode.INTEGRITY, 'outcome does not identify the actual revised decision')
        key = 'teaching:' + digest([self.profile.workspace_id, episode.request.inquiry_id])
        entry = {'lesson_id':key, 'workspace_id':self.profile.workspace_id,
            'inquiry_id':episode.request.inquiry_id, 'objective':episode.request.purpose,
            'context_sha256':episode.context.sha256,
            'draft_response_id':drafts[-1].response_id,
            'independent_response_ids':[r.response_id for r in episode.responses if by_job[r.job_id].teaching_stage=='independent'],
            'critique_response_id':critique[-1].response_id, 'revision_response_id':revisions[-1].response_id,
            'guidance':list(critique[-1].procedural_guidance), 'outcome_record_id':record_id,
            'chosen_operation':data['chosen_operation'], 'controller_state':data['controller_state'],
            'status':'provisional', 'limitation':'Tool execution and a teacher opinion do not establish lesson validity or student learning'}
        self.journal.begin(key, {'inquiry_id':episode.request.inquiry_id, 'outcome_record_id':record_id}, reserve_bytes=512*1024)
        self.journal.finish(key, entry)
        return {'lesson_id':key, 'status':'provisional', 'outcome_record_id':record_id}

    def recent(self, *, limit=4):
        if type(limit) is not int or not 1<=limit<=4:
            raise EDIError(ErrorCode.INVALID, 'teaching recall limit is 1..4')
        with self.journal.connect() as db:
            rows = db.execute(f'SELECT result FROM {self.journal.table} WHERE state=? ORDER BY rowid DESC LIMIT ?',
                ('completed',limit)).fetchall()
        selected=[]
        for row in rows:
            value=json.loads(row[0])
            guidance=[x for x in value['guidance'] if len(x.encode('utf-8'))<=1024]
            view={key:value[key] for key in ('lesson_id','inquiry_id','critique_response_id','outcome_record_id','status','controller_state')}
            view.update(guidance=guidance, guidance_complete=len(guidance)==len(value['guidance']),
                objective=value['objective'] if len(value['objective'].encode('utf-8'))<=512 else 'Objective omitted; consult native episode',
                limitation=value['limitation'])
            # Omit whole lessons rather than truncate an instruction or remove
            # a negation. Source IDs allow explicit native reinspection.
            if len(canonical(selected+[view]).encode('utf-8'))<=12288:
                selected.append(view)
        return selected
