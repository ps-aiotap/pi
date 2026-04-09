#!/usr/bin/env python3
"""Generate pi/specs and pi/test-plans from pi/input/Book2.csv (one-off batch).

Specs are ready for technical review. Test plans are **drafts** only: they embed
code hotspots from EVIDENCE where present and **require** a follow-up pass with
`pi/skills/pi-test-plan/SKILL.md` (repo search) to fill regression and automation
rows and to remove the draft callout. Do not approve QA on batch output alone.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
BOOK2_CANDIDATES = [
    ROOT / "pi" / "input" / "Book2.csv",
    ROOT / "pi" / "input" / "processed" / "Book2.csv",
]
INPUT_CSV = next(p for p in BOOK2_CANDIDATES if p.exists())
URL_DIR = ROOT / "pi" / "input" / "urls"
SPECS_DIR = ROOT / "pi" / "specs"
PLANS_DIR = ROOT / "pi" / "test-plans"


def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("-", "_")
    return s


def load_url_catalog() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in URL_DIR.glob("*.csv"):
        with p.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cn = row.get("client_name", "").strip()
                url = row.get("url", "").strip()
                if cn and url:
                    out[norm(cn)] = url
    return out


def hc_uat_from_catalog(url: str) -> str:
    p = urlparse(url)
    host = p.hostname or ""
    parts = host.split(".")
    if not parts or not parts[0]:
        return url
    tenant = parts[0]
    rest = ".".join(parts[1:])
    if tenant.startswith("hcuat"):
        first = "hc" + tenant[5:]
    elif tenant.startswith("hc"):
        first = tenant
    else:
        first = "hc" + tenant
    if rest.endswith("assetvantage.com"):
        rest = rest[: -len("assetvantage.com")] + "assetvantage.in"
    new_host = f"{first}.{rest}" if rest else first
    scheme = p.scheme or "https"
    return f"{scheme}://{new_host}/"


# Catalog lookup key (normalized) per ItemId; None = no catalog tenant
TENANT_LOOKUP: dict[str, tuple[str, str, str | None]] = {
    # item_id: (match_type, rationale, catalog_norm_key or None)
    "PI-9878": ("Fuzzy", "token `feliciana` from **Name** → `felicianacorp`", "felicianacorp"),
    "PI-8327": ("Fuzzy", "token `ruben` from **Name** → `rubencompanies`", "rubencompanies"),
    "PI-2260": ("None", "`Client Name` empty; narrative is generic PAR beta (no unique tenant token).", None),
    "PI-9799": ("None", "`Client Name` empty; internal COA template issue (tenant unknown).", None),
    "PI-0200": ("Fuzzy", "token `luzerne` from **Name** → `luzerne`", "luzerne"),
    "PI-6168": ("Fuzzy", "URL in **Bug Description** → `blueocean`", "blueocean"),
    "PI-4524": ("Fuzzy", "token `ruben` from **Name** → `rubencompanies`", "rubencompanies"),
    "PI-0198": ("Fuzzy", "URL in **Bug Description** → `lgtsecurities`", "lgtsecurities"),
    "PI-8136": ("None", "No tenant in PI export; needs client confirmation.", None),
    "PI-8002": ("Fuzzy", "token `gary` / `peters` from **Name** → `garypeters`", "garypeters"),
    "PI-1891": ("Fuzzy", "token `styner` from Stayner Family in **Bug Description** → `eacpstyner`", "eacpstyner"),
    "PI-0967": ("Fuzzy", "URL in **Bug Description** → `blueocean`", "blueocean"),
    "PI-6587": ("Fuzzy", "token `acadia` from **Name** → `acadiafo`", "acadiafo"),
    "PI-9220": ("Fuzzy", "token `rmc` from **Bug Description** link → `rmc`", "rmc"),
    "PI-3673": ("Fuzzy", "token `dalton` from **Name** → `daltonpartners`", "daltonpartners"),
    "PI-8535": ("Fuzzy", "token `tjcny` from **Name** → `tjcny`", "tjcny"),
    "PI-6393": ("Fuzzy", "token `nextworld` from **Name** → `nextworld`", "nextworld"),
    "PI-1635": ("Fuzzy", "token `altium` from **Name** → `altium`", "altium"),
    "PI-6479": ("Fuzzy", "token `tectonic` from **Name** → `tectonicadvisors`", "tectonicadvisors"),
    "PI-7123": ("Fuzzy", "hostname `hcmuthoot` in **Bug Description** → `muthoot`", "muthoot"),
    "PI-3973": ("Fuzzy", "URL in **Bug Description** → `lgtsecurities`", "lgtsecurities"),
    "PI-1216": ("Fuzzy", "token `rockdale` from **Name** → `rockdale`", "rockdale"),
    "PI-2017": ("Fuzzy", "token `kkp` from **Name** → `kkpgroup`", "kkpgroup"),
    "PI-8283": ("None", "URL `hclgtindia1.assetvantage.in` in narrative — tenant not in `pi/input/urls/` catalogs.", None),
    "PI-9273": ("Fuzzy", "token `ruben` from **Name** → `rubencompanies`", "rubencompanies"),
    "PI-9058": ("None", "Mentions Patni / LGT1 without resolvable catalog tokens; **ambiguous — human must confirm** tenant.", None),
    "PI-3962": ("Fuzzy", "token `feliciana` from **Bug Description** → `felicianacorp`", "felicianacorp"),
}


def resolve_url(item_id: str, catalog: dict[str, str]) -> tuple[str, str, str]:
    """Returns (markdown body, hc_uat_or_empty, kind)."""
    if item_id not in TENANT_LOOKUP:
        return (
            "- **Match type:** None\n- **Rationale:** No tenant mapping for this batch entry.\n- **HC UAT base URL:** Not determined.\n",
            "",
            "None",
        )
    kind, rationale, key = TENANT_LOOKUP[item_id]
    if key and norm(key) in catalog:
        url = catalog[norm(key)]
        h = hc_uat_from_catalog(url)
        body = (
            f"- **Match type:** {kind}\n"
            f"- **Rationale:** {rationale}\n"
            f"- **HC UAT base URL:** {h}\n"
        )
        return body, h, kind
    body = (
        f"- **Match type:** {kind}\n"
        f"- **Rationale:** {rationale}\n"
        f"- **HC UAT base URL:** Not determined (no catalog match).\n"
    )
    return body, "", kind


TEAM_MAP = {
    "Transformers": ("Transformers Ingestion", "Sandip Valanju"),
    "Code": ("Code UI", "Ravi Prakash"),
    "Product Team": ("Code UI", "Ravi Prakash"),
    "Spartans": ("Spartans GL", "Anil Chandran"),
    "Arjun": ("Arjun TRANSACTIONS", "Sandip Valanju"),
    "Avengers": ("Avengers performance", "Ravi Prakash"),
    "SCOT": ("SCOT Misc", "Anil Chandran"),
}

# Code/doc citations per ItemId (path:line — approximate; verify during implementation)
EVIDENCE: dict[str, str] = {
    "PI-9878": "`controller/app/common/transaction/InvestmentsTransaction.php:2760-2785` (Bill.com `feedid == 4`, `mapMultidistribution`); `controller/app/common/transaction/InvestmentsTransaction.php:2792+` (`mapMultidistribution`); `controller/app/common/transaction/Feedmapping/BilldotcomMappingTransaction.php:130-144` (multi-distribution ledger validation).",
    "PI-8327": "Search: dashboard widgets Angular/report-book UI; `av_v3_lambda` / frontend widget loaders (confirm module path in repo).",
    "PI-2260": "`av_v3_lambda/src/PerformanceApiReport/par_response.py` and `av_v3_lambda/src/AUMReport/par_response.py` (period quantity added/sold aggregation for PAR).",
    "PI-9799": "`controller/app/common/transaction/ChartOfAccountTransaction.php` (`deleteTemplate`, `Delete` switch); `controller/app/modules/masters/controllers/IndexController.php` (`chartofaccounttemplate` delete routing).",
    "PI-0200": "`controller/app/common/transaction/InvestmentsTransaction.php` (`saveFeedTransaction`, `getTransactionJsonString`); `controller/app/common/transaction/AccountTransaction.php` (Electra `feedtypeid == 1` DB reads for transactions/holdings).",
    "PI-6168": "Direct equity demerger save path under `controller/app/common/transaction/` (search demerger); performance/timeouts on large txn volume.",
    "PI-4524": "Feed dedup / Morningstar sync: `InvestmentsTransaction` and related feed mapping (search Morningstar / duplicate transaction handling).",
    "PI-0198": "Transaction persistence, audit trail models and reports (search audit + mutual fund transaction delete).",
    "PI-8136": "Cash feed posting → ledger mapping (search investment temp / feed post blank ledger).",
    "PI-8002": "Bank reconciliation totals / selection logic (search bank recon reconcile withdrawal deposit aggregation).",
    "PI-1891": "Report Book balance sheet data pipeline: GL vs report widgets (lambda/report services + dashboard).",
    "PI-0967": "Realized gain report generation (search gain report export; timeout/perf).",
    "PI-6587": "Custodian recon security data fetch (search custodian recon).",
    "PI-9220": "Benchmark returns in report book (search benchmark twr; compare platform vs training tenants — config/data issue).",
    "PI-3673": "Report book + widget cache loading (frontend + API; perf).",
    "PI-8535": "Open lot report vs balance sheet cost (search open lot, cost basis).",
    "PI-6393": "PCR / auto-sync unidentified bucket (search PCR unidentified).",
    "PI-1635": "Transaction sync account selection UI + auto-sync flags (search sync account checkbox).",
    "PI-6479": "Custom account mapping withdrawal/deposit (search custom mapping feed).",
    "PI-7123": "Wealth register vs PAR opening/closing market value (PAR lambda + WR report).",
    "PI-3973": "Mutual fund holding cost display (grouped holdings; search holding cost negative).",
    "PI-1216": "Profit share master + audit (search profit share; entity audit coverage).",
    "PI-2017": "Arch security auto-create / delete respect (search `saveArchTransaction`, Arch sync).",
    "PI-8283": "Taxation master STCG/LTCG rules for listed commodity funds (search taxation gains period).",
    "PI-9273": "Feed field escaping / security identifier parsing (search backslash escape in feed description).",
    "PI-9058": "Direct equity demerger delete cascade (search demerger, transfer in/out transaction cleanup).",
    "PI-3962": "Balance sheet equity positions sold-out filter (search balance sheet cost sold).",
}


def md_escape(s: str) -> str:
    return (s or "").replace("\n", "\n\n").strip()


def narrative(row: dict[str, str]) -> str:
    """Monday export for this batch often leaves **Bug Description** empty and puts text in **Days until Resolution**."""
    for key in ("Bug Description", "Days until Resolution"):
        v = (row.get(key) or "").strip()
        if not v:
            continue
        if re.match(r"^\d+\s+days?\s+[\d.]+\s+hours?$", v, re.I):
            continue
        return v
    return (row.get("Name") or "").strip()


def write_spec(row: dict[str, str], catalog: dict[str, str]) -> None:
    item_id = (row.get("ITEM ID") or "").strip()
    if not item_id:
        return
    name = row.get("Name", "")
    desc = narrative(row)
    team_csv = (row.get("TEAM") or "").strip()
    roster_team, leader = TEAM_MAP.get(team_csv, ("SCOT Misc", "Anil Chandran"))
    assigned = row.get("Assigned To", "")
    developer = row.get("Developer", "")
    env_section, _hc_uat, _ = resolve_url(item_id, catalog)

    g = row.get("Group") or ""
    meta_rows = [
        "| Field | Value |",
        "|---|---|",
        f"| Group | {g} |",
        f"| Name | {name} |",
        f"| ITEM ID | {item_id} |",
        f"| Status | {row.get('Status', '')} |",
        f"| Priority | {row.get('Priority', '')} |",
        f"| Environment | {row.get('Environment', '')} |",
        f"| Reporter | {row.get('Reporter', '')} |",
        f"| Report Date | {row.get('Report Date', '')} |",
        f"| TEAM (CSV) | {team_csv} |",
        f"| Assigned To | {assigned} |",
        f"| Developer | {developer} |",
    ]

    spec = f"""# {item_id}: {name}

