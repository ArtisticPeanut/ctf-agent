"""Shared stdlib-only helpers for status, habit, walkthrough, and report tooling."""

from __future__ import annotations

import http.cookiejar
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"
REPORTS = ROOT / "reports"
CHALLENGES = ROOT / "challenges"
WALKTHROUGHS = ROOT / "walkthroughs"
ENV_FILE = ROOT / ".env"

TRACE_RE = re.compile(r"^trace-(?P<rest>.+)-(?P<stamp>\d{8}-\d{6})\.jsonl$")

# The CTFd front-end WAF rejects non-browser User-Agents on the login POST (403),
# so always present a browser-like UA for CTFd HTTP calls.
_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def load_dotenv(path: Path | str | None = None) -> dict[str, str]:
    """Load .env without overriding variables already present in the environment."""
    env_path = Path(path) if path else ENV_FILE
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    for raw in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        os.environ.setdefault(key, value)
        values[key] = value
    return values


def env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def env_float(key: str, default: float = 0.0) -> float:
    try:
        return float(env(key) or default)
    except ValueError:
        return default


def now() -> float:
    return time.time()


def slugify(name: str) -> str:
    slug = re.sub(r'[<>:"/\\|?*.\x00-\x1f]', "", name.lower().strip())
    slug = re.sub(r"[\s_]+", "-", slug)
    return re.sub(r"-+", "-", slug).strip("-") or "challenge"


def sanitize_trace_part(value: str) -> str:
    return value.replace("/", "_").replace(" ", "_")


def human_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds}s"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m{sec:02d}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h{minutes:02d}m"


