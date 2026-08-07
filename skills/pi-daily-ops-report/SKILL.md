---
name: pi-daily-ops-report
description: >-
  Generates the daily PI ops email (markdown) for 5 PM IST. Queue counts plus Dev RCA,
  Leakage RCA, and ETA gaps — no ageing. "Open PI" = four board-774 columns only.
  Skill-only; writes pi/reports/daily-ops-YYYY-MM-DD.md.
---

# PI daily ops report (5 PM IST email)

## Location in repo

Stored under `pi/skills/pi-daily-ops-report/`. Symlink only (no copy) to `.cursor/skills/pi-daily-ops-report` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Produce a **paste-ready email body (markdown)** for the daily PI ops send by **5:00 PM IST**. Focus: **queues**, **ETA gaps**, **Dev RCA gaps**, **Leakage RCA** summary — **no PI ageing** (no days-since-created buckets or oldest-open rankings).

## Open PI definition (mandatory)

**Open PI** = issues in **exactly four** [board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774) columns — same as **`pi-monthly-ageing`** and `jql_open_ageing()` in `pi_config.py`:

| Board column | Jira status |
| --- | --- |
| INCOMING BUGS | To Do |
| In Engineering Queue | In Review |
| IN DEVELOPMENT | In Progress |
| Reopened | On Hold/Reopened - Dev Team |

**Not open** for this count: In QA, Verify Prod, Watchlist, BA, Closed, Done, Historical.

Do **not** use `jql_open_engineering()` (six statuses) when reporting **open PI** count, ETA gaps on open PIs, or subject-line open count.

## Schedule

| Item | Value |
| --- | --- |
| Send by | **5:00 PM IST** (`Asia/Kolkata`) |
| Cadence | Weekdays (or daily if PIs run weekends — human decides) |
| Format | **Email body, markdown** (evolve to Confluence/Slack later) |
| Automation | **Skill only** for now; cron/script later after stabilization |

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Command (preferred)

**Personal dashboard (live Jira → HTML):** double-click `current/pi/Refresh PI Dashboard.command`, or:

```bash
cd jira && python -m scripts.jira_automation dashboard
```

Writes `current/pi/reports/pi-ops-dashboard.html` (embedded snapshot), **`pi-ops-dashboard.md`** (paste-ready email — same content as dated md), plus `daily-ops-YYYY-MM-DD.md` and `.json`.

Email-only refresh:

```bash
python -m scripts.jira_automation daily-ops-report
```

Implementation: `jira/scripts/jira_automation/daily_ops_report.py`.

## Data collection (agent fallback)

Use `daily_ops_report.build_report()` or Jira API + `pi_config.jql_open_pi_eta_scope()` for ETA lists.

**Open PI (4 columns)** — `pi_config.jql_open_ageing()` / `jql_open_pi()`:

- Open PI count
- Critical / Highest / High **within open PIs only**: `jql_open_pi_critical()`, `jql_open_pi_highest()`, `jql_open_pi_high()`

**ETA (Client Committed Timeline)** — `pi_config.jql_open_pi_eta_scope()` **only**:

- Missing / overdue / due-in-7d ETA tracked **only** for open PIs (four columns).
- **Never** flag In QA, Verify Prod, Watchlist, BA, or Closed for missing ETA.
- Chase list: `Missing ETA` / `Overdue ETA` gaps **only** for keys in the open-PI set.

**Other queues** (report separately — **not** counted as open PI):

- `jql_in_qa()`, `jql_verify_prod()`
- `jql_open_pi_critical()`, `jql_open_pi_highest()`, `jql_open_pi_high()` — severity within open PIs only
- `jql_critical_open()`, `jql_highest_open()` — all active non-terminal (optional context row)

Do **not** include in this report: Watchlist, Missing Team, `jql_open_engineering()` (six-status dashboard filter), or per-column sub-count tables.

**Dev RCA** — `customfield_10935`:

- Gap: **In QA + Verify Prod** (`jql_post_eng_rca_scope()`) with empty Dev RCA — eng handoff only; **never** flag open PIs still in dev
- Retro: **Closed** PIs without Dev RCA where `created >= 2026-05-21` (`pi_config.MONDAY_JIRA_IMPORT_DATE` — Monday.com import); listed in RCA gaps, not chase list

**Leakage RCA** — `customfield_11345` (single-select; legacy text was `customfield_10940`):

- Gap: **Verify Prod** with empty Leakage RCA (PM category before close)
- Retro: **Closed** PIs without Leakage RCA where `created >= 2026-05-21`
- Trend only: Leakage RCA category breakdown for **closed last 7 days** (same created cutoff)

## Output

| Artifact | Path |
| --- | --- |
| Email draft (stable, refresh overwrites) | `pi/reports/pi-ops-dashboard.md` |
| Email draft (dated archive) | `pi/reports/daily-ops-YYYY-MM-DD.md` |
| Dashboard HTML | `pi/reports/pi-ops-dashboard.html` |
| JSON snapshot | `pi/reports/daily-ops-YYYY-MM-DD.json` |

## Email structure (mandatory sections)

### 1. Subject line

```text
Subject: PI Daily Ops — {YYYY-MM-DD} — {open_pi_count} open PIs | {missing_eta_count} missing ETA | {missing_dev_rca_post_eng} missing Dev RCA (post-eng)
```

`open_pi_count` = **four-column** count only. Dev RCA count = **In QA + Verify Prod** only.

### 2. Executive snapshot (≤5 bullets)

- **Open PIs (4 columns):** count
- Critical / Highest **within open PIs** (not all active)
- **In QA** and **Verify Prod** queue sizes (separate — not open)
- Open PIs **missing Client Committed Timeline**
- **In QA / Verify Prod** missing Dev RCA; **Verify Prod** missing Leakage RCA

### 3. Queue table

Include a row only when **count &gt; 0**. Omit Watchlist, Missing Team, Open Engineering (6-status), and **Open PIs by column**.

### 4–8. Conditional sections (skip when empty)

Do **not** print `_None._` placeholders. **Omit** the heading and body when there is no data:

| Section | Skip when |
| --- | --- |
| `## ETA — …` entire block | missing, overdue, and due-in-7d lists all empty |
| `### Missing ETA` | no rows |
| `### Overdue ETA` | no rows |
| `### Due in next 7 days` | no rows |
| `## RCA gaps` entire block | all RCA subsections empty |
| `### In QA / Verify Prod missing Dev RCA` | no rows |
| `### Verify Prod missing Leakage RCA` | no rows |
| `### Closed without Dev RCA (created ≥ 2026-05-21)` | no rows |
| `### Closed without Leakage RCA (created ≥ 2026-05-21)` | no rows |
| `## Leakage RCA (closed last 7 days, created ≥ 2026-05-21)` | no qualifying closures in last 7 days |
| `## Chase list` | chase list empty |
| `## Volume` | created/resolved today and last 7d all zero |

### Email body header

After subject and `# PI Daily Ops — {date}`, go straight to **Executive snapshot**. No generated timestamp line, no open-PI definition footnote in the email (definition stays in this skill only).

### Explicitly exclude

- Age buckets, client ageing, `pi-monthly-ageing` bucket tables
- Treating Verify Prod or In QA as **open PI**
- Missing Dev/Leakage RCA on **open PIs** (still in dev — RCA not knowable yet)

## Related

- **`pi-monthly-ageing`** — same four-column open definition
- `pi_config.OPEN_AGEING_BOARD_COLUMNS`, `jql_open_ageing()`
- Per-PI: **`pi-dev-rca`**, **`pi-leakage-rca`**, **`pi-eta`**
