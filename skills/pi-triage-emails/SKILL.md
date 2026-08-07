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

Dated archives: `daily-progress-YYYY-MM-DD.html` + `.json`, `daily-progress-summary-YYYY-MM-DD.txt` (and eta/weekly prefixes).

The summary is also stored on the progress JSON as `email_summary` and printed to stdout after each run.

## Command

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation triage-emails          # open browser
python -m scripts.jira_automation triage-emails --no-open
```

Or: `open "current/pi/Run PI Triage Emails (5 PM).command"`

## How to send Daily Progress

1. Subject from the HTML header bar (or JSON `subject`)
2. Body = contents of `pi-daily-progress-summary.txt`, then the HTML report below it

## Schedule

| Item | Value |
| --- | --- |
| Cron | `5 17 * * *` (Asia/Kolkata) — **every day** including weekends |
| Job id | `pi-triage-emails` |
| Runner | `cron/runners/pi-triage-emails.sh` |

## Red clients

[`pi/input/red-clients.csv`](../../input/red-clients.csv) — match Jira Client field, then summary.

## Rules

- Exec progress: **no** stale, **no** ETA/RCA chase tables
- Intake is a **cohort funnel** on PIs *created* in the window: Reported = Redirected to CR/Feedback + Closed + Still on defect path (by current status). Never subtract "status changed in window" counts from created counts — those are different PIs. Window disposition activity for PIs of any age is a footnote only
- Placeholder tickets (summary exactly `test`, `testing`, `dummy`, etc. — see `INTAKE_NOISE_SUMMARIES`) are dropped from intake and listed in the footnote
- Email summary (`render_daily_progress_summary`) must follow the same cohort math — never claim “all redirected” from unequal populations
- Verify Prod waiting-closure: Department table Product/Engineering vs Services (CS) + Grand Total (assignee vs `pi/input/team/atlassian-teams.md`)
- Critical open + Red client tables include **Ageing days** (days in current status)
- ETA chase: missing/overdue/due-7d + assigned stale only
- Weekly data: capped Dev/Leakage RCA debt (created ≥ 2026-05-21)
- Primary artifact is **HTML**; cron **opens** files in the browser; summary is plain text for the email intro
