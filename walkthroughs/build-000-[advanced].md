# Build 000 [ADVANCED]

<!-- SCRIBE: replace this block with a 5-line 'what the trick was' intro. -->

- **Category**: MISC
- **Points**: 500
- **Solves**: 0
- **Flag**: `FLAG{SC04_3C7FC4063689}`
- **Winner**: `deepseek-flash`
- **Swarm cost**: $0.00 (winner $0.00)
- **Wall time**: 21s
- **Traces**: 2

## Description

~~~
A municipal emergency relay received a software update that passed the build server's green checks.
Soon afterward, the service began accepting unauthorised handovers.
Investigators recovered the uploaded package, a QA reference, several independent source snapshots, competing dependency packages and signed build receipts.
Some packages contain familiar version labels and even a valid-looking CTF flag.
Neither proves that the package was an authorised release.
Your mission is to audit the software supply chain, identify the contaminated build and reconstruct the exact authorised production artefact.
Verify the release evidence against the applicable trust policy. Compare the compromised components against their legitimate counterparts and reproduce the trusted build byte for byte.
Only the correctly authenticated release will unlock the sealed disclosure.
Flag format: FLAG{SC04\_XXXXXXXXXXXX}
This challenge is completely independent. All systems, packages and evidence are fictional. No internet connection or external infrastructure is required.
~~~

## Distfiles

| File | Size | SHA-256 |
|---|---:|---|
| `SC04_Build_000_Participants.zip` | 24590 | `e53dd332d58dd54f1c6bc33d88996c36e7929b8813dd018d19159bffaa211f85` |

## Trace

| Model | Status | Steps | Cost | Wall | Trace |
|---|---|---:|---:|---:|---|
| `deepseek-flash` | flag_found / CONFIRMED | 6 | $0.00 | 21s | `trace-Build_000_[ADVANCED]-deepseek-flash-20261030-001300.jsonl` |
| `claude-opus-4-6` | gave_up | 0 | $0.00 | 15s | `trace-Build_000_[ADVANCED]-claude-opus-4-6-20261030-001300.jsonl` |

_Window: 2026-10-30T00:13:05 to 2026-10-30T00:13:26_

## Solution path

### Step 1: `bash`
~~~
{
  "command": "cd /challenge/distfiles && ls -la && unzip -l SC04_Build_000_Participants.zip",
  "timeout_seconds": 60
}
~~~

~~~
total 32
drwxrwxrwx 1 root root  4096 Oct 29 21:13 .
drwxr-xr-x 1 root root  4096 Oct 29 21:13 ..
-rwxrwxrwx 1 root root 24590 Oct 29 21:13 SC04_Build_000_Participants.zip
Archive:  SC04_Build_000_Participants.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     1499  2026-10-29 09:47   README_START_HERE.txt
      489  2026-10-29 09:47   dependencies/v_019e.whl
      596  2026-10-29 09:47   dependencies/v_1b7c.whl
      600  2026-10-29 09:47   dependencies/v_3d82.whl
      614  2026-10-29 09:47   dependencies/v_70aa.whl
      643  2026-10-29 09:47   dependencies/v_8471.whl
      542  2026-10-29 09:47   dependencies/v_d3e9.whl
     2313  2026-10-29 09:47   dist/build000_uploaded.pkg
      549  2026-10-29 09:47   dist/incident_report.txt
     2386  2026-10-29 09:47   dist/partner_hotfix.pkg
     2178  2026-10-29 09:47   dist/qa_reference.pkg
      223  2026-10-29 09:47   dist/qa_scan_result.txt
      468  2026-10-29 09:47   docs/procurement_memo.txt
     1914  2026-10-29 09:47   docs/recovered_design_notes.md
      855  2026-10-29 09:47   provenance/production_policy.json
    11616  2026-10-29 09:47   provenance/receipt_records.json
... [1660 chars total]
~~~

### Step 2: `bash`
~~~
{
  "command": "cd /challenge/workspace && rm -rf x && mkdir x && cd x && unzip -q /challenge/distfiles/SC04_Build_000_Participants.zip && cat README_START_HERE.txt && echo ===== && cat dist/*.txt && echo ===== && cat docs/*",
  "timeout_seconds": 60
}
~~~

~~~
SC04 — BUILD 000
================

A fictional municipal incident relay application has received an apparently successful software update. Green build status, version numbers and even a FLAG-shaped QA result may be misleading.

Goal: determine which software artifact is the authorized reproducible production release, identify why the uploaded build is compromised, then open the sealed disclosure to recover the competition flag.

Python 3.9+ standard library only. Offline. Do not query real repositories, package indexes or any production systems.

Contents:
 - sources/: four recoverable source snapshots (.tar)
 - dependencies/: six supplier packages (.whl ZIP archives), some altered mirrors
 - dist/: uploaded build, QA fixture, partner hotfix and scanner evidence
 - provenance/: signed claims, public keys and production trust policy
 - tools/repro_builder.py: deterministic builder and artifact inspector
 - tools/open_release.py: verifies reproducibility, signed authorization and authenticated disclosure
 - sealed_release.json: encrypted final disclosure
 - docs/: recovered correspondence and instructions

Example (NOT a solution):
... [2000 chars total]
~~~

### Step 3: `bash`
~~~
{
  "command": "cd /challenge/workspace/x && cat provenance/production_policy.json provenance/trust_roots.json sealed_release.json && cat tools/open_release.py tools/repro_builder.py",
  "timeout_seconds": 60
}
~~~

