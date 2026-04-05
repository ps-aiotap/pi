---
name: pi-code-fix
description: >-
  Future phase: implements an approved PI fix from pi/specs/ in application code.
  Run only after human sign-off on the specification; keep changes minimal and
  aligned with repo conventions.
---

# PI code fix (future use)

## Location in repo

`pi/skills/`. Symlink to `.cursor/skills/pi-code-fix` when you enable this phase.

## Preconditions

- From the **repository root**, sync with the team remote on Bitbucket before editing application code: run `git fetch`, then integrate the latest changes using your team’s practice (for example `git pull` on your feature or integration branch, or rebase onto the appropriate `origin/...` branch). If you cannot sync safely, **stop** and get human direction.
- `pi/specs/{ItemId}.md` is **reviewed and approved** (man in the loop).
- Prefer a clean branch and normal PR/review process for your team.

## Instructions (when activated)

1. Read `pi/specs/{ItemId}.md` and any linked `pi/impact/{ItemId}.md`.
2. Implement the minimum code changes required; match existing patterns (naming, layers, i18n, config—**no hardcoded** secrets or environment-specific values; use existing env/config mechanisms).
3. Do not expand scope beyond the approved spec without explicit user direction.
4. After implementation, note in chat or in a short append to the spec what files changed (until you adopt a different tracking convention).

This skill intentionally stays minimal until you start automated fix application.
