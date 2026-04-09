#!/usr/bin/env python3
"""One-off generator: Book2.csv -> pi/specs/*.md and pi/test-plans/*.md. Run from repo root."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT_CSV = ROOT / "pi" / "input" / "Book2.csv"
URL_DIR = ROOT / "pi" / "input" / "urls"
SPECS = ROOT / "pi" / "specs"
PLANS = ROOT / "pi" / "test-plans"


def norm(s: str) -> str:
    if not s:
        return ""
    s = s.lower().strip()
    s = re.sub(r"[_\-]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def hc_uat_url(catalog_url: str) -> str:
    """Catalog URL -> HC UAT host per PI skill (`hc` + tenant; `.assetvantage.in`)."""
    u = catalog_url.strip()
    if not u.startswith("http"):
        return u
    from urllib.parse import urlparse

    p = urlparse(u)
    host = p.hostname or ""
    if not host:
        return u
    parts = host.split(".")
    tenant = parts[0]
    rest = ".".join(parts[1:]) if len(parts) > 1 else ""
    if tenant.startswith("hcuat"):
        new_first = "hc" + tenant[5:]
    elif tenant.startswith("hc"):
        new_first = tenant
    else:
        new_first = "hc" + tenant
    if rest.endswith("assetvantage.com"):
        rest = rest[: -len("assetvantage.com")] + "assetvantage.in"
    new_host = new_first + ("." + rest if rest else "")
    return f"{p.scheme}://{new_host}/"


def load_clients() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for f in sorted(URL_DIR.glob("*.csv")):
        with f.open(newline="", encoding="utf-8") as fp:
            for r in csv.DictReader(fp):
                cn = (r.get("client_name") or "").strip()
                url = (r.get("url") or "").strip()
                if cn and url:
                    rows.append((cn, url))
    return rows


def url_from_description(text: str) -> str | None:
    if not text:
        return None
    m = re.search(r"https?://([a-z0-9-]+)\.assetvantage\.(?:com|in)(?:/[^\s]*)?", text, re.I)
    if m:
        return f"https://{m.group(0).split('://', 1)[-1].split()[0]}"
    return None


def exact_client(client_name: str, clients: list[tuple[str, str]]) -> tuple[str, str] | None:
    n = norm(client_name)
    if not n:
        return None
    hits = [(c, u) for c, u in clients if norm(c) == n]
    if len(hits) == 1:
        return hits[0]
    return None


def fuzzy_clients(token: str, clients: list[tuple[str, str]]) -> list[tuple[str, str]]:
    t = norm(token)
    if len(t) < 4:
        return []
    out: list[tuple[str, str]] = []
    for c, u in clients:
        cn = norm(c)
        if t in cn or cn in t:
            out.append((c, u))
    return out


def host_to_client(host: str, clients: list[tuple[str, str]]) -> tuple[str, str] | None:
    """Map tenant hostname (e.g. hcmuthoot) to catalog client (e.g. muthoot)."""
    from urllib.parse import urlparse

    if "://" in host:
        host = (urlparse(host).hostname or "").split(".")[0]
    else:
        host = host.split(".")[0]
    hn = norm(host)
    if not hn:
        return None
    exact = [(c, u) for c, u in clients if norm(c) == hn]
    if len(exact) == 1:
        return exact[0]
    subs: list[tuple[str, str]] = []
    for c, u in clients:
        cn = norm(c)
        if cn in hn or hn in cn:
            subs.append((c, u))
    if len(subs) == 1:
        return subs[0]
    return None


def resolve_client(
    row: dict,
    clients: list[tuple[str, str]],
) -> tuple[str, str, str]:
    """Returns (kind, detail, hc_uat_url_or_message). kind: primary|fuzzy|url_in_text|ambiguous|none"""
    cn = (row.get("Client Name") or "").strip()
    name = row.get("Name") or ""
    desc = narrative_text(row)
    text = name + " " + desc

    ex = exact_client(cn, clients)
    if ex:
        c, u = ex
        return ("primary", f"**Client Name** normalized match → `{c}`", hc_uat_url(u))

    udesc = url_from_description(text)
    if udesc:
        from urllib.parse import urlparse

        host_first = (urlparse(udesc).hostname or "").split(".")[0]
        hc = host_to_client(host_first, clients)
        if hc:
            c, u = hc
            return ("url_in_text", f"Tenant from description URL hostname `{host_first}` → catalog `{c}`", hc_uat_url(u))
        return ("url_in_text", f"Hostname `{host_first}` could not be matched uniquely in URL catalog", "—")

    STOPWORDS = {
        "wealth",
        "report",
        "book",
        "client",
        "issue",
        "when",
        "from",
        "with",
        "that",
        "this",
        "same",
        "while",
        "team",
    }
    tokens = set(re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", text)) - STOPWORDS
    # Prefer longer / more specific tokens
    tokens_sorted = sorted(tokens, key=lambda x: (-len(x), x.lower()))
    all_hits: dict[str, list[tuple[str, str]]] = {}
    for tok in tokens_sorted:
        hits = fuzzy_clients(tok, clients)
        if len(hits) == 1:
            c, u = hits[0]
            return ("fuzzy", f"**Fuzzy match** — token `{tok}` → `{c}`", hc_uat_url(u))
        if len(hits) > 1:
            all_hits[tok] = hits

    if all_hits:
        lines = []
        for tok, hits in list(all_hits.items())[:5]:
            names = ", ".join(f"`{c}`" for c, _ in hits[:6])
            lines.append(f"- Token `{tok}`: {names} — **ambiguous**")
        return ("ambiguous", "\n".join(lines), "—")

    return ("none", "No **Client Name**, no unique fuzzy token, and no catalog URL in description.", "—")


MODULE_TEAM = [
    (("dashboard", "widget", "report book", "benchmark", "angular"), "Code UI", "Ravi Prakash"),
    (
        (
            "bill.com",
            "bill com",
            "feed electra",
            "electra",
            "morningstar",
            "custodian recon",
            "bank recon",
            "auto sync",
            "transaction sync",
            "unidentified",
            "arch setup",
            "pcr feed",
            "feed ",
        ),
        "Transformers Ingestion",
        "Sandip Valanju",
    ),
    (("chart of account", "coa", "profit share", "partnership", "general ledger"), "Spartans GL", "Anil Chandran"),
    (("performance", "gain report", "return", "cost", "lot", "wealth register", "market value", " par ", "aum"), "Avengers performance", "Ravi Prakash"),
    (("direct equity", "demerger", "mutual fund", "taxation master", "de module"), "Arjun TRANSACTIONS", "Sandip Valanju"),
    (("balance sheet", "sold out"), "SCOT Misc", "Anil Chandran"),
]


def narrative_text(row: dict) -> str:
    """Book2.csv sometimes shifts long bug text into **Days until Resolution** (Bug Description empty)."""
    bug = (row.get("Bug Description") or "").strip()
    if bug:
        return bug
    dur = (row.get("Days until Resolution") or "").strip()
    if dur and not re.match(r"^\d+\s*days", dur, re.I):
        return dur
    return ""


def suggest_team(module: str, name: str, desc: str, team_csv: str) -> tuple[str, str, str]:
    blob = norm(module + " " + name + " " + desc)
    for keys, t, l in MODULE_TEAM:
        if any(k in blob for k in keys):
            rationale = f"**Module** / text maps to `{', '.join(keys)}` heuristics → **{t}**."
            return t, l, rationale
    return "SCOT Misc", "Anil Chandran", "No strong keyword match; default **SCOT Misc**."


def build_competing_hypotheses(module: str, name: str, desc: str, hs: str) -> list[dict[str, str]]:
    blob = norm(f"{module} {name} {desc}")
    guide = "`pi/user_manual/README.md`"
    if any(k in blob for k in ("feed", "electra", "morningstar", "sync", "recon", "import")):
        return [
            {
                "title": "Provider payload is complete but ingest filter drops rows",
                "why": "Symptom is partial/missing records after sync/import.",
                "code": hs,
                "doc": guide,
                "disprover": "For one missing record, compare provider payload row-count and AV persisted row-count for same account/date; parity rejects ingest-drop.",
                "confidence": "high",
            },
            {
                "title": "Mapping resolution fails for account/security identifiers",
                "why": "Records land in unidentified/wrong state despite source availability.",
                "code": hs,
                "doc": guide,
                "disprover": "Inspect mapping keys in request/logs and corresponding master ids; exact key-to-id match rejects mapping-failure.",
                "confidence": "medium",
            },
            {
                "title": "Post-ingest status/visibility filter hides valid records",
                "why": "Data exists but UI/report omits expected rows.",
                "code": hs,
                "doc": guide,
                "disprover": "Query persisted rows directly and compare to API response filter fields for same scope; identical sets reject visibility-filter bug.",
                "confidence": "medium",
            },
        ]
    if any(k in blob for k in ("widget", "dashboard", "report book", "report", "grid", "par", "performance")):
        return [
            {
                "title": "Report/query uses incorrect grouping or date basis",
                "why": "Mismatch appears between comparable report views or entities.",
                "code": hs,
                "doc": guide,
                "disprover": "Capture request parameters and generated SQL for both views; identical grouping/date clauses reject this.",
                "confidence": "high",
            },
            {
                "title": "Aggregation step collapses dimensions (entity/account/security) too early",
                "why": "Group totals differ from expected sum of detailed rows.",
                "code": hs,
                "doc": guide,
                "disprover": "Log pre-aggregate and post-aggregate row keys; unchanged key cardinality rejects early-collapse.",
                "confidence": "medium",
            },
            {
                "title": "UI formatter renders incorrect value despite correct backend payload",
                "why": "Grid/visual value differs while non-grid path often matches.",
                "code": hs,
                "doc": guide,
                "disprover": "Compare API payload numeric precision with rendered DOM value for same cell; equality rejects formatter defect.",
                "confidence": "medium",
            },
        ]
    return [
        {
            "title": "Input validation branch rejects valid payload for this workflow",
            "why": "User action fails at save/process boundary.",
            "code": hs,
            "doc": guide,
            "disprover": "Replay same payload with validation logging enabled; no failed rule rejects validation-branch hypothesis.",
            "confidence": "high",
        },
        {
            "title": "Persistence write path stores incomplete or transformed values",
            "why": "Saved state diverges from submitted data.",
            "code": hs,
            "doc": guide,
            "disprover": "Compare request payload fields with persisted columns for one transaction id; exact one-to-one match rejects write-path bug.",
            "confidence": "medium",
        },
        {
            "title": "Read/report path applies stricter filters than write path",
            "why": "Data appears saved but not visible in report/screen.",
            "code": hs,
            "doc": guide,
            "disprover": "Run API/read query with and without optional filters for same entity/date; unchanged result set rejects filter mismatch.",
            "confidence": "medium",
        },
    ]


def hypotheses_md(hypotheses: list[dict[str, str]]) -> str:
    parts: list[str] = []
    for i, h in enumerate(hypotheses, start=1):
        parts.extend(
            [
                f"- **H{i}: {h['title']}**",
                f"  - Why likely: {h['why']}",
                f"  - Code evidence: {h['code']}",
                f"  - Product-doc evidence: {h['doc']}",
                f"  - Quick disprover: {h['disprover']}",
                f"  - Confidence: **{h['confidence']}**",
            ]
        )
    return "\n".join(parts)


def fast_plan_md(hypotheses: list[dict[str, str]]) -> str:
    h1 = hypotheses[0]["title"]
    h2 = hypotheses[1]["title"]
    h3 = hypotheses[2]["title"]
    return "\n".join(
        [
            f"- **Check 1 (5 min):** Capture failing request/response and compare required fields to expected contract. If mismatch appears at boundary -> likely **{h1}**.",
            f"- **Check 2 (10 min):** Compare one failing case in DB/log rows vs API/report payload for same ids/date. If DB correct but API/render wrong -> likely **{h2}** or **{h3}**.",
            f"- **Check 3 (15 min):** Trace first divergence across request -> persistence -> read/render with exact row counts/keys; branch to the hypothesis owning that stage.",
        ]
    )


CODE_HOTSPOTS = {
    "widgets": "`dashboard/src/app/asset-vantage/dashboard/`**,** `dashboard/src/app/services/dashboard.service.ts`**,** `av_v3_lambda/` (widget data APIs)",
    "report_book": "`dashboard/src/app/asset-vantage/report-book/`**,** `dashboard/src/app/test/.../report-book.component.spec.ts`**,** `av_v3_lambda/src/PerformanceApiReport/par_response.py`**,** `av_v3_lambda/src/AUMReport/par_response.py`",
    "lambda_perf": "`av_v3_lambda/src/PerformanceApiReport/`**,** `av_v3_lambda/src/AUMReport/emvCalculation.py` (quantity / period logic)",
    "electra": "`controller/app/modules/settings/controllers/IndexController.php` (Electra settings/actions)**,** `controller/public/directory.php` (`ELECTRA_PATH`)",
    "controller_gl": "`controller/app/modules/` (GL / masters) — search **Chart of Accounts** / template",
    "ingestion": "`controller/` feed & transaction sync modules**,** `pcr/` PCR pipeline",
    "de": "`controller/` Direct Equity / demerger transaction handlers — search **demerger**",
}


def automation_table() -> str:
    return """| Area | Framework / location | Notes |
