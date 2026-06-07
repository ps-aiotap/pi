---
name: pi-special-cases
description: >-
  Applies pi/docs/pi-special-cases.md and pi/docs/cross-cutting-impact-dimensions.md:
  resolves the Cross-cutting impact matrix in specs (vehicles, report surfaces, stack,
  feed path, tenant, period/currency, txn types) and aligns test plans before code fix.
---

# PI special cases and cross-cutting impact enforcement

## Location in repo

Stored under `pi/skills/pi-special-cases/`. For Cursor Agent Skill discovery, symlink or copy to `.cursor/skills/pi-special-cases` at the workspace root (parent of `pi/`).

## Goal (non-negotiable)

Before **pi-code-fix** and **pi-test-implement**, ensure each PI spec has a completed **`## Cross-cutting impact matrix`** and that **Impact / blast radius**, **Acceptance criteria**, and (when present) **`pi/test-plans/{ItemId}.md`** reflect every `in-scope` dimension.

## Mandatory reads

1. `pi/docs/pi-special-cases.md`
2. `pi/docs/cross-cutting-impact-dimensions.md` (dimension registry: triggers, search hints, minimum outputs)
3. **`pi/docs/jira-pi-board-status.md`** — board column = status; **BA = Change Request** (eng complete on PI; feature request(s) may follow; not “Done” in prose)
4. `pi/specs/{ItemId}.md` for each PI being processed
5. If present: `pi/similar/{ItemId}.md` (from **`pi-similar-pis`** / intake)
6. If present: `pi/business-impact/{ItemId}.md` (from optional **`pi-business-impact`** — use for sibling/recurrence narrative to humans)
7. If present: `pi/impact/{ItemId}.md`, `pi/test-plans/{ItemId}.md`

## Inputs and scope

- Primary input: Jira issue(s) on **PB**, `pi/input/*.csv` (e.g. legacy `Book2.csv`), or file/keys the human specifies.
- Edit only under `pi/`:
  - `pi/specs/{ItemId}.md` (required)
  - `pi/impact/{ItemId}.md` (optional extended write-up)
  - `pi/test-plans/{ItemId}.md` (regression alignment only)
  - `pi/docs/process-log.md` (optional one-line audit)
- Do not edit application code in this skill.

## Workflow (per PI row)

1. Build trigger text from **Name** / summary, **Bug Description** / description, **Module**, **status/column** (per `pi/docs/jira-pi-board-status.md`), and existing spec sections.
2. Read **`pi/similar/{ItemId}.md`** when present. For **Strong** or **Related** matches:
   - Note closed siblings on another asset class (e.g. MF closed, DE open) in **Impact / blast radius** and **Asset vehicles** matrix rationale.
   - If no similar-PI file and `{ItemId}` is `PB-*`, run **`pi/skills/pi-similar-pis/SKILL.md`** first, then continue.
3. For **each dimension** in `pi/docs/cross-cutting-impact-dimensions.md`:
   - If **triggers** match (or dimension is `special_cases_doc`, which always applies), include a matrix row.
   - Run the dimension’s **sibling search hints** in the application repos (workspace root siblings of `pi/`, excluding `pi/`).
   - Set status: `in-scope` | `out-of-scope` | `unknown` with one-line **evidence** (path, symbol, or doc cite).
4. Apply narrative guidance from any matching **pi-special-cases.md** case (summary, data correction, AC).
5. Update spec sections listed under **Required spec updates**.
6. If `pi/test-plans/{ItemId}.md` exists, add or adjust regression rows so each `in-scope` dimension has at least one targeted case with a **Code / UX anchor**.

## Dimension-specific rules

### Asset vehicles (`asset_vehicles`)

When triggers match, you **must** evaluate Mutual Fund, Direct Equity, Fixed Income, and Derivatives (not only the vehicle named in the PI). Compare `transfernetamount`, `transfernavperunit`, and shared report names (`portfolioperformance`, PAR/PPS/WR/gains) across `*Calculation.php` and lambda report modules.

