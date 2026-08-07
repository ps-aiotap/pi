---
name: pi-monthly-mr-deck
description: >-
  First working day (Mon–Fri) 11:20 IST: build the prior-month MR (Management
  Review) PPTX — 4 slides (Defect Leakage & Issue Aging, DM & PI Trend, CPE
  Update for the month, CPE AWS Costs) — and refresh stable CSV sidecars in
  OneDrive MR/ for Excel paste. Starts from the prior month's MR deck and writes
  AV MR - <Month> <Year>.pptx (re-runs bump to _v<N>).
---

# Monthly MR (Management Review) deck

## Location in repo

`pi/skills/pi-monthly-mr-deck/` → symlink `.cursor/skills/pi-monthly-mr-deck`.

## Goal

Each run (cron or manual) does two things for the **prior month**:

1. Refresh **MR Excel CSV sidecars** in OneDrive `MR/` (Jira PB/DM + leakage /
   ageing / AWS monthly series) so you can paste into the Excel workbooks that
   feed the charts.
2. Build the **4-slide Management Review PPTX**.

| Slide | Content |
| --- | --- |
| 1 | Engineering — Defect Leakage & Issue Aging (12-month charts) |
| 2 | Engineering — DM Trend & PI Trend (12-month lines) + Reported vs Qualified on PI chart |
| 3 | Cloud Platform Engineering — Update for the month (achievements + planned tables) |
| 4 | Cloud Platform Engineering — AWS Costs (chart + top cost heads) |

## When to run

- **Automatic**: first working day of the month, 11:20 IST (cron fires days 1–3;
  runner no-ops unless it is the first weekday). Prior month.
- **Manual**: `current/pi/Run Monthly MR Deck.command`, or:

```bash
cd /Users/pushpendu/data/code/av
DECK_FORCE=1 ./cron/run-job.sh run pi-monthly-mr-deck manual
```

Or the pieces separately:

```bash
cd jira && source .venv/bin/activate
MONTH=$(python -m scripts.jira_automation.deck_common prior-month)
python -m scripts.jira_automation export-mr-excel-sidecars --months "$MONTH"
python -m scripts.jira_automation monthly-engineering-deck --month "$MONTH"
```

Backfill more than one month into the CSVs (does not change the PPTX):

```bash
python -m scripts.jira_automation export-mr-excel-sidecars --months 2026-06,2026-07
```

## Prerequisites

- `jira/.env` (`ping` succeeds).
- Valid AWS SSO sessions for the AWS cost slide / CSV (profiles av-prod/av-qa/av-poc);
  falls back to carried-forward chart values if unavailable.
- **Base deck**: prior month's engineering MR deck in OneDrive `MR/`
  (`AV MR - <PriorMonth> <Year>.pptx`, highest `_v<N>`). Pass `--template` to
  override. The generator errors out if no prior deck is found — it does **not**
  fall back to the 2-slide `jira/templates/presentation-engineering-monthly.pptx`.
- Monday export `MR/MR_Production_Issues.xlsx` — used once to seed the Qualified
  PI history when the prior deck does not yet have that series.

## Versioning / destination

| Item | Value |
| --- | --- |
| Folder | OneDrive `MR/` (not `PI/Problem Management`) |
| First write | `AV MR - <Month> <Year>.pptx` |
| Re-runs | `AV MR - <Month> <Year>_v2.pptx`, `_v3`, … |

## Outputs

| Artifact | Path |
| --- | --- |
| PPTX | OneDrive `MR/AV MR - <Month> <Year>.pptx` (or `_v<N>`) |
| CSV sidecars | OneDrive `MR/` — see below (overwritten each run) |
| Metrics JSON | `pi/reports/monthly-engineering-deck-YYYY-MM.json` |
| Summary MD | `pi/reports/monthly-engineering-deck-YYYY-MM.md` |

## MR Excel CSV sidecars

Stable filenames in OneDrive `MR/` — **overwritten every monthly run** with the
prior-month window (same as the deck). Use them to update the Excel workbooks;
the skill does **not** write into the `.xlsx` files (Analysis pivots and AWS
region sheets stay yours to refresh).

