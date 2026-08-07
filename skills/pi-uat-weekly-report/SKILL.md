---
name: pi-uat-weekly-report
description: >-
  Weekly rollup of UAT evidence reviews + regression map drift for discussion
  with the test automation lead. Writes pi/reports/uat-evidence-weekly-YYYY-MM-DD.md.
---

# PI UAT weekly report

## Location in repo

`pi/skills/pi-uat-weekly-report/` → symlink `.cursor/skills/pi-uat-weekly-report`.

## Goal

Aggregate **`pi-uat-evidence-review`** outputs for the week into one doc for your **automation lead sync**:

- PIs reviewed and verdicts
- Recurring evidence gaps
- Develop vs master regression drift
- Proposed **dev impact checklist** updates from recurring patterns

| Output | Path |
|--------|------|
| Weekly markdown | `pi/reports/uat-evidence-weekly-YYYY-MM-DD.md` |
| Weekly JSON | `pi/reports/uat-evidence-weekly-YYYY-MM-DD.json` |

## When to run

- **Friday 11:00 IST** (cron) — after Thu regression map refresh + weekday UAT reviews
- On demand before automation lead meeting

## Prerequisites

- UAT reviews ran during the week (`pi-uat-evidence-review`)
- Regression map present (`pi-regression-map`)

## CLI

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation uat-weekly-report
python -m scripts.jira_automation uat-weekly-report --week-ending 2026-07-10
python -m scripts.jira_automation uat-weekly-report --json
```

## Cron chain (recommended)

1. **Thu 10:30** — `pi-regression-map` (fresh Develop refs)
2. **Mon–Fri 10:35** — `pi-uat-evidence-review --uat-column --live`
3. **Fri 11:00** — `pi-uat-weekly-report`

## Related

- **`pi-uat-evidence-review`** — per-ticket reviews + Jira comments
- **`pi-regression-map`** — benchmark source

Implementation: `jira/scripts/jira_automation/uat_weekly_report.py`
