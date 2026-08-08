---
name: pi-sdlc-fix-loop
description: >-
  Hourly weekday orchestration for open PB board-774 PIs: refresh app clones,
  run PI analysis (skills 1-8), code fix, verify-the-fix Playwright in dashboard,
  prevention regression list, linked PM Tasks on board 1144, then stop for human PR.
  Does not create Bitbucket PR or implement prevention tests on source branch.
---

# PI SDLC fix loop (stop before PR)

## Location in repo

`pi/skills/`. Symlink to `.cursor/skills/pi-sdlc-fix-loop`.

## Goal

For each open **PB** PI on [board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774):

1. Refresh application code on **`master`**
2. Run analysis pipeline → `pi/specs/{KEY}.md`, `pi/test-plans/{KEY}.md`
3. **Code fix** via `/implementation-agent` (or `pi-code-fix`)
4. **Verify-the-fix Playwright** only → `dashboard/tests/e2e/pi/{KEY}/`
5. **Prevention regression list** in test plan (not implemented on source branch)
6. **Create PM Task(s)** on [board 1144](https://assetvantage.atlassian.net/jira/software/c/projects/PM/boards/1144), linked `relates to` `{KEY}`
7. **Stop** — handoff for human PR decision

## Open PI JQL

```jql
project = PB AND status in ("To Do", "In Review", "In Progress", "On Hold/Reopened - Dev Team")
ORDER BY priority DESC, updated ASC
```

## Schedule (cron)

| Item | Value |
| --- | --- |
| Cron | `0 9-18 * * 1-5` (`Asia/Kolkata`) — hourly weekdays 09:00–18:00 via **`pi-hourly-ops`** |
| Job id | `pi-sdlc-fix-loop` (also dispatched by `pi-hourly-ops`) |
| Runner | `cron/runners/pi-sdlc-fix-loop.sh` |
| State | `cron/state/pi-sdlc-fix-loop.json` |
| Throughput | **1 PI per hour** |

Hourly umbrella (`pi-hourly-ops`) runs **`pi-assign-engineering-queue`** first (In Engineering Queue → assign → IN DEVELOPMENT), then this fix-loop, plus analysis skills by IST hour (deep dive at 10:00, meeting brief at 11:00, etc.) — see `cron/config/hourly-skill-matrix.json` and `cron/SCHEDULED-JOBS-REFERENCE.md`.

```bash
./cron/run-job.sh run pi-hourly-ops manual
./cron/run-job.sh run pi-sdlc-fix-loop manual   # fix-loop only
```

## State file schema

`cron/state/pi-sdlc-fix-loop.json`:

```json
{
  "last_run_ist": null,
  "current_key": null,
  "entries": {
    "PB-xxxx": {
      "status": "in_flight|awaiting_human_pr|awaiting_audit|blocked|done|trashed",
      "branch": "bugfix/PB-xxxx-...",
      "prevention_pm": ["PM-nnn"],
      "playwright_paths": ["dashboard/tests/e2e/pi/PB-xxxx.verify-fix.spec.ts"],
      "handoff": "pi/ops/drafts/fix-handoff-PB-xxxx.md",
      "updated_ist": "2026-08-08T10:00:00+05:30"
    }
  }
}
```

Skip keys already in `in_flight`, `awaiting_human_pr`, `awaiting_audit`, `done`, `blocked`, or `trashed`.

## Agent workflow (one PI)

### 0. Preflight

```bash
./cron/scripts/refresh-app-clones.sh
```

Fails if any app clone is dirty or cannot fast-forward `master`. Do **not** pull inside `pi/` (GitHub PI repo).

### 1. Analysis (skills 1–8) — skip if already done

**Skip intake & deep analysis when already completed earlier** for `{KEY}`:

```bash
./cron/scripts/skill-already-done.py --check-intake {KEY}
```

Exit 0 means skip: `pi/specs/{KEY}.md` (and usually test-plan / evidence-analysis) already exists. Do **not** re-run fetch-evidence → intake → similar-pis etc. Only fill missing **Verify the fix** / **Prevention** sections in the test plan if needed.

If not done yet, follow [`pi/skil_run.txt`](/var/www/pi/skil_run.txt) for `{KEY}`:

1. `pi-fetch-evidence`
2. `pi-evidence-analysis`
3. `pi-intake-impact-fix-spec`
4. `pi-similar-pis`
5. optional `pi-business-impact`
6. `pi-special-cases`
7. `pi-legacy-php-hypothesis` (when PHP/report paths apply)
8. `pi-spec-manual-reproduction`
9. `pi-test-plan` — must include **Verify the fix** and **Prevention regression tests (future PIs)**

### 2. Code fix

```
/implementation-agent

JIRA: {KEY}
Implement the approved fix in pi/specs/{KEY}.md (respect Cross-cutting impact matrix in-scope rows).
Branch: bugfix/{KEY}-short-slug from latest master.
Do not create PR.
```

Or: `Run the skill @pi/skills/pi-code-fix/SKILL.md {KEY}` when enabled.

**Hard rules (master hygiene):**

- All product + Playwright edits stay on `bugfix/{KEY}-...` only.
- Never leave uncommitted files on `dashboard`/`controller` **master** (that aborts `refresh-app-clones.sh` for the next cron hour).
- Before ending the hour: `git -C /var/www/dashboard status --porcelain` and same for other app clones must be empty while on `master`.

### 3. Verify-the-fix Playwright

```
/test-generation-agent

Generate verify-the-fix Playwright for {KEY}.
Read pi/test-plans/{KEY}.md Verify the fix only.
Write ONLY on branch bugfix/{KEY}-... under dashboard/tests/e2e/pi/{KEY}/ with // PI: {KEY} header.
Do not implement Prevention regression tests (future PIs).
Do NOT write or leave Playwright files on master.
Run: cd dashboard && npx playwright test tests/e2e/pi/{KEY}
```

See `.cursor/prompts/workflow/04-test-generation-agent.md` PI fix loop block.

**Gate before handoff:**

| Outcome | State status | Notes |
| --- | --- | --- |
| `npx playwright test ...` ran and passed | may set `awaiting_human_pr` | Specs remain on bugfix branch only |
| UAT/env missing or test cannot run | set `blocked` with reason | Do **not** invent `awaiting_human_pr` or leave `test.fixme` stubs on master |
| Tests failing after fix | keep `in_flight` or `blocked` | Fix code or note blocker; never check in unverified specs to master |

### 4. Prevention regression list

Ensure `pi/test-plans/{KEY}.md` has concrete **Prevention regression tests (future PIs)** rows (anchors, intent, suggested suite). Copy summary to handoff.

### 5. Create PM Tasks (board 1144)

**Before create:** JQL `project = PM AND issue in linkedIssues({KEY}) AND summary ~ "Test:"` — skip if open prevention Tasks already exist.

For each prevention row (or one Task with checklist if ≤3 items):

- **Project:** PM
- **Issue type:** Task
- **Summary:** `[{KEY}] Test: {prevention title}`
- **Description:** steps, expected, automation anchor, source PI link
- **Link:** `relates to` `{KEY}`

Use Atlassian MCP `createJiraIssue` + `createIssueLink`, or draft `pi/ops/drafts/{KEY}-prevention-tasks.json` when offline (pattern from `pi-prevention-pack`).

**Do not** create a second PB bug for prevention coverage.

### 6. Stop — handoff

Only after verify Playwright has **actually been run** (pass → handoff; cannot run → `blocked`).

Write **`pi/ops/drafts/fix-handoff-{KEY}.md`**:

```markdown
# Fix handoff — {KEY}

**Status:** awaiting_human_pr
**Branch:** bugfix/{KEY}-...
**Playwright:** dashboard/tests/e2e/pi/{KEY}/... (on bugfix branch only)
**Playwright result:** PASSED (paste command + summary)
**Run:** cd dashboard && git checkout bugfix/{KEY}-... && npx playwright test tests/e2e/pi/{KEY}
**Prevention PM:** PM-nnn, PM-nnn
**Prevention list:** (summary bullets)
**Next:** Human inspects diff + Playwright; open Bitbucket PR when ready.
**Do not:** auto-merge, auto-close Jira, implement prevention list on this branch, leave master dirty.
```

Update `cron/state/pi-sdlc-fix-loop.json` → `awaiting_human_pr` **only if Playwright passed**. Otherwise → `blocked`.

### 7. End-of-hour hygiene

1. Checkout `master` on each app clone touched.
2. Discard/stash any accidental master dirt so `./cron/scripts/refresh-app-clones.sh` succeeds next hour.
3. Confirm `git status --porcelain` is empty on master.

## Paths

| Artifact | Path |
| --- | --- |
| Spec | `pi/specs/{KEY}.md` |
| Test plan | `pi/test-plans/{KEY}.md` |
| Playwright | `dashboard/tests/e2e/pi/{KEY}/` |
| Handoff | `pi/ops/drafts/fix-handoff-{KEY}.md` |
| PM draft | `pi/ops/drafts/{KEY}-prevention-tasks.json` |
| Cron log | `cron/logs/pi-sdlc-fix-loop.log` |

## Out of scope

- PR Creation / PR Review agents
- Implementing prevention regression on source branch
- Stage 2 Playwright audit (see `pi-playwright-fix-audit`)
- PIs in IN QA, Verify Prod, BA, Closed

## Related

- [`pi-test-plan`](pi-test-plan/SKILL.md), [`pi-test-implement`](pi-test-implement/SKILL.md)
- [`pi-prevention-pack`](pi-prevention-pack/SKILL.md) — PM Task patterns
- [`testing-standards`](../../.cursor/skills/testing-standards/SKILL.md) — Playwright conventions
- [SDLC agent setup](7529abfe-57a9-44ac-9b91-ca4bc80f10eb) — invoke via `/implementation-agent`, `/test-generation-agent`
