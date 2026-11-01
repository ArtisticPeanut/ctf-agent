---
description: Run one commander operating-loop tick
agent: commander
---

Run one commander operating-loop tick now.

1. `uv run python -m tools.status --json`
2. `uv run python -m tools.habit_watch --once --send`
3. Pick the highest points/minute unsolved challenge.
4. Apply the lowest applicable escalation rung. Only message the engine if rung >= 1.
5. Append exactly one line with `uv run python -m tools.command_log "..."`.

If nothing changed since the previous tick, reply `NO-OP` and stop. Do not read
more than one trace tail, and do not spend more than 5 minutes of context.
