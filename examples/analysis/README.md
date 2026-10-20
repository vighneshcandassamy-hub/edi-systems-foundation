# C5 authored usage assets — not executed

The two-stock transfer example is hypothetical and deliberately small. It is not an empirical ecosystem model, numerical result or acceptance fixture that has run. See [C5 scope](../../docs/implementation/C5_ANALYSIS_RUNTIME.md).

For later execution, use a fresh workspace `analysis-demo` and its separate owner stores:

1. `world-propose world-patch.json` creates candidate left/right stocks, one transfer flow and the joint response. The IR describes a first-order identity transfer with an explicitly assumed rate constant. References target their first native versions; choose a new patch/references if an existing workspace already contains those IDs.
2. `analysis-compile compile.json` reads revision 1 and the response at version 1 with explicit `candidate-exploration` policy. A supported compile result is a grammar/mapping result, not qualification.
3. Replace `REPLACE_WITH_RETURNED_COMPILED_ID` in `run.template.json` with the actual compiled ID. `analysis-run` is the later numerical operation; it has not been invoked here. The profile requires the pinned optional numerical dependencies. No model API is involved.
4. Inspect `analysis-status REQUEST_ID`, `analysis-get-run RUN_ID` and the immutable trajectory/diagnostics. The output retains source assumptions, candidate policy, units and simulation origin. Finite parameter variants do not become independent evidence or confidence intervals.
5. For live work, a separate C0 control request may set `action=cancel`. If a worker is known to be interrupted, query its attempt and use `action=interrupt` with `expected_attempt` and a reason. Fencing protects final-result admission; process termination is a separate operator responsibility. Retry an original completed request to retrieve its result, never automatically repeat an unresolved intent.

All commands use the normal global `--workspace analysis-demo` option and chosen database/config paths. C4 test identifiers may be passed through C0 in the request; C4 never directly invokes C5. Prospective forecast registration/scoring belongs to C6 and remains unavailable.
