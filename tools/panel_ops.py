"""Operations behind the operator control panel.

Kept out of the HTTP layer so the dangerous parts (env edits, process
lifecycle, challenge storage) can be tested without opening a socket.
"""

from __future__ import annotations

import hmac
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any

import yaml

from tools.ctf_common import CHALLENGES, ENV_FILE, REPORTS, ROOT, load_meta, slugify

ENGINE_LOG = REPORTS / "engine-console.log"

MANAGED_KEYS: tuple[str, ...] = (
    "CTFD_URL",
    "CTFD_TOKEN",
    "CTFD_USER",
    "CTFD_PASS",
    "DEEPSEEK_API_KEY",
    "DEEPSEEK_BASE_URL",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "OPENCODE_ZEN_API_KEY",
    "CTF_MODELS",
    "MAX_CONCURRENT_CHALLENGES",
    "CONTAINER_MEMORY_LIMIT",
    "CTF_MSG_PORT",
    "CTF_BUDGET_USD",
    "CTF_TOTAL_HOURS",
    "CTF_BLOCK_PRIVATE_FETCH",
)

SECRET_KEYS: frozenset[str] = frozenset(
    {
        "CTFD_TOKEN",
        "CTFD_PASS",
        "DEEPSEEK_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GEMINI_API_KEY",
        "OPENCODE_ZEN_API_KEY",
    }
)

CONFIG_FIELDS: list[dict[str, str]] = [
    {
        "key": "CTFD_URL",
        "label": "CTFd URL",
        "group": "CTFd",
        "kind": "text",
        "placeholder": "http://192.168.100.200:8000",
    },
    {"key": "CTFD_TOKEN", "label": "API token", "group": "CTFd", "kind": "secret"},
    {"key": "CTFD_USER", "label": "Username", "group": "CTFd", "kind": "text"},
    {"key": "CTFD_PASS", "label": "Password", "group": "CTFd", "kind": "secret"},
    {
        "key": "DEEPSEEK_API_KEY",
        "label": "DeepSeek key",
        "group": "Keys",
        "kind": "secret",
    },
    {
        "key": "DEEPSEEK_BASE_URL",
        "label": "DeepSeek base URL",
        "group": "Keys",
        "kind": "text",
        "placeholder": "https://api.deepseek.com/v1",
    },
    {"key": "OPENAI_API_KEY", "label": "OpenAI key", "group": "Keys", "kind": "secret"},
    {
        "key": "ANTHROPIC_API_KEY",
        "label": "Anthropic key",
        "group": "Keys",
        "kind": "secret",
    },
    {"key": "GEMINI_API_KEY", "label": "Gemini key", "group": "Keys", "kind": "secret"},
    {
        "key": "OPENCODE_ZEN_API_KEY",
        "label": "OpenCode Zen key",
        "group": "Keys",
        "kind": "secret",
    },
    {
        "key": "CTF_MODELS",
        "label": "Default solver lineup",
        "group": "Engine",
        "kind": "models",
        "help": "Comma-separated provider/model[/effort]. Empty uses backend defaults.",
    },
    {
        "key": "MAX_CONCURRENT_CHALLENGES",
        "label": "Concurrent challenges",
        "group": "Engine",
        "kind": "number",
    },
    {
        "key": "CONTAINER_MEMORY_LIMIT",
        "label": "Container memory",
        "group": "Engine",
        "kind": "text",
        "placeholder": "4g",
    },
    {"key": "CTF_MSG_PORT", "label": "Coordinator port", "group": "Engine", "kind": "number"},
    {
        "key": "CTF_BUDGET_USD",
        "label": "Budget USD (0 = off)",
        "group": "Engine",
        "kind": "number",
    },
    {
        "key": "CTF_TOTAL_HOURS",
        "label": "Event hours",
        "group": "Engine",
        "kind": "number",
    },
    {
        "key": "CTF_BLOCK_PRIVATE_FETCH",
        "label": "Block private fetches",
        "group": "Engine",
        "kind": "text",
        "placeholder": "empty or 1",
    },
]

