---
name: pi-monthly-ageing
description: >-
  Generates the monthly PI ageing report for Jira PB board 774. Counts only four
  open columns (INCOMING BUGS, In Engineering Queue, IN DEVELOPMENT, Reopened),
  buckets by days since created, writes JSON and markdown for retro. Use on the
  1st of the month, for monthly PI retro, ageing, backlog age, or board 774 open counts.
---

# PI monthly ageing (board 774)

## Location in repo

Stored under `pi/skills/pi-monthly-ageing/`. Symlink only (no copy) to `.cursor/skills/pi-monthly-ageing` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Produce a **repeatable monthly ageing snapshot** for leadership retro. **Open** means only these four [board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774) columns — **not** In QA, Verify Prod, Watchlist, BA, or Closed:

| Board column | Jira status |
| --- | --- |
| INCOMING BUGS | To Do |
| In Engineering Queue | In Review |
| IN DEVELOPMENT | In Progress |
| Reopened | On Hold/Reopened - Dev Team |

This is **narrower** than `PI — Ops — Open Engineering` (six statuses). Do not mix the two definitions in one report.

## When to run

- **1st of each month** (or last business day of the prior month) as part of monthly retro.
- After major queue changes when leadership asks for current ageing.
- Invoke explicitly: `@pi/skills/pi-monthly-ageing` or *"run PI monthly ageing"*.

Pair with **PI — Monthly Retro** dashboard ([dashboard 10068](https://assetvantage.atlassian.net/jira/dashboards/10068)) for created/closed volume; this skill covers **age of open backlog**.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping   # must succeed
```

## Command

From `jira/` repo root:

```bash
python -m scripts.jira_automation ageing
python -m scripts.jira_automation ageing --as-of 2026-05-31   # month-end snapshot
```

## Outputs

| Artifact | Path |
| --- | --- |
| JSON (full issue list + buckets) | `jira/output/pi_ageing_YYYY-MM.json` |
| Markdown (retro / deck table) | `jira/output/pi_ageing_YYYY-MM.md` |

Age buckets: **0–30d**, **31–60d**, **61–90d**, **91+d** (days since `created`, as-of run date).

## Agent workflow

1. Confirm `jira/.env` credentials (`ping`).
2. Run `ageing` (use `--as-of` with last day of prior month if retro is on the 1st).
3. Read `jira/output/pi_ageing_YYYY-MM.md` — summarize **total open**, **91+d count**, **oldest 5 keys**, **by column**.
4. Compare to prior month file in `jira/output/pi_ageing_*.json` if present (month-over-month trend).
5. Optional: open saved filter **`PI — Ageing — Open (4 columns)`** in Jira to validate counts.

## Do not

- Use **Average Age Chart** or **Aging Chart** gadgets (unavailable or misleading on this site — see `jira/docs/PI_REPORTING_DELIVERABLES.md`).
- Count **Open Engineering** (six statuses) when the ask is **ageing open** — use this skill’s four-column definition only.

## Related

- Runbook: `jira/docs/PI_REPORTING_DELIVERABLES.md` (Phase 5 — monthly retro)
- JQL/constants: `jira/scripts/jira_automation/pi_config.py` (`OPEN_AGEING_STATUSES`, `jql_open_ageing()`)
- Board columns: `pi/docs/jira-pi-board-status.md`
