---
name: pi-daily-deep-dive
description: >-
  Daily deep analysis of 5 PB board-774 PIs from the IN DEVELOPMENT column so the
  PI lead builds understanding (boss-driven learning ritual). Runs fetch+evidence
  analysis when attachments exist (content-level, not inventory). Enriches with
  gaps, code paths, questions, and CR-candidate check — does not invent intake facts.
  Writes pi/deep-dives/{KEY}.md and pi/reports/daily-deep-dive-YYYY-MM-DD.md.
  Never writes to Jira unless a human asks.
---

# PI daily deep dive (5 × IN DEVELOPMENT)

## Location in repo

`current/pi/skills/pi-daily-deep-dive/` → symlink `.cursor/skills/pi-daily-deep-dive`.

## Goal

Every workday, go **deep** on **5 PIs** currently in **IN DEVELOPMENT** (Jira status `In Progress`) on [board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774).

Purpose: **personal / lead understanding** (boss coaching ritual) — not thin triage, not reporter coaching (that is **`pi-detail-elaboration`**).

**Enrichment is analysis, not invention.** Add structure, codebase grounding, gaps, and questions. Do **not** fabricate client requirements, fake RCAs, or fake ETAs beyond what intake + code evidence support.

**Never write to Jira** unless a human explicitly asks.

## Cron / run

| Item | Value |
| --- | --- |
| Run at | **10:00 AM IST** (`Asia/Kolkata`) — via weekday **`pi-hourly-ops`** |
| Cadence | **Weekdays** (`Mon–Fri`), once per IST day |
| Cron job id | `pi-hourly-ops` (matrix skill `pi-daily-deep-dive`) |
| Cron does | Shared clone refresh + emit agent prompt under `cron/state/prompts/` |
| Agent does | Chat `pi-daily-deep-dive` → deep MDs + **`pi-cr-candidate`** |

Hourly matrix: `cron/config/hourly-skill-matrix.json` (10:00 pack also includes open analysis, detail elaboration, non-eng disposition, stale reminder).

**Skip if already done today:** hourly ops checks artifacts before emitting a prompt:

```bash
./cron/scripts/skill-already-done.py pi-daily-deep-dive   # exit 0 = skip
```

Done when `pi/reports/daily-deep-dive-YYYY-MM-DD.md` exists, or `pi/ops/daily-deep-dive-state.json` already has today’s `runs` entry.

```bash
# Preferred — part of hourly ops (fires deep-dive at IST hour 10 only if not done)
./cron/run-job.sh run pi-hourly-ops manual
HOUR_OVERRIDE=10 ./cron/runners/pi-hourly-ops.sh

# Prompt only
./cron/scripts/build-skill-prompt.sh pi-daily-deep-dive

# then chat (keys from queue or auto-select):
pi-daily-deep-dive PB-a PB-b PB-c PB-d PB-e
```

## Chat prompts

```text
pi-daily-deep-dive              # pick next 5 from IN DEVELOPMENT
pi-daily-deep-dive --today      # same; force today's IST date
pi-daily-deep-dive PB-a PB-b …  # explicit keys (still write daily rollup)
```

## Selection rules (when keys not given)

1. Query Jira: `project = PB AND status = "In Progress" ORDER BY priority DESC, updated ASC`
2. Load `pi/ops/daily-deep-dive-state.json` (create if missing).
3. Prefer keys **not** listed in `analyzed_keys` (or whose `last_deep_dive` is older than 14 days).
4. Take **up to 5**. If fewer than 5 remain unanalyzed, continue with oldest `last_deep_dive`, then any remaining In Progress.
5. If IN DEVELOPMENT has **fewer than 5** total, deep-dive **all** of them and note the shortfall in the daily report.
6. After the run, update state with today’s keys + IST timestamp.

### State file shape

`pi/ops/daily-deep-dive-state.json`:

```json
{
  "analyzed_keys": {
    "PB-3001": {"last_deep_dive": "2026-07-22", "verdict_hint": "Stay PI"}
  },
  "runs": [
    {"date": "2026-07-22", "keys": ["PB-3001", "PB-3002", "PB-3003", "PB-3004", "PB-3005"]}
  ]
}
```