|------|---------------------|--------|
| PHP controller | `controller/unittest/tests/DateCalculationHelperTest.php` (sample); broader: `**/*Test*.php` under `controller/` | Search `rg 'class.*Test' controller` for coverage near changed files |
| Angular dashboard | Karma + Jasmine: `dashboard/karma.conf.js`**,** `dashboard/**/*.spec.ts` (e.g. `dashboard/src/app/asset-vantage/report-book/report-book.component.spec.ts`, widget specs) | Run team’s `npm test` / CI job for `dashboard/` |
| Lambda / Python | `av_v3_lambda/` — check for pytest or deploy pipelines in repo CI | Add unit tests alongside `emvCalculation.py` / `par_response.py` if team standard exists |
| CI | `.github/workflows/` (if present) | Align with existing jobs |"""


def main() -> None:
    clients = load_clients()
    csv_path = INPUT_CSV if INPUT_CSV.exists() else ROOT / "pi" / "input" / "processed" / "Book2.csv"
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        raw_id = (row.get("ITEM ID") or row.get("Item ID") or "").strip()
        iid = raw_id if re.match(r"^PI-\d+$", raw_id) else (row.get("ITEM ID") or "").strip()
        if not iid:
            continue
        name = row.get("Name") or ""
        desc = narrative_text(row)
        module = row.get("Module") or ""
        status = row.get("Status") or ""
        priority = row.get("Priority") or ""
        env = row.get("Environment") or ""
        assigned = row.get("Assigned To") or ""
        developer = row.get("Developer") or ""
        team_csv = row.get("TEAM") or ""

        ck, cdetail, hcu = resolve_client(row, clients)
        team, leader, team_r = suggest_team(module, name, desc, team_csv)

        if "widget" in norm(name + desc) or "dashboard" in norm(name + desc):
            hs = CODE_HOTSPOTS["widgets"]
        elif "report book" in norm(name + desc) or "par" in norm(name + desc):
            hs = CODE_HOTSPOTS["report_book"] + "**,** " + CODE_HOTSPOTS["lambda_perf"]
        elif "electra" in norm(desc) or "feed" in norm(name.lower()):
            hs = CODE_HOTSPOTS["electra"] + "**,** " + CODE_HOTSPOTS["ingestion"]
        elif "chart of account" in norm(name + desc) or "template" in norm(name.lower()):
            hs = CODE_HOTSPOTS["controller_gl"]
        elif "demerger" in norm(name + desc) or "direct equity" in norm(name + desc):
            hs = CODE_HOTSPOTS["de"]
        elif "benchmark" in norm(name + desc) or "return" in norm(name + desc):
            hs = CODE_HOTSPOTS["lambda_perf"] + "**,** " + CODE_HOTSPOTS["report_book"]
        else:
            hs = CODE_HOTSPOTS["ingestion"] + "**,** `controller/` business modules"
        hypotheses = build_competing_hypotheses(module, name, desc, hs)

        spec_path = SPECS / f"{iid}.md"
        meta_rows = "\n".join(
            f"| {k} | {v} |"
            for k, v in [
                ("Name", name.replace("|", "\\|")[:500]),
                ("Status", status),
                ("Priority", priority),
                ("Module", module),
                ("Environment", env),
                ("Assigned To", assigned),
                ("Developer", developer),
                ("TEAM (CSV)", team_csv),
            ]
        )

        client_section = f"""### Client environment URL

