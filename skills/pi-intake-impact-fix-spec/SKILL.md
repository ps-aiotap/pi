---
name: pi-intake-impact-fix-spec
description: >-
  Reads PI CSVs from pi/input (schema from pi/specs/pi.csv), looks up client URLs in
  pi/input/urls (exact + fuzzy client match), suggests team and leader from pi/input/team, searches the repo for
  relevant code and docs, writes impact analysis and a detailed fix specification
  under pi/ only. Man-in-the-loop phase; does not change application code or tests.
---

# PI intake, impact analysis, and fix specification

## Location in repo

This skill lives under `pi/skills/` so all PI workflow assets stay inside `pi/`. To have Cursor treat it as a first-class Agent Skill, copy or symlink this directory to `.cursor/skills/pi-intake-impact-fix-spec` at the project root.

## Before you start (mandatory)

From the **repository root**, sync with the team remote on Bitbucket before searching application code or writing specs that cite it: run `git fetch`, then integrate the latest changes using your team’s practice (for example `git pull` on the branch you use for PI work, or rebase onto the appropriate `origin/...` branch). If the network is unavailable, git state is ambiguous, or a pull would conflict with local work, **stop** and get direction from a human rather than assuming the tree is current.

## Paths (workspace root = repository root)

| Role | Path |
|------|------|
| Column schema + fix specs (same folder) | `pi/specs/pi.csv` (headers only) and `pi/specs/{ItemId}.md` (fix spec) |
| Pending PI exports | `pi/input/*.csv` (PI-related CSVs only; not inside `processed/`) |
| Client tenant → base URL | `pi/input/urls/*.csv` (e.g. `us_clients.csv`, `india_clients.csv`): columns `client_name`, `url` |
| Team roster (squads + leaders) | `pi/input/team/*` (e.g. `TeamMembers.txt`: blocks `TeamName - Leader: Name` then member lines) |
| After processing a file | Move `pi/input/<file>.csv` → `pi/input/processed/<file>.csv` |
| Impact notes (optional) | `pi/impact/{ItemId}.md` |
| What was done (optional log) | Append a short dated entry to `pi/docs/process-log.md` (file, rows / ItemIds) |

Use a safe filename token for `{ItemId}` (e.g. `PI-2148`): take the value from **`Item ID`**, or if empty **`ITEM ID`**, stripping characters unsafe in paths.

## Client URL lookup (`pi/input/urls/`)

1. **Read** every `*.csv` under `pi/input/urls/` (do not hardcode only US or India; new region files should work automatically).
2. **Primary match — `Client Name`:** Compare the PI row’s **`Client Name`** to CSV **`client_name`** after normalizing: trim, lowercase, collapse internal spaces; treat hyphen/underscore equivalently if helpful. Exact equality after normalization wins.
3. **Fuzzy match — when primary fails or `Client Name` is empty:**  
   - Build **candidate tokens** from PI text: **`Name`**, **`Bug Description`**, and (if needed) other narrative columns—extract plausible **tenant hints** (company fragments, surnames, well-known client nicknames). Normalize tokens the same way as `client_name`. Ignore very short tokens (shorter than **4 characters**) unless they are a clear whole-word match in context.  
   - For each token, search all **`client_name`** values: **substring match** in either direction (token contained in `client_name`, or `client_name` contained in token), still case-insensitive.  
   - **Uniqueness:** Use a fuzzy hit only if **exactly one** `client_name` qualifies for that token across all URL CSVs. If **zero** hits, say no match. If **multiple** hits, list candidate `client_name`s + URLs and flag **ambiguous — human must confirm**; do not pick one arbitrarily.  
   - **Label** the result in the spec as **Fuzzy match** and cite the token(s) and fields used (e.g. “token `ruben` from **Name** → `rubencompanies`”). If the human has stated the tenant explicitly in chat (e.g. “client is rubencompanies”), treat that as an override: normalize and match **`client_name`** first before broader fuzzy text extraction.
