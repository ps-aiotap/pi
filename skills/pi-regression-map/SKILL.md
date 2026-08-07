---
name: pi-regression-map
description: >-
  Builds and refreshes pi/docs/regression-suite-map.json + .md from avautomation
  (Bitbucket). Primary branch Develop (full regression); compares master lag.
  Feeds pi-uat-evidence-review and weekly automation-lead reports.
---

# PI regression suite map

## Location in repo

Stored under `pi/skills/pi-regression-map/`. Symlink only (no copy) to `.cursor/skills/pi-regression-map` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

Maintain an **objective, repo-grounded map** of the AV pytest regression suite so PI skills do not guess coverage from an outdated checkout.

| Output | Path |
|--------|------|
| Machine-readable map | `pi/docs/regression-suite-map.json` |
| Human-readable map | `pi/docs/regression-suite-map.md` |

**Primary reference branch:** `Develop` (full Regression + Smoke + Features).  
**Reference branch:** `master` (smoke-only; lags Develop — document drift, do not use as benchmark).

## When to run

- **Cron Thu 10:30 IST** — `Run PI Regression Map.command` / `pi-regression-map` job
- **Before** first `pi-uat-evidence-review` on a PI (map must exist)
- After significant merges to `avautomation` **Develop**

## Prerequisites

- `avautomation/` clone at workspace root (sibling of `pi/`).
- Network for `git fetch` (or `--no-fetch` when offline).

## Command

From workspace root:

```bash
python pi/scripts/regression_suite_map.py
python pi/scripts/regression_suite_map.py --no-fetch      # offline / cached refs
python pi/scripts/regression_suite_map.py --no-content    # faster; skip Excel sheet parse
python pi/scripts/regression_suite_map.py --json-only
```

No Jira credentials required.

## What the map contains

1. **Full test inventory** — every `Tests/**/*.py` on `Develop` and `master`.
2. **Branch drift** — files on Develop only vs master only (merge lag signal).
3. **Evidence benchmarks** — per module, what the regression suite expects for UAT evidence breadth:
   - **Transactions:** per vehicle (BC, DE, FI, MF, Derivatives, Insurance, …).
   - **Analytics / ReportBook / GL / Masters:** per report or vehicle.
   - **Features (LockPeriod):** per vehicle.
4. **Keyword index** — maps PI summary tokens (e.g. "gains", "mutual fund") → modules, vehicles, test paths.
5. **Excel sheet names** — from `read_excel_data(..., "Sheet")` when content parsing enabled.

## How downstream skills use this

| Skill | Usage |
|-------|--------|
| **`pi-uat-evidence-review`** | Load `evidence_benchmarks` for the PI's module; compare to evidence inventory — **not** the dev's incomplete impact matrix. |
| **`pi-uat-weekly-report`** | Aggregate evidence gaps + `branch_drift.develop_only` for automation-lead discussion. |
| **Dev impact checklist** | When weekly review finds recurring gaps, append benchmark rows to the checklist template (see `pi/docs/uat-test-evidence-gate-findings.md`). |

## Path discipline

- Keep outputs under `pi/docs/`.
- Do not modify `avautomation/` or application code.
- Cite map paths only after verifying they exist (`ls pi/docs/regression-suite-map.json`).

## Validation

After run, confirm:

```bash
ls -la pi/docs/regression-suite-map.json pi/docs/regression-suite-map.md
python -c "import json; d=json.load(open('pi/docs/regression-suite-map.json')); print(d['counts'], list(d['evidence_benchmarks'].keys()))"
```

Expect **Develop** count ≫ **master** (Regression folder exists only on Develop).

## Related

- [`pi/docs/uat-test-evidence-gate-findings.md`](../docs/uat-test-evidence-gate-findings.md) — UAT evidence gate design
- [`pi/docs/cross-cutting-impact-dimensions.md`](../docs/cross-cutting-impact-dimensions.md) — vehicle dimension IDs
- **`pi-uat-evidence-review`** — consumes this map (cron Mon–Fri 10:35)
- **`pi-uat-weekly-report`** — weekly rollup (Fri 11:00)
