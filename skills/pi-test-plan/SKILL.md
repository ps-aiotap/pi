---
name: pi-test-plan
description: >-
  Given an approved PI fix specification under pi/specs/, documents verification
  tests (fix-specific, regression, and adjacent areas) under pi/test-plans/ only,
  grounded in repo code and pi/user_manual/ guides for expected UX and flows.
  Does not implement tests or change application code.
---

# PI test plan (documentation only)

## Location in repo

Stored under `pi/skills/`. For Cursor Agent Skill discovery, symlink or copy to `.cursor/skills/pi-test-plan`.

## Before you start (mandatory)

### Path discipline (mandatory)

- Do **not** use `@PI`, `@pi`, or alias-style path shorthand in test-plan evidence.
- Do **not** use or refer to `@old_pi` for test-plan inputs, citations, or evidence.
- Use only direct paths defined in this skill and discovered by repository search (for example `pi/specs/{ItemId}.md`, `pi/impact/{ItemId}.md`, `pi/user_manual/...`, concrete app/test paths).
- In test plans, cite explicit files/routes/symbols; avoid folder-alias references.

### No placeholder rows or paths (mandatory)

- Do **not** write **TBD**, **TODO**, "(if present)", or cite test/evidence paths unless they exist after a workspace search.
- **Automation mapping:** Replace gaps with concrete outcomes of search (for example "no `*.spec.ts` under `dashboard/src/app/foo` after `rg`")—never lazy filler.
- Do not reference `pi/input/pi-evidence/*.zip` unless that file exists for the PI.

### PI special cases context (mandatory)

Before drafting or updating `pi/test-plans/{ItemId}.md`, read `pi/docs/pi-special-cases.md`.
If a listed case applies, include explicit regression and verification rows for that nuance and note any client data-correction handling expected by the spec.

### Jira board status (mandatory)

Read **`pi/docs/jira-pi-board-status.md`**. Use **board column** as workflow status. If the PI is in **BA (Change Request)**, acceptance criteria should cover **PI defect verification** and closure—not full delivery of follow-on feature requests unless the spec explicitly includes them.

### Source code refresh (Bitbucket application clones)

Same rules as **`pi-intake-impact-fix-spec`**: **workspace root** = parent of `pi/`. **Do not** refresh **`pi/`** (separate **GitHub** PI repository) as part of updating application source. Before the mandatory repository search, in **each** application clone under `WORKSPACE_ROOT` (discover with):

```bash
find "$WORKSPACE_ROOT" -name .git -type d | grep -v '/pi/' | sort
```

run `git fetch --prune`, check out **`master`**, then integrate **`master`** with `origin` (e.g. `git pull --ff-only origin master` or team equivalent) so the **working tree** matches **`origin/master`**.

**All** such Bitbucket repos should be current on **`master`**. If the network is unavailable, **any** clone fails, **`master` is missing**, git state is ambiguous, or integration would conflict, **stop** and get human direction.

## Inputs and outputs

| | Path |
|---|------|
| Read | `pi/specs/{ItemId}.md` (approved or draft spec from the intake skill) |
| Optional context | `pi/impact/{ItemId}.md` |
| Write | `pi/test-plans/{ItemId}.md` |
| Expected product behavior (manual steps, labels, flows) | `pi/user_manual/` — see **User manual** below |

Do not modify files outside `pi/`.

## User manual

Use **`pi/user_manual/`** so test cases match **documented** user-facing behavior, not only code.

1. **Index:** **`pi/user_manual/README.md`** groups guides by theme (transactions, GL, report book, performance, etc.). Use **`Module`** and spec keywords to pick the closest guides.
2. **Search:** `rg -l "phrase" pi/user_manual` from repo root; open the best matches. If two revisions exist (`_1`), prefer the one that matches current product language in the spec; note ambiguity in the plan.
3. **Test plan usage:**
   - **Verify the fix** and **Regression** rows: where helpful, add a **User manual** column or bullet referencing **`pi/user_manual/<file>.md`** as the “expected flow” anchor alongside **Code / UX anchor**.
   - **Environment / data prerequisites:** mention setup steps that guides describe (masters, COA, report book, permissions) when the PI depends on them.
4. **Conventions:** Screenshots may be missing (`media/`); use written menu paths from the guide. Use on-disk filenames exactly (including typos in slug names per README).

Do not treat the user manual as a substitute for the mandatory **repository search** for automation—it complements UX and manual verification.

## Instructions

1. Read the fix spec for `{ItemId}`. Extract acceptance criteria, **Root cause** / **Suggested assignment** paths, **`## Cross-cutting impact matrix`**, and **Impact / blast radius**. Every matrix row marked **`in-scope`** must have at least one regression or verify-the-fix case (or an explicit open question if blocked). Pull any **user manual** citations already listed in the spec; extend with **`pi/user_manual/`** search if gaps remain for repro or regression flows.
2. **Repository search (mandatory):** Before finalizing the plan, search for automated coverage and conventions, for example:
   - `controller/unittest/` and `**/*Test*.php` under `controller/`
   - `dashboard/**/*.spec.ts` and `dashboard/karma.conf.js` (Karma + Jasmine)
   - `**/phpunit*.xml`, `.github/workflows/`, or other CI configs  
   Use findings to fill **Automation mapping** with **concrete** framework names, file paths, or globs.
3. Write or update **`pi/test-plans/{ItemId}.md`** including:
   - **Code hotspots:** Table or bullets tying the PI to controllers, services, SQL, or UI entry points (start from spec + batch **Code hotspots (seed)** if present).
   - **Verify the fix:** cases that directly prove the PI is resolved (steps, data, expected result).
   - **Regression:** Each row must cite a **Code / UX anchor** (file::symbol, route, or screen), not generic “smoke module” text.
   - **Adjacent:** Only flows justified by impact analysis, **`## Cross-cutting impact matrix`** `in-scope` rows, or shared code.
   - **Automation mapping:** A table (or explicit “manual-only” with rationale). **Do not** leave the word **TBD** as the answer when the spec names `controller/` or other repo paths — either list matching tests/globs or state that no tests reference those paths after the search.
4. If the file still has the batch **Draft (batch-generated)** callout, remove it once regression and automation sections meet the rules above.
5. Do not write or edit executable test code here—that belongs to the `pi-test-implement` skill later.

## Test plan section checklist

- Scope and references (link to `pi/specs/{ItemId}.md`; summarize **`## Cross-cutting impact matrix`** `in-scope` dimensions; list relevant **`pi/user_manual/*.md`** when they define expected behavior for manual cases). If you paste the **HC UAT** URL from the spec, keep the spec’s **markdown link** syntax so it stays clickable.
- Code hotspots (spec- and repo-grounded)
- Environment / data prerequisites
- Test cases with steps and expected results
- Regression table with **Code / UX anchor** per row
- Adjacent-area cases (trim irrelevant defaults)
- Automation mapping: frameworks + what exists vs gap (**no lazy TBD**)
