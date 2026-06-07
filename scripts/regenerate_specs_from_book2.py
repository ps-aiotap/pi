#!/usr/bin/env python3
"""Regenerate pi/specs/PI-*.md from Book2.csv with concrete, non-generic content."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "input" / "processed" / "Book2.csv"
URL_DIR = ROOT / "input" / "urls"
SPECS_DIR = ROOT / "specs"
EVIDENCE_DIR = ROOT / "input" / "pi-evidence"


TEAM_MAP = {
    "Transformers": ("Transformers Ingestion", "Sandip Valanju"),
    "Code": ("Code UI", "Ravi Prakash"),
    "Product Team": ("Code UI", "Ravi Prakash"),
    "Spartans": ("Spartans GL", "Anil Chandran"),
    "Arjun": ("Arjun TRANSACTIONS", "Sandip Valanju"),
    "Avengers": ("Avengers performance", "Ravi Prakash"),
    "SCOT": ("SCOT Misc", "Anil Chandran"),
}

STOPWORDS = {
    "assetvantage",
    "client",
    "issue",
    "report",
    "system",
    "data",
    "error",
    "team",
    "from",
    "with",
    "when",
    "where",
    "there",
    # Substrings of unrelated catalog slugs (e.g. lgtsecurities).
    "securities",
    "investment",
    "investments",
}


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").strip()


def narrative_text(row: dict[str, str]) -> str:
    bug = (row.get("Bug Description") or "").strip()
    if bug:
        return bug
    dur = (row.get("Days until Resolution") or "").strip()
    if dur and not re.fullmatch(r"\d+\s+days?\s+\d+(?:\.\d+)?\s+hours?", dur, flags=re.I):
        return dur
    return ""


def load_clients() -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for path in sorted(URL_DIR.glob("*.csv")):
        with path.open(newline="", encoding="utf-8", errors="replace") as f:
            for row in csv.DictReader(f):
                name = (row.get("client_name") or "").strip()
                url = (row.get("url") or "").strip()
                if name and url:
                    out.append((name, url, norm(name)))
    return out


def hc_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if not host:
        return ""
    first = host.split(".")[0]
    tenant = first if first.startswith("hc") else f"hc{first}"
    return f"https://{tenant}.assetvantage.in"


def find_client_url(row: dict[str, str], clients: list[tuple[str, str, str]]) -> tuple[str, str, str]:
    client_name = (row.get("Client Name") or "").strip()
    name = (row.get("Name") or "").strip()
    desc = narrative_text(row)

    if client_name:
        n = norm(client_name)
        exact = [(cn, url) for cn, url, nn in clients if nn == n]
        if len(exact) == 1:
            cn, url = exact[0]
            return ("Primary", f"`Client Name` matched `{cn}`.", hc_url(url))

    host_match = re.search(r"https?://([a-z0-9-]+)\.assetvantage\.(?:com|in)", f"{name} {desc}", re.I)
    if host_match:
        token = norm(host_match.group(1).removeprefix("hc"))
        hits = [(cn, url) for cn, url, nn in clients if nn == token]
        if len(hits) == 1:
            cn, url = hits[0]
            return ("From URL", f"Hostname token matched `{cn}`.", hc_url(url))

    tokens = [t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9]{3,}", f"{name} {desc}")]
    for token in sorted(set(tokens), key=len, reverse=True):
        if token in STOPWORDS:
            continue
        tn = norm(token)
        hits = [(cn, url) for cn, url, nn in clients if tn and (tn in nn or nn in tn)]
        uniq = list({cn: (cn, url) for cn, url in hits}.values())
        if len(uniq) == 1:
            cn, url = uniq[0]
            return ("Fuzzy", f"Token `{token}` matched `{cn}`.", hc_url(url))

    return ("None", "No confident tenant match from CSV or narrative.", "")


def get_team(team_csv: str) -> tuple[str, str]:
    team_csv = (team_csv or "").strip()
    return TEAM_MAP.get(team_csv, ("SCOT Misc", "Anil Chandran"))


def build_spec(row: dict[str, str], clients: list[tuple[str, str, str]]) -> str:
    pi_id = (row.get("PI ID") or "").strip()
    title = (row.get("Name") or "").strip()
    item_id = (row.get("Item ID") or row.get("ITEM ID") or "").strip()
    description = narrative_text(row)
    match_type, match_note, hc = find_client_url(row, clients)
    suggested_team, suggested_lead = get_team((row.get("TEAM") or "").strip())

    metadata_fields = [
        ("Item ID", item_id),
        ("Group", row.get("Group", "")),
        ("Status", row.get("Status", "")),
        ("Priority", row.get("Priority", "")),
        ("Report Date", row.get("Report Date", "")),
        ("Environment", row.get("Environment", "")),
        ("Module", row.get("Module", "")),
        ("Reporter", row.get("Reporter", "")),
        ("Assigned To", row.get("Assigned To", "")),
        ("Developer", row.get("Developer", "")),
        ("TEAM (CSV)", row.get("TEAM", "")),
        ("Resolution", row.get("Resolution", "")),
        ("Dev RCA", row.get("Dev RCA", "")),
    ]
    metadata_rows = "\n".join(f"| {k} | {md_escape(v)} |" for k, v in metadata_fields)

    evidence: list[str] = []
    pic = (row.get("Picture/Video") or "").strip()
    if pic:
        evidence.append(f"- Monday **Picture/Video**: {pic}")
    zip_path = EVIDENCE_DIR / f"{pi_id}.zip"
    if zip_path.is_file():
        evidence.append(f"- Evidence archive: `pi/input/pi-evidence/{pi_id}.zip`")

    notes = []
    for key, label in [
        ("RCA", "RCA"),
        ("Leakage RCA", "Leakage RCA"),
        ("Sanity Test Coverage", "Sanity Test Coverage"),
        ("Automation Feasibility", "Automation Feasibility"),
        ("Release Impact", "Release Impact"),
        ("High Priority", "High Priority"),
        ("Automation Candidate", "Automation Candidate"),
        ("Within 30 days", "Within 30 days"),
    ]:
        value = (row.get(key) or "").strip()
        if value:
            notes.append(f"- {label}: {value}")

    team_csv = (row.get("TEAM") or "").strip()
    team_why = (
        f"CSV **TEAM** is `{team_csv}`."
        if team_csv
        else "CSV **TEAM** field is empty in this export."
    )

    hc_line = f"- HC UAT URL: {hc}" if hc else "- HC UAT URL: not resolved (no catalog match)."
    desc_block = description if description else "**Bug Description** is empty in this Book2 export."

    evidence_section = ""
    if evidence:
        evidence_lines = "\n".join(evidence)
        evidence_section = f"""
