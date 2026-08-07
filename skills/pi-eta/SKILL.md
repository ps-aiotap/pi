---
name: pi-eta
description: >-
  Draft or validate Client Committed Timeline (ETA) for open PB PIs only (four board-774
  columns). Skips In QA, Verify Prod, Watchlist, BA, Closed. Writes pi/ops/drafts/.
  Does not auto-update Jira unless human explicitly asks to apply.
---

# PI ETA — Client Committed Timeline

## Location in repo

Stored under `pi/skills/pi-eta/`. Symlink only (no copy) to `.cursor/skills/pi-eta` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Set or validate **Client Committed Timeline** (`customfield_11118`) for **open PIs only**.

**ETA is required only when the PI is open** — same four columns as **`pi-daily-ops-report`** and **`pi-monthly-ageing`**:

| Board column | Jira status |
| --- | --- |
| INCOMING BUGS | To Do |
| In Engineering Queue | In Review |
| IN DEVELOPMENT | In Progress |
| Reopened | On Hold/Reopened - Dev Team |

**ETA not required** (do not draft, do not chase): In QA, Verify Prod, Watchlist, BA, Closed, Done, Historical.

Constant: `pi_config.FIELD_CLIENT_COMMITTED_TIMELINE` · scope JQL: `pi_config.jql_open_pi_eta_scope()`.

## When to run

- PI is **open** (status in `pi_config.OPEN_PI_STATUSES`) and ETA missing or overdue.
- Human: *"set ETA for PB-xxxx"* on an **open** PI.

## When to skip (mandatory)

1. Fetch Jira status for `{ItemId}`.
2. If `pi_config.is_open_pi_status(status)` is **false** → stop. Reply:

   `ETA not required — {ItemId} is not open (status: {status}). ETA applies only to INCOMING BUGS, In Engineering Queue, IN DEVELOPMENT, Reopened.`

3. Do **not** write `pi/ops/drafts/{ItemId}-eta.md` unless human explicitly overrides.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

Timezone: **Asia/Kolkata** (IST).

## Inputs and outputs

| | Path |
| --- | --- |
| Read | Jira: status, priority, Team, assignee, `customfield_11118` |
| Read (if present) | `pi/specs/{ItemId}.md` |
| Write | `pi/ops/drafts/{ItemId}-eta.md` (open PIs only) |

## Jira writes (default vs apply)

| Mode | Behavior |
| --- | --- |
| **Draft (default)** | Human pastes into Jira **Client Committed Timeline** |
| **Apply** | Only if human says *"apply ETA to Jira"* and PI is still **open** |

## Workflow (open PIs only)

1. Confirm status ∈ `OPEN_PI_STATUSES`; else skip (see above).
2. If ETA set and not overdue → *ETA OK* with days remaining (IST).
3. If missing or overdue → draft proposed date + rationale.
4. Write `pi/ops/drafts/{ItemId}-eta.md`.

## ETA rules

- Date format **YYYY-MM-DD**.
- No **TBD** in the Jira value.
- Align with `pi/docs/jira-pi-board-status.md`.

## Related

- **`pi-daily-ops-report`** — ETA gaps from open PIs only
- **`pi-dev-rca`**, **`pi-leakage-rca`**
