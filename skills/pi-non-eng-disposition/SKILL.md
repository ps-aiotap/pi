---
name: pi-non-eng-disposition
description: >-
  Daily report of PB board-774 PIs dispositioned without engineering: Feedback,
  Convert to CR, or Closed with no eng path — plus gaps (missing Leakage RCA,
  missing closer comment) with draft suggestions. First run = Jun–Jul 2026 backlog;
  later = prior IST day. Cron 10:05 IST. Writes pi/reports/non-eng-disposition*.md.
  Never writes to Jira.
---

# PI non-engineering disposition report (10:05 AM IST)

## Location in repo

`current/pi/skills/pi-non-eng-disposition/` → symlink `.cursor/skills/pi-non-eng-disposition`.

## Goal

List PIs on [board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774) that were **dispositioned without an engineering fix path**, flag **remaining gaps**, and include **draft suggestions** (report only):

| Disposition | Jira status | Rule |
| --- | --- | --- |
| Feedback | `Feedback PI` | Always in scope |
| Convert to CR - BA | `Convert_To_CR` | Always in scope |
| CLOSED | `Closed` | Only if changelog never touched eng statuses |

**Engineering touch statuses:** In Review (Engineering Queue), In Progress (IN DEVELOPMENT), In QA, `VERIFICATION ON PRODUTION`, Reopen.

### Gaps (chase list)

Among in-scope PIs:

| Gap | Rule |
| --- | --- |
| **Missing Leakage RCA** | `customfield_11345` empty (legacy text field accepted if set). **Not** Dev RCA — no eng path. |
| **Missing closer comment** | Person who moved the PI into the disposition has **no** comment on the issue. Any comment by that closer counts. |

### Draft suggestions (report only — no Jira writes)

For each gap row the report includes:

| Field | How suggested |
| --- | --- |
| **Suggested Leakage RCA** | Keyword match on summary/description/comments → else disposition prior (Feedback/Closed-no-eng → `Not an Issue`; Convert to CR → `New Requirement`). Confidence: high / medium / low + rationale. |
| **Suggested closer comment** | Paste-ready 1–2 sentences for the **closer** to post (includes disposition + Leakage RCA label + short summary). |

**Never** `PUT` Leakage RCA or post comments from this skill/CLI. Human pastes after review. Related apply path remains **`pi-leakage-rca`** only when explicitly asked.

Report sections: **Counts** → **Gaps** (table + paste-ready fill-ins) → **PIs (full in-scope list)**.

## Schedule

| Item | Value |
| --- | --- |
| Run at | **10:05 AM IST** (`Asia/Kolkata`) |
| Cadence | **Daily** (cron `pi-non-eng-disposition`) |
| **1st run** | Full backlog: PIs **created** Jun–Jul 2026 currently in scope |
| **Later runs** | Prior IST calendar day — status **entered** Feedback / Convert_To_CR / Closed (Closed filtered for no eng) |

First-run vs daily is tracked in `current/pi/ops/non-eng-disposition-state.json` (`--mode auto`).

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Command

```bash
cd jira
python -m scripts.jira_automation non-eng-disposition-report
python -m scripts.jira_automation non-eng-disposition-report --mode backlog   # force Jun–Jul backlog
python -m scripts.jira_automation non-eng-disposition-report --mode prior-day # force prior IST day
```

**macOS:** double-click `current/pi/Run PI Non-Eng Disposition.command`.

Implementation: `jira/scripts/jira_automation/non_eng_disposition_report.py`.

## Outputs

| Artifact | Path |
| --- | --- |
| Stable | `current/pi/reports/non-eng-disposition.md` |
| Dated | `current/pi/reports/non-eng-disposition-YYYY-MM-DD.md` |
| JSON | `current/pi/reports/non-eng-disposition-YYYY-MM-DD.json` (includes suggestion fields) |
| State | `current/pi/ops/non-eng-disposition-state.json` |

## Agent workflow

1. Confirm `jira/.env` (`ping`).
2. Run `non-eng-disposition-report` (default `--mode auto`).
3. Summarize: in-scope totals + gap counts; surface high-confidence Leakage suggestions and paste-ready closer comments.
4. Do **not** apply suggestions to Jira unless the human explicitly asks (then use **`pi-leakage-rca`** apply / manual comment as appropriate).

## Do not

- Write Leakage RCA, Dev RCA, or comments to Jira from this report.
- Require or flag **Dev RCA** for this population.
- Count open engineering columns (To Do / In Review / In Progress / Reopen) as dispositions.
- Treat Closed-after-eng-path as in scope.
- Reset `non-eng-disposition-state.json` unless the human asks for a fresh backlog run.

## Related

- **`pi-daily-open-analysis`** — open-PI morning snapshot (10:00)
- **`pi-daily-executive-preventability`** — fixed PIs with eng path / Leakage RCA (09:30)
- **`pi-leakage-rca`** — draft/apply Leakage RCA for a single PI (only path that may write Jira when human asks)
- `pi/docs/jira-pi-board-status.md` — column ↔ status map
