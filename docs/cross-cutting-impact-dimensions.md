# Cross-cutting impact dimensions (PI registry)

Use this registry with **`pi/skills/pi-special-cases/SKILL.md`** to enforce blast-radius analysis beyond the PI row’s primary module or asset class.

**Maintenance:** When a PI fix misses a sibling surface (e.g. MF-only fix, DE still broken), add or extend a dimension row here and optionally a narrative case in `pi/docs/pi-special-cases.md`.

## How skills use this file

1. **pi-intake-impact-fix-spec** — Seeds `## Cross-cutting impact matrix` in `pi/specs/{ItemId}.md` with `unknown` for every dimension whose **triggers** match the PI text.
2. **pi-special-cases** — Resolves each matching row to `in-scope` / `out-of-scope` / `unknown` with code/doc evidence; updates acceptance criteria and test plans.
3. **pi-legacy-php-hypothesis** — Feeds the **Stack (PHP vs lambda)** row when PAR/performance/AUM paths are involved.
4. **pi-test-plan** / **pi-code-fix** — Must honor every `in-scope` row (regression + fix scope).

## Matrix status values

| Status | Meaning |
|--------|---------|
| `in-scope` | Same or parallel logic likely affected; include in fix and regression |
| `out-of-scope` | Different mechanism confirmed; cite evidence |
| `unknown` | Triggers matched but not yet discriminated; list quickest check in Open questions |

---

## Dimension: Asset vehicles (MF / DE / FI / Derivatives)

**ID:** `asset_vehicles`

**Triggers (any match in Name, Bug Description, Module, or spec narrative):**

- transfer price, transfer amount, transfer in, transfer out, transfer date
- mutual fund, direct equity, fixed income, derivatives (when symptom is calculation/report, not UI-only)
- PAR, portfolio activity, PPS, portfolio performance, wealth register, WR, gains report, tax schedule, open lot
- demerger, merger (cost/transfer context)

**Sibling search hints:**

- `controller/app/common/calculation/MutualFundCalculation.php`
- `controller/app/common/calculation/DirectEquityCalculation.php`
- `controller/app/common/calculation/FixedIncomeCalculation.php` (if present)
- `controller/app/common/transaction/MutualFundTransaction.php`, `DirectEquityTransaction.php`, `FixedIncomeTransaction.php`, `DerivativesTransaction.php`
- `av_v3_lambda/src/PerformanceApiReport/`, `AUMReport/` — per-vehicle query builders (`getDirectEquityQuery`, mutual fund equivalents)
- Fields: `transfernetamount`, `transfernavperunit`, `transferprice`, transaction types **45** / **46**

**Minimum blast-radius note:** List MF, DE, FI, Derivatives each with status and one-line rationale.

**Minimum acceptance:** One validation bullet per vehicle marked `in-scope` (same txn type / report as PI).

**Known pattern:** MF and DE often share PAR/PPS transfer-in logic; MF-only fixes frequently under-scope DE.

---

## Dimension: Report surfaces (on-screen vs export vs job)

**ID:** `report_surfaces`

**Triggers:**

- report book, widget, dashboard, PDF, export, excel, xlsx, download, print
- “on screen correct but export wrong” (or inverse)
- scheduled report, email report

**Sibling search hints:**

- Same report API vs PDF/layout pipeline vs Excel export handlers under `controller/` and `dashboard/`
- Compare network payload for on-screen widget vs export request for same filters

**Minimum blast-radius note:** UI (Report Book) / PDF / Excel / scheduled job — status each.

**Minimum acceptance:** If `in-scope`, repeat symptom check on each listed surface with same entity/period filters.

---

## Dimension: Stack (legacy PHP vs lambda / API)

**ID:** `stack_php_lambda`

**Triggers:**

- PAR, PPS, TWR, MPPR, AUM, performance report, portfolio activity
- lambda, API report, tourbillon (when tied to reporting)
- slowness on report that has both PHP and lambda paths

**Sibling search hints:**

