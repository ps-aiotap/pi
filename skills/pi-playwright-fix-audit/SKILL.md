---
name: pi-playwright-fix-audit
description: >-
  Stage 2 (future): auto-run verify-the-fix Playwright for a source PB PI and
  record pass/fail to validate the fix worked. Does not run prevention PM Task
  suite or auto-close Jira. Design stub until Stage 1 loop is stable.
---

# PI Playwright fix audit (Stage 2 — design stub)

## Location in repo

`pi/skills/`. Symlink to `.cursor/skills/pi-playwright-fix-audit`.

## Goal

After Stage 1 handoff (`awaiting_human_pr` or human marks `awaiting_audit`), **automatically run** the source PI's verify-the-fix Playwright specs and record whether the fix is validated.

**Does not:**

- Implement or run **Prevention regression tests (future PIs)** (PM Tasks backlog)
- Auto-close Jira or merge PR without human gate

## When to run (planned)

- Manual: *"playwright audit for PB-xxxx"* or *"pi-playwright-fix-audit PB-xxxx"*
- Cron (future): post-handoff hook when state = `awaiting_audit`
- After human PR merge + deploy to UAT (configurable)

## Prerequisites (planned)

- Stage 1 handoff exists: `pi/ops/drafts/fix-handoff-{KEY}.md`
- Playwright specs exist with `// PI: {KEY}` under `dashboard/tests/e2e/pi/{KEY}/`
- `PLAYWRIGHT_BASE_URL` points at UAT (or local with fix branch deployed)
- Fix branch merged or checked out in `dashboard` + backend repos as needed

## Selection

```bash
dashboard/tests/e2e/pi/{KEY}*
dashboard/tests/e2e/pi/{KEY}.verify-fix.spec.ts
```

Grep header: `// PI: {KEY}`

## Run command (planned)

```bash
cd /var/www/dashboard
PLAYWRIGHT_BASE_URL="${PLAYWRIGHT_BASE_URL:-http://localhost:4200}" \
  npx playwright test "tests/e2e/pi/{KEY}" \
  --reporter=json --output=pi/ops/audit/{KEY}-playwright-run
```

## Outputs (planned)

| Artifact | Path |
| --- | --- |
| JSON result | `pi/ops/audit/{KEY}-playwright.json` |
| Summary md | `pi/ops/audit/{KEY}-playwright.md` |
| State update | `cron/state/pi-sdlc-fix-loop.json` → `audit_passed` or `audit_failed` |

## Pass criteria

- Playwright exit code 0
- Assertions map to **Verify the fix** rows in `pi/test-plans/{KEY}.md`

## Fail path

- State `audit_failed`
- Append log to `cron/logs/pi-playwright-fix-audit.log`
- Notify human — **no** auto Jira transition

## Planned cron hook (not implemented)

| Item | Value |
| --- | --- |
| Job id | `pi-playwright-fix-audit` |
| Runner | `cron/runners/pi-playwright-fix-audit.sh` |
| Trigger | After human sets `{KEY}` to `awaiting_audit` in state file |

## Implementation checklist (Stage 2)

- [ ] `cron/runners/pi-playwright-fix-audit.sh`
- [ ] Parse Playwright JSON → `pi/ops/audit/{KEY}-playwright.json`
- [ ] UAT credentials via env (never commit)
- [ ] Wire to state transitions from `pi-sdlc-fix-loop`

## Related

- [`pi-sdlc-fix-loop`](pi-sdlc-fix-loop/SKILL.md) — Stage 1 producer of Playwright paths
- [`testing-standards`](../../.cursor/skills/testing-standards/SKILL.md)
