---
name: pi-incoming-reduction-ideate
description: >-
  Weekly idea generation for incoming-PI MoM reduction (~3% target). Cron Fri 14:15
  IST builds a pending draft from Friday RCA/funnel JSON (excludes AO-56), opens it
  for approval. Chat mode can deepen with code/similar-PI context. Writes
  pi/ops/drafts/ideation-pending.md. Does not create AO issues unless
  `incoming-reduction-ideate approve --ranks … --create`. Use after Friday
  reduction reports, on cron present, or when asked to brainstorm / approve PI
  prevention ideas.
---

# PI incoming reduction — ideate

## Location in repo

Stored under `pi/skills/pi-incoming-reduction-ideate/`. Symlink only (no copy) to `.cursor/skills/pi-incoming-reduction-ideate` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Treat Cursor + cron as the **idea crowd** for **~3% MoM reduction in incoming PIs**. Evidence → pending draft → **human approve** → optional AO-56 create.

| This skill / CLI does | Does **not** |
| --- | --- |
| Cron: build ranked NEW levers from Friday JSON + AO-56 exclusion | Auto-create AO/PM/PB issues |
| Present: open `ideation-pending.md` for review | Replace Friday briefs |
| Chat: deepen candidates with code / similar PIs | Claim KPI credit without shipped work |
| `approve --create` only when human passes ranks | Skip the approval gate |

## Schedule (cron)

| Item | Value |
| --- | --- |
| **Evidence job** | Fri **14:00** IST — `pi-incoming-pi-reduction-friday` |
| **Ideate job** | Fri **14:15** IST — `pi-incoming-reduction-ideate` |
| **Runner** | `cron/runners/pi-incoming-reduction-ideate.sh` |
| **Launcher** | `current/pi/Run PI Incoming Reduction Ideate.command` |
| **Outputs** | `pi/ops/drafts/ideation-pending.md` (+ dated + `.json`) |

After editing `cron/crontab.example`, reinstall: `crontab cron/crontab.example`.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
# Friday briefs must exist (JSON):
#   pi/reports/rca-reduction-brief-YYYY-MM-DD.json
#   pi/reports/leakage-coverage-funnel-YYYY-MM-DD.json
```

## CLI

```bash
# Cron / manual — build + open for approval
python -m scripts.jira_automation incoming-reduction-ideate run --present

# Inspect pending
python -m scripts.jira_automation incoming-reduction-ideate status

# Approve ranks only (no Jira)
python -m scripts.jira_automation incoming-reduction-ideate approve --ranks 1,2

# Create AO Tasks under AO-56 (explicit)
python -m scripts.jira_automation incoming-reduction-ideate approve --ranks 1,2 --create
python -m scripts.jira_automation incoming-reduction-ideate approve --ranks 1,2 --create --dry-run

# Reject
python -m scripts.jira_automation incoming-reduction-ideate reject --ranks 5,6,7
```

## Chat workflow (deepen before approve)

1. Ensure pending draft exists (cron or `run --present`).
2. Chat: `pi-incoming-reduction-ideate` — read `ideation-pending.md` + briefs; **enrich** top candidates with concrete code paths / similar PIs; update the draft markdown if findings change ranking.
3. Stop for human pick.
4. Human runs `approve --ranks …` and only then `--create` if promoting to AO-56.

## Inputs (run)

| Source | Why |
| --- | --- |
| Latest `rca-reduction-brief-*.json` | Duplicate Dev RCA groups + failure-mode clusters |
| Latest `leakage-coverage-funnel-*.json` | Open regression gaps |
| Jira `parent = AO-56` | Exclude levers already on the board |

## Quality bar

- **Do** leave overall status `pending_approval` until ranks are approved/rejected.
- **Do not** create Jira unless `approve --create`.
- **Do** prefer recurrence groups and high-count clusters.
- Chat enrichment must cite file paths or mark “no code hit — weak”.

## Related

- **`pi-rca-reduction-brief`** / **`pi-leakage-coverage-funnel`** — Friday evidence
- Epic: [AO-56](https://assetvantage.atlassian.net/browse/AO-56)
- Board: [AO 1309](https://assetvantage.atlassian.net/jira/software/c/projects/AO/boards/1309)
- Cron docs: `cron/SCHEDULED-JOBS-REFERENCE.md`
