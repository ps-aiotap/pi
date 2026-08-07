---
name: pi-daily-open-analysis
description: >-
  Weekday batch analysis of all open PIs (four board-774 columns). Queue counts,
  RCA gaps, and stale lists — no ETA. Writes pi/reports/daily-ops-YYYY-MM-DD.md.
  Run manually at 10:00 AM IST; cron later. Pair with pi-stale-assignee-reminder.
---

# PI daily open analysis (10 AM IST, weekdays)

## Location in repo

Stored under `current/pi/skills/pi-daily-open-analysis/`. Symlink to `.cursor/skills/pi-daily-open-analysis` at the workspace root for Cursor Agent Skill discovery.

## Goal

Produce a **weekday morning snapshot** of all **open PIs** for ops visibility. **No ETA** sections. Includes **stale** open PIs (≥2 working days without meaningful update, Mon–Fri IST).

**Open PI** = same four [board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774) columns as `pi-monthly-ageing` and `pi-daily-ops-report`.

## Schedule

| Item | Value |
| --- | --- |
| Run at | **10:00 AM IST** (`Asia/Kolkata`) |
| Cadence | **Weekdays only** |
| Automation | Manual now; `cron` later after confidence |

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Command

```bash
cd jira
python -m scripts.jira_automation daily-open-analysis
python -m scripts.jira_automation daily-open-analysis --open   # refresh + open HTML dashboard
```

**macOS:** double-click `current/pi/Run PI Weekday Morning.command` (analysis + stale reminders) or `Run PI Weekday Morning (dry-run).command` (preview only).

Implementation: `jira/scripts/jira_automation/daily_open_analysis.py` → `daily_ops_report.build_report(include_eta=False, include_stale=True)`.

## Outputs

| Artifact | Path |
| --- | --- |
| Report (dated) | `current/pi/reports/daily-ops-YYYY-MM-DD.md` |
| Stable email/dashboard md | `current/pi/reports/pi-ops-dashboard.md` |
| JSON snapshot | `current/pi/reports/daily-ops-YYYY-MM-DD.json` |
| HTML dashboard | `current/pi/reports/pi-ops-dashboard.html` |

## Report sections

- Executive snapshot (open count, severity within open, In QA, Verify Prod)
- Queue counts
- **Stale — assigned** (≥2 working days; eligible for Jira comment via `pi-stale-assignee-reminder`)
- **Unassigned — stale** (report only — **no Jira comment**)
- RCA gaps (post-eng Dev/Leakage; closed backfill)
- Chase list (RCA gaps only — no ETA)
- Volume (created/resolved today and 7d)

## Agent workflow

1. Confirm `jira/.env` credentials (`ping`).
2. Run `daily-open-analysis`.
3. Summarize: open count, assigned/unassigned stale counts, top RCA gaps.
4. If assignee reminders are due, run **`pi-stale-assignee-reminder`** (`stale-remind`; use `--dry-run` first).

## Related

- **`pi-stale-assignee-reminder`** — Jira comments to assignees on stale assigned open PIs
- **`pi-daily-ops-report`** — 5 PM IST variant **with ETA** (legacy ops email)
- **`pi-spec-manual-reproduction`** — on-demand repro steps in `pi/specs/` (not daily)
- `pi_config.jql_open_pi()`, `jira/scripts/jira_automation/stale_reminder.py`
