#!/usr/bin/env python3
"""Generate pi/specs/{ItemId}.md and pi/test-plans/{ItemId}.md from pi/input/Book2.csv."""
from __future__ import annotations

import csv
import re
from pathlib import Path

# Repo folder that contains input/, specs/, test-plans/ (the `pi/` tree).
ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "input" / "Book2.csv"
URL_DIR = ROOT / "input" / "urls"
EVIDENCE_ZIP_DIR = ROOT / "input" / "pi-evidence"
SPECS = ROOT / "specs"
PLANS = ROOT / "test-plans"
USER_MANUAL_DIR = ROOT / "user_manual"
WORKSPACE_ROOT = ROOT.parent

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
    "system",  # avoids fuzzy match to unrelated *globalsystem* tenants when narrative says "the system"
    "securities",
    "investment",
    "investments",
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


def discover_manual_guides(module: str, name: str, bug: str, limit: int = 3) -> list[str]:
    """Rank guides by token overlap with filename + content."""
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


def _strip_ticks(pathish: str) -> str:
    return (pathish or "").strip().strip("`")


def _token_hits_for_path(rel_path: str, tokens: set[str]) -> set[str]:
    rel = _strip_ticks(rel_path)
    if not rel:
        return set()
    p = WORKSPACE_ROOT / rel
    if not p.exists() or not p.is_file():
        return set()
    try:
        text = p.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return set()
    return {tok for tok in tokens if tok in text}


def competing_markdown(hypo_list: list[dict[str, str]]) -> str:
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


def evidence_competing_hypotheses(
    module: str, name: str, bug: str, hotspots: list[str], guides: list[str]
) -> list[dict[str, str]]:
    """Generate hypotheses strictly from token overlap in discovered code + manual files."""
    query_tokens = tokenize(f"{module} {name} {bug}")
    if not query_tokens:
        return []

    code_hits_by_file: dict[str, set[str]] = {}
    for hp in hotspots:
        hits = _token_hits_for_path(hp, query_tokens)
        if hits:
            code_hits_by_file[_strip_ticks(hp)] = hits

    doc_hits_by_file: dict[str, set[str]] = {}
    for gp in guides:
        hits = _token_hits_for_path(gp, query_tokens)
        if hits:
            doc_hits_by_file[_strip_ticks(gp)] = hits

    if not code_hits_by_file or not doc_hits_by_file:
        return []

    code_tokens: set[str] = set().union(*code_hits_by_file.values())
    doc_tokens: set[str] = set().union(*doc_hits_by_file.values())
    common = sorted(code_tokens & doc_tokens, key=lambda t: (-len(t), t))
    if not common:
        return []

    hypotheses: list[dict[str, str]] = []
    for tok in common[:3]:
        code_file = next((p for p, hs in code_hits_by_file.items() if tok in hs), list(code_hits_by_file.keys())[0])
        doc_file = next((p for p, hs in doc_hits_by_file.items() if tok in hs), list(doc_hits_by_file.keys())[0])
        hypotheses.append(
            {
                "title": f"Behavior around '{tok}' may diverge from documented flow",
                "why": (
                    f"Token '{tok}' appears in PI narrative and is present in both matched code and user-manual sources."
                ),
                "code": f"`{code_file}`",
                "doc": f"`{doc_file}`",
                "disprover": (
                    f"Trace the '{tok}' path end-to-end for one failing and one passing case; "
                    "if execution and output are identical, reject this hypothesis."
                ),
                "confidence": "evidence-based (token overlap)",
            }
        )
    return hypotheses


def fast_elimination_plan(hypotheses: list[dict[str, str]]) -> list[str]:
    if not hypotheses:
        return [
            "**Check 1 (5 min):** Validate the PI can be reproduced and capture exact request/response payload.",
            "**Check 2 (10 min):** Expand code/manual search tokens from the PI narrative and regenerate evidence links.",
            "**Check 3 (15 min):** If still no overlap evidence, mark root cause as unresolved and require manual triage.",
        ]
    h1 = hypotheses[0]["title"]
    h2 = hypotheses[1]["title"] if len(hypotheses) > 1 else hypotheses[0]["title"]
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


def doc_key(row: dict) -> str:
    """Prefer PI ID for file naming; fallback to Item ID."""
    pi = (row.get("PI ID") or "").strip()
    if pi:
        return pi
    return (row.get("ITEM ID") or row.get("Item ID") or "").strip()