### Report surfaces (`report_surfaces`)

When triggers match, status UI vs PDF vs Excel vs scheduled job separately; do not assume on-screen fix covers export.

### Stack (`stack_php_lambda`)

When triggers match, check both legacy PHP calculation paths and `av_v3_lambda` report code. If **pi-legacy-php-hypothesis** already ran for this PI, incorporate its conclusion into this row; otherwise note `unknown` and the quickest layer discriminant (API payload vs PHP-only repro).

### Data path (`data_path_feed`)

When triggers match, state whether the defect is likely ingestion, persistence, or read/render; require persistence evidence before accepting UI-only fix scope.

### Tenant / config (`tenant_config`)

When triggers match, state single-tenant vs product-wide; list config/compare check if `unknown`.

### Period / currency (`period_currency`)

When triggers match, note as-of, FX, and locked-period sensitivity in blast radius and AC.

### Transaction type family (`txn_type_family`)

When triggers match, list txn types sharing the same branch (e.g. 45/46) and mark each `in-scope` or `out-of-scope`.

### Product nuance (`special_cases_doc`)

Always read `pi/docs/pi-special-cases.md`; if a case applies, set row status and fold case AC into the spec.

## Required spec updates

For each `pi/specs/{ItemId}.md`:

1. **`## Cross-cutting impact matrix`** — table per template in `cross-cutting-impact-dimensions.md`; only rows whose triggers matched (plus resolved `out-of-scope` with evidence).
2. **`## Impact / blast radius`** — short narrative summarizing all `in-scope` rows; no generic-only text when any dimension was triggered.
3. **Root cause / Fast elimination plan** — when any dimension is `in-scope` or `unknown`, include at least one hypothesis or check that discriminates a sibling surface (e.g. MF vs DE, UI vs PDF, PHP vs lambda).
4. **`## Acceptance criteria`** — at least one bullet per `in-scope` dimension (and per in-scope vehicle or txn type within `asset_vehicles` / `txn_type_family`).
5. **`## Open questions`** — list quickest check for each remaining `unknown` cell.

Optional: `pi/impact/{ItemId}.md` with the full matrix and recommended fix scope (Option A minimal vs Option B structural across dimensions).

## Recording findings

| Artifact | Purpose |
|----------|---------|
| `pi/specs/{ItemId}.md` → `## Cross-cutting impact matrix` | **Canonical** record for reviewers |
| `pi/specs/{ItemId}.md` → `## Impact / blast radius`, `## Acceptance criteria` | Narrative + testable scope |
| `pi/impact/{ItemId}.md` | Optional deep-dive |
| `pi/test-plans/{ItemId}.md` | Regression tied to matrix rows |
| `pi/docs/process-log.md` | Optional: `YYYY-MM-DD: {ItemId} cross-cutting matrix resolved` |

## Quality bar

- Do not leave triggered dimensions off the matrix.
- Do not mark `out-of-scope` without code/path/doc evidence.
- Do not ship MF-only blast radius when DE (or FI/Derivatives) shares the same transfer/report logic (`in-scope` or `unknown` until disproved).
- Do not use placeholder filler; every `unknown` must name the discriminating artifact (log, SQL, API field, file path).

## Relationship to other PI skills

- Runs **after** `pi-intake-impact-fix-spec` and **`pi-similar-pis`** (which seeds similar-PI list and the matrix).
- Runs **before** `pi-legacy-php-hypothesis`, `pi-code-fix`, `pi-test-plan`, and `pi-test-implement`.
- **`pi-test-plan`** must read the matrix and cover every `in-scope` row.
- **`pi-code-fix`** must not narrow scope below `in-scope` rows without explicit human approval in chat.

## Maintaining the registry

When a missed blast radius is discovered in production or QA, update `pi/docs/cross-cutting-impact-dimensions.md` (triggers and search hints) and, if needed, add a case to `pi/docs/pi-special-cases.md`.
