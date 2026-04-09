#!/usr/bin/env python3
"""Generate pi/specs/{ItemId}.md and pi/test-plans/{ItemId}.md from pi/input/Book2.csv."""
from __future__ import annotations

import csv
import re
from pathlib import Path

from pi_hypothesis_overrides import TAILORED, competing_markdown, fast_plan_markdown

# Repo folder that contains input/, specs/, test-plans/ (the `pi/` tree).
ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "input" / "Book2.csv"
URL_DIR = ROOT / "input" / "urls"
SPECS = ROOT / "specs"
PLANS = ROOT / "test-plans"
USER_MANUAL_DIR = ROOT / "user_manual"
WORKSPACE_ROOT = ROOT.parent

# Code / UX anchors (seed from repo search; refine per PI)
HOTSPOTS: dict[str, str] = {
    "PI-9878": """- `pi/user_manual/billpay_integration_with_bill.com.md` — Bill.com / Billpay flows.
- `controller/app/common/transaction/` — ledger posting paths for partner-sourced transactions.
- Search: `rg -n "bill" controller/app` for Bill.com–related handlers.""",
    "PI-8327": """- `dashboard/src/app/asset-vantage/dashboard/` — widget load and data binding.
- `dashboard/src/app/test/component/dashboard.component.spec.ts` — dashboard shell tests.
- `dashboard/karma.conf.js` — Karma/Jasmine entry.""",
    "PI-2260": """- `dashboard/src/app/asset-vantage/report-book/` — Report Book UI.
- `pi/user_manual/setting_up_user_dashboard_access_to_the_report_book_.md` — access and navigation context.""",
    "PI-9799": """- `controller/app/modules/masters/controllers/IndexController.php` — Chart of Accounts / masters actions.
- `pi/user_manual/` — Chart of Accounts theme (see `pi/user_manual/README.md` index).""",
    "PI-0200": """- `controller/app/modules/masters/controllers/IndexController.php` — `GetelectraTransaction`, Electra feed name checks (see grep `Electra`).
- `controller/public/js/wealth.js` — `importElectraFeed` and related Electra UI.
- `controller/app/library/etcetera/Constants.php` — `ELECTRAURL` / Electra API base.""",
    "PI-6168": """- `controller/app/common/transaction/DirectEquityTransaction.php` — de-merger and related DE flows.
- `pi/user_manual/README.md` — Direct equity / corporate actions themes.""",
    "PI-4524": """- `controller/app/modules/investments/` — Morningstar / feed transaction ingestion (search `morningstar`, `G33`).
- `av_v3_lambda/` — feed/sync lambdas if this tenant uses API pipeline.""",
    "PI-0198": """- `controller/app/modules/settings/` — audit and user activity (`Auditreport`, `UseractivityController`).
- `controller/app/common/transaction/MutualFundTransaction.php` — MF persistence layer.
- `pi/user_manual/` — transaction entry and audit reports (operational reports theme).""",
    "PI-8136": """- `controller/app/common/transaction/LedgerTransaction.php` / feed posting — ledger line population from feed.
- `controller/app/common/transaction/BaseFeedMappingTransaction.php` — feed-to-ledger mapping.""",
    "PI-8002": """- `controller/app/modules/wealth/controllers/AccountreconciliationController.php` — bank reconciliation.
- `controller/app/common/report/ReconciliationReport.php` — reconciliation totals logic.""",
    "PI-1891": """- `balancesheet/` — balance sheet engine (sibling repo).
- `dashboard/src/app/asset-vantage/report-book/` — Portfolio Activity / Report Book presentation.
- `controller/app/modules/reports/` — report data APIs.""",
    "PI-0967": """- `controller/app/modules/reports/controllers/IndexController.php` — report generation endpoints.
- Search: `rg -l "gain" controller/app/modules/reports` — realized / LTCG report paths.""",
    "PI-6587": """- `controller/app/modules/wealth/controllers/ReconciliationController.php` — custodian reconciliation.
- `controller/public/js/wealth.js` — recon UI (large file; search `recon`).""",
    "PI-9220": """- `av-edge-api/app/routes/alpha_wrt_benchmark/` — benchmark / alpha vs benchmark (recent churn on `master`).
- `dashboard/src/app/asset-vantage/dashboard/widget/` — benchmark widgets.""",
    "PI-3673": """- `dashboard/src/app/asset-vantage/report-book/` — Report Book.
- `pi/user_manual/how_to_clear_cache_from_the_browser.md` — client-side cache guidance (symptom overlap).""",
    "PI-8535": """- `controller/app/modules/reports/` — Open Lot / holdings cost reports.
- Search: `rg -l "open.?lot" controller` (case-insensitive).""",
    "PI-6393": """- `pcr/` — PCR feed pipeline (sibling repo).
- `controller/app/common/transaction/` — unidentified / sync posting for feeds.""",
    "PI-1635": """- `dashboard/src/app/asset-vantage/dashboard/widget/widget-charts/sync-treeGrid/` — sync account selection UI.
- Search: `rg -l "sync" dashboard/src/app/asset-vantage/dashboard` — transaction sync screens.""",
    "PI-6479": """- `controller/app/common/transaction/Feedmapping/` — custom account mapping.
- `controller/app/modules/masters/controllers/IndexController.php` — account/feed master maintenance.""",
    "PI-4426": """- `controller/app/common/transaction/AccountTransaction.php` — `copyMappingsToAccounts` (~6184+), `feedmappingdetails` / `iscopy` paths (~5852+).
- `controller/app/modules/masters/views/index/account/defaultaccountlist.phtml` — account mapping UI (search copy / mapping).
- `pi/user_manual/how_to_perform_custom_account_mapping.md` — documented flow.""",
    "PI-7123": """- `balancesheet/` / `controller/app/modules/reports/` — WR vs PAR valuation continuity.
- `av_v3_lambda/` — performance/position APIs if used for PAR.""",
    "PI-3973": """- `controller/app/modules/wealth/` — holdings / wealth register presentation.
- Search: `rg -l "holding.?cost" controller` (case-insensitive).""",
    "PI-1216": """- `controller/app/modules/partnership/` or `controller/app/common/` — profit share / partnership allocations (search `profit`).
- `controller/app/modules/settings/models/Auditreport.php` — audit coverage gaps vs. entity history.""",
    "PI-2017": """- Search: `rg -l "arch" controller/app av_v3_lambda` — Arch security auto-create paths.
- `controller/app/modules/masters/` — security master lifecycle.""",
    "PI-8283": """- `controller/app/common/calculation/` — taxation / holding period for listed instruments.
- `pi/user_manual/README.md` — taxation / gains themes.""",
    "PI-9273": """- `controller/app/common/transaction/Feedmapping/BaseFeedMappingTransaction.php` — feed field normalization.
- Transformers ingestion — security identifier parsing (escape/backslash handling).""",
    "PI-9058": """- `controller/app/common/transaction/DirectEquityTransaction.php` — demerger-generated transfer in/out.
- Deletion cascades for generated child transactions.""",
    "PI-3962": """- `balancesheet/` — sold-out positions on balance sheet.
- `controller/app/modules/reports/` — BS vs wealth register consistency.""",
}

