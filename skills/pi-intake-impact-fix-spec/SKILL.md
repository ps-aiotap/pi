---
name: pi-intake-impact-fix-spec
description: >-
  Reads PI CSVs from pi/input (schema from pi/specs/pi.csv), looks up client URLs in
  pi/input/urls (exact + fuzzy client match), suggests team and leader from pi/input/team, searches the repo and
  pi/user_manual/ (Asset Vantage end-user guides) for expected behavior and terminology, writes impact analysis
  and a detailed fix specification under pi/ only. Man-in-the-loop phase; does not change application code or tests.
---

# PI intake, impact analysis, and fix specification

## Location in repo

This skill lives under `pi/skills/` so all PI workflow assets stay inside `pi/`. To have Cursor treat it as a first-class Agent Skill, copy or symlink this directory to `.cursor/skills/pi-intake-impact-fix-spec` at the project root.

## Before you start (mandatory)

### Path discipline (mandatory)

- Do **not** use `@PI`, `@pi`, or any path-indirection shorthand as source evidence.
- Do **not** use or refer to `@old_pi` for PI skill inputs, evidence, citations, or outputs.
- Use only direct repository paths explicitly defined in this skill (for example `pi/input/*.csv`, `pi/input/urls/*.csv`, `pi/input/team/*`, `pi/user_manual/`, `docs/PI/...`, and application-code paths discovered by search).
- In specs, cite evidence as concrete file paths (and line anchors for code where applicable), not folder aliases.

### PI special cases context (mandatory)

Before processing any row, read `pi/docs/pi-special-cases.md` and apply any relevant nuance to:

- bug-vs-data-correction classification,
- root-cause framing,
- acceptance criteria,
- and open questions for humans.

### Source code refresh (Bitbucket application clones)

**Workspace root** is the directory that **contains** `pi/` as a subdirectory (for example the folder next to `controller/`, `dashboard/`, `av_v3_lambda/`). That folder often has **no** `.git` of its own; application source is usually **several separate Bitbucket clones**, each with its own `.git`.

1. **Do not refresh `pi/` here.** The `pi/` tree is a **separate repository** (typically **GitHub**) used for PI workflow, CSVs, specs, skills, and user-manual Markdown. Syncing `pi/` is **out of scope** for this step unless a human explicitly asks to update that repo.

2. **Before** searching application code or citing paths in specs, refresh **every Bitbucket clone** under the workspace root **except** anything under `pi/`:
   - Set `WORKSPACE_ROOT` to the parent of `pi/` (the directory you `cd` to so that `test -d pi` succeeds).
   - List clone roots (each line is a `.git` directory; exclude the PI repo and nested paths under `pi/`):

     ```bash
     find "$WORKSPACE_ROOT" -name .git -type d | grep -v '/pi/' | sort
     ```

   - For **each** listed `.git`, in the **parent** of that `.git` directory: run `git fetch --prune`, check out **`master`**, then integrate **`master`** with the default remote (usually `origin`) so the **working tree** matches the latest remote tip—for example `git checkout master` then `git pull --ff-only origin master`, or `git pull --rebase origin master`, or `git merge origin/master` if your team does not use fast-forward-only. **All** such application repos must be on up-to-date **`master`** before searching or citing application code.

3. If the network is unavailable, **any** clone fails to fetch/pull, **`master` is missing** on a remote, git state is ambiguous, or **any** integration would conflict with local work, **stop** and get direction from a human.

Do not hardcode Bitbucket URLs; use each clone’s configured remote (typically `origin`). The integration branch for application clones is **`master`** unless a human explicitly overrides in chat.

## Paths (workspace root = parent directory containing `pi/`)

