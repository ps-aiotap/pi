---
name: pi-executive-narrative
description: >-
  Executive sync narrative: MTD/week counts from pi-executive-weekly-report plus top
  open Critical PIs with business one-liners. Writes pi/reports/executive-narrative-YYYY-MM-DD.md.
  Run Mon and Thu ~9 AM IST or on demand.
---

# PI executive narrative

## Location in repo

Stored under `pi/skills/pi-executive-narrative/`. Symlink only (no copy) to `.cursor/skills/pi-executive-narrative` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Support **2×/week executive sync** with **volume + story**:

1. Reuse metrics from **`pi-executive-weekly-report`** (do not reimplement JQL)
2. Add **top open Critical / Business Critical** PIs with business impact one-liners

Does **not** replace `pi/reports/executive-weekly.md` — **appends** a narrative section in a separate file (or combined if human asks).

## Schedule

| Item | Value |
| --- | --- |
| **Cadence** | **Monday + Thursday** ~9:00 AM IST (2×/week exec sync) |
| **Chat** | `pi-executive-narrative` |
| **Prerequisite** | Run `executive-weekly-report` same day or copy table from `executive-weekly.md` |

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
python -m scripts.jira_automation executive-weekly-report   # if counts stale
```

## Workflow

1. Read `pi/reports/executive-weekly.md` (or dated archive) — copy summary table into narrative file.
2. JQL / fetch open PIs in four columns with priority Critical or Business Critical (max **7** rows).
3. For each: business one-liner from `pi/business-impact/{KEY}.md` or spec summary; board column; ETA if any.
4. Optional: one sentence on **resolved this week** highlight (highest priority closed, if human cares).
5. Write `pi/reports/executive-narrative-YYYY-MM-DD.md`.

## Output template

```markdown
Subject: PI Executive — YYYY-MM-DD — {MTD reported} reported MTD · {N} critical open

# PI Executive Narrative — YYYY-MM-DD

## Volume (from executive weekly)

| Metric | Month (MTD) | This week |
| --- | ---: | ---: |
| PIs reported | | |
| Total resolved | | |
| Reported & resolved | | |
| Planned (next week) | — | |
| Planned (by EOM) | | — |

## Critical open — business view

| Key | Summary | Column | Client pain | ETA |
|-----|---------|--------|-------------|-----|
| PB-xxxx | … | IN DEVELOPMENT | … | — |

## Talking points (3 bullets max)

1. …
2. …
3. …

_Source: pi/reports/executive-weekly.md · IST as-of YYYY-MM-DD_
```

## Quality bar

- Business view table max **7** rows
- Talking points are **outcomes**, not technical hypotheses
- If `pi-business-impact` missing, note *impact doc pending* and use spec summary

## Related

- **`pi-executive-weekly-report`** — counts only (keep unchanged)
- **`pi-business-impact`** — improves client pain column
- **`pi-meeting-brief`** — manager-level detail