USER_MANUAL: dict[str, str] = {
    "PI-9878": "`pi/user_manual/billpay_integration_with_bill.com.md`, `pi/user_manual/bill_–_accounts_payable_partner_feature.md`",
    "PI-8327": "`pi/user_manual/setting_up_user_dashboard_access_to_the_report_book_.md` (dashboards), report book widgets index",
    "PI-2260": "`pi/user_manual/README.md` → Report book, widgets & charts",
    "PI-9799": "`pi/user_manual/README.md` → Chart of accounts",
    "PI-0200": "`pi/user_manual/README.md` → Feeds, statements & custodians",
    "PI-8002": "`pi/user_manual/README.md` → Feeds, statements & custodians; bank/cash operational guides as applicable",
    "PI-1891": "`pi/user_manual/README.md` → Report book & General ledger",
    "PI-1635": "`pi/user_manual/README.md` → Feeds, statements & custodians",
    "PI-3673": "`pi/user_manual/how_to_clear_cache_from_the_browser.md`, report book theme",
    "PI-8283": "Taxation / gains guides under `pi/user_manual/README.md`",
}

# Memoize expensive full-tree scans (one scan per distinct token set across the batch).
_HOTSPOT_CACHE: dict[tuple[str, ...], list[str]] = {}

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
    "into",
    "are",
    "not",
    "able",
    "showing",
    "show",
    "client",
    "issue",
    "when",
    "where",
    "which",
    "have",
    "has",
    "was",
    "were",
    "as",
    "on",
    "all",
    "any",
    "per",
    "via",
    "but",
    "you",
    "your",
    "can",
    "may",
    "should",
    "will",
    "found",
    "unable",
    "even",
    "like",
    "team",
    "positions",
}


def slug_accepts_token(tok: str, cn_norm: str) -> bool:
    """Avoid spurious fuzzy hits (e.g. token `found` inside `bellwetherfoundation`)."""
    if not tok or not cn_norm:
        return False
    if tok == cn_norm:
        return True
    if cn_norm.startswith(tok) or cn_norm.endswith(tok):
        return True
    if len(tok) < 8:
        return False
    return tok in cn_norm


