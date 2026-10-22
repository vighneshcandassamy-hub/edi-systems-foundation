"""Real C1/C2/C3/C4 neutral model integration; never loads a benchmark oracle."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import platform
from time import monotonic
import traceback

from edi import __version__
from edi.inquiry.runtime import Runtime
from edi.interpret.contracts import InputSpec, InterpretRequest, SubmissionRequest as DecodeSubmission
from edi.observe.contracts import Capture, OriginSpec
from edi.reason.config import ReasoningProfile
from edi.reason.contracts import Budget, InquiryRequest, ModelBinding, StepRequest, SubmissionRequest
from edi.reason.gateway import NativeGateway, VllmBackend
from edi.shared.config import LocalProfile
from edi.shared.durable_io import canonical

REVISION = "0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
MODEL = "Qwen/Qwen3-VL-8B-Instruct"


def run(endpoint, api_key, out):
    from PIL import Image, ImageDraw
    out = Path(out)
    state_dir = out / "edi-native-state"
    state_dir.mkdir(exist_ok=False)
    workspace = "neutral-native-integration-v1"
    binding = ModelBinding(model_id=MODEL, revision=REVISION,
        provider="local-kaggle", engine="vllm/0.21.0",
        tokenizer_revision=REVISION)
    profile = LocalProfile(database=state_dir/"c1.sqlite", workspace_id=workspace)
    reason_profile = ReasoningProfile(database=state_dir/"c4.sqlite",
        workspace_id=workspace, student=binding)
    runtime = Runtime(profile, reasoning_profile=reason_profile)
    backend = VllmBackend(endpoint, MODEL, api_key=api_key, max_model_len=16384)
    calls = []
    def send(messages, job):
        started = monotonic()
        try:
            result = backend(messages, job)
        except Exception:
            calls.append({"job_id":job.job_id, "elapsed_seconds":monotonic()-started,
                "input_tokens":None,"output_tokens":None,"status":"unresolved-provider-call"})
            raise
        calls.append({"job_id":job.job_id, "elapsed_seconds":monotonic()-started,
            "input_tokens":result[2], "output_tokens":result[3]})
        return result
    origin = runtime.register_origin(OriginSpec(namespace="engineering.neutral",
        native_source_id="authored-mixed-modal-v1", epoch="1",
        deliverer="neutral-fixture", channel="native-bytes",
        adapter="edi-native-probe/1", binding_basis="configured",
        descriptor={"scope":"authored engineering fixture; no forest or empirical claim"}))
    image = Image.new("RGB",(256,128),"white")
    draw=ImageDraw.Draw(image)
    draw.rectangle((16,16,112,112),fill=(255,0,0))
    draw.ellipse((144,16,240,112),fill=(0,0,255))
    buffer=BytesIO(); image.save(buffer,format="PNG")
    cases=[
        ("numeric", "text/csv", b"step,count\n0,8\n1,12\n2,16\n",
         "Describe the pattern in this authored table and distinguish it from a verified causal law. Retain useful candidate hypotheses or relationships if justified. No external action is needed."),
        ("image", "image/png", buffer.getvalue(),
         "Identify the visible shape and color on the left and on the right. Distinguish directly visible details from unsupported causal or identity claims. No external action is needed.")
    ]
    report={"kind":"neutral-native-EDI-integration", "edi_version":__version__,
        "model":binding.model_dump(mode="json"),"context_window":16384,
        "input_token_cap":12288,"output_token_cap":2048,"image_pixel_cap":65536,
        "teacher_enabled":False,"forest_benchmark_started":False,
        "full_eight_owner_P1_run":False,"hard_isolation_qualified":False,
        "python":platform.python_version(),"cases":[],"inference_calls":calls,
        "scope":"Trusted SDK engineering diagnostic; synthetic inputs; no intelligence advantage claim"}
    def save():
        (out/"edi-native-result.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    save()
    try:
        for name,media,data,question in cases:
            started=monotonic()
            obs=runtime.observe(Capture(origin_ref=origin.origin_ref,
                idempotency_key=name,media_type=media,origin_class="generated",
                lineage=("authored-neutral-engineering-v1",name),completeness="complete",
                expected_bytes=len(data),expected_sha256=sha256(data).hexdigest()),BytesIO(data)).observation
            derived=runtime.interpretation.interpret(InterpretRequest(workspace_id=workspace,
                request_id=name+":decode",inputs=(InputSpec(record_id=obs.record_id),)))
            retained=runtime.interpretation.submit(DecodeSubmission(
                derivation_id=derived.derivation.derivation_id,
                world_request_id=name+":decode-candidates",base_revision=runtime.world.head()))
            inquiry=InquiryRequest(workspace_id=workspace,inquiry_id=name,request_id=name,
                question=question,purpose="Neutral native integration diagnostic",
                scope="Only selected authored source bytes and native candidate records",
                horizon="Current selected evidence; no empirical forecast",
                model_revision=runtime.world.head(),world_ids=tuple(retained.changed_ids)[:3],
                evidence=({"record_id":obs.record_id,"offset":0,"length":len(data)},),
                budget=Budget(input_token_cap=12288,output_token_cap=2048,reserved_tokens=28672))
            ep=runtime.reasoning.investigate(inquiry)
            ep=runtime.reasoning.step(StepRequest(workspace_id=workspace,
                inquiry_id=name,request_id=name+":student",action="student",reason="Inspect neutral native evidence"))
            gateway=NativeGateway(runtime,binding,reason_profile.database,send,backend.count_tokens,
                attribution="REAL PINNED QWEN INFERENCE; authored neutral inputs; fixed weights",
                max_calls=4,max_images=1)
            job=ep.jobs[-1]
            messages,images=gateway.messages(job,ep)
            request_bytes=canonical(messages).encode()
            (out/("edi-native-"+name+"-request.json")).write_bytes(request_bytes)
            counted=backend.count_tokens(messages)
            entry={"name":name,"record_id":obs.record_id,
                "input_sha256":sha256(data).hexdigest(),"context_sha256":ep.context.sha256,
                "request_sha256":sha256(request_bytes).hexdigest(),
                "rendered_input_tokens":counted,"fits_4k_with_reserved_output":counted+2048<=4096,
                "fits_16k_with_reserved_output":counted+2048<=16384,
                "native_image_parts":len(images),"c2_status":derived.derivation.status,
                "c2_candidate_ids":list(retained.changed_ids),"world_revision_before_model":runtime.world.head(),
                "status":"awaiting-model"}
            report["cases"].append(entry);save()
            response=gateway.complete(job,ep)
            imported=runtime.reasoning.import_response(response)
            model_candidates=[]
            if response.candidates:
                submission=runtime.reasoning.submit(SubmissionRequest(workspace_id=workspace,
                    inquiry_id=name,request_id=name+":model-candidates",
                    response_id=response.response_id,reason="Retain actual model candidates without promotion"))
                model_candidates=list(submission.changed_ids)
            (out/("edi-native-"+name+"-response.json")).write_text(response.model_dump_json(indent=2),encoding="utf-8")
            entry.update(status="native-response-imported",
                rationale_summary=response.rationale_summary,limitation=response.limitation,
                input_tokens=response.input_tokens,output_tokens=response.output_tokens,
                hypothesis_count=len(response.hypotheses),model_candidate_ids=model_candidates,
                native_job_status=imported.jobs[-1].status,
                elapsed_seconds=monotonic()-started)
            # Re-open native owner stores and replay the exact completed gateway job.
            # This verifies one completed-call recovery, not whole-application restore.
            replay_runtime=Runtime(profile,reasoning_profile=reason_profile)
            reopened=NativeGateway(replay_runtime,binding,reason_profile.database,send,backend.count_tokens,
                attribution=gateway.attribution,max_calls=4,max_images=1)
            before=len(calls)
            replay=reopened.complete(job,ep)
            assert replay==response and len(calls)==before
            entry["completed_gateway_reopen_without_new_inference"]=True
            save()
        report["status"]="completed"
    except Exception as error:
        report.update(status="failed",error_type=type(error).__name__,error=str(error)[:2000])
        traceback.print_exc()
    finally:
        report["total_input_tokens"]=sum(c["input_tokens"] or 0 for c in calls)
        report["total_output_tokens"]=sum(c["output_tokens"] or 0 for c in calls)
        report["usage_unknown"]=any(c["input_tokens"] is None or c["output_tokens"] is None for c in calls)
        report["source_hashes"]={str(p.relative_to(Path(__file__).resolve().parents[2])).replace("\\","/"):sha256(p.read_bytes()).hexdigest()
            for p in sorted((Path(__file__).resolve().parents[2]/"src").rglob("*.py"))}
        save()
    return report
