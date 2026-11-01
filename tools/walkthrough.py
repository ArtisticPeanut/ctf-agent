"""Rebuild deterministic challenge walkthroughs from solver traces.

Usage:
    python tools/walkthrough.py                    # every confirmed challenge
    python tools/walkthrough.py --challenge <name-or-dir>
    python tools/walkthrough.py --all --force
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ctf_common import (  # noqa: E402
    CHALLENGES,
    LOGS,
    WALKTHROUGHS,
    Trace,
    challenge_dirs,
    file_sha256,
    find_meta_by_name,
    human_duration,
    iter_traces,
    load_meta,
    short,
    slugify,
)

SCRIBE_MARKER = (
    "<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->"
)


def _confirmed_ts(trace: Trace) -> float:
    for event in trace.events:
        if event.get("type") == "flag_confirmed":
            return float(event.get("ts") or 0.0)
    for event in trace.events:
        if event.get("type") == "finish" and event.get("confirmed"):
            return float(event.get("ts") or 0.0)
    return trace.last_ts


def pick_winner(traces: list[Trace], include_unsolved: bool = False) -> Trace | None:
    confirmed = [trace for trace in traces if trace.confirmed and trace.flag]
    if confirmed:
        return min(confirmed, key=_confirmed_ts)
    if include_unsolved and traces:
        return max(traces, key=lambda trace: trace.last_ts)
    return None


def _clip(text: str, limit: int) -> str:
    text = str(text)
    if len(text) <= limit:
        return text
    lines = text.splitlines()
    kept: list[str] = []
    size = 0
    for line in lines:
        if size + len(line) + 1 > limit:
            break
        kept.append(line)
        size += len(line) + 1
    if not kept:
        kept = [text[:limit]]
    return "\n".join(kept) + f"\n... [{len(text)} chars total]"


def _fence(text: str) -> str:
    fence = "~~~"
    while fence in text:
        fence += "~"
    return f"{fence}\n{text}\n{fence}"


def _pretty_args(raw: Any) -> str:
    if isinstance(raw, dict):
        return json.dumps(raw, indent=2, ensure_ascii=False)
    try:
        parsed = json.loads(str(raw))
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except (json.JSONDecodeError, TypeError):
        return str(raw)


def render_transcript(trace: Trace, max_result_chars: int = 1200) -> list[str]:
    lines: list[str] = []
    pending_response: str | None = None

    for event in trace.events:
        kind = event.get("type")
        if kind == "tool_call":
            step = event.get("step", "?")
            tool = event.get("tool", "?")
            lines.append(f"### Step {step}: `{tool}`")
            if pending_response:
                lines.append(f"> {short(pending_response, 500)}")
                lines.append("")
                pending_response = None
            lines.append(_fence(_clip(_pretty_args(event.get("args", "")), 900)))
            lines.append("")
        elif kind == "tool_result":
            result = str(event.get("result", ""))
            lines.append(_fence(_clip(result, max_result_chars)))
            lines.append("")
        elif kind == "model_response":
            pending_response = str(event.get("text", ""))
        elif kind == "bump":
            pending_response = None
            lines.append("> **BUMP** (dead end; new guidance injected)")
            lines.append(f"> {short(str(event.get('insights', '')), 600)}")
            lines.append("")
        elif kind == "loop_break":
            lines.append(f"> **LOOP BREAK** at step {event.get('step', '?')}")
            lines.append("")
        elif kind == "flag_confirmed":
            lines.append(f"> **FLAG CONFIRMED**: `{event.get('flag', '?')}`")
            lines.append("")
        elif kind in ("error", "turn_failed"):
            lines.append(f"> **{kind.upper()}**: {short(str(event.get('error', '')), 400)}")
            lines.append("")

    return lines


def render_walkthrough(
    challenge_dir: Path,
    traces: list[Trace],
    winner: Trace,
    max_result_chars: int = 1200,
) -> str:
    meta = load_meta(challenge_dir / "metadata.yml")
    name = str(meta.get("name") or challenge_dir.name)
    category = meta.get("category", "")
    value = meta.get("value", "")
    description = str(meta.get("description") or "").strip()

    total_cost = sum(trace.cost_usd for trace in traces)
    started = min((trace.start_ts for trace in traces if trace.start_ts), default=0.0)
    ended = max((trace.last_ts for trace in traces if trace.last_ts), default=0.0)
    wall = max(0.0, ended - started) if started and ended else winner.wall_s

    lines = [
        f"# {name}",
        "",
        SCRIBE_MARKER,
        "",
        f"- **Category**: {category or 'unknown'}",
        f"- **Points**: {value or '?'}",
        f"- **Solves**: {meta.get('solves', '?')}",
        f"- **Flag**: `{winner.flag or 'UNSOLVED'}`",
        f"- **Winner**: `{winner.model}`",
        f"- **Swarm cost**: ${total_cost:.2f} (winner ${winner.cost_usd:.2f})",
        f"- **Wall time**: {human_duration(wall)}",
        f"- **Traces**: {len(traces)}",
        "",
    ]

    if meta.get("adversarial") or meta.get("ground_truth"):
        flags = ", ".join(sorted(k for k, v in (meta.get("adversarial") or {}).items() if v))
        lines += [
            "## Adversarial description flags",
            "",
            f"- Flags: {flags or 'manual review'}",
        ]
        if meta.get("ground_truth"):
            lines.append(f"- Ground truth: {meta['ground_truth']}")
        lines.append("")

    if meta.get("connection_info"):
        lines += ["## Connection", "", _fence(str(meta["connection_info"])), ""]

    if description:
        lines += ["## Description", "", _fence(description), ""]

    hints = meta.get("hints") or []
    visible = [hint for hint in hints if isinstance(hint, dict) and hint.get("content")]
    if visible:
        lines += ["## Hints", ""]
        for hint in visible:
            lines.append(f"- {hint['content']}")
        lines.append("")

    distfiles = sorted((challenge_dir / "distfiles").glob("*")) if (challenge_dir / "distfiles").exists() else []
    if distfiles:
        lines += [
            "## Distfiles",
            "",
            "| File | Size | SHA-256 |",
            "|---|---:|---|",
        ]
        for path in distfiles:
            if path.is_file():
                lines.append(
                    f"| `{path.name}` | {path.stat().st_size} | `{file_sha256(path)}` |"
                )
        lines.append("")

    lines += [
        "## Trace",
        "",
        "| Model | Status | Steps | Cost | Wall | Trace |",
        "|---|---|---:|---:|---:|---|",
    ]
    for trace in sorted(traces, key=lambda item: item.start_ts):
        status = trace.status + (" / CONFIRMED" if trace.confirmed else "")
        lines.append(
            f"| `{trace.model}` | {status} | {trace.steps} | ${trace.cost_usd:.2f} | "
            f"{human_duration(trace.wall_s)} | `{trace.path.name}` |"
        )
    lines.append("")

    starts = [trace.start_ts for trace in traces if trace.start_ts]
    if starts:
        lines.append(
            f"_Window: {datetime.fromtimestamp(min(starts)).isoformat(timespec='seconds')} to "
            f"{datetime.fromtimestamp(ended).isoformat(timespec='seconds')}_"
        )
        lines.append("")

    lines += ["## Solution path", ""]
    lines += render_transcript(winner, max_result_chars=max_result_chars)

    lines += [
        "## Result",
        "",
        f"- **Flag**: `{winner.flag or 'UNSOLVED'}`",
        f"- **Confirmed by CTFd**: {'yes' if winner.confirmed else 'no'}",
        f"- **Cost**: ${winner.cost_usd:.2f} (winner), ${total_cost:.2f} (whole swarm)",
        f"- **Wall time**: {human_duration(wall)}",
        f"- **Generated**: {datetime.now().isoformat(timespec='seconds')}",
        "",
    ]
    return "\n".join(lines)


def resolve_challenge_dirs(values: list[str], root: Path) -> list[Path]:
    if not values:
        return challenge_dirs(root)
    resolved: list[Path] = []
    for value in values:
        candidate = Path(value)
        if (candidate / "metadata.yml").exists():
            resolved.append(candidate)
            continue
        found = find_meta_by_name(value, root)
        if found:
            resolved.append(found)
    return resolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--challenges", default=str(CHALLENGES))
    parser.add_argument("--logs", default=str(LOGS))
    parser.add_argument("--out", default=str(WALKTHROUGHS))
    parser.add_argument("--challenge", action="append", default=[], help="Name or directory")
    parser.add_argument("--all", action="store_true", help="All confirmed challenges")
    parser.add_argument("--include-unsolved", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--max-result-chars", type=int, default=1200)
    args = parser.parse_args(argv)

    all_traces = iter_traces(Path(args.logs))
    targets = resolve_challenge_dirs(args.challenge, Path(args.challenges))
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    for challenge_dir in targets:
        meta = load_meta(challenge_dir / "metadata.yml")
        name = str(meta.get("name") or challenge_dir.name)
        traces = [trace for trace in all_traces if trace.challenge == name]
        if not traces:
            continue
        winner = pick_winner(traces, include_unsolved=args.include_unsolved)
        if winner is None:
            skipped += 1
            continue
        destination = out_dir / f"{slugify(name)}.md"
        if destination.exists() and not args.force:
            skipped += 1
            continue
        destination.write_text(
            render_walkthrough(
                challenge_dir,
                traces,
                winner,
                max_result_chars=args.max_result_chars,
            ),
            encoding="utf-8",
        )
        written += 1
        print(f"wrote {destination}  ({winner.flag or 'UNSOLVED'})")

    print(f"\n{written} written, {skipped} skipped.")
    return 0 if written or not targets else 1


if __name__ == "__main__":
    raise SystemExit(main())
