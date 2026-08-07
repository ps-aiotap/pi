---
name: pi-uat-evidence-review
description: >-
  At Verification on UAT (In QA): review Jira attachments against avautomation
  regression benchmarks (pi/docs/regression-suite-map.json). Posts Jira comment +
  pi/reports/uat-evidence-review-{KEY}.md. No filename/type restriction on evidence.
---

# PI UAT evidence review

## Location in repo

`pi/skills/pi-uat-evidence-review/` → symlink `.cursor/skills/pi-uat-evidence-review`.

## Goal

When a PI is on **Verification on UAT** (`In QA`), validate that **test evidence exists** and that coverage signals match the **regression suite breadth** for the inferred module — **not** the dev's (possibly incomplete) impact matrix.

| Output | Path |
|--------|------|
| Per-PI report | `pi/reports/uat-evidence-review-{KEY}.md` |
| Per-PI JSON | `pi/reports/uat-evidence-review-{KEY}.json` |
| Batch snapshot | `pi/reports/uat-evidence-review-batch-YYYY-MM-DD.json` |
| Jira comment | On ticket (when `--live`) |

## Prerequisites

1. **Regression map** refreshed: `python3 pi/scripts/regression_suite_map.py`
2. Jira credentials: `cd jira && source .venv/bin/activate && python -m scripts.jira_automation ping`

## When to run

| Trigger | Command |
|---------|---------|
| Single PI | `uat-evidence-review PB-xxxx --live` |
| All In QA column (cron) | `uat-evidence-review --uat-column --live` |
| Preview | `uat-evidence-review --uat-column --dry-run` |

## Verdicts

| Verdict | Meaning |
|---------|---------|
| `NO_EVIDENCE` | No Jira attachments |
| `NEEDS_MORE_EVIDENCE` | Attachments exist but benchmark items missing from text/filenames |
| `PARTIAL` | Few gaps — lead review |
| `READY` | Benchmark breadth appears covered |
| `UNKNOWN_MODULE` | Evidence exists but module not inferred from summary |

## Evidence rules (agreed)

- **Any** attachment type/name counts as evidence (no filename convention).
- Coverage signals from: summary, description, attachment filenames.
- Benchmark source: `Develop` branch regression map (`pi/docs/regression-suite-map.json`).

## Workflow  vs regression

For each missing benchmark item, the review notes whether a **Develop regression test exists**. If not, suggests a test file addition for the automation lead (also rolled into **`pi-uat-weekly-report`**).

## Path discipline

- Do not modify application code or `avautomation/`.
- Verify regression map exists before citing paths.

## Related

- **`pi-regression-map`** — refresh benchmarks first
- **`pi-uat-weekly-report`** — Friday rollup for automation lead
- [`pi/docs/uat-test-evidence-gate-findings.md`](../docs/uat-test-evidence-gate-findings.md)

## CLI

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation uat-evidence-review PB-2888 --live
python -m scripts.jira_automation uat-evidence-review --uat-column --live
python -m scripts.jira_automation uat-evidence-review --uat-column --dry-run
```

Implementation: `jira/scripts/jira_automation/uat_evidence_review.py`