def norm(s: str) -> str:
    s = (s or "").lower().strip()
    s = re.sub(r"[\s_\-]+", " ", s)
    return s


def load_clients() -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for csv_path in sorted(URL_DIR.glob("*.csv")):
        with csv_path.open(newline="", encoding="utf-8", errors="replace") as f:
            for row in csv.DictReader(f):
                cn = (row.get("client_name") or "").strip()
                url = (row.get("url") or "").strip()
                if cn and url:
                    out.append((cn, url, norm(cn)))
    return out


def tenant_hc_uat(catalog_url: str) -> str:
    """hc + first host label + .assetvantage.in per skill."""
    m = re.search(r"https?://([^.]+)\.", catalog_url)
    if not m:
        return ""
    tenant = m.group(1)
    return f"https://hc{tenant}.assetvantage.in"


def md_link(url: str) -> str:
    if not url:
        return ""
    return f"[{url}]({url})"


def primary_match(client_name: str, clients: list[tuple[str, str, str]]) -> tuple[str, str] | None:
    n = norm(client_name)
    if not n:
        return None
    hits = [(cn, url) for cn, url, cn_norm in clients if cn_norm == n]
    if len(hits) == 1:
        return hits[0]
    return None


def fuzzy_match(name: str, bug: str, clients: list[tuple[str, str, str]]) -> tuple[str, str, str] | str:
    """Returns (client_name, url, token) or 'none' or 'ambiguous: ...'"""
    text = f"{name} {bug}"
    tokens = set(re.findall(r"[a-zA-Z][a-zA-Z0-9]{3,}", text))
    tokens = {t.lower() for t in tokens if t.lower() not in STOPWORDS}
    # URL-like host hints
    for m in re.finditer(r"https?://([^.]+)\.assetvantage\.(?:com|in)", text, re.I):
        tokens.add(m.group(1).lower())

    best: dict[str, list[tuple[str, str]]] = {}
    for tok in tokens:
        hits = []
        for cn, url, cn_norm in clients:
            if cn_norm in tok and len(cn_norm) >= 4:
                hits.append((cn, url))
            elif slug_accepts_token(tok, cn_norm) or (
                len(tok) >= 4 and len(cn_norm) >= 4 and slug_accepts_token(cn_norm, tok)
            ):
                hits.append((cn, url))
        if hits:
            best[tok] = hits

    # Prefer unique single client across any token
    for tok, hits in sorted(best.items(), key=lambda x: -len(x[0])):
        uniq = list({h[0]: h for h in hits}.values())
        if len(uniq) == 1:
            return (uniq[0][0], uniq[0][1], tok)
    if not best:
        return "none"
    # ambiguous: summarize
    lines = []
    for tok, hits in list(best.items())[:5]:
        names = sorted({h[0] for h in hits})
        lines.append(f"`{tok}` → {', '.join(names[:6])}{'…' if len(names) > 6 else ''}")
    return "ambiguous: " + "; ".join(lines)


def narrative_text(row: dict) -> str:
    """Monday CSV exports often leave **Bug Description** empty and put text in **Days until Resolution**."""
    b = (row.get("Bug Description") or "").strip()
    if b:
        return b
    return (row.get("Days until Resolution") or "").strip()


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", (text or "").lower())
    return {w for w in words if w not in STOPWORDS}


def discover_manual_guides(iid: str, module: str, name: str, bug: str, limit: int = 3) -> list[str]:
    """Rank guides by token overlap with filename + content."""
    if iid in USER_MANUAL:
        # Preserve curated mapping first when present.
        return []

    query_tokens = tokenize(f"{module} {name} {bug}")
    if not query_tokens or not USER_MANUAL_DIR.exists():
        return []

    ranked: list[tuple[int, str]] = []
    for md in sorted(USER_MANUAL_DIR.glob("*.md")):
        if md.name.lower() == "readme.md":
            continue
        rel = f"pi/user_manual/{md.name}"
        filename_tokens = tokenize(md.stem.replace("_", " "))
        score = len(query_tokens & filename_tokens) * 4
        if score == 0:
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            text = ""
        # Add lightweight content signal without overfitting.
        content_hits = 0
        for tok in query_tokens:
            if tok in text:
                content_hits += 1
        score += min(content_hits, 8)
        ranked.append((score, rel))

    ranked.sort(key=lambda x: (-x[0], x[1]))
    return [rel for _, rel in ranked[:limit]]