MODEL_CATALOG: list[dict[str, Any]] = [
    {
        "spec": "deepseek/deepseek-flash",
        "label": "DeepSeek Flash",
        "provider": "deepseek",
        "solver": True,
        "requires": "DEEPSEEK_API_KEY",
        "note": "Fast, vision, 1M context. Interim default.",
    },
    {
        "spec": "deepseek/deepseek-v4-pro",
        "label": "DeepSeek V4 Pro",
        "provider": "deepseek",
        "solver": True,
        "requires": "DEEPSEEK_API_KEY",
        "note": "Deeper reasoning, 1M context, text only.",
    },
    {
        "spec": "codex/gpt-5.4",
        "label": "Codex GPT-5.4",
        "provider": "codex",
        "solver": True,
        "requires": "codex login",
        "note": "Codex CLI solver.",
    },
    {
        "spec": "codex/gpt-5.4-mini",
        "label": "Codex GPT-5.4 Mini",
        "provider": "codex",
        "solver": True,
        "requires": "codex login",
        "note": "Cheaper Codex solver.",
    },
    {
        "spec": "codex/gpt-5.3-codex",
        "label": "Codex GPT-5.3",
        "provider": "codex",
        "solver": True,
        "requires": "codex login",
        "note": "Codex-tuned model.",
    },
    {
        "spec": "claude-sdk/claude-opus-4-6/medium",
        "label": "Claude Opus 4.6 medium",
        "provider": "claude-sdk",
        "solver": True,
        "requires": "claude login",
        "note": "Claude Agent SDK solver.",
    },
    {
        "spec": "claude-sdk/claude-opus-4-6/max",
        "label": "Claude Opus 4.6 max",
        "provider": "claude-sdk",
        "solver": True,
        "requires": "claude login",
        "note": "Highest effort, most expensive.",
    },
    {
        "spec": "opencode/big-pickle",
        "label": "Big Pickle",
        "provider": "opencode",
        "solver": False,
        "requires": "opencode CLI",
        "note": "Commander/CLI only. Raw Zen API is free-tier limited.",
    },
]

ENV_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
MODEL_RE = re.compile(
    r"^(bedrock|azure|deepseek|zen|google|claude-sdk|codex)/"
    r"[A-Za-z0-9._:-]+(?:/(?:low|medium|high|max))?$"
)


class PanelError(Exception):
    """User-facing validation or operation failure."""


def read_env_file(path: Path | str = ENV_FILE) -> dict[str, str]:
    path = Path(path)
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        values[key] = value
    return values


def _format_env_value(value: str) -> str:
    if "\n" in value or "\r" in value:
        raise PanelError("environment values cannot contain newlines")
    if value and (any(char.isspace() for char in value) or "#" in value):
        return '"' + value.replace('"', "'") + '"'
    return value


def write_env_file(updates: dict[str, Any], path: Path | str = ENV_FILE) -> None:
    path = Path(path)
    unknown = set(updates) - set(MANAGED_KEYS)
    if unknown:
        raise PanelError(f"not editable: {', '.join(sorted(unknown))}")
    clean = {key: str(value).strip() for key, value in updates.items()}

    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    out: list[str] = []
    seen: set[str] = set()
    for line in lines:
        match = ENV_RE.match(line)
        if match and match.group(1) in clean:
            key = match.group(1)
            if key in seen:
                continue
            out.append(f"{key}={_format_env_value(clean[key])}")
            seen.add(key)
        else:
            out.append(line)

    for field in CONFIG_FIELDS:
        key = field["key"]
        if key in clean and key not in seen:
            out.append(f"{key}={_format_env_value(clean[key])}")
            seen.add(key)

    text = "\n".join(out).rstrip() + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    try:
        tmp.chmod(0o600)
    except OSError:
        pass
    tmp.replace(path)


def reload_env(path: Path | str = ENV_FILE) -> dict[str, str]:
    values = read_env_file(path)
    for key in MANAGED_KEYS:
        if key in values:
            os.environ[key] = values[key]
        else:
            os.environ.pop(key, None)
    return values


