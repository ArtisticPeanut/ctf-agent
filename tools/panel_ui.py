"""HTML/JS for the operator control panel (served by tools.report_center)."""

from __future__ import annotations

CONTROL_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CTF OPS / control</title>
<style>
:root{--bg:#0b0f14;--panel:#111821;--line:#22303f;--fg:#d7e2ee;--dim:#7d93a8;
--acc:#4cc2ff;--ok:#3ddc97;--warn:#ffc857;--bad:#ff6b6b;--mono:ui-monospace,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,Segoe UI,sans-serif}
header{display:flex;gap:18px;align-items:baseline;padding:10px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:3}
h1{font-size:16px;margin:0;letter-spacing:.12em} h1 a{color:var(--acc);text-decoration:none}
nav{display:flex;gap:10px} nav a{color:var(--dim);text-decoration:none} nav a.active{color:var(--acc)}
#clock{margin-left:auto;color:var(--dim);font-family:var(--mono);font-size:12px}
main{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px;padding:10px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px;min-width:0}
.panel.wide{grid-column:span 2}
.panel h2{font-size:11px;letter-spacing:.14em;color:var(--dim);margin:0 0 10px;text-transform:uppercase}
.note{text-transform:none;letter-spacing:0;color:var(--dim);font-size:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}
label{display:block;color:var(--dim);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
input,select,textarea{width:100%;margin-top:4px;background:#080c11;border:1px solid var(--line);color:var(--fg);border-radius:6px;padding:7px 8px;font:inherit}
textarea{font-family:var(--mono);font-size:12px;resize:vertical}
input:focus,select:focus,textarea:focus{outline:1px solid var(--acc)}
button{background:var(--acc);color:#04121b;border:0;border-radius:6px;padding:8px 12px;font-weight:700;cursor:pointer}
button.secondary{background:#1b2a39;color:var(--fg)}
button.danger{background:var(--bad);color:#1b0505}
button:disabled{opacity:.45;cursor:default}
.actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
.chip{border:1px solid var(--line);border-radius:999px;padding:4px 9px;font-size:11px;cursor:pointer;color:var(--dim);background:#0d151e}
.chip.on{border-color:var(--acc);color:var(--acc)}
.chip.off{opacity:.5;text-decoration:line-through}
.status{display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;margin-bottom:8px}
.status b{color:var(--fg)} .ok{color:var(--ok)} .warn{color:var(--warn)} .bad{color:var(--bad)} .dim{color:var(--dim)}
.log{height:220px;overflow:auto;background:#080c11;border:1px solid #1b2632;border-radius:6px;padding:8px;font:11px/1.4 var(--mono);white-space:pre-wrap;word-break:break-word}
.cfg-group{margin-top:12px;border-top:1px solid #1b2632;padding-top:10px}
.cfg-group h3{font-size:10px;color:var(--dim);letter-spacing:.12em;text-transform:uppercase;margin:0 0 8px}
.cfg-help{color:var(--dim);font-size:10px;margin-top:2px}
.split{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:12px}
table{width:100%;border-collapse:collapse;font-size:12px} th,td{text-align:left;padding:5px 6px;border-bottom:1px solid #1b2632;vertical-align:top}
th{color:var(--dim);font-weight:500;font-size:10px;letter-spacing:.1em;text-transform:uppercase}
td.name{color:var(--acc);cursor:pointer;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
td .mini{font-size:10px;color:var(--dim)}
.flag{font-family:var(--mono);font-size:10px;color:var(--warn);white-space:normal;word-break:break-word;max-width:160px}
#cfg-note,#ch-note,#e-note{font-size:11px;color:var(--dim)}
#ch-form{border-left:1px solid #1b2632;padding-left:12px}
footer{color:var(--dim);font-family:var(--mono);font-size:11px;padding:4px 16px 14px}
@media(max-width:1000px){main{grid-template-columns:1fr}.panel.wide{grid-column:span 1}.split{grid-template-columns:1fr}#ch-form{border-left:0;border-top:1px solid #1b2632;padding-left:0;padding-top:10px}}
</style>
</head>
<body>
<header>
  <h1><a href="/">CTF OPS</a></h1>
  <nav><a href="/">dashboard</a><a class="active" href="/control">control</a></nav>
  <span id="clock">-</span>
</header>
<main>
  <section class="panel">
    <h2>Engine <span id="e-note" class="note"></span></h2>
    <div class="status" id="engine-status"><span class="dim">loading...</span></div>
    <div class="grid">
      <label>Mode<select id="e-mode"><option value="coordinator">Coordinator</option><option value="single">Single challenge</option></select></label>
      <label>Challenge<select id="e-challenge"></select></label>
      <label>Coordinator<select id="e-coordinator"><option value="codex">codex</option><option value="claude">claude</option></select></label>
      <label>Coordinator model<input id="e-coord-model" placeholder="gpt-5.4"></label>
      <label>Max challenges<input id="e-max" type="number" min="1" max="64" value="1"></label>
      <label>Msg port<input id="e-port" type="number" value="9400"></label>
      <label>&nbsp;<span><input id="e-nosubmit" type="checkbox" checked style="width:auto;margin:0 6px 0 0">no submit</span></label>
    </div>
    <div style="margin-top:10px"><label>Solver lineup</label><div id="model-chips" class="chips"></div>
      <textarea id="e-models" rows="2" placeholder="deepseek/deepseek-flash,codex/gpt-5.4"></textarea></div>
    <div class="actions"><button id="e-start">Start engine</button><button id="e-stop" class="danger">Stop</button></div>
    <div style="margin-top:10px"><label>Engine console</label><pre id="engine-log" class="log"></pre></div>
  </section>

  <section class="panel">
    <h2>Configuration <span id="cfg-note" class="note"></span></h2>
    <form id="config-form" autocomplete="off"></form>
    <div class="actions"><button id="cfg-save">Save .env</button><button id="cfg-reload" class="secondary">Reload</button></div>
    <div class="note" style="margin-top:8px">Secrets are write-only: leave blank to keep the current value. The panel never returns key material.</div>
  </section>

  <section class="panel wide">
    <h2>Captured flags <span id="flag-note" class="note"></span></h2>
    <div class="actions" style="margin-top:0">
      <button id="flag-refresh" class="secondary">Refresh flags</button>
      <button id="wt-build" class="secondary">Save walkthroughs</button>
      <span class="note">Stored in <code>reports/flags.json</code> and <code>reports/flags.md</code>. Submit manually.</span>
    </div>
    <div style="max-height:30vh;overflow:auto;margin-top:8px"><table>
      <thead><tr><th>Challenge</th><th>Flag</th><th>Model</th><th>Confirmed</th><th>Trace</th></tr></thead>
      <tbody id="flag-list"></tbody>
    </table></div>
  </section>

  <section class="panel wide">
    <h2>Challenges <span id="ch-note" class="note"></span></h2>
    <div class="split">
      <div>
        <div class="actions" style="margin-top:0"><button id="ch-new" class="secondary">New challenge</button><button id="ch-refresh" class="secondary">Refresh</button></div>
        <div style="max-height:52vh;overflow:auto;margin-top:8px"><table>
          <thead><tr><th>Name</th><th>Cat</th><th>Pts</th><th>Files</th><th>Flags</th><th></th></tr></thead>
          <tbody id="ch-list"></tbody>
        </table></div>
      </div>
      <form id="ch-form" autocomplete="off">
        <input type="hidden" id="ch-original">
        <div class="grid">
          <label>Slug<input id="ch-slug" placeholder="auto from name"></label>
          <label>Name<input id="ch-name" required></label>
          <label>Category<input id="ch-category"></label>
          <label>Points<input id="ch-value" type="number" value="0"></label>
          <label>Tags<input id="ch-tags" placeholder="pwn, easy"></label>
          <label>Connection<input id="ch-conn" placeholder="nc host port"></label>
        </div>
        <label style="margin-top:8px">Description<textarea id="ch-desc" rows="5"></textarea></label>
        <label style="margin-top:8px">Hints <span class="note">one per line: cost|title|content</span><textarea id="ch-hints" rows="3"></textarea></label>
        <label style="margin-top:8px">Ground truth <span class="note">operator-only note</span><textarea id="ch-truth" rows="2"></textarea></label>
        <label style="margin-top:8px">Distfiles<input id="ch-files" type="file" multiple></label>
        <label style="margin-top:6px"><span><input id="ch-replace" type="checkbox" style="width:auto;margin:0 6px 0 0">replace existing distfiles</span></label>
        <div class="actions"><button id="ch-save">Save challenge</button><button id="ch-delete" class="danger" type="button">Delete</button></div>
      </form>
    </div>
  </section>
</main>
<footer id="footer">-</footer>
<script>
const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const KEY = "ctfPanelToken";
let token = localStorage.getItem(KEY) || "";
let cfg = null;
let challenges = [];
let busy = false;
let logPinned = true;

function setNote(el, text, cls) {
  const node = $(el);
  node.textContent = text || "";
  node.className = "note " + (cls || "");
}

async function api(path, opts = {}) {
  opts.headers = Object.assign({}, opts.headers || {});
  if (token) opts.headers["X-Panel-Token"] = token;
  if (opts.json !== undefined) {
    opts.body = JSON.stringify(opts.json);
    opts.headers["Content-Type"] = "application/json";
    delete opts.json;
  }
  const response = await fetch(path, opts);
  if (response.status === 401) {
    const entered = prompt("Panel token:");
    if (entered) {
      token = entered;
      localStorage.setItem(KEY, token);
      return api(path, opts);
    }
  }
  const type = response.headers.get("content-type") || "";
  const data = type.includes("json") ? await response.json() : await response.text();
  if (!response.ok) throw new Error((data && data.error) || data || response.statusText);
  return data;
}

function guard(fn) {
  return async (...args) => {
    if (busy) return;
    busy = true;
    try { await fn(...args); }
    catch (err) { setNote("#footer", String(err.message || err), "bad"); }
    finally { busy = false; }
  };
}

function renderConfig(data) {
  cfg = data;
  const groups = new Map();
  for (const field of data.fields) {
    if (!groups.has(field.group)) groups.set(field.group, []);
    groups.get(field.group).push(field);
  }
  const form = $("#config-form");
  form.innerHTML = "";
  for (const [group, fields] of groups) {
    const section = document.createElement("div");
    section.className = "cfg-group";
    section.innerHTML = `<h3>${esc(group)}</h3>`;
    const grid = document.createElement("div");
    grid.className = "grid";
    for (const field of fields) {
      const wrap = document.createElement("label");
      const value = data.values[field.key] || {};
      const isSecret = data.secrets.includes(field.key);
      const current = isSecret ? "" : (value.value || "");
      const placeholder = isSecret
        ? (value.set ? `set ${value.hint ? "(…" + value.hint + ")" : ""} — blank keeps it` : "not set")
        : (field.placeholder || "");
      let control;
      if (field.kind === "models") {
        control = `<textarea data-env="${esc(field.key)}" rows="2" placeholder="${esc(placeholder)}">${esc(current)}</textarea>`;
      } else {
        control = `<input data-env="${esc(field.key)}" type="${field.kind === "secret" ? "password" : (field.kind === "number" ? "number" : "text")}" value="${esc(current)}" placeholder="${esc(placeholder)}">`;
      }
      wrap.innerHTML = `<span>${esc(field.label)}</span>${control}` +
        (field.help ? `<div class="cfg-help">${esc(field.help)}</div>` : "");
      grid.appendChild(wrap);
    }
    section.appendChild(grid);
    form.appendChild(section);
  }
  renderChips();
  const lineup = ($("#config-form [data-env='CTF_MODELS']") || {}).value || "";
  if (lineup) $("#e-models").value = lineup;
}

function renderChips() {
  if (!cfg) return;
  const current = new Set(($("#e-models").value || "").split(",").map(x => x.trim()).filter(Boolean));
  $("#model-chips").innerHTML = cfg.models.map(model => {
    const on = current.has(model.spec);
    const cls = !model.solver ? "chip off" : (on ? "chip on" : "chip");
    const title = `${model.note}${model.available ? "" : " | requires " + model.requires}`;
    return `<span class="${cls}" data-spec="${esc(model.spec)}" title="${esc(title)}">${esc(model.label)}</span>`;
  }).join("");
  document.querySelectorAll("#model-chips .chip").forEach(chip => {
    chip.onclick = () => {
      if (!cfg.models.find(m => m.spec === chip.dataset.spec && m.solver)) {
        setNote("#e-note", "that model is not an engine solver", "warn");
        return;
      }
      const box = $("#e-models");
      const items = box.value.split(",").map(x => x.trim()).filter(Boolean);
      const at = items.indexOf(chip.dataset.spec);
      if (at >= 0) items.splice(at, 1); else items.push(chip.dataset.spec);
      box.value = items.join(",");
      renderChips();
    };
  });
}

async function loadConfig() {
  const data = await api("/api/config");
  renderConfig(data);
  setNote("#cfg-note", "loaded", "ok");
}

async function saveConfig() {
  const updates = {};
  document.querySelectorAll("#config-form [data-env]").forEach(input => {
    const key = input.dataset.env;
    const value = input.value.trim();
    if (cfg.secrets.includes(key) && value === "") return;
    updates[key] = value;
  });
  const data = await api("/api/config", {method: "POST", json: {updates}});
  renderConfig(data);
  setNote("#cfg-note", "saved .env", "ok");
}

function renderChallenges() {
  $("#ch-list").innerHTML = challenges.length ? challenges.map(ch => {
    const flags = Object.keys(ch.adversarial || {}).join(", ");
    const files = ch.files.map(f => `${f.name} (${f.size}b)`).join(", ");
    return `<tr><td class="name" data-edit="${esc(ch.slug)}" title="${esc(ch.description)}">${esc(ch.name)}</td>` +
      `<td class="dim">${esc(ch.category)}</td><td>${esc(ch.value)}</td>` +
      `<td class="mini" title="${esc(files)}">${ch.file_count}</td>` +
      `<td class="flag">${esc(flags)}</td>` +
      `<td><button class="secondary" style="padding:3px 7px" data-edit="${esc(ch.slug)}">edit</button></td></tr>`;
  }).join("") : `<tr><td colspan="6" class="dim">No local challenges yet</td></tr>`;
  document.querySelectorAll("[data-edit]").forEach(node => {
    node.onclick = () => editChallenge(node.dataset.edit);
  });
  const select = $("#e-challenge");
  select.innerHTML = challenges.map(ch => `<option value="${esc(ch.slug)}">${esc(ch.name)}</option>`).join("");
}

async function loadChallenges() {
  const data = await api("/api/challenges");
  challenges = data.challenges || [];
  renderChallenges();
  setNote("#ch-note", `${challenges.length} local`, "ok");
}

function renderFlags(data) {
  const flags = data.flags || [];
  $("#flag-list").innerHTML = flags.length ? flags.map(flag =>
    `<tr><td class="name">${esc(flag.challenge)}</td>` +
    `<td class="flag">${esc(flag.flag)}</td>` +
    `<td class="dim">${esc(flag.model)}</td>` +
    `<td class="dim">${esc(flag.confirmed_at_iso || "")}</td>` +
    `<td class="mini">${esc(flag.trace || "")}</td></tr>`
  ).join("") : `<tr><td colspan="5" class="dim">No confirmed flags yet</td></tr>`;
  setNote("#flag-note", `${flags.length} stored`, flags.length ? "ok" : "dim");
}

async function loadFlags() {
  const data = await api("/api/flags");
  renderFlags(data);
}

async function buildWalkthroughs() {
  setNote("#flag-note", "building...", "warn");
  const data = await api("/api/walkthroughs", {method: "POST", json: {force: true}});
  setNote(
    "#flag-note",
    `${(data.files || []).length} walkthrough(s) saved` + (data.ok ? "" : " (partial)"),
    data.ok ? "ok" : "warn"
  );
}

function clearForm() {
  for (const id of ["ch-original","ch-slug","ch-name","ch-category","ch-value","ch-tags","ch-conn","ch-desc","ch-hints","ch-truth"]) {
    $("#" + id).value = "";
  }
  $("#ch-value").value = "0";
  $("#ch-files").value = "";
  $("#ch-replace").checked = false;
}

function fillForm(ch) {
  $("#ch-original").value = ch.slug;
  $("#ch-slug").value = ch.slug;
  $("#ch-name").value = ch.name || "";
  $("#ch-category").value = ch.category || "";
  $("#ch-value").value = ch.value ?? 0;
  $("#ch-tags").value = (ch.tags || []).join(", ");
  $("#ch-conn").value = ch.connection_info || "";
  $("#ch-desc").value = ch.description || "";
  $("#ch-hints").value = (ch.hints || []).map(h => {
    const cost = h.cost ?? 0;
    return h.title ? `${cost}|${h.title}|${h.content || ""}` : `${cost}|${h.content || ""}`;
  }).join("\n");
  $("#ch-truth").value = ch.ground_truth || "";
  $("#ch-files").value = "";
  $("#ch-replace").checked = false;
  setNote("#ch-note", `editing ${ch.slug}`, "warn");
}

function editChallenge(slug) {
  const ch = challenges.find(item => item.slug === slug);
  if (ch) fillForm(ch);
  window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"});
}

async function saveChallenge() {
  const form = new FormData();
  for (const [id, key] of [["ch-original","original_slug"],["ch-slug","slug"],["ch-name","name"],
    ["ch-category","category"],["ch-value","value"],["ch-tags","tags"],["ch-conn","connection_info"],
    ["ch-desc","description"],["ch-hints","hints"],["ch-truth","ground_truth"]]) {
    form.append(key, $("#" + id).value);
  }
  if ($("#ch-replace").checked) form.append("replace_files", "1");
  for (const file of $("#ch-files").files) form.append("files", file, file.name);
  const data = await api("/api/challenges", {method: "POST", body: form});
  await loadChallenges();
  fillForm(data.challenge);
  setNote("#ch-note", "saved", "ok");
}

async function deleteChallenge() {
  const slug = $("#ch-original").value || $("#ch-slug").value;
  if (!slug) { setNote("#ch-note", "select a challenge first", "warn"); return; }
  if (!confirm(`Delete challenge ${slug} and its distfiles?`)) return;
  await api("/api/challenges?slug=" + encodeURIComponent(slug), {method: "DELETE"});
  clearForm();
  await loadChallenges();
  setNote("#ch-note", "deleted", "ok");
}

function renderEngine(data) {
  const running = data.running;
  $("#engine-status").innerHTML =
    `<span class="${running ? "ok" : "dim"}">${running ? "running" : "stopped"}</span>` +
    `<span>pid <b>${running ? data.pid : "-"}</b></span>` +
    `<span>elapsed <b>${running ? data.elapsed_s + "s" : "-"}</b></span>` +
    `<span>last exit <b>${data.returncode ?? "-"}</b></span>`;
  $("#e-start").disabled = running;
  $("#e-stop").disabled = !running;
  const log = $("#engine-log");
  const atBottom = log.scrollHeight - log.scrollTop - log.clientHeight < 40;
  log.textContent = (data.log_tail || []).join("\n");
  if (atBottom) log.scrollTop = log.scrollHeight;
  if (data.args && !running) $("#e-note").textContent = "";
}

async function loadEngine() {
  const data = await api("/api/engine");
  renderEngine(data);
}

async function startEngine() {
  const models = $("#e-models").value.split(",").map(x => x.trim()).filter(Boolean);
  const options = {
    mode: $("#e-mode").value,
    challenge: $("#e-challenge").value,
    coordinator: $("#e-coordinator").value,
    coordinator_model: $("#e-coord-model").value.trim(),
    max_challenges: Number($("#e-max").value || 1),
    msg_port: Number($("#e-port").value || 9400),
    no_submit: $("#e-nosubmit").checked,
    models,
  };
  setNote("#e-note", "starting...", "warn");
  const data = await api("/api/engine/start", {method: "POST", json: options});
  renderEngine(data);
  setNote("#e-note", "started", "ok");
}

async function stopEngine() {
  setNote("#e-note", "stopping...", "warn");
  const data = await api("/api/engine/stop", {method: "POST", json: {}});
  renderEngine(data);
  setNote("#e-note", "stopped", "ok");
}

const click = (selector, fn) => { $(selector).onclick = guard(fn); };
click("#cfg-save", saveConfig);
click("#cfg-reload", async () => { await loadConfig(); setNote("#cfg-note", "reloaded", "ok"); });
click("#ch-new", async () => { clearForm(); setNote("#ch-note", "new challenge", "warn"); });
click("#ch-refresh", loadChallenges);
click("#ch-save", saveChallenge);
click("#ch-delete", deleteChallenge);
click("#flag-refresh", async () => { await loadFlags(); setNote("#flag-note", "refreshed", "ok"); });
click("#wt-build", buildWalkthroughs);
click("#e-start", startEngine);
click("#e-stop", stopEngine);
$("#e-models").oninput = renderChips;
$("#ch-form").onsubmit = event => { event.preventDefault(); saveChallenge().catch(err => setNote("#ch-note", String(err.message || err), "bad")); };
$("#clock").textContent = new Date().toLocaleTimeString();

async function boot() {
  try {
    await Promise.all([loadConfig(), loadChallenges(), loadEngine(), loadFlags()]);
    const options = {
      mode: $("#e-mode").value,
      challenge: $("#e-challenge").value,
      coordinator: $("#e-coordinator").value,
      coordinator_model: $("#e-coord-model").value,
      max_challenges: $("#e-max").value,
      msg_port: $("#e-port").value,
    };
    $("#footer").textContent = "control panel ready | " + Object.keys(options).length + " engine options";
  } catch (err) {
    setNote("#footer", String(err.message || err), "bad");
  }
}

boot();
setInterval(() => { loadEngine().catch(() => {}); }, 4000);
setInterval(() => { loadFlags().catch(() => {}); }, 10000);
setInterval(() => { $("#clock").textContent = new Date().toLocaleTimeString(); }, 1000);
</script>
</body>
</html>
"""
