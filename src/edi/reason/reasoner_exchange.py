"""Sole external reasoner; explicit import, native admission, no inference API."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from pydantic import ValidationError
from edi.observe.contracts import Capture, OriginSpec
from edi.reason.contracts import Job, Response
from edi.reason.exchange import AwaitingModelResponse, ModelOutputRejected, stored_result
from edi.shared.contracts import utc_now
from edi.shared.durable_io import CallJournal, canonical, digest
from edi.shared.errors import EDIError, ErrorCode

class AwaitingReasonerResponse(AwaitingModelResponse):
    def __init__(self, job_id, request_path):
        EDIError.__init__(self, ErrorCode.INCOMPLETE, 'Sole reasoner proposal awaits explicit import')
        self.job_id, self.request_path = job_id, str(request_path)

class ReasonerExchangeGateway:
    capacity_basis = 'external-session-byte-bounded'
    def __init__(self, runtime, binding, journal_path, directory, *, attribution,
                 max_calls=64, max_images=1, max_request_bytes=262144, max_response_bytes=65536):
        if binding != runtime.reasoning.profile.student or binding.model_id == 'unbound':
            raise EDIError(ErrorCode.INVALID, 'reasoner differs from C4 proposer binding')
        if journal_path.resolve() != runtime.reasoning.profile.database.resolve():
            raise EDIError(ErrorCode.INVALID, 'reasoner journal belongs to C4')
        if not 0 <= max_images <= 2 or not 16384 <= max_request_bytes <= 1048576 or not 1024 <= max_response_bytes <= 1048576:
            raise EDIError(ErrorCode.INVALID, 'invalid explicit byte/image capacity')
        self.runtime, self.binding, self.attribution = runtime, binding, attribution
        self.max_images, self.max_request_bytes, self.max_response_bytes = max_images, max_request_bytes, max_response_bytes
        self.directory = Path(directory).resolve(); self.directory.mkdir(parents=True, exist_ok=True)
        self.journal = CallJournal(journal_path, 'reasoner_exchange_c4', max_calls=max_calls, max_bytes=128*1024**2)
        self.origin = runtime.register_origin(OriginSpec(namespace='edi.reasoner.outputs', native_source_id=binding.model_id,
            epoch=binding.revision, deliverer='explicit-session-import', channel='reasoning-proposal',
            adapter='edi-reasoner-exchange/1.0', binding_basis='configured',
            descriptor={'binding':binding.model_dump(mode='json'),'identity':'operator-declared; unauthenticated',
                        'usage':'unmeasured unless explicitly supplied'}))
    def request_path(self, job_id):
        return self.directory/(sha256(job_id.encode()).hexdigest()+'.request.json')
    def _request(self, job, episode):
        if (job.role != 'student' or job.teaching_stage != 'standard' or episode.request.teaching_mode != 'selective'
                or job.binding != self.binding or job.context_sha256 != episode.context.sha256):
            raise EDIError(ErrorCode.INTEGRITY, 'sole reasoner job/stage/cut differs')
        from edi.reason.gateway import render_job_messages
        from edi.reason.operation_args import generation_schema
        messages, images = render_job_messages(self.runtime,self.binding,job,episode,max_images=self.max_images,schema_in_transport=True)
        control=json.loads(messages[0]['content'])
        control['response_identity'].update(request_id='reasoner:'+job.job_id,response_id='reasoner:'+job.job_id)
        control['reasoning_role']='Sole EDI reasoner; no teacher, peer assessment or training cycle'
        control['response_fields']['transport']='Request includes the native schema; imports undergo native admission. No provider decoder or measured tokenizer is enforced by this manual session.'
        messages[0]['content']=canonical(control)
        schema=generation_schema(controller_policy=episode.request.controller_policy)
        if episode.request.response_mode=='controller-turn' and 'operation_proposals' not in schema['required']:
            schema['required'].append('operation_proposals')
        return {'inquiry_id':episode.request.inquiry_id,'job':job.model_dump(mode='json',exclude={'status','response_id'}),
            'reasoning_role':'sole','messages':messages,'image_refs':images,'messages_sha256':digest(messages),
            'response_schema':schema,'transport':'explicit-reasoner-file-exchange/1.0','capacity_basis':self.capacity_basis,
            'instructions':'Propose reasoning and one next operation from this exact cut. No teacher exists. C0 schedules, C3 admits, C7 authorizes. Do not access the world outside native operations or invent execution.',
            'usage_status':'Actual session usage and energy unknown; C0 charges the full job reservation'}
    def preview(self, request):
        from edi.reason.protocol import PROTOCOL_ID, questions
        episode=self.runtime.reasoning.preview(request)
        job=Job(job_id='01234567-89ab-cdef-0123-456789abcdef',role='student',round=1,binding=self.binding,
            context_sha256=episode.context.sha256,protocol_id=PROTOCOL_ID,questions=questions(request.axes),
            input_token_cap=request.budget.input_token_cap,output_token_cap=request.budget.output_token_cap,
            created_at=utc_now(),reason='Prospective external export; no job allocated',teaching_stage='standard')
        episode=episode.model_copy(update={'jobs':(job,)})
        size=len(canonical(self._request(job,episode)).encode('utf-8'))+1
        if size>self.max_request_bytes:raise EDIError(ErrorCode.CAPACITY,'reasoner export exceeds byte budget')
        return {'input_tokens':None,'request_bytes':size,'max_request_bytes':self.max_request_bytes,
                'basis':self.capacity_basis,'context_sha256':episode.context.sha256}
    def complete(self, job, episode):
        request=self._request(job,episode);payload=(canonical(request)+'\n').encode('utf-8')
        if len(payload)>self.max_request_bytes:raise EDIError(ErrorCode.CAPACITY,'reasoner export exceeds byte budget')
        row=self.journal.begin(job.job_id,request,reserve_bytes=self.max_response_bytes)
        if row['state']=='completed':return stored_result(row)
        path=self.request_path(job.job_id)
        try:
            with path.open('xb') as stream:stream.write(payload)
        except FileExistsError:
            if path.read_bytes()!=payload:raise EDIError(ErrorCode.INTEGRITY,'original reasoner request changed')
        raise AwaitingReasonerResponse(job.job_id,path)
    def import_response(self, job_id, path):
        row=self.journal.get(job_id)
        if row is None:raise EDIError(ErrorCode.NOT_FOUND,'export original reasoner job before import')
        if row['state']=='completed':raise EDIError(ErrorCode.CONFLICT,'reasoner response already retained; immutable')
        request=json.loads(row['request']);job=request['job']
        with Path(path).open('rb') as stream:raw=stream.read(self.max_response_bytes+1)
        if len(raw)>self.max_response_bytes:raise EDIError(ErrorCode.CAPACITY,'reasoner response exceeds byte budget')
        try:content=json.loads(raw)
        except (ValueError,UnicodeError):content=None
        usage=content.get('usage',{}) if isinstance(content,dict) else {}
        valid=isinstance(usage,dict) and not set(usage)-{'input_tokens','output_tokens'}
        if valid:valid=all(v is None or (type(v) is int and v>=0) for v in usage.values())
        inp,out=(usage.get('input_tokens'),usage.get('output_tokens')) if valid else (None,None)
        receipt=self.runtime.observe(Capture(origin_ref=self.origin.origin_ref,
            idempotency_key='reasoner:'+job_id+':'+sha256(raw).hexdigest(),kind='reasoner-response',
            media_type='application/json',origin_class='generated',
            lineage=('explicit-reasoner-exchange/1.0',self.binding.model_id,self.binding.revision,job_id),
            profiles={'context_sha256':job['context_sha256'],'input_tokens':inp,'output_tokens':out,
                      'usage_basis':'operator-declared; not independently measured'},
            expected_bytes=len(raw),expected_sha256=sha256(raw).hexdigest()),BytesIO(raw))
        result={'raw_record_id':receipt.observation.record_id,'input_tokens':inp,'output_tokens':out}
        try:
            if not isinstance(content,dict) or not valid:raise ValueError('response must be object with valid optional declared usage')
            allowed=set(request['response_schema']['properties'])|{'usage'}
            if set(content)-allowed:raise ValueError('undeclared fields or transport-owned identity supplied')
            if (inp is not None and inp>job['input_token_cap']) or (out is not None and out>job['output_token_cap']):
                raise ValueError('declared usage exceeds job reservation')
            response=Response.model_validate_json(canonical({**{k:v for k,v in content.items() if k!='usage'},
                'workspace_id':self.runtime.profile.workspace_id,'inquiry_id':request['inquiry_id'],'job_id':job_id,
                'request_id':'reasoner:'+job_id,'response_id':'reasoner:'+job_id,'context_sha256':job['context_sha256'],
                'binding':self.binding.model_dump(mode='json'),'origin':'external-model-output','attribution':self.attribution,
                'input_tokens':inp,'output_tokens':out}))
        except (ValidationError,ValueError,TypeError,KeyError) as exc:
            result.update(outcome='rejected',diagnostic=str(exc)[:8192]);self.journal.finish(job_id,result)
            raise ModelOutputRejected(result) from exc
        result.update(outcome='returned',response=response.model_dump(mode='json'));self.journal.finish(job_id,result)
        return {'job_id':job_id,'raw_record_id':result['raw_record_id'],'status':'retained; native C0/C4 admission pending'}
    def receipt(self, job_id):
        row=self.journal.get(job_id)
        return json.loads(row['result']) if row and row['state']=='completed' else None
