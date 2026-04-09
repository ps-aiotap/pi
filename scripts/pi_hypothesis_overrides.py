"""Per-PI tailored competing hypotheses + fast elimination (and optional primary line).

Used by generate_book2_specs_and_plans.py and apply_tailored_hypotheses.py."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

Competing = dict[str, str]
Pack = dict[str, Any]

TAILORED: dict[str, Pack] = {
    "PI-0808": {
        "primary": (
            "For **All entities** (group) scope, the cash-flow projection path is under-counting "
            "fixed-income cash inflows (interest and principal repayment) versus per-entity runs—consistent "
            "with aggregation keyed too coarsely (e.g. security/ISIN without entity) or over-aggressive "
            "de-duplication when the same bond appears in multiple entities."
        ),
        "competing": [
            {
                "title": "Group rollup loses rows per entity",
                "why": "Reporter described a bond held in **three** entities where the group report shows interest for **one** only—suggests entity dimension dropped from grouping, `JOIN`, or `WHERE` when parent/group is selected.",
                "code": "Cash-flow / report aggregation in `ReportTransaction.php` and bond cash-flow math in `FixedIncomeCalculationBonds.php` (trace group vs single-entity code paths).",
                "doc": "pi/user_manual/cashflow_projection_widget_in_report_book.md",
                "disprover": "For bond *Chaitanya India Fin Credit Pvt Ltd 10.55% 30-Sep-2026*, compare intermediate row counts (per entity vs group) in the same date range; if three entity-level rows exist before merge but one after, this hypothesis holds.",
                "confidence": "high",
            },
            {
                "title": "Incorrect de-duplication by security across entities",
                "why": "A guard against double-counting the same instrument might key only on security/master id and collapse legitimate per-entity positions.",
                "code": "`FixedIncomeCalculationBonds.php` and any shared “unique security” or map merge before summing cash flows.",
                "doc": "pi/user_manual/capital_flow_by_investment_-_drill_down_cash_flows_for_each_position_for_a_period.md",
                "disprover": "Log or breakpoint at merge/dedupe step; if distinct `(entity_id, security_id, account_id)` rows are folded into one, this is the bug.",
                "confidence": "medium",
            },
            {
                "title": "Group uses different date basis or filter than single-entity",
                "why": "Smaller group totals could follow a stricter as-on window or entity filter even when user expects a straight sum of entity widgets.",
                "code": "Request parameters and filters built for Report Book “All entities” vs one entity in dashboard/report-book code paths.",
                "doc": "pi/user_manual/capital_flow_report_account_wise_drill_down_cash_roll_forward_report.md",
                "disprover": "Dump API/report parameters for both runs; identical date range, entity inclusion list (implicit “all”), and classification filters rule this out.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Reproduce with the named bond on **each of the three entities** individually, then **All entities**; capture whether missing amounts match “two entities dropped” vs proportional scaling.",
            "Trace group path for cash-flow widget: confirm whether results are summed per `(entity, position)` or collapsed earlier; compare SQL/PHP aggregation keys to single-entity path.",
            "If persistence is identical, diff **response JSON** (or rendered series) between single-entity and group for the same period—locate first stage where row count drops.",
        ],
    },
    "PI-0200": {
        "primary": (
            "Electra shows far fewer imported transactions than custodian statements for accounts 6075, 9110, 9660—likely AV-side filtering, pagination/import batch limits, duplicate suppression, or account mapping—not necessarily incomplete Electra payload until proven."
        ),
        "competing": [
            {
                "title": "Electra API or import batch truncates or pages incorrectly",
                "why": "Statement line count exceeds rows persisted for the same statement period.",
                "code": "`IndexController.php` (`GetelectraTransaction`), Electra client usage in `wealth.js` / `Constants.php` (`ELECTRAURL`).",
                "doc": "pi/user_manual/README.md",
                "disprover": "Log raw Electra response count for one account/date range; if it matches statement rows but DB has fewer, reject; if API already short, escalate provider.",
                "confidence": "high",
            },
            {
                "title": "Account mapping or entity scope excludes some statement lines",
                "why": "Only a subset of Electra accounts or transaction types map into AV for entity 1950.",
                "code": "Feed mapping / account linkage for the three account ids; Electra import filters.",
                "doc": "pi/user_manual/map_and_sync_custodian's_electronic_data_feeds_to_your_av_system.md",
                "disprover": "Compare Electra account ids on each missing statement line vs AV mapped accounts; full overlap rejects this.",
                "confidence": "medium",
            },
            {
                "title": "Duplicate or status filter drops rows on ingest",
                "why": "Re-import logic may skip transactions already partially keyed or marked.",
                "code": "Electra persist path in `controller/app/common/transaction/` (search `electra`, `duplicate`).",
                "doc": "pi/user_manual/README.md",
                "disprover": "Find a specific missing statement line; search DB for same amount/date/reference; if absent entirely, not a display bug.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Pick one missing transaction from a statement: trace from Electra payload → import log → DB row for entity 1950 and accounts 6075, 9110, 9660.",
            "Compare **row counts** from raw API vs rows inserted in one import window.",
            "If raw data is complete, binary-search AV filters (date, account mapping, transaction type) for the first drop.",
        ],
    },
    "PI-0967": {
        "primary": (
            "Realized gain report with **Since inception** through **28 Feb 2026** and **Grandfathered LTCG** is **too slow** (>5 min) and may **time out** client-side—query cost, N+1 valuation passes, or oversized result materialization dominate over wrong filters."
        ),
        "competing": [
            {
                "title": "SQL/report engine scans excessive history for tax-lot / LTCG logic",
                "why": "Grandfathered LTCG expands tax-lot work across full inception range.",
                "code": "`controller/app/modules/reports/controllers/IndexController.php` and gains report builders (search `gain`, `ltcg`, `grandfather`).",
                "doc": "pi/user_manual/gains_report__filter_tax-lot_wise_realized_&_unrealized_gains_by_desired_grouping.md",
                "disprover": "Run same entity with a **1-year** window; if runtime collapses, scope/cost hypothesis holds.",
                "confidence": "high",
            },
            {
                "title": "Client browser OOM or UI lock on expand/export",
                "why": "Blue Ocean tenant may hit memory or single-threaded export limits even when server finishes.",
                "code": "Dashboard report grid / export (`dashboard/src/app/`, `wealth.js` report paths).",
                "doc": "pi/user_manual/gains_report__filter_tax-lot_wise_realized_&_unrealized_gains_by_desired_grouping.md",
                "disprover": "Run identical report via API or smaller browser window; if server fast but UI still fails, UI-side.",
                "confidence": "medium",
            },
            {
                "title": "Environment or data skew (entity size, indexes)",
                "why": "Works internally but client data volume or missing DB index amplifies the same query plan.",
                "code": "DB explain on slow query; compare row counts for *Santara Capital And Management Consultants LLP*.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Explain plan on HC UAT clone with production stats; missing index or full table scan confirms.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Profile server time for the exact filter set vs a **narrower date range** on the same entity.",
            "Capture **HTTP timeout** vs **200 with delay** from browser network tab.",
            "If server is fast, reproduce **export** vs **on-screen** separately to split UI vs backend.",
        ],
    },
    "PI-1002": {
        "primary": (
            "Manage Account blocks **new security** when **exchange** differs—likely masters validation (unique symbol+exchange, listing rules) or a stale client check—not persistence of unrelated modules."
        ),
        "competing": [
            {
                "title": "Server rejects symbol+exchange combination",
                "why": "Error on save points to PHP validation in masters/security create.",
                "code": "`controller/app/modules/masters/` — security create/save; search `exchange`, `security`.",
                "doc": "pi/user_manual/selection_of_exchange_for_listed_indian_equity.md",
                "disprover": "Read API error payload / PHP log on submit; generic validation message with field names confirms.",
                "confidence": "high",
            },
            {
                "title": "Manage Account UI sends wrong exchange id or cached form state",
                "why": "Client-side script may not bind exchange dropdown to payload.",
                "code": "Masters Angular/JS for manage account security flow (narrower than jQuery bundles in seed hotspots).",
                "doc": "pi/user_manual/how_to_perform_custom_account_mapping.md",
                "disprover": "Compare POST body exchange field to user selection in DevTools; mismatch confirms.",
                "confidence": "medium",
            },
            {
                "title": "Tenant or role flag disables multi-exchange securities",
                "why": "Policy gate unrelated to generic JS libraries.",
                "code": "Settings / feature flags for listed equity per tenant.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Same steps on HC training tenant; if succeeds, compare tenant config.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Capture **failed request** response body and stack trace from logs.",
            "Retry with **same symbol** and **default exchange** that works—isolate exchange-specific branch.",
            "Grep masters controller for the exact **error string** shown in the screenshot.",
        ],
    },
    "PI-1216": {
        "primary": (
            "**Profit Share** (e.g. S&N 7.393 → 7.392) changed without user-visible audit—either **rounding/recalculation** on re-run, **silent partnership allocation** job, or **audit trail gap** for that field."
        ),
        "competing": [
            {
                "title": "Stored profit-share field was updated by batch or partnership recalculation",
                "why": "Value drift across dates matches backend recomputation more than random UI glitch.",
                "code": "`controller/app/modules/partnership/` and related allocation jobs (search `profit`, `share`).",
                "doc": "pi/user_manual/generating_voucher_audit_report.md",
                "disprover": "DB audit/version table or binlog for the partnership row on 11/1/25; no update rejects.",
                "confidence": "high",
            },
            {
                "title": "Display rounding differs from stored precision",
                "why": "Small delta (0.001) may be formatting-only.",
                "code": "Report/view layer formatting partnership percentages.",
                "doc": "pi/user_manual/change_in_net_worth_roll-forward_movement_of_the_balance_sheet_view_of_assets_and_liabilities.md",
                "disprover": "Query raw DB value for the field; unchanged vs displayed confirms.",
                "confidence": "medium",
            },
            {
                "title": "Audit product does not log profit-share edits",
                "why": "Entity audit excludes this column by design.",
                "code": "`controller/app/modules/settings/models/Auditreport.php` and partnership write paths.",
                "doc": "pi/user_manual/generating_voucher_audit_report.md",
                "disprover": "Confirm schema of audited columns for partnership; if profit share absent, expected gap.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Pull **current raw value** for the partnership profit share from DB vs UI.",
            "Search **application logs / jobs** around the date client re-ran the report.",
            "Define whether **audit** should cover profit share; if yes, file follow-up for logging gap.",
        ],
    },
    "PI-1635": {
        "primary": (
            "**Select all** on Transaction Sync includes **greyed auto-sync accounts**, leading to **duplicate syncs** and broken uncheck state—selection model does not respect the auto-sync exclusion flag."
        ),
        "competing": [
            {
                "title": "TreeGrid “check all” ignores disabled-row semantics",
                "why": "Parent checkbox selects every child row regardless of `auto sync` / disabled styling.",
                "code": "`dashboard/src/app/asset-vantage/dashboard/widget/widget-charts/sync-treeGrid/`",
                "doc": "pi/user_manual/map_and_sync_custodian's_electronic_data_feeds_to_your_av_system.md",
                "disprover": "After check-all, inspect selected id list in component state; if auto-sync ids present, confirmed.",
                "confidence": "high",
            },
            {
                "title": "Backend processes duplicate account ids when UI sends overlapping selection",
                "why": "Server may not de-duplicate accounts in one sync run.",
                "code": "Transaction sync API in `controller/` (search `sync`, `account`).",
                "doc": "pi/user_manual/README.md",
                "disprover": "Log request body for Start Sync; duplicate account ids confirm.",
                "confidence": "medium",
            },
            {
                "title": "Post-sync UI does not refresh selection model",
                "why": "Visual state stale after run completes.",
                "code": "Same sync TreeGrid component lifecycle after sync success callback.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Full page reload clears bad selection; if yes, client state bug.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Reproduce: note **account ids** selected vs **auto-sync** flags before Start Sync.",
            "Confirm **duplicate transactions** in DB for one affected account.",
            "Patch check-all handler to **skip** non-selectable rows; retest uncheck-all.",
        ],
    },
    "PI-2260": {
        "primary": (
            "PAR (beta) shows **closing quantity = open quantity** with no adds/reductions—period activity not applied in the beta PAR engine or wrong period bounds on the widget."
        ),
        "competing": [
            {
                "title": "Beta PAR calculation omits intra-period movements",
                "why": "Closing should roll open ± activity; equality implies activity array empty or ignored.",
                "code": "`controller/public/fancy/optimise_cfi_beta.js` and linked PAR beta services; `dashboard/.../report-book/`.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Compare PAR beta API payload quantities vs legacy PAR or ledger for same security/date.",
                "confidence": "high",
            },
            {
                "title": "Date filter uses point-in-time open only",
                "why": "Widget passes as-on date that bypasses range transactions.",
                "code": "Report Book PAR widget request parameters.",
                "doc": "pi/user_manual/setting_up_user_dashboard_access_to_the_report_book_.md",
                "disprover": "Inspect request: missing start/end range confirms.",
                "confidence": "medium",
            },
            {
                "title": "Caching returns stale PAR snapshot",
                "why": "UI shows old computed grid.",
                "code": "Client cache keys for report book widgets.",
                "doc": "pi/user_manual/how_to_clear_cache_from_the_browser.md",
                "disprover": "Hard refresh / incognito with new data; if fixed, cache.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Pick a security with **known buys/sells** in range; verify ledger quantity change.",
            "Trace **network response** for PAR beta: open, activity, closing fields.",
            "Compare **non-beta** PAR or holding report for same filters.",
        ],
    },
    "PI-3673": {
        "primary": (
            "Dalton Report Book **slowness** and **blank widgets** after cache warm—likely **client memory pressure**, **failed widget API** swallowed by UI, or **session/auth** edge—not generic persistence bugs."
        ),
        "competing": [
            {
                "title": "Per-widget API errors leave blank tiles without surfacing toast",
                "why": "Some widgets error while others load; matches intermittent blanks.",
                "code": "`dashboard/src/app/asset-vantage/report-book/` — widget loaders and error handlers.",
                "doc": "pi/user_manual/how_to_clear_cache_from_the_browser.md",
                "disprover": "Network tab: 4xx/5xx on blank widgets; parity confirms.",
                "confidence": "high",
            },
            {
                "title": "Heavy dashboard exhausts browser memory (large tenant)",
                "why": "Slowness + blank after many widgets match OOM or tab limits.",
                "code": "Angular change detection + chart libs in report book.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Reproduce with **fewer widgets** on layout; if stable, load issue.",
                "confidence": "medium",
            },
            {
                "title": "Server-side timeouts on expensive report APIs",
                "why": "Slowness is backend; UI shows empty on timeout.",
                "code": "`controller/app/common/report/ReportTransaction.php` and report module timeouts.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Server log slow query / 504 timestamp aligned with blank tile.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Open DevTools **Console + Network** while loading full Report Book.",
            "Retry with **half the widgets** removed from layout.",
            "Compare **HC Dalton** vs smaller tenant with same build.",
        ],
    },
    "PI-3751": {
        "primary": (
            "After **Plaid** mapping in masters, **accounts stay hidden**—mapping row exists but **visibility query** (entity, feed status, or Plaid link flag) excludes them from the picker/list."
        ),
        "competing": [
            {
                "title": "Mapped accounts filtered by active Plaid connection or sync state",
                "why": "UI lists only “ready” linked accounts.",
                "code": "`controller/app/modules/settings/controllers/IndexController.php`, Plaid handlers; `AccountTransaction.php` for account visibility.",
                "doc": "pi/user_manual/how_to_connect_your_account_via_plaid.md",
                "disprover": "DB: mapped rows present but `visible`/status column not active; confirms.",
                "confidence": "high",
            },
            {
                "title": "Entity or user permission hides new accounts until cache refresh",
                "why": "Masters saved but session-scoped list stale.",
                "code": "Account list APIs for masters grid.",
                "doc": "pi/user_manual/creating_various_masters_using_bulk_file_upload.md",
                "disprover": "Cold session / incognito shows accounts; if yes, cache.",
                "confidence": "medium",
            },
            {
                "title": "Wrong tenant or sandbox Plaid item vs production mapping",
                "why": "CohnReznick Sanders demo environment mismatch.",
                "code": "Plaid item id storage per tenant (`Constants`, settings).",
                "doc": "pi/user_manual/how_to_connect_your_account_via_plaid.md",
                "disprover": "Verify Plaid `item_id` and institution on the rows that should appear.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Query **account / mapping tables** for expected Plaid accounts after save.",
            "Hit the **same API** the UI uses for the account list; diff with UI.",
            "Confirm **Plaid webhook / link** status in logs for the integration.",
        ],
    },
    "PI-3973": {
        "primary": (
            "**Holding cost** negative for *Nippon India ETF Liquid BeES* under grouped view—likely **cost basis / accrual sign** in MF holding math or **FX/INR translation** of components, not literal negative position."
        ),
        "competing": [
            {
                "title": "Accrued interest or fee components subtracted twice in holding cost",
                "why": "FI/MF hybrid classification may use wrong formula for ETF/debt-like MF.",
                "code": "`controller/app/modules/wealth/` holding cost; `MutualFundTransaction.php` cost basis.",
                "doc": "pi/user_manual/adding_tds_field_to_mutual_fund,_direct_equity,_fixed_income_&_private_equity_modules.md",
                "disprover": "Break holding cost into cost, accrual, FX; find double-counted negative leg.",
                "confidence": "high",
            },
            {
                "title": "Grouping (Asset class FI + Holdings name) applies wrong aggregation sign",
                "why": "Sub-rows net incorrectly at parent.",
                "code": "Wealth register aggregation query for grouped view.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Drill to lot level: if lots non-negative but parent negative, aggregation bug.",
                "confidence": "medium",
            },
            {
                "title": "Stale price or rate used on as-on date",
                "why": "Mark causes artificial negative cost.",
                "code": "Valuation snapshot for the as-on date.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Recalc with manual price override; if sign flips, data.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Reproduce on **23-Feb-2026** for *Myron Wealth Management Private Limited* with drill-down.",
            "Export **lot-level cost** components for the security.",
            "Compare **non-grouped** holdings row vs grouped parent total.",
        ],
    },
    "PI-4426": {
        "primary": (
            "Copy **21 custom mappings** yields **2 persisted** and a **misleading success count (23)**—split between **`copyMappingsToAccounts` merge/iscopy** logic and **UI counting** default+custom rows together."
        ),
        "competing": [
            {
                "title": "Server copy path drops rows (constraint, merge, or iscopy flag)",
                "why": "Only 2 rows land in target account.",
                "code": "`AccountTransaction.php` — `copyMappingsToAccounts` (~6184+); `iscopy` / merge (~5852+).",
                "doc": "pi/user_manual/how_to_perform_custom_account_mapping.md",
                "disprover": "Count `feedmappingdetails` for target after copy; if 2, server-side.",
                "confidence": "high",
            },
            {
                "title": "Success toast counts selected defaults as “custom”",
                "why": "User selected all including defaults; message says 23 custom incorrectly.",
                "code": "`defaultaccountlist.phtml` + client script for selection count.",
                "doc": "pi/user_manual/how_to_perform_custom_account_mapping.md",
                "disprover": "Select **only** known custom rows; if copy count matches, messaging bug.",
                "confidence": "medium",
            },
            {
                "title": "Target list query filters out copied rows on reload",
                "why": "DB correct but UI filter hides new mappings.",
                "code": "Post-copy read API / grid filter (custom vs default).",
                "doc": "pi/user_manual/how_to_perform_custom_account_mapping.md",
                "disprover": "Raw DB has 21; UI shows 2—query filter confirmed.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "After copy, **SQL count** mappings on target vs source.",
            "Repeat with **only custom** rows selected (exclude defaults).",
            "Step through **`copyMappingsToAccounts`** for one failing row.",
        ],
    },
    "PI-5343": {
        "primary": (
            "**Yearly** income statement shows **December 2025** instead of **Apr–Mar FY**—period label / fiscal-year config for the GL widget is calendar-year or locale-default, not Indian FY."
        ),
        "competing": [
            {
                "title": "Widget uses calendar-year rollup for “Yearly”",
                "why": "December label matches Dec YTD calendar interpretation.",
                "code": "General Ledger income statement report builder (`controller/app/modules/reports/`); GL widget params from dashboard.",
                "doc": "pi/user_manual/general_ledger_-_multi-period_income_statement.md",
                "disprover": "Inspect report request: `fiscal_year_start` or period type; if Jan–Dec, confirmed.",
                "confidence": "high",
            },
            {
                "title": "Tenant fiscal calendar not applied to Report Book GL",
                "why": "Masters have FY Apr–Mar but widget ignores.",
                "code": "Tenant settings for financial year; report parameter mapping.",
                "doc": "pi/user_manual/how_to_generate_an_income_statement_from_the_general_ledger_in_report_book.md",
                "disprover": "Other GL reports respect FY; if yes, widget-only gap.",
                "confidence": "medium",
            },
            {
                "title": "Pure label bug (data is FY but header wrong)",
                "why": "Underlying numbers span Apr–Mar but title shows Dec.",
                "code": "Date formatting in widget header.",
                "doc": "pi/user_manual/general_ledger_-_multi-period_income_statement.md",
                "disprover": "Sum line items vs known FY totals; if match, label only.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Capture **request JSON** for Yearly period from Network tab.",
            "Compare **transaction date filter** in SQL/logs to expected Apr–Mar range.",
            "Cross-check **tenant FY** setting in masters.",
        ],
    },
    "PI-6026": {
        "primary": (
            "**Open Lot Report** empty for **JNJ** while **wealth register / UGL** show data—tax-lot / open-lot query uses **stricter filters** (lot status, wash sale, account, or instrument id) that exclude this holding."
        ),
        "competing": [
            {
                "title": "Open-lot API requires lots with open quantity > 0 in tax-lot table",
                "why": "Position exists in WR but lots closed or not materialized.",
                "code": "`av_v3_lambda/src/AUMReport/par_response.py`, `PerformanceApiReport/par_response.py`; `ReportTransaction.php` open lot paths.",
                "doc": "pi/user_manual/gains_report__filter_tax-lot_wise_realized_&_unrealized_gains_by_desired_grouping.md",
                "disprover": "Query tax-lot rows for JNJ for entity; empty explains blank report.",
                "confidence": "high",
            },
            {
                "title": "Entity or account filter on report mismatches WR",
                "why": "User runs open lot on subset account.",
                "code": "Open lot report filter handling.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Run with **all accounts**; if appears, filter bug.",
                "confidence": "medium",
            },
            {
                "title": "Instrument mapping (CUSIP/ ticker) differs between WR and open-lot source",
                "why": "Lot query keys on different security id.",
                "code": "Security alias / mapping tables.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Join WR position security_id to lot table key; mismatch confirms.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Confirm **entity** and **account** scope on both WR and Open Lot runs.",
            "Inspect **tax-lot rows** for JNJ (quantity, status).",
            "Compare **security id** used in WR vs open-lot API response.",
        ],
    },
    "PI-6139": {
        "primary": (
            "Transaction Sync shows **green** for rows that should be **invalid security (red)**—status/color rules disagree with **actual mapping resolution** for “unlisted” securities."
        ),
        "competing": [
            {
                "title": "UI status uses cached mapping while detail view uses fresh lookup",
                "why": "Grid color wrong; drill-down shows different mapping state.",
                "code": "Transaction sync grid component + API (`dashboard/`, `controller/` sync list).",
                "doc": "pi/user_manual/map_and_sync_custodian's_electronic_data_feeds_to_your_av_system.md",
                "disprover": "API returns `mapped=true` for green rows but security master missing; inconsistent payload confirms.",
                "confidence": "high",
            },
            {
                "title": "Unlisted security detection flag wrong for Altium feed rows",
                "why": "Classification of “unlisted” vs mapped differs by custodian.",
                "code": "Feed mapping transaction classes for Altium.",
                "doc": "pi/user_manual/map_and_sync_custodian's_electronic_data_feeds_to_your_av_system.md",
                "disprover": "Row metadata: `listed` / `security_id` null but color green.",
                "confidence": "medium",
            },
            {
                "title": "Process action validates stricter rule than list coloring",
                "why": "Green allows select; process rejects.",
                "code": "Process/sync POST validation vs list GET.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Compare two endpoints’ mapping checks for same transaction id.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Pick one **green** problem row: capture **list API** fields vs **process** error.",
            "Verify **security master** exists for mapped id.",
            "Align **color rule** with documented unlisted/missing-security states.",
        ],
    },
    "PI-6393": {
        "primary": (
            "PCR auto-sync deposits transactions into **Unidentified**—**PCR parser / mapping** or **account-security linkage** for NextWorld is not resolving custodian ids to AV masters."
        ),
        "competing": [
            {
                "title": "PCR mapping file or account id mismatch for this tenant",
                "why": "Unidentified bucket is default when account or symbol unknown.",
                "code": "`pcr/` pipeline + `controller/app/common/transaction/` unidentified routing.",
                "doc": "pi/user_manual/map_and_sync_custodian's_electronic_data_feeds_to_your_av_system.md",
                "disprover": "Log first unidentified row: missing account or symbol key; fix mapping and retest.",
                "confidence": "high",
            },
            {
                "title": "Auto-sync job uses different credentials or file slice than manual import",
                "why": "Subset of rows lack context only in auto path.",
                "code": "Auto-sync scheduler vs manual PCR upload.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Same file manual vs auto: if manual maps, job config.",
                "confidence": "medium",
            },
            {
                "title": "Security master missing for PCR symbols",
                "why": "Rows cannot attach to instrument.",
                "code": "Security creation from PCR feed.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Create missing masters; replay row—if identified, data gap.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Sample **10 unidentified** rows: extract custodian account and symbol from raw PCR.",
            "Verify **AV account mapping** and **security** exist.",
            "Replay one file through **PCR dev** with debug logging.",
        ],
    },
    "PI-6479": {
        "primary": (
            "A **custom account mapping** appears as both **withdrawal and deposit** (contradiction)—likely **stale feed mapping rows**, **system-protected mapping**, or **duplicate opposites** from import that UI will not delete."
        ),
        "competing": [
            {
                "title": "Two opposing mapping rows exist for same feed line pattern",
                "why": "User sees contradiction; delete blocked as system mapping.",
                "code": "`controller/app/common/transaction/Feedmapping/` and masters delete rules.",
                "doc": "pi/user_manual/how_to_perform_custom_account_mapping.md",
                "disprover": "Query feed mapping table for account pair; two rows with opposite txn types confirm.",
                "confidence": "high",
            },
            {
                "title": "System-generated mapping cannot be removed via UI",
                "why": "Client needs data fix or admin path.",
                "code": "Flags on mapping rows (`system`, `protected`).",
                "doc": "pi/user_manual/how_to_perform_custom_account_mapping.md",
                "disprover": "Column indicates system-owned; UI delete disabled by design.",
                "confidence": "medium",
            },
            {
                "title": "Display bug shows wrong txn type label",
                "why": "Single row but UI mislabels.",
                "code": "Masters grid rendering for mappings.",
                "doc": "pi/user_manual/how_to_perform_custom_account_mapping.md",
                "disprover": "DB shows one consistent type; UI shows both—render bug.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Export **mapping rows** for the affected account from DB.",
            "Identify **which row** is system vs user.",
            "Apply approved **data cleanup** or product rule for contradictions.",
        ],
    },
    "PI-6526": {
        "primary": (
            "**Newly provisioned client** missing features vs reference tenant—**license / feature package**, **template client** copy incompleteness, or **role permissions**—not transaction code paths."
        ),
        "competing": [
            {
                "title": "Feature flags or modules not enabled for new org",
                "why": "SWAT-style new client setup skipped entitlements.",
                "code": "`controller/app/modules/settings/`, license/module tables.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Compare `module` / `feature` tables to a known-good tenant.",
                "confidence": "high",
            },
            {
                "title": "User roles missing menu entries",
                "why": "Features exist but RBAC hides them.",
                "code": "Role-permission assignment for admin user.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Login as superadmin; if visible, RBAC.",
                "confidence": "medium",
            },
            {
                "title": "Wrong template client used at creation",
                "why": "Clone source was minimal.",
                "code": "Client onboarding / clone scripts.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Check provisioning record for template id.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Document **which features** are missing (menus, modules).",
            "Diff **settings** vs benchmark tenant on HC.",
            "Verify **license** line items for the new client id.",
        ],
    },
    "PI-6587": {
        "primary": (
            "**Custodian Recon** returns **no data** for selected securities with **3/12–3/12** date—likely **zero-width date range**, **timezone midnight**, or **recon query** requiring activity on both sides when none exists."
        ),
        "competing": [
            {
                "title": "Single-day range excludes custodian file window",
                "why": "File posts T-1 or different TZ; query returns empty.",
                "code": "`ReconciliationController.php`, `ReconciliationReport.php`, `wealth.js` recon.",
                "doc": "pi/user_manual/map_and_sync_custodian's_electronic_data_feeds_to_your_av_system.md",
                "disprover": "Widen to ±3 days; if data appears, date logic.",
                "confidence": "high",
            },
            {
                "title": "Security selection not passed to recon query",
                "why": "UI shows pick but API omits filter → empty set.",
                "code": "Recon request builder from `wealth.js` to PHP.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Network payload missing `securityIds` confirms.",
                "confidence": "medium",
            },
            {
                "title": "No custodian file ingested for Acadia on that date",
                "why": "True data gap.",
                "code": "Feed file receipt logs for custodian.",
                "doc": "pi/user_manual/map_and_sync_custodian's_electronic_data_feeds_to_your_av_system.md",
                "disprover": "Confirm file landed and parsed for 3/12.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Reproduce with **wider date** and note result.",
            "Verify **custodian file** presence for the security and date.",
            "Inspect **recon API** query parameters in Network tab.",
        ],
    },
    "PI-6815": {
        "primary": (
            "**Decimal quantity** user preference (**6** places) ignored in **grid view** but honored elsewhere—**grid column formatter** or **DataTables/ej2** column def hard-codes 2 decimals."
        ),
        "competing": [
            {
                "title": "Grid uses fixed `toFixed(2)` or pipe ignoring user setting",
                "why": "Non-grid view reads preference; grid does not.",
                "code": "`wealth.js` / dashboard grid config for quantity column (search `decimal`, `quantity`).",
                "doc": "pi/user_manual/README.md",
                "disprover": "Find formatter with literal 2; replace with setting—issue resolves.",
                "confidence": "high",
            },
            {
                "title": "Widget-specific setting not subscribed to preference change",
                "why": "Preference saved but grid not invalidated.",
                "code": "User preference service + grid refresh.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Reload page after save: if 6 appears, event wiring.",
                "confidence": "medium",
            },
            {
                "title": "Server returns rounded quantity for grid endpoint only",
                "why": "API shape differs by view.",
                "code": "Grid vs detail API field precision.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Compare JSON number full precision in both endpoints.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Search codebase for **quantity** format in **grid** components vs **detail** view.",
            "Confirm **preference key** persisted for decimal quantity.",
            "Patch grid to use **shared formatting** helper.",
        ],
    },
    "PI-7486": {
        "primary": (
            "**Fixed Income report**: **Summation Amount** blank per **Strategy** while row data exists—**subtotal row** not populated in query or **DataTables footer** mis-bound, not raw transaction absence."
        ),
        "competing": [
            {
                "title": "Strategy-level aggregate not computed in report SQL",
                "why": "Detail lines exist but summary column null.",
                "code": "`controller/app/modules/reports/` fixed income report; `FixedIncomeCalculationBonds.php` if used.",
                "doc": "pi/user_manual/booking_of_accrued_interest_on_coupon_bearing_fixed_income_securities_to_the_balance_sheet.md",
                "disprover": "Inspect report JSON: `strategyTotal` missing/null confirms.",
                "confidence": "high",
            },
            {
                "title": "Front-end table hides or fails to render footer for grouped strategies",
                "why": "Data present wrong column index.",
                "code": "jQuery DataTables config for FI report (see hotspots).",
                "doc": "pi/user_manual/README.md",
                "disprover": "Raw response has totals; DOM lacks cell—UI.",
                "confidence": "medium",
            },
            {
                "title": "Strategy dimension null on rows so rollup key missing",
                "why": "Cannot sum to bucket.",
                "code": "Strategy assignment on positions for FI report.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Rows have `strategy_id` null; if yes, master data.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Inspect **API JSON** for strategy subtotals before DataTables.",
            "Pick one strategy with detail lines: **sum manually** vs expected column.",
            "Fix **server aggregate** first, then **column binding**.",
        ],
    },
    "PI-8345": {
        "primary": (
            "**CSV export** from **Voucher Audit** grid has **misaligned headers**—classic **extra/missing delimiter**, **quoted field with comma**, or **export omitting hidden columns** vs header row."
        ),
        "competing": [
            {
                "title": "Header row built from column defs that do not match data row order",
                "why": "Grid view columns differ from export pipeline.",
                "code": "`wealth.js` voucher audit export; GL voucher audit handlers.",
                "doc": "pi/user_manual/generating_voucher_audit_report.md",
                "disprover": "Count columns in header vs first data line in CSV; mismatch confirms.",
                "confidence": "high",
            },
            {
                "title": "Unescaped comma in voucher text shifts cells",
                "why": "Data fields break CSV grammar.",
                "code": "CSV builder must quote fields.",
                "doc": "pi/user_manual/generating_voucher_audit_report.md",
                "disprover": "Open in text editor; find unquoted comma in row.",
                "confidence": "medium",
            },
            {
                "title": "Excel locale opens UTF-8 CSV with wrong delimiter",
                "why": "User perception of misalignment.",
                "code": "*(Client Excel)* — delimiter/encoding on import, not AV export code.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Open same file in Google Sheets; if aligned, client Excel settings.",
                "confidence": "low",
            },
        ],
        "fast_plan": [
            "Download CSV and **diff header count** vs first line field count.",
            "Search export code for **join** of row cells.",
            "Add **integration test** with voucher text containing commas.",
        ],
    },
    "PI-9273": {
        "primary": (
            "Extra **`\\` in Security Name / identifier** breaks **mapping and process**—**escape handling** double-escapes feed text or JSON corrupts display; edit form loads **blank security**."
        ),
        "competing": [
            {
                "title": "Ingestion stores escaped string that does not match master lookup",
                "why": "Green status but process fails; matcher uses cleaned key.",
                "code": "`BaseFeedMappingTransaction.php` and sync normalization (slashes, JSON).",
                "doc": "pi/user_manual/map_and_sync_custodian's_electronic_data_feeds_to_your_av_system.md",
                "disprover": "Compare raw feed text to `security_name` column; extra backslash only in AV confirms.",
                "confidence": "high",
            },
            {
                "title": "UI JSON encoding adds escape on display",
                "why": "Feed file clean; screen shows `\\`.",
                "code": "Angular/JS template binding for sync grid.",
                "doc": "pi/user_manual/README.md",
                "disprover": "API returns clean string; UI shows escaped—front-end.",
                "confidence": "medium",
            },
            {
                "title": "Process validation requires exact security match including stray char",
                "why": "Edit screen blank because invalid security id after parse.",
                "code": "Process transaction validation path.",
                "doc": "pi/user_manual/README.md",
                "disprover": "Strip slash in test harness; process succeeds.",
                "confidence": "medium",
            },
        ],
        "fast_plan": [
            "Compare **feed file line** to **DB stored description** for one txn.",
            "Trace **first transformation** that injects `\\`.",
            "Normalize **identifier fields** on ingest (single unescape pass).",
        ],
    },
}


def competing_markdown(hypo_list: list[Competing]) -> str:
    parts: list[str] = []
    for i, h in enumerate(hypo_list):
        parts.extend(
            [
                f"- **H{i + 1}: {h['title']}**",
                f"  - Why likely: {h['why']}",
                f"  - Code evidence: {h['code']}",
                f"  - Product-doc evidence: `{h['doc'].strip('`')}`",
                f"  - Quick disprover: {h['disprover']}",
                f"  - Confidence: **{h['confidence']}**",
            ]
        )
    return "\n".join(parts)


def fast_plan_markdown(items: list[str]) -> str:
    return "\n".join(f"- {c}" for c in items)


def patch_spec_content(text: str, iid: str) -> str | None:
    """Replace competing hypotheses + fast plan; set primary line in Root cause. Returns None if no override."""
    pack = TAILORED.get(iid)
    if not pack:
        return None

    competing = pack["competing"]
    fast_items = pack["fast_plan"]
    new_competing = "## Competing hypotheses\n\n" + competing_markdown(competing)
    new_fast = "## Fast elimination plan\n\n" + fast_plan_markdown(fast_items)

    text, n = re.subn(
        r"## Competing hypotheses\n\n.*?## Fast elimination plan\n\n.*?(?=\n## Proposed fix)",
        new_competing + "\n\n" + new_fast,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if n != 1:
        return None

    primary = pack.get("primary")
    if primary is not None:
        hypo_line = f"- **Hypothesis:** {primary}\n"
        if re.search(r"^- \*\*Hypothesis:\*\* ", text, re.MULTILINE):
            text = re.sub(
                r"^- \*\*Hypothesis:\*\*[^\n]+\n",
                hypo_line,
                text,
                count=1,
                flags=re.MULTILINE,
            )
        else:
            text = text.replace(
                "## Root cause (hypothesis)\n\n",
                "## Root cause (hypothesis)\n\n" + hypo_line,
                1,
            )

    return text


def patch_spec_file(spec_path: Path) -> bool:
    raw = spec_path.read_text(encoding="utf-8")
    iid = spec_path.stem
    updated = patch_spec_content(raw, iid)
    if updated is None:
        return False
    spec_path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "specs"
    n = 0
    for iid in sorted(TAILORED):
        p = root / f"{iid}.md"
        if not p.exists():
            print("skip missing", p.name)
            continue
        if patch_spec_file(p):
            print("patched", p.name)
            n += 1
        else:
            print("failed pattern", p.name)
    print("done", n)


if __name__ == "__main__":
    main()
