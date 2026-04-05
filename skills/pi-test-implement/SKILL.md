---
name: pi-test-implement
description: >-
  Future phase: implements automated or scripted tests from pi/test-plans/ for a
  given ItemId. Run only after the test plan is approved.
---

# PI test implementation (future use)

## Location in repo

`pi/skills/`. Symlink to `.cursor/skills/pi-test-implement` when you enable this phase.

## Preconditions

- From the **repository root**, sync with the team remote on Bitbucket before adding or changing tests: run `git fetch`, then integrate the latest changes using your team’s practice (for example `git pull` on the branch under test, or rebase onto the appropriate `origin/...` branch). If you cannot sync safely, **stop** and get human direction.
- `pi/test-plans/{ItemId}.md` exists and is **approved**.
- Application fix (if any) is merged or available on the branch under test.

## Instructions (when activated)

1. Read `pi/test-plans/{ItemId}.md` and the corresponding `pi/specs/{ItemId}.md`.
2. Add or extend tests in the **appropriate** test tree for this repo (discover via existing tests and CI). Prefer the framework already in use.
3. Keep tests focused: prove acceptance criteria and critical regressions first.
4. Run the relevant test command if available and fix failures tied to the new tests.

This skill stays minimal until you begin automated test authoring.
