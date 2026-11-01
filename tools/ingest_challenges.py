"""Pull challenges from CTFd, then sanitize their descriptions.

Usage:
    uv run python -m tools.ingest_challenges
    uv run python -m tools.ingest_challenges --url http://192.168.100.200:8000
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if __package__ in (None, ""):
    sys.path.insert(0, str(ROOT))

from tools.ctf_common import challenge_dirs, env, load_dotenv  # noqa: E402


def run(command: list[str], label: str) -> int:
    print(f"\n== {label} ==")
    print(" ".join(command))
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        print(f"FAILED ({result.returncode}): {label}", file=sys.stderr)
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=env("CTFD_URL", ""))
    parser.add_argument("--token", default=env("CTFD_TOKEN", ""))
    parser.add_argument("--username", default=env("CTFD_USER", ""))
    parser.add_argument("--password", default=env("CTFD_PASS", ""))
    parser.add_argument("--output", default="challenges")
    parser.add_argument("--skip-sanitize", action="store_true")
    args = parser.parse_args(argv)

    if not args.url:
        print("ERROR: set CTFD_URL or pass --url", file=sys.stderr)
        return 2

    pull = [sys.executable, "pull_challenges.py", "--url", args.url, "--output", args.output]
    if args.token:
        pull += ["--token", args.token]
    elif args.username:
        pull += ["--username", args.username, "--password", args.password]
    code = run(pull, "CTFd ingest")
    if code != 0:
        return code

    dirs = challenge_dirs(args.output)
    print(f"\n{len(dirs)} challenge dir(s) under {args.output}")

    if not args.skip_sanitize:
        code = run(
            [sys.executable, "tools/sanitize_desc.py", args.output],
            "adversarial description scan",
        )
        if code != 0:
            return code

    print("\nNext: start the engine with --msg-port 9400, then the report center.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