Keep `runs` to the last ~60 days.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
bash current/pi/scripts/refresh_bitbucket_app_clones.sh --primary-only
```

## Per-PI deep dive (do all five)

For each selected key:

1. **Fetch Jira** — summary, description, priority, assignee/developer/team, comments, linked issues, attachment names.
2. **Evidence (mandatory when attachments exist):**
   - Run **`pi-fetch-evidence`** if `pi/input/pi-evidence/{KEY}.zip` is missing (direct `ls`).
   - Run **`pi-evidence-analysis`** if `pi/evidence-analysis/{KEY}.md` is missing **or** is inventory-only boilerplate (see that skill’s quality bar). Open images; quote tabular tokens.
   - If Jira has **no** attachments, note that under Intake facts vs gaps — do not invent evidence.
3. **Read local artifacts if present** — `pi/specs/{KEY}.md`, `pi/elaborations/{KEY}.md`, `pi/evidence-analysis/{KEY}.md`, `pi/similar/{KEY}.md`, `pi/business-impact/{KEY}.md`, `pi/ops/debug/{KEY}-*.md`.
4. **CR check** — run **`pi-cr-candidate`** for this key (or perform the same workflow inline) and link `pi/cr-candidates/{KEY}.md`. Ground Stay-PI vs CR in attachment facts when present (e.g. mock “desired columns” spreadsheet → often CR-B signal).
5. **Code grounding** — search AV app clones under workspace root (siblings of `pi/`: `controller/`, `dashboard/`, `av_v3_lambda/`, etc.). Prefer search tokens from evidence-analysis **Extracted tokens**. Cite real paths; mark adjacent vs exact.
6. **Understanding write-up** — write `pi/deep-dives/{KEY}.md` using the template below.
7. **Mark assumptions** — anything not in intake/evidence must be labeled `Assumption:` or listed under **Open questions**.

## What “more detail” means (allowed)

| Add | Do not invent |
| --- | --- |
| Gap analysis (what’s missing to act) | Fake client / tenant facts |
| Likely modules / code paths (cited) | Unverified root cause as fact |
| Clarifying questions for BA / reporter / assignee | Fake ETAs |
| Related / similar PIs (from search or `pi/similar/`) | Scope the client never asked for |
| Draft repro / AC **only** when grounded in intake + evidence, else as questions | |
| Blast radius / test angles | |
| CR vs Stay-PI verdict (`pi-cr-candidate`) | |
| Content-level evidence findings (`pi-evidence-analysis`) when attachments exist | Zip inventory without opening images/CSV |

## Per-PI template → `pi/deep-dives/{KEY}.md`

```markdown
# Deep dive — {KEY}

**Generated (IST):** YYYY-MM-DD HH:MM
**Jira:** https://assetvantage.atlassian.net/browse/{KEY}
**Column:** IN DEVELOPMENT
**Priority / Team / Assignee / Developer:** …
**Summary:** …

## In one minute

What is broken or asked for, in plain language (from intake only).

## Intake facts vs gaps

| Have | Missing / thin |
| --- | --- |
| … | … |

## Evidence findings

- Link: `pi/evidence-analysis/{KEY}.md` (or *no attachments* / *analysis N/A — {reason}*)
- Symptom anchors (3–7 bullets from analysis — **required** when zip exists): …
- What attachments do **not** prove: …

## Product / domain context

Terms, screens, reports involved — cite `pi/user_manual/` or intake; else questions.

## Codebase map

- Entry points / modules found: `path` …
- Data / calc touchpoints: …
- **CR candidate:** link `../cr-candidates/{KEY}.md` — Stay PI | Convert to CR (A/B) | Unclear

## Working hypotheses (labeled)

1. … — **Evidence:** (code path and/or attachment token) … | **Confidence:** low/med/high
2. …

Do not promote a hypothesis to “root cause” without evidence.

## Open questions

Numbered questions for reporter, BA, or assignee — paste-ready.

## Suggested verification angles

What you would check on HC UAT / SQL / API if debugging next (not a full test plan).

## Learning notes (for you)

What this PI teaches about the product or stack (2–5 bullets). This section is for the boss-driven understanding ritual.
```

## Daily rollup → `pi/reports/daily-deep-dive-YYYY-MM-DD.md`

```markdown
# Daily PI deep dive — YYYY-MM-DD

**Column:** IN DEVELOPMENT (`In Progress`)
**Count analyzed today:** N / 5
**Keys:** PB-… 

## Summary table

| Key | Priority | Summary | CR verdict | Top gap | Deep dive |
| --- | --- | --- | --- | --- | --- |
| PB-xxxx | Critical | … | Stay PI | … | [md](../deep-dives/PB-xxxx.md) |

## Themes today

- Patterns across the five (modules, CR-ish asks, thin intake, etc.)

## Follow-ups for you

- [ ] …
```

Also refresh stable pointer (optional overwrite): `pi/reports/daily-deep-dive.md` → same content as today’s dated file.

## Agent workflow

1. Ping Jira; refresh Bitbucket primary clones.
2. Select 5 keys (or use explicit list).
3. For each key: deep dive + **`pi-cr-candidate`**.
4. Write daily rollup + update `pi/ops/daily-deep-dive-state.json`.
5. In chat: table of 5 keys, CR verdicts, and the 1–2 strongest learning themes — keep it short; point to the MD files.

## Do not

- Invent intake details to “fill” the ticket.
- Post to Jira or transition to Convert_To_CR without an explicit human ask.
- Duplicate **`pi-detail-elaboration`** (ready/thin coach-the-reporter) — different audience and goal.
- Skip the CR check; always produce or refresh `pi/cr-candidates/{KEY}.md` for today’s five.
- Skip **`pi-evidence-analysis`** when Jira attachments or a verified zip exist; do not deep-dive from summary text alone while screenshots/Excel sit unread.
- Analyze Feedback / Verify Prod / Incoming instead of IN DEVELOPMENT unless the human overrides the selection.

## Related

- **`pi-fetch-evidence`** / **`pi-evidence-analysis`** — mandatory attachment path before hypotheses when evidence exists
- **`pi-cr-candidate`** — Stay PI vs Convert to CR (A/B)
- **`pi-detail-elaboration`** — thin/ready scoring + reporter coaching (all open columns)
- **`pi-debug-playbook`** — when you move from understanding to hands-on debug
- **`pi-intake-impact-fix-spec`** — full fix spec when eng path is confirmed
- `pi/docs/jira-pi-board-status.md`
