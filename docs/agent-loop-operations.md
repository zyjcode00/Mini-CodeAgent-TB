# Agent Execution Loop: Implementation and Operations

This document describes the execution-loop hardening introduced for executor shutdowns, tool-result integrity, repeated reads, no-progress runs, and completion verification.

## Scope

The implementation spans these runtime boundaries:

- `tools/execution_backend.py`: executor ownership and lifecycle.
- `core/engine.py`: Agent run state, tool-result delivery, fatal termination, and completion gating.
- `core/read_guard.py`: read ledger, repeated-call detection, and no-progress policy.
- `core/compression_engine.py`: durable task, file, command, test, error, and decision summaries.
- `scripts/run_terminal_bench_agent.py`: Terminal-Bench session execution and timeout cleanup.

The runtime now treats execution state as part of the Agent session instead of reconstructing it from the latest model turn.

## State Machines

### Execution backend

`TerminalSessionExecutionBackend` has three states:

| State | Meaning | Allowed operation |
| --- | --- | --- |
| `running` | The backend owns a usable executor. | Submit tool work and shut down. |
| `closing` | Shutdown has started. | Finish cleanup only. New submissions fail. |
| `closed` | Executor resources have been released. | Idempotent shutdown only. New submissions fail. |

A submission outside `running` raises `ExecutorShutdownError`. The backend owns the executor it creates and shuts it down once. Timeout or cancellation paths cancel pending work before releasing the executor.

### Agent run

A run progresses through model inference, tool execution, progress evaluation, and completion validation. It terminates in one of these outcomes:

- `success`: the completion gate accepts the final answer.
- `blocked`: the Agent identifies a specific external prerequisite and no executable next action remains.
- `max_turns`: the internal reasoning limit is reached before completion.
- `executor_shutdown`: the execution backend is unavailable; this is fatal for the current run.
- `no_progress`: repeated calls or failures reached a stop threshold.

`executor_shutdown` is not returned to the model as retryable tool text. `core/engine.py` catches it at the run boundary, records a structured terminal result, saves the session, and returns immediately. This prevents post-shutdown inference loops.

## Tool Result Protocol

Assistant tool calls and tool results remain paired in conversation history. A tool result is delivered as tool-role data, never injected as a new user request.

Structured results use these fields where applicable:

```json
{
  "status": "success | error | deduplicated",
  "error_code": "stable_machine_readable_code",
  "retryable": false,
  "message": "human-readable detail"
}
```

Error handling follows these rules:

- Retry only when `retryable` is true and the retry changes a relevant input or runtime condition.
- Treat executor shutdown as non-retryable and terminate the run.
- Count identical failure signatures across consecutive tool batches.
- Warn after two identical failures and stop after three.
- Preserve complete assistant-call/tool-result groups during context assembly and compression. A half tool exchange must never be retained.

## Read Ledger

`ReadLedger` records normalized paths, requested line ranges, file fingerprints, and read counts. The ledger belongs to the Agent instance and survives multiple `execute_query` calls in the same session.

Read behavior:

1. A new path or uncovered range performs file I/O and records the result.
2. A covered range with the same fingerprint returns a lightweight `deduplicated` result without reinjecting file content.
3. A changed fingerprint invalidates the old coverage for that file and permits a fresh read.
4. The ledger summary is included in context and compression state so the model can act on what has already been read.

This separates a model-requested read from actual file I/O. Operational metrics should count both requested reads and executed reads; the difference is the deduplication count.

## No-Progress Policy

`NoProgressTracker` evaluates consecutive tool batches. Current thresholds are code-level policy values:

| Signal | Checkpoint | Stop |
| --- | ---: | ---: |
| Identical tool call batch | 3 consecutive batches | 5 consecutive batches |
| Identical failing batch | 2 consecutive batches | 3 consecutive batches |

At a checkpoint the Agent is instructed to summarize the available result and choose a different next action. At the stop threshold the current run ends with an explicit reason.

A successful, non-repeated action clears the repeated-failure state. Changing an argument without changing the effective operation may still normalize to the same call signature.

These values are not environment-variable settings in the current release. Changing them requires a code change in `core/read_guard.py` and corresponding regression tests.

## Completion Gate

The completion gate tracks the task objective, plan steps, changed files, executed commands, tests, errors, and decisions. A model answer that claims completion is rejected when any of these conditions hold:

- A plan step remains incomplete.
- Files were modified but no relevant verification was run.
- The latest relevant test failed or has unknown status.
- The run has an unresolved fatal execution error.

