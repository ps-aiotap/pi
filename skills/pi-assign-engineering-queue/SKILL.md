---
name: pi-assign-engineering-queue
description: >-
  Auto-assigns Developer + Team on PB board-774 In Engineering Queue PIs that
  are missing both fields, then moves them to IN DEVELOPMENT. Uses
  developer-domains.json rules. Runs hourly via pi-hourly-ops before the fix
  loop; supports --dry-run. Pair with pi-developer-domain-learn for rule tuning.
---

# PI assign engineering queue (In Engineering → Development)

## Location in repo

Stored under `current/pi/skills/pi-assign-engineering-queue/`. Symlink to `.cursor/skills/pi-assign-engineering-queue` at the workspace root for Cursor Agent Skill discovery.

## Goal

For **In Engineering Queue** only (`status = In Review` on board **774**):

| Condition | Action |
| --- | --- |
| Developer **and** Team both empty | Suggest from `developer-domains.json` → set Developer + Team + assignee → transition to **IN DEVELOPMENT** (`In Progress`) |
| Developer or Team already set | **Skip** (no overwrite) |
| No domain match / low confidence / API error | **Skip** / report — do **not** transition |

## Schedule (cron)

| Item | Value |
| --- | --- |
| Cron | `0 9-18 * * 1-5` (`Asia/Kolkata`) — every hour via **`pi-hourly-ops`**, **before** `pi-sdlc-fix-loop` |
| Matrix | `cron/config/hourly-skill-matrix.json` |
| Prompt builder | `cron/scripts/build-skill-prompt.sh pi-assign-engineering-queue` |
| Chat | `pi-assign-engineering-queue` |

Also on demand: *"assign engineering queue"*, *"assign In Engineering PIs"*. Prefer `--dry-run` when unsure about domain coverage.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Commands

```bash
cd jira && source .venv/bin/activate

# Preview (no Jira writes)
python -m scripts.jira_automation assign-engineering-queue --dry-run

# Live: assign + move to IN DEVELOPMENT
python -m scripts.jira_automation assign-engineering-queue

# Cap batch size / full JSON
python -m scripts.jira_automation assign-engineering-queue --dry-run --limit 20 --json
```

Implementation: `jira/scripts/jira_automation/assign_engineering_queue.py`  
Team UUID write: `assign_developer.apply_assignment` + `pi/input/team/atlassian-teams.md`

## Outputs

| Role | Path |
| --- | --- |
| Report (markdown) | `pi/reports/assign-engineering-queue-YYYY-MM-DD.md` |
| Report (JSON) | `pi/reports/assign-engineering-queue-YYYY-MM-DD.json` |

## Agent workflow

1. `ping` credentials.
2. Run `assign-engineering-queue --dry-run`; summarize applied / skipped / errors from the report.
3. If the user asked for live assign (default for this skill when not told dry-run), run without `--dry-run`.
4. Show keys moved to Development and any errors.

## Do not

- Touch **INCOMING BUGS**, **IN DEVELOPMENT**, **Reopened**, In QA, Verify Prod, or Feedback.
- Overwrite an existing **Developer** or **Team** value.
- Transition when assignment failed or confidence is low / no rule matched.
- Auto-apply during **intake** — intake stays suggest-only (`assign_developer_apply: false`). This skill is the separate queue auto-apply path.
- Reference AO board / AO keys in shared artifacts.

## Related

- **`pi-developer-domain-learn`** — tune `developer-domains.json`
- **`assign-developer suggest/apply`** — single-PI intake helper
- **`pi/docs/jira-pi-board-status.md`** — column ↔ status map
