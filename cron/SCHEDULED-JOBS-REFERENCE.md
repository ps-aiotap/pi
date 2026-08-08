# Scheduled PI jobs

| Job id | Schedule (IST) | Runner | Skill / notes |
| --- | --- | --- | --- |
| `pi-hourly-ops` | `0 9-18 * * 1-5` hourly weekdays (`CRON_TZ=Asia/Kolkata`) | `cron/runners/pi-hourly-ops.sh` | Dispatcher: assign-engineering-queue + fix-loop every hour + analysis skills by IST hour (see matrix). Install: `crontab cron/crontab.example` |
| `pi-sdlc-fix-loop` | *(invoked by hourly-ops; still runnable alone)* | `cron/runners/pi-sdlc-fix-loop.sh` | `pi-sdlc-fix-loop` — 1 PI/hour |
| `pi-playwright-fix-audit` | *(Stage 2 — not scheduled yet)* | `cron/runners/pi-playwright-fix-audit.sh` | `pi-playwright-fix-audit` |
| `blueocean-new-pi` | `30 9-17/2 * * 1-5` | `cron/runners/blueocean-new-pi.sh` | `pi-blueocean-new-pi-watch` |

## Dispatcher vs Agent

Cron is a **dispatcher only**. It does **not** run Cursor Agent or finish Jira/code/Playwright work by itself.

```text
crontab → bash runners → refresh clones
                      → write prompts under cron/state/prompts/
                      → fix-loop: pick PI + write PB-*-agent-prompt.md
```

| Layer | What it does | What it does not do |
| --- | --- | --- |
| **Dispatcher** (`pi-hourly-ops` / `pi-sdlc-fix-loop.sh`) | Refresh app clones; choose skills from the hourly matrix; write markdown prompts; pick next queue PI | Edit product code; call Jira; run Playwright; “complete” assign/deep-dive/fix |
| **Agent** (Cursor Agent mode) | Open a prompt from `cron/state/prompts/` and follow `@pi/skills/...` | — |

So a log line like `OK: pi-assign-engineering-queue → ...agent-prompt.md` means the **prompt was written**. Assign/fix/analysis finish only after someone opens that prompt in Agent mode (or a Cursor Automation does).

After each hour, open `cron/state/prompts/hourly-ops-YYYY-MM-DD-HH.md` and run the listed prompts.

## Hourly skill matrix (IST)

Configured in `cron/config/hourly-skill-matrix.json`:

| Hour | Skills |
| --- | --- |
| 09, 12–18 | **`pi-assign-engineering-queue`** then `pi-sdlc-fix-loop` |
| **10** | assign-engineering-queue + fix-loop + **deep dive** + open analysis + detail elaboration + non-eng disposition + stale reminder |
| **11** | assign-engineering-queue + fix-loop + meeting brief |

**Skip if already done (intake & deep analysis):**

| Skill | Considered done when |
| --- | --- |
| `pi-daily-deep-dive` | `pi/reports/daily-deep-dive-YYYY-MM-DD.md` or today’s entry in `pi/ops/daily-deep-dive-state.json` |
| `pi-daily-open-analysis` | `pi/reports/daily-ops-YYYY-MM-DD.md` |
| `pi-detail-elaboration` | `pi/reports/pi-detail-elaboration.md` updated / dated today |
| `pi-non-eng-disposition` | dated non-eng report under `pi/reports/` |
| `pi-meeting-brief` | `pi/reports/meeting-brief-YYYY-MM-DD.md` |
| Per-PI intake (fix loop) | `pi/specs/{KEY}.md` (+ test-plan or evidence-analysis) — see `skill-already-done.py --check-intake` |

Checker: `cron/scripts/skill-already-done.py`. Secondary: once-per-day flag in `cron/state/pi-hourly-ops.json`.

## Manual run

```bash
cd /var/www/sourcecode
./cron/run-job.sh run pi-hourly-ops manual
HOUR_OVERRIDE=10 ./cron/runners/pi-hourly-ops.sh   # backfill 10:00 pack
PI_KEY=PB-xxxx ./cron/runners/pi-sdlc-fix-loop.sh  # fix-loop only
```

## State

- `cron/state/pi-hourly-ops.json` — which skills fired per IST date
- `cron/state/pi-sdlc-fix-loop.json` — fix-loop queue + per-PI status
- `cron/state/prompts/hourly-ops-YYYY-MM-DD-HH.md` — index of prompts for the hour
- `cron/state/prompts/{skill}-YYYY-MM-DD-agent-prompt.md` — analysis skill prompts
- `cron/state/prompts/{KEY}-agent-prompt.md` — fix-loop PI prompt

## Logs

- `cron/logs/pi-hourly-ops.log`
- `cron/logs/pi-sdlc-fix-loop.log`
