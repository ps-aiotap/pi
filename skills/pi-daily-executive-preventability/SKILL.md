---
name: pi-daily-executive-preventability
description: >-
  Daily MTD preventability report for fixed PIs only (Closed/Done/Convert_To_CR).
  Leakage RCA, prevention lever, links to post-RCA test plans and cross-cutting
  prevention summaries. Run via cron pi-daily-executive-analysis or mtd-preventability-report CLI.
---

# PI daily executive preventability

## Location in repo

`pi/skills/pi-daily-executive-preventability/` → symlink `.cursor/skills/pi-daily-executive-preventability`.

## Goal

**Executive preventability view** for **fixed** PIs reported MTD — not open/in-flight backlog.

| Included | Excluded |
| --- | --- |
| Closed, Done, Convert_To_CR | Open engineering, UAT, Verify Prod, Feedback |
| Leakage RCA + preventable classification | Hypothesis intake test plans |
| Link to `#post-rca` + `#cross-cutting-prevention` | Inline generic test bullets |

## Lifecycle (with reconcile)

```text
FIXED + Dev RCA  →  test-plan-reconcile  →  pi/test-plans/PB-xxxx.md
                                              ↓
DAILY 09:30 IST  →  mtd-preventability-report  →  pi/reports/pi-daily-executive-preventability.md
```

Run **`pi-test-plan-reconcile`** before this report when new PIs closed overnight.

## Schedule

| Item | Value |
| --- | --- |
| **Run** | **Daily 09:30 IST** (with `pi-daily-executive-analysis` cron) |
| **As-of** | Run date (IST) |
| **Automation** | `Run PI Daily Executive Analysis.command` or CLI below |

## Commands

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation mtd-preventability-report
python -m scripts.jira_automation mtd-preventability-report --as-of YYYY-MM-DD
```

Full morning job (volume + reconcile + preventability):

```bash
./cron/run-job.sh run pi-daily-executive-analysis manual
```

## Per-PI fields

| Field | Source |
| --- | --- |
| **Preventable** | Leakage RCA category map + spec inference |
| **Prevention lever** | Category → lever (testing, config, platform, …) |
| **Prevention tests** | Link to `../test-plans/PB-xxxx.md#post-rca` or _pending reconcile_ |
| **Cross-cutting prevention** | One-line summary from reconcile table + link `#cross-cutting-prevention` |

Cross-cutting dimensions follow **`pi/docs/cross-cutting-impact-dimensions.md`** (Tier 1+2). Summary only in this report — full table lives in reconciled test plan.

## Outputs

| Artifact | Path |
| --- | --- |
| Primary (stable) | `pi/reports/pi-daily-executive-preventability.md` |
| Legacy alias (same content) | `pi/reports/executive-mtd-preventability.md` |
| Dated archive | `pi/reports/pi-daily-executive-preventability-YYYY-MM-DD.md` |
| Machine data | `pi/reports/mtd-per-pi-prevention-YYYY-MM-DD.json` |

## Do not

- List open PIs in the per-PI section (they appear only in excluded-count summary).
- Inline generic bullets like “review pi/similar/” or “unit + integration tests…”.
- Treat intake `pi/test-plans/` hypothesis as confirmed prevention.

## Related

- **`pi-test-plan-reconcile`** — post-RCA + cross-cutting table in test plans
- **`pi-executive-weekly-report`** — volume counts (same cron job, step 1)
- **`pi-prevention-pack`** — PM backlog from confirmed RCAs
- **`pi/docs/cross-cutting-impact-dimensions.md`** — dimension registry
