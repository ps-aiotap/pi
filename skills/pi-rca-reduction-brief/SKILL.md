---
name: pi-rca-reduction-brief
description: >-
  Friday leads meeting brief: cluster Jira Dev RCA narratives (both RCA filled) by
  failure mode, flag recurrences, similar-pis history, and reduction levers. Not
  preventability rules or test-plan docs. Writes pi/reports/rca-reduction-brief-YYYY-MM-DD.md.
  Run every Friday IST.
---

# PI RCA reduction brief

## Location in repo

Stored under `pi/skills/pi-rca-reduction-brief/`. Symlink only (no copy) to `.cursor/skills/pi-rca-reduction-brief` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Prepare the **Friday meeting with leads on reducing incoming PIs** by analyzing **what actually broke** — not executive preventability rollups.

| This skill does | This skill does **not** |
| --- | --- |
| Read **Jira Dev RCA** + **Leakage RCA** (both filled) | Use `mtd-preventability` preventable flags |
| Cluster by **failure mode** from Dev RCA text | Count cross-cutting sections in test plans |
| Flag **duplicate Dev RCA** (same root cause, multiple tickets) | Infer Leakage when Jira dropdown is empty |
| `similar-pis` on cluster representatives for **historical repeats** | Replace per-PI `pi-dev-rca` / `pi-leakage-rca` drafts |

**Leakage RCA** informs context; **reduction levers** come from **Dev RCA narratives** and recurrence evidence.

## Schedule

| Item | Value |
| --- | --- |
| **Cadence** | **Fridays 14:00 IST** (cron `pi-incoming-pi-reduction-friday`) |
| **First run (2026-07-10)** | **Last 30 days entered UAT** (`--window 30d`) |
| **Subsequent Fridays** | **Last 7 days entered UAT** (`--window 7d`) |
| **Chat** | `pi-rca-reduction-brief` |
| **Output** | `pi/reports/rca-reduction-brief-YYYY-MM-DD.md` |
| **Stable alias** | `pi/reports/rca-reduction-brief.md` |

Runs with **`pi-leakage-coverage-funnel`** in the same Friday job. Pair with **`pi-friday-rca-sync`** (your debug RCA vs Jira) — different audience and method.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Commands

```bash
# Default: last 30 days entered UAT
python -m scripts.jira_automation rca-reduction-brief

# Last 7 days entered UAT (normal Friday cron after first run)
python -m scripts.jira_automation rca-reduction-brief --window 7d
```

Double-click: `pi/Run PI RCA Reduction Brief.command`

## Cohort (default)

1. PIs that **entered UAT** (`In QA` / `In_UAT`) in window (default **30d**; `--window 7d` on recurring Fridays)
2. **Both** on Jira: Dev RCA (`customfield_10935`) + Leakage RCA (`customfield_11345`) — required at UAT gate
3. **Analyzable** = substantive Dev RCA (excludes `"Code Fix"`, &lt;25 chars, etc.)
4. Includes **fixed and in-flight** — recurrence while Verify Prod is high-signal

Human can narrow: *"rca reduction brief --window 7d"* or *"skip similar for speed"*.

## Workflow

1. Run CLI (or chat this skill) — `rca_reduction_brief.build_report()`.
2. Review report sections in order:
   - **Recurrence** — duplicate Dev RCA pairs (second PI should not have arrived)
   - **Failure-mode clusters** — reduction lever per cluster, owner teams
   - **Historical repeats** — similar PIs outside cohort (score ≥50)
   - **Weak Dev RCA** — backfill before close
   - **In-flight** — forward risk
3. In the meeting: one **ask per cluster**, not leakage pie charts.
4. Optional follow-up: `pi-prevention-pack` for top hotspot per cluster.

## Cluster registry

Pattern rules live in `jira/scripts/jira_automation/rca_reduction_brief.py` → `CLUSTER_RULES`. Extend when a new failure mode repeats (e.g. bank recon stale cache, multidist orphan temp, feed import scope).

Cross-cutting dimensions: `pi/docs/cross-cutting-impact-dimensions.md` — use when drafting prevention tests after the meeting, not as the primary cluster source.

## Output sections

```markdown
Subject: PI RCA Reduction Brief — YYYY-MM-DD — N analyzable · D recurrence groups

# PI RCA Reduction Brief — YYYY-MM-DD

## Cohort
## Recurrence — duplicate Dev RCA
## Failure-mode clusters
## Historical repeats (similar-pis)
## Weak Dev RCA
## In-flight with both RCAs
## Leads asks
## Per-PI detail (both RCA)
```

## Quality bar

- **Do not** cite `preventable_yes` from `mtd-per-pi-prevention-*.json`.
- **Do not** treat inferred leakage as confirmed for clustering.
- **Do** call out duplicate Dev RCA with both ticket keys and dates.
- **Do** mark weak Dev RCA as blocking reduction work.
- Snippets in tables max **150 chars**; link every key to Jira.

## Related

- **`pi-friday-rca-sync`** — your RCA vs dev, leakage gaps (same Friday slot)
- **`pi-prevention-pack`** — PM Story from confirmed cluster hotspot
- **`pi-similar-pis`** — per-PI deep dive after meeting
- **`pi-daily-executive-preventability`** — exec preventability (different purpose)
- CLI: `rca-reduction-brief` in `jira/scripts/jira_automation/__main__.py`