| Role | Path |
|------|------|
| Column schema + fix specs (same folder) | `pi/specs/pi.csv` (headers only) and `pi/specs/{ItemId}.md` (fix spec) |
| Pending PI exports | `pi/input/*.csv` (PI-related CSVs only; not inside `processed/`) |
| Client tenant → base URL | `pi/input/urls/*.csv` (e.g. `us_clients.csv`, `india_clients.csv`): columns `client_name`, `url` |
| Team roster (squads + leaders) | `pi/input/team/*` (e.g. `TeamMembers.txt`: blocks `TeamName - Leader: Name` then member lines) |
| After processing a file | Move `pi/input/<file>.csv` → `pi/input/processed/<file>.csv` |
| Impact notes (optional) | `pi/impact/{ItemId}.md` |
| What was done (optional log) | Append a short dated entry to `pi/docs/process-log.md` (file, rows / ItemIds) |
| Product behavior (end users) | `pi/user_manual/` — see **User manual (product context)** below |

Use a safe filename token for `{ItemId}` (e.g. `PI-2148`): take the value from **`Item ID`**, or if empty **`ITEM ID`**, stripping characters unsafe in paths.

## User manual (product context)

Use **`pi/user_manual/`** alongside code and `docs/` so specs reflect **documented** product behavior, menu paths, and domain terms.

1. **Index:** Read or skim **`pi/user_manual/README.md`** for the theme index (GL, transactions, report book, corporate actions, partnership, performance, AV Pro, etc.) and conventions (slugged filenames, duplicate guides with `_1` suffix—prefer the business process that matches the PI; note conflicts in open questions).
2. **Discovery:** From the PI row, search guides by **`Module`**, feature names, and phrases from **`Bug Description`** / **`Name`**. From the repo root, e.g. `rg -l "keyword" pi/user_manual` (try synonyms: “wash sale”, “report book”, “locked period”).
3. **Use in outputs:** When a guide matches, open the Markdown file and fold **expected steps, screen names, and definitions** into **Reproduction**, **acceptance criteria**, and **root-cause hypothesis** (contrast “what docs say” vs “what the bug reports”). Cite guides as **`pi/user_manual/<filename>.md`** (no need to paste long excerpts—point to the file and the relevant section heading if clear).
4. **Limits:** Images may reference missing `media/` assets; rely on written steps. Filename typos in the index (e.g. `general_legder`) match on-disk names—use those paths literally.
5. **Mismatch:** If code and user manual disagree, **state both** and flag whether the fix should align code to docs, update docs, or treat as undocumented behavior (open question for humans).

## Client URL lookup (`pi/input/urls/`)

1. **Read** every `*.csv` under `pi/input/urls/` (do not hardcode only US or India; new region files should work automatically).
2. **Primary match — `Client Name`:** Compare the PI row’s **`Client Name`** to CSV **`client_name`** after normalizing: trim, lowercase, collapse internal spaces; treat hyphen/underscore equivalently if helpful. Exact equality after normalization wins.
3. **Fuzzy match — when primary fails or `Client Name` is empty:**  
   - Build **candidate tokens** from PI text: **`Name`**, **`Bug Description`**, and (if needed) other narrative columns—extract plausible **tenant hints** (company fragments, surnames, well-known client nicknames). Normalize tokens the same way as `client_name`. Ignore very short tokens (shorter than **4 characters**) unless they are a clear whole-word match in context.  
   - For each token, search all **`client_name`** values: **substring match** in either direction (token contained in `client_name`, or `client_name` contained in token), still case-insensitive — but **reject** matches where a short token is only an **embedded** substring inside a longer slug (e.g. `found` inside `bellwetherfoundation`) unless the token is a plausible prefix/suffix of the normalized slug or is long enough (e.g. ≥ 8 characters) to be intentional; also exclude narrative stopwords (`found`, `team`, `issue`, …) as tokens.  
   - **Uniqueness:** Use a fuzzy hit only if **exactly one** `client_name` qualifies for that token across all URL CSVs. If **zero** hits, say no match. If **multiple** hits, list candidate `client_name`s + HC UAT URLs and flag **ambiguous — human must confirm**; do not pick one arbitrarily. Render each HC UAT URL as a **markdown link** (same pattern as step 5).  
   - **Label** the result in the spec as **Fuzzy match** and cite the token(s) and fields used (e.g. “token `ruben` from **Name** → `rubencompanies`”). If the human has stated the tenant explicitly in chat (e.g. “client is rubencompanies”), treat that as an override: normalize and match **`client_name`** first before broader fuzzy text extraction.