def hypothesis_line(module: str, name: str, bug: str) -> str | None:
    """Return a concrete hypothesis when the PI text suggests one; otherwise omit (no generic filler)."""
    text = f"{module} {name} {bug}".lower()
    if "processing" in text or "stuck" in text or "save" in text:
        return (
            "Likely long-running or blocked transaction-processing path for this workflow "
            "(queue/job completion, validation gate, or post-save recalculation)."
        )
    if "not matching" in text or "mismatch" in text or "difference" in text:
        return (
            "Likely valuation/report parity gap: differing date basis, filter scope, "
            "or source table between compared reports."
        )
    if "no position" in text or "position" in text:
        return (
            "Likely position-resolution gap: upstream holdings not materialized for the report date "
            "or UI/report query applying an unintended filter."
        )
    if "feed" in text or "import" in text or "electra" in text or "morningstar" in text:
        return (
            "Likely ingestion/mapping issue where provider payload fields are not normalized "
            "to AV transaction/security expectations."
        )
    return None


def competing_hypotheses(module: str, name: str, bug: str, hotspots: list[str], guides: list[str]) -> list[dict[str, str]]:
    text = f"{module} {name} {bug}".lower()
    hot = hotspots[0] if hotspots else "`(no code match found)`"
    guide = guides[0] if guides else "`pi/user_manual/README.md`"

    if "processing" in text or "stuck" in text or "save" in text:
        return [
            {
                "title": "Async completion path stalls after save",
                "why": "Symptom reports transaction stuck at processing after save.",
                "code": hot,
                "doc": guide,
                "disprover": "Check job/queue state for the transaction; if completion event exists and status still pending, reject this hypothesis.",
                "confidence": "high",
            },
            {
                "title": "Validation gate blocks post-save transition",
                "why": "Workflow accepts input but does not finalize transaction state.",
                "code": hot,
                "doc": guide,
                "disprover": "Replay with same payload while logging validation outcomes; no failed guard means reject.",
                "confidence": "medium",
            },
        ]
    if "not matching" in text or "mismatch" in text or "difference" in text:
        return [
            {
                "title": "As-on date basis differs across compared reports",
                "why": "PI explicitly mentions expected closing value date mismatch.",
                "code": hot,
                "doc": guide,
                "disprover": "Compare generated SQL/filter parameters for both reports on same run; identical date basis rejects this.",
                "confidence": "high",
            },
            {
                "title": "Report aggregation filter mismatch",
                "why": "Values diverge despite same business context.",
                "code": hot,
                "doc": guide,
                "disprover": "Run both queries with identical entity/account/security filters; parity rejects this.",
                "confidence": "medium",
            },
        ]
    if "no position" in text or "position" in text:
        return [
            {
                "title": "Holdings snapshot missing for report date",
                "why": "Output says no position despite expected holdings.",
                "code": hot,
                "doc": guide,
                "disprover": "Query holdings snapshot table for entity/account/date; row present rejects this.",
                "confidence": "high",
            },
            {
                "title": "UI/report filter excludes valid positions",
                "why": "No-position symptom can come from join/filter conditions.",
                "code": hot,
                "doc": guide,
                "disprover": "Execute backend response without UI filters; if positions appear, this is likely true.",
                "confidence": "medium",
            },
        ]
    return [
        {
            "title": "Request-to-persistence mapping mismatch",
            "why": "Behavior deviates from expected workflow with no explicit processing error.",
            "code": hot,
            "doc": guide,
            "disprover": "Capture request payload and persisted row for same action; one-to-one match rejects this.",
            "confidence": "medium",
        },
        {
            "title": "Persistence-to-report/render transformation gap",
            "why": "Stored data may be correct but reported/rendered state diverges.",
            "code": hot,
            "doc": guide,
            "disprover": "Compare persisted values against API/report payload for same entity/date; parity rejects this.",
            "confidence": "medium",
        },
    ]


def pad_hypotheses_three(
    hypotheses: list[dict[str, str]], hot: str, guide: str
) -> list[dict[str, str]]:
    """Intake skill requires 2–3 competing hypotheses; pad to three when branches return two."""
    if len(hypotheses) >= 3:
        return hypotheses
    out = list(hypotheses)
    out.append(
        {
            "title": "Master data, configuration, or tenant-specific override",
            "why": "Same build behaves elsewhere; client flags, COA, or security masters may alter filters and joins.",
            "code": hot,
            "doc": guide,
            "disprover": "Reproduce on a neutral training tenant with minimal data; if the issue disappears, compare tenant config and masters.",
            "confidence": "low",
        }
    )
    return out


def fast_elimination_plan(hypotheses: list[dict[str, str]]) -> list[str]:
    h1 = hypotheses[0]["title"] if hypotheses else "H1"
    h2 = hypotheses[1]["title"] if len(hypotheses) > 1 else "H2"
    return [
        f"**Check 1 (5 min):** Capture failing request and immediate response. If payload/response already inconsistent, likely **{h1}**; else continue.",
        f"**Check 2 (10 min):** Verify persisted rows for same entity/account/date. If persistence is correct but API/report output differs, likely **{h2}**; else likely **{h1}**.",
        f"**Check 3 (15 min):** Compare one known-good case vs failing case end-to-end (request -> DB -> API/report). First divergence pinpoints owning layer.",
    ]


