---
name: pi-legacy-php-hypothesis
description: >-
  Generates concrete, actionable competing hypotheses for PI items that involve
  legacy PHP code paths in controller/. Use when PI symptoms point to old PHP
  modules, Zend-era controllers/models, legacy helpers, or mixed PHP+JS flows.
---

# PI legacy PHP hypothesis skill

## Jira board status

Read **`pi/docs/jira-pi-board-status.md`** when the PI row or spec includes workflow position. **BA = Change Request** (engineering complete on the PI; not “Done” in narrative).

## When to use

Use this skill when any of the following are true:

- Code hotspots are primarily under `controller/app/` PHP modules.
- The bug depends on legacy server-rendered pages (`*.phtml`) or old JS in `controller/public/js/`.
- The suspected behavior differs between request handling, DB writes, and legacy report rendering.

## Output contract (mandatory)

Produce **at least 3 competing hypotheses**. Each hypothesis must include:

- **Why likely** tied to PI symptoms.
- **Code evidence** with concrete legacy PHP path(s) and symbol hints.
- **Product-doc evidence** from `pi/user_manual/*.md` where relevant.
- **Quick disprover** with exact runnable check and expected branch outcome.
- **Confidence** (`high`, `medium`, `low`).

Do not output generic placeholders ("needs investigation", "manual check", "triage required").

### Paths and artifacts (mandatory)

- Cite `controller/...` and other paths only after confirming they exist in the workspace or are returned by search. Do not invent file paths as "likely" hotspots without a locate step.

## Legacy PHP hypothesis patterns

Use these patterns to form hypotheses that are concrete and testable:

1. **Request normalization mismatch**
   - Focus: controller action parses/normalizes params differently from UI expectation.
   - Evidence targets: controller action, request helper, input sanitizer.
   - Fast disprover: compare raw request payload vs normalized PHP vars at controller entry.

2. **Validation or guard branch misfire**
   - Focus: legacy condition blocks valid flow due to stale enum/status/feature flag.
   - Evidence targets: early returns, `if` guards, error message branches in controller/model.
   - Fast disprover: log branch condition values for failing and passing cases.

3. **Persistence/write-path divergence**
   - Focus: write succeeds partially or transforms fields before commit.
   - Evidence targets: model save/update method, transaction boundaries, mapper arrays.
   - Fast disprover: compare submitted payload fields with inserted/updated DB columns.

4. **Read/report query filter mismatch**
   - Focus: data saved correctly but omitted by report/list query filters.
   - Evidence targets: report query builders, joins, date/entity/account filters.
   - Fast disprover: run SQL/API with and without optional filters and compare row set delta.

5. **Legacy formatter/rendering defect**
   - Focus: `phtml`/JS formatter shows wrong values despite correct backend data.
   - Evidence targets: view formatter helpers, `number_format`, client-side rendering transforms.
   - Fast disprover: compare API/DB value to rendered DOM/text for same row id.

## Fast elimination plan format (mandatory)

Always provide timed checks:

- **Check 1 (5 min):** boundary check (request -> controller vars).
- **Check 2 (10 min):** persistence parity (payload -> DB row).
- **Check 3 (15 min):** read/render parity (DB/API -> final output).

Each check must state:

- exact file/symbol/query/log point,
- expected outcome,
- branch rule (`if A -> H1`, `else -> H2/H3`).

## Evidence discipline

- Prefer concrete references under `controller/app/`, `controller/public/js/`, and related legacy views.
- Keep hypotheses mutually differentiable: each check should strongly support/reject at least one hypothesis.
- If evidence is missing, explicitly say what artifact is missing and why that blocks confidence.
