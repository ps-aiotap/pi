---
name: pi-monthly-engineering-deck
description: >-
  Generates the monthly Engineering leadership PPTX (3 slides): defect leakage,
  issue ageing, PI/DM trends, and CPE achievements/planned. Run at month-end;
  writes presentation1-YYYY-MM.pptx and pi/reports/monthly-engineering-deck-*.json.
---

# Monthly Engineering leadership deck

## Location in repo

`pi/skills/pi-monthly-engineering-deck/` → symlink `.cursor/skills/pi-monthly-engineering-deck`.

## Goal

Produce **`presentation1-YYYY-MM.pptx`** — leadership deck (template may be 2 or 3 slides):

| Slide | Content (when present in template) |
| --- | --- |
| 1 | Defect leakage + issue ageing (12-month charts), AWS cost note |
| 2 | **Either** PI/DM trends + snapshot **or** CPE AWS Costs chart + top heads |
| 3 | CPE achievements (report month) + planned (next month) — when template includes it |

**Defects, issues, and PIs** are the same thing (PB project).

## When to run

- **Last business day of the month** or **1st of the following month** for the prior month retro.
- Invoke: `@pi-monthly-engineering-deck` or *"run monthly engineering deck for June 2026"*.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping   # must succeed
```

Template: `jira/templates/presentation-engineering-monthly.pptx` (copy of leadership deck).

## Command

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation monthly-engineering-deck --month 2026-06
```

| Flag | Purpose |
| --- | --- |
| `--month YYYY-MM` | Report month (default: prior calendar month) |
| `--output PATH` | PPTX path (default: `~/Downloads/presentation1-YYYY-MM.pptx`) |
| `--from-json PATH` | Re-render from saved metrics (skip Jira) |
| `--template PATH` | Override PPTX template |

## Metric definitions (mandatory)

| Metric | Rule |
| --- | --- |
| **Defect leakage** | PIs **reported** in month with Leakage RCA = `New Code Fix`, **plus** PIs in **Reopen at month-end** (union, deduped) |
| **Issue ageing** | Avg days from `created` → exit from 4 open columns for PIs resolved that month |
| **PI reported (chart)** | PB issues **created** in each month |
| **PI reported (snapshot)** | Same for report month |
| **Resolved (fleet-wide)** | `status changed FROM` 4 open columns in report month (any vintage) |
| **BPE** | `resolved_fleet / reported × 100` (can exceed 100%) |
| **Open / carry-over** | PB in 4 engineering columns on **1st of next month** (`status WAS IN` … `ON "YYYY-MM-01"`) |
| **DM open (chart)** | Unresolved DM count at each month-end |
| **CPE achievements** | Strategic CPE items **Done** in report month (Route53, LB, Audit, WAF, automation cluster) |
| **CPE planned** | Open CPE + SWAT + RM infra items for next month (Hangfire, RDS Proxy, MySQL 8.4, Chatbot, WAF) |

### Four open PI columns (board 774)

INCOMING BUGS · In Engineering Queue · IN DEVELOPMENT · Reopened

Jira statuses: To Do · In Review · In Progress · Reopen

## Outputs

| Artifact | Path |
| --- | --- |
| PPTX | `~/Downloads/presentation1-YYYY-MM.pptx` (or `--output`) |
| Metrics JSON | `pi/reports/monthly-engineering-deck-YYYY-MM.json` |
| Summary MD | `pi/reports/monthly-engineering-deck-YYYY-MM.md` |

## Agent workflow

1. Confirm `jira/.env` credentials (`ping`).
2. Run `monthly-engineering-deck --month YYYY-MM`.
3. Open the PPTX and spot-check slide 2 snapshot vs Jira filters.
4. If Jira auth fails, ask the human to refresh `jira/.env`, or re-render with `--from-json` after fixing the JSON.

## Boards referenced

- PI: [PB board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774)
- DM: [DM board 977](https://assetvantage.atlassian.net/jira/software/c/projects/DM/boards/977)
- CPE: [CPE board 206](https://assetvantage.atlassian.net/jira/software/c/projects/CPE/boards/206)
- Roadmap (CPE-related): [RM board 944](https://assetvantage.atlassian.net/jira/software/c/projects/RM/boards/944)

## Related

- `jira/scripts/jira_automation/monthly_engineering_deck.py`
- `pi-executive-weekly-report` — same PI reported/resolved definitions
- `pi-monthly-ageing` — open PI count (live snapshot; deck uses historical `status WAS` for month-end)