def fix_options(module: str, name: str, bug: str) -> list[dict[str, str]]:
    text = f"{module} {name} {bug}".lower()
    if "processing" in text or "stuck" in text or "save" in text:
        return [
            {
                "name": "Option A (minimal)",
                "approach": "Patch transition guard/queue completion condition for this transaction type only.",
                "risk": "Low-medium; localized behavior change.",
                "rollback": "Revert patch and reprocess affected transactions if needed.",
            },
            {
                "name": "Option B (structural)",
                "approach": "Unify async completion + status transition into a single shared flow with idempotent retries.",
                "risk": "Medium-high; touches wider transaction lifecycle.",
                "rollback": "Feature-flag toggle or full revert with lifecycle regression run.",
            },
        ]
    return [
        {
            "name": "Option A (minimal)",
            "approach": "Patch the specific filter/date/source selection causing wrong output for the PI flow.",
            "risk": "Low-medium; scoped to identified branch/query.",
            "rollback": "Revert commit and run targeted regression checks.",
        },
        {
            "name": "Option B (structural)",
            "approach": "Refactor shared report/position calculation path to remove duplicated logic and enforce one source of truth.",
            "risk": "Medium-high; broader blast radius across related reports/screens.",
            "rollback": "Guard behind config/flag if available, otherwise revert and rerun full module regression.",
        },
    ]


def code_search_tokens(module: str, name: str, bug: str) -> list[str]:
    tokens = tokenize(f"{module} {name} {bug}")
    # Drop noisy short/common stems to keep code search targeted.
    bad = {"report", "client", "issue", "value", "values", "data", "stock", "stocks"}
    cleaned = [t for t in sorted(tokens) if len(t) >= 4 and t not in bad]
    return cleaned[:6]


def discover_code_hotspots(module: str, name: str, bug: str, limit: int = 3) -> list[str]:
    tokens = code_search_tokens(module, name, bug)
    if not tokens:
        return []
    cache_key = tuple(sorted(tokens))
    if cache_key in _HOTSPOT_CACHE:
        return _HOTSPOT_CACHE[cache_key]
    search_dirs = [
        WORKSPACE_ROOT / "controller",
        WORKSPACE_ROOT / "dashboard",
        WORKSPACE_ROOT / "av-edge-api",
        WORKSPACE_ROOT / "av_v3_lambda",
        WORKSPACE_ROOT / "balancesheet",
        WORKSPACE_ROOT / "pcr",
    ]
    existing_dirs = [p for p in search_dirs if p.exists()]
    if not existing_dirs:
        return []

    exts = {".php", ".ts", ".tsx", ".js", ".py", ".sql"}
    qset = set(tokens)
    scored: list[tuple[int, str]] = []

    for d in existing_dirs:
        for path in d.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in exts:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace").lower()
            except OSError:
                continue
            content_hits = sum(1 for tok in qset if tok in text)
            if content_hits == 0:
                continue
            path_tokens = tokenize(str(path).replace("/", " ").replace("_", " ").replace("-", " "))
            path_hits = len(qset & path_tokens)
            score = (content_hits * 3) + path_hits
            try:
                rel = str(path.resolve().relative_to(WORKSPACE_ROOT.resolve()))
            except ValueError:
                rel = str(path)
            scored.append((score, rel))

    if not scored:
        return []

    scored.sort(key=lambda x: (-x[0], x[1]))
    result = [f"`{p}`" for _, p in scored[:limit]]
    _HOTSPOT_CACHE[cache_key] = result
    return result


