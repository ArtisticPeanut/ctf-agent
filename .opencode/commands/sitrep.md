---
description: Write a full sitrep (use at T-2h, T-1h, T-30m)
agent: commander
---

Write a full sitrep to `reports/sitrep-<hhmm>.md`.

Gather:
- `uv run python -m tools.status --json`
- `uv run python -m tools.status` for the human view
- `uv run python -m tools.habit_watch --once --json`
- `uv run python -m tools.command_log --show`

Include:
1. Solved / total, flags per hour, cost, burn rate, remaining budget.
2. Per-challenge table: name, points, status, cost, minutes, best model.
3. Stalled list with the exact rung-4 decisions.
4. Top 3 actions for the remaining time, ordered.
5. Anything the operator must do by hand (credentials, restarts, paid hints).

Be terse and factual. No speculation about flags that are not confirmed.
