---
name: pi-debug-playbook
description: >-
  PI lead debugging: generate breakpoint playbook from spec hypotheses, log debug
  sessions, and write your RCA compared to Jira Dev RCA (developers fill that field).
  Modes generate / session / conclude. Writes pi/ops/debug/{KEY}-*.md. On demand after intake.
---

# PI debug playbook (your RCA via debugging)

## Location in repo

Stored under `pi/skills/pi-debug-playbook/`. Symlink only (no copy) to `.cursor/skills/pi-debug-playbook` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Support **your** independent debugging and RCA — **not** drafting Jira Dev RCA for developers.

| Actor | Responsibility |
| --- | --- |
| **Developers** | Fix + fill Jira **Dev RCA** (`customfield_10935`) |
| **You** | Debug on HC UAT / SQL / API; record **your RCA**; compare at Friday RCA sync |

This skill is **not** a gate before `pi-dev-rca`. Run **`pi-dev-rca`** only if you want a paste draft for someone else.

## Modes (one skill, three triggers)

| Mode | Chat prompt | Writes |
| --- | --- | --- |
| **generate** | `pi-debug-playbook generate PB-xxxx` | `pi/ops/debug/{ItemId}-playbook.md` |
| **session** | `pi-debug-playbook session PB-xxxx` | `pi/ops/debug/{ItemId}-session-YYYY-MM-DD.md` |
| **conclude** | `pi-debug-playbook conclude PB-xxxx` | `pi/ops/debug/{ItemId}-my-rca.md` + spec `## Debug status` |

Default if mode omitted: **generate** when no playbook exists; **session** when human pastes debug results; **conclude** when human asks for verdict.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

Requires `pi/specs/{ItemId}.md` with `## Root cause hypothesis` and `## Fast elimination plan`.

## Mandatory reads

1. `pi/specs/{ItemId}.md` — hypotheses, elimination plan, HC UAT URL, cross-cutting matrix
2. `pi/docs/jira-pi-board-status.md`
3. If present: `pi/business-impact/{ItemId}.md`, `pi/evidence-analysis/{ItemId}.md`, `pi/similar/{ItemId}.md`
4. Skim cited `path:line` in spec — expand into breakpoints (do not invent paths not in spec unless repo search confirms)

## Paths

| Artifact | Path |
| --- | --- |
| Playbook | `pi/ops/debug/{ItemId}-playbook.md` |
| Session log | `pi/ops/debug/{ItemId}-session-YYYY-MM-DD.md` (IST date) |
| Your RCA | `pi/ops/debug/{ItemId}-my-rca.md` |
| Evidence (optional) | `pi/ops/debug/{ItemId}-evidence/` |
| Spec pointer | `pi/specs/{ItemId}.md` → `## Debug status` |

Edit only under `pi/`. Do not modify application code. Do not write Jira Dev RCA unless human explicitly asks to compare only (read via API).

## Breakpoint layers (L0–L6)

Use only layers that **differentiate hypotheses**:

| Layer | What | Examples |
| --- | --- | --- |
| **L0** | HC UAT reproduction | Login, entity, period, vehicle; symptom visible? |
| **L1** | UI / network | Request URL, payload, response JSON |
| **L2** | PHP / API entry | Controller action, report service method |
| **L3** | Calc / transform | PHP calculation class or lambda handler |
| **L4** | Persistence | SQL on tables named in spec (entityid, txn id, position id) |
| **L5** | Product debug artifact | PAR / PPR / MPPR debug file from UI (see `pi/user_manual/`) |
| **L6** | Logs | `feedprocesslog`, app log grep by txn/report id |

### Module → default layer hints

| Module / symptom | Start layers |
| --- | --- |
| PAR / PPR / MPPR / Beta | L5, L1, L3 (`PerformanceApiReport/`, tourbillon) |
| Report Book widgets | L1, L2 (`format.service.ts`, dashboard API) |
| GL / ledger | L4 (`ledgerentry`, `bankcash`), L2 (`AVBankcashTransaction`) |
| Feeds / Plaid | L6, L4 duplicate keys, ingestion path |
| Transactions upload | L2 upload controller, L4 voucher/ledger post-save |
| Look-through / MF DE | L3 tourbillon, VR ISIN linkage |

## Mode: generate

1. Read spec hypotheses (H1, H2, …) and fast elimination plan.
2. For each hypothesis, add breakpoint rows: Layer, location (`path:line` or SQL/API), what to capture, branch rule (`if A → H1`, `else → H2`).
3. Map elimination plan checks 1–3 to the first playbook rows (5 / 10 / 15 min).
4. Add **L0** HC UAT steps from `## Reproduction / symptoms`.
5. Write `pi/ops/debug/{ItemId}-playbook.md` (template below).
6. Add or update **`## Quick links by audience`** and **`## Debug status`** in spec (see intake checklist in `pi-intake-impact-fix-spec`).

## Mode: session

