"""Collect confirmed flags from solver traces and persist them for the team.

Usage:
    python tools/flags.py
    python tools/flags.py --refresh
    python tools/flags.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ctf_common import LOGS, REPORTS, Trace, iter_traces  # noqa: E402

FLAGS_JSON = REPORTS / "flags.json"
FLAGS_MARKDOWN = REPORTS / "flags.md"


def _confirmed_at(trace: Trace) -> float:
    for event in trace.events:
        if event.get("type") == "flag_confirmed" and event.get("flag") == trace.flag:
            return float(event.get("ts") or 0.0)
    for event in trace.events:
        if event.get("type") == "finish" and event.get("flag") == trace.flag:
            return float(event.get("ts") or 0.0)
    return trace.last_ts


def _iso(timestamp: float) -> str:
    if not timestamp:
        return ""
    return datetime.fromtimestamp(timestamp).isoformat(timespec="seconds")


def _read_existing() -> list[dict[str, Any]]:
    try:
        data = json.loads(FLAGS_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    records = data.get("flags") if isinstance(data, dict) else None
    return [record for record in records or [] if isinstance(record, dict)]


def collect_flags(logs: Path | str = LOGS) -> list[dict[str, Any]]:
    """Return unique confirmed flags, newest first.

    Existing persisted records are merged in so flags survive trace cleanup.
    """
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for trace in iter_traces(logs):
        if not trace.confirmed or not trace.flag:
            continue
        confirmed_at = _confirmed_at(trace)
        key = (trace.challenge, trace.flag)
        record = {
            "challenge": trace.challenge,
            "flag": trace.flag,
            "model": trace.model,
            "confirmed": True,
            "confirmed_at": confirmed_at,
            "confirmed_at_iso": _iso(confirmed_at),
            "trace": trace.path.name,
            "source": "trace",
        }
        previous = records.get(key)
        if previous is None or confirmed_at < float(previous.get("confirmed_at") or 0.0):
            records[key] = record

    for record in _read_existing():
        challenge = str(record.get("challenge") or "")
        flag = str(record.get("flag") or "")
        if challenge and flag:
            records.setdefault((challenge, flag), record)

    return sorted(
        records.values(),
        key=lambda item: (float(item.get("confirmed_at") or 0.0), str(item.get("challenge"))),
        reverse=True,
    )


def _markdown(records: list[dict[str, Any]], generated_iso: str) -> str:
    lines = [
        "# Captured flags",
        "",
        f"_Updated: {generated_iso} — {len(records)} flag(s). Operator-only; submit manually._",
        "",
        "| Challenge | Flag | Model | Confirmed at | Trace |",
        "|---|---|---|---|---|",
    ]
    for record in records:
        challenge = str(record.get("challenge") or "").replace("|", "\\|")
        flag = str(record.get("flag") or "").replace("|", "\\|")
        model = str(record.get("model") or "").replace("|", "\\|")
        confirmed = str(record.get("confirmed_at_iso") or "").replace("|", "\\|")
        trace = str(record.get("trace") or "").replace("|", "\\|")
        lines.append(f"| {challenge} | `{flag}` | {model} | {confirmed} | `{trace}` |")
    lines.append("")
    return "\n".join(lines)


def write_flags(records: list[dict[str, Any]]) -> dict[str, Any]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    generated = time.time()
    generated_iso = _iso(generated)
    data = {
        "generated_at": generated,
        "generated_at_iso": generated_iso,
        "count": len(records),
        "flags": records,
    }
    tmp = FLAGS_JSON.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(FLAGS_JSON)
    FLAGS_MARKDOWN.write_text(_markdown(records, generated_iso), encoding="utf-8")
    return {
        "generated_at": generated,
        "generated_at_iso": generated_iso,
        "count": len(records),
        "flags": records,
        "json_path": str(FLAGS_JSON),
        "markdown_path": str(FLAGS_MARKDOWN),
    }


def refresh_flags(logs: Path | str = LOGS) -> dict[str, Any]:
    return write_flags(collect_flags(logs))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logs", default=str(LOGS))
    parser.add_argument("--refresh", action="store_true", help="Write reports/flags.json and .md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.refresh:
        data = refresh_flags(args.logs)
        records = data["flags"]
        if not args.json:
            print(f"stored {data['count']} flag(s) in {data['json_path']}")
    else:
        records = collect_flags(args.logs)

    if args.json:
        print(json.dumps(records, indent=2, ensure_ascii=False))
    else:
        for record in records:
            print(
                f"{record.get('challenge')}: {record.get('flag')} "
                f"[{record.get('model')}] {record.get('confirmed_at_iso') or ''}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
