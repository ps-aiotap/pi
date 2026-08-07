---
name: pi-meeting-brief
description: >-
  Daily manager-sync brief: open Critical/High PIs with business one-liners, debug
  status, and queue context. Writes pi/reports/meeting-brief-YYYY-MM-DD.md. Weekdays;
  run after morning ops or on demand.
---

# PI meeting brief (daily manager sync)

## Location in repo

Stored under `pi/skills/pi-meeting-brief/`. Symlink only (no copy) to `.cursor/skills/pi-meeting-brief` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

**One page** for your daily PI sync with managers — substance, not only queue counts.

Complements **`pi-daily-open-analysis`** / **`pi-daily-ops-report`** (metrics and RCA gaps).

## Schedule

| Item | Value |
| --- | --- |
| **Cadence** | Weekdays, after ~10 AM morning ops (or before 5 PM sync) |
| **Chat** | `pi-meeting-brief` or `pi-meeting-brief YYYY-MM-DD` |
| **Output** | `pi/reports/meeting-brief-YYYY-MM-DD.md` |

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

Prefer fresh `pi/reports/pi-ops-dashboard.md` or run `daily-open-analysis` first.

## Open PI definition

Same **four board-774 columns** as `pi-daily-ops-report` (INCOMING BUGS, In Engineering Queue, IN DEVELOPMENT, Reopened).

## Workflow

1. Fetch open PIs from Jira (or read latest `daily-ops-*.md` / dashboard JSON).
2. Filter to **Critical**, **Highest**, **High**, **Business Critical** (include Medium only if human names keys).
3. For each row, pull:
   - Summary, column, assignee, team, ETA if set
   - **Business one-liner:** from `pi/business-impact/{KEY}.md` → "What the client sees" OR spec summary (1 sentence)
   - **Debug status:** from spec `## Debug status` or `pi/ops/debug/{KEY}-my-rca.md` (verdict / inconclusive / no playbook)
   - HC UAT link from spec
4. Add **3-line exec snapshot** from dashboard (open count, missing ETA, missing Dev RCA on post-eng).
5. Write `pi/reports/meeting-brief-YYYY-MM-DD.md`.

## Output template

```markdown
Subject: PI Manager Brief — YYYY-MM-DD — {N} open · {C} critical/high

# PI Manager Brief — YYYY-MM-DD

## Snapshot

- Open PIs (4 columns): …
- Critical / High in open: …
- Missing ETA (open): …

## Critical / High — talk track

| Key | Summary | Column | Assignee | Client pain (1 line) | Your debug | Links |
|-----|---------|--------|----------|----------------------|------------|-------|
| PB-xxxx | … | IN DEVELOPMENT | … | Wrong PAR opening on CFD | H1 likely · [my RCA](../ops/debug/PB-xxxx-my-rca.md) | [spec](../specs/PB-xxxx.md) · [Jira](…) |

## Stale / needs attention

(from morning ops stale list if available — max 5 rows)

## Your follow-ups today

- [ ] …
```

## Quality bar

- Client pain line must be **specific** to the PI — no "users impacted".
- If no business-impact file, compress from spec **Summary** — note *no business-impact yet*.
- Max **15** PI rows in main table; overflow in "Other open" bullet list.

## Related

- **`pi-business-impact`** — backfill improves this brief
- **`pi-debug-playbook`** — debug column
- **`pi-master-index`** — full catalog
- **`pi-daily-ops-report`** — 5 PM email (queues)
