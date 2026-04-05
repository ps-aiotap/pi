---
name: pi-test-plan
description: >-
  Given an approved PI fix specification under pi/specs/, documents verification
  tests (fix-specific, regression, and adjacent areas) under pi/test-plans/ only.
  Does not implement tests or change application code.
---

# PI test plan (documentation only)

## Location in repo

Stored under `pi/skills/`. For Cursor Agent Skill discovery, symlink or copy to `.cursor/skills/pi-test-plan`.

## Before you start (mandatory)

From the **repository root**, sync with the team remote on Bitbucket before the mandatory repository search: run `git fetch`, then integrate the latest changes using your team’s practice (for example `git pull` on the branch you use for PI work, or rebase onto the appropriate `origin/...` branch). If the network is unavailable, git state is ambiguous, or a pull would conflict with local work, **stop** and get direction from a human rather than assuming paths and tests in the plan match the remote.

## Inputs and outputs

| | Path |
|---|------|
| Read | `pi/specs/{ItemId}.md` (approved or draft spec from the intake skill) |
| Optional context | `pi/impact/{ItemId}.md` |
| Write | `pi/test-plans/{ItemId}.md` |

Do not modify files outside `pi/`.

## Instructions

1. Read the fix spec for `{ItemId}`. Extract acceptance criteria, **Root cause** / **Suggested assignment** paths, and **Impact / blast radius**.
2. **Repository search (mandatory):** Before finalizing the plan, search for automated coverage and conventions, for example:
   - `controller/unittest/` and `**/*Test*.php` under `controller/`
   - `dashboard/**/*.spec.ts` and `dashboard/karma.conf.js` (Karma + Jasmine)
   - `**/phpunit*.xml`, `.github/workflows/`, or other CI configs  
   Use findings to fill **Automation mapping** with **concrete** framework names, file paths, or globs.
3. Write or update **`pi/test-plans/{ItemId}.md`** including:
   - **Code hotspots:** Table or bullets tying the PI to controllers, services, SQL, or UI entry points (start from spec + batch **Code hotspots (seed)** if present).
   - **Verify the fix:** cases that directly prove the PI is resolved (steps, data, expected result).
   - **Regression:** Each row must cite a **Code / UX anchor** (file::symbol, route, or screen), not generic “smoke module” text.
   - **Adjacent:** Only flows justified by impact analysis or shared code.
   - **Automation mapping:** A table (or explicit “manual-only” with rationale). **Do not** leave the word **TBD** as the answer when the spec names `controller/` or other repo paths — either list matching tests/globs or state that no tests reference those paths after the search.
4. If the file still has the batch **Draft (batch-generated)** callout, remove it once regression and automation sections meet the rules above.
5. Do not write or edit executable test code here—that belongs to the `pi-test-implement` skill later.

## Test plan section checklist

- Scope and references (link to `pi/specs/{ItemId}.md`)
- Code hotspots (spec- and repo-grounded)
- Environment / data prerequisites
- Test cases with steps and expected results
- Regression table with **Code / UX anchor** per row
- Adjacent-area cases (trim irrelevant defaults)
- Automation mapping: frameworks + what exists vs gap (**no lazy TBD**)
