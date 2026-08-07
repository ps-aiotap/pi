---
name: pi-test-plan-reconcile
description: >-
  After a PB PI is fixed and Dev RCA (+ Leakage RCA) are on Jira, append or update
  ## Post-RCA (confirmed) in pi/test-plans/{KEY}.md from confirmed RCA, spec matrix,
  and cross-cutting prevention dimensions. Feeds pi-daily-executive-preventability links.
---

# PI test plan reconcile (post-RCA)

## Location in repo

`pi/skills/pi-test-plan-reconcile/` → symlink `.cursor/skills/pi-test-plan-reconcile`.

## Goal

Bridge **open intake** (`pi-test-plan` hypothesis) and **fixed PI executive preventability**:

| Phase | PI state | Test artifact |
| --- | --- | --- |
| Intake | Open | `pi/test-plans/{KEY}.md` — hypothesis (optional) |
| **Reconcile** | **Fixed** + RCAs | **`## Post-RCA (confirmed)`** + **`### Cross-cutting prevention`** |
| Daily report | Fixed MTD | Links to `#post-rca` and `#cross-cutting-prevention` |

Does **not** delete intake content. Grounded in **Jira Dev RCA** + `pi/specs/` cross-cutting matrix (`pi/docs/cross-cutting-impact-dimensions.md`).

## Cross-cutting prevention (Tier 1 + 2)

When spec matrix rows are `in-scope` / `unknown`, or triggers match in summary/Dev RCA:

| Dimension ID | Prevention question |
| --- | --- |
| `asset_vehicles` | DE fix — MF/FI/Deriv siblings tested? |
| `report_surfaces` | UI fix — PDF/Excel/job too? |
| `stack_php_lambda` | PHP fix — lambda path too? |
| `data_path_feed` | UI fix — ingest/DB path too? |
| `tenant_config` | One tenant — others on same module? |
| `period_currency` | Single period — multi-period/FX? |
| `txn_type_family` | One txn type — siblings on same branch? |

Emitted as table under `### Cross-cutting prevention` with anchor `#cross-cutting-prevention`.

## When to run

- PI **Closed**, **Done**, or **Convert_To_CR**
- **Dev RCA** on Jira (field or comment)
- **Not** for open / in-flight PIs

## Commands

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation test-plan-reconcile PB-xxxx
python -m scripts.jira_automation test-plan-reconcile --mtd-fixed
python -m scripts.jira_automation test-plan-reconcile --mtd-fixed --force
```

## Outputs

| Artifact | Path |
| --- | --- |
| Test plan | `pi/test-plans/{KEY}.md` |
| Batch JSON | `pi/reports/test-plan-reconcile-YYYY-MM-DD.json` |

## Trust order

1. Jira Dev RCA + Leakage RCA  
2. Spec `## Cross-cutting impact matrix`  
3. Trigger inference (summary + Dev RCA) if matrix absent  
4. Code paths from Dev RCA  

## Related

- **`pi-test-plan`** — intake hypothesis  
- **`pi-daily-executive-analysis`** — cron: reconcile → preventability report  
- **`pi/docs/cross-cutting-impact-dimensions.md`** — dimension registry  