def short(text: str, limit: int = 160) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def read_jsonl(path: Path | str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(item, dict):
                    events.append(item)
    except FileNotFoundError:
        pass
    return events


def append_jsonl(path: Path | str, record: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def post_msg(message: str, port: int | None = None, host: str = "127.0.0.1") -> tuple[bool, str]:
    """Send an operator message to the coordinator."""
    port = port or int(env("CTF_MSG_PORT", "9400") or 9400)
    body = json.dumps({"message": message}).encode("utf-8")
    request = urllib.request.Request(
        f"http://{host}:{port}/msg",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))
            return True, str(data.get("queued", "queued"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        return False, str(exc)


def http_json(url: str, token: str = "", timeout: float = 10.0) -> Any:
    # This CTFd only honours `Authorization: Token` when Content-Type is JSON;
    # without it the request is treated as a browser and 302-redirects to /login.
    headers = {
        "User-Agent": _BROWSER_UA,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if token:
        headers["Authorization"] = f"Token {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def ctfd_base() -> str:
    return env("CTFD_URL", "http://localhost:8000").rstrip("/")


def ctfd_token() -> str:
    return env("CTFD_TOKEN", "")


# --- CTFd auth: token header, with transparent web-session fallback ---------
# The API token can be stale/invalid (CTFd answers 302 -> /login). When that
# happens we log in once with CTFD_USER/CTFD_PASS and reuse the session cookie,
# so status/scoreboard/walkthrough keep working without a fresh token.
_token_state: dict[str, bool] = {"dead": False}
_session_opener: urllib.request.OpenerDirector | None = None
_session_ts: float = 0.0


def _ctfd_session_opener() -> urllib.request.OpenerDirector:
    global _session_opener
    if _session_opener is None:
        jar = http.cookiejar.CookieJar()
        _session_opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(jar)
        )
    return _session_opener


def _ctfd_web_login(force: bool = False) -> bool:
    """Log in with CTFD_USER/CTFD_PASS and keep the session cookie. Cached ~10 min."""
    global _session_ts
    if not force and _session_ts and time.time() - _session_ts < 600:
        return True
    user = env("CTFD_USER", "")
    password = env("CTFD_PASS", "")
    if not user or not password:
        return False
    base = ctfd_base()
    opener = _ctfd_session_opener()
    try:
        with opener.open(
            urllib.request.Request(
                f"{base}/login",
                headers={"User-Agent": _BROWSER_UA, "Accept": "text/html"},
            ),
            timeout=10,
        ) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        match = re.search(r'name="nonce"[^>]*value="([^"]+)"', html)
        nonce = match.group(1) if match else ""
        payload = urllib.parse.urlencode(
            {"name": user, "password": password, "nonce": nonce, "_submit": "Submit"}
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{base}/login",
            data=payload,
            headers={
                "User-Agent": _BROWSER_UA,
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": base,
                "Referer": f"{base}/login",
            },
        )
        with opener.open(request, timeout=10) as resp:
            resp.read()
            final_url = resp.geturl()
        _session_ts = time.time()
        return "/login" not in final_url
    except Exception:
        return False


def ctfd_fetch(path: str, token: str = "", timeout: float = 10.0) -> Any:
    """Fetch a CTFd API path. Try the API token first; fall back to session cookie."""
    url = path if path.startswith("http") else f"{ctfd_base()}{path}"
    token = token or ctfd_token()
    if token and not _token_state["dead"]:
        try:
            return http_json(url, token, timeout)
        except Exception:
            _token_state["dead"] = True
    if _ctfd_web_login():
        opener = _ctfd_session_opener()
        request = urllib.request.Request(
            url,
            headers={"User-Agent": _BROWSER_UA, "Accept": "application/json"},
        )
        try:
            with opener.open(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8", errors="replace"))
        except Exception:
            pass
    return http_json(url, "", timeout)


def ctfd_challenges(token: str = "") -> list[dict[str, Any]]:
    data = ctfd_fetch("/api/v1/challenges?per_page=500", token or ctfd_token())
    return [ch for ch in data.get("data", []) if ch.get("type") != "hidden"]


def ctfd_solved(token: str = "") -> set[str]:
    try:
        me = ctfd_fetch("/api/v1/users/me", token or ctfd_token())
        user = me.get("data", {})
        if user.get("team_id"):
            solves = ctfd_fetch(f"/api/v1/teams/{user['team_id']}/solves", token or ctfd_token())
        else:
            solves = ctfd_fetch(f"/api/v1/users/{user.get('id')}/solves", token or ctfd_token())
        return {
            item["challenge"]["name"]
            for item in solves.get("data", [])
            if item.get("challenge", {}).get("name")
        }
    except Exception:
        return set()


def ctfd_scoreboard(token: str = "", limit: int = 10) -> list[dict[str, Any]]:
    try:
        data = ctfd_fetch("/api/v1/scoreboard", token or ctfd_token())
        return data.get("data", [])[:limit]
    except Exception:
        return []


def load_meta(path: Path | str) -> dict[str, Any]:
    import yaml

    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def challenge_dirs(root: Path | str = CHALLENGES) -> list[Path]:
    root = Path(root)
    if not root.exists():
        return []
    return sorted(p.parent for p in root.rglob("metadata.yml"))


def find_meta_by_name(name: str, root: Path | str = CHALLENGES) -> Path | None:
    for directory in challenge_dirs(root):
        meta = load_meta(directory / "metadata.yml")
        if meta.get("name") == name or directory.name == name:
            return directory
    return None


def file_sha256(path: Path | str, chunk: int = 1024 * 1024) -> str:
    import hashlib

    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


@dataclass
class Trace:
    path: Path
    challenge: str = "?"
    model: str = "?"
    events: list[dict[str, Any]] = field(default_factory=list)
    start_ts: float = 0.0
    last_ts: float = 0.0
    cost_usd: float = 0.0
    status: str = "unknown"
    flag: str | None = None
    confirmed: bool = False
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)

    @property
    def steps(self) -> int:
        return len(self.tool_calls)

    @property
    def age_s(self) -> float:
        return max(0.0, now() - self.last_ts) if self.last_ts else float("inf")

    @property
    def wall_s(self) -> float:
        return max(0.0, self.last_ts - self.start_ts) if self.start_ts else 0.0

    @property
    def active(self) -> bool:
        return self.status in ("running", "gave_up", "bumped") and self.age_s < 180

    def model_response_count(self) -> int:
        return sum(1 for event in self.events if event.get("type") == "model_response")


def _extract_cost(events: list[dict[str, Any]]) -> float:
    """Usage events are cumulative per agent; take the max instead of summing."""
    cost = 0.0
    for event in events:
        kind = event.get("type")
        if kind in ("usage", "finish", "turn_complete"):
            try:
                cost = max(cost, float(event.get("cost_usd") or event.get("cost") or 0.0))
            except (TypeError, ValueError):
                pass
    return cost


def _extract_flag(events: list[dict[str, Any]]) -> tuple[str | None, bool]:
    flag: str | None = None
    confirmed = False
    for event in events:
        kind = event.get("type")
        if kind == "flag_confirmed":
            value = event.get("flag")
            if value:
                flag = str(value)
                confirmed = True
        elif kind == "finish":
            if event.get("flag"):
                flag = str(event["flag"])
            if event.get("confirmed"):
                confirmed = True
    return flag, confirmed


def parse_trace(path: Path | str) -> Trace:
    path = Path(path)
    events = read_jsonl(path)
    trace = Trace(path=path, events=events)
    if events:
        trace.start_ts = float(events[0].get("ts") or 0.0)
        trace.last_ts = float(events[-1].get("ts") or 0.0)

    for event in events:
        kind = event.get("type")
        if kind == "start":
            trace.challenge = str(event.get("challenge") or trace.challenge)
            trace.model = str(event.get("model") or trace.model)
        elif kind == "tool_call":
            trace.tool_calls.append(event)
        elif kind == "tool_result":
            trace.tool_results.append(event)
        elif kind == "finish":
            trace.status = str(event.get("status") or trace.status)
        elif kind == "stop" and trace.status == "unknown":
            trace.status = "stopped"

    if trace.challenge == "?":
        match = TRACE_RE.match(path.name)
        if match:
            trace.challenge = match.group("rest")

    trace.cost_usd = _extract_cost(events)
    trace.flag, trace.confirmed = _extract_flag(events)

    if trace.status == "unknown":
        trace.status = "running" if trace.age_s < 180 else "stopped"
    mtime = path.stat().st_mtime if path.exists() else 0.0
    if trace.status == "running" and mtime and now() - mtime > 300:
        trace.status = "stalled"
    return trace


def iter_traces(logs: Path | str = LOGS) -> list[Trace]:
    logs = Path(logs)
    if not logs.exists():
        return []
    files = sorted(logs.glob("trace-*.jsonl"), key=lambda p: p.stat().st_mtime)
    return [parse_trace(path) for path in files]


def traces_for(challenge: str, logs: Path | str = LOGS) -> list[Trace]:
    return [trace for trace in iter_traces(logs) if trace.challenge == challenge]


def sort_key(trace: Trace) -> tuple[int, float]:
    return (1 if trace.confirmed else 0, trace.last_ts)
