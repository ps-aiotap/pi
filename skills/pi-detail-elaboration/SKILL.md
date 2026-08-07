---
name: pi-detail-elaboration
description: >-
  Daily 10:06 IST: score open PB board-774 PIs as ready vs thin one-liners,
  coach reporters to add missing detail, and draft codebase-grounded elaborations
  for thin ones. Pull Bitbucket first. Writes pi/reports/pi-detail-elaboration.md.
  Never writes to Jira unless a human asks.
---

# PI detail evaluation & elaboration (10:06 IST)

## Goal

For **open PIs** on [board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774) (INCOMING BUGS / In Engineering Queue / IN DEVELOPMENT / Reopened):

1. Mark each **ready** / **thin** / **borderline** (advisory — subjective).
2. **Coach the PI creator (reporter)** with a paste-ready ask for the missing detail so engineering can progress without stalls.
3. For thin/borderline: optionally draft an elaboration grounded in refreshed Bitbucket clones (fill gaps while coaching happens).

Primary outcome: **creators learn what “work-ready” means** (repro, expected/actual, tenant/env, evidence) so the next steps start quickly.

**Never write to Jira** unless a human explicitly asks.

## Cron / run

```bash
open "current/pi/Run PI Detail Elaboration.command"
# or:
./cron/run-job.sh run pi-detail-elaboration manual
```

Chat: `pi-detail-elaboration`

## Agent steps

1. Refresh Bitbucket (primary clones only):

   ```bash
   bash current/pi/scripts/refresh_bitbucket_app_clones.sh --primary-only
   ```

2. Read/refresh queue: `current/pi/reports/pi-detail-elaboration.md` (includes **Reporter** + coach asks).

3. Score (advisory):

   | → thin | → ready |
   | --- | --- |
   | Empty / ≤~25 words / summary-only | Repro steps + expected/actual (or clear media + env) |
   | No repro / no expected vs actual | Enough to start without guessing |

4. For each **thin/borderline** (Critical/High first):

   - Keep/refresh the **coach ask** aimed at the **reporter** (what to add, why it unblocks next steps).
   - Optionally write/update `current/pi/elaborations/{KEY}.md` (problem, gaps, code paths, draft repro/AC with assumptions marked).

5. Summarize: thin count by reporter (who needs coaching most) + highest-priority thin keys.

## Do not

- Auto-comment on Jira without an explicit human ask.
- Invent client/tenant facts or cite code you did not find after refresh.
- Treat scores as blocking gates.
- Refresh `pi/` as application code.
