---
name: pi-triage-emails
description: >-
  Generates three Outlook-friendly HTML PI reports: daily exec progress (red clients,
  intake, Verify Prod waiting-closure), daily ETA+stale chase, and weekly RCA data
  chase — plus a paste-ready Daily Progress email summary. Opens HTML in browser.
  Cron daily 17:05 IST all 7 days.
---

# PI triage emails (17:05 IST daily)

## Outputs (stable HTML — overwrite each run)

| Report | Path | Audience |
| --- | --- | --- |
| Daily Progress | `pi/reports/pi-daily-progress.html` | Exec |
| Daily Progress email summary | `pi/reports/pi-daily-progress-summary.txt` | Exec (paste above HTML) |
| Daily ETA Chase | `pi/reports/pi-daily-eta-chase.html` | You (ops) |
| Weekly Data Chase | `pi/reports/pi-weekly-data-chase.html` | You (ops) |

Dated archives: `daily-progress-YYYY-MM-DD.{html,json}`, etc. under `pi/reports/`.

## Red clients

Source of truth: [`pi/input/red-clients.csv`](../../../pi/input/red-clients.csv)
(`Red Clients`, `Leader`). Matched on Jira Client field + summary (substring /
aliases — TFB→hctfb, Michael\*→zusman). Shared helper:
`load_red_clients` / `match_red_client` in
`jira/scripts/jira_automation/triage_emails.py`.

Also used by the PI monthly retro deck (slide 7 roster block).

## Run

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation triage-emails
```

## Related

- `jira/scripts/jira_automation/triage_emails.py`
- Skill: `pi-monthly-retro-deck` (slide 7 red-client roster)