## Metadata

{chr(10).join(meta_rows)}

## Client environment URL

{env_section.strip()}

## Suggested assignment

- **Team:** {roster_team}
- **Leader:** {leader}
- **Rationale:** CSV **TEAM** `{team_csv}` maps to **{roster_team}** per `pi/input/team/TeamMembers.txt`. Code/doc focus: {EVIDENCE.get(item_id, '(see repo search)')}
- **Alignment with CSV:** Assigned **{assigned}** / Developer **{developer}** — confirm whether this matches squad ownership.

## Summary

{md_escape(desc)[:4000]}

## Reproduction / symptoms

1. Use tenant HC UAT URL above when available; otherwise confirm client with support.
2. Follow steps described in the PI **Name** and **Bug Description** (entities/accounts/dates as cited).
3. Capture screenshots or exports referenced in Monday attachments when reproducing internally.

## Root cause (hypothesis + evidence)

- **Hypothesis:** To be confirmed during dev investigation; initial code area: {EVIDENCE.get(item_id, 'ripgrep by module keywords from PI title.')}
- **Evidence:** See paths cited above; add stack traces and query results during triage.

## Proposed fix (behavior-level)

- Narrow the change to the subsystem indicated by evidence; preserve existing feed and GL invariants.
- Add logging or validation only where it aids diagnosis without widening blast radius.
- Any environment-specific behavior must use existing config/env mechanisms (**no hardcoded** tenant URLs in code).