def spec_md(row: dict, clients: list[tuple[str, str, str]]) -> str:
    did = doc_key(row)
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

    discovered_guides = discover_manual_guides(module, name, bug)
    discovered_hotspots = discover_code_hotspots(module, name, bug)
    um = ", ".join(f"`{p}`" for p in discovered_guides) if discovered_guides else "- *(No manual guide match from current PI text.)*"
    hotspots = "\n".join(f"- {p}" for p in discovered_hotspots) if discovered_hotspots else "- *(No code hotspot match from current PI text.)*"
    repro_text = bug if bug else "*(No description in export.)*"
    status_value = row.get("Status", "").strip().lower()
    group_value = row.get("Group", "").strip().lower()
    if "closed" in status_value or "released" in status_value or "closed" in group_value:
        status_note = (
            "Item appears closed/released in source export; use this spec for RCA traceability and regression checks."
        )
    else:
        status_note = (
            "Item appears active in source export; use this spec to drive live triage and implementation."
        )

    evidence_lines: list[str] = []
    analysis_path = ROOT / "evidence-analysis" / f"{did}.md"
    if analysis_path.is_file():
        evidence_lines.append(f"- Source analysis: `pi/evidence-analysis/{did}.md`")
    zip_path = EVIDENCE_ZIP_DIR / f"{did}.zip"
    if zip_path.is_file():
        evidence_lines.append(f"- Evidence archive: `pi/input/pi-evidence/{did}.zip`")
    evidence_block = ""
    if evidence_lines:
        evidence_block = "## Evidence files\n\n" + "\n".join(evidence_lines) + "\n\n"

    return f"""# {did}: {name}

## Metadata

| Field | Value |
|------|--------|
{meta}

## Client environment URL

{client_block(iid, row.get("Client Name", "").strip(), name, bug, clients)}

## Suggested assignment

- **Team:** {team}
- **Leader:** {leader}
- **Rationale from intake fields:** {team_rationale}
{assign_note}

## Summary

{name}

## Reproduction / symptoms

{repro_text}

## Known facts from intake

- **Issue title:** {name}
- **Source narrative:** captured from Monday export (Bug Description / Days until Resolution).
- **Module (CSV):** {module if module else "(not provided)"}
- **Environment (CSV):** {row.get("Environment", "").strip() if row.get("Environment", "").strip() else "(not provided)"}
- **Current lifecycle note:** {status_note}

## Investigation inputs (seed, not conclusions)

- **Product context (candidate manuals):**
{um if um.startswith("- ") else f"- {um}"}
- **Code hotspots (candidate files):**
{hotspots}

## Investigation checklist

- Reproduce once with tenant/user/date-range from PI (or note explicit gaps).
- Capture request/response payload and at least one screenshot/PDF proving actual behavior.
- Identify first divergence point (UI state, API payload, DB row, or export renderer).
- Record confirmed root cause with concrete evidence before proposing code changes.

## Proposed fix approach

- Apply the smallest patch at the first confirmed divergence point.
- Add targeted regression coverage in the touched layer (UI/API/service).
- Keep blast radius notes specific to changed modules/classes.
- Rollback path: revert patch and rerun affected regression set.

## Acceptance criteria

- PI symptoms no longer reproduce on **HC UAT** (or agreed environment) with agreed test data.
- Root cause and fix are both backed by concrete evidence (payloads/logs/screenshots).
- No regressions in adjacent flows listed in `pi/test-plans/{did}.md`.

{evidence_block}## Open questions

- Is this confirmed AV defect vs provider/data issue?
- Which exact account/entity/date range is the acceptance baseline?
"""


def test_plan_md(doc_id: str, name: str) -> str:
    return f"""# Test plan: {doc_id}

## Scope and references

- Fix spec: `pi/specs/{doc_id}.md`
- User manual: see spec **Root cause** / `pi/user_manual/README.md` for theme index.

## Code hotspots

(See `pi/specs/{doc_id}.md` — **Investigation inputs (seed, not conclusions)**; refine during dev.)

## Environment / data prerequisites

- HC UAT tenant from spec **Client environment URL** (or human-confirmed tenant).
- Entity / account / security IDs from the PI narrative where applicable.
- Appropriate roles to access Report Book, feeds, recon, or masters screens under test.

## Verify the fix

| # | Objective | Steps | Expected |
|---|------------|-------|----------|
| 1 | Primary symptom gone | Reproduce the original PI path on HC UAT with same data | Symptom no longer occurs |
| 2 | Evidence-backed behavior | Compare payload/log/screenshot before vs after fix | Divergence is removed at confirmed root cause point |
| 3 | Data integrity | Spot-check persisted rows and exported/rendered output | Data and output remain consistent |

## Regression

| Area | Code / UX anchor | Notes |
|------|------------------|-------|
| Same module (happy path) | Touched files from implementation PR | Run happy-path smoke checks |
| Adjacent flow | Neighbor feature using shared method/component | Validate no behavior drift |
| Export/report parity | If PI affects report/PDF/widgets | Verify UI view and exported output match |

## Adjacent

- Only flows sharing the same code paths identified in the fix spec after implementation.

## Automation mapping

| Layer | Framework / location | Existing coverage | Gap |
|-------|----------------------|-------------------|-----|
| PHP (controller) | PHPUnit under `controller/unittest/` | Existing tests vary by module | Add focused unit/integration for changed service/controller |
| Angular (dashboard) | Karma/Jasmine under `dashboard/src/app/**/*.spec.ts` | Existing coverage varies by feature | Extend nearest spec for changed component/service |
| Python (av-edge-api) | Tests near `av-edge-api/app/` routes/services | Route coverage varies | Add API/service tests if backend path changed |
| Lambdas | Tests under `av_v3_lambda/` (if touched) | Function-specific | Add handler-level regression only for touched lambda |

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
            did = doc_key(row)
            iid = (row.get("ITEM ID") or row.get("Item ID") or "").strip()
            if not did:
                continue
            name = row.get("Name", "").strip()
            (SPECS / f"{did}.md").write_text(spec_md(row, clients), encoding="utf-8")
            (PLANS / f"{did}.md").write_text(test_plan_md(did, name), encoding="utf-8")
            print("wrote", did, "(item:", iid or "n/a", ")")

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