- **Match type:** {ck}
- **Rationale:** {cdetail}
- **HC UAT URL (validation):** {hcu}
"""

        spec = f"""# {iid}: {name}

## Metadata

| Field | Value |
|-------|-------|
{meta_rows}

{client_section}

### Suggested assignment

- **Team:** {team}
- **Leader:** {leader}
- **Rationale:** {team_r} CSV **TEAM** = `{team_csv}`; align with assignee **{assigned}** / **{developer}** as needed.

### Summary

{(desc or name)[:1200]}{"…" if len(desc or name) > 1200 else ""}

### Reproduction / symptoms

1. Use client context from **Client environment URL** (confirm tenant with PM if ambiguous).
2. Follow steps implied in **Bug Description**; capture entity/account/security IDs already listed in the PI.
3. For UI issues, compare **HC UAT** vs prod only per your process; this spec does not prescribe environment beyond catalog mapping.

### Root cause

- **Code anchors (seed):** {hs}
- **User manual:** Index `pi/user_manual/README.md` — e.g. **Report book, widgets & charts**; **Feeds, statements & custodians**; **Transactions**; **Chart of accounts** as the **Module** suggests. Search: `rg -l "keyword" pi/user_manual` from repo root.

### Competing hypotheses

{hypotheses_md(hypotheses)}

