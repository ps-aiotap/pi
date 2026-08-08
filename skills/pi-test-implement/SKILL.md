---
name: pi-test-implement
description: >-
  Implements verify-the-fix Playwright from pi/test-plans/ for a given ItemId
  under dashboard/tests/e2e/pi/. Does not implement prevention regression list
  (PM Tasks). Run after test plan exists and code fix is on branch.
---

# PI test implementation (verify-the-fix Playwright)

## Location in repo

`pi/skills/`. Symlink to `.cursor/skills/pi-test-implement`.

## Preconditions

- **Jira status:** Read **`pi/docs/jira-pi-board-status.md`**. Tests prove the **PI defect** scope only.
- **No placeholder refs:** Test plans and assertions must reference real paths (`rg`/glob verified).
- **Path discipline (mandatory):** Use direct file paths (e.g. `pi/test-plans/{ItemId}.md`, `dashboard/tests/e2e/pi/{ItemId}/`).
- **PI special cases context (mandatory):** Read `pi/docs/pi-special-cases.md` before implementing tests.
- **Source code refresh (Bitbucket):** Same as **`pi-code-fix`** — refresh every app clone except `pi/` on `master` before authoring tests.
- `pi/test-plans/{ItemId}.md` exists with **Verify the fix** and **Prevention regression tests (future PIs)** sections.
- Application fix is on the working branch under test.

## Scope

| In scope | Out of scope |
|----------|--------------|
| **Verify the fix** rows → Playwright under `dashboard/tests/e2e/pi/{ItemId}/` | **Prevention regression tests (future PIs)** → PM Tasks only |
| PHPUnit for backend-only verify rows when no UI | Org-wide avautomation suite expansion |
| Tag files with `// PI: {ItemId}` | PR creation |

Prefer **`/test-generation-agent`** with Playwright forced (see `.cursor/prompts/workflow/04-test-generation-agent.md` PI fix loop prompt).

## Instructions

1. Read `pi/test-plans/{ItemId}.md` and `pi/specs/{ItemId}.md` — implement **Verify the fix** only.
2. Write Playwright under `dashboard/tests/e2e/pi/{ItemId}/` following `dashboard/tests/e2e/balance-sheet*.spec.ts` patterns.
3. Each spec file: header `// PI: {ItemId}`.
4. Run `cd dashboard && npx playwright test tests/e2e/pi/{ItemId}` when environment allows; note blockers in handoff.
5. Do **not** implement rows under **Prevention regression tests (future PIs)** — orchestrator creates PM Tasks from that list.

## Handoff fields

Record in `pi/ops/drafts/fix-handoff-{ItemId}.md`:

- Playwright paths created
- Run command
- Pass/fail or environment blocker
