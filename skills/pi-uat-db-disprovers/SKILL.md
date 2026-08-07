---
name: pi-uat-db-disprovers
description: >-
  Trial: run read-only SQL from spec Quick disprovers against the PI tenant UAT
  MySQL DB (per-client database via EC2 connection). Writes pi/ops/disprovers/
  and optionally annotates the spec. Skip when uat_db_disprovers_trial is false,
  no runner.env, or tenant/vars missing.
---

# UAT DB disprover trial (intake RCA)

## Status

**Trial** — gated by `uat_db_disprovers_trial: true` in `pi/docs/pi-pipeline-config.md`. Promote to permanent after validation (see `pi/docs/uat-db-disprovers-trial.md`).

## When to run

- **After** `pi-intake-impact-fix-spec` has written `pi/specs/{ItemId}.md` with `## Root cause hypothesis` and **HC UAT URL**.
- **Before** or alongside `pi-debug-playbook` — disprovers here are the same SQL the playbook would run at L4.
- Skip when: flag off, ambiguous tenant, no `runner.env`, or disprovers are non-SQL (DOM/network).

## Prerequisites

1. Read `pi/docs/uat-db-disprovers-trial.md`
2. `pi/input/uat-db/runner.env` from `runner.env.example` (gitignored)
3. EC2 can reach UAT MySQL; **read-only** user; per PI = correct **database** for tenant slug
4. Optional `pi/input/uat-db/vars/{ItemId}.json` for `<txn_id>` etc.

## Paths

| Role | Path |
|------|------|
| Runner config (secret) | `pi/input/uat-db/runner.env` |
| Tenant DB overrides | `pi/input/uat-db/tenant-overrides.json` |
| Per-PI SQL vars | `pi/input/uat-db/vars/{ItemId}.json` |
| Run log | `pi/ops/disprovers/{ItemId}-YYYY-MM-DD.md` |
| Spec annotation | `pi/specs/{ItemId}.md` → `## UAT DB disprover trial` |

## What to do

1. Read `pi/docs/pi-pipeline-config.md` — if `uat_db_disprovers_trial` is **false**, stop and note *skipped — trial disabled*.
2. Read `pi/specs/{ItemId}.md` — confirm single **HC UAT URL** tenant (not ambiguous list).
3. If disprovers need `<txn_id>` / entity ids, create or update `pi/input/uat-db/vars/{ItemId}.json` (do not commit secrets).
4. **Dry-run first** (mandatory on first use per PI):

   ```bash
   python pi/scripts/uat_db_disprovers.py {ItemId} --dry-run
   ```

5. If dry-run shows runnable SQL and `runner.env` exists, execute:

   ```bash
   python pi/scripts/uat_db_disprovers.py {ItemId} --annotate-spec
   ```

6. Open `pi/ops/disprovers/{ItemId}-YYYY-MM-DD.md` — for each hypothesis, compare stdout to the disprover branch rule (`if … → Hn`). Update spec **Confidence** or add one line under the hypothesis:
   - `- **Disprover result (trial):** …`
   - `- **Trial status:** confirmed | eliminated | inconclusive | skipped`
   Only mark **confirmed** / **eliminated** when the SQL output clearly satisfies the disprover's stated branch; otherwise **inconclusive**.
7. Do **not** modify application code. Do **not** run write SQL.

## Safety (mandatory)

- Script blocks mutating SQL; **CALL** is skipped in trial.
- Never commit `runner.env`, passwords, or prod connection strings.
- If database or tenant is uncertain, **skip** — do not guess a connection.

## Relationship to other skills

| Skill | Relationship |
|-------|----------------|
| `pi-intake-impact-fix-spec` | Runs **before** this trial step; writes hypotheses + disprovers |
| `pi-debug-playbook` | Can reuse ops/disprovers log as L4 evidence in session/conclude |
| `pi-dev-rca` | Unaffected — developers still own Jira Dev RCA |

## Promote to permanent

Human sets `uat_db_disprovers_trial: false` and adds `uat_db_disprovers: true` when ready; fold step into default intake in `pi/skil_run.txt`.
