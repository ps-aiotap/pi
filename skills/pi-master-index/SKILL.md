---
name: pi-master-index
description: >-
  Cumulative index of all analyzed PIs: key, summary, status, client, HC UAT, and
  links to spec, business impact, debug playbook, similar PIs, test plans. Writes
  pi/reports/pi-master-index.md. On demand or after intake batches.
---

# PI master index

## Location in repo

Stored under `pi/skills/pi-master-index/`. Symlink only (no copy) to `.cursor/skills/pi-master-index` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

One **bookmarkable catalog** of every PI with analysis artifacts — not a per-run intake summary.

| Artifact | Scope |
| --- | --- |
| `intake-summary-YYYY-MM-DD.md` | Single batch run |
| **`pi-master-index.md`** | All keys with `pi/specs/{KEY}.md` (+ optional Jira live status) |

## When to run

- After an intake batch completes
- On demand: `pi-master-index` or `pi-master-index refresh`
- Weekly (optional) to refresh board column from Jira

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping   # optional but preferred for live status
```

## Workflow

1. **Discover keys:** list `pi/specs/PB-*.md` and `pi/specs/PI-*.md` (exclude `README.md`, `pi.csv`).
2. For each key, read spec metadata (summary, board column, HC UAT URL) from file.
3. **Optional Jira refresh:** for each `PB-*` key, fetch `summary`, `status` via API; map status to board column per `pi/docs/jira-pi-board-status.md`.
4. **Link columns** — file exists or `—`:

| Column | Path pattern |
| --- | --- |
| Spec | `pi/specs/{KEY}.md` |
| Business impact | `pi/business-impact/{KEY}.md` |
| Debug playbook | `pi/ops/debug/{KEY}-playbook.md` |
| My RCA | `pi/ops/debug/{KEY}-my-rca.md` |
| Similar | `pi/similar/{KEY}.md` |
| Test plan | `pi/test-plans/{KEY}.md` |

5. Sort: `PB-*` by numeric key desc (newest first); `PI-*` legacy block below or separate section.
6. Write `pi/reports/pi-master-index.md` and optional `pi/reports/pi-master-index.json`.
7. Append one line to `pi/docs/process-log.md`.

## Outputs

| Artifact | Path |
| --- | --- |
| Markdown index | `pi/reports/pi-master-index.md` |
| JSON (optional) | `pi/reports/pi-master-index.json` |

## Template

```markdown
# PI master index

**Generated (IST):** YYYY-MM-DD HH:MM
**PIs indexed:** N (PB: n1 · PI legacy: n2)
**Jira status:** live API / spec metadata only

## Open PB (four board columns) — quick view

| Key | Summary | Column | Priority | HC UAT | Spec | Business | Debug | My RCA | Similar |
|-----|---------|--------|----------|--------|------|----------|-------|--------|---------|
| PB-xxxx | … | IN DEVELOPMENT | Critical | [hc…](https://…) | [spec](../specs/PB-xxxx.md) | — | [playbook](../ops/debug/PB-xxxx-playbook.md) | — | [similar](../similar/PB-xxxx.md) |

## All PB

(same table, all PB-* specs)

## Legacy PI (Monday)

(same columns for PI-* keys if any)
```

Use `—` for missing artifacts; do not link to non-existent files.

## Audience quick-links

The index **is** the navigation hub. Per-PI **`## Quick links by audience`** in specs (from `pi-debug-playbook generate` or intake) deep-link to the same paths.

## Related

- Batch intake table: **`pi-intake-impact-fix-spec`** → `intake-summary-*.md`
- Ops queues: **`pi-daily-ops-report`**, dashboard HTML
- Meeting briefs: **`pi-meeting-brief`**
