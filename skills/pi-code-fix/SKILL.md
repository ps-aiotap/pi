---
name: pi-code-fix
description: >-
  Future phase: implements an approved PI fix from pi/specs/ in application code.
  Cross-check pi/user_manual/ when the spec ties behavior to documented product
  flows. Run only after human sign-off; keep changes minimal and aligned with repo conventions.
---

# PI code fix (future use)

## Location in repo

`pi/skills/`. Symlink to `.cursor/skills/pi-code-fix` when you enable this phase.

## Preconditions

- **Jira status:** Read **`pi/docs/jira-pi-board-status.md`**. **BA (Change Request)** means engineering on the PI is complete—do not expand scope into feature-request work unless the approved spec explicitly includes it.
- **No placeholder refs:** Do not cite `pi/input/pi-evidence/` zips or attachment paths unless they exist; align implementation notes with files actually changed.
- **Path discipline (mandatory):** Do **not** use `@PI`, `@pi`, `@old_pi`, or alias-style folder indirection in implementation evidence or notes. Refer to concrete paths defined in this skill and the approved spec (for example `pi/specs/{ItemId}.md`, `pi/user_manual/...`, and exact application file paths).
- **PI special cases context (mandatory):** Read `pi/docs/pi-special-cases.md` before implementation. If a listed case applies, keep the fix aligned to the approved spec and include any required data-remediation notes in implementation handoff comments.
- **Cross-cutting impact matrix (mandatory):** Read `## Cross-cutting impact matrix` in `pi/specs/{ItemId}.md`. Implement for every row marked **`in-scope`** unless the human explicitly narrows scope in chat; do not ship a single-vehicle or single-layer fix when sibling rows remain `in-scope` or `unknown` without approval.
- **Source code refresh (Bitbucket):** The **workspace root** contains `pi/` plus sibling application trees (`controller/`, `dashboard/`, etc.), often as **multiple separate clones**. **Do not** `git fetch` / `git pull` inside `pi/` as part of this step (`pi/` is typically a **GitHub** PI repo). Before editing application code, for **each** `.git` under `WORKSPACE_ROOT` **excluding** paths under `pi/` (e.g. `find "$WORKSPACE_ROOT" -name .git -type d | grep -v '/pi/'`): run `git fetch --prune`, `git checkout master`, then integrate **`master`** with `origin` (e.g. `git pull --ff-only origin master` or your team’s equivalent). If **`master` is missing**, **any** repo cannot be synced safely, or integration would conflict, **stop** and get human direction.
- `pi/specs/{ItemId}.md` is **reviewed and approved** (man in the loop).
- Prefer a clean branch and normal PR/review process for your team.

## User manual

If the spec or impact doc cites **`pi/user_manual/*.md`**, or the fix changes **user-visible** behavior (screens, messages, calculations users see in reports), **re-read those guides** so the implementation matches **documented** intent unless the approved spec explicitly overrides (e.g. bug fix that corrects wrong behavior). Use **`pi/user_manual/README.md`** to find adjacent guides by theme. Discover extra context with `rg -l "keyword" pi/user_manual`. If code must **differ** from the manual, flag **doc update** as a follow-up—do not silently contradict product docs without human awareness.

## Instructions (when activated)

1. Read `pi/specs/{ItemId}.md` (including **`## Cross-cutting impact matrix`**) and any linked `pi/impact/{ItemId}.md`.
2. When behavior is user-facing, align with cited **`pi/user_manual/`** guides; resolve spec-vs-manual conflicts per spec + human process, not ad hoc.
3. Implement the minimum code changes required; match existing patterns (naming, layers, i18n, config—**no hardcoded** secrets or environment-specific values; use existing env/config mechanisms).
4. Do not expand scope beyond the approved spec and matrix **`in-scope`** rows without explicit user direction; do not shrink scope below those rows without explicit user direction.
5. After implementation, note in chat or in a short append to the spec what files changed (until you adopt a different tracking convention).

This skill intentionally stays minimal until you start automated fix application.
