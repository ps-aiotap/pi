---
name: pi-dev-rca
description: >-
  Draft or validate Dev RCA for a PB PI (customfield_10935). Reads Jira + pi/spec;
  writes a paste-ready draft under pi/ops/drafts/. Does not auto-update Jira unless
  the human explicitly asks to apply. Required before Verification on UAT (In QA).
---

# PI Dev RCA (Jira field)

## Location in repo

Stored under `pi/skills/pi-dev-rca/`. Symlink only (no copy) to `.cursor/skills/pi-dev-rca` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Produce a **concise, paste-ready Dev RCA** for Jira field **Dev RCA** (`customfield_10935`). Required **before Verification on UAT** (Jira status **`In QA`**) together with **Leakage RCA** (`customfield_11345`). See `current/pi/docs/rca-gate-implementation.md`.

This skill targets the **Jira field**, not the long-form RCA in `pi/specs/{ItemId}.md`. For BA/human enrichment inside the spec, use **`pi-rca-human-enhancement`** instead.

## Jira fields (pair at gate)

| Display name | Field ID | Type | Required on → In QA? |
| --- | --- | --- | ---: |
| Dev RCA | `customfield_10935` | Text (short) | **Yes** |
| Leakage RCA | `customfield_11345` | Single-select | **Yes** |

Constants: `FIELD_DEV_RCA`, `FIELD_LEAKAGE_RCA` in `jira/scripts/jira_automation/pi_config.py`.

## When to run

- PI in **In Progress** — before handoff to **Verification on UAT** (`In QA`).
- **`pi-daily-ops-report`** flags missing Dev RCA on In QA + Verify Prod.
- Human: *"draft Dev RCA for PB-xxxx"*.

Run **`pi-leakage-rca`** for the same PI before → In QA.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Fetch from Jira (mandatory)

```python
from scripts.jira_automation.client import JiraClient
from scripts.jira_automation import pi_config as c

client = JiraClient()
issue = client.get(
    f"/issue/PB-xxxx",
    params={
        "fields": f"summary,status,priority,assignee,{c.FIELD_TEAM},"
        f"{c.FIELD_DEV_RCA},{c.FIELD_LEAKAGE_RCA}"
    },
)
fields = issue["fields"]
dev_rca = fields.get(c.FIELD_DEV_RCA)
leakage = fields.get(c.FIELD_LEAKAGE_RCA)
leakage_val = leakage.get("value") if isinstance(leakage, dict) else leakage
```

## Inputs and outputs

| | Path |
| --- | --- |
| Read | Jira issue `PB-*` (summary, status, Dev RCA, Leakage RCA, Team) |
| Read (if present) | `pi/specs/{ItemId}.md` — `## RCA - System Generated`, consolidated RCA, fix summary |
| Write | `pi/ops/drafts/{ItemId}-dev-rca.md` |
| Optional log | `pi/docs/process-log.md` one line |

Edit only under `pi/` (and read Jira via API). Do not modify application code.

## Jira writes (default vs apply)

| Mode | When | Behavior |
| --- | --- | --- |
| **Draft (default)** | Always unless human opts in | Write `pi/ops/drafts/{ItemId}-dev-rca.md`; human copies into Jira **Dev RCA** |
| **Apply** | Human says *"apply Dev RCA to Jira"* | `PUT /rest/api/3/issue/{key}` with `{ "fields": { "customfield_10935": "<text>" } }` only after human approves draft |

Do **not** apply to Jira on a routine run. Confirm draft with human first.

## Workflow

1. Resolve `{ItemId}` as **`PB-*`**; run `ping`.
2. Fetch from Jira (see above).
3. If Jira **Dev RCA** is already non-empty and human did not ask for refresh → report *already set*; optionally suggest edits only if spec contradicts.
4. Read `pi/specs/{ItemId}.md` if present; distill **root cause** (not reproduction steps). Treat spec RCA as **hypothesis** if fix is now confirmed in Jira/comments.
5. Write **`pi/ops/drafts/{ItemId}-dev-rca.md`** using template below.
6. Tell human: paste into Jira → **Dev RCA**, then set **Leakage RCA** (`pi-leakage-rca`), then move to **Verification on UAT** (In QA).

## Dev RCA content rules

- **2–5 sentences** or **3–5 bullets** — fits Jira text field (~255 char limit if still enforced); no code dumps.
- State **what broke** (behavior), **why** (cause class: logic, config, data, regression, requirement gap), **where** (module/report area in plain language).
- If fix is tactical vs structural, say so in one line.
- Align status language with `pi/docs/jira-pi-board-status.md`.
- No placeholders: **TBD**, **N/A**, **pending**.

## Template — `pi/ops/drafts/{ItemId}-dev-rca.md`

```markdown
# Dev RCA draft — {ItemId}

**Jira:** https://assetvantage.atlassian.net/browse/{ItemId}
**Status:** {status} · **Priority:** {priority}
**Current Jira Dev RCA:** {empty | quote existing}
**Leakage RCA:** {empty | value}

## Paste into Jira → Dev RCA

{proposed text — single block human can copy}

## Source

- Spec: pi/specs/{ItemId}.md (sections used: …)
- Jira fetched: {ISO date}

## Gate

Pair with **Leakage RCA** before → **Verification on UAT** (In QA).

## Apply (optional)

Human must say "apply Dev RCA to Jira" to write via API.
PUT `customfield_10935` with plain text string.
```

## Do not

- Replace or delete RCA sections in `pi/specs/{ItemId}.md`.
- Run intake, code-fix, or test skills as part of this step.
- Use Dev RCA in JQL filters until admin enables search (`ENABLE_DEV_RCA_JQL_FILTERS` in `pi_config.py`).

## Related

- **Your debug RCA:** **`pi-debug-playbook`** → `pi/ops/debug/{ItemId}-my-rca.md` (compare to Jira below)
- Leakage category: **`pi-leakage-rca`** (required pair before → In QA)
- Post-close prevention: **`pi-prevention-pack`**
- ETA: **`pi-eta`**
- Daily gaps list: **`pi-daily-ops-report`**
- Runbook: `current/pi/docs/rca-gate-implementation.md`