- `controller/app/common/calculation/*Calculation.php`, `controller/app/library/etcetera/PerformanceCalculation.php`
- `av_v3_lambda/src/PerformanceApiReport/`, `PerformanceApiReport/par_response.py`, `AUMReport/`
- Run **pi-legacy-php-hypothesis** when this dimension matches; copy conclusion into matrix row

**Minimum blast-radius note:** PHP path vs lambda path — which owns the failing field; both if shared contract.

**Minimum acceptance:** Confirm fix at the layer cited in root cause; if only one layer patched, note risk on the other as `unknown` or `in-scope`.

---

## Dimension: Data path (feed / sync / ingestion → DB → UI)

**ID:** `data_path_feed`

**Triggers:**

- feed, sync, Electra, PCR, custodian, ingestion, ETL, auto sync, categorization
- “missing transaction”, “duplicate”, “wrong mapping”, broker file

**Sibling search hints:**

- Ingestion jobs under `controller/` / transformers; staging tables; post-sync UI/report readers
- Trace: file arrival → parse → persist → report/API read

**Minimum blast-radius note:** Ingestion / persistence / read path — where divergence first appears.

**Minimum acceptance:** At least one check at persistence (row/SQL) before UI-only fix is accepted.

---

## Dimension: Tenant / configuration / feature flags

**ID:** `tenant_config`

**Triggers:**

- single client name in title, “only this tenant”, works on UAT not prod, feature flag, license, entitlement
- new tenant, provisioning, template

**Sibling search hints:**

- Tenant config / license APIs; compare failing vs known-good tenant on same build

**Minimum blast-radius note:** Tenant-specific vs all tenants on same module path.

**Minimum acceptance:** Reproduce on second tenant or document why single-tenant; config diff if applicable.

---

## Dimension: Period / currency / locked period

**ID:** `period_currency`

**Triggers:**

- as-of, period, locked period, FX, currency, multi-period, income statement period
- wrong value “for date range” or “after lock”

**Sibling search hints:**

- Date filters on report params; `currencyrate`, `reportcurrency`; locked-period guards in calculation layers

**Minimum blast-radius note:** Single period vs multi-period; base vs report currency.

**Minimum acceptance:** Vary as-of or currency once if dimension is `in-scope` or `unknown`.

---

## Dimension: Transaction type family

**ID:** `txn_type_family`

**Triggers:**

- transfer in, transfer out, demerger, merger, corporate action, CBA, contribution, distribution
- transaction type id, type 45, type 46

**Sibling search hints:**

- Same report/calculation branch for adjacent types (e.g. 45 vs 46; demerger vs standard transfer)
- `transactiontypeid` CASE blocks in calculation and lambda SQL

**Minimum blast-radius note:** Which txn types share the buggy branch.

**Minimum acceptance:** One bullet per in-scope txn type in the same vehicle/report.

---

## Dimension: Product nuance (pi-special-cases.md)

**ID:** `special_cases_doc`

**Triggers:**

- Always run: read `pi/docs/pi-special-cases.md` for every PI.

**Sibling search hints:**

- Match PI narrative to case sections (e.g. short sell sign visibility).

**Minimum blast-radius note:** Reference case id/title if applicable; else `out-of-scope`.

**Minimum acceptance:** Include case-specific AC from `pi-special-cases.md` when matched.

---

## Spec template (copy into `pi/specs/{ItemId}.md`)

```markdown
## Cross-cutting impact matrix

| Dimension | Status | Rationale / evidence |
|-----------|--------|----------------------|
| Asset vehicles (MF/DE/FI/Deriv) | unknown | |
| Report surfaces (UI/PDF/Excel/job) | unknown | |
| Stack (PHP vs lambda) | unknown | |
| Data path (feed → DB → UI) | unknown | |
| Tenant / config | unknown | |
| Period / currency | unknown | |
| Transaction type family | unknown | |
| Product nuance (special cases) | unknown | |

## Impact / blast radius

(Summary narrative; do not replace the matrix—reference `in-scope` rows here.)
```

Only include rows whose triggers matched; omit non-matching dimensions or mark `out-of-scope` with evidence after **pi-special-cases** runs.
