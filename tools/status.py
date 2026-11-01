"""One-screen competition status for the operator (and the commander agent).

Usage:
    python tools/status.py
    python tools/status.py --json
    python tools/status.py --watch 15
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ctf_common import (  # noqa: E402
    LOGS,
    REPORTS,
    Trace,
    ctfd_challenges,
    ctfd_solved,
    env,
    env_float,
    human_duration,
    iter_traces,
    load_dotenv,
    short,
)


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _habit_tail(limit: int = 10) -> list[dict]:
    path = REPORTS / "habits.jsonl"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-limit:]
    out: list[dict] = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def build_status(traces: list[Trace]) -> dict[str, Any]:
    challenges: list[dict] = []
    ctfd_ok = False
    solved_names: set[str] = set()
    try:
        challenges = ctfd_challenges()
        solved_names = ctfd_solved()
        ctfd_ok = True
    except Exception:
        pass

    confirmed_names = {trace.challenge for trace in traces if trace.confirmed}
    if not solved_names:
        solved_names = confirmed_names

    total_cost = sum(trace.cost_usd for trace in traces)
    confirmed_flags = {trace.flag for trace in traces if trace.confirmed and trace.flag}
    first_ts = min((trace.start_ts for trace in traces if trace.start_ts), default=0.0)
    elapsed = max(0.0, time.time() - first_ts) if first_ts else 0.0

    by_challenge: dict[str, list[Trace]] = defaultdict(list)
    for trace in traces:
        by_challenge[trace.challenge].append(trace)

    challenge_rows: list[dict] = []
    for name, items in by_challenge.items():
        meta = next((ch for ch in challenges if ch.get("name") == name), {})
        starts = [item.start_ts for item in items if item.start_ts]
        ends = [item.last_ts for item in items if item.last_ts]
        window_s = (max(ends) - min(starts)) if starts and ends else 0.0
        challenge_rows.append(
            {
                "name": name,
                "category": meta.get("category", ""),
                "value": meta.get("value", 0),
                "solves": meta.get("solves", 0),
                "solved": name in solved_names,
                "cost_usd": round(sum(item.cost_usd for item in items), 4),
                "steps": sum(item.steps for item in items),
                "window_s": round(window_s, 1),
                "models": sorted({item.model for item in items}),
                "flag": next((item.flag for item in items if item.confirmed), None),
                "last_event_age_s": round(min(item.age_s for item in items), 1),
            }
        )
    challenge_rows.sort(key=lambda row: (bool(row["solved"]), -float(row["cost_usd"])))

    active = [
        {
            "challenge": trace.challenge,
            "model": trace.model,
            "steps": trace.steps,
            "cost_usd": round(trace.cost_usd, 4),
            "age_s": round(trace.age_s, 1),
            "status": trace.status,
            "trace": trace.path.name,
        }
        for trace in traces
        if trace.active
    ]
    active.sort(key=lambda row: row["challenge"])

    stalled = [
        {
            "challenge": trace.challenge,
            "model": trace.model,
            "steps": trace.steps,
            "cost_usd": round(trace.cost_usd, 4),
            "idle_s": round(trace.age_s, 1),
            "status": trace.status,
            "trace": trace.path.name,
        }
        for trace in traces
        if not trace.confirmed
        and trace.steps > 0
        and trace.age_s > 480
        and trace.status not in ("flag_found", "stopped")
    ]
    stalled.sort(key=lambda row: -float(row["idle_s"]))

    total_challenges = len(challenges) if challenges else len(by_challenge)
    unsolved = (
        sorted(
            name
            for ch in challenges
            if isinstance((name := ch.get("name")), str) and name not in solved_names
        )
        if challenges
        else sorted(set(by_challenge) - solved_names)
    )

    hours = elapsed / 3600 if elapsed else 0.0
    return {
        "generated_at": time.time(),
        "ctfd": {"url": env("CTFD_URL"), "reachable": ctfd_ok},
        "elapsed_s": round(elapsed, 1),
        "solved": sorted(solved_names),
        "solved_count": len(solved_names),
        "challenge_count": total_challenges,
        "unsolved": unsolved,
        "cost_usd": round(total_cost, 4),
        "budget_usd": env_float("CTF_BUDGET_USD", 0.0),
        "burn_per_hour": round(total_cost / hours, 4) if hours else 0.0,
        "flags_per_hour": round(len(confirmed_flags) / hours, 3) if hours else 0.0,
        "active": active,
        "stalled": stalled,
        "challenges": challenge_rows,
        "habits": _habit_tail(),
        "trace_count": len(traces),
    }


def render(status: dict[str, Any]) -> str:
    clock = time.strftime("%H:%M:%S")
    budget = ""
    if status["budget_usd"]:
        remaining = status["budget_usd"] - status["cost_usd"]
        budget = f" | budget ${remaining:.2f} left"
    header = (
        f"== {clock} | {status['solved_count']}/{status['challenge_count']} solved | "
        f"${status['cost_usd']:.2f} | {status['flags_per_hour']:.2f} flags/h | "
        f"burn ${status['burn_per_hour']:.2f}/h{budget} | "
        f"{status['elapsed_s'] / 3600:.2f}h elapsed =="
    )
    lines = [header]

    if status["solved"]:
        lines.append("solved: " + ", ".join(status["solved"]))
    if status["unsolved"]:
        shown = ", ".join(status["unsolved"][:20])
        extra = "" if len(status["unsolved"]) <= 20 else f" (+{len(status['unsolved']) - 20})"
        lines.append(f"unsolved: {shown}{extra}")

    lines.append("")
    if status["active"]:
        lines.append("active:")
        for row in status["active"]:
            lines.append(
                f"  {row['challenge'][:30]:30} {row['model'][:28]:28} "
                f"steps={row['steps']:<4} ${row['cost_usd']:.2f} idle={human_duration(row['age_s'])}"
            )
    else:
        lines.append("active: none")

    if status["stalled"]:
        lines.append("stalled:")
        for row in status["stalled"]:
            lines.append(
                f"  {row['challenge'][:30]:30} {row['model'][:28]:28} "
                f"steps={row['steps']:<4} ${row['cost_usd']:.2f} idle={human_duration(row['idle_s'])}"
            )

    costliest = [row for row in status["challenges"] if not row["solved"]][:5]
    if costliest:
        lines.append("costliest unsolved:")
        for row in costliest:
            lines.append(
                f"  {row['name'][:30]:30} ${row['cost_usd']:.2f} "
                f"steps={row['steps']:<5} models={len(row['models'])}"
            )

    if status["habits"]:
        lines.append("latest habits:")
        for habit in status["habits"][-5:]:
            lines.append(
                f"  [{habit.get('name')}] {habit.get('challenge')}/{habit.get('model')}: "
                f"{short(str(habit.get('detail', '')), 90)}"
            )

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logs", default=str(LOGS))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--watch", type=float, default=0.0)
    args = parser.parse_args(argv)

    load_dotenv()
    while True:
        traces = iter_traces(Path(args.logs))
        status = build_status(traces)
        if args.json:
            print(json.dumps(status, ensure_ascii=False))
        else:
            print(render(status))
        if not args.watch:
            return 0
        time.sleep(max(2.0, args.watch))


if __name__ == "__main__":
    raise SystemExit(main())
