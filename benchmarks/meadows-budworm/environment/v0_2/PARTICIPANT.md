# Cedar District information access

Your mission and authority are in mission.json. This is a constructed development world. External records retain their original source identity and are not observations of Cedar District. Generated charts, video and audio are representations; their provenance does not make them independent field observations.

The operator supplies an API URL and token. Your client uses EDI_BENCHMARK_TOKEN and defaults to a loopback URL. All operations are POST /v2/OPERATION. Each request includes a unique request_id. Retrying exactly the same request returns its committed response; reusing an ID with changed contents is a conflict. PUBLIC_OPERATIONS.json describes the allowed fields and operational limits.

You choose how to investigate. No hypothesis, rationale, expected answer, prescribed reading sequence or predefined policy choice is required. You may browse or search the available sources, obtain original assets, ask registered roles, request supported measurements, schedule permitted work, advance time and submit a report. You may propose changes to the objective; those proposals require a human decision and do not automatically change the original mission.

Independent request examples (replace placeholder IDs with IDs actually returned by the service):

```bash
python client.py sources --json '{"request_id":"sources-1"}'
python client.py search --json '{"request_id":"browse-1","query":"","limit":30}'
python client.py read --json '{"request_id":"document-1","document_id":"RETURNED_DOCUMENT_ID","include_asset":true}'
python client.py ask --json '{"request_id":"question-1","person_id":"RETURNED_PERSON_ID","question":"YOUR_QUESTION"}'
```

Original assets are returned as base64 byte chunks with offset/total_bytes/has_more. Decode the bytes using your existing observation tools; request later chunks with new request IDs. Search examines stored text and ordinary metadata; it is lexical search, not semantic understanding. Empty-query browsing remains available when vocabulary differs.

Roles disclose their recorded knowledge with source references. This prototype does not provide arbitrary generated answers to natural-language questions. Unsupported facts remain unknown. Field observations have declared units and uncertainty. Historical records and missing measurements are not retroactively invented.

Measurements cost two accounting units per stand and become available after the next annual time step. Broad treatment costs eight units times dose per stand; selective treatment eleven; harvesting costs five times the harvested fraction per stand. Work in the same future year shares the 240-unit authorization. Different methods have different consequences; their effects must be assessed from evidence. Routine reports arrive on advancing time. No ordinary clock advances automatically while you read.

The current instruments cover insects, enemy activity, foliage, fir/spruce/birch fractions and age estimates. A trap activity index is not a complete species census or pathogen assay. Unsupported measurements return an explicit error. Each stand may have at most one treatment and one harvesting job per year; overlapping work is rejected. Advance one to five years at a time, up to simulation year 50. These are declared experimental boundaries, not claims about every real-world operation.

Final submission accepts a conclusion and optional recommendations, uncertainties, evidence IDs and a forecast object. Cite documents you acquired or observations published to your session. Submission closes the session; it does not return private evaluation notes or a preferred answer. An exact final retry remains valid.
