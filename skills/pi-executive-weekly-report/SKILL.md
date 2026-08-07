---
name: pi-executive-weekly-report
description: >-
  Weekly executive PI email: reported, total resolved, reported & resolved (MTD +
  this week), planned next week and by EOM. IST Mon–Sun boundaries. Run every Monday;
  paste from pi/reports/executive-weekly.md. Manual plan via pi/input/executive-weekly-plan.json.
---

# PI executive weekly report

## Location in repo

`pi/skills/pi-executive-weekly-report/` → symlink `.cursor/skills/pi-executive-weekly-report`.

## Goal

**Weekly leadership email** — one summary table, paste-ready subject line.

| Metric | Month (MTD) | This week |
| --- | --- | --- |
| PIs reported | | |
| Total resolved | | |
| Reported & resolved | | |
| Planned (next week) | — | |
| Planned (by EOM) | | — |

## Schedule

| Item | Value |
| --- | --- |
| **Send** | **Every Monday ~9:00 AM IST** (`Asia/Kolkata`) |
| **As-of** | Run date (same day as send) |
| **Format** | Email body, markdown |
| **Automation** | Double-click `current/pi/Run PI Executive Weekly.command` or CLI below; cron later if desired |

## Weekly send workflow

1. **Update plan** (until Jira ETAs are populated): edit `pi/input/executive-weekly-plan.json` with integer counts for `planned_next_week` and `planned_eom`. Use `null` to fall back to Jira ETA on open PIs.
2. **Refresh from Jira:**
   ```bash
   cd jira && source .venv/bin/activate
   python -m scripts.jira_automation executive-weekly-report
   ```
   Or double-click **`Run PI Executive Weekly.command`**.
3. **Send email:** open `pi/reports/executive-weekly.md` — copy **Subject** line + body into your mail client.
4. Dated archive kept at `pi/reports/executive-weekly-YYYY-MM-DD.md`.

## Time boundaries (mandatory, IST)

| Metric | Boundary |
| --- | --- |
| **Month (MTD)** | 1st of calendar month → `as-of` date (inclusive) |
| **This week** | Monday → Sunday containing `as-of` (inclusive) |
| **Planned next week** | Following Monday → Sunday |
| **Planned by EOM** | `as-of` → last day of month |

Week boundaries use **explicit IST dates in JQL** — not Jira `startOfWeek()`.

## Definitions

| Term | Rule |
| --- | --- |
| **Reported** | `created` in the time window |
| **Total resolved** | `status changed FROM` four open columns in the window (any vintage) |
| **Reported & resolved** | Both in the **same** window |
| **Planned** | Jira ETA on open PIs, or **manual** counts in `executive-weekly-plan.json` |

## Manual plan file

`pi/input/executive-weekly-plan.json`:

```json
{
  "planned_next_week": 8,
  "planned_eom": 22
}
```

When a key is set (not `null`), it **overrides** Jira ETA for that row in the report.

## Outputs

| Artifact | Path |
| --- | --- |
| Email draft (stable, refresh overwrites) | `pi/reports/executive-weekly.md` |
| Email draft (dated archive) | `pi/reports/executive-weekly-YYYY-MM-DD.md` |
| JSON snapshot | `pi/reports/executive-weekly-YYYY-MM-DD.json` |

## Email structure

1. **Subject** — auto-generated first line of markdown
2. **Summary table** — five metric rows only
3. **Boundary footnote** — one line (MTD / week / plan ranges)

No status breakdowns, BPE, or ops detail — use **`pi-daily-ops-report`** for that.

## Related

- **`pi-daily-ops-report`** — weekday ops queues and RCA
- **`pi-eta`** — populate Jira Client Committed Timeline (reduces need for manual plan file)
