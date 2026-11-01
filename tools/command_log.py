"""Append one commander status line to reports/command.log.

Usage:
    uv run python -m tools.command_log "solved 3/42 | active 2 | $1.20 | action: rung 1 on web-x"
    uv run python -m tools.command_log --show
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ctf_common import REPORTS  # noqa: E402

LOG_PATH = REPORTS / "command.log"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("line", nargs="*", help="Status line to append")
    parser.add_argument("--show", action="store_true", help="Show the last 40 lines")
    parser.add_argument("--file", default=str(LOG_PATH))
    args = parser.parse_args(argv)
    path = Path(args.file)
    path.parent.mkdir(parents=True, exist_ok=True)

    if args.show:
        if not path.exists():
            print("(empty)")
            return 0
        for line in path.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-40:]:
            print(line)
        return 0

    text = " ".join(args.line).strip()
    if not text:
        parser.error("provide a status line or --show")
    stamp = time.strftime("%H:%M")
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(f"{stamp} | {text}\n")
    print(f"{stamp} | {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
