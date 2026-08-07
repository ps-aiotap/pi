---
name: pi-leakage-coverage-funnel
description: >-
  Friday funnel: Leakage RCA → test-preventable subset → regression suite gap
  cross-check vs pi/docs/regression-suite-map.json. Tracks open vs closed coverage
  gaps to trend incoming PIs lower. Writes pi/reports/leakage-coverage-funnel-YYYY-MM-DD.md.
  Run Fridays 14:00 IST with pi-rca-reduction-brief.
---

# PI Leakage coverage funnel

## Location in repo

`pi/skills/pi-leakage-coverage-funnel/` → symlink `.cursor/skills/pi-leakage-coverage-funnel`.

## Goal

Measure **where bugs leaked** and whether **regression / UAT coverage** could have caught them — the feedback loop for trending incoming PIs lower.

| This skill does | This skill does **not** |
| --- | --- |
| Funnel: Leakage RCA → test-preventable → module → regression gap | Replace per-PI `pi-leakage-rca` drafts |
| Cross-check gaps against `regression-suite-map.json` (Develop) | Require complete dev impact matrix |
| Cross-ref `uat-evidence-review-*.json` when present | Infer Leakage when Jira dropdown empty |
| Recurring open-gap list for automation lead | Add tests automatically |

**Test-preventable leakage** (default cohort filter): `Legacy Code Fix`, `New Code Fix`.

Pair with **`pi-rca-reduction-brief`** — Dev RCA failure-mode clusters on the same Friday slot.

## Schedule

| Item | Value |
| --- | --- |
| **Cadence** | **Fridays 14:00 IST** (with `pi-rca-reduction-brief`) |
| **First run (2026-07-10)** | **Last 30 days entered UAT** |
| **Subsequent Fridays** | **Last 7 days entered UAT** |
| **Chat** | `pi-leakage-coverage-funnel` |
| **Output** | `pi/reports/leakage-coverage-funnel-YYYY-MM-DD.md` |
| **Stable alias** | `pi/reports/leakage-coverage-funnel.md` |

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
python3 pi/scripts/regression_suite_map.py   # or wait for Thu cron
```

## Commands

```bash
# Default: last 30 days entered UAT
python -m scripts.jira_automation leakage-coverage-funnel

# Last 7 days entered UAT (normal Friday cron after first run)
python -m scripts.jira_automation leakage-coverage-funnel --window 7d

# As-of date
python -m scripts.jira_automation leakage-coverage-funnel --as-of YYYY-MM-DD --window mtd
```

Double-click: `pi/Run PI Incoming PI Reduction (Friday).command` (runs both funnel + Dev RCA brief).

## Funnel stages

1. PIs that **entered UAT** in window
2. **Leakage RCA** filled on Jira
3. **Test-preventable** leakage category
4. **Module inferred** from summary + Dev RCA text
5. **Gap confirmed** — missing Develop regression and/or UAT review flagged gap
6. **Gap still open** — test not in current regression map

## Output sections

```markdown
Subject: PI Leakage Coverage Funnel — YYYY-MM-DD — N gaps · M open in suite

# PI Leakage Coverage Funnel — YYYY-MM-DD

## Funnel
## Leakage path distribution
## Module × leakage
## Recurring open gaps (Develop suite)
## Per-PI — regression gap confirmed
## Action items
## Per-PI detail (test-preventable leakage)
```

## Quality bar

- **Do not** infer Leakage RCA from comments when dropdown is empty.
- **Do** link every PB key to Jira.
- **Do** cite regression map commit in header.
- Recurring gaps with count ≥ 2 are the automation-lead agenda.

## Related

- **`pi-rca-reduction-brief`** — Dev RCA failure-mode clusters (same Friday job)
- **`pi-uat-evidence-review`** — per-PI UAT evidence vs benchmarks
- **`pi-regression-map`** — benchmark source (refresh Thu 10:30)
- **`pi-uat-weekly-report`** — weekly UAT rollup (Fri 11:00)
- CLI: `leakage-coverage-funnel` in `jira/scripts/jira_automation/__main__.py`
