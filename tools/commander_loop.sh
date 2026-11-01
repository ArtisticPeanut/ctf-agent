#!/usr/bin/env bash
# Optional autonomous commander tick. Run inside tmux.
set -uo pipefail
INTERVAL_MINUTES="${INTERVAL_MINUTES:-3}"
AGENT="${AGENT:-commander}"
PROMPT="${PROMPT:-Run one commander operating-loop tick. If nothing changed since the last tick, reply NO-OP and stop.}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p reports
LOG="$ROOT/reports/commander_loop.log"
first=1

while true; do
  stamp="$(date -u +'%Y-%m-%d %H:%M:%S')"
  echo "[$stamp] tick" | tee -a "$LOG"
  if [ "$first" = "1" ]; then
    opencode run --agent "$AGENT" "$PROMPT" 2>&1 | tee -a "$LOG"
    first=0
  else
    opencode run --agent "$AGENT" --continue "$PROMPT" 2>&1 | tee -a "$LOG"
  fi
  sleep $(( INTERVAL_MINUTES * 60 > 30 ? INTERVAL_MINUTES * 60 : 30 ))
done
