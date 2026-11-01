"""Check the things that silently break a CTF run.

Usage:
    uv run python -m tools.preflight
    uv run python -m tools.preflight --json
"""

from __future__ import annotations

import argparse
import json
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.ctf_common import ENV_FILE, ROOT, env, http_json, load_dotenv  # noqa: E402


@dataclass
class Check:
    name: str
    status: str
    detail: str


def add(checks: list[Check], name: str, status: str, detail: str) -> None:
    checks.append(Check(name=name, status=status, detail=detail))


def run(cmd: list[str], timeout: int = 15) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, (proc.stdout or proc.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, str(exc)


def port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def claude_state() -> tuple[bool, bool]:
    cli = shutil.which("claude") is not None
    logged_in = False
    if cli:
        code, out = run(["claude", "auth", "status"], timeout=20)
        if code == 0:
            try:
                logged_in = bool(json.loads(out).get("loggedIn"))
            except json.JSONDecodeError:
                logged_in = '"loggedIn": true' in out.lower()
    return cli, logged_in


def codex_state() -> tuple[bool, bool]:
    cli = shutil.which("codex") is not None
    logged_in = False
    if cli:
        code, _ = run(["codex", "login", "status"], timeout=20)
        logged_in = code == 0
    return cli, logged_in


def model_specs() -> list[str]:
    raw = env("CTF_MODELS", "").strip()
    if raw:
        return [part.strip() for part in raw.split(",") if part.strip()]
    from backend.models import DEFAULT_MODELS

    return list(DEFAULT_MODELS)


def provider_ready(provider: str, claude_ok: bool, codex_ok: bool) -> tuple[bool, str]:
    match provider:
        case "claude-sdk":
            return claude_ok, "claude auth or ANTHROPIC_API_KEY"
        case "codex":
            return codex_ok, "codex login"
        case "google":
            return bool(env("GEMINI_API_KEY") or env("GOOGLE_API_KEY")), "GEMINI_API_KEY"
        case "bedrock":
            return bool(
                env("AWS_BEARER_TOKEN")
                or (env("AWS_ACCESS_KEY_ID") and env("AWS_SECRET_ACCESS_KEY"))
            ), "AWS credentials"
        case "azure":
            return bool(env("AZURE_OPENAI_ENDPOINT") and env("AZURE_OPENAI_API_KEY")), "Azure endpoint + key"
        case "zen":
            return bool(env("OPENCODE_ZEN_API_KEY")), "OPENCODE_ZEN_API_KEY"
        case "deepseek":
            return bool(env("DEEPSEEK_API_KEY")), "DEEPSEEK_API_KEY"
        case _:
            return False, f"unknown provider {provider}"


def collect() -> list[Check]:
    load_dotenv()
    checks: list[Check] = []

    add(checks, "repo", "ok", str(ROOT))
    add(checks, ".env", "ok" if ENV_FILE.exists() else "warn",
        "found" if ENV_FILE.exists() else "missing; defaults will be used")

    url = env("CTFD_URL", "")
    if not url:
        add(checks, "CTFD_URL", "fail", "not set")
    elif "localhost" in url or "127.0.0.1" in url:
        add(checks, "CTFD_URL", "warn", f"{url} (expected the event host)")
    else:
        add(checks, "CTFD_URL", "ok", url)

    token = env("CTFD_TOKEN", "")
    user = env("CTFD_USER", "")
    password = env("CTFD_PASS", "")
    if token:
        add(checks, "CTFd auth", "ok", "API token set")
    elif user and password:
        add(checks, "CTFd auth", "ok", "username/password set")
    else:
        add(checks, "CTFd auth", "fail", "set CTFD_TOKEN or CTFD_USER + CTFD_PASS")

    if url:
        try:
            data = http_json(f"{url.rstrip('/')}/api/v1/challenges?per_page=1", token, timeout=8)
            count = len(data.get("data", []))
            add(checks, "CTFd reachable", "ok", f"HTTP 200, {count}+ challenge(s) in first page")
        except Exception as exc:
            add(checks, "CTFd reachable", "fail", str(exc)[:180])

    claude_cli, claude_login = claude_state()
    if claude_cli:
        add(checks, "claude CLI", "ok" if claude_login else "warn",
            "logged in" if claude_login else "installed, not logged in (run: claude auth login)")
    else:
        add(checks, "claude CLI", "warn", "missing")
    if env("ANTHROPIC_API_KEY"):
        add(checks, "ANTHROPIC_API_KEY", "ok", "set")
    codex_cli, codex_login = codex_state()
    if codex_cli:
        add(checks, "codex CLI", "ok", "on PATH")
        add(checks, "codex auth", "ok" if codex_login else "fail",
            "logged in" if codex_login else "not logged in (run: codex login)")
    else:
        add(checks, "codex CLI", "fail", "missing (npm install -g @openai/codex)")

    claude_ok = claude_login or bool(env("ANTHROPIC_API_KEY"))
    codex_ok = codex_cli and codex_login
    specs = model_specs()
    add(checks, "models", "ok" if specs else "fail", ", ".join(specs) or "none")
    for spec in specs:
        provider = spec.split("/", 1)[0]
        ready, need = provider_ready(provider, claude_ok, codex_ok)
        add(checks, f"model {spec}", "ok" if ready else "fail", "ready" if ready else f"needs {need}")

    code, out = run(["docker", "info", "--format", "{{.ServerVersion}}"], timeout=15)
    if code == 0 and out:
        add(checks, "docker daemon", "ok", f"server {out.splitlines()[-1]}")
        code, _ = run(["docker", "image", "inspect", env("SANDBOX_IMAGE", "ctf-sandbox")], timeout=15)
        add(checks, "sandbox image", "ok" if code == 0 else "warn",
            env("SANDBOX_IMAGE", "ctf-sandbox") if code == 0 else "not built")
    else:
        add(checks, "docker daemon", "fail", "not running (start Docker Desktop)")

    free_gb = shutil.disk_usage(ROOT).free / 1024**3
    add(checks, "disk", "ok" if free_gb >= 20 else "warn", f"{free_gb:.1f} GB free")

    for port in (int(env("CTF_MSG_PORT", "9400") or 9400), 8080):
        add(checks, f"port {port}", "ok" if port_free(port) else "warn",
            "free" if port_free(port) else "in use")

    if not (ROOT / "reports").exists():
        add(checks, "reports dir", "warn", "will be created on first write")
    return checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    started = time.time()
    checks = collect()
    if args.json:
        print(json.dumps({"checks": [asdict(c) for c in checks]}, indent=2))
    else:
        icon = {"ok": "[ok]  ", "warn": "[warn]", "fail": "[FAIL]"}
        for check in checks:
            print(f"{icon.get(check.status, '[?]   ')} {check.name:24} {check.detail}")
        fails = sum(1 for c in checks if c.status == "fail")
        warns = sum(1 for c in checks if c.status == "warn")
        print(f"\n{fails} fail, {warns} warn, {len(checks)} checks in {time.time() - started:.1f}s")
    return 1 if any(c.status == "fail" for c in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
