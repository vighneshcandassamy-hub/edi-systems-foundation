import json,sys,sqlite3
from pathlib import Path
root=Path("/kaggle/temp/edi-engineering-source")
sys.path.insert(0,str(root))
from complete_run import runtime,read,save,plain,ROOT
r=runtime(False)
run=r.analysis.get_run("run")
assert run.artifact_sha256==read("numerical-run.json")["artifact_sha256"]
comparison=r.assessment.get_comparison("assessment")
assert comparison.artifact_sha256==read("compare.json")["artifact_sha256"]
candidate=r.world_for("C0").get("review-candidate")
assert candidate.state=="candidate" and candidate.decision_authority=="C3-candidate-policy"
receipt=r.agency_for("C0").get_receipt("read-execution")
assert receipt.receipt.status=="completed"
ep=r.reasoning.get("inquiry")
assert len(ep.responses)==3 and sum(j.role=="student" and j.status=="completed" for j in ep.jobs)==2
assert len(ep.rejections)==0
known_in=sum(value.input_tokens or 0 for value in ep.responses)
known_out=sum(value.output_tokens or 0 for value in ep.responses)
charge=sum((value.input_tokens if value.input_tokens is not None else next(j for j in ep.jobs if j.job_id==value.job_id).input_token_cap)+(value.output_tokens if value.output_tokens is not None else next(j for j in ep.jobs if j.job_id==value.job_id).output_token_cap) for value in ep.responses)
save("native-restart-audit.json",{"status":"passed","c5_native_hash_verified":True,"c6_native_hash_verified":True,"c3_candidate_not_admitted":True,"c7_native_receipt":"completed","real_student_responses":2,"teacher_responses":1,"known_input_tokens":known_in,"known_output_tokens":known_out,"conservative_charged_tokens":charge,"teacher_usage":"unknown; full reservation charged","new_model_calls_in_restart":0,"paid_spend":0,"energy":"not measured"})