def public_config(path: Path | str = ENV_FILE) -> dict[str, Any]:
    values = read_env_file(path)
    rendered: dict[str, dict[str, Any]] = {}
    for field in CONFIG_FIELDS:
        key = field["key"]
        raw = values.get(key, "")
        if key in SECRET_KEYS:
            rendered[key] = {
                "set": bool(raw),
                "hint": raw[-4:] if len(raw) >= 8 else "",
                "value": "",
            }
        else:
            rendered[key] = {"set": bool(raw), "value": raw}
    return {
        "fields": CONFIG_FIELDS,
        "values": rendered,
        "secrets": sorted(SECRET_KEYS),
        "models": model_catalog(values),
        "default_models": default_models(),
    }


def _key_ready(values: dict[str, str], key: str) -> bool:
    return bool(values.get(key, ""))


def model_catalog(values: dict[str, str] | None = None) -> list[dict[str, Any]]:
    values = values or read_env_file()
    catalog: list[dict[str, Any]] = []
    for item in MODEL_CATALOG:
        row = dict(item)
        requires = row.pop("requires")
        if requires.startswith("DEEPSEEK") or requires.endswith("_API_KEY"):
            available = _key_ready(values, requires)
        elif requires == "codex login":
            available = shutil.which("codex") is not None
        elif requires == "claude login":
            available = shutil.which("claude") is not None
        elif requires == "opencode CLI":
            available = shutil.which("opencode") is not None
        else:
            available = False
        row["available"] = available
        row["requires"] = requires
        catalog.append(row)
    return catalog


def default_models() -> list[str]:
    try:
        from backend.models import DEFAULT_MODELS
    except Exception:
        return []
    return list(DEFAULT_MODELS)


def validate_updates(updates: dict[str, Any]) -> dict[str, str]:
    unknown = set(updates) - set(MANAGED_KEYS)
    if unknown:
        raise PanelError(f"not editable: {', '.join(sorted(unknown))}")
    clean: dict[str, str] = {}
    for key, value in updates.items():
        text = str(value).strip()
        if key in SECRET_KEYS and text == "":
            continue
        if key == "MAX_CONCURRENT_CHALLENGES":
            number = _int(text, key)
            if not 1 <= number <= 64:
                raise PanelError("MAX_CONCURRENT_CHALLENGES must be 1..64")
            text = str(number)
        elif key == "CTF_MSG_PORT":
            number = _int(text, key)
            if not 0 <= number <= 65535:
                raise PanelError("CTF_MSG_PORT must be 0..65535")
            text = str(number)
        elif key in ("CTF_BUDGET_USD", "CTF_TOTAL_HOURS"):
            try:
                number = float(text or 0)
            except ValueError as exc:
                raise PanelError(f"{key} must be a number") from exc
            if number < 0:
                raise PanelError(f"{key} cannot be negative")
            text = str(number)
        elif key == "CTF_MODELS":
            for spec in _split_models(text):
                validate_model_spec(spec)
        elif key == "CTFD_URL" and text and not text.startswith(("http://", "https://")):
            raise PanelError("CTFD_URL must start with http:// or https://")
        elif key == "CONTAINER_MEMORY_LIMIT" and text and not re.fullmatch(r"\d+(?:\.\d+)?[mMgG]", text):
            raise PanelError("CONTAINER_MEMORY_LIMIT must look like 4g or 4096m")
        elif key == "CTF_BLOCK_PRIVATE_FETCH" and text not in ("", "0", "1"):
            raise PanelError("CTF_BLOCK_PRIVATE_FETCH must be empty, 0, or 1")
        elif key == "DEEPSEEK_BASE_URL" and text and not text.startswith(("http://", "https://")):
            raise PanelError("DEEPSEEK_BASE_URL must start with http:// or https://")
        if "\n" in text or "\r" in text:
            raise PanelError(f"{key} cannot contain newlines")
        clean[key] = text
    return clean


def update_config(updates: dict[str, Any], path: Path | str = ENV_FILE) -> dict[str, Any]:
    clean = validate_updates(updates)
    write_env_file(clean, path)
    reload_env(path)
    return public_config(path)