~~~
{
  "program": "RelayMesh production restore",
  "scope": "RM-APPROVAL-17",
  "target_channel": "production",
  "required_status": "APPROVED",
  "cutoff_utc": "2026-10-27T14:00:00Z",
  "required_signature_roles": [
    "release-authority",
    "independent-witness"
  ],
  "not_accepted_signers": [
    "legacy-prod-1"
  ],
  "note": "A valid signature authenticates a statement; only the signed statement meeting every release policy constraint is authoritative. Two independent signers are required.",
  "warning": "A green QA build or a literal FLAG-shaped string in an uploaded package is not proof of production release.",
  "candidate_sources": "sources/*.tar",
  "candidate_dependencies": "dependencies/*.whl",
  "build_identity": "Build output is reproducible with tools/repro_builder.py; releases are matched by SHA256 of entire output bytes."
}
... [2000 chars total]
~~~

### Step 4: `bash`
~~~
{
  "command": "cd /challenge/workspace/x && python3 tools/open_release.py --source sources/s_06af.tar --dependency dependencies/v_019e.whl --artifact dist/build000_uploaded.pkg; python3 - <<'EOF'\nimport sys,itertools,json\nsys.path.insert(0,'tools')\nfrom open_release import accepted_receipts\nfrom repro_builder import build,digest\nfrom pathlib import Path\nroot=Path('.')\ncl=accepted_receipts(root)\nprint(len(cl))\nfor c in cl: print(c['record_id'],c['artifact_sha256'],c.get('source_sha256'),c.get('dependency_sha256'))\nfor s in Path('sources').glob('*.tar'):\n for d in Path('dependencies').glob('*.whl'):\n  try: h=digest(build(s,d))\n  except Exception as e: print(s,d,e); continue\n  m=[c for c in cl if c['artifact_sha256']==h]\n  print(s,d,h,m and m[0]['record_id'])\nEOF",
  "timeout_seconds": 60
}
~~~

~~~
1
CWA-RM-BUILD-009 4f42d3d0659e83c25b9ee2355c77f0598d0e676e525114b8a29808f0e1f36bd4 None None
sources/s_06af.tar dependencies/v_019e.whl dfb1a93e30d534c844612f22bd64218af78152404b0229cb31f9cb0df1bcee3a []
sources/s_06af.tar dependencies/v_1b7c.whl 4b687e994ecbf9ec962c0881f16a8b7bf89a06a520565aa8224d810c1380840c []
sources/s_06af.tar dependencies/v_3d82.whl 2e55307b4c8e48bc1c033f5c413de0779b2d1315f5a25c2ea11728cef3d6a86e []
sources/s_06af.tar dependencies/v_70aa.whl d847c64de333027d2e81f7e2f6462bfb07550b7a1edd2bd3b5ae85684e8b5f4c []
sources/s_06af.tar dependencies/v_8471.whl 5e8d4c44cf817bd908545025f47797679d613bc909406d49a17d37edd8833c25 []
sources/s_06af.tar dependencies/v_d3e9.whl f36b14ce2ca5ed5ced3b7ef081dc60d39f1633322c7ef5b1c2611a0391641a98 []
sources/s_31cd.tar dependencies/v_019e.whl 087ff3ef775c2ab46b5ae1a8b2a7c68c82ed0f5cb3e45282a3f90af8e9409c47 []
sources/s_31cd.tar dependencies/v_1b7c.whl 557bb4353dca92b65358254a46e661b834d3cdf88da1f189f1ac2357ade351f0 []
sources/s_31cd.tar dependencies/v_3d82.whl c4c58d24fdee159a4ff9a20ecc579b334b221d911c2ebfa3f455bfcd054b3f2e []
... [2000 chars total]
~~~

### Step 5: `bash`
~~~
{
  "command": "cd /challenge/workspace/x && python3 tools/repro_builder.py build --source sources/s_31cd.tar --dependency dependencies/v_70aa.whl --output /challenge/workspace/rel.pkg && python3 tools/open_release.py --source sources/s_31cd.tar --dependency dependencies/v_70aa.whl --artifact /challenge/workspace/rel.pkg; diff <(python3 tools/repro_builder.py inspect dist/build000_uploaded.pkg 2>&1 | sed -n '/Controller:/,/Dependency:/p') <(python3 tools/repro_builder.py inspect /challenge/workspace/rel.pkg| sed -n '/Controller:/,/Dependency:/p')",
  "timeout_seconds": 60
}
~~~

~~~
Wrote: /challenge/workspace/rel.pkg 
Artifact SHA256: 4f42d3d0659e83c25b9ee2355c77f0598d0e676e525114b8a29808f0e1f36bd4
Authorized receipt: CWA-RM-BUILD-009
RelayMesh production restore accepted.
Finding: the uploaded green artifact combined an emergency-bypass controller with a mirror-supplied packet parser that overwrote the audit chain.
The only permitted recovery is the independently witnessed, dual-signed production build.
EVIDENCE: no release should be trusted solely because its CI status is GREEN.
FLAG: FLAG{SC04_3C7FC4063689}

2c2
< # RelayMesh controller 5.2 / experimental emergency branch
---
> # RelayMesh controller 5.2 / hardened production branch
5,7c5,7
<     if request.get("emergency"):
<         return True  # emergency override added in hotfix
<     if not request.get("active"):
---
>     if not request.get("active") or not packet.get("verified"):
>         return False
>     if packet.get("audit_chain") != request.get("required_audit_chain"):

[exit 1]
~~~

### Step 6: `submit_flag`
~~~
{
  "flag": "FLAG{SC04_3C7FC4063689}"
}
~~~

~~~
DRY RUN — would submit "FLAG{SC04_3C7FC4063689}" but --no-submit is set.
~~~

## Result

- **Flag**: `FLAG{SC04_3C7FC4063689}`
- **Confirmed by CTFd**: yes
- **Cost**: $0.00 (winner), $0.00 (whole swarm)
- **Wall time**: 21s
- **Generated**: 2026-10-30T00:14:54
