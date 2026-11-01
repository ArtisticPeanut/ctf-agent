"""Detect token-wasting solver behaviour from JSONL traces.

Usage:
    python tools/habit_watch.py --once
    python tools/habit_watch.py --once --send
    python tools/habit_watch.py --watch 30 --send
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ctf_common import (  # noqa: E402
    LOGS,
    REPORTS,
    Trace,
    append_jsonl,
    env,
    human_duration,
    iter_traces,
    load_dotenv,
    post_msg,
    short,
)

ARTIFACT_RE = re.compile(r"CORRECT|ALREADY SOLVED|Written \d+ bytes|FLAG:", re.IGNORECASE)
INCORRECT_RE = re.compile(r"INCORRECT", re.IGNORECASE)
TRUNCATED_RE = re.compile(r"\.\.\. \[truncated|\[truncated", re.IGNORECASE)

HABIT_ACTIONS = {
    "loop": "Break the loop: require a new hypothesis before the next call.",
    "narration": "Stop describing; execute one concrete test.",
    "tool_thrash": "Force a hypothesis: state the top theory, then test only that.",
    "re_read": "The file is already in context; stop re-reading it.",
    "big_dump": "Pipe output through head/grep/xxd | head instead of dumping files.",
    "slow_burn": "Bump with a concrete technique or kill and respawn.",
    "wrong_submit": "Verify locally before submitting; no more guesses.",
    "give_up_drift": "Respawn with a different model mix; do not bump.",
    "stalled": "No progress: read the tail and intervene.",
    "broken_solver": "Solver never started; respawn it (0 steps, $0).",
}


def _args(event: dict) -> dict:
    raw = event.get("args", "")
    if isinstance(raw, dict):
        return raw
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except (json.JSONDecodeError, TypeError):
        return {}


def _arg_path(event: dict) -> str:
    args = _args(event)
    for key in ("path", "filename", "file", "directory"):
        if args.get(key):
            return str(args[key])
    return short(str(event.get("args", "")), 80)


def _result_of(event: dict) -> str:
    value = event.get("result", "")
    return value if isinstance(value, str) else str(value)


def _has_artifact(traces: list[dict]) -> bool:
    for event in traces:
        tool = event.get("tool", "")
        if tool == "write_file":
            return True
        if ARTIFACT_RE.search(_result_of(event)):
            return True
    return False


def detect(trace: Trace) -> list[dict]:
    if trace.confirmed:
        return []

    habits: list[dict] = []
    calls = trace.tool_calls
    results = trace.tool_results
    steps = trace.steps

    signatures = [
        f"{call.get('tool', '?')}:{short(str(call.get('args', '')), 300)}" for call in calls[-12:]
    ]
    if signatures:
        signature, count = Counter(signatures).most_common(1)[0]
        if count >= 5:
            habits.append(
                {
                    "name": "loop",
                    "severity": "high",
                    "detail": f"same call {count}x in last 12: {signature[:180]}",
                }
            )

    narration_run = 0
    max_narration = 0
    for event in trace.events:
        if event.get("type") == "model_response":
            narration_run += 1
            max_narration = max(max_narration, narration_run)
        elif event.get("type") == "tool_call":
            narration_run = 0
    if max_narration >= 3:
        habits.append(
            {
                "name": "narration",
                "severity": "medium",
                "detail": f"{max_narration} consecutive model responses with no tool call",
            }
        )

    recent_calls = calls[-10:]
    recent_steps = {call.get("step") for call in recent_calls}
    recent_results = [item for item in results if item.get("step") in recent_steps]
    distinct_tools = {call.get("tool") for call in recent_calls}
    if len(recent_calls) >= 8 and len(distinct_tools) >= 8 and not _has_artifact(recent_results):
        habits.append(
            {
                "name": "tool_thrash",
                "severity": "medium",
                "detail": f"{len(distinct_tools)} distinct tools in last 10 calls, no artifacts",
            }
        )

    paths = [
        _arg_path(call)
        for call in calls
        if call.get("tool") in ("read_file", "list_files")
    ]
    if paths:
        path, count = Counter(paths).most_common(1)[0]
        if count >= 3:
            habits.append(
                {
                    "name": "re_read",
                    "severity": "low",
                    "detail": f"{path} read/listed {count}x",
                }
            )

    big_run = 0
    max_big = 0
    for result in results:
        text = _result_of(result)
        is_big = bool(TRUNCATED_RE.search(text)) or len(text) >= 1900
        big_run = big_run + 1 if is_big else 0
        max_big = max(max_big, big_run)
    if max_big >= 4:
        habits.append(
            {
                "name": "big_dump",
                "severity": "medium",
                "detail": f"{max_big} consecutive truncated tool results",
            }
        )

    wrong_submits = sum(
        1
        for result in results
        if result.get("tool") == "submit_flag" and INCORRECT_RE.search(_result_of(result))
    )
    if wrong_submits > 2:
        habits.append(
            {
                "name": "wrong_submit",
                "severity": "high",
                "detail": f"{wrong_submits} incorrect submissions",
            }
        )

    if (trace.cost_usd >= 0.75 or trace.wall_s >= 720) and not _has_artifact(results):
        habits.append(
            {
                "name": "slow_burn",
                "severity": "medium",
                "detail": (
                    f"${trace.cost_usd:.2f} / {human_duration(trace.wall_s)} "
                    f"with no confirmed artifact"
                ),
            }
        )

    if trace.status == "gave_up" and steps < 15:
        habits.append(
            {
                "name": "give_up_drift",
                "severity": "high",
                "detail": f"gave up after only {steps} steps",
            }
        )

    if steps == 0 and trace.cost_usd == 0 and trace.status in ("error", "gave_up", "stopped"):
        habits.append(
            {
                "name": "broken_solver",
                "severity": "high",
                "detail": "0 steps and $0 spent; solver never produced work",
            }
        )

    if steps > 0 and trace.age_s > 480 and trace.status not in ("flag_found", "stopped"):
        habits.append(
            {
                "name": "stalled",
                "severity": "high",
                "detail": f"no trace event for {human_duration(trace.age_s)}",
            }
        )

    for habit in habits:
        habit["action"] = HABIT_ACTIONS.get(habit["name"], "Review the trace.")
    return habits


def load_state(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def should_raise(state: dict, key: str, trace: Trace, cooldown: float = 900.0) -> bool:
    previous = state.get(key)
    if not previous:
        return True
    if trace.steps - int(previous.get("steps", 0)) >= 5:
        return True
    return time.time() - float(previous.get("last_alert", 0)) >= cooldown


def run_once(args: argparse.Namespace) -> list[dict]:
    state_path = Path(args.state)
    state = load_state(state_path)
    cutoff = time.time() - args.max_age_hours * 3600
    raised: list[dict] = []
    traces = [trace for trace in iter_traces(Path(args.logs)) if trace.last_ts >= cutoff]

    for trace in traces:
        for habit in detect(trace):
            key = f"{trace.path.name}|{habit['name']}"
            if not should_raise(state, key, trace):
                continue
            record = {
                "raised_at": time.time(),
                "challenge": trace.challenge,
                "model": trace.model,
                "trace": str(trace.path),
                "steps": trace.steps,
                "cost_usd": round(trace.cost_usd, 4),
                "age_s": round(trace.age_s, 1),
                **habit,
            }
            raised.append(record)
            state[key] = {"steps": trace.steps, "last_alert": time.time()}
            append_jsonl(REPORTS / "habits.jsonl", record)
            message = (
                f"HABIT[{habit['name']}] challenge={trace.challenge} model={trace.model} "
                f"({trace.path.name}): {habit['detail']}. ACTION: {habit['action']}"
            )
            if args.send:
                ok, response = post_msg(message, port=args.port)
                record["sent"] = ok
                if not ok:
                    print(f"WARN: could not send message: {response}", file=sys.stderr)
            if args.json:
                print(json.dumps(record, ensure_ascii=False))
            else:
                print(
                    f"[{habit['severity']}] {trace.challenge}/{trace.model} "
                    f"{habit['name']}: {habit['detail']}"
                )
                print(f"    -> {habit['action']}")

    for key in list(state):
        if time.time() - float(state[key].get("last_alert", 0)) > 86400:
            del state[key]
    save_state(state_path, state)
    return raised


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logs", default=str(LOGS), help="Trace directory")
    parser.add_argument("--state", default=str(REPORTS / ".habit_state.json"))
    parser.add_argument("--once", action="store_true", help="Run a single pass (default)")
    parser.add_argument("--watch", type=float, default=0.0, help="Repeat every N seconds")
    parser.add_argument("--send", action="store_true", help="POST findings to the coordinator")
    parser.add_argument("--port", type=int, default=int(env("CTF_MSG_PORT", "9400") or 9400))
    parser.add_argument("--max-age-hours", type=float, default=16.0)
    parser.add_argument("--json", action="store_true", help="Emit JSONL to stdout")
    args = parser.parse_args(argv)

    if not Path(args.logs).exists():
        print(f"No trace directory: {args.logs}", file=sys.stderr)
        return 1

    while True:
        raised = run_once(args)
        if not args.json:
            print(f"\n{len(raised)} new finding(s).", file=sys.stderr)
        if not args.watch:
            return 0
        time.sleep(max(5.0, args.watch))


if __name__ == "__main__":
    raise SystemExit(main())