4. **If exactly one row is selected** (primary or fuzzy): take the catalog **`url`** from CSV (e.g. `https://{tenant}.assetvantage.com`) for lookup validation only.
5. **HC UAT URL in specs:** The URL to show in **`pi/specs/{ItemId}.md`** (and optional impact doc) is the **HC UAT** host: prefix the tenant subdomain with **`hcuat`**. Example: `https://rubencompanies.assetvantage.com` → **`https://hcuatrubencompanies.assetvantage.com`**. Parse the catalog URL’s hostname: first DNS label = tenant slug; HC UAT hostname = `hcuat` + that label + remainder of the host (e.g. `.assetvantage.com`). If the catalog URL uses a nonstandard pattern, apply the same “`hcuat` + tenant label” rule and note any assumption.
6. **If no match:** state that in the output; do not invent URLs. Note whether `Client Name` was empty, narrative gave no unique token, or tenant is missing from the lists.
7. **If duplicate `client_name` in different files** with same URL pattern: still one logical tenant; if URLs differ, treat as ambiguity.
8. **Client environment URL subsection — do not** paste internal provenance such as `Source: pi/input/urls/...` or raw CSV lines. Keep **Primary** vs **Fuzzy** rationale and the **HC UAT** URL only (no file paths or comma-separated row echoes).

## Team and leader suggestion (`pi/input/team/`)

1. **Read** all files under `pi/input/team/` (today `TeamMembers.txt`; future files should be merged conceptually by parsing the same pattern).
2. **Parse** blocks: a header line `TeamName - Leader: LeaderName` followed by member names until the next blank line or next header.
3. **Suggest** one primary **team** and its **leader** (from the roster), plus an optional alternate team if ambiguous. Use, in order of weight:
   - **`Module`** from the PI row (e.g. dashboard, report, GL, ingestion, performance, transactions, platform).
   - **`TEAM`** or similar CSV hints if present (map loosely to roster names—e.g. UI/dashboard work → **Code UI**; not every CSV value maps 1:1; explain gaps).
   - **Code/doc evidence** from the repo search (which subsystem the bug touches).
4. **Heuristic map** (adjust if product renames squads): dashboard / report-book / widgets / Angular UI → **Code UI**; broad perf / scale → **Avengers performance**; GL / ledger → **Spartans GL**; data feed / ETL / ingestion → **Transformers Ingestion**; transactional workflows → **Arjun TRANSACTIONS**; cross-cutting platform / infra → **CPE - Platform**; otherwise **SCOT Misc** or closest match—**say why**.
5. **Always** include a **Suggested assignment** subsection in `pi/specs/{ItemId}.md`: **Team**, **Leader**, **Rationale** (PI fields + code area + roster citation). If the CSV already has `Assigned To` / `Developer`, mention whether it aligns with the suggestion or conflicts.

## CSV rules

1. **Headers** must match the names in `pi/specs/pi.csv` (same columns; order may differ—map by header name).
2. **Row order:** process data rows top to bottom as they appear in the file.
3. **Selecting which file:** use the path the user specifies; if none, use one file under `pi/input/` (if several, prefer the one the user names next, or ask—do not silently merge multiple files).

## What to do

1. Read the chosen CSV from `pi/input/`.
2. For each row the user wants handled (or each row in order, if they said “process the file”):
   - Build a short PI summary from `Name`, `Bug Description`, `Module`, `Status`, `Priority`, `Environment`, **`Client Name`**, and other useful columns.
   - **Client URL:** run the **Client URL lookup** steps using `pi/input/urls/`.
   - **Team / leader:** run the **Team and leader suggestion** steps using `pi/input/team/`.
   - Search the codebase and `docs/` for relevant implementation and references (ripgrep, semantic exploration, read files). Cite evidence as **`path:line`** where possible.
   - Write **`pi/impact/{ItemId}.md`** when a separate impact write-up helps; otherwise fold impact into the fix spec.
   - Write **`pi/specs/{ItemId}.md`** with: metadata (key columns), **Client environment URL**, **Suggested assignment** (team + leader + rationale), summary, reproduction, root-cause hypothesis with evidence, proposed fix at **behavior level** (not a full unsolicited patch), blast radius, risks/rollback, acceptance criteria, open questions.
3. **Do not** edit files outside `pi/` (no application code or test changes in this phase).
4. When the user confirms the **entire** input file is done for this pass, **move** that CSV to `pi/input/processed/`.
5. Optionally **append** a brief dated line to **`pi/docs/process-log.md`** (input filename, `ItemId`s handled).

## Fix spec section checklist

- Title and `ItemId`
- Metadata table (from CSV)
- **Client environment URL** — **HC UAT** URL (`hcuat` + tenant label; see Client URL lookup); primary vs fuzzy rationale; **no** `Source:` lines or raw CSV rows
- **Suggested assignment** — team name, leader (from `pi/input/team/`), rationale; note alignment/conflict with CSV assignees if any
- Summary
- Reproduction / symptoms
- Root cause (hypothesis + code/doc citations)
- Proposed fix (behavior-level)
- Impact / blast radius
- Acceptance criteria
- Open questions
