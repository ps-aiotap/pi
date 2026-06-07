---
name: pi-test-implement
description: >-
  Future phase: implements automated or scripted tests from pi/test-plans/ for a
  given ItemId, using pi/user_manual/ when UI or flow assertions need documented
  labels and steps. Run only after the test plan is approved.
---

# PI test implementation (future use)

## Location in repo

`pi/skills/`. Symlink to `.cursor/skills/pi-test-implement` when you enable this phase.

## Preconditions

- **Jira status:** Read **`pi/docs/jira-pi-board-status.md`**. Tests prove the **PI defect** scope; **BA (Change Request)** does not require automating follow-on feature requests unless the approved plan says so.
- **No placeholder refs:** Test plans and assertions must reference real paths (`rg`/glob verified). Do not leave **TBD** automation rows or cite evidence zips that are not in the workspace.
- **Path discipline (mandatory):** Do **not** use `@PI`, `@pi`, `@old_pi`, or alias-style folder shorthand in test evidence. Use direct file paths defined in this skill and plan/spec inputs (for example `pi/test-plans/{ItemId}.md`, `pi/specs/{ItemId}.md`, `pi/user_manual/...`, and concrete test/code paths).
- **PI special cases context (mandatory):** Read `pi/docs/pi-special-cases.md` before implementing tests. When applicable, add coverage for the nuance-specific behavior and the expected client remediation path documented in the spec/test plan.
- **Source code refresh (Bitbucket):** Same as **`pi-code-fix`**: **workspace root** holds `pi/` (GitHub PI repo — **exclude** from this refresh) and **multiple Bitbucket clones**. In **every** application clone (`find "$WORKSPACE_ROOT" -name .git -type d | grep -v '/pi/'`): `git fetch --prune`, `git checkout master`, then pull/merge **`origin/master`** into **`master`** so the working tree is current. If **any** repo cannot be synced safely, **stop** and get human direction.
- `pi/test-plans/{ItemId}.md` exists and is **approved**.
- Application fix (if any) is merged or available on the branch under test.

## User manual

When the test plan references **`pi/user_manual/*.md`** or covers UI flows, **open those guides** (and **`pi/user_manual/README.md`** to find related topics) so assertions use **documented** menu paths, field labels, and expected outcomes—reducing brittle guesses. If the guide and the app UI diverge, align tests to **approved spec** and note the doc drift in chat or the test plan follow-up. Search: `rg -l "phrase" pi/user_manual` from repo root.

## Instructions (when activated)

1. Read `pi/test-plans/{ItemId}.md` and the corresponding `pi/specs/{ItemId}.md` (including **`## Cross-cutting impact matrix`** — implement coverage for each `in-scope` row reflected in the plan).
2. For manual-test anchors or UI coverage, cross-check cited **`pi/user_manual/`** files (and supplement via README index + ripgrep if the plan is thin).
3. Add or extend tests in the **appropriate** test tree for this repo (discover via existing tests and CI). Prefer the framework already in use.
4. Keep tests focused: prove acceptance criteria and critical regressions first.
5. Run the relevant test command if available and fix failures tied to the new tests.

This skill stays minimal until you begin automated test authoring.