## Evidence and references

{evidence_lines}
"""
    notes_section = ""
    if notes:
        notes_lines = "\n".join(notes)
        notes_section = f"""
## Additional intake notes

{notes_lines}
"""

    return f"""# {pi_id}: {title}

## Metadata

| Field | Value |
|---|---|
{metadata_rows}

## Client environment URL

- Match type: {match_type}
- Match notes: {match_note}
{hc_line}

## Suggested assignment

- Suggested Team: {suggested_team}
- Suggested Lead: {suggested_lead}
- Rationale: {team_why} Compare with **Assigned To** / **Developer** in metadata.

## Issue summary

{title}

## Reported behavior

{desc_block}
{evidence_section}{notes_section}
"""


def main() -> None:
    if not INPUT_CSV.exists():
        raise SystemExit(f"Input CSV not found: {INPUT_CSV}")

    clients = load_clients()
    SPECS_DIR.mkdir(parents=True, exist_ok=True)

    generated: set[str] = set()
    with INPUT_CSV.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        for row in csv.DictReader(f):
            pi_id = (row.get("PI ID") or "").strip()
            if not pi_id.startswith("PI-"):
                continue
            content = build_spec(row, clients)
            (SPECS_DIR / f"{pi_id}.md").write_text(content, encoding="utf-8")
            generated.add(pi_id)

    # Remove stale PI specs that are no longer in the latest Book2 export.
    for path in SPECS_DIR.glob("PI-*.md"):
        if path.stem not in generated:
            path.unlink()

    print(f"Regenerated {len(generated)} specs in {SPECS_DIR}")


if __name__ == "__main__":
    main()
