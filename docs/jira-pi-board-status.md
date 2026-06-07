# Jira PI board — status and columns (PB / board 774)

Source of truth for PI skills when interpreting **where a ticket is in the workflow**.  
Site: `assetvantage.atlassian.net` · project **PB** (PI Board) · kanban board **774**.

## How status works on the board

- The board has **no horizontal swimlanes**; workflow is expressed as **kanban columns**.
- Each column maps to **exactly one Jira workflow status**. Moving a card to another column **updates that issue’s Jira status**.
- For skills and specs, treat the ticket’s **board column** as operational status. When data comes from Jira API or export, use the **column label** in metadata when available; note the underlying Jira status name if it differs (see table below).

Refresh column ↔ status mapping after board admin changes:

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping   # credentials OK first
# Re-fetch via Agile API board/774/configuration (see jira automation or agent runbook)
```

## Column ↔ Jira status (current)

| Board column | Jira status (workflow) | Notes |
|--------------|------------------------|--------|
| Backlog | *(unmapped)* | Backlog column; not a workflow status |
| INCOMING BUGS | To Do | New / triage intake |
| QA REPLICATED | In Review | Replicated or under review |
| IN DEVELOPMENT | In Progress | Active dev |
| On Hold/Reopened - Dev Team | On Hold/Reopened - Dev Team | Paused or reopened |
| IN QA | In QA | QA verification |
| VERIFICATION ON PRODUTION | VERIFICATION ON PRODUTION | Prod verification (spelling as in Jira) |
| Watchlist / Suspended Issues | Watchlist / Suspended Issues | Suspended / watch |
| **BA** | Done *(temporary)* | **Semantic: Change Request** — see below |
| Historical Redmine Issues | Historical Redmine Issues | Legacy import |
| CLOSED | Closed | PI closed on the board |

## BA column = Change Request (not “Done”)

**Product meaning (use in specs and skills):**

- **BA** = **Change Request** stage: **engineering work on this PI ticket is complete** for the reported defect.
- The **PI ticket** is expected to move to **CLOSED** (or equivalent terminal handling).
- **One or more feature / change requests** are created to carry follow-on product work (enhancements, structural fixes, new requirements surfaced during the PI).

**Do not** describe BA as generic Jira **Done** or “ticket finished forever” in narrative. **Done** is the current Jira status name behind the BA column only until workflow is corrected (~1 week).

**When writing specs / acceptance criteria:**

- If status/column is **BA** (Change Request): state that eng fix for the PI is complete; list follow-up feature request(s) if known; separate **PI closure** from **feature delivery**.
- Do not require full product delivery as part of closing the PI unless the human explicitly scoped that.

**Planned Jira change:** Remap the BA column off workflow status **Done** to a dedicated **Change Request** (or equivalent) status. Until then, skills use **BA = Change Request** in prose and map API/export **Done** under BA column to that meaning.

## Issue keys

- New work in Jira uses **`PB-*`** (e.g. `PB-2912`).
- Legacy Monday / exports may use **`PI-*`**. Specs and evidence may use either; `{ItemId}` in paths is whichever key the row or human specifies.

## Inputs besides Jira

- **Live Jira (preferred):** `PB-*` issue key + `jira/.env` — fetch summary, description, status via REST API. **No PI CSV export required.**
- **Evidence:** Jira **attachments** on the issue — `python -m scripts.jira_automation fetch-evidence PB-xxxx` → `pi/input/pi-evidence/PB-xxxx.zip`. **No separate evidence export.**
- **CSV (legacy):** `pi/input/Book2.csv` (Monday) or old exports — only when no `PB-*` key or API unavailable.
- Canonical column names for Monday-era CSVs remain in `pi/specs/pi.csv`; Jira column labels take precedence when the row source is PB.

## Related repo config

- Reporting JQL and dashboards: `jira/scripts/jira_automation/pi_config.py`, `jira/docs/PI_REPORTING_DELIVERABLES.md`
- `pi_config.py` status constants may lag board labels until aligned after the BA workflow fix.