4. **If exactly one row is selected** (primary or fuzzy): take the catalog **`url`** from CSV (e.g. `https://{tenant}.assetvantage.com`) for lookup validation only.
5. **HC UAT URL in specs:** The URL to show in **`pi/specs/{ItemId}.md`** (and optional impact doc) is the **HC UAT** host: prefix the tenant subdomain with **`hc`** and use the **`.in`** domain. Example: `https://rubencompanies.assetvantage.com` → **`https://hcrubencompanies.assetvantage.in`**. Parse the catalog URL’s hostname: first DNS label = tenant slug; HC UAT hostname = `hc` + that label + remainder of the host, with the top-level domain set to `.in` (e.g. `.assetvantage.in`). If the catalog URL uses a nonstandard pattern, apply the same “`hc` + tenant label + .in domain” rule and note any assumption.  
   **Clickable Markdown:** On its own line under **Client environment URL**, emit the HC UAT URL as an inline link so previews (Cursor, GitHub, etc.) make it clickable — **not** wrapped in backticks. Use this shape (replace with the computed URL):  
   `**HC UAT URL:** [https://hcluzerne.assetvantage.in](https://hcluzerne.assetvantage.in)`  
   Link text and destination must be the same full `https://` URL. For **ambiguous** fuzzy matches, list each candidate URL the same way (markdown link per URL).
6. **If no match:** state that in the output; do not invent URLs. Note whether `Client Name` was empty, narrative gave no unique token, or tenant is missing from the lists.
7. **If duplicate `client_name` in different files** with same URL pattern: still one logical tenant; if URLs differ, treat as ambiguity.
8. **Client environment URL subsection — do not** paste internal provenance such as `Source: pi/input/urls/...` or raw CSV lines. Keep **Primary** vs **Fuzzy** rationale and the **HC UAT** URL only (no file paths or comma-separated row echoes). The HC UAT line must use the **clickable Markdown link** format from step 5.

## Team and leader suggestion (`pi/input/team/`)

1. **Read** all files under `pi/input/team/` (today `TeamMembers.txt`; future files should be merged conceptually by parsing the same pattern).
2. **Parse** blocks: a header line `TeamName - Leader: LeaderName` followed by member names until the next blank line or next header.
3. **Suggest** one primary **team** and its **leader** (from the roster), plus an optional alternate team if ambiguous. Use, in order of weight:
   - **`Module`** from the PI row (e.g. dashboard, report, GL, ingestion, performance, transactions, platform).
   - **`TEAM`** or similar CSV hints if present (map loosely to roster names—e.g. UI/dashboard work → **Code UI**; not every CSV value maps 1:1; explain gaps).
   - **Code/doc evidence** from the repo search (which subsystem the bug touches).
4. **Heuristic map** (adjust if product renames squads): dashboard / report-book / widgets / Angular UI → **Code UI**; broad perf / scale → **Avengers performance**; GL / ledger → **Spartans GL**; data feed / ETL / ingestion → **Transformers Ingestion**; transactional workflows → **Arjun TRANSACTIONS**; cross-cutting platform / infra → **CPE - Platform**; otherwise **SCOT Misc** or closest match—**say why**.
5. **Disambiguation — Report Book vs look-through engine:** If the PI is **MF / Look Through / LT Market Cap / underlying holdings** (data missing or wrong in the look-through output, Value Research / scheme ISIN linkage, tourbillon lookthrough queries), weight **Avengers performance** (report/calculation path) and optionally **Transformers Ingestion** (feed file → DB). Do **not** default to **Code UI** solely because the menu path says “Report Book” when symptoms point at look-through data resolution.
6. **Always** include a **Suggested assignment** subsection in `pi/specs/{ItemId}.md`: **Team**, **Leader**, **Rationale** (PI fields + code area + roster citation). If the CSV already has `Assigned To` / `Developer`, mention whether it aligns with the suggestion or conflicts.

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
   - Search the codebase, `docs/`, and **`pi/user_manual/`** (see **User manual**) for implementation plus **documented** behavior. Cite code as **`path:line`**; cite guides as **`pi/user_manual/<file>.md`**.
   - Write **`pi/impact/{ItemId}.md`** when a separate impact write-up helps; otherwise fold impact into the fix spec.
  - Write **`pi/specs/{ItemId}.md`** with: metadata (key columns), **Client environment URL**, **Suggested assignment** (team + leader + rationale), summary, reproduction, **competing hypotheses** with evidence, **fast elimination plan**, **fix options** at behavior level (not a full unsolicited patch), blast radius, risks/rollback, acceptance criteria, open questions.
