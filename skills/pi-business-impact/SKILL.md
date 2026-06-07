---
name: pi-business-impact
description: >-
  Optional PI skill: plain-language business impact and domain primer for learning
  and developer handoff. Writes pi/business-impact/{KEY}.md and a short spec section.
  Skip when pi/docs/pi-pipeline-config.md has business_impact false or human asks to skip.
---

# PI business impact explainer (optional)

## Location in repo

Stored under `pi/skills/pi-business-impact/`. Symlink or copy to `.cursor/skills/pi-business-impact` at the workspace root for Cursor Agent Skill discovery.

## Goal

For each PI, produce **business-facing impact** and a **domain primer** so that:

1. **You** learn the product faster (`pi/business-impact/{ItemId}.md`).
2. **Developers** see why the fix matters, not only technical blast radius (`## Business impact (for engineering)` in the spec).

This skill is **not** technical impact analysis (code paths, cross-cutting matrix) — that stays in **`pi-intake-impact-fix-spec`** and **`pi-special-cases`**.

## Optional — how to skip

Check **`pi/docs/pi-pipeline-config.md`** before running:

- If `business_impact: false` → **skip** this skill entirely.
- If the human says *"skip business impact"* in chat → skip for that PI only.
- If `pi/specs/{ItemId}.md` does not exist yet → skip (run after intake).

When skipped, do not create placeholder files; optionally note in `pi/docs/process-log.md`: `{ItemId} business-impact skipped (config)`.

## When to run

- **After** **`pi-intake-impact-fix-spec`** and **`pi-similar-pis`** (needs spec + similar PI list).
- **Before** **`pi-special-cases`** (business angle can inform vehicle/sibling emphasis).
- **Default:** on when `business_impact: true` in pipeline config.

## Mandatory reads

1. `pi/specs/{ItemId}.md` (summary, reproduction, priority, client URL, status)
2. `pi/docs/pi-pipeline-config.md` (skip if disabled)
3. `pi/docs/jira-pi-board-status.md` (status/column labels)
4. If present: `pi/similar/{ItemId}.md` (Strong/Related rows for business recurrence)
5. If present: `pi/evidence-analysis/{ItemId}.md` or evidence findings in spec
6. Skim `pi/user_manual/` / `pi/user_manual/av_overview.md` for domain terms only — inline short definitions in output; do not require the reader to open manuals

## Inputs and outputs

| | Path |
|---|---|
| Write (full) | `pi/business-impact/{ItemId}.md` |
| Update | `pi/specs/{ItemId}.md` → section **`## Business impact (for engineering)`** |
| Optional log | `pi/docs/process-log.md` one-line audit |

Edit only under `pi/`. Do not modify application code.

## Workflow (per PI)

1. Read pipeline config; exit if `business_impact: false` or human skip.
2. Read spec and optional similar/evidence artifacts.
3. Write **`pi/business-impact/{ItemId}.md`** using the template below (plain language; no code paths).
4. Add or replace **`## Business impact (for engineering)`** in the spec:
   - Max ~10 lines or a tight bullet list
   - Link: `Full context: pi/business-impact/{ItemId}.md`
5. Do **not** duplicate or replace **`## Impact / blast radius`** (technical) — complementary only.

## Template — `pi/business-impact/{ItemId}.md`

```markdown
# Business impact — {ItemId}

## What the client sees
(1–3 sentences: wrong screen/report/number; no internal module names unless the PI title uses them.)

## Who is affected
- Client / entity (from spec)
- Roles: ops, advisor, tax, client-facing — pick what fits

## Business process at risk
(What workflow is blocked or misleading: month-end, client report pack, tax filing, reconciliation, audit.)

## Domain primer (learn this PI)
(2–4 short bullets: define report/txn/vehicle terms *for this case*, e.g. PAR, transfer in/out, MF vs DE.)

## Why engineering should care
- Decisions made on wrong data
- Priority / prod / client tier if known
- Recurrence: cite Strong/Related similar PIs (key + one line), e.g. MF fixed, DE still broken

## Severity signals
(Priority, status column, prod verification, Critical/Highest — factual from Jira/spec.)

## Open business questions
(What to confirm with reporter; omit if none.)
```

## Spec section template — `## Business impact (for engineering)`

Keep this **short** so devs read it:

```markdown
## Business impact (for engineering)

- **Client pain:** …
- **Process at risk:** …
- **Domain (this PI):** … (one line)
- **Why fix completely:** … (sibling/recurrence if applicable)

Full context: [pi/business-impact/{ItemId}.md](pi/business-impact/{ItemId}.md)
```

## Quality bar

- Plain language; explain acronyms once (PAR, PPS, WR, MF, DE).
- No code paths or file citations in business-impact doc (those belong in technical impact / spec RCA).
- No generic filler (“users may be impacted”) — tie every sentence to this PI’s narrative, client, or similar PI.
- If similar PIs exist, mention at most **3** Strong/Related keys with business consequence, not the full scored list.

## Relationship to other PI skills

| Skill | Overlap |
|-------|---------|
| `pi-intake-impact-fix-spec` | Technical spec + blast radius; this skill adds business layer after intake |
| `pi-similar-pis` | Feeds recurrence / sibling business story |
| `pi-special-cases` | May read `pi/business-impact/{ItemId}.md` when arguing MF+DE scope to humans |
| `pi-rca-human-enhancement` | Optional; human RCA notes — separate from business impact |