def team_suggestion(csv_team: str, name: str, bug: str) -> tuple[str, str, str]:
    t = (csv_team or "").strip().lower()
    narrative = f"{name} {bug}".lower()
    # Specific report-engine / valuation narratives before generic "report book" → UI (intake skill order).
    if not t and any(
        k in narrative
        for k in (
            "look through",
            "lookthrough",
            "lt market",
            "mf look",
            "mutual fund look",
            "value research",
            "underlying",
        )
    ):
        return (
            "Avengers performance",
            "Ravi Prakash",
            "CSV **TEAM** empty; narrative points to MF look-through / LT Market Cap / underlying holdings — report & tourbillon stack (`MFLookThrough`, lookthrough data). **Alternate if feed-only:** Transformers Ingestion (Value Research file → DB) once API proves master/ISIN load is wrong.",
        )
    # Custom account mapping / copy between accounts (transaction sync + masters), not provider-file ingestion.
    if not t and any(
        k in narrative
        for k in (
            "custom mapping",
            "custom mappings",
            "custom account mapping",
            "copying custom",
            "copy custom",
            "copy mappings",
            "mappings from one account",
            "mappings to another",
            "mapping from one account",
            "mapping to another",
        )
    ):
        return (
            "Arjun TRANSACTIONS",
            "Sandip Valanju",
            "CSV **TEAM** empty; narrative is **custom account mapping** (save/copy between accounts, `feedmappingdetails`, `AccountTransaction::copyMappingsToAccounts`, masters account UI). **Not** Transformers: that squad owns **feed/ETL ingestion** from providers; this PI is **per-account mapping configuration** in transaction sync / manage account.",
        )
    # Intake skill: dashboard / report-book / widgets / Angular → Code UI when CSV TEAM is blank.
    if not t and any(
        k in narrative
        for k in (
            "grid",
            "widget",
            "dashboard",
            "decimal",
            "non grid",
            "nongrid",
            "report book",
            "angular",
        )
    ):
        return (
            "Code UI",
            "Ravi Prakash",
            "CSV **TEAM** empty; narrative indicates dashboard / grid / widget UI work.",
        )
    if "transformers" in t:
        return "Transformers Ingestion", "Sandip Valanju", f"CSV **TEAM** is {csv_team!r}; ingestion/feeds alignment."
    if t == "code":
        return "Code UI", "Ravi Prakash", f"CSV **TEAM** is {csv_team!r}; dashboard / Angular UI."
    if "spartans" in t:
        return "Spartans GL", "Anil Chandran", f"CSV **TEAM** is {csv_team!r}; GL / masters."
    if "arjun" in t:
        return "Arjun TRANSACTIONS", "Sandip Valanju", f"CSV **TEAM** is {csv_team!r}; transactional workflows."
    if "scot" in t:
        return "SCOT Misc", "Anil Chandran", f"CSV **TEAM** is {csv_team!r}; cross-cutting reports / misc."
    if "avengers" in t:
        return "Avengers performance", "Ravi Prakash", f"CSV **TEAM** is {csv_team!r}; performance / valuation."
    if "product" in t:
        return "Code UI", "Ravi Prakash", "**Product Team** in CSV mapped to Report Book / UI-heavy work (Code UI); confirm with PM if backend-only."
    return "SCOT Misc", "Anil Chandran", f"CSV **TEAM** is {csv_team!r}; default fallback—refine after code review."


def client_block(
    item_id: str,
    client_name_col: str,
    name: str,
    bug: str,
    clients: list[tuple[str, str, str]],
) -> str:
    lines = []
    pm = primary_match(client_name_col, clients)
    if pm:
        cn, url = pm
        hc = tenant_hc_uat(url)
        lines.append("**Match type:** Primary (**Client Name** column vs catalog).")
        lines.append(f"**Catalog tenant:** `{cn}`")
        lines.append(f"**HC UAT URL:** {md_link(hc)}")
        return "\n".join(lines)
    fm = fuzzy_match(name, bug, clients)
    if isinstance(fm, tuple):
        cn, url, tok = fm
        hc = tenant_hc_uat(url)
        lines.append(f"**Match type:** Fuzzy (token `{tok}` from **Name** / **Bug Description**).")
        lines.append(f"**Catalog tenant:** `{cn}`")
        lines.append(f"**HC UAT URL:** {md_link(hc)}")
        return "\n".join(lines)
    lines.append("**Match type:** No confident catalog match.")
    if isinstance(fm, str) and fm.startswith("ambiguous"):
        lines.append(f"**Note:** {fm} — human must confirm tenant before using HC UAT.")
    else:
        lines.append("Narrative did not yield a unique `client_name` in `pi/input/urls/*.csv`.")
    lines.append("**HC UAT URL:** *(not assigned — confirm tenant first)*")
    return "\n".join(lines)


