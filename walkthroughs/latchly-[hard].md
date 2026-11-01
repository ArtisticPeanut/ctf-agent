# Latchly [HARD]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 400
- **Solves**: 9
- **Flag**: `FLAG{d3duc3-th3-c0d3-b34t-th3-cl0ck}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.01 (winner $0.01)
- **Wall time**: 3m35s
- **Traces**: 2

## Description

~~~
Latchly's smart-lock diagnostics portal runs a **Crack the Code** self-test.
Each round shows a few clue rows — a three-digit guess and how close it is
(how many digits are correct, and whether they are in the right place). Use the
clues to work out the secret PIN and enter it before the clock runs out.
- One guess per round.
- A wrong guess or a timeout sends you back to round 1 with a fresh code.
- Clear every round in a single clean run and the vault opens.
Flag format: `FLAG{...}`
Connection: http://chal2.hackathon.ke:8025
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 28 | $0.01 | 3m35s | `trace-Latchly_[HARD]-deepseek-flash-20261029-201915.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 6s | `trace-Latchly_[HARD]-claude-opus-4-6-20261029-201915.jsonl` |

_Window: 2026-10-29T20:19:18 to 2026-10-29T20:22:53_

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
  "command": "curl -s -i http://chal2.hackathon.ke:8025/ ; echo; curl -s http://chal2.hackathon.ke:8025/robots.txt",
  "timeout_seconds": 60
}
~~~

~~~
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 17:19:26 GMT
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Content-Length: 5778

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Latchly</title>
<style>
  :root{--bg:#0d1117;--panel:#161b22;--line:#273040;--ink:#e6edf3;--mut:#8b98a9;
        --accent:#f0b429;--accent2:#d99a1c;--good:#3fb950;--bad:#f85149;--tile:#1f2733}
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(1200px 600px at 50% -10%,#15202b,#0d1117);
       color:var(--ink);font:15px/1.5 "Segoe UI",system-ui,sans-serif;min-height:100vh}
  .wrap{max-width:760px;margin:0 auto;padding:28px 18px 60px}
  header{display:flex;align-items:center;gap:12px;margin-bottom:6px}
  .lock{width:34px;height:34px;border:3px solid var(--accent);border-radius:7px;position:relative;margin-top:10px}
  .lock:before{content:"";position:absolute;top:-13px;left:50%;transform:translateX(-50%);
       width:18px;height:16px;border:3px solid var(--accent);border-bottom:0;border-radius:9px 9px 0 0}
  h1{font-size:26px;letter-spacing:.5px;margin:0}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "cd /workspace 2>/dev/null || cd /tmp; curl -s -c c.txt http://chal2.hackathon.ke:8025/api/puzzle; echo; curl -s -b c.txt -i http://chal2.hackathon.ke:8025/api/puzzle",
  "timeout_seconds": 60
}
~~~

~~~
{"clues":[{"digits":[5,3,7],"verdict":"One Number is correct and well placed"},{"digits":[9,8,4],"verdict":"One Number is correct and well placed"},{"digits":[8,7,6],"verdict":"One Number is correct and well placed"}],"code_length":3,"round":1,"seconds_left":8.0,"time_limit":8,"total_rounds":20}

HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 17:19:29 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 298

{"clues":[{"digits":[5,3,7],"verdict":"One Number is correct and well placed"},{"digits":[9,8,4],"verdict":"One Number is correct and well placed"},{"digits":[8,7,6],"verdict":"One Number is correct and well placed"}],"code_length":3,"round":1,"seconds_left":7.62,"time_limit":8,"total_rounds":20}
~~~

### Step 4: `bash`
~~~
{
  "command": "cd /tmp; for h in /api/reset /api/guess /api/puzzle/0 /api/state /api/debug; do echo \"== $h\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://chal2.hackathon.ke:8025$h; done; curl -s -X POST http://chal2.hackathon.ke:8025/api/reset; echo; curl -s -X OPTIONS -i http://chal2.hackathon.ke:8025/api/guess",
  "timeout_seconds": 60
}
~~~

~~~
== /api/reset
405
== /api/guess
405
== /api/puzzle/0
404
== /api/state
404
== /api/debug
200
{"clues":[{"digits":[1,7,4],"verdict":"Nothing is correct"},{"digits":[1,6,9],"verdict":"One Number is correct and well placed"},{"digits":[1,9,0],"verdict":"One Number is correct but wrongly placed"},{"digits":[2,6,7],"verdict":"Two Numbers are correct: 1 well placed and 1 wrongly placed"}],"code_length":3,"round":1,"seconds_left":8.0,"time_limit":8,"total_rounds":20}

HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 17:19:34 GMT
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Allow: OPTIONS, POST
Content-Length: 0
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /tmp; curl -s http://chal2.hackathon.ke:8025/api/debug; echo; for w in admin source flag secret code answer solution pin reset status round debug/1 flag.txt app.py source .git/HEAD; do echo \"== $w\"; curl -s -o /dev/null -w \"%{http_code} \" http://chal2.hackathon.ke:8025/$w; done; echo",
  "timeout_seconds": 60
}
~~~

~~~
{"build":"2.3.1","factory_master_note":"FAKE-FLAG{Try-Harder-Mate}","hint":"codes rotate every round; the vault opens after a clean run","service":"latchly"}

== admin
404 == source
404 == flag
404 == secret
404 == code
404 == answer
404 == solution
404 == pin
404 == reset
404 == status
404 == round
404 == debug/1
404 == flag.txt
404 == app.py
404 == source
404 == .git/HEAD
404
~~~

### Step 6: `bash`
~~~
{
  "command": "cd /tmp; cat > probe.sh <<'EOF'\nstr=\"$1\"; hdr=\"$2\"\ncurl -s -X POST http://chal2.hackathon.ke:8025/api/guess -H 'Content-Type: application/json' -H \"$hdr\" -d \"$str\"\necho\nEOF\nfor s in '{\"pin\":null}' '{\"pin\":\"\"}' '{\"pin\":true}' '{\"pin\":false}' '{\"pin\":[]}' '{\"pin\":{}}' '{\"pin\":\"000\"}' 'null' '[]'; do echo \"== $s\"; bash probe.sh \"$s\" \"X: y\"; done",
  "timeout_seconds": 60
}
~~~

~~~
== {"pin":null}
{"clues":[{"digits":[0,1,9],"verdict":"One Number is correct but wrongly placed"},{"digits":[0,3,1],"verdict":"One Number is correct but wrongly placed"},{"digits":[3,1,6],"verdict":"Nothing is correct"},{"digits":[5,4,6],"verdict":"One Number is correct and well placed"},{"digits":[7,9,0],"verdict":"One Number is correct but wrongly placed"},{"digits":[7,8,6],"verdict":"Nothing is correct"},{"digits":[2,9,1],"verdict":"One Number is correct but wrongly placed"}],"code_length":3,"ok":false,"reason":"wrong","round":1,"seconds_left":8.0,"solved":false,"time_limit":8,"total_rounds":20}

== {"pin":""}
{"clues":[{"digits":[1,5,6],"verdict":"One Number is correct but wrongly placed"},{"digits":[4,7,5],"verdict":"Three Numbers are correct: 1 well placed and 2 wrongly placed"},{"digits":[7,3,5],"verdict":"Two Numbers are correct but wrongly placed"}],"code_length":3,"ok":false,"reason":"wrong","round":1,"seconds_left":8.0,"solved":false,"time_limit":8,"total_rounds":20}

== {"pin":true}
... [2000 chars total]
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /tmp; cat > test.sh <<'EOF'\ns=\"$1\"\na=$(curl -s -X POST http://chal2.hackathon.ke:8025/api/guess -H 'Content-Type: application/json' -d \"$s\")\nb=$(curl -s http://chal2.hackathon.ke:8025/api/puzzle)\nc=$(curl -s -X POST http://chal2.hackathon.ke:8025/api/reset)\necho \"GUESS($s): $(echo $a | head -c 120)\"\necho \"PUZZLE: $(echo $b | head -c 120)\"\necho \"RESET: $(echo $c | head -c 120)\"\nEOF\nbash test.sh '{\"pin\":\"123\",\"round\":2}'\nbash test.sh '{\"pin\":\"123\",\"password\":\"x\"}'\nbash test.sh '{\"pin\":\"123\",\"session\":{}}'\nbash test.sh '{\"pin\":\"123\",\"code_length\":0}'",
  "timeout_seconds": 60
}
~~~

