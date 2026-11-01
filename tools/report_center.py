"""Single-page operator console for the running CTF engine (stdlib only).

Usage:
    uv run python -m tools.report_center
    uv run python tools/report_center.py --port 8080

Endpoints:
    GET  /                 dashboard
    GET  /api/status       solved/challenges/cost/active/stalled
    GET  /api/trace?name=  tail of one trace
    GET  /api/habits       recent habit findings
    POST /api/msg          {"message": "..."} -> coordinator :9400
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import time
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import flags as flag_store  # noqa: E402
from tools import panel_ops, walkthrough  # noqa: E402
from tools.ctf_common import (  # noqa: E402
    LOGS,
    REPORTS,
    WALKTHROUGHS,
    ctfd_scoreboard,
    env,
    env_float,
    iter_traces,
    load_dotenv,
    post_msg,
)
from tools.panel_ui import CONTROL_HTML  # noqa: E402
from tools.status import build_status  # noqa: E402

STATUS_TTL = 3.0
ENGINE = panel_ops.EngineSupervisor()


class BodyTooLargeError(Exception):
    """Request body exceeded the configured panel limit."""


_cache: dict[str, Any] = {"ts": 0.0, "status": {}, "scoreboard": []}


def get_state(force: bool = False) -> dict[str, Any]:
    now = time.time()
    if not force and now - float(_cache["ts"]) < STATUS_TTL and _cache["status"]:
        return {"status": _cache["status"], "scoreboard": _cache["scoreboard"]}
    traces = iter_traces(LOGS)
    status = build_status(traces)
    try:
        scoreboard = ctfd_scoreboard(limit=12)
    except Exception:
        scoreboard = []
    _cache.update(ts=now, status=status, scoreboard=scoreboard)
    return {"status": status, "scoreboard": scoreboard}


def trace_names() -> list[str]:
    if not LOGS.exists():
        return []
    return [path.name for path in sorted(LOGS.glob("trace-*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)]


def trace_tail(name: str, limit: int = 200) -> dict[str, Any]:
    safe = Path(name).name
    if safe != name or not safe.startswith("trace-") or not safe.endswith(".jsonl"):
        raise ValueError("invalid trace name")
    path = LOGS / safe
    if not path.exists():
        raise FileNotFoundError(safe)
    lines = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-limit:]
    events: list[dict[str, Any]] = []
    for line in lines:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append({"type": "raw", "text": line[:500]})
    return {"name": safe, "size": path.stat().st_size, "events": events}


def habits(limit: int = 80) -> list[dict[str, Any]]:
    path = REPORTS / "habits.jsonl"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-limit:]
    out: list[dict[str, Any]] = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return list(reversed(out))


class Handler(BaseHTTPRequestHandler):
    server_version = "CTFOperator/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        if self.path.startswith("/api/"):
            return
        super().log_message(format, *args)

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, data: Any, status: int = HTTPStatus.OK) -> None:
        self._send(status, json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json")

    def _authorized(self) -> bool:
        return panel_ops.panel_authorized(
            self.headers.get("X-Panel-Token", ""),
            env("PANEL_TOKEN", ""),
        )

    def _require_auth(self) -> bool:
        if self._authorized():
            return True
        self._json({"error": "unauthorized"}, HTTPStatus.UNAUTHORIZED)
        return False

    def _read_body(self, limit: int) -> bytes:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("bad Content-Length") from exc
        if length <= 0:
            raise ValueError("empty body")
        if length > limit:
            raise BodyTooLargeError(f"body exceeds {limit} bytes")
        return self.rfile.read(length)

    def _read_json(self, limit: int = 64 * 1024) -> dict[str, Any]:
        body = self._read_body(limit)
        try:
            data = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"bad json: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError("expected a JSON object")
        return data

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        try:
            if parsed.path == "/":
                self._send(
                    HTTPStatus.OK,
                    INDEX_HTML.encode("utf-8"),
                    "text/html; charset=utf-8",
                )
            elif parsed.path == "/control":
                self._send(
                    HTTPStatus.OK,
                    CONTROL_HTML.encode("utf-8"),
                    "text/html; charset=utf-8",
                )
            elif parsed.path in ("/api/config", "/api/engine", "/api/challenges", "/api/flags"):
                if not self._require_auth():
                    return
                if parsed.path == "/api/config":
                    self._json(panel_ops.public_config())
                elif parsed.path == "/api/engine":
                    self._json(ENGINE.status())
                elif parsed.path == "/api/flags":
                    self._json(flag_store.refresh_flags())
                else:
                    slug = (params.get("slug") or [""])[0]
                    if slug:
                        self._json({"challenge": panel_ops.get_challenge(slug)})
                    else:
                        self._json({"challenges": panel_ops.list_challenges()})
            elif parsed.path == "/api/status":
                state = get_state()
                state["traces"] = trace_names()
                self._json(state)
            elif parsed.path == "/api/trace":
                name = (params.get("name") or [""])[0]
                limit = min(1000, int((params.get("limit") or ["200"])[0]))
                self._json(trace_tail(name, limit))
            elif parsed.path == "/api/habits":
                self._json({"habits": habits()})
            elif parsed.path == "/api/health":
                self._json({"ok": True, "ts": time.time()})
            else:
                self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
        except (ValueError, panel_ops.PanelError) as exc:
            self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except FileNotFoundError as exc:
            self._json({"error": f"trace not found: {exc}"}, HTTPStatus.NOT_FOUND)
        except Exception as exc:
            self._json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_DELETE(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if parsed.path != "/api/challenges":
            self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return
        if not self._require_auth():
            return
        try:
            slug = (params.get("slug") or [""])[0]
            panel_ops.delete_challenge(slug)
            self._json({"ok": True})
        except (ValueError, panel_ops.PanelError) as exc:
            self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except Exception as exc:
            self._json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        try:
            if parsed.path == "/api/msg":
                data = self._read_json()
                message = str(data.get("message", "")).strip()
                if not message:
                    self._json({"error": "empty message"}, HTTPStatus.BAD_REQUEST)
                    return
                ok, response = post_msg(message)
                self._json(
                    {"ok": ok, "response": response},
                    HTTPStatus.OK if ok else HTTPStatus.BAD_GATEWAY,
                )
                return

            if not self._require_auth():
                return

            if parsed.path == "/api/config":
                data = self._read_json()
                updates = data.get("updates")
                if not isinstance(updates, dict):
                    self._json({"error": "updates must be an object"}, HTTPStatus.BAD_REQUEST)
                    return
                self._json(panel_ops.update_config(updates))
            elif parsed.path == "/api/engine/start":
                self._json(ENGINE.start(self._read_json()))
            elif parsed.path == "/api/engine/stop":
                self._json(ENGINE.stop())
            elif parsed.path == "/api/flags/refresh":
                self._json(flag_store.refresh_flags())
            elif parsed.path == "/api/walkthroughs":
                data = self._read_json() if self.headers.get("Content-Length") else {}
                force = bool(data.get("force", True))
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = walkthrough.main(["--force"] if force else [])
                files = [
                    path.name
                    for path in sorted(WALKTHROUGHS.glob("*.md"), key=lambda p: p.name)
                ]
                self._json(
                    {
                        "ok": code == 0,
                        "force": force,
                        "output": output.getvalue(),
                        "files": files,
                    }
                )
            elif parsed.path == "/api/challenges":
                max_mb = env_float("PANEL_MAX_UPLOAD_MB", 128.0)
                limit = int(max(1.0, max_mb) * 1024 * 1024)
                body = self._read_body(limit)
                fields, files = panel_ops.parse_multipart(
                    self.headers.get("Content-Type", ""), body
                )
                challenge = panel_ops.save_challenge(fields, files)
                self._json({"ok": True, "challenge": challenge})
            else:
                self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
        except BodyTooLargeError as exc:
            self._json({"error": str(exc)}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        except (ValueError, panel_ops.PanelError) as exc:
            self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except Exception as exc:
            self._json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)


INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CTF OPS</title>
<style>
:root{--bg:#0b0f14;--panel:#111821;--line:#22303f;--fg:#d7e2ee;--dim:#7d93a8;
--acc:#4cc2ff;--ok:#3ddc97;--warn:#ffc857;--bad:#ff6b6b;--mono:ui-monospace,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,Segoe UI,sans-serif}
header{display:flex;gap:18px;align-items:baseline;padding:10px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:3}
h1{font-size:16px;margin:0;letter-spacing:.12em;color:var(--acc)}
.stat{color:var(--dim)} .stat b{color:var(--fg);font-family:var(--mono)}
main{display:grid;grid-template-columns:280px 1fr 1.25fr;gap:10px;padding:10px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px;min-width:0}
.panel h2{font-size:11px;letter-spacing:.14em;color:var(--dim);margin:0 0 8px;text-transform:uppercase}
.panel.wide{grid-column:span 2}
.row{display:flex;justify-content:space-between;gap:8px;padding:3px 0;border-bottom:1px dashed #1b2632}
.row:last-child{border-bottom:0}
.mono{font-family:var(--mono);font-size:12px}
.dim{color:var(--dim)} .ok{color:var(--ok)} .warn{color:var(--warn)} .bad{color:var(--bad)}
table{width:100%;border-collapse:collapse;font-size:12px}
th,td{text-align:left;padding:4px 6px;border-bottom:1px solid #1b2632;white-space:nowrap}
th{color:var(--dim);font-weight:500;font-size:10px;letter-spacing:.1em;text-transform:uppercase}
tr.active{cursor:pointer} tr.active:hover{background:#16212d}
#tail{height:52vh;overflow:auto;font-family:var(--mono);font-size:11px;background:#080c11;border:1px solid #1b2632;border-radius:6px;padding:8px}
.ev{padding:2px 0;border-bottom:1px solid #101820;white-space:pre-wrap;word-break:break-word}
.ev .t{color:var(--dim)} .ev.call{color:var(--acc)} .ev.flag{color:var(--ok)}
.ev.err{color:var(--bad)} .ev.usage{color:var(--warn)}
textarea{width:100%;height:64px;background:#080c11;border:1px solid var(--line);color:var(--fg);border-radius:6px;padding:8px;font-family:var(--mono);resize:vertical}
button{background:var(--acc);color:#04121b;border:0;border-radius:6px;padding:7px 12px;font-weight:700;cursor:pointer;margin-top:6px}
button:disabled{opacity:.5;cursor:default}
#msgout{font-family:var(--mono);font-size:11px;color:var(--dim);margin-left:8px}
footer{color:var(--dim);font-family:var(--mono);font-size:11px;padding:4px 16px 14px}
@media(max-width:1100px){main{grid-template-columns:1fr 1fr}.panel.wide{grid-column:span 2}}
@media(max-width:700px){main{grid-template-columns:1fr}.panel.wide{grid-column:span 1}}
</style>
</head>
<body>
<header>
  <h1>CTF OPS</h1>
  <a class="stat" href="/control" style="color:var(--acc);text-decoration:none">control &rarr;</a>
  <div class="stat">solved <b id="s-solved">-</b></div>
  <div class="stat">cost <b id="s-cost">-</b></div>
  <div class="stat">burn <b id="s-burn">-</b></div>
  <div class="stat">flags/h <b id="s-fph">-</b></div>
  <div class="stat">elapsed <b id="s-elapsed">-</b></div>
  <div class="stat">active <b id="s-active">-</b></div>
  <div class="stat">stalled <b id="s-stalled">-</b></div>
  <div class="stat" style="margin-left:auto" id="s-clock">-</div>
</header>
<main>
  <section class="panel">
    <h2>Scoreboard</h2>
    <div id="scoreboard" class="mono"></div>
  </section>
  <section class="panel">
    <h2>Challenges</h2>
    <div style="max-height:44vh;overflow:auto"><table>
      <thead><tr><th>Name</th><th>Cat</th><th>Pts</th><th>Cost</th><th>Steps</th></tr></thead>
      <tbody id="challenges"></tbody>
    </table></div>
  </section>
  <section class="panel">
    <h2>Live traces <span class="dim" id="tracecount"></span></h2>
    <div style="max-height:42vh;overflow:auto"><table>
      <thead><tr><th>Challenge</th><th>Model</th><th>Steps</th><th>Cost</th><th>Idle</th><th>Status</th></tr></thead>
      <tbody id="traces"></tbody>
    </table></div>
  </section>
  <section class="panel wide">
    <h2>Trace tail <span class="dim" id="tailname">select a trace</span></h2>
    <div id="tail"></div>
  </section>
  <section class="panel">
    <h2>Habits</h2>
    <div id="habits" class="mono" style="max-height:42vh;overflow:auto"></div>
  </section>
  <section class="panel wide">
    <h2>Operator message</h2>
    <textarea id="msg" placeholder="kill swarm X, respawn 2 models / GROUND TRUTH: ..."></textarea>
    <button id="send">Send to coordinator</button><span id="msgout"></span>
    <div class="dim mono" style="margin-top:8px">Engine must be running with --msg-port 9400.</div>
  </section>
</main>
<footer id="footer">-</footer>
<script>
let selected = null;
let statusData = null;
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fmtDur = s => { s = Math.max(0, Math.round(s)); if (s < 60) return s+"s"; const m = Math.floor(s/60); if (m < 60) return m+"m"; return Math.floor(m/60)+"h"+(m%60)+"m"; };
const fmtMoney = n => "$" + Number(n || 0).toFixed(2);

async function tick() {
  try {
    const r = await fetch("/api/status");
    const data = await r.json();
    statusData = data;
    renderStatus(data);
    await renderTail();
  } catch (e) {
    document.getElementById("s-clock").textContent = "disconnected";
  }
}

function renderStatus(data) {
  const s = data.status;
  document.getElementById("s-solved").textContent = s.solved_count + "/" + s.challenge_count;
  document.getElementById("s-cost").textContent = fmtMoney(s.cost_usd);
  document.getElementById("s-burn").textContent = fmtMoney(s.burn_per_hour) + "/h";
  document.getElementById("s-fph").textContent = Number(s.flags_per_hour || 0).toFixed(2);
  document.getElementById("s-elapsed").textContent = fmtDur(s.elapsed_s);
  document.getElementById("s-active").textContent = s.active.length;
  document.getElementById("s-stalled").textContent = s.stalled.length;
  document.getElementById("s-clock").textContent = new Date().toLocaleTimeString();

  const sb = data.scoreboard || [];
  document.getElementById("scoreboard").innerHTML = sb.length
    ? sb.map((t, i) => `<div class="row"><span>${i+1}. ${esc(t.name || t.team || "?")}</span><b>${esc(t.score ?? t.value ?? 0)}</b></div>`).join("")
    : `<div class="dim">No scoreboard (CTFD_TOKEN missing or unreachable)</div>`;

  const ch = s.challenges || [];
  document.getElementById("challenges").innerHTML = ch.length ? ch.map(c => {
    const cls = c.solved ? "ok" : (c.models.length ? "warn" : "dim");
    return `<tr><td class="${cls}" title="${esc(c.name)}">${esc(c.name.slice(0,34))}</td><td class="dim">${esc(c.category)}</td><td>${esc(c.value)}</td><td>${fmtMoney(c.cost_usd)}</td><td>${c.steps}</td></tr>`;
  }).join("") : `<tr><td colspan="5" class="dim">No traces yet</td></tr>`;

  const all = [...(s.active || []).map(x => ({...x, _live:true})), ...(s.stalled || []).map(x => ({...x, _live:false}))];
  all.sort((a,b) => a.challenge.localeCompare(b.challenge));
  document.getElementById("tracecount").textContent = "(" + (data.traces || []).length + " files)";
  document.getElementById("traces").innerHTML = all.length ? all.map(t => {
    const cls = t._live ? "active" : "bad";
    const status = t._live ? "running" : t.status;
    const idle = t._live ? t.age_s : t.idle_s;
    return `<tr class="active" data-name="${esc(t.trace)}"><td class="warn">${esc(t.challenge.slice(0,26))}</td><td class="dim">${esc(t.model.slice(0,24))}</td><td>${t.steps}</td><td>${fmtMoney(t.cost_usd)}</td><td>${fmtDur(idle)}</td><td class="${cls}">${esc(status)}</td></tr>`;
  }).join("") : `<tr><td colspan="6" class="dim">No active or stalled solvers</td></tr>`;
  document.querySelectorAll("tr.active[data-name]").forEach(tr => tr.onclick = () => { selected = tr.dataset.name; renderTail(true); });

  if (!selected && (data.traces || []).length) selected = data.traces[0];
  const hs = s.habits || [];
  document.getElementById("habits").innerHTML = hs.length ? hs.slice().reverse().map(h =>
    `<div class="row"><span class="bad">${esc(h.name)}</span><span class="dim">${esc((h.challenge||"").slice(0,18))}/${esc((h.model||"").slice(0,14))}</span></div>` +
    `<div class="dim" style="padding:0 0 6px 6px">${esc(h.detail||"")}</div>`
  ).join("") : `<div class="dim">No findings yet</div>`;

  document.getElementById("footer").textContent =
    `updated ${new Date().toLocaleTimeString()} | traces ${data.traces?.length || 0} | ` +
    `ctfd ${s.ctfd?.reachable ? "ok" : "unreachable"} | ${s.ctfd?.url || ""}`;
}

async function renderTail(force) {
  if (!selected) { document.getElementById("tail").innerHTML = `<span class="dim">no trace selected</span>`; return; }
  document.getElementById("tailname").textContent = selected;
  const r = await fetch("/api/trace?name=" + encodeURIComponent(selected) + "&limit=250");
  const data = await r.json();
  if (data.error) { document.getElementById("tail").innerHTML = `<span class="bad">${esc(data.error)}</span>`; return; }
  const el = document.getElementById("tail");
  const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 40;
  el.innerHTML = data.events.map(ev => {
    const t = ev.type || "?";
    let cls = "";
    if (t === "tool_call") cls = "call";
    else if (t === "flag_confirmed" || t === "finish") cls = "flag";
    else if (t === "error" || t === "turn_failed") cls = "err";
    else if (t === "usage") cls = "usage";
    const body = t === "tool_call" ? `${ev.step ?? ""} ${ev.tool} ${ev.args ?? ""}`
      : t === "tool_result" ? `${ev.step ?? ""} ${ev.tool}: ${ev.result ?? ""}`
      : t === "model_response" ? (ev.text ?? "")
      : (ev.flag || ev.error || ev.status || ev.insights || ev.detail || "");
    return `<div class="ev ${cls}"><span class="t">${esc(t)}</span> ${esc(body)}</div>`;
  }).join("");
  if (atBottom) el.scrollTop = el.scrollHeight;
}

document.getElementById("send").onclick = async () => {
  const msg = document.getElementById("msg").value.trim();
  if (!msg) return;
  const out = document.getElementById("msgout");
  out.textContent = "sending...";
  const r = await fetch("/api/msg", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({message: msg})});
  const data = await r.json();
  out.textContent = data.ok ? "sent" : ("failed: " + (data.response || data.error || ""));
  if (data.ok) document.getElementById("msg").value = "";
};

tick();
setInterval(tick, 3000);
</script>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=env("REPORT_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(env_float("REPORT_PORT", 8080)))
    args = parser.parse_args(argv)
    panel_token = env("PANEL_TOKEN", "")
    if args.host not in ("127.0.0.1", "localhost", "::1") and not panel_token:
        print("Refusing to bind a non-loopback host without PANEL_TOKEN.", file=sys.stderr)
        print("Set PANEL_TOKEN in .env, or use --host 127.0.0.1.", file=sys.stderr)
        return 2
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Report center: http://{args.host}:{args.port}")
    print(f"  control:     http://{args.host}:{args.port}/control")
    print(f"  traces: {LOGS}")
    print(f"  coordinator: http://127.0.0.1:{env('CTF_MSG_PORT', '9400')}/msg")
    print(f"  auth:        {'token required' if panel_token else 'loopback only'}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