| CSV | Feeds | Contents |
| --- | --- | --- |
| `MR_Production_Issues.csv` | `MR_Production_Issues.xlsx` → `production issues` | PB issues created in the month (Monday column order) |
| `MR_Data_Maintenance_Issues.csv` | `MR_Data_Maintenance_Issues.xlsx` → `data maintenance issues` | DM issues created in the month |
| `DefectLeakage_monthly.csv` | `DefectLeakage_Ageing_AwsCost.xlsx` → Analysis | `month,defect_leakage` |
| `IssueAgeing_monthly.csv` | same Analysis sheet | ageing days + sample / cutover columns |
| `AWS_Cost_monthly.csv` | same (Actual series) | `month,actual_total,av_prod,av_qa,av_poc` |

**How to use**

1. Run the monthly skill (or `export-mr-excel-sidecars` alone).
2. **PI / DM:** delete the matching month’s rows on the raw sheet, paste the CSV
   under the header, refresh the `Analysis` pivot.
3. **Leakage / Ageing / AWS Cost:** paste the month’s values into the Analysis
   month columns (or chart data source). Leave `AWS` / `AWSQA` / `AWSPoC`
   region sheets alone.

CLI: `python -m scripts.jira_automation export-mr-excel-sidecars`
([`export_mr_excel_sidecars.py`](../../../jira/scripts/jira_automation/export_mr_excel_sidecars.py)).

## How series are built (PPTX)

PB was migrated from Monday.com on **21 May 2026** (`pi_config.MONDAY_JIRA_IMPORT_DATE`).
Imported issues carry the import timestamp as `created`, so pre-cutover history
**cannot** be rebuilt from Jira.

1. Read the prior deck's chart caches (leakage, ageing, DM, PI reported, AWS).
2. Shift left one month; append the report-month value from Jira / Cost Explorer.
3. Qualified PI history: from the prior deck if present, otherwise from
   `MR_Production_Issues.xlsx` (Monday statuses) with blank-status May rows
   dispositioned via live Jira; report month always from Jira.

The Monday-vs-Jira source break at the cutover (e.g. Jun reported 94 Monday vs
~102 Jira) is inherited from the June deck and left as-is.

## Qualified PI

**Qualified** = reported in the month, minus PIs dispositioned with no engineering
fix. Same rule as the non-eng disposition report:

- **Jira**: `Feedback PI`, `Convert_To_CR`, or `Closed` with no engineering-touch
  status in the changelog (`In Review`, `In Progress`, `In QA`,
  `VERIFICATION ON PRODUTION`, `Reopen`).
- **Monday history**: Status in Convert to CR / Feedback / Rejected & Closed /
  Fix Not Required / Duplicate / Duplicate & Closed / Not Replicated, or Group = BA.

Plotted as a second line on the PI Trend chart (Reported + Qualified), with a
definition note in the Issue Management text block on slide 2.

## Issue ageing (report month)

Mean days from `created` to first terminal status (`Closed` / `Convert_To_CR` /
`Done`) for PIs that closed in the month. Issues created **before** the Monday
cutover are excluded from the headline average (their `created` is the import
timestamp). The summary MD records excluded count and the unfiltered average.

## Chart integrity

Charts are updated via `python-pptx` `replace_data` (lxml). Do **not** patch
chart XML with `xml.etree.ElementTree` — that renames namespaces to `ns0:` and
destroys `mc:AlternateContent` / `c16`, producing a corrupt PPTX that PowerPoint
prompts to repair.

## Related

- `pi-monthly-engineering-deck` — same PPTX generator (`monthly_engineering_deck.py`)
- `pi-monthly-retro-deck` — 8-slide PI retro deck, same first-working-day schedule
- `jira/scripts/jira_automation/deck_common.py` (first-working-day + version bump)
- `jira/scripts/jira_automation/export_mr_excel_sidecars.py` (CSV sidecars)
