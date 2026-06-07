#!/usr/bin/env python3
"""
Merge 'Manual reproduction (self-contained)' into 'Reproduction / symptoms' and place
that section immediately after Metadata. Optionally replace root-cause stack for ItemIds
listed in UPGRADES.
"""
from __future__ import annotations

from pathlib import Path

SPECS_DIR = Path(__file__).resolve().parents[1] / "specs"

REST_ORDER = [
    "Root cause (hypothesis)",
    "Competing hypotheses",
    "Fast elimination plan",
    "Legacy PHP / view-stack note",
    "Legacy PHP hypothesis patterns (supplement)",
    "Proposed fix (behavior-level)",
    "Fix options",
    "Impact / blast radius",
    "Risks / rollback",
    "Acceptance criteria",
]

SKIP_WHEN_UPGRADED = frozenset(
    {"Root cause (hypothesis)", "Competing hypotheses", "Fast elimination plan"}
)


def split_doc(text: str) -> tuple[str, dict[str, str]]:
    lines = text.splitlines()
    if not lines:
        return "", {}
    title = lines[0]
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in lines[1:]:
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return title, sections


def rebuild(text: str, item_id: str, upgrade: str | None) -> str:
    title, sec = split_doc(text)
    repro = sec.get("Reproduction / symptoms", "").strip()
    manual = sec.get("Manual reproduction (self-contained)", "").strip()
    if manual:
        merged_repro = f"{repro}\n\n{manual}".strip() if repro else manual
    else:
        merged_repro = repro

    chunks: list[str] = [title, "", f"## Metadata\n\n{sec.get('Metadata', '')}\n"]
    chunks.append(f"## Reproduction / symptoms\n\n{merged_repro}\n")

    for name in ("Client environment URL", "Suggested assignment", "Summary"):
        body = sec.get(name, "").strip()
        if body:
            chunks.append(f"## {name}\n\n{body}\n")

    if upgrade:
        chunks.append(upgrade.strip() + "\n")

    for name in REST_ORDER:
        if upgrade and name in SKIP_WHEN_UPGRADED:
            continue
        body = sec.get(name, "").strip()
        if body:
            chunks.append(f"## {name}\n\n{body}\n")

    oq = sec.get("Open questions", "").strip()
    chunks.append(f"## Open questions\n\n{oq}\n")
    return "\n".join(chunks).rstrip() + "\n"


