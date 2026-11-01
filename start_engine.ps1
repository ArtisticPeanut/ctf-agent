param(
    [switch]$NoSubmit,
    [int]$MaxChallenges = 5,
    [string]$Coordinator = "codex",
    [string]$CoordinatorModel = "gpt-5.4",
    [int]$MsgPort = 9400
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $root
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"

if (-not (Test-Path -LiteralPath ".env")) {
    Write-Error "Missing .env. Copy .env.example to .env and fill CTFD_URL plus credentials."
    exit 2
}

New-Item -ItemType Directory -Force -Path logs, reports | Out-Null

$engineArgs = @(
    "run", "ctf-solve",
    "--challenges-dir", "challenges",
    "--max-challenges", "$MaxChallenges",
    "--msg-port", "$MsgPort",
    "--coordinator", $Coordinator,
    "--coordinator-model", $CoordinatorModel,
    "-v"
)
if ($NoSubmit) { $engineArgs += "--no-submit" }

Write-Host "Launching: uv $($engineArgs -join ' ')"
& uv @engineArgs
exit $LASTEXITCODE