### Fast elimination plan

{fast_plan_md(hypotheses)}

### Proposed fix (behavior-level)

1. Reproduce on a controlled dataset (entity/account from PI).
2. Trace server + UI (or lambda) for the reported calculation / sync / display path.
3. Implement minimal change preserving existing API contracts; **no hardcoded** tenant URLs or secrets — use existing config/env patterns.
4. Add or extend automated tests per `pi/test-plans/{iid}.md` after approval.

### Impact / blast radius

Touches **{team}** areas; regression risk on adjacent reports/sync paths sharing the same services. Rollback: revert deployment + data fix script if any one-off cleanup is required.

### Acceptance criteria

- Reported scenario no longer reproduces on validated HC UAT / agreed environment.
- No regression on sibling flows called out in the test plan.
- Audit/logging expectations met where the PI mentions audit gaps (if applicable).

### Open questions

- Confirm **tenant** when client match is ambiguous or missing from URL CSVs.
- **Git / Bitbucket:** Workspace was not a git repo at generation time — sync with team remote before implementation per skills.

"""
        spec_path.write_text(spec, encoding="utf-8")

        plan = f"""# Test plan: {iid}

## Scope and references

- Fix spec: `pi/specs/{iid}.md`
- Product context: `pi/user_manual/README.md` and theme guides under `pi/user_manual/` (report book, feeds, transactions, GL as relevant).

