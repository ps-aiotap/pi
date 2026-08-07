---
name: pi-blueocean-new-pi-watch
description: >-
  Weekday every-2h watch for newly created BlueOcean PB PIs; fires macOS
  Notification Center alert. State in cron/state only — no pi/reports files.
---

# BlueOcean new-PI macOS alert (≤2h)

## Goal

If a **new** BlueOcean PI is created, notify within ~2 hours via **macOS notification**. Not part of red-client daily email.

## Command

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation blueocean-new-pi-watch
python -m scripts.jira_automation blueocean-new-pi-watch --dry-run
```

Or: `open "current/pi/Run BlueOcean New PI Watch.command"`

## Schedule

| Item | Value |
| --- | --- |
| Cron | `30 9-17/2 * * 1-5` (Asia/Kolkata) — 09:30, 11:30, 13:30, 15:30, 17:30 weekdays |
| Job id | `blueocean-new-pi` |
| Runner | `cron/runners/blueocean-new-pi.sh` |

## Match

Client field or summary contains `blue ocean` / `blueocean` / `hcblueocean` (case-insensitive).

## Artifacts

| Path | Role |
| --- | --- |
| `cron/state/blueocean-new-pi.json` | `last_run_ist` + `seen` keys (TTL ~30d) |
| `cron/logs/blueocean-new-pi.log` | Runner log |

**Do not** write MD/HTML under `pi/reports/`.

## Silence

No new BlueOcean creates since last run → no notification.