~~~
GUESS({"pin":"123","round":2}): {"clues":[{"digits":[3,5,9],"verdict":"Two Numbers are correct and well placed"},{"digits":[9,4,7],"verdict":"Nothing is
PUZZLE: {"clues":[{"digits":[2,5,8],"verdict":"One Number is correct but wrongly placed"},{"digits":[3,0,9],"verdict":"Nothing i
RESET: {"clues":[{"digits":[1,8,4],"verdict":"Nothing is correct"},{"digits":[7,3,5],"verdict":"Two Numbers are correct: 1 well
GUESS({"pin":"123","password":"x"}): {"clues":[{"digits":[3,2,4],"verdict":"Nothing is correct"},{"digits":[1,9,3],"verdict":"Two Numbers are correct: 1 well
PUZZLE: {"clues":[{"digits":[0,3,5],"verdict":"Two Numbers are correct but wrongly placed"},{"digits":[3,4,7],"verdict":"One Num
RESET: {"clues":[{"digits":[4,3,1],"verdict":"One Number is correct but wrongly placed"},{"digits":[5,9,8],"verdict":"One Numbe
GUESS({"pin":"123","session":{}}): {"clues":[{"digits":[6,4,8],"verdict":"One Number is correct but wrongly placed"},{"digits":[9,3,0],"verdict":"Two Numbe
PUZZLE: {"clues":[{"digits":[6,0,8],"verdict":"Nothing is correct"},{"digits":[7,1,5],"verdict":"Two Numbers are correct and wel
... [1653 chars total]
~~~

### Step 8: `bash`
~~~
{
  "command": "cd /tmp; cat > t2.sh <<'EOF'\ns=\"$1\"\necho \"== $s\"\ncurl -s -X POST http://chal2.hackathon.ke:8025/api/guess -H 'Content-Type: application/json' -d \"$s\" | python3 -c 'import sys,json;d=json.load(sys.stdin);print({k:v for k,v in d.items() if k!=\"clues\"}, [c[\"verdict\"] for c in d.get(\"clues\",[])])'\nEOF\nbash t2.sh '{\"pin\":\"123\",}'\nbash t2.sh '{\"pin\":\"123\", \"pin\":\"456\"}'\nbash t2.sh '{\\u0070in:\"123\"}'\nbash t2.sh '{\"pin\":\"123\"} '\nbash t2.sh '{\"PIN\":\"123\"}'\nbash t2.sh '{\"pin\":123}'\nbash t2.sh '{\"pin\":\" 123\"}'\nbash t2.sh '\"123\"'\nbash t2.sh '{\"pin\":[\"1\",\"2\",\"3\"]}'",
  "timeout_seconds": 60
}
~~~

~~~
== {"pin":"123",}
{'code_length': 3, 'ok': False, 'reason': 'wrong', 'round': 1, 'seconds_left': 8.0, 'solved': False, 'time_limit': 8, 'total_rounds': 20} ['Nothing is correct', 'Two Numbers are correct and well placed', 'One Number is correct and well placed', 'One Number is correct but wrongly placed', 'One Number is correct but wrongly placed', 'Nothing is correct']
== {"pin":"123", "pin":"456"}
{'code_length': 3, 'ok': False, 'reason': 'wrong', 'round': 1, 'seconds_left': 8.0, 'solved': False, 'time_limit': 8, 'total_rounds': 20} ['One Number is correct but wrongly placed', 'One Number is correct and well placed', 'Two Numbers are correct: 1 well placed and 1 wrongly placed', 'One Number is correct but wrongly placed', 'One Number is correct but wrongly placed']
== {\u0070in:"123"}
{'code_length': 3, 'ok': False, 'reason': 'wrong', 'round': 1, 'seconds_left': 8.0, 'solved': False, 'time_limit': 8, 'total_rounds': 20} ['Two Numbers are correct: 1 well placed and 1 wrongly placed', 'One Number is correct but wrongly placed', 'Nothing is correct', 'Two Numbers are correct: 1 well placed and 1 wrongly placed', 'Nothing is correct']
== {"pin":"123"} 
... [2000 chars total]
~~~

### Step 9: `bash`
~~~
{
  "command": "cd /tmp; for s in '{\"pin\":\"123\",\"flag\":true}' '{\"pin\":\"123\",\"solved\":true}' '{\"pin\":\"123\",\"__proto__\":{\"solved\":true}}' '{\"pin\":\"123\",\"debug\":1}' '{\"pin\":\"123\",\"round\":20}'; do echo \"== $s\"; curl -s -X POST http://chal2.hackathon.ke:8025/api/guess -H 'Content-Type: application/json' -d \"$s\" | head -c 300; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== {"pin":"123","flag":true}
{"clues":[{"digits":[2,8,6],"verdict":"Two Numbers are correct: 1 well placed and 1 wrongly placed"},{"digits":[0,1,8],"verdict":"Nothing is correct"},{"digits":[8,6,4],"verdict":"One Number is correct and well placed"},{"digits":[8,5,4],"verdict":"One Number is correct but wrongly placed"}],"code_l
== {"pin":"123","solved":true}
{"clues":[{"digits":[0,4,1],"verdict":"One Number is correct but wrongly placed"},{"digits":[0,7,9],"verdict":"One Number is correct but wrongly placed"},{"digits":[8,7,0],"verdict":"One Number is correct but wrongly placed"},{"digits":[5,6,2],"verdict":"Two Numbers are correct but wrongly placed"},
== {"pin":"123","__proto__":{"solved":true}}
{"clues":[{"digits":[7,3,9],"verdict":"Nothing is correct"},{"digits":[6,5,1],"verdict":"One Number is correct and well placed"},{"digits":[7,6,5],"verdict":"One Number is correct but wrongly placed"},{"digits":[8,2,7],"verdict":"Two Numbers are correct but wrongly placed"},{"digits":[9,1,2],"verdic
== {"pin":"123","debug":1}
... [1664 chars total]
~~~

### Step 10: `bash`
~~~
{
  "command": "cd /tmp; (timeout 15 curl -s -N -H 'Accept: text/event-stream' http://chal2.hackathon.ke:8025/api/puzzle; echo \"---done\") ; for h in api api/v1 api/v2 admin health metrics config env internal test dev upload export log logs ws socket; do printf \"%s \" $h; curl -s -o /dev/null -w \"%{http_code}\\n\" http://chal2.hackathon.ke:8025/$h; done",
  "timeout_seconds": 60
}
~~~

~~~
{"clues":[{"digits":[7,0,5],"verdict":"One Number is correct but wrongly placed"},{"digits":[7,2,6],"verdict":"Two Numbers are correct but wrongly placed"},{"digits":[9,1,5],"verdict":"One Number is correct but wrongly placed"},{"digits":[1,5,0],"verdict":"One Number is correct but wrongly placed"},{"digits":[6,4,3],"verdict":"One Number is correct and well placed"}],"code_length":3,"round":1,"seconds_left":8.0,"time_limit":8,"total_rounds":20}
---done
api 404
api/v1 404
api/v2 404
admin 404
health 200
metrics 404
config 404
env 404
internal 404
test 404
dev 404
upload 404
export 404
log 404
logs 404
ws 404
socket 404
~~~

### Step 11: `bash`
~~~
{
  "command": "cd /tmp; curl -s http://chal2.hackathon.ke:8025/health; echo; curl -s -i http://chal2.hackathon.ke:8025/api/reset -X POST; echo; curl -s -i -X POST http://chal2.hackathon.ke:8025/api/guess -H 'Content-Type: text/plain' -d '{\"pin\":\"123\"}' | head -20",
  "timeout_seconds": 60
}
~~~

~~~
ok
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 17:20:22 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 379
Set-Cookie: sid=6ae23de3f093b399ce87c4bf; Path=/; SameSite=Lax

{"clues":[{"digits":[2,7,1],"verdict":"Nothing is correct"},{"digits":[3,9,8],"verdict":"Two Numbers are correct but wrongly placed"},{"digits":[1,9,3],"verdict":"One Number is correct but wrongly placed"},{"digits":[9,8,4],"verdict":"Three Numbers are correct: 1 well placed and 2 wrongly placed"}],"code_length":3,"round":1,"seconds_left":8.0,"time_limit":8,"total_rounds":20}

HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 17:20:23 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 539
Set-Cookie: sid=3ae962b3ab41f94356bb02ff; Path=/; SameSite=Lax

... [1351 chars total]
~~~

### Step 12: `bash`
~~~
{
  "command": "cd /tmp; rm -f cj; curl -s -c cj -b cj http://chal2.hackathon.ke:8025/api/puzzle >/dev/null; cat cj; echo \"--- no cookie\"; curl -s http://chal2.hackathon.ke:8025/api/puzzle | head -c 150; echo; echo \"--- with cookie\"; curl -s -b cj http://chal2.hackathon.ke:8025/api/puzzle | head -c 150; echo; echo \"--- forged\"; curl -s -b 'sid=6ae23de3f093b399ce87c4bf' http://chal2.hackathon.ke:8025/api/puzzle | head -c 150",
  "timeout_seconds": 60
}
~~~

~~~
# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

chal2.hackathon.ke	FALSE	/	FALSE	0	sid	7d548b833856ee5d0de8b542
--- no cookie
{"clues":[{"digits":[8,4,0],"verdict":"One Number is correct and well placed"},{"digits":[6,3,0],"verdict":"Nothing is correct"},{"digits":[6,1,7],"ve
--- with cookie
{"clues":[{"digits":[9,8,0],"verdict":"Nothing is correct"},{"digits":[4,5,0],"verdict":"Nothing is correct"},{"digits":[6,4,5],"verdict":"Nothing is 
--- forged
{"clues":[{"digits":[2,7,1],"verdict":"Nothing is correct"},{"digits":[3,9,8],"verdict":"Two Numbers are correct but wrongly placed"},{"digits":[1,9,3
~~~

### Step 13: `bash`
~~~
{
  "command": "cd /tmp; s1=$(curl -s http://chal2.hackathon.ke:8025/api/puzzle); sleep 1; s2=$(curl -s http://chal2.hackathon.ke:8025/api/puzzle); echo \"$s1\"; echo \"$s2\"",
  "timeout_seconds": 60
}
~~~

~~~
{"clues":[{"digits":[8,4,3],"verdict":"One Number is correct and well placed"},{"digits":[8,3,1],"verdict":"Two Numbers are correct: 1 well placed and 1 wrongly placed"},{"digits":[1,3,9],"verdict":"One Number is correct but wrongly placed"},{"digits":[0,9,2],"verdict":"One Number is correct and well placed"},{"digits":[6,8,0],"verdict":"One Number is correct but wrongly placed"},{"digits":[0,6,1],"verdict":"One Number is correct but wrongly placed"}],"code_length":3,"round":1,"seconds_left":8.0,"time_limit":8,"total_rounds":20}
{"clues":[{"digits":[1,9,3],"verdict":"One Number is correct but wrongly placed"},{"digits":[5,2,7],"verdict":"One Number is correct but wrongly placed"},{"digits":[5,4,3],"verdict":"Nothing is correct"},{"digits":[9,2,8],"verdict":"Two Numbers are correct: 1 well placed and 1 wrongly placed"},{"digits":[8,2,0],"verdict":"One Number is correct but wrongly placed"},{"digits":[3,1,0],"verdict":"Nothing is correct"},{"digits":[6,0,7],"verdict":"One Number is correct but wrongly placed"}],"code_length":3,"round":1,"seconds_left":8.0,"time_limit":8,"total_rounds":20}
~~~

### Step 14: `bash`
~~~
{
  "command": "cd /tmp; for leak in '{\"pin\":\"{{7*7}}\"}' '{\"pin\":\"${7*7}\"}' '{\"pin\":{\"toString\":1}}' '{\"pin\":\"\\u0000\"}' '{\"pin\":1e999}'; do echo \"== $leak\"; curl -s -X POST http://chal2.hackathon.ke:8025/api/guess -H 'Content-Type: application/json' -d \"$leak\" | head -c 400; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== {"pin":"{{7*7}}"}
{"clues":[{"digits":[0,6,7],"verdict":"One Number is correct and well placed"},{"digits":[5,3,9],"verdict":"One Number is correct and well placed"},{"digits":[9,8,6],"verdict":"Two Numbers are correct but wrongly placed"},{"digits":[4,0,6],"verdict":"One Number is correct but wrongly placed"},{"digits":[2,9,3],"verdict":"Nothing is correct"},{"digits":[2,6,7],"verdict":"One Number is correct and w
== {"pin":"${7*7}"}
{"clues":[{"digits":[4,6,5],"verdict":"Two Numbers are correct: 1 well placed and 1 wrongly placed"},{"digits":[4,3,0],"verdict":"Nothing is correct"},{"digits":[1,7,9],"verdict":"Nothing is correct"},{"digits":[6,9,8],"verdict":"One Number is correct and well placed"},{"digits":[8,9,6],"verdict":"One Number is correct but wrongly placed"}],"code_length":3,"ok":false,"reason":"wrong","round":1,"se
== {"pin":{"toString":1}}
... [2000 chars total]
~~~

### Step 15: `bash`
~~~
{
  "command": "cd /tmp; for p in '/api/puzzle?pin=123' '/api/puzzle?round=20' '/api/puzzle?code=000' '/api/guess/1' '/api/puzzle/debug'; do echo \"== $p\"; curl -s \"http://chal2.hackathon.ke:8025$p\" | head -c 200; echo; done; for p in flag.txt flag app.py source main.py server.py run.py requirements.txt .env Dockerfile; do printf \"%s \" $p; curl -s -o /dev/null -w \"%{http_code}\\n\" \"http://chal2.hackathon.ke:8025/$p\"; done",
  "timeout_seconds": 60
}
~~~

~~~
== /api/puzzle?pin=123
{"clues":[{"digits":[3,0,8],"verdict":"One Number is correct but wrongly placed"},{"digits":[3,5,2],"verdict":"Nothing is correct"},{"digits":[7,4,5],"verdict":"Two Numbers are correct: 1 well placed 
== /api/puzzle?round=20
{"clues":[{"digits":[5,7,4],"verdict":"Nothing is correct"},{"digits":[0,9,2],"verdict":"One Number is correct and well placed"},{"digits":[9,3,8],"verdict":"Three Numbers are correct but wrongly plac
== /api/puzzle?code=000
{"clues":[{"digits":[5,3,7],"verdict":"Nothing is correct"},{"digits":[6,4,2],"verdict":"Two Numbers are correct but wrongly placed"},{"digits":[1,6,0],"verdict":"One Number is correct and well placed
== /api/guess/1
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try agai
== /api/puzzle/debug
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try agai
flag.txt 404
flag 404
app.py 404
source 404
main.py 404
server.py 404
run.py 404
... [1238 chars total]
~~~

### Step 16: `bash`
~~~
{
  "command": "cd /tmp; time curl -s -b cj http://chal2.hackathon.ke:8025/api/puzzle | head -c 100; echo; time curl -s -b cj http://chal2.hackathon.ke:8025/api/puzzle | head -c 100; echo; curl -s -b cj -i http://chal2.hackathon.ke:8025/api/puzzle | grep -i set-cookie",
  "timeout_seconds": 60
}
~~~

~~~
{"clues":[{"digits":[9,8,0],"verdict":"Nothing is correct"},{"digits":[4,5,0],"verdict":"Nothing is 
{"clues":[{"digits":[9,8,0],"verdict":"Nothing is correct"},{"digits":[4,5,0],"verdict":"Nothing is 

[stderr]

real	0m0.340s
user	0m0.001s
sys	0m0.009s

real	0m0.440s
user	0m0.001s
sys	0m0.010s

[exit 1]
~~~

### Step 17: `bash`
~~~
{
  "command": "cd /tmp; cat > client.py <<'EOF'\nimport requests, json, time\nS=requests.Session()\nB='http://chal2.hackathon.ke:8025'\nr=S.get(B+'/api/puzzle').json(); print(r['round'], r['seconds_left'], len(r['clues']))\npayload={\"clues\":r['clues'],\"code_length\":r['code_length'],\"round\":r['total_rounds'],\"seconds_left\":999,\"time_limit\":999,\"total_rounds\":r['total_rounds'],\"pin\":\"000\",\"ok\":False,\"solved\":True,\"reason\":\"wrong\",\"flag\":\"FLAG{fake}\"}\nt=time.time()\nr2=S.post(B+'/api/guess',json=payload).json()\nprint(time.time()-t, r2.get('round'), r2.get('ok'), r2.get('solved'), len(r2.get('clues',[])), list(r2.keys()))\nEOF\npython3 client.py",
  "timeout_seconds": 60
}
~~~

~~~
1 8.0 6
0.19443225860595703 1 False False 6 ['clues', 'code_length', 'ok', 'reason', 'round', 'seconds_left', 'solved', 'time_limit', 'total_rounds']
~~~

### Step 18: `bash`
~~~
{
  "command": "cd /tmp; python3 - <<'EOF'\nimport requests,time\nS=requests.Session(); B='http://chal2.hackathon.ke:8025'\nfor i in range(5):\n    t=time.time(); r=S.get(B+'/api/puzzle').json(); print(r['round'], r['seconds_left'], round(time.time()-t,3))\n    time.sleep(1)\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
1 8.0 0.378
1 6.83 0.161
1 5.66 0.167
1 4.5 0.159
1 3.34 0.166
~~~

### Step 19: `bash`
~~~
{
  "command": "cd /tmp; python3 - <<'EOF'\nimport requests\nB='http://chal2.hackathon.ke:8025'\nfor n in range(3):\n    S=requests.Session(); S.get(B+'/api/puzzle')\n    for i in range(3):\n        r=S.post(B+'/api/guess',json={\"pin\":\"000\"}).json()\n        print(r['round'], r['seconds_left'], r['reason'])\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
1 8.0 wrong
1 8.0 wrong
1 8.0 wrong
1 8.0 wrong
1 8.0 wrong
1 8.0 wrong
1 8.0 wrong
1 8.0 wrong
1 8.0 wrong
~~~

### Step 20: `bash`
~~~
{
... [1513 chars total]
~~~

~~~
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 26, in <module>
  File "<stdin>", line 6, in parse
IndexError: list index out of range

[exit 1]
~~~

### Step 21: `bash`
~~~
{
... [1290 chars total]
~~~

~~~
{'clues': [{'digits': [4, 7, 5], 'verdict': 'One Number is correct and well placed'}, {'digits': [3, 1, 8], 'verdict': 'Nothing is correct'}, {'digits': [3, 2, 5], 'verdict': 'Two Numbers are correct: 1 well placed and 1 wrongly placed'}, {'digits': [0, 1, 6], 'verdict': 'Nothing is correct'}, {'digits': [2, 6, 9], 'verdict': 'Two Numbers are correct: 1 well placed and 1 wrongly placed'}], 'code_length': 3, 'round': 1, 'seconds_left': 8.0, 'time_limit': 8, 'total_rounds': 20}
round 1 cands 0 []
ambiguous
~~~

### Step 22: `bash`
~~~
{
  "command": "cd /tmp; python3 - <<'EOF'\nimport requests,re,itertools\nB='http://chal2.hackathon.ke:8025'\nS=requests.Session()\ndef parse(v):\n    d=re.findall(r'\\d',v)\n    if len(d)<2: return 0,0\n    return int(d[0]),int(d[1])\ndef score(guess,code):\n    well=sum(1 for a,b in zip(guess,code) if a==b)\n    common=sum(min(guess.count(d),code.count(d)) for d in set(guess))\n    return well,common-well\nfor it in range(5):\n    r=S.get(B+'/api/puzzle').json()\n    clues=[{'digits':c['digits'],'w':parse(c['verdict'])[0],'wrong':parse(c['verdict'])[1]} for c in r['clues']]\n    best=[]\n    for code in itertools.product(range(10),repeat=3):\n        err=sum(abs(score(code,c['digits'])[0]-c['w'])+abs(score(code,c['digits'])[1]-c['wrong']) for c in clues)\n        best.append((err,code))\n    best.sort()\n    print(best[:6])\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
[(1, (0, 0, 2)), (1, (0, 2, 0)), (1, (0, 2, 1)), (1, (0, 2, 2)), (1, (0, 7, 2)), (1, (1, 2, 1))]
[(1, (0, 0, 2)), (1, (0, 2, 0)), (1, (0, 2, 1)), (1, (0, 2, 2)), (1, (0, 7, 2)), (1, (1, 2, 1))]
[(1, (0, 0, 2)), (1, (0, 2, 0)), (1, (0, 2, 1)), (1, (0, 2, 2)), (1, (0, 7, 2)), (1, (1, 2, 1))]
[(1, (0, 0, 2)), (1, (0, 2, 0)), (1, (0, 2, 1)), (1, (0, 2, 2)), (1, (0, 7, 2)), (1, (1, 2, 1))]
[(1, (0, 0, 2)), (1, (0, 2, 0)), (1, (0, 2, 1)), (1, (0, 2, 2)), (1, (0, 7, 2)), (1, (1, 2, 1))]
~~~

### Step 23: `bash`
~~~
{
  "command": "cd /tmp; python3 - <<'EOF'\nimport requests,json\nB='http://chal2.hackathon.ke:8025'\nS=requests.Session()\nr=S.get(B+'/api/puzzle').json()\nprint(json.dumps(r['clues']))\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
[{"digits": [7, 2, 0], "verdict": "Nothing is correct"}, {"digits": [2, 5, 3], "verdict": "One Number is correct but wrongly placed"}, {"digits": [7, 8, 5], "verdict": "Nothing is correct"}, {"digits": [4, 6, 8], "verdict": "Nothing is correct"}, {"digits": [6, 9, 8], "verdict": "One Number is correct and well placed"}, {"digits": [9, 4, 7], "verdict": "One Number is correct but wrongly placed"}]
~~~

### Step 24: `bash`
~~~
{
... [1729 chars total]
~~~

~~~
[{"digits": [8, 3, 7], "verdict": "One Number is correct but wrongly placed"}, {"digits": [2, 0, 8], "verdict": "Two Numbers are correct: 1 well placed and 1 wrongly placed"}, {"digits": [9, 4, 6], "verdict": "Nothing is correct"}, {"digits": [6, 1, 4], "verdict": "One Number is correct but wrongly placed"}, {"digits": [6, 3, 5], "verdict": "Nothing is correct"}, {"digits": [4, 7, 1], "verdict": "One Number is correct but wrongly placed"}]
1 [(1, 2, 8)]
~~~

### Step 25: `bash`
~~~
{
... [1843 chars total]
~~~

~~~
round 1 cands 1 [(0, 3, 9)]
039 True False None
round 2 cands 1 [(2, 5, 8)]
258 True False None
round 3 cands 1 [(3, 0, 4)]
304 True False None
round 4 cands 1 [(3, 2, 0)]
320 True False None
round 5 cands 1 [(6, 0, 5)]
605 True False None
round 6 cands 1 [(2, 1, 4)]
214 True False None
round 7 cands 1 [(5, 1, 0)]
510 True False None
round 8 cands 1 [(0, 3, 6)]
036 True False None
round 9 cands 1 [(9, 4, 2)]
942 True False None
round 10 cands 1 [(2, 5, 1)]
251 True False None
round 11 cands 1 [(3, 2, 8)]
328 True False None
round 12 cands 2 [(5, 8, 6), (5, 8, 8)]
[{"digits": [7, 4, 3], "verdict": "Nothing is correct"}, {"digits": [8, 0, 3], "verdict": "One Number is correct but wrongly placed"}, {"digits": [3, 8, 2], "verdict": "One Number is correct and well placed"}, {"digits": [3, 4, 1], "verdict": "Nothing is correct"}, {"digits": [3, 4, 5], "verdict": "One Number is correct but wrongly placed"}, {"digits": [0, 7, 9], "verdict": "Nothing is correct"}]
~~~

### Step 26: `bash`
~~~
{
... [1960 chars total]
~~~

~~~
round 3 cands 1
742 True False None
round 4 cands 1
923 True False None
round 5 cands 3
[{"digits": [4, 6, 9], "verdict": "One Number is correct and well placed"}, {"digits": [1, 4, 0], "verdict": "One Number is correct but wrongly placed"}, {"digits": [7, 5, 3], "verdict": "Nothing is correct"}, {"digits": [5, 3, 1], "verdict": "Nothing is correct"}, {"digits": [3, 6, 1], "verdict": "Nothing is correct"}, {"digits": [1, 8, 7], "verdict": "One Number is correct and well placed"}, {"digits": [5, 7, 2], "verdict": "Nothing is correct"}]
089 True False None
round 6 cands 1
283 True False None
round 7 cands 2
[{"digits": [4, 2, 5], "verdict": "One Number is correct but wrongly placed"}, {"digits": [6, 4, 5], "verdict": "Nothing is correct"}, {"digits": [6, 9, 3], "verdict": "Nothing is correct"}, {"digits": [8, 3, 6], "verdict": "One Number is correct but wrongly placed"}, {"digits": [5, 1, 4], "verdict": "Nothing is correct"}, {"digits": [5, 1, 8], "verdict": "One Number is correct and well placed"}, {"digits": [9, 7, 3], "verdict": "Nothing is correct"}]
208 True False None
round 8 cands 1
327 True False None
round 9 cands 1
389 True False None
round 10 cands 1
035 True False None
... [1777 chars total]
~~~

### Step 27: `bash`
~~~
{"command": "cd /tmp; cat > solve4.py <<'EOF'\nimport requests,json,itertools\nB='http://chal2.hackathon.ke:8025'\nS=requests.Session()\ndef parse(code,c):\n    g=c['digits']; v=c['verdict']\n    well=sum(a==b for a,b in zip(g,code))\n    common=sum(min(g.count(d),code.count(d)) for d in set(g))\n    return well,common-well,v\ndef check(code,clues,dedup=True):\n    for c in clues:\n        well,wrong,v=parse(code,c)\n        if v.startswith('Nothing'):\n            if well+wrong!=0: return False\n        elif v.startswith('Three'):\n            if (well,wrong)!=(1,2): return False\n        elif v.startswith('Two Numbers are correct and well placed'):\n            if (well,wrong)!=(2,0): return False\n        elif v.startswith('Two Numbers are correct:'):\n            if (well,wrong)!=(1,1): return False\n        elif v.startswith('Two Numbers are correct but wrongly placed'):\n          
... [2000 chars total]
~~~

~~~
468 True False
round 19 cands 1 [(8, 3, 4)]
834 True False
round 20 cands 1 [(2, 7, 1)]
271 True True
FLAG FLAG{d3duc3-th3-c0d3-b34t-th3-cl0ck}
round 5 cands 0 []
[{"digits": [8, 5, 7], "verdict": "Two Numbers are correct: 1 well placed and 1 wrongly placed"}, {"digits": [8, 4, 5], "verdict": "Three Numbers are correct but wrongly placed"}, {"digits": [4, 7, 5], "verdict": "Two Numbers are correct: 1 well placed and 1 wrongly placed"}]
Traceback (most recent call last):
  File "/tmp/solve4.py", line 38, in <module>
    code=''.join(map(str,cands[0]))
IndexError: list index out of range

[exit 137]
~~~

### Step 28: `submit_flag`
~~~
{
  "flag": "FLAG{d3duc3-th3-c0d3-b34t-th3-cl0ck}"
}
~~~

~~~
DRY RUN — would submit "FLAG{d3duc3-th3-c0d3-b34t-th3-cl0ck}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{d3duc3-th3-c0d3-b34t-th3-cl0ck}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.01 (winner), $0.01 (whole swarm)
- **Wall time**: 3m35s
- **Generated**: 2026-10-30T00:14:55