## Code hotspots

| Area | Seed paths / symbols |
|------|------------------------|
| Primary | {hs} |

## Environment / data prerequisites

- Tenant URL per spec **HC UAT** mapping; entity/account IDs from PI description.
- Test data covering the reported security/period where possible.

## Verify the fix

| # | Case | Steps | Expected |
|---|------|-------|----------|
| 1 | PI scenario | Execute user flow from **Bug Description** with PI IDs | Behavior matches **Acceptance criteria** in spec |
| 2 | Negative | Adjacent filter/period | No new errors in app or server logs |

## Regression

| # | Area | Code / UX anchor | Steps |
|---|------|------------------|-------|
| 1 | Dashboard widgets | `dashboard/src/app/asset-vantage/dashboard/widget/`**,** `dashboard.service.spec.ts` | Open dashboard; load widgets of same family |
| 2 | Report book | `dashboard/src/app/asset-vantage/report-book/report-book.component.ts` | Run report book widget cited in PI |
| 3 | Lambda PAR / performance | `av_v3_lambda/src/PerformanceApiReport/par_response.py`**,** `emvCalculation.py` | Same report with alternate period |
| 4 | Settings / feeds | `controller/app/modules/settings/controllers/IndexController.php` (Electra-related actions) | Feed settings and sync smoke |

(Trim rows that are unrelated to this PI’s blast radius after dev confirms.)

## Adjacent

- Only if shared code: same service as **Code hotspots** table in spec.

## Automation mapping

{automation_table()}

- **Gap:** No `phpunit.xml` at repo root in this snapshot; PHP tests under `controller/unittest/` are sparse — prefer adding tests where team standards allow.

"""
        (PLANS / f"{iid}.md").write_text(plan, encoding="utf-8")

    print(f"Wrote {len(rows)} specs and {len(rows)} test plans.")


if __name__ == "__main__":
    main()