3. **Do not** edit files outside `pi/` (no application code or test changes in this phase).
4. When the user confirms the **entire** input file is done for this pass, **move** that CSV to `pi/input/processed/`.
5. Optionally **append** a brief dated line to **`pi/docs/process-log.md`** (input filename, `ItemId`s handled).

## Root cause quality bar (mandatory)

The spec is **invalid** unless the root-cause section includes **at least 3 competing hypotheses** (target 3-5 when evidence supports it), and each hypothesis has:

- **Why likely:** tie to one or more PI symptoms.
- **Code evidence:** at least one concrete application path (prefer `path:line` when available).
- **Product-doc evidence:** at least one `pi/user_manual/*.md` citation for expected behavior when user-facing.
- **Quick disprover:** one fast check that can eliminate this hypothesis (query/log/API comparison) with exact artifact to inspect.
- **Confidence:** `high`, `medium`, or `low`.

If evidence is missing, explicitly write **insufficient evidence** and list what is missing. Do not output generic filler text.

### Hypothesis quality rules (mandatory)

- Every hypothesis must be **concrete and actionable**: name the failing boundary (API/filter/join/cache/job/formatter/etc.), not a vague area.
- Do **not** use generic placeholders (for example "data issue", "code issue", "investigate module", "tenant-specific issue") unless immediately narrowed to a concrete mechanism and check.
- Do **not** use manual verification instructions as hypotheses or disprovers (for example "verify manually", "ask QA to check"). Disprovers must be runnable checks on logs, payloads, SQL results, or code branches.
- Prefer hypotheses that are **mutually differentiable** by the fast elimination checks (each check should meaningfully raise/lower confidence in at least one hypothesis).

### Reject phrases (unless backed by concrete evidence)

Do not use placeholders such as:

- “triage required”
- “module-specific behavior gap”
- “confirm manually”
- “needs investigation”

unless immediately followed by specific code/doc/data checks that can confirm or disprove in <= 15 minutes.

## Fast elimination plan (mandatory)

Add a **Fast elimination plan** section with 3 timed checks:

- **Check 1 (5 min)** — quickest differentiator.
- **Check 2 (10 min)** — confirm data path or filter logic.
- **Check 3 (15 min)** — isolate boundary (API vs persistence vs rendering/report).

Each check must include:

- exact location (file/symbol/query/log endpoint),
- expected outcomes,
- branch rule (`if A -> likely H1`, `else -> likely H2/H3`).
- concrete output artifact (log line, SQL row count, JSON field/value, stack frame) so the decision is auditable.

## Fix spec section checklist

- Title and `ItemId`
- Metadata table (from CSV)
- **Client environment URL** — **HC UAT** URL as a **clickable Markdown link**: `**HC UAT URL:** [https://…](https://…)` (`hc` + tenant on `.assetvantage.in`; see Client URL lookup); primary vs fuzzy rationale; **no** `Source:` lines or raw CSV rows; **no** backticks around the URL (that disables linking)
- **Suggested assignment** — team name, leader (from `pi/input/team/`), rationale; note alignment/conflict with CSV assignees if any
- Summary
- Reproduction / symptoms
- Root cause with **>=3 competing hypotheses** (why likely + code/doc evidence + quick disprover + confidence), concrete and non-generic
- **Fast elimination plan** (5/10/15 minute checks with branch rules)
- **Fix options** (Option A minimal patch, Option B structural fix; risks and rollback note for each)
- Impact / blast radius
- Acceptance criteria
- Open questions