A rejected completion returns actionable feedback to the model and keeps the run active. A blocked exit remains valid when the missing prerequisite is external, concrete, and cannot be resolved with available tools.

Session compression preserves this workflow state. It also removes bulky raw tool output and incomplete tool-call groups, allowing a resumed run to distinguish completed work from pending verification.

## Compatibility Changes

The hardened loop intentionally changes several observable behaviors:

- Repeated reads may return metadata instead of file contents.
- Tool failures appear as tool-role structured results, not user-role messages.
- A closed executor ends the current Agent run immediately instead of allowing retries.
- Completion text may be rejected until plan and test evidence agree.
- Context compression retains workflow state and may produce a different summary shape.

Callers that parse human-readable tool error strings should migrate to `status`, `error_code`, and `retryable`. Callers that assume every read returns source text must handle `deduplicated` status.

## Verification

The required local regression command is:

```bash
pytest -q
```

The final implementation verification completed with `283 passed, 1 skipped in 61.56s`. Focused Terminal-Bench runner and backend smoke coverage completed with `16 passed in 0.14s`:

```bash
pytest -q tests/test_terminal_bench_runner.py tests/test_terminal_bench_session_backend.py
```

The focused suites cover backend reuse and shutdown, timeout cleanup, fatal shutdown handling, paired OpenAI-compatible tool messages, read-ledger persistence, no-progress stopping, and completion gating.

Historical Terminal-Bench evidence under `eval_runs_test/2026-08-24__18-22-17` captured the pre-hardening failure mode: the `3d-model-format-legacy` Agent timed out at 1200 seconds after a short read-only sequence and then failed task tests. That run is a failure baseline, not a post-change success result. A fresh full harness score requires the Terminal-Bench task corpus, Docker, credentials, and network access; do not infer success rate from unit smoke tests.

For before/after evaluation, record these per-run metrics:

- Task success rate from Terminal-Bench `results.json`.
- Requested tool calls and actually executed tool calls.
- Duplicate/deduplicated read count.
- Turns after the first non-retryable error.
- Identical-error retry count.
- Wall-clock duration and timeout count.

Acceptance targets for the loop hardening are zero turns after executor shutdown, at most two repeated identical failures before stop, no repeated content injection for unchanged covered reads, and no successful completion with pending plan or failed-test state.

## Rollout

Use a staged rollout because the compatibility changes affect model context and tool-result consumers.

1. Deploy to local development and CI with the full pytest suite required.
2. Run a small representative Terminal-Bench set and retain raw logs plus `results.json`.
3. Compare the metrics above with a fixed baseline using the same model, timeout, task revision, and container image.
4. Expand to a minority of interactive sessions while monitoring `executor_shutdown`, `no_progress`, deduplication rate, and completion rejections.
5. Promote to all sessions only after task success is non-regressive and timeout/error-after-stop metrics improve.

No runtime feature flag exists for the hardening as a whole. Therefore the recommended deployment unit is a versioned build or Git commit, not a live policy toggle.

## Rollback

Before rollout, record the known-good commit or image tag. To roll back:

1. Stop new Agent sessions on the candidate build.
2. Allow active sessions to finish or cancel them; do not move an in-memory executor between versions.
3. Deploy the recorded known-good build.
4. Preserve candidate session JSON and Terminal-Bench logs for diagnosis.
5. Start new sessions on the old build and rerun the focused backend/runner smoke tests.

Session JSON is designed for additive workflow state, but downgrade readers may ignore new fields. For a strict rollback, resume important sessions on the same build that created them or start a new session and provide the compressed task summary. Never rewrite or truncate session history merely to make a downgrade load.

## Operational Diagnosis

When a run stops unexpectedly, inspect the terminal outcome first:

- `executor_shutdown`: verify backend ownership and find the first shutdown/timeout event; model retries are not the cause after hardening.
- `no_progress`: inspect normalized call and failure signatures, then determine whether the threshold exposed a missing action or an overly broad signature.
- Completion rejected: inspect pending steps, latest test status, and changed-file verification evidence.
- Excessive deduplication: compare file fingerprints and requested ranges; stale fingerprints indicate an invalidation defect.
- Tool-message API error: verify every assistant tool call has a following tool-role response and that compression did not split the group.

Any change to lifecycle transitions, error classification, read normalization, thresholds, or completion rules must include a focused regression test and pass the full pytest suite before release.