## Impact / blast radius

- Feeds, ledger posting, reporting, or UI depending on PI scope; regression-test adjacent flows listed in the test plan.

## Acceptance criteria

- PI symptoms no longer reproduce on a validated tenant with agreed test data.
- No new errors in feed sync, posting, or report totals for sampled adjacent accounts/entities.
- Performance meets agreed threshold where the PI is performance-related.

## Open questions

- Confirm production tenant and entity/account identifiers.
- Data samples (exports) from client if not already attached.

---
*Generated from `pi/input/Book2.csv` via `pi/scripts/generate_from_book2.py`. Review and approve before code changes.*
"""
    path = SPECS_DIR / f"{item_id}.md"
    path.write_text(spec, encoding="utf-8")


def hotspots_block(item_id: str) -> str:
    """Narrative for Code hotspots section; safe to embed in plan (no f-string braces in EVIDENCE)."""
    ev = (EVIDENCE.get(item_id) or "").strip()
    if ev:
        return (
            "The batch script seeded the lines below from the `EVIDENCE` map in this file — "
            "**verify, narrow, and expand** during `pi-test-plan` (repo search, spec updates).\n\n"
            + ev
        )
    return (
        f"No batch `EVIDENCE` entry for `{item_id}`. Copy **Root cause** / **Suggested assignment** "
        f"code paths from [`pi/specs/{item_id}.md`](../specs/{item_id}.md), then search the repo for "
        "callers, SQL, and tests."
    )


def write_test_plan(row: dict[str, str]) -> None:
    item_id = row.get("ITEM ID", "").strip()
    if not item_id:
        return
    hot = hotspots_block(item_id)
    plan = (
        f"# Test plan: {item_id}\n\n"
        "> **Draft (batch-generated).** Do not treat as approved QA documentation until the **pi-test-plan** "
        "skill (see `pi/skills/pi-test-plan/SKILL.md`) fills **Regression** and **Automation mapping** from "
        "this spec and the codebase, then **remove this callout**.\n\n"
        "## Scope and references\n\n"
        f"- Fix spec: [`pi/specs/{item_id}.md`](../specs/{item_id}.md)\n"
        f"- Impact doc: optional `pi/impact/{item_id}.md` (if created separately)\n\n"
        "## Code hotspots (seed)\n\n"
        f"{hot}\n\n"
        "## Environment / data prerequisites\n\n"
        "- HC UAT tenant from fix spec (or confirmed client sandbox).\n"
        "- Entity, accounts, securities, and date ranges exactly as in the PI description.\n"
        "- Test user with permissions for the affected modules (report book, feeds, masters, etc.).\n\n"
        "## Verify the fix\n\n"
        "1. **Primary scenario (*manual*):** Repeat the client workflow from the PI; observed behavior matches "
        "**Acceptance criteria** in the fix spec.\n"
        "2. **Data check (*manual*):** Compare key totals (balances, quantities, costs, recon totals) against "
        "expected spreadsheets or GL.\n"
        "3. **Negative check (*manual*):** Nearby account/entity not in the bug report still behaves as before.\n\n"
        "## Regression\n\n"
        "**Required before approval:** Replace the placeholder row with real cases **anchored to files, methods, "
        "screens, or jobs** (from hotspots above + `pi-test-plan` repo review). Generic “smoke the module” rows "
        "are not sufficient for a final plan.\n\n"
        "| # | Area | Code / UX anchor | Steps | Expected |\n"
        "|---|------|------------------|-------|----------|\n"
        "| — | *add* | *tie to hotspot* | | |\n\n"
        "## Adjacent\n\n"
        f"- Derive bullets from [`pi/specs/{item_id}.md`](../specs/{item_id}.md) **Impact / blast radius** and "
        "from shared components found during `pi-test-plan`. Delete bullets that do not apply.\n\n"
        "## Automation mapping\n\n"
        "**Required before approval:** Search the repository (for example `controller/unittest/`, `**/*Test*.php`, "
        "`dashboard/**/*.spec.ts`, and CI workflow configs) and complete the table. Either name **existing** tests "
        "or globs that touch the hotspots, or state **none** with a one-line justification (e.g. searched paths). "
        "Do **not** ship the literal string **TBD** here.\n\n"
        "| Layer | Framework (if any) | Tests or globs touching hotspots | Gap / next step |\n"
        "|-------|-------------------|----------------------------------|----------------|\n"
        "| — | *fill* | | |\n\n"
        "Until automated coverage exists for a scenario, label those cases **manual** in **Regression** and note "
        "future `pi-test-implement` if useful.\n\n"
        "---\n"
        "*Generated from `pi/input/Book2.csv` via `pi/scripts/generate_from_book2.py` — draft only; finish via "
        "`pi/skills/pi-test-plan/SKILL.md`.*\n"
    )
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    (PLANS_DIR / f"{item_id}.md").write_text(plan, encoding="utf-8")


def main() -> None:
    catalog = load_url_catalog()
    SPECS_DIR.mkdir(parents=True, exist_ok=True)
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    with INPUT_CSV.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            item_id = (row.get("ITEM ID") or "").strip()
            if not item_id.startswith("PI-"):
                continue
            write_spec(row, catalog)
            write_test_plan(row)
    print("Wrote specs and test plans for Book2.csv rows.")


if __name__ == "__main__":
    main()