1. Read existing playbook.
2. Human provides results (paste SQL output, API JSON, UI observation, debug file snippet) OR agent runs checks when credentials/DB access available.
3. Write `pi/ops/debug/{ItemId}-session-YYYY-MM-DD.md` — fill **Actual** and **Hypothesis impact** per check.
4. Update spec `## Debug status`: last session date, leading hypothesis or *inconclusive*.

Do **not** use "verify manually" without a concrete artifact. Every row needs an auditable output (row count, JSON field, log line).

## Mode: conclude

1. Read playbook + latest session(s).
2. Fetch Jira **Dev RCA** and **Leakage RCA** (read-only):

```python
from scripts.jira_automation.client import JiraClient
from scripts.jira_automation import pi_config as c

issue = JiraClient().get(
    f"/issue/{ItemId}",
    params={"fields": f"summary,status,{c.FIELD_DEV_RCA},{c.FIELD_LEAKAGE_RCA}"},
)
```

3. Write `pi/ops/debug/{ItemId}-my-rca.md` — your confirmed RCA + **Alignment** vs Jira Dev RCA.
4. Update spec `## Debug status`: verdict, link to my-rca, alignment (Match / Partial / Disagree).

If no hypothesis confirmed → state **inconclusive** and list next checks; do not fabricate RCA.

## Template — playbook

```markdown
# Debug playbook — {ItemId}

**Summary:** {one line from spec}
**HC UAT:** {clickable link from spec}
**Spec:** [pi/specs/{ItemId}.md](../../specs/{ItemId}.md)
**Generated (IST):** YYYY-MM-DD HH:MM

## Hypotheses (from spec)

| ID | One-line | Confidence (intake) |
|----|----------|---------------------|
| H1 | … | high/medium/low |

## Breakpoints

| Check | Hyp | Layer | Location | Capture | Expected branch |
|-------|-----|-------|----------|---------|-----------------|
| 1 (5m) | H1 | L4 | `SELECT entityid FROM ledgerentry WHERE …` | row entityids | mixed 401/501 → **H1** |
| 2 (10m) | H3 | L0 | HC UAT entity-only filter 401 | screenshot / note | gone → **H3** |

## Elimination order

Run checks 1 → N in table order; stop early if one hypothesis is clearly confirmed.

## Evidence folder

Optional captures: `pi/ops/debug/{ItemId}-evidence/`
```

## Template — session

```markdown
# Debug session — {ItemId} — YYYY-MM-DD

**Environment:** HC UAT · **Duration:** ~N min
**Playbook:** [pi/ops/debug/{ItemId}-playbook.md]({ItemId}-playbook.md)

| Check | Planned | Actual | Hypothesis impact |
|-------|---------|--------|-------------------|
| 1 | … | … | H1 strengthened / H2 ruled out |

## Notes

…

## Next session

…
```

## Template — my-rca

```markdown
# My RCA — {ItemId}

**As-of (IST):** YYYY-MM-DD
**Jira:** https://assetvantage.atlassian.net/browse/{ItemId}
**Status:** {from Jira}

## My RCA (debug-confirmed)

**Cause:** …
**Evidence:** … (cite session artifacts)
**Ruled out:** H2 (…), H3 (…)

## Jira Dev RCA (developer)

{quote or *empty*}

## Leakage RCA (Jira)

{value or *empty*}

## Alignment

**Match / Partial / Disagree** — …

## Friday RCA sync (30 sec)

…
```

## Spec sections (add/update in `pi/specs/{ItemId}.md`)

```markdown
## Quick links by audience

- **Executive:** [business impact](../business-impact/{ItemId}.md) · HC UAT in metadata
- **Manager sync:** [Jira](https://assetvantage.atlassian.net/browse/{ItemId}) · [similar](../similar/{ItemId}.md)
- **Your debug:** [playbook](../ops/debug/{ItemId}-playbook.md) · [my RCA](../ops/debug/{ItemId}-my-rca.md)
- **Engineering:** hypotheses below · [test plan](../test-plans/{ItemId}.md)

## Debug status

| Field | Value |
|-------|-------|
| Playbook | [pi/ops/debug/{ItemId}-playbook.md](../ops/debug/{ItemId}-playbook.md) |
| Last session | YYYY-MM-DD or — |
| My RCA | [pi/ops/debug/{ItemId}-my-rca.md](../ops/debug/{ItemId}-my-rca.md) or *pending* |
| vs Jira Dev RCA | Match / Partial / Disagree / — |
```

Omit broken links — if `business-impact` or `test-plans` file missing, omit that bullet.

## Quality bar

- Every breakpoint ties to a **hypothesis** or elimination check from the spec.
- No generic "investigate module" — name boundary (API, join, filter, entity scope).
- Branch rules must be **falsifiable** with a named artifact.
- **Disagree** with Jira Dev RCA is valid output — document why with evidence.

## Related

- Intake hypotheses: **`pi-intake-impact-fix-spec`**
- Business context: **`pi-business-impact`**
- Friday rollup: **`pi-friday-rca-sync`**
- Developer Jira draft (optional): **`pi-dev-rca`**
