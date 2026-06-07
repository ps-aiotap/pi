#!/usr/bin/env python3
"""Regenerate pi/specs/PI-*.md and pi/test-plans/PI-*.md from Book2.csv.

Output shape matches the intake bar set by pi/specs/PI-6587.md:
Metadata, Client environment URL (clickable HC UAT), Suggested assignment,
Issue summary, Reported behavior, Reproduction / symptoms (subsections),
Root cause hypothesis (>=3 concrete hypotheses), Fast elimination plan,
Fix options, Impact, Acceptance criteria, Open questions, Evidence.

Reuses discovery helpers from generate_book2_specs_and_plans.py (client match,
manual/code discovery, team suggestion).

Usage:
  python3 pi/scripts/full_book2_generator.py --csv pi/input/Book2.csv --no-move
"""

from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = ROOT.parent

# Hand-refined specs to never overwrite
SKIP_IDS = frozenset({"PI-6587"})


def load_gb():
    path = ROOT / "scripts" / "generate_book2_specs_and_plans.py"
    spec = importlib.util.spec_from_file_location("gb", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


gb = load_gb()


def strip_ticks(s: str) -> str:
    return (s or "").strip().strip("`")


def narrative(row: dict) -> str:
    """Prefer real bug text; ignore bogus 'Days until Resolution' duration-only strings."""
    n = gb.narrative_text(row).strip()
    if not n:
        return ""
    if re.fullmatch(r"\d+\s+days?\s+\d+(?:\.\d+)?\s+hours?", n, flags=re.I):
        return ""
    if re.fullmatch(r"0\s+days\s+0\s+hours", n, flags=re.I):
        return ""
    return n


def doc_key(row: dict) -> str:
    return gb.doc_key(row)


def hc_link(url: str) -> str:
    if not url:
        return ""
    return f"**HC UAT URL:** [{url}]({url})"


def _catalog_match_hostname(hostname_token: str, clients: list) -> tuple[str, str] | None:
    """Match first DNS label (no hc prefix) to client_name."""
    tok = re.sub(r"^hc", "", hostname_token.lower())
    n = gb.norm(tok)
    hits = [(cn, url) for cn, url, nn in clients if nn == n]
    if len(hits) == 1:
        return hits[0]
    return None


def client_environment_markdown(row: dict, clients: list) -> str:
    cn_col = (row.get("Client Name") or "").strip()
    name = (row.get("Name") or "").strip()
    bug = narrative(row)
    combined = f"{name} {bug}"

    # Hostname from narrative beats fuzzy tokens (avoids spurious `management` → wrong tenant).
    for m in re.finditer(r"https?://([a-z0-9-]+)\.assetvantage\.(?:com|in)", combined, re.I):
        hit = _catalog_match_hostname(m.group(1), clients)
        if hit:
            cat, url = hit
            hc = gb.tenant_hc_uat(url)
            lines = [
                "- **Match type:** From URL",
                f"- **Match notes:** Hostname matched catalog tenant `{cat}`.",
                "",
            ]
            if hc:
                lines.append(hc_link(hc))
            return "\n".join(lines)

    pm = gb.primary_match(cn_col, clients)
    if pm:
        cat, url = pm
        hc = gb.tenant_hc_uat(url)
        lines = [
            "- **Match type:** Primary (**Client Name** vs catalog).",
            f"- **Match notes:** Catalog tenant `{cat}`.",
            "",
        ]
        if hc:
            lines.append(hc_link(hc))
        return "\n".join(lines)

    fm = gb.fuzzy_match(name, bug, clients)
    if isinstance(fm, tuple):
        cat, url, tok = fm
        hc = gb.tenant_hc_uat(url)
        lines = [
            "- **Match type:** Fuzzy",
            f"- **Match notes:** Token `{tok}` matched `{cat}`.",
            "",
        ]
        if hc:
            lines.append(hc_link(hc))
        return "\n".join(lines)

    lines = [
        "- **Match type:** No confident catalog match.",
        "- **Match notes:** Confirm tenant from reporter before relying on HC UAT.",
        "",
        "**HC UAT URL:** *(not assigned — confirm tenant first)*",
    ]
    if isinstance(fm, str) and fm.startswith("ambiguous"):
        lines.insert(2, f"- **Ambiguity:** {fm}")
    return "\n".join(lines)


def infer_category(name: str, bug: str) -> str:
    t = f"{name} {bug}".lower()
    # Gains before generic "minutes/slow" performance (many gain PIs mention runtime).
    if any(
        x in t
        for x in (
            "gain report",
            "gains report",
            "realized gain",
            "grandfathered",
            "gains mismatch",
            "sell quantity",
            "unrealized sell",
        )
    ):
        return "gains_voucher"
    rules: list[tuple[list[str], str]] = [
        (["custodian recon"], "custodian_recon"),
        (["investment search", "search for an investment"], "security_search_ui"),
        (["multi-period", "income statement"], "income_statement_entity"),
        (["short sell", "short sell"], "short_sell_positions"),
        (["holding cost", "mutual fund"], "mf_valuation"),
        (["multi edit"], "multi_edit"),
        (["trial balance"], "trial_balance_drill"),
        (["demerger", "wealth registrar"], "demerger_cost"),
        (["specific lot"], "feed_specific_lot"),
        (["report book", "widget", "dashboard", "pdf export", "blank widget"], "report_book"),
        (["look through", "lookthrough"], "look_through"),
        (["custom account mapping", "payee", "payor"], "custom_account_mapping"),
        (["benchmark", "spsirbk", "stale"], "benchmark_prices"),
        (["transaction sync", "sync issue", "auto sync"], "transaction_sync_feed"),
        (["corporate action", "corp action"], "corporate_actions"),
        (["contract note", "upload pdf"], "contract_upload"),
        (["excel", "download excel", "xlsx"], "excel_export_equity"),
        (["bank recon", "reconcile"], "bank_reconciliation"),
        (["audit history", "entity"], "entity_audit_ui"),
        (["slowness", "slow", "minutes", "performance"], "performance_slow"),
        (["gains mismatch", "voucher"], "gains_voucher"),
        (["ledger", "schedule b", "tax report"], "ledger_tax"),
        (["twr", "mppr", "par ", "portfolio activity"], "twr_par_reports"),
        (["bulk upload", "transfer in"], "bulk_upload_transfer"),
        (["electra", "jefferies", "itau", "feed no transaction", "pcr"], "feed_pipeline"),
        (["undefined", " isin"], "categorization_feed"),
        (["double entry", "trial balance"], "trial_balance_double"),
        (["units held", "tallying"], "equity_units"),
        (["password protected"], "report_password"),
        (["refresh icon", "saved automatically"], "report_book_ux"),
        (["open lot"], "open_lot_report"),
        (["look through> csv", "csv file handling"], "lookthrough_csv"),
        (["expense", "coa template", "unclassified"], "coa_expense"),
        (["balance sheet", "wealth register", "market value"], "bs_wr_valuation"),
        (["aum", "no position"], "aum_report"),
        (["electra", "brokers not showing"], "feed_pipeline"),
    ]
    for keys, cat in rules:
        for k in keys:
            if k in t:
                return cat
    return "general_legacy"


def pick_hotspots(row: dict) -> list[str]:
    raw = gb.discover_code_hotspots(
        row.get("Module", "").strip(),
        row.get("Name", "").strip(),
        narrative(row),
        limit=8,
    )
    return [strip_ticks(x) for x in raw if strip_ticks(x)]


def pick_guides(row: dict) -> list[str]:
    return gb.discover_manual_guides(
        row.get("Module", "").strip(),
        row.get("Name", "").strip(),
        narrative(row),
        limit=5,
    )


def fallback_code_paths(category: str) -> list[str]:
    """Known-real paths as fallback when token discovery is weak."""
    m: dict[str, list[str]] = {
        "custodian_recon": [
            "controller/app/common/report/ReconciliationReport.php",
            "controller/app/modules/wealth/controllers/ReconciliationController.php",
        ],
        "gains_voucher": [
            "controller/app/common/report/GainsReport.php",
            "controller/app/common/report/GainsReportData.php",
        ],
        "report_book": [
            "controller/app/common/transaction/ReportBookTransaction.php",
            "controller/app/common/models/ReportBooks.php",
        ],
        "trial_balance_drill": [
            "controller/app/common/report/ReportTransaction.php",
        ],
        "transaction_sync_feed": [
            "controller/app/common/transaction/Feedmapping/BaseFeedMappingTransaction.php",
        ],
        "feed_pipeline": [
            "controller/app/common/transaction/Feedmapping/BaseFeedMappingTransaction.php",
        ],
        "look_through": [
            "controller/app/common/report/ReportTransaction.php",
        ],
        "performance_slow": [
            "controller/app/common/report/ReportTransaction.php",
        ],
        "general_legacy": [
            "controller/app/modules/wealth/controllers/ReconciliationController.php",
        ],
    }
    cand = m.get(category, m["general_legacy"])
    out = []
    for p in cand:
        if (WORKSPACE_ROOT / p).is_file():
            out.append(p)
    return out[:5]


def merge_hotspots(primary: list[str], category: str) -> list[str]:
    """Prefer domain fallback files (GainsReport, ReconciliationReport, …) over noisy token hits."""
    fb = fallback_code_paths(category)
    prefer_first = category in (
        "gains_voucher",
        "custodian_recon",
        "report_book",
        "transaction_sync_feed",
        "feed_pipeline",
    )
    seq = (fb + [p for p in primary if p not in fb]) if prefer_first else (primary + fb)
    seen: set[str] = set()
    out: list[str] = []
    for p in seq:
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out[:8]


def hypothesis_pack(
    category: str,
    name: str,
    bug: str,
    hotspots: list[str],
    guides: list[str],
) -> list[dict[str, str]]:
    doc = guides[0] if guides else "pi/user_manual/README.md"
    doc2 = guides[1] if len(guides) > 1 else doc
    c0 = hotspots[0] if hotspots else "controller/app/common/controllers/BaseController.php"
    c1 = hotspots[1] if len(hotspots) > 1 else c0
    c2 = hotspots[2] if len(hotspots) > 2 else c1

    sym = bug[:280].replace("\n", " ").strip()

    packs: dict[str, list[dict[str, str]]] = {
        "gains_voucher": [
            {
                "title": "Lot-level gains aggregation differs from voucher GL posting",
                "why": f"Symptoms ({sym[:120]}…) suggest realized/unrealized lot logic in gains export/grid diverges from voucher amounts.",
                "code": f"`{c0}` — gains aggregation / export path",
                "doc": doc,
                "disprover": "Compare voucher line amounts for the same txn id vs gains grid row raw JSON/SQL intermediate for one security.",
                "confidence": "medium",
            },
            {
                "title": "Report filters (holding scope / date) change quantity basis for grid export",
                "why": "Export-all-holdings vs single-holding runs can apply different filters.",
                "code": f"`{c1}` — report parameter binding",
                "doc": doc2,
                "disprover": "Run gains for single ISIN vs all holdings; diff request payload and row keys.",
                "confidence": "medium",
            },
            {
                "title": "Short-sell / visibility sign handling affects displayed sell quantity",
                "why": "If short-sell quantity visibility changed, historical rows may look inconsistent across WR vs gains.",
                "code": f"`{c2}`",
                "doc": "pi/docs/pi-special-cases.md (short-sell visibility nuance)",
                "disprover": "Check quantity sign in DB vs report column for the flagged lot ids.",
                "confidence": "low",
            },
            {
                "title": "Stale cache or saved report parameter session",
                "why": "Saved parameters could reuse prior period or entity filter.",
                "code": f"`{c0}`",
                "doc": doc,
                "disprover": "Hard refresh session, clear saved report prefs, rerun with explicit dates.",
                "confidence": "low",
            },
            {
                "title": "FX / reporting currency conversion boundary",
                "why": "Voucher may post in account currency while gains grid uses another basis.",
                "code": f"`{c1}`",
                "doc": doc,
                "disprover": "Log currency columns on voucher vs gains for the txn.",
                "confidence": "low",
            },
        ],
        "report_book": [
            {
                "title": "Widget refresh / PDF render pipeline drops late-loaded series",
                "why": sym[:200],
                "code": f"`{c0}` — report book transaction / widget assembly",
                "doc": doc,
                "disprover": "Capture network responses for each widget before PDF; compare to PDF layout engine input.",
                "confidence": "medium",
            },
            {
                "title": "Angular dashboard state vs saved dashboard definition",
                "why": "Unsaved filter changes may still persist on navigation for some tenants.",
                "code": f"`{c1}`",
                "doc": doc,
                "disprover": "Diff widget filter payload on Save vs implicit navigation exit.",
                "confidence": "medium",
            },
            {
                "title": "Cache warming / Redis widget cache incomplete",
                "why": "Heavy dashboards may timeout partial widgets server-side.",
                "code": f"`{c2}`",
                "doc": doc,
                "disprover": "Compare widget API latency and payload size good vs bad tenant.",
                "confidence": "medium",
            },
            {
                "title": "PDF generator viewport vs browser grid layout",
                "why": "PDF export uses different layout rules than on-screen grid.",
                "code": f"`{c0}`",
                "doc": doc,
                "disprover": "Export same dashboard to PDF and screenshot grid; map missing sections to HTML/CSS.",
                "confidence": "low",
            },
            {
                "title": "Password / gateway feature flag mismatch per environment",
                "why": "Gateway-enabled options may not propagate to client stack.",
                "code": f"`{c1}`",
                "doc": doc,
                "disprover": "Read effective feature flags JSON for tenant on HC vs prod.",
                "confidence": "low",
            },
        ],
        "custodian_recon": [
            {
                "title": "As-of date normalization yields empty holdings window",
                "why": "Corner date display (e.g. single-day range) may not match internal txndate used in queries.",
                "code": "`controller/app/common/report/ReconciliationReport.php` — `getReconciliationData` date handling",
                "doc": "pi/user_manual/reconcile_custodian_account_investment_holdings,_cash_balances_and_tax_lots_with_feeds.md",
                "disprover": "Log `txndate` request param vs `getLookByDate` inputs for failing account.",
                "confidence": "medium",
            },
            {
                "title": "Feed holdings missing for identifiers on recon date",
                "why": "PCR/feed row absence breaks join by ISIN/CUSIP/Symbol.",
                "code": f"`{c0}`",
                "doc": doc,
                "disprover": "Query feed holdings table for account+identifiers on recon date.",
                "confidence": "medium",
            },
            {
                "title": "WR subset empty before feed compare",
                "why": "`getWrReportData` returned no positions for parameters.",
                "code": "`controller/app/common/report/ReconciliationReport.php`",
                "doc": doc,
                "disprover": "Compare WR row count vs recon JSON row count for same scope.",
                "confidence": "medium",
            },
            {
                "title": "`reconciliation` vs `reconciliationbeta` module split",
                "why": "Different module flag may route to alternate controller/view.",
                "code": "`controller/app/modules/wealth/controllers/ReconciliationController.php`",
                "doc": doc,
                "disprover": "Confirm tenant feature flags for beta recon.",
                "confidence": "low",
            },
            {
                "title": "Client-side grid filter hides rows present in payload",
                "why": "Selection of securities may filter JSON rows incorrectly.",
                "code": "`controller/app/modules/wealth/views/index/reconciliation/listgrid.phtml`",
                "doc": doc,
                "disprover": "Diff JSON `jsonTable` vs DOM row count.",
                "confidence": "low",
            },
        ],
        "general_legacy": [
            {
                "title": "Legacy PHP request parameter normalization mismatch",
                "why": f"Symptoms in narrative may stem from bind/sanitize differences at controller entry ({sym[:100]}…).",
                "code": f"`{c0}`",
                "doc": doc,
                "disprover": "Log raw POST vs mapped PHP vars for failing vs passing case.",
                "confidence": "medium",
            },
            {
                "title": "Persistence layer partial write or transform before commit",
                "why": "Field transforms in model save could diverge from UI expectation.",
                "code": f"`{c1}`",
                "doc": doc,
                "disprover": "Compare submitted payload columns to DB row after save.",
                "confidence": "medium",
            },
            {
                "title": "Read/report query filter excludes valid rows",
                "why": "Saved data exists but list/report SQL filters it out.",
                "code": f"`{c2}`",
                "doc": doc,
                "disprover": "Run SQL/API with filter toggles and compare row deltas.",
                "confidence": "medium",
            },
            {
                "title": "Formatter / phtml rendering defect",
                "why": "Correct API payload but wrong display.",
                "code": f"`{c0}`",
                "doc": doc,
                "disprover": "Compare API JSON field to rendered cell for same id.",
                "confidence": "low",
            },
            {
                "title": "Tenant-specific configuration or master data gap",
                "why": "Org settings, COA, or security master incomplete for workflow.",
                "code": f"`{c1}`",
                "doc": doc,
                "disprover": "Diff masters vs reference tenant where flow works.",
                "confidence": "low",
            },
        ],
    }

    # Map specialized categories to existing packs or general
    alias = {
        "performance_slow": "report_book",
        "feed_pipeline": "transaction_sync_feed",
        "transaction_sync_feed": "transaction_sync_feed",
        "bank_reconciliation": "custodian_recon",
        "bulk_upload_transfer": "general_legacy",
        "excel_export_equity": "general_legacy",
        "mf_valuation": "general_legacy",
        "coa_expense": "general_legacy",
        "security_search_ui": "general_legacy",
        "income_statement_entity": "general_legacy",
        "short_sell_positions": "gains_voucher",
        "demerger_cost": "general_legacy",
        "feed_specific_lot": "transaction_sync_feed",
        "look_through": "report_book",
        "custom_account_mapping": "transaction_sync_feed",
        "benchmark_prices": "report_book",
        "corporate_actions": "general_legacy",
        "contract_upload": "general_legacy",
        "entity_audit_ui": "general_legacy",
        "ledger_tax": "general_legacy",
        "twr_par_reports": "gains_voucher",
        "categorization_feed": "transaction_sync_feed",
        "trial_balance_double": "trial_balance_drill",
        "trial_balance_drill": "general_legacy",
        "equity_units": "gains_voucher",
        "report_password": "report_book",
        "report_book_ux": "report_book",
        "open_lot_report": "gains_voucher",
        "lookthrough_csv": "report_book",
        "bs_wr_valuation": "general_legacy",
        "aum_report": "report_book",
    }

    key = alias.get(category, category)
    key = alias.get(key, key)
    if key in packs:
        hyps = packs[key]
    elif key == "transaction_sync_feed":
        hyps = [
            {
                "title": "Feed mapping / categorization drops or mis-tags transactions",
                "why": sym[:200],
                "code": f"`{c0}`",
                "doc": doc,
                "disprover": "Inspect staging rows for txn ids vs AV mapped type.",
                "confidence": "medium",
            },
            {
                "title": "Auto-sync selection includes greyed accounts leading to duplicates",
                "why": "Checkbox logic may sync unintended accounts.",
                "code": f"`{c1}`",
                "doc": doc,
                "disprover": "Compare selected account ids payload vs UI checked state screenshot.",
                "confidence": "medium",
            },
            {
                "title": "PCR file arrived but job did not parse date window",
                "why": "File-level filter might exclude rows client expects.",
                "code": f"`{c2}`",
                "doc": doc,
                "disprover": "Verify job log line count vs raw file row count.",
                "confidence": "medium",
            },
            {
                "title": "Undefined bucket overflow when feed attributes incomplete",
                "why": "Mapped security name present but classification rules fail.",
                "code": f"`{c0}`",
                "doc": doc,
                "disprover": "Trace categorization rule chain for sample txn.",
                "confidence": "low",
            },
            {
                "title": "Concurrency / duplicate posting on historical sync",
                "why": "Re-posting deleted txns suggests idempotency gap.",
                "code": f"`{c1}`",
                "doc": doc,
                "disprover": "Audit txn hash keys in sync insert path.",
                "confidence": "low",
            },
        ]
    else:
        hyps = packs["general_legacy"]

    # Rewrite code paths to discovered files where templates used fixed strings only in custodian pack — others already use c0,c1,c2
    return hyps[:5]


def fast_elimination(hypotheses: list[dict[str, str]]) -> str:
    h0 = hypotheses[0]["title"] if hypotheses else "primary divergence"
    h1 = hypotheses[1]["title"] if len(hypotheses) > 1 else h0
    return "\n".join(
        [
            f"- **Check 1 (5 min):** Capture failing request + first JSON/SQL touchpoint. If payload wrong at wire → **{h0}**; else continue.",
            f"- **Check 2 (10 min):** Verify persisted rows for same entity/account/date. If DB correct but UI/report wrong → **{h1}**; else persistence path.",
            f"- **Check 3 (15 min):** Compare one known-good tenant/account vs failing — first layer where outputs diverge owns the defect.",
        ]
    )


def fix_options_md(category: str) -> str:
    return "\n".join(
        [
            "- **Option A (minimal):** Patch the narrowest branch (single query/filter/format) confirmed by elimination checks.",
            "- **Option B (structural):** Consolidate duplicated report/feed logic into one service with shared tests; higher blast radius.",
            "- **Risks / rollback:** Feature-flag if available; otherwise revert and rerun targeted regression from `pi/test-plans/{ItemId}.md`.",
        ]
    )


def reproduction_block(name: str, bug: str, guides: list[str], category: str) -> str:
    pre = [
        "### Preconditions",
        "",
        "- Use the **HC UAT URL** from **Client environment URL** when a tenant match exists; otherwise confirm tenant with reporter.",
        "- Roles: user can reach the module implied by this PI (reports, transactions, feeds, or masters as applicable).",
        "",
        "**Unknown / confirm with reporter:**",
        "",
        "- Exact entity, accounts, securities, and date range from production narrative.",
        "",
        "### Steps",
        "",
    ]
    # Category-flavored first steps (always concrete; no “refer to manual”).
    cat_steps: dict[str, list[str]] = {
        "custodian_recon": [
            "1. Open **Transactions** → **Reconciliation** → **Custodian Reconciliation**.",
            "2. Select the **Entity** (or group) and **custodian account(s)** involved.",
            "3. Set the **as-of date** for reconciliation and run/refresh the report.",
            "4. Locate the securities described in the PI and observe position vs feed rows.",
        ],
        "gains_voucher": [
            "1. Open **Analytics** (or **Reports**) → **Gains Report** (path may vary by tenant packaging).",
            "2. Select **Entity**, **Account**, **Report period**, and filters matching the PI (e.g. realized / LTCG).",
            "3. Run the report in **grid** and/or **export** as described in the PI.",
            "4. Open the related **voucher** or GL drill for the same transaction ids.",
        ],
        "report_book": [
            "1. Open **Report Book** and load the named **dashboard** (or group report).",
            "2. Ensure filters and **Save** state match the PI (refresh widgets if required).",
            "3. Reproduce **on-screen** behavior, then **PDF export** (or other export) if the PI involves export.",
            "4. Compare widget-by-widget output vs expectation.",
        ],
        "transaction_sync_feed": [
            "1. Open **Transaction Sync** (or feed-driven sync entry point used by the tenant).",
            "2. Select **Entity** and **accounts** per the PI.",
            "3. Run sync / review staging or **Undefined** bucket as described.",
            "4. Compare to source custodian file or PCR reference if available.",
        ],
        "general_legacy": [
            "1. Sign in to the confirmed tenant (**HC UAT** when assigned).",
            "2. Navigate to the module implied by the PI title (use **Reports**, **Transactions**, **Masters**, or **Feeds** as appropriate).",
            "3. Apply the **filters, entities, and dates** from the PI narrative.",
            "4. Repeat the user actions until the defect appears (save, export, refresh, or sync as relevant).",
        ],
    }
    steps_key = category if category in cat_steps else "general_legacy"
    steps = cat_steps[steps_key]

    trace = ""
    if guides:
        trace = (
            "\n### Traceability (optional)\n\n"
            f"- Guides consulted for navigation wording: {', '.join('`' + g + '`' for g in guides[:3])}. "
            "Not required to reproduce; for maintainers only.\n"
        )

    symptom = bug.strip() if bug.strip() else name

    return (
        "\n".join(pre)
        + "\n".join(steps)
        + "\n\n### Symptom check\n\n"
        + f"- **Expected:** Behavior consistent with product docs and comparable tenants.\n"
        + f"- **Actual (per PI):** {symptom[:1200]}{'…' if len(symptom) > 1200 else ''}\n"
        + trace
    )


def escape_md_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def build_spec(row: dict, clients: list) -> str:
    did = doc_key(row)
    name = (row.get("Name") or "").strip()
    bug = narrative(row)
    module = (row.get("Module") or "").strip()
    iid = (row.get("Item ID") or row.get("ITEM ID") or "").strip()
    category = infer_category(name, bug)
    guides = pick_guides(row)
    hotspots = merge_hotspots(pick_hotspots(row), category)
    team, leader, rationale = gb.team_suggestion((row.get("TEAM") or "").strip(), name, bug)
    hyps = hypothesis_pack(category, name, bug, hotspots, guides)

    meta_rows = [
        ("Item ID", iid),
        ("Group", (row.get("Group") or "").strip()),
        ("Status", (row.get("Status") or "").strip()),
        ("Priority", (row.get("Priority") or "").strip()),
        ("Report Date", (row.get("Report Date") or "").strip()),
        ("Environment", (row.get("Environment") or "").strip()),
        ("Module", module),
        ("Reporter", (row.get("Reporter") or "").strip()),
        ("Assigned To", (row.get("Assigned To") or "").strip()),
        ("Developer", (row.get("Developer") or "").strip()),
        ("TEAM (CSV)", (row.get("TEAM") or "").strip()),
        ("Resolution", (row.get("Resolution") or "").strip()),
        ("Dev RCA", (row.get("Dev RCA") or "").strip()),
    ]
    meta = "\n".join(f"| {escape_md_cell(k)} | {escape_md_cell(v)} |" for k, v in meta_rows)

    assign = "\n".join(
        [
            f"- **Suggested Team:** {team}",
            f"- **Suggested Leader:** {leader}",
            f"- **Rationale:** {rationale}",
        ]
    )
    if (row.get("Developer") or "").strip():
        assign += f"\n- **CSV assignee note:** Developer `{row.get('Developer')}` / Assigned To `{row.get('Assigned To')}` — align ownership with squad lead."

    hyp_md = "\n\n".join(
        "\n".join(
            [
                f"{i + 1}. **{h['title']}**",
                f"   - **Why likely:** {h['why']}",
                f"   - **Code evidence:** {h['code']}",
                f"   - **Product-doc evidence:** `{h['doc'].strip().strip('`')}`",
                f"   - **Quick disprover:** {h['disprover']}",
                f"   - **Confidence:** {h['confidence']}",
            ]
        )
        for i, h in enumerate(hyps)
    )

    evidence_lines: list[str] = []
    zpath = ROOT / "input" / "pi-evidence" / f"{did}.zip"
    if zpath.is_file():
        evidence_lines.append(f"- Evidence archive: `pi/input/pi-evidence/{did}.zip`")
    ev_path = ROOT / "evidence-analysis" / f"{did}.md"
    if ev_path.is_file():
        evidence_lines.append(f"- Evidence analysis: `pi/evidence-analysis/{did}.md`")
    pic = (row.get("Picture/Video") or "").strip()
    if pic and "http" in pic:
        evidence_lines.append(f"- Monday **Picture/Video** / links: {pic[:500]}{'…' if len(pic)>500 else ''}")

    leakage = (row.get("Leakage RCA") or row.get("Dev RCA") or "").strip()
    notes = ""
    if leakage:
        notes = f"\n## Additional intake notes\n\n- Leakage RCA / classification: {leakage}\n"

    return f"""# {did}: {name}

## Metadata

| Field | Value |
|---|---|
{meta}

## Client environment URL

{client_environment_markdown(row, clients)}

## Suggested assignment

{assign}

## Issue summary

{name}

## Reported behavior

{bug if bug else "*(No narrative text in Monday export for this row.)*" }

## Reproduction / symptoms

{reproduction_block(name, bug, guides, category)}

## Root cause hypothesis

{hyp_md}

### Code hotspots (seed)

{chr(10).join(f"- `{h}`" for h in hotspots[:6]) if hotspots else "- *(No scored code hits — rely on elimination checks and deeper search.)*"}

## Fast elimination plan

{fast_elimination(hyps)}

## Fix options

{fix_options_md(category)}

## Impact / blast radius

- **Users:** Tenants running the same module path (see category **{category}**).
- **Systems:** Legacy PHP controller/report paths under `controller/` and related jobs when feeds are implicated.

## Acceptance criteria

- Symptom no longer reproduces on agreed environment with agreed entity/account/security scope.
- Elimination checks pass for the confirmed root-cause layer (wire vs persistence vs render vs feed file).
- Regression cases in `pi/test-plans/{did}.md` pass for touched layers.

## Open questions

- Confirm tenant if **HC UAT URL** was not assigned.
- Confirm whether behavior is **data/feed** vs **product defect** after Check 2.

## Evidence and references

{chr(10).join(evidence_lines) if evidence_lines else "- *(No zip or Monday media in export for this ItemId.)*" }

{notes}"""


def build_test_plan(did: str, name: str, row: dict, hotspots: list[str]) -> str:
    hs = "\n".join(f"| {i+1} | `{p}` | Seed from narrative + repo search |" for i, p in enumerate(hotspots[:6]))
    if not hs:
        hs = "| 1 | *(Refine during implementation)* | Run `generate_book2_specs_and_plans.discover_code_hotspots` after scope narrows |"

    return f"""# Test plan: {did}

## Scope and references

- Fix spec: [`pi/specs/{did}.md`](../specs/{did}.md)
- User manual: see **Root cause** and reproduction traceability in the fix spec; index at `pi/user_manual/README.md`.

## Code hotspots

| # | Path | Notes |
|---|------|-------|
{hs}

## Environment / data prerequisites

- HC UAT or reporter-confirmed tenant from the fix spec **Client environment URL**.
- Entity / account / security identifiers explicitly named in the PI narrative.

## Verify the fix

| # | Objective | Steps | Expected |
|---|------------|-------|----------|
| 1 | Primary symptom cleared | Reproduce PI path on agreed environment | Symptom absent |
| 2 | Same data edge case | Use failing account/security/date from PI | Correct output or explicit handled state |
| 3 | Export/PDF/widget if applicable | Repeat export path from PI | Parity with on-screen data |

## Regression

| Area | Code / UX anchor | Notes |
|------|------------------|-------|
| Same module | First hotspot path in table above | Happy path smoke |
| Adjacent | Sibling report or feed job sharing helper | No drift |
| Data integrity | DB row vs API payload | Consistent keys/amounts |

## Adjacent

- Only modules sharing code paths confirmed in the implementation PR.

## Automation mapping

| Layer | Location | Action |
|-------|----------|--------|
| PHPUnit | `controller/unittest/` | Add unit/integration for changed PHP class when fix lands |
| Angular | `dashboard/src/app/**/*.spec.ts` | Extend if dashboard/report book UI changed |
| API | `av-edge-api/` | Add if edge route involved |

**Manual-only:** Feed-file parity, custodian PDF compare, or tenant-specific masters may remain manual until stable fixtures exist.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=ROOT / "input" / "Book2.csv")
    ap.add_argument("--no-move", action="store_true")
    args = ap.parse_args()

    if not args.csv.exists():
        raise SystemExit(f"Missing {args.csv}")

    clients = gb.load_clients()
    (ROOT / "specs").mkdir(parents=True, exist_ok=True)
    (ROOT / "test-plans").mkdir(parents=True, exist_ok=True)

    import csv

    with args.csv.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        for row in csv.DictReader(f):
            did = doc_key(row)
            if not did:
                continue
            if did in SKIP_IDS:
                print("skip (preserved)", did)
                continue
            name = row.get("Name", "").strip()
            spec_body = build_spec(row, clients)
            category = infer_category(name, narrative(row))
            hotspots = merge_hotspots(pick_hotspots(row), category)
            (ROOT / "specs" / f"{did}.md").write_text(spec_body, encoding="utf-8")
            (ROOT / "test-plans" / f"{did}.md").write_text(
                build_test_plan(did, name, row, hotspots), encoding="utf-8"
            )
            print("wrote", did)

    if not args.no_move and args.csv.resolve() == (ROOT / "input" / "Book2.csv").resolve():
        proc = ROOT / "input" / "processed"
        proc.mkdir(parents=True, exist_ok=True)
        dest = proc / args.csv.name
        if dest.exists():
            dest.unlink()
        args.csv.rename(dest)
        print("moved", args.csv, "->", dest)


if __name__ == "__main__":
    main()