def _int(value: str, key: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise PanelError(f"{key} must be an integer") from exc


def _split_models(value: str | list[str] | tuple[str, ...]) -> list[str]:
    parts = value.replace("\n", ",").split(",") if isinstance(value, str) else list(value)
    return [part.strip() for part in parts if part and part.strip()]


def validate_model_spec(spec: str) -> None:
    if not MODEL_RE.fullmatch(spec):
        raise PanelError(
            f"unsupported solver spec: {spec!r} "
            "(expected provider/model[/low|medium|high|max])"
        )


def panel_authorized(supplied: str, expected: str) -> bool:
    if not expected:
        return True
    return hmac.compare_digest(supplied, expected)


def challenge_root(root: Path | str = CHALLENGES) -> Path:
    return Path(root).resolve()


def challenge_path(slug: str, root: Path | str = CHALLENGES) -> Path:
    slug = str(slug).strip()
    if not SLUG_RE.fullmatch(slug):
        raise PanelError("invalid challenge slug")
    base = challenge_root(root)
    path = (base / slug).resolve()
    if path.parent != base:
        raise PanelError("challenge path escapes the challenges directory")
    return path


def _safe_filename(name: str) -> str:
    name = Path(str(name)).name
    name = re.sub(r'[\x00-\x1f<>:"/\\|?*]', "_", name).strip(". ")
    if not name or name in (".", ".."):
        raise PanelError("invalid upload filename")
    return name


def _parse_tags(value: Any) -> list[str]:
    if isinstance(value, list):
        items = [str(item) for item in value]
    else:
        items = str(value or "").split(",")
    return [item.strip() for item in items if item and item.strip()]


def _parse_hints(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    hints: list[dict[str, Any]] = []
    for raw in str(value or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            cost = _int(parts[0].strip() or "0", "hint cost")
            title = parts[1].strip()
            content = parts[2].strip()
            hint: dict[str, Any] = {"cost": cost, "content": content}
            if title:
                hint["title"] = title
        elif len(parts) == 2:
            cost = _int(parts[0].strip() or "0", "hint cost")
            hint = {"cost": cost, "content": parts[1].strip()}
        else:
            hint = {"cost": 0, "content": line}
        hints.append(hint)
    return hints


def _sanitize(meta: dict[str, Any]) -> dict[str, Any]:
    try:
        from tools.sanitize_desc import sanitize_meta
    except Exception:
        return meta
    result = sanitize_meta(meta)
    return result if result is not None else meta


def _challenge_summary(path: Path) -> dict[str, Any]:
    meta = load_meta(path / "metadata.yml")
    distfiles = path / "distfiles"
    files: list[dict[str, Any]] = []
    if distfiles.exists():
        for child in sorted(distfiles.iterdir()):
            if child.is_file():
                files.append({"name": child.name, "size": child.stat().st_size})
    return {
        "slug": path.name,
        "name": meta.get("name", path.name),
        "category": meta.get("category", ""),
        "value": meta.get("value", 0),
        "description": meta.get("description", ""),
        "connection_info": meta.get("connection_info", ""),
        "tags": meta.get("tags", []),
        "hints": meta.get("hints", []),
        "ground_truth": meta.get("ground_truth", ""),
        "adversarial": meta.get("adversarial", {}),
        "sanitized": bool(meta.get("sanitized", False)),
        "files": files,
        "file_count": len(files),
        "file_bytes": sum(int(item["size"]) for item in files),
    }


def list_challenges(root: Path | str = CHALLENGES) -> list[dict[str, Any]]:
    base = challenge_root(root)
    if not base.exists():
        return []
    rows: list[dict[str, Any]] = []
    for meta_path in base.rglob("metadata.yml"):
        path = meta_path.parent.resolve()
        if not path.is_relative_to(base):
            continue
        rows.append(_challenge_summary(path))
    rows.sort(key=lambda row: str(row["name"]).lower())
    return rows


def get_challenge(slug: str, root: Path | str = CHALLENGES) -> dict[str, Any]:
    path = challenge_path(slug, root)
    if not (path / "metadata.yml").is_file():
        raise PanelError(f"challenge not found: {slug}")
    return _challenge_summary(path)


def save_challenge(
    data: dict[str, Any],
    files: list[tuple[str, bytes]] | None = None,
    root: Path | str = CHALLENGES,
) -> dict[str, Any]:
    name = str(data.get("name") or "").strip()
    if not name:
        raise PanelError("challenge name is required")
    explicit = str(data.get("slug") or "").strip()
    slug = explicit if explicit else slugify(name)
    if not SLUG_RE.fullmatch(slug):
        raise PanelError("slug must be lowercase letters, digits, and hyphens")

    original = str(data.get("original_slug") or "").strip()
    path = challenge_path(slug, root)
    if original and original != slug:
        old = challenge_path(original, root)
        if old.exists() and not path.exists():
            old.rename(path)

    value_raw = str(data.get("value") or "0").strip() or "0"
    value = _int(value_raw, "value")
    meta: dict[str, Any] = {
        "version": "beta1",
        "name": name,
        "category": str(data.get("category") or "").strip(),
        "value": value,
        "description": str(data.get("description") or "").strip(),
    }
    tags = _parse_tags(data.get("tags"))
    if tags:
        meta["tags"] = tags
    connection = str(data.get("connection_info") or "").strip()
    if connection:
        meta["connection_info"] = connection
    hints = _parse_hints(data.get("hints"))
    if hints:
        meta["hints"] = hints
    ground_truth = str(data.get("ground_truth") or "").strip()
    if ground_truth:
        meta["ground_truth"] = ground_truth
    meta = _sanitize(meta)

    path.mkdir(parents=True, exist_ok=True)
    distfiles = path / "distfiles"
    if files:
        if not distfiles.resolve().is_relative_to(path.resolve()):
            raise PanelError("distfiles directory escapes the challenge directory")
        if str(data.get("replace_files") or "").lower() in ("1", "true", "on", "yes"):
            shutil.rmtree(distfiles, ignore_errors=True)
        distfiles.mkdir(exist_ok=True)
        for filename, payload in files:
            safe = _safe_filename(filename)
            (distfiles / safe).write_bytes(payload)

    (path / "metadata.yml").write_text(
        yaml.safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return _challenge_summary(path)


def delete_challenge(slug: str, root: Path | str = CHALLENGES) -> None:
    path = challenge_path(slug, root)
    if not path.exists():
        raise PanelError(f"challenge not found: {slug}")
    shutil.rmtree(path)


def parse_multipart(
    content_type: str, body: bytes
) -> tuple[dict[str, str], list[tuple[str, bytes]]]:
    if not content_type.lower().startswith("multipart/form-data"):
        raise PanelError("expected multipart/form-data")
    header = (
        f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n"
    ).encode("utf-8", errors="replace")
    message = BytesParser(policy=policy.HTTP).parsebytes(header + body)
    if not message.is_multipart():
        raise PanelError("malformed multipart body")
    fields: dict[str, str] = {}
    files: list[tuple[str, bytes]] = []
    for part in message.iter_parts():
        disposition = part.get("Content-Disposition", "")
        if "form-data" not in disposition:
            continue
        name = part.get_param("name", header="content-disposition")
        if not name:
            continue
        payload = part.get_payload(decode=True) or b""
        filename = part.get_filename()
        if filename:
            files.append((_safe_filename(filename), payload))
        else:
            fields[str(name)] = payload.decode("utf-8", errors="replace")
    return fields, files


def engine_env(base: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(base or os.environ)
    for key in list(env):
        if key in MANAGED_KEYS or key.startswith(("CTF_", "CTFD_")):
            env.pop(key, None)
    return env


def build_engine_args(options: dict[str, Any], root: Path | str = ROOT) -> list[str]:
    root = Path(root)
    mode = str(options.get("mode") or "coordinator")
    args = [sys.executable, "-m", "backend.cli"]
    if mode == "single":
        slug = str(options.get("challenge") or "").strip()
        path = challenge_path(slug, root / "challenges")
        if not (path / "metadata.yml").is_file():
            raise PanelError(f"challenge not found: {slug}")
        args += ["--challenge", str(path)]
    elif mode == "coordinator":
        args += ["--challenges-dir", "challenges"]
    else:
        raise PanelError("mode must be coordinator or single")

    models = _split_models(options.get("models") or [])
    for spec in models:
        validate_model_spec(spec)
        args += ["--models", spec]

    max_challenges = _int(str(options.get("max_challenges") or "1"), "max_challenges")
    if not 1 <= max_challenges <= 64:
        raise PanelError("max_challenges must be 1..64")
    args += ["--max-challenges", str(max_challenges)]

    if mode == "coordinator":
        coordinator = str(options.get("coordinator") or "codex")
        if coordinator not in ("codex", "claude"):
            raise PanelError("coordinator must be codex or claude")
        args += ["--coordinator", coordinator]
        coordinator_model = str(options.get("coordinator_model") or "").strip()
        if coordinator_model:
            args += ["--coordinator-model", coordinator_model]

    msg_port = _int(str(options.get("msg_port") or "9400"), "msg_port")
    if not 0 <= msg_port <= 65535:
        raise PanelError("msg_port must be 0..65535")
    args += ["--msg-port", str(msg_port)]
    if options.get("no_submit", True):
        args += ["--no-submit"]
    if options.get("verbose", True):
        args += ["-v"]
    return args


class EngineSupervisor:
    """Start/stop the engine and capture its console log."""

    def __init__(self, root: Path | str = ROOT, log_path: Path | str = ENGINE_LOG) -> None:
        self.root = Path(root)
        self.log_path = Path(log_path)
        self._lock = threading.RLock()
        self._proc: subprocess.Popen[str] | None = None
        self._handle: Any = None
        self._args: list[str] = []
        self._started_at = 0.0
        self._returncode: int | None = None

    def _reap(self) -> None:
        if self._proc is not None and self._proc.poll() is not None:
            self._returncode = self._proc.returncode
            self._proc = None
            if self._handle is not None:
                self._handle.close()
                self._handle = None

    def status(self) -> dict[str, Any]:
        with self._lock:
            self._reap()
            running = self._proc is not None
            return {
                "running": running,
                "pid": self._proc.pid if self._proc else None,
                "started_at": self._started_at,
                "elapsed_s": round(time.time() - self._started_at, 1) if running else 0.0,
                "returncode": self._returncode,
                "args": self._args,
                "log_tail": self.log_tail(),
            }

    def log_tail(self, limit: int = 250) -> list[str]:
        path = self.log_path
        if not path.exists():
            return []
        try:
            size = path.stat().st_size
            with open(path, "rb") as handle:
                if size > 131_072:
                    handle.seek(size - 131_072)
                data = handle.read()
        except OSError:
            return []
        lines = data.decode("utf-8", errors="replace").splitlines()
        return lines[-limit:]

    def start(self, options: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            self._reap()
            if self._proc is not None:
                raise PanelError("engine is already running")
            args = build_engine_args(options, self.root)
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            handle = open(self.log_path, "a", encoding="utf-8", buffering=1)
            handle.write(f"\n=== {time.strftime('%Y-%m-%d %H:%M:%S')} engine start ===\n")
            handle.write("$ " + subprocess.list2cmdline(args) + "\n")
            handle.flush()
            kwargs: dict[str, Any] = {}
            if os.name == "nt":
                kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                kwargs["start_new_session"] = True
            try:
                self._proc = subprocess.Popen(
                    args,
                    cwd=self.root,
                    env=engine_env(),
                    stdin=subprocess.DEVNULL,
                    stdout=handle,
                    stderr=subprocess.STDOUT,
                    text=True,
                    **kwargs,
                )
            except Exception:
                handle.close()
                raise
            self._handle = handle
            self._args = args
            self._started_at = time.time()
            self._returncode = None
            return self.status()

    def stop(self) -> dict[str, Any]:
        with self._lock:
            self._reap()
            proc = self._proc
            if proc is None:
                return self.status()
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            else:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    except ProcessLookupError:
                        pass
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
            self._reap()
            return self.status()
