param(
    [int]$IntervalMinutes = 3,
    [string]$Agent = "commander",
    [string]$Prompt = "Run one commander operating-loop tick. If nothing changed since the last tick, reply NO-OP and stop."
)

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location -LiteralPath $root
New-Item -ItemType Directory -Force -Path "reports" | Out-Null
$log = Join-Path $root "reports\commander_loop.log"
$first = $true

while ($true) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -LiteralPath $log -Value "[$stamp] tick"
    try {
        if ($first) {
            opencode run --agent $Agent $Prompt 2>&1 | Tee-Object -FilePath $log -Append
            $first = $false
        } else {
            opencode run --agent $Agent --continue $Prompt 2>&1 | Tee-Object -FilePath $log -Append
        }
    } catch {
        Add-Content -LiteralPath $log -Value "[$stamp] ERROR: $_"
    }
    Start-Sleep -Seconds ([Math]::Max(30, $IntervalMinutes * 60))
}
