---
name: pi-stale-assignee-reminder
description: >-
  Posts Jira comments @mentioning assignees on open PIs with no meaningful update
  for ≥2 working days (IST weekdays). Unassigned stale PIs appear in the daily
  report only — no Jira comment. Run weekdays ~10 AM IST after pi-daily-open-analysis.
---

# PI stale assignee reminder (10 AM IST, weekdays)

## Location in repo

Stored under `current/pi/skills/pi-stale-assignee-reminder/`. Symlink to `.cursor/skills/pi-stale-assignee-reminder` at the workspace root for Cursor Agent Skill discovery.

## Goal

Nudge **assignees** when an **open PI** (four board-774 columns) has had **no meaningful update** for **≥ 2 working days** (Monday–Friday, **IST**).

| Case | Action |
| --- | --- |
| Assigned + stale | Jira **comment** @mentioning assignee |
| Unassigned + stale | **Report only** (`pi-daily-open-analysis`) — **no Jira comment** |
| Not stale | No action |

**Meaningful update** = any changelog activity or comment **except** this automation's own stale-reminder comments (matched by author + wording — so bot nudges do not reset the clock).

**Repeat:** If still stale, post again only after **≥ 2 working days** since the last stale-reminder comment on that ticket.

## Schedule

| Item | Value |
| --- | --- |
| Run at | **10:00 AM IST** weekdays |
| Order | After **`pi-daily-open-analysis`** |
| Automation | **Manual only** (not part of `pi-weekday-morning` cron) |

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Commands

```bash
cd jira
# Preview (no Jira writes)
python -m scripts.jira_automation stale-remind --dry-run

# Post comments
python -m scripts.jira_automation stale-remind

# Full JSON result
python -m scripts.jira_automation stale-remind --dry-run --json
```

Implementation: `jira/scripts/jira_automation/stale_reminder.py`.

## Comment format

Plain assignee nudge (ADF `@mention`). Example:

```text
Hi @Dhananjay Davhale — This open PI has had no visible progress for 8 working days. Please add a status comment, update the ETA if needed, or move the ticket.
```

No timestamp, no automation footer. The script recognizes its own prior comments by author + wording (for cooldown only — not shown as a tag).

## Agent workflow

1. Run **`pi-daily-open-analysis`** (or read today's `daily-ops-*.json` stale section).
2. Run `stale-remind --dry-run`; show keys that would be commented.
3. On user approval, run `stale-remind` without `--dry-run`.
4. Report posted keys and any API errors.

## Do not

- Comment on **unassigned** stale PIs (PI ops triages from report).
- Use for In QA, Verify Prod, or Watchlist — **open four columns only**.

## Related

- **`pi-daily-open-analysis`** — stale lists in markdown/JSON
- `pi_config.jql_open_pi()`, `working_days.py`