def escape_md_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def spec_md(row: dict, clients: list[tuple[str, str, str]]) -> str:
    iid = (row.get("ITEM ID") or row.get("Item ID") or "").strip()
    name = row.get("Name", "").strip()
    bug = narrative_text(row)
    module = row.get("Module", "").strip()
    team, leader, team_rationale = team_suggestion(row.get("TEAM", ""), name, bug)
    dev = row.get("Developer", "").strip()
    assigned = row.get("Assigned To", "").strip()
    meta_rows = [
        ("Item ID", iid),
        ("Group", row.get("Group", "").strip()),
        ("Status", row.get("Status", "").strip()),
        ("Priority", row.get("Priority", "").strip()),
        ("Environment", row.get("Environment", "").strip()),
        ("Report Date", row.get("Report Date", "").strip()),
        ("TEAM (CSV)", row.get("TEAM", "").strip()),
        ("Assigned To", assigned),
        ("Developer", dev),
        ("Client Name (CSV)", row.get("Client Name", "").strip()),
    ]
    meta = "\n".join(f"| {escape_md_cell(k)} | {escape_md_cell(v)} |" for k, v in meta_rows)
    assign_note = ""
    if dev:
        assign_note = f"CSV lists **Developer** `{dev}` and **Assigned To** `{assigned}`; compare with suggested squad below."

    discovered_guides = discover_manual_guides(iid, module, name, bug)
    discovered_hotspots = discover_code_hotspots(module, name, bug)
    if iid in USER_MANUAL:
        um = USER_MANUAL[iid]
    elif discovered_guides:
        um = ", ".join(f"`{p}`" for p in discovered_guides)
    else:
        um = "`pi/user_manual/README.md` — search by **Module** / keywords from this PI."
    hotspots = HOTSPOTS.get(iid, "- *(Run `rg` in `controller/`, `dashboard/`, sibling repos from bug keywords.)*")
    if iid not in HOTSPOTS and discovered_hotspots:
        hotspots = "\n".join(f"- {p}" for p in discovered_hotspots)
    guide_paths = re.findall(r"`([^`]+)`", um)
    hot0 = discovered_hotspots[0] if discovered_hotspots else "`(no code match found)`"
    guide0 = guide_paths[0] if guide_paths else "pi/user_manual/README.md"
    tailored = TAILORED.get(iid)
    if tailored:
        primary_override = tailored.get("primary")
        if primary_override is not None:
            hypothesis_bullet = (
                f"- **Hypothesis:** {primary_override}\n" if primary_override else ""
            )
        else:
            primary_hypo = hypothesis_line(module, name, bug)
            hypothesis_bullet = f"- **Hypothesis:** {primary_hypo}\n" if primary_hypo else ""
        hypo_md = competing_markdown(tailored["competing"])
        fast_checks = fast_plan_markdown(tailored["fast_plan"])
    else:
        primary_hypo = hypothesis_line(module, name, bug)
        hypothesis_bullet = f"- **Hypothesis:** {primary_hypo}\n" if primary_hypo else ""
        hypo_list = pad_hypotheses_three(
            competing_hypotheses(module, name, bug, discovered_hotspots, guide_paths),
            hot0,
            guide0,
        )
        hypo_md = "\n".join(
            "\n".join(
                [
                    f"- **H{i + 1}: {h['title']}**",
                    f"  - Why likely: {h['why']}",
                    f"  - Code evidence: {h['code']}",
                    f"  - Product-doc evidence: `{h['doc'].strip('`')}`",
                    f"  - Quick disprover: {h['disprover']}",
                    f"  - Confidence: **{h['confidence']}**",
                ]
            )
            for i, h in enumerate(hypo_list)
        )
        fast_checks = "\n".join(f"- {c}" for c in fast_elimination_plan(hypo_list))
    options_md = "\n".join(
        f"- **{o['name']}**\n  - Approach: {o['approach']}\n  - Risk: {o['risk']}\n  - Rollback: {o['rollback']}"
        for o in fix_options(module, name, bug)
    )

    return f"""# {iid}: {name}

## Metadata

| Field | Value |
|------|--------|
{meta}

## Client environment URL

{client_block(iid, row.get("Client Name", "").strip(), name, bug, clients)}

## Suggested assignment

- **Team:** {team}
- **Leader:** {leader}
- **Rationale:** {team_rationale}
{assign_note}

## Summary

{name}

## Reproduction / symptoms

{bug if bug else "*(No description in export.)*"}

## Root cause (hypothesis)

{hypothesis_bullet}- **Product context (user manual):** {um}
- **Code hotspots (seed):**

{hotspots}

## Competing hypotheses

{hypo_md}

## Fast elimination plan

{fast_checks}

## Proposed fix (behavior-level)

1. Reproduce under controlled data (entity/account/security from PI).
2. Trace the failing layer (ingestion vs. UI vs. report engine) using hotspots above.
3. Implement the smallest change that restores documented behavior (or approved new behavior); avoid scope creep.
4. Add or extend automated tests where the **test plan** maps to existing frameworks (`controller/unittest/`, `dashboard/**/*.spec.ts`).

## Fix options

{options_md}

## Impact / blast radius

- Depends on subsystem: feeds may affect many tenants; UI bugs are often localized; report/valuation changes can affect compliance reporting — assess per area after root-cause confirmation.

## Risks / rollback

- Feature-flag or config toggles if available; otherwise revert commit and re-run regression suite for the touched module.

## Acceptance criteria

- PI symptoms no longer reproduce on **HC UAT** (or agreed environment) with agreed test data.
- No regressions in adjacent flows listed in `pi/test-plans/{iid}.md`.
- If behavior aligns to user manual, manual steps in the cited guide succeed end-to-end.

## Open questions

- Tenant confirmation if **Client environment URL** was fuzzy or unmatched.
- Whether provider-side (Electra, Morningstar, Bill.com, etc.) vs. AV defect — some PIs explicitly ask for vendor escalation.
"""


