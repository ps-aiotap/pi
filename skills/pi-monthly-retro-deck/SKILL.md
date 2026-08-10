---
name: pi-monthly-retro-deck
description: >-
  First working day (Mon–Fri) 11:15 IST: build the prior-month PI retro PPTX —
  8-slide AV_PI_Management_<Mon><YYYY>_v<N>.pptx auto-versioned into OneDrive
  PI/Problem Management. Incoming SoT = Monday.com Excel (report date ≤ 21 May
  2026) + Jira PB created after cutover; pure Jira for later months. Saves the
  JQL used to pi/reports/pi-management-retro-jql-YYYY-MM.md for sanity checks.
---

# PI Management monthly retro deck

## Location in repo

`pi/skills/pi-monthly-retro-deck/` → symlink `.cursor/skills/pi-monthly-retro-deck`.

## Goal

Reproduce the April 2026 Retro2 v8 layout for the **prior month**, 8 slides:

| Slide | Content |
| --- | --- |
| 1 | Title — Monthly Retro · `<Month> <Year>` |
| 2 | PI Pulse — KPI tiles (Total, Critical, High, C+H%, Watchlist, VoP, CR, Closed) + Key Insight MoM line |
| 3 | PI Disposition — "Not All PIs Are Bugs" table + blurb + action (charts removed) |
| 4 | Top Problem Themes — per engineering team (plain text) |
| 5 | PI Root Causes — Dev RCA + Leakage RCA with real counts (plain text) |
| 6 | Problem Management Actions — 6 commitments, auto-filled from metrics + carried forward |
| 7 | Open Critical Watch List + **Red Clients roster** (see below) |
| 8 | Month-over-Month Trends — prior vs report month |

Charts, the OLE image, decorative formatting and slide numbers are stripped;
slides 4–8 are plain readable text.

### Slide 7 detail

1. **Open Critical Watch List** — Critical / Business Critical PIs not Closed and
   not Rejected/FNR (columns: PI ID, Status, Team, Issue).
2. **Red clients (escalation roster)** — appended under the watch table. Loaded
   at render time from [`pi/input/red-clients.csv`](../../../pi/input/red-clients.csv)
   (columns `Red Clients`, `Leader`). Format: `Client — Leader`. Do not hardcode
   client names in the skill or generator; edit the CSV to change the roster.

Current roster (for sanity checks only — CSV is SoT):

| Red client | Leader |
| --- | --- |
| Acadia | Anil |
| Cohn Reznick | Anil |
| Heritage Wealth | Anil |
| Altium | Ravi |
| TFB | Ravi |
| Zeeco | Ravi |
| Dayan | Sandip |
| Michael Zusman | Sandip |
| Mobo | Sandip |

## Incoming source of truth (mandatory)

- **Monday.com era** — report date **≤ 21 May 2026**: rows from the Monday.com
  Excel export (`~/Downloads/Production_Issues_May26.xlsx`, "Report Date").
- **After 21 May 2026**: Jira **PB `created`** in the month.
- Months fully after the cutover (Jun 2026 onward) are **pure Jira created**.
- The exact JQL (and Monday file/row count) is written to
  `pi/reports/pi-management-retro-jql-YYYY-MM.md` every run.

## Metric definitions

| Metric | Rule |
| --- | --- |
| **Total** | Incoming cohort per SoT above (or `--incoming-override` for a manual monthly-review number) |
| **Critical** | Priority ∈ {Critical, Business Critical} |
| **High** | Priority = High |
| **Disposition** | Derived from Jira status / Monday group (Closed, VoP, Convert to CR, Watchlist, QA Replicated, Open/In-flight) |
| **Watchlist** | disposition = Watchlist / Suspended Issues (Feedback PI) |
| **Convert to CR** | status `Convert_To_CR` / Monday BA group |
| **Reopened** | status Reopen |
| **Dev RCA / Leakage RCA** | `customfield_10935` / `customfield_11345`, bucketed for slides 5 & 8 |
| **Watch list** | Critical PIs not Closed and not Rejected/FNR |
| **Red clients (slide 7)** | Static escalation roster from `pi/input/red-clients.csv` (not a live open-PI filter) |

## When to run

- **Automatic**: first working day of the month, 11:15 IST (cron fires days 1–3;
  runner no-ops unless it is the first weekday). Prior month.
- **Manual**: `current/pi/Run PI Monthly Retro Deck.command`, or:

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation pi-management-retro-deck --month 2026-06
```

| Flag | Purpose |
| --- | --- |
| `--month YYYY-MM` | Report month (default: prior calendar month) |
| `--output PATH` | Explicit output path (skips auto-version) |
| `--output-dir DIR` | Auto-versioned dir (default: OneDrive PI/Problem Management) |
| `--monday-excel PATH` | Monday.com export (auto-detected for the May era) |
| `--incoming-override N` | Force reported total (monthly-review SoT) |
| `--require-first-working-day` | No-op unless today is the month's first weekday |

## Versioning

Output is `AV_PI_Management_<Mon><YYYY>_v<N>.pptx`; `N` = highest existing + 1
in the OneDrive folder (so re-runs bump the version, never overwrite).

## Outputs

| Artifact | Path |
| --- | --- |
| PPTX | OneDrive `PI/Problem Management/AV_PI_Management_<Mon><YYYY>_v<N>.pptx` |
| Metrics JSON | `pi/reports/pi-management-retro-YYYY-MM.json` (feeds next month's MoM) |
| JQL audit | `pi/reports/pi-management-retro-jql-YYYY-MM.md` |

## Agent workflow

1. Confirm `jira/.env` (`ping`).
2. Run `pi-management-retro-deck` (add `--month` for a specific month).
3. Open the PPTX; spot-check slide 2 KPI tiles and slide 8 MoM vs the saved JQL.
4. If Jira auth fails, refresh `jira/.env` and re-run.

## Related

- `jira/scripts/jira_automation/pi_management_retro_deck.py`
- `jira/scripts/jira_automation/deck_common.py` (first-working-day + version bump)
- `pi-monthly-mr-deck` — 4-slide Management Review deck, same schedule
- Template: OneDrive `AV_PI_Management_April2026_Retro2_v8.pptx`
