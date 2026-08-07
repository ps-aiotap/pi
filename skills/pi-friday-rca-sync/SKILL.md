---
name: pi-friday-rca-sync
description: >-
  Friday team-lead RCA sync rollup: your debug RCAs vs Jira Dev RCA, leakage gaps,
  alignment disagreements, and prevention themes. Writes pi/reports/friday-rca-sync-YYYY-MM-DD.md.
  Run Fridays on demand.
---

# PI Friday RCA sync

## Location in repo

Stored under `pi/skills/pi-friday-rca-sync/`. Symlink only (no copy) to `.cursor/skills/pi-friday-rca-sync` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Prepare your **Friday PI RCA sync with team leads**:

- **Your RCA** (`pi/ops/debug/{KEY}-my-rca.md`) vs **Jira Dev RCA** (developer-filled)
- Leakage RCA gaps on post-eng PIs
- Themes for recurrence / prevention

Does **not** replace per-PI **`pi-dev-rca`** / **`pi-leakage-rca`** drafts for developers.

## Schedule

| Item | Value |
| --- | --- |
| **Cadence** | Fridays (IST) |
| **Chat** | `pi-friday-rca-sync` |
| **Output** | `pi/reports/friday-rca-sync-YYYY-MM-DD.md` |

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Scope (default)

1. **Open PIs** (four columns) with Critical/High — your active debug agenda
2. **In QA + Verify Prod** — Dev RCA / Leakage RCA missing or alignment review
3. Optional: PIs you debugged this week (`pi/ops/debug/*-session-*.md` dated Mon–Fri IST)

Human can narrow: *"friday rca sync for PB-2956 PB-2965 only"*.

## Workflow

1. Build candidate key list (scope above).
2. For each key:
   - Fetch Jira: Dev RCA (`customfield_10935`), Leakage RCA (`customfield_11345`), status, assignee
   - Read `pi/ops/debug/{KEY}-my-rca.md` if present → Alignment field
   - Read `pi/ops/debug/{KEY}-playbook.md` → inconclusive checks
3. **Aggregate:**
   - **Disagree / Partial** count — discussion list
   - **Missing Dev RCA** on In QA / Verify Prod
   - **Missing Leakage RCA** on Verify Prod
   - **Leakage category histogram** (last 7 days closed if easy from Jira search; else open post-eng only)
4. Write rollup report.

## Output template

```markdown
Subject: PI Friday RCA Sync — YYYY-MM-DD — {N} to review · {D} disagreements

# PI Friday RCA Sync — YYYY-MM-DD

## Agenda summary

- Open critical/high with your debug: …
- Post-eng missing Dev RCA: …
- Post-eng missing Leakage RCA: …
- Your vs Jira disagreements: …

## Discussion table

| Key | Status | Assignee | Jira Dev RCA (snippet) | Your RCA (snippet) | Alignment | Action |
|-----|--------|----------|------------------------|-------------------|-----------|--------|
| PB-xxxx | In Progress | … | … | … | Disagree | Re-run check 2 on HC UAT |

## Inconclusive debug (your side)

| Key | Next check | Owner |
|-----|------------|-------|

## Leakage / prevention themes

- …

## Carry to next week

- …
```

## Quality bar

- Snippets max **80 chars** + "…" — link to full `my-rca.md` and Jira
- **Disagree** rows must cite one evidence line from your session log
- Do not invent developer Dev RCA — fetch or mark *empty*

## Related

- **`pi-debug-playbook`** conclude → `my-rca.md`
- **`pi-daily-ops-report`** — RCA gap counts
- **`pi-prevention-pack`** — after confirmed RCAs
- Gate doc: `pi/docs/rca-gate-implementation.md`