def test_plan_md(iid: str, name: str) -> str:
    return f"""# Test plan: {iid}

## Scope and references

- Fix spec: `pi/specs/{iid}.md`
- User manual: see spec **Root cause** / `pi/user_manual/README.md` for theme index.

## Code hotspots

(See `pi/specs/{iid}.md` — **Code hotspots (seed)**; refine during dev.)

## Environment / data prerequisites

- HC UAT tenant from spec **Client environment URL** (or human-confirmed tenant).
- Entity / account / security IDs from the PI narrative where applicable.
- Appropriate roles to access Report Book, feeds, recon, or masters screens under test.

## Verify the fix

| # | Objective | Steps | Expected |
|---|------------|-------|----------|
| 1 | Primary symptom gone | Follow spec **Reproduction** inversely: setup → execute flow → observe | Matches **Acceptance criteria** in spec |
| 2 | Data integrity | Spot-check DB or export where PI references counts/amounts | Matches statements/feeds or business expectation |

## Regression

| Area | Code / UX anchor | Notes |
|------|------------------|-------|
| Same module (happy path) | Paths in `pi/specs/{iid}.md` hotspots | Smoke core navigation |
| Adjacent feed/report | `controller/app/modules/reports/controllers/IndexController.php` or `dashboard/src/app/asset-vantage/dashboard/` as applicable | If PI touched reports or widgets |
| Ledger / holdings | `controller/app/common/transaction/` relevant transaction class | If PI touched posting |

## Adjacent

- Only flows sharing the same code paths identified in the fix spec after implementation.

## Automation mapping

| Layer | Framework / location | Existing coverage | Gap |
|-------|----------------------|-------------------|-----|
| PHP (controller) | PHPUnit under `controller/unittest/` (`tests/DateCalculationHelperTest.php` present) | Minimal sample tests | Add targeted tests if pure logic extracted; else API/integration per team practice |
| Angular (dashboard) | Karma + Jasmine; `dashboard/karma.conf.js`; `dashboard/src/app/**/*.spec.ts` (46+ spec files) | Widget/dashboard specs exist | Extend closest `*.spec.ts` if UI logic fix |
| Python (av-edge-api) | Routes under `av-edge-api/app/` | Benchmark routes active on `master` | Add tests if changing `alpha_wrt_benchmark` |
| Lambdas | `av_v3_lambda/` | Repo-specific | Add handler tests if feed/sync logic changes |

**Manual-only rationale (if applicable):** End-to-end feed or Electra provider parity may require manual compare to custodian files when no stable mock exists.
"""


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Generate PI specs and test plans from a Monday CSV export.")
    ap.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="Input CSV (default: pi/input/Book2.csv if present, else pi/input/processed/Book2.csv)",
    )
    ap.add_argument("--no-move", action="store_true", help="Do not move input to pi/input/processed/ after success.")
    args = ap.parse_args()

    csv_path = args.csv
    if csv_path is None:
        csv_path = INPUT_CSV if INPUT_CSV.exists() else (ROOT / "input" / "processed" / "Book2.csv")
    if not csv_path.exists():
        raise SystemExit(f"No input CSV at {csv_path}")

    clients = load_clients()
    SPECS.mkdir(parents=True, exist_ok=True)
    PLANS.mkdir(parents=True, exist_ok=True)

    with csv_path.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            iid = (row.get("ITEM ID") or row.get("Item ID") or "").strip()
            if not iid:
                continue
            name = row.get("Name", "").strip()
            (SPECS / f"{iid}.md").write_text(spec_md(row, clients), encoding="utf-8")
            (PLANS / f"{iid}.md").write_text(test_plan_md(iid, name), encoding="utf-8")
            print("wrote", iid)

    if not args.no_move and csv_path.resolve() == INPUT_CSV.resolve():
        proc = ROOT / "input" / "processed"
        proc.mkdir(parents=True, exist_ok=True)
        dest = proc / csv_path.name
        if dest.exists():
            dest.unlink()
        csv_path.rename(dest)
        print("moved", csv_path, "->", dest)


if __name__ == "__main__":
    main()