# Full replacement: Root cause + Competing hypotheses + Fast elimination plan
UPGRADES: dict[str, str] = {
    "PI-6526": """## Root cause (hypothesis)

Newly provisioned tenants may ship with **incomplete feature flags**, **license entitlements**, or **default template** data compared with mature tenants—presenting as “missing features” rather than a single UI defect.

## Competing hypotheses

- **H1: Tenant provisioning / onboarding job skipped steps (masters, modules, or report templates)**
  - **Why likely:** “Newly created client” + SWAT-style rollout often ties to scripted setup; missing rows in setup tables surface as absent menus or widgets.
  - **Code evidence:** `controller/app/modules/user/controllers/IndexController.php` and related **admin / tenant bootstrap** paths (search `rg -n "provision|onboard|new.*client" controller/app` from workspace root).
  - **Product-doc evidence:** `pi/user_manual/setting_up_entities_and_groups.md`, `pi/user_manual/setting_up_users_and_user_profile_permissions.md`.
  - **Quick disprover:** SQL row count compare: **feature/module** tables (names from internal schema) for **new** vs **reference** tenant id on same build; first table with large delta localizes H1.
  - **Confidence:** medium

- **H2: License or subscription entitlements hide modules for the new org**
  - **Why likely:** Same UI works on old tenant; new tenant may have **license profile** without optional modules.
  - **Code evidence:** Search `rg -n "license|entitlement|module.*enabled" controller/app` for gating around menu assembly.
  - **Product-doc evidence:** `pi/user_manual/setting_up_users_and_user_profile_permissions.md` (permission vs product packaging).
  - **Quick disprover:** Compare **license JSON** or **tenant config** API payload for new vs known-good tenant; if modules differ, H2 holds before code defects.
  - **Confidence:** medium

- **H3: Cached config / CDN / browser profile serves stale assets only on new subdomain**
  - **Why likely:** Rare, but new hostname can hit **edge cache miss** or **old bundle** if version pins differ.
  - **Code evidence:** `controller/public/js/ej2-min.js` load path and **asset versioning** in layout views.
  - **Product-doc evidence:** `pi/user_manual/how_to_clear_cache_from_the_browser.md`.
  - **Quick disprover:** Hard refresh + incognito on new tenant URL; compare **Network** tab JS bundle hash vs reference tenant. If identical and issue persists, reject H3.
  - **Confidence:** low

## Fast elimination plan

- **Check 1 (5 min):** Side-by-side login **new** vs **reference** tenant → open same **Menu** path; screenshot missing items. **If** menus differ before any data entry → **H1/H2**.
- **Check 2 (10 min):** Export **tenant metadata** (license/entitlement API or admin screen). **If** module list ⊂ reference → **H2** first.
- **Check 3 (15 min):** DB diff **config/masters** tables for tenant ids (exact tables from schema discovery). **If** schema rows missing → **H1** remediation path.""",
    "PI-0967": """## Root cause (hypothesis)

**Gains Report** path for **since inception** + **Grandfathered LTCG** likely executes **heavy server aggregation** (large tax-lot set) and/or **expensive expand/export**—client may **timeout** while internal run completes slowly (>5 min).

## Competing hypotheses

- **H1: Server-side gains engine / SQL path is O(rows × lots) for wide inception window**
  - **Why likely:** Filters maximize data volume; internal repro also >5 min points to backend cost, not only client network.
  - **Code evidence:** `controller/app/common/report/GainsReport.php`, `controller/app/library/tourbillon/GainsCalculationTourbillon.php`, `controller/app/modules/reports/controllers/IndexController.php` (gains actions).
  - **Product-doc evidence:** `pi/user_manual/gains_report__filter_tax-lot_wise_realized_&_unrealized_gains_by_desired_grouping.md`.
  - **Quick disprover:** Run same report with **narrow date range** on same entity. **If** runtime drops orders of magnitude → **H1** (data volume / query plan).
  - **Confidence:** high

- **H2: Client browser timeout, proxy, or WASM/JS export stall while server eventually finishes**
  - **Why likely:** Client “could not generate” may be **504/timeout** though batch completes server-side.
  - **Code evidence:** `controller/public/js/wealth.js` export handlers; reverse-proxy timeout config (outside repo—record observed HTTP status).
  - **Product-doc evidence:** Same gains guide — user expectation is completion without manual retry.
  - **Quick disprover:** Repeat generation with **browser devtools** → **Network**; note **status code** and **time to first byte** vs **download complete**. **If** HTTP 200 but browser aborts late → **H2** export/client path.
  - **Confidence:** medium

- **H3: Expand-all / grid virtualization triggers pathological front-end work after payload returns**
  - **Why likely:** “Expand and export” in ticket; huge DOM after expand can freeze UI independently of SQL time.
  - **Code evidence:** Gains grid JS (search `rg -n "gainsreport|expand" controller/public/js/wealth.js`).
  - **Product-doc evidence:** `pi/user_manual/av's_powerful_report_filtering_explained.md`.
  - **Quick disprover:** Generate **without expanding**; time to ready. **If** acceptable, then expand step blows time → **H3**.
  - **Confidence:** medium

## Fast elimination plan

- **Check 1 (5 min):** Narrow **to date** to **one quarter**; regenerate. **If** fast → **H1** volume; **If** still slow → continue.
- **Check 2 (10 min):** Server log / PHP slow query log for same request id during client failure window. **If** query >300s → **H1** confirmed regardless of UI.
- **Check 3 (15 min):** Compare **export** timing **without** expand vs **with** expand. **If** delta huge → **H3**; **If** network shows gateway timeout → **H2**.""",
    "PI-5028": """## Root cause (hypothesis)

**AUM** pipeline (`av_v3_lambda` / `av-edge-api`) may return **empty position set** for Slocum due to **filter mismatch** (entity, as-of, vehicle), **lambda aggregation bug**, or **data not synced** to the store the report reads—while other reports use a different source.

## Competing hypotheses

- **H1: AUM API filters exclude the entity’s vehicles or accounts**
  - **Why likely:** “No Position” is often **zero rows** from API, not a formatter bug.
  - **Code evidence:** `av_v3_lambda/src/AUMReport/position_details.py`, `av_v3_lambda/src/PerformanceApiReport/par_response.py`.
  - **Product-doc evidence:** `pi/user_manual/README.md` — **Performance & benchmarks** theme.
  - **Quick disprover:** Log **raw API JSON** for AUM call with entity id + as-of from reporter. **If** `positions` array empty but DB has rows → **H1/H3**; **If** API has rows → UI mapping bug (new hypothesis).
  - **Confidence:** high

- **H2: As-of date or timezone boundary drops holdings**
  - **Why likely:** End-of-day vs UTC mismatch yields no snapshot.
  - **Code evidence:** Same lambda modules — date parameter normalization.
  - **Product-doc evidence:** `pi/user_manual/av's_powerful_report_filtering_explained.md`.
  - **Quick disprover:** Shift **as-of** ±1 business day; **If** positions appear → **H2**.
  - **Confidence:** medium

- **H3: Slocum data exists only in legacy controller path not wired to new AUM service**
  - **Why likely:** Split stack: dashboard calls **lambda** while **holdings** screen still hits **PHP**.
  - **Code evidence:** `controller/app/common/report/ReportTransaction.php` vs lambda routes in `av-edge-api`.
  - **Product-doc evidence:** `pi/user_manual/investment_positions_and_the_position_master_explained.md`.
  - **Quick disprover:** Compare **same entity/as-of** in **position master / holdings** API vs **AUM** API row counts.
  - **Confidence:** medium

## Fast elimination plan

- **Check 1 (5 min):** Capture **AUM** XHR URL + JSON body/response in browser. **If** empty `data` → backend (**H1–H3**).
- **Check 2 (10 min):** SQL / internal tool: count **open positions** for tenant **slocummgmt** on as-of. **If** SQL > 0 and API 0 → **H1/H3**.
- **Check 3 (15 min):** Vary **as-of** and **currency** params. **If** sensitivity → **H2** first.""",
    "PI-6479": """## Root cause (hypothesis)

**Custom account mapping** rows for **withdrawal/deposit** may be **seeded as system** records, **referenced by transactions** (FK), or **protected by validation**—blocking delete and appearing as a “contradiction” to users.

## Competing hypotheses

- **H1: Mapping row is flagged `system` / non-editable in master table**
  - **Why likely:** User says “seems to be a system mapping.”
  - **Code evidence:** `controller/app/common/transaction/AVBankcashTransaction.php`, `controller/app/common/transaction/AccountTransaction.php` — search `custom.*mapping|withdrawal|deposit` with `rg`.
  - **Product-doc evidence:** `pi/user_manual/how_to_perform_custom_account_mapping.md`.
  - **Quick disprover:** SQL: inspect mapping row **type/source** columns; **If** `is_system=1` or equivalent → **H1** (product rule vs bug).
  - **Confidence:** high

- **H2: Dependent transactions prevent delete (FK or soft-delete guard)**
  - **Why likely:** Even user-created mappings become undeletable once used.
  - **Code evidence:** Same PHP modules — delete/update handlers and exception messages.
  - **Product-doc evidence:** `pi/user_manual/how_to_transfer_from_a_managed_account_into_a_brokerage_account_with_underlying_securities.md`.
  - **Quick disprover:** Attempt delete; read **exact** error string + stack. **If** FK violation → **H2**; offer **inactivate** vs **purge** per policy.
  - **Confidence:** medium

- **H3: UI shows “system” for any non-user-origin mapping due to mis-labeling**
  - **Why likely:** Mapping is deletable server-side but UI disables control.
  - **Code evidence:** `controller/app/modules/*/views/**/*.phtml` for custom mapping screens (discover via `rg -l "custom.*mapping" controller/app`).
  - **Product-doc evidence:** `pi/user_manual/how_to_perform_custom_account_mapping.md`.
  - **Quick disprover:** Call **delete API** directly (curl) with admin cookie. **If** succeeds while UI blocks → **H3**.
  - **Confidence:** low

## Fast elimination plan

- **Check 1 (5 min):** Read **DB row** for the mapping id shown in UI (tenant **tectonicadvisors**). **If** system flag set → **H1**.
- **Check 2 (10 min):** Count **transactions** referencing mapping id. **If** count > 0 → **H2**.
- **Check 3 (15 min):** API delete vs UI delete parity test → **H3** split.""",
    "PI-6815": """## Root cause (hypothesis)

**Grid view** uses a **different formatter** or **column metadata** than **non-grid** view—hard-coding **2 decimal** quantity display despite user **6-decimal** preference.

## Competing hypotheses

- **H1: Grid column definition sets `decimalPlaces: 2` (or legacy `toFixed(2)`)**
  - **Why likely:** Classic split between **ej2/DataGrid** config and **detail** formatter.
  - **Code evidence:** `controller/public/js/ej2-min.js` usage sites; `rg -n "decimal|quantity|format" dashboard/src` if Angular path; `controller/public/js/wealth.js` for legacy grids.
  - **Product-doc evidence:** `pi/user_manual/av's_powerful_report_filtering_explained.md`.
  - **Quick disprover:** Inspect **column JSON** or **Angular columnDefs** for quantity field in grid vs list. **If** grid hardcodes 2 → **H1**.
  - **Confidence:** high

- **H2: User unit-decimal preference not passed into grid datasource request**
  - **Why likely:** Non-grid reads session **userdecimals**; grid uses default.
  - **Code evidence:** Grid data adapter / API query params (search `userUnitPlaces|decimals` in `controller/public/js` and `dashboard/`).
  - **Product-doc evidence:** `pi/user_manual/setting_up_users_and_user_profile_permissions.md`.
  - **Quick disprover:** Network tab: compare API **metadata** block for grid vs non-grid responses for same screen.
  - **Confidence:** medium

- **H3: Rounding occurs in SQL for grid query only**
  - **Why likely:** Two endpoints: one rounds `ROUND(qty,2)`.
  - **Code evidence:** `controller/app/common/report/ReportTransaction.php` or module-specific grid queries.
  - **Product-doc evidence:** N/A (server contract).
  - **Quick disprover:** Raw JSON **quantity** field: **If** already 2 decimals from API for grid → **H3**; **If** 6 decimals in JSON but UI 2 → **H1**.
  - **Confidence:** medium

## Fast elimination plan

- **Check 1 (5 min):** DevTools → **Response** JSON for grid load: inspect quantity precision. **If** 6 in JSON → **H1** front-end.
- **Check 2 (10 min):** Search codebase for **quantity** column format in **grid** config for Gary Peters module (exact module from reporter).
- **Check 3 (15 min):** Temporarily set user pref to **4** decimals; **If** grid stuck at 2 → confirms **H1/H2**.""",
    "PI-6587": """## Root cause (hypothesis)

**Custodian Recon** returns **no rows** for selected **securities** due to **date-window filter** (bug cites **3/12–3/12**), **wrong security/position id resolution**, or **missing feed** for that window—not necessarily “no custodian data” in DB globally.

## Competing hypotheses

- **H1: Date filter uses exclusive end boundary or wrong timezone → zero rows**
  - **Why likely:** Single-day range in corner often triggers off-by-one.
  - **Code evidence:** `rg -n "Custodian|Recon" controller/app/modules` → controller actions building SQL `BETWEEN`.
  - **Product-doc evidence:** `pi/user_manual/README.md` — **Feeds, statements & custodians**.
  - **Quick disprover:** Widen range ±7 days. **If** data appears → **H1**.
  - **Confidence:** high

- **H2: Security multi-select maps to wrong internal ids (ISIN vs symbol)**
  - **Why likely:** “Selecting them” returns nothing if lookup fails silently.
  - **Code evidence:** Recon filter handler + `positionmaster` join conditions.
  - **Product-doc evidence:** Same custodian theme guides.
  - **Quick disprover:** Run recon with **one** known `positionid` from SQL. **If** works → **H2** mapping bug.
  - **Confidence:** medium

- **H3: Feed file not loaded for Acadia on that date (operational gap)**
  - **Why likely:** Empty recon is correct if no file.
  - **Code evidence:** Feed ingest logs / staging tables (discover table names via code).
  - **Product-doc evidence:** N/A.
  - **Quick disprover:** Confirm **custodian file** receipt row for **3/12** in ingest table. **If** missing → **H3** ops, not product defect.
  - **Confidence:** medium

## Fast elimination plan

- **Check 1 (5 min):** Widen date range; **If** rows → **H1**.
- **Check 2 (10 min):** SQL count custodian staging rows for **security + date** on **acadiafo**.
- **Check 3 (15 min):** Single-security recon with explicit id from DB → **H2**.""",
    "PI-6393": """## Root cause (hypothesis)

**PCR Auto Sync** posts transactions into **Unidentified** when **symbol/ISIN mapping** fails or **listed-security heuristic** misclassifies rows—green UI may reflect **sync status** not **mapping validity**.

## Competing hypotheses

- **H1: Feed mapping rules lack PCR symbol variant → unidentified bucket**
  - **Why likely:** Classic feed integration gap.
  - **Code evidence:** `rg -n "Unidentified|PCR|autosync" controller/app/common/transaction` — mapping transactions.
  - **Product-doc evidence:** `pi/user_manual/README.md` — **Feeds, statements & custodians**.
  - **Quick disprover:** Inspect **raw PCR line** vs **mapping table** for failing txn; **If** no rule matches → **H1**.
  - **Confidence:** high

- **H2: Security exists in master but `listed` flag wrong → green highlight logic inverted**
  - **Why likely:** PI says green for unlisted; expectation red.
  - **Code evidence:** Transaction sync UI PHP/JS classifying rows (search `unlisted|listed|green|red` in sync views).
  - **Product-doc evidence:** Transaction sync guides under feeds theme.
  - **Quick disprover:** DB: **security master** row for mapped id — **listed?** vs UI color. **If** mismatch → **H2**.
  - **Confidence:** medium

- **H3: Stale cache shows old mapping after master update**
  - **Why likely:** Less common for NextWorld but quick to rule out.
  - **Code evidence:** Cache keys in sync list API.
  - **Product-doc evidence:** `pi/user_manual/how_to_clear_cache_from_the_browser.md`.
  - **Quick disprover:** Hard refresh + re-run sync list. **If** color fixes → **H3**; else not.
  - **Confidence:** low

## Fast elimination plan

- **Check 1 (5 min):** Pick one **green** bad txn → note **feed symbol** and **resolved position id** from detail API.
- **Check 2 (10 min):** Verify **mapping rule** coverage for that symbol in DB.
- **Check 3 (15 min):** Compare **listed** attribute on security vs UI CSS class in DOM.""",
    "PI-3973": """## Root cause (hypothesis)

**Grouped MF holdings** view computes **holding cost** with a **sign/FX/aggregation** bug for **Fixed Income** bucket (Nippon Liquid BeES), or exposes **short-sell visibility** math per `pi/docs/pi-special-cases.md`—distinct from true economic negative position.

## Competing hypotheses

- **H1: Rollup aggregation double-flips sign for one sub-row in grouped asset class**
  - **Why likely:** Negative **holding cost** in **grouped** view only suggests SUM across child rows with wrong sign join.
  - **Code evidence:** `controller/app/common/transaction/MutualFundTransaction.php`, `controller/app/common/report/ReportTransaction.php` — grouped holdings queries.
  - **Product-doc evidence:** `pi/user_manual/README.md` — equity/funds themes; `pi/docs/pi-special-cases.md` (short sell visibility).
  - **Quick disprover:** Run same security **ungrouped** vs **grouped by asset class**; dump **constituent row costs** from API. **If** constituents sum ≠ displayed group total → **H1**.
  - **Confidence:** high

- **H2: INR FX translation uses wrong rate or cost basis column for ETF**
  - **Why likely:** INR display with underlying USD or odd instrument type.
  - **Code evidence:** MF valuation + FX columns in report SQL.
  - **Product-doc evidence:** FX adjustment guides in `pi/user_manual/`.
  - **Quick disprover:** Compare **local vs INR** columns for same row; **If** local sane and INR wrong → **H2**.
  - **Confidence:** medium

- **H3: Expected visibility change (special case doc) misread as defect**
  - **Why likely:** Short quantities now visible; client interprets as wrong negative.
  - **Code evidence:** Report quantity sign fields for the position.
  - **Product-doc evidence:** `pi/docs/pi-special-cases.md`.
  - **Quick disprover:** Confirm position is **short** or **margin**; reconcile with doc. **If** matches → **H3** triage not code bug.
  - **Confidence:** medium

## Fast elimination plan

- **Check 1 (5 min):** API JSON for **grouped** row **total** vs **drill-down** children for Nippon BeES.
- **Check 2 (10 min):** Same report **un-grouped** — **If** negative disappears → **H1**.
- **Check 3 (15 min):** Custodian vs AV **quantity** sign for entity **Myron** on **23-Feb-2026** → **H3**.""",
    "PI-2260": """## Root cause (hypothesis)

**PAR (beta)** widget uses **open quantity** as **closing** when **period activity** is not merged—bug in **beta JS** (`optimise_cfi_beta.js`) or **PAR API** snapshot missing **transaction deltas** for the selected window.

## Competing hypotheses

- **H1: Front-end PAR table copies open → closing columns without applying period movements**
  - **Why likely:** Symptom literal: open == closing always.
  - **Code evidence:** `controller/public/fancy/optimise_cfi_beta.js` (PAR beta).
  - **Product-doc evidence:** `pi/user_manual/setting_up_user_dashboard_access_to_the_report_book_.md`.
  - **Quick disprover:** Network: inspect **PAR API** payload — **If** `closing` already equals `open` in JSON → **H2** backend; **If** API correct but DOM wrong → **H1**.
  - **Confidence:** high

- **H2: PAR backend returns static snapshot ignoring trade date filter**
  - **Why likely:** Beta endpoint may default **as-of** to inception.
  - **Code evidence:** `rg -n "par|PAR|cfi_beta" controller/app av_v3_lambda` (discover handler).
  - **Product-doc evidence:** Report Book PAR guide if present in `pi/user_manual/`.
  - **Quick disprover:** CURL PAR endpoint with entity + period including known buy; **If** closing unchanged → **H2**.
  - **Confidence:** medium

- **H3: Feature flag routes to legacy quantity field that is “open only”**
  - **Why likely:** Constants / toggles miswire field names.
  - **Code evidence:** `controller/app/library/etcetera/Constants.php` near PAR flags.
  - **Product-doc evidence:** N/A.
  - **Quick disprover:** Toggle **PAR beta** off (if possible) — compare non-beta behavior for same data.
  - **Confidence:** low

## Fast elimination plan

- **Check 1 (5 min):** Inspect **API JSON** for open/closing fields before JS render.
- **Check 2 (10 min):** Known **buy** in period; regenerate — **If** API closing flat → **H2**.
- **Check 3 (15 min):** Breakpoint in `optimise_cfi_beta.js` assignment to closing column → **H1**.""",
    "PI-0808": """## Root cause (hypothesis)

**Cash flow widget** **group (All entities)** path **under-aggregates** interest and **capital repayment** vs **single-entity** run—likely **duplicate suppression**, **wrong GROUP BY**, or **entity-scope filter** dropping multi-entity bond cashflows.

## Competing hypotheses

- **H1: SQL/API aggregates bond cashflow once per ISIN instead of per entity-position in group mode**
  - **Why likely:** Bug example: bond in **3 entities** but group shows **one** interest payout.
  - **Code evidence:** `controller/app/common/calculation/FixedIncomeCalculationBonds.php`, `controller/public/fancy/capitalFlow.js`, `controller/app/common/report/ReportTransaction.php`.
  - **Product-doc evidence:** `pi/user_manual/cashflow_projection_widget_in_report_book.md`, `pi/user_manual/capital_flow_report_account_wise_drill_down_cash_roll_forward_report.md`.
  - **Quick disprover:** Log **SQL** or API rows for group run: count rows per **entity** for bond **Chaitanya…**. **If** count < 3 → **H1**.
  - **Confidence:** high

- **H2: Group run applies DISTINCT on narrative key that collapses multi-entity lines**
  - **Why likely:** De-dupe bug for “same” coupon payment.
  - **Code evidence:** `GROUP_CONCAT` / `DISTINCT` in cashflow query builders.
  - **Product-doc evidence:** Same cashflow guides.
  - **Quick disprover:** Remove `DISTINCT` locally in dev — **If** totals rise to sum of individuals → **H2**.
  - **Confidence:** medium

- **H3: FX or rounding difference makes group total appear lower though components exist**
  - **Why likely:** Less likely given “only one entity” symptom but quick check.
  - **Code evidence:** Currency conversion in widget aggregator.
  - **Product-doc evidence:** FX guides.
  - **Quick disprover:** Run group in **single currency** mode vs **mixed**; **If** issue persists → deprioritize **H3**.
  - **Confidence:** low

## Fast elimination plan

- **Check 1 (5 min):** Export **group** cashflow lines to Excel; count lines for sample bond vs **3** expected entities.
- **Check 2 (10 min):** Compare **sum(individual entity amounts)** for same bond vs **group** total.
- **Check 3 (15 min):** Trace query builder branch: `isGroup` / `all entities` flag in PHP or JS → **H1/H2**.""",
    "PI-5343": """## Root cause (hypothesis)

**Yearly** period in **Report Book → General Ledger / Income Statement** widget uses **calendar-year** or **month bucket** labeling (e.g. **December 2025**) instead of **April–March FY** columns when user expects Indian FY presentation.

## Competing hypotheses

- **H1: Widget maps “Yearly” to Dec–Dec or last month of fiscal period label string only**
  - **Why likely:** Header formatter uses `Date.getMonth()` calendar month.
  - **Code evidence:** Report Book GL widget JS (search `rg -n "Yearly|income.*statement|Report Book" dashboard/src controller/public/js`); lambda only if data comes pre-bucketed — `av_v3_lambda` paths in seed list are weak; prefer **controller/dashboard** widget code after `rg` discovery.
  - **Product-doc evidence:** `pi/user_manual/how_to_generate_an_income_statement_from_the_general_ledger_in_report_book.md`, `pi/user_manual/general_ledger_-_multi-period_income_statement.md`.
  - **Quick disprover:** API returns FY buckets but UI prints **Dec 2025** → **H1** pure label bug. **If** API months wrong → **H2**.
  - **Confidence:** high

- **H2: Entity fiscal-year start month not passed from Report Book widget to report API**
  - **Why likely:** Defaults to Jan–Dec when entity FY is Apr–Mar.
  - **Code evidence:** Request payload from widget: `fiscalYearStart` or equivalent missing.
  - **Product-doc evidence:** `pi/user_manual/setting_up_entities_and_groups.md` (entity fiscal settings if documented).
  - **Quick disprover:** Compare payload **entity FY** param for **Report Book** vs **standalone** GL income statement screen.
  - **Confidence:** medium

- **H3: Test tenant `shaileshssotest0912december` has December-named data seed confusing testers (display correct, data odd)**
  - **Why likely:** Fuzzy URL match artifact.
  - **Code evidence:** N/A — data audit.
  - **Product-doc evidence:** N/A.
  - **Quick disprover:** Reproduce on **second tenant** with known Apr–Mar FY. **If** issue universal → reject **H3**.
  - **Confidence:** low

## Fast elimination plan

- **Check 1 (5 min):** Network payload + response: are **period keys** FY-apr-mar aligned? **If** no → **H2**.
- **Check 2 (10 min):** Standalone **Multi-Period Income Statement** with Yearly — **If** correct there but wrong in Report Book → **widget-only H1/H2**.
- **Check 3 (15 min):** Second tenant reproduction → **H3**.""",
    "PI-6139": """## Root cause (hypothesis)

**Transaction sync** colors (**green** vs **red**) and **security mapping** state diverge: either **listed/unlisted** check uses wrong field, **CSS class** mapping is inverted, or **master** data missing makes **unlisted** txn show as healthy.

## Competing hypotheses

- **H1: Highlight uses “sync success” bit instead of “security resolved” bit**
  - **Why likely:** Green = posted, red = error—but PI expects red when security missing.
  - **Code evidence:** `rg -n "unlisted|listed|highlight|green|red" controller/app/modules` for transaction sync.
  - **Product-doc evidence:** `pi/user_manual/README.md` — transactions/feeds.
  - **Quick disprover:** DOM: class names on green row vs server JSON **securityId** null? **If** null still green → **H1**.
  - **Confidence:** high

- **H2: Wrong security master row linked (maps to delisted placeholder marked listed)**
  - **Why likely:** Mapping points to garbage master.
  - **Code evidence:** Resolution query joining **transaction → security**.
  - **Product-doc evidence:** N/A.
  - **Quick disprover:** DB: resolved **security id** on sample txn — **listed** flag value vs narrative “unlisted”.
  - **Confidence:** medium

- **H3: Client-specific rule pack for Altium overrides default colors**
  - **Why likely:** Tenant config feature flags.
  - **Code evidence:** Tenant-scoped JS config.
  - **Product-doc evidence:** N/A.
  - **Quick disprover:** Same build on **different tenant** with same data shape. **If** only Altium → **H3**.
  - **Confidence:** low

## Fast elimination plan

- **Check 1 (5 min):** One txn: JSON **securityResolved** + **listed** + UI class.
- **Check 2 (10 min):** Master row for mapped security — **listed** column.
- **Check 3 (15 min):** Cross-tenant compare → **H3**.""",
}


def main() -> None:
    for path in sorted(SPECS_DIR.glob("PI-*.md")):
        item_id = path.stem
        text = path.read_text(encoding="utf-8")
        upgrade = UPGRADES.get(item_id)
        out = rebuild(text, item_id, upgrade)
        path.write_text(out, encoding="utf-8")
        print(path.name, "upgrade" if upgrade else "reorder-only")


if __name__ == "__main__":
    main()
