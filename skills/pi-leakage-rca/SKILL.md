---
name: pi-leakage-rca
description: >-
  Draft or validate Leakage RCA dropdown for a PB PI (customfield_11345). Classifies
  why the issue leaked for PM trends and prevention steering. Writes paste-ready draft
  under pi/ops/drafts/. Does not auto-update Jira unless human explicitly asks to apply.
---

# PI Leakage RCA (Jira field)

## Location in repo

Stored under `pi/skills/pi-leakage-rca/`. Symlink only (no copy) to `.cursor/skills/pi-leakage-rca` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Assign or validate **Leakage RCA** on Jira (`customfield_11345`) — the **single-select leakage category** for PM trends, the **→ In QA gate**, and **`pi-prevention-pack`** steering. Not the engineering narrative in **Dev RCA**.

**Leakage RCA** answers: *Why did this issue exist at all / what caused it to leak?* — not test-gap labels, performance tags, or free-text fix descriptions.

## Jira fields

| Display name | Field ID | Type | Gate? |
| --- | --- | --- | ---: |
| **Leakage RCA** | `customfield_11345` | Single-select (12 options) | **Yes** — required before → **In QA** (when validator live) |
| Leakage RCA - old | `customfield_10940` | Text (legacy) | No — hidden from forms; audit only |

Constants: `FIELD_LEAKAGE_RCA`, `FIELD_LEAKAGE_RCA_OLD`, `LEAKAGE_RCA_OPTIONS` in `jira/scripts/jira_automation/pi_config.py`.

## Dropdown values (exact labels only)

Use **one** of these twelve — spelling and casing must match Jira:

1. Legacy Code Fix  
2. New Code Fix  
3. New Requirement  
4. Not an Issue  
5. Configuration Update  
6. Legacy Architecture  
7. Legacy Data Fix  
8. Data Issue  
9. By Design  
10. Feed Issue  
11. Gap in Requirement  
12. Infra Issue  

| Category | Use when |
| --- | --- |
| Legacy Code Fix | Regression in old PHP/report path; known fragile area |
| Legacy Architecture | Structural/design debt allowed the failure |
| New Code Fix | Bug in recently shipped code |
| New Requirement | Behavior was never specified |
| Gap in Requirement | Spec/AC gap; partial implementation |
| Configuration Update | Tenant/setup/parameter issue, not product code |
| Legacy Data Fix | Historical data model / migration issue |
| Data Issue | Bad source data or manual entry |
| Feed Issue | Ingestion, feed mapping, batch job |
| Infra Issue | Platform, vendor, timeout, scale constraints |
| By Design | Documented behavior; not a defect |
| Not an Issue | Invalid report / duplicate / cannot reproduce |

**Do not** use retired free-text labels (Missing Test Scenario, Performance Issue, Change Request, etc.) — map to the closest option above.

## When to run

- PI in **In Progress** — **before** transition to **Verification on UAT** (`In QA`).
- **`pi-daily-ops-report`** flags missing Leakage RCA on post-eng PIs.
- Human: *"classify Leakage RCA for PB-xxxx"*.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Fetch from Jira (mandatory)

Use Jira REST API via `JiraClient` or equivalent:

```python
from scripts.jira_automation.client import JiraClient
from scripts.jira_automation import pi_config as c

client = JiraClient()
issue = client.get(
    f"/issue/PB-xxxx",
    params={"fields": f"summary,status,{c.FIELD_DEV_RCA},{c.FIELD_LEAKAGE_RCA}"},
)
fields = issue["fields"]
leakage = fields.get(c.FIELD_LEAKAGE_RCA)
# select field → {"value": "Legacy Code Fix", ...} or None
current = leakage.get("value") if isinstance(leakage, dict) else leakage
```

Optional: read **Leakage RCA - old** (`10940`) for historical context only — **never** write to it.

## Inputs and outputs

| | Path |
| --- | --- |
| Read | Jira: `customfield_11345`, `customfield_10935`, summary, status |
| Read (if present) | `pi/specs/{ItemId}.md`, `pi/similar/{ItemId}.md` |
| Write | `pi/ops/drafts/{ItemId}-leakage-rca.md` |

## Jira writes (default vs apply)

| Mode | Behavior |
| --- | --- |
| **Draft (default)** | `pi/ops/drafts/{ItemId}-leakage-rca.md` — human sets Jira **Leakage RCA** dropdown |
| **Apply** | Only if human says *"apply Leakage RCA to Jira"* → `PUT /rest/api/3/issue/{key}` with select payload |

**Apply payload (dropdown):**

```json
{
  "fields": {
    "customfield_11345": { "value": "Legacy Code Fix" }
  }
}
```

Use exact label from `LEAKAGE_RCA_OPTIONS`. Do **not** write to `customfield_10940`.

## Workflow

1. Resolve `{ItemId}` as **`PB-*`**; run `ping`.
2. Fetch Jira fields for `{ItemId}` (see above).
3. If **Leakage RCA** (`11345`) already set and human did not ask to reclassify → note current value and exit.
4. Read Dev RCA, spec fix outcome, `pi/similar/` (sibling patterns → often **Legacy Code Fix**).
5. Choose **one** option from the twelve; document rationale in draft only.
6. Write draft; remind human both **Dev RCA** and **Leakage RCA** are required before **→ In QA** (Verification on UAT).
7. If Leakage is **By Design** or **Not an Issue** → note that **`pi-prevention-pack`** will skip PM issues.

## Template — `pi/ops/drafts/{ItemId}-leakage-rca.md`

```markdown
# Leakage RCA draft — {ItemId}

**Jira:** https://assetvantage.atlassian.net/browse/{ItemId}
**Status:** {status}
**Current Leakage RCA (dropdown):** {empty | value}
**Dev RCA (reference):** {snippet or empty}
**Legacy Leakage RCA - old:** {value or —} *(read-only context)*

## Paste into Jira → Leakage RCA (dropdown)

{single label from LEAKAGE_RCA_OPTIONS}

## Rationale (not pasted)

{1–3 sentences — why it leaked, not how it was fixed}

## Gate

Required with Dev RCA before move to **Verification on UAT** (In QA).

## Apply (optional)

Human must say "apply Leakage RCA to Jira".
PUT `customfield_11345` with `{"value": "<exact label>"}`.
```

## Do not

- Write to **Leakage RCA - old** (`10940`).
- Confuse with **Dev RCA** (`customfield_10935`).
- Invent labels outside `LEAKAGE_RCA_OPTIONS`.
- Use free-text categories from pre-migration Monday imports on new transitions.

## Related

- **`pi-dev-rca`** (pair before → In QA)
- **`pi-prevention-pack`** (post-close; uses Leakage RCA to steer prevention)
- **`pi-daily-ops-report`**
- Runbook: `current/pi/docs/rca-gate-implementation.md`
