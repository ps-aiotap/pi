---
name: pi-intake-impact-fix-spec
description: >-
  Intakes PI rows from Jira (live API), Jira/Monday CSV, or pi/input (schema from pi/specs/pi.csv).
  Uses Jira board column as status per pi/docs/jira-pi-board-status.md (BA = Change Request).
  Fetches attachments, runs content-level pi-evidence-analysis when a zip exists, looks up
  client URLs (HC UAT links), suggests team from pi/input/team, searches repo and
  pi/user_manual/, writes fix specs under pi/specs/ and a mandatory per-run intake summary at
  pi/reports/intake-summary-YYYY-MM-DD.md (Key, Summary, board column, Jira link, HC UAT URL, spec path).
  Man-in-the-loop; no application code or test changes.
---

# PI intake, impact analysis, and fix specification

## Location in repo

This skill lives under `pi/skills/` so all PI workflow assets stay inside `pi/`. To have Cursor treat it as a first-class Agent Skill, symlink only (no copy) to `.cursor/skills/pi-intake-impact-fix-spec` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Before you start (mandatory)

### Path discipline (mandatory)

- Do **not** use `@PI`, `@pi`, or any path-indirection shorthand as source evidence.
- Do **not** use or refer to `@old_pi` for PI skill inputs, evidence, citations, or outputs.
- Use only direct repository paths explicitly defined in this skill (for example `pi/input/*.csv`, `pi/input/urls/*.csv`, `pi/input/team/*`, `pi/user_manual/`, `docs/PI/...`, and application-code paths discovered by search).
- In specs, cite evidence as concrete file paths (and line anchors for code where applicable), not folder aliases.

### No placeholder or speculative artifacts (mandatory)

- **Evidence archives:** For **`PB-*`**, run **`pi-fetch-evidence`** (or confirm zip already exists via direct `ls`) before citing `pi/input/pi-evidence/<ItemId>.zip`. Never write that path unless the file **exists** after a real check. If no attachments on Jira, state that fact; do not use "if present" or invented paths.
- **Evidence analysis (mandatory when zip exists):** After a verified zip, run **`pi-evidence-analysis`** and write `pi/evidence-analysis/<ItemId>.md` with **content-level** findings (open images; quote CSV/Excel values). Inventory-only boilerplate is invalid. Fold symptom anchors into the spec (`## Evidence analysis`). Do not write the fix spec as if attachments were unread.
- **Metadata:** If a CSV field is empty, either **omit** the row from the metadata table or state factually that the column is empty in the export—do not use `(not provided)`, `(blank)`, **TBD**, or **N/A** as generic stand-ins.
- **URLs:** Do not fabricate HC UAT links; follow **Client URL lookup** and leave tenant unresolved when there is no confident match.
- **Sections:** Do not paste boilerplate investigation checklists, fake acceptance criteria, or generic "proposed fix" bullets that repeat every PI; every sentence must tie to this row’s narrative, module, or cited code/doc paths.

### PI special cases context (mandatory)

Before processing any row, read `pi/docs/pi-special-cases.md` and apply any relevant nuance to:

- bug-vs-data-correction classification,
- root-cause framing,
- acceptance criteria,
- and open questions for humans.

Also skim `pi/docs/cross-cutting-impact-dimensions.md` so intake seeds the **Cross-cutting impact matrix** for dimensions whose triggers match the PI row (full resolution is **`pi-special-cases`**).

Read **`pi/docs/pi-pipeline-config.md`** before intake. Default: **`assign_developer_apply: false`** — suggest team/developer in the spec only; do not update Jira assignee fields unless the human opts in.

**UAT DB disprover trial (optional after spec write):** If `uat_db_disprovers_trial: true` and `pi/input/uat-db/runner.env` exists, run **`pi-uat-db-disprovers`** for the same `{ItemId}` after the spec is written — see `pi/docs/uat-db-disprovers-trial.md`. Skip when tenant is ambiguous, flag is false, or runner is not configured.

### Jira PI board status (mandatory)

Read **`pi/docs/jira-pi-board-status.md`** before interpreting **Status** on any row.

- **Status = board column:** On project **PB** board **774**, each kanban column maps to one Jira status; moving columns updates status.
- Prefer the **board column label** in spec metadata (e.g. INCOMING BUGS, IN QA, CLOSED). If the source only has the Jira status name, map using that doc’s table.
- **BA column = Change Request:** Engineering on the PI is complete; the PI will close and feature request(s) may follow. **Do not** call this “Done” in spec prose even if Jira still stores status **Done** behind the BA column until workflow is fixed.
- **Issue keys:** `PB-*` (Jira) or `PI-*` (legacy Monday); use the key from the row for `{ItemId}` filenames.

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
| What was done (log) | Append a short dated entry to `pi/docs/process-log.md` (input source, ItemIds, intake summary path) |
| Product behavior (end users) | `pi/user_manual/` — see **User manual (product context)** below |
| Jira board columns / status semantics | `pi/docs/jira-pi-board-status.md` |
| Similar PI search (Jira) | `pi/similar/{ItemId}.md` — see **`pi-similar-pis`** skill |
| Evidence zip (Jira attachments) | `pi/input/pi-evidence/{ItemId}.zip` — see **`pi-fetch-evidence`** skill |
| Evidence analysis (mandatory when zip exists) | `pi/evidence-analysis/{ItemId}.md` — see **`pi-evidence-analysis`** skill |
| Business impact (optional) | `pi/business-impact/{ItemId}.md` — see **`pi-business-impact`**; skip if `pi/docs/pi-pipeline-config.md` has `business_impact: false` |
| **Intake batch summary (mandatory per run)** | `pi/reports/intake-summary-YYYY-MM-DD.md` (+ optional `pi/reports/intake-summary-YYYY-MM-DD.json`) |

Use a safe filename token for `{ItemId}` (e.g. `PI-2148`, `PB-2912`): **`Issue key`** / **`PI ID`** from Jira when present; else **`Item ID`** / **`ITEM ID`**, stripping characters unsafe in paths.

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

## Team, leader, and developer assignment (`pi/input/team/`)

1. **Read** all files under `pi/input/team/` (today `TeamMembers.txt`; merge `developer-domains.json` for auto-assign rules).
2. **Parse** blocks: a header line `TeamName - Leader: LeaderName` followed by member names until the next blank line or next header.
3. **Suggest** one primary **team** and its **leader** (from the roster), plus an optional alternate team if ambiguous. Use, in order of weight:
   - **`Module`** from the PI row (e.g. dashboard, report, GL, ingestion, performance, transactions, platform).
   - **`TEAM`** or similar CSV hints if present (map loosely to roster names—e.g. UI/dashboard work → **Code UI**; not every CSV value maps 1:1; explain gaps).
   - **Code/doc evidence** from the repo search (which subsystem the bug touches).
4. **Heuristic map** (adjust if product renames squads): dashboard / report-book / widgets / Angular UI → **Code UI**; broad perf / scale → **Avengers performance**; GL / ledger → **Spartans GL**; data feed / ETL / ingestion → **Transformers Ingestion**; transactional workflows → **Arjun TRANSACTIONS**; cross-cutting platform / infra → **CPE - Platform**; otherwise **SCOT Misc** or closest match—**say why**.
5. **Disambiguation — Report Book vs look-through engine:** If the PI is **MF / Look Through / LT Market Cap / underlying holdings** (data missing or wrong in the look-through output, Value Research / scheme ISIN linkage, tourbillon lookthrough queries), weight **Avengers performance** (report/calculation path) and optionally **Transformers Ingestion** (feed file → DB). Do **not** default to **Code UI** solely because the menu path says “Report Book” when symptoms point at look-through data resolution.
6. **Developer suggestion (mandatory on `PB-*` intake; Jira apply is off by default):** After team suggestion, resolve a **developer** (not leader) using `pi/input/team/developer-domains.json` and CLI:
   - `cd jira && python -m scripts.jira_automation assign-developer suggest PB-xxxx`
   - Domain rules take precedence (e.g. transaction/feed **Custom Account Mapping** → **Rushikesh Bhilare**, team **Arjun**; UI-only CAM → **Code UI** / **Nitisha Telavane**).
   - **Never** leave leader as the suggested developer when the roster has other members — pick the best-matching **member**.
   - **Do not write to Jira during intake** unless the human **explicitly** asks to apply (e.g. *"apply assign-developer to PB-2951"*). Default is **suggest-only + manual review** — see `pi/docs/pi-pipeline-config.md` (`assign_developer_apply: false`).
   - When apply is off (default): record suggestions in **`pi/specs/{ItemId}.md`** only; set **Jira apply** to *Pending human review — not applied*.
   - **Apply to Jira (opt-in only):** `assign-developer apply PB-xxxx` sets **Developer** (`customfield_10933`), **Team** (`customfield_10001`), and **assignee**. Use `--dry-run` first if the human asked to preview before apply.
   - **Continuous learning:** weekly or after batches, run **`pi-developer-domain-learn`** (`domain-learn run`) to tune `developer-domains.json` from closed PIs; apply proposals only on human approval.
7. **Always** include a **Suggested assignment** subsection in `pi/specs/{ItemId}.md`: **Team** (roster + Jira), **Leader**, **Developer**, **Confidence** (`high`/`medium`/`low`), **Rationale** (domain rule id + code area), **Jira apply** (*Pending human review — not applied* unless human opted in). If CSV/Jira already has assignees, note alignment or conflict.

## PI row input (Jira API preferred; CSV legacy)

1. **Preferred:** Live Jira issue key(s) on **PB** (e.g. `PB-2888`) when `jira/.env` is available. Fetch fields via REST API; map **status** to board column per **`pi/docs/jira-pi-board-status.md`**. **No Jira CSV export required.**
2. **Evidence (mandatory pair):** Attachments on the same Jira issue — (a) **`pi-fetch-evidence`** → `pi/input/pi-evidence/{ItemId}.zip`, then (b) **`pi-evidence-analysis`** → `pi/evidence-analysis/{ItemId}.md` with content-level findings. Skip (b) only when fetch reports **no Jira attachments**. Do not require a separate evidence export.
3. **CSV (legacy):** Monday `Book2.csv` or old Jira CSV only when there is no `PB-*` key or API is unavailable. Map columns to canonical fields.
4. **Row order (CSV only):** top to bottom as in the file.
5. **Selecting input:** use `PB-*` key(s) the user specifies; legacy CSV only when explicitly requested.

### Batch execution (mandatory)

- Process PIs **one at a time, sequentially** in a single agent session (or one PI per chat turn). **Do not** fan out parallel subagents for intake batches — each PI needs Jira fetch, code search, and spec write in order; parallel runs duplicate work, contend on git/API, and are slower in practice.
- Shared CLI prep (run once before the PI loop when possible): `fetch-evidence` for all keys, then **per key** run **`pi-evidence-analysis`** (vision/CSV inspection cannot be skipped in a pure CLI batch), then `similar-pis` — write specs **sequentially** only after analysis MD exists or “no attachments” is recorded.
- After the **last** PI in the run, write the **intake batch summary** (below) — not after each PI unless the human asked for incremental saves.

## What to do

1. Load the PI row(s) from the chosen input (CSV path, Jira fetch, or explicit keys in chat).
2. For each row the user wants handled (or each row in order, if they said “process the file”):
   - Build a short PI summary from title/name, description, `Module`, **status/column** (per Jira board doc), `Priority`, `Environment`, **`Client Name`**, and other useful fields.
   - **Evidence fetch + analysis:** For `PB-*`, run **`pi-fetch-evidence`** then **`pi-evidence-analysis`** (see **`pi/skills/pi-evidence-analysis/SKILL.md`**). Require `pi/evidence-analysis/{ItemId}.md` with concrete Observed tokens whenever the zip exists. If no attachments, record *Evidence fetch: no Jira attachments* in the spec and continue.
   - **Client URL:** run the **Client URL lookup** steps using `pi/input/urls/`.
   - **Team / leader / developer:** run roster + **`developer-domains.json`** steps; run **`assign-developer suggest`** only for `PB-*` keys. **Do not** run **`assign-developer apply`** during intake unless the human explicitly requests it (see `pi/docs/pi-pipeline-config.md`).
   - **Similar PIs (Jira):** when `{ItemId}` is a **`PB-*`** key, run **`pi/skills/pi-similar-pis/SKILL.md`** (command: `cd jira && python -m scripts.jira_automation similar-pis {ItemId}`). Embed **`## Similar PIs (Jira)`** in the spec (summary table + link to `pi/similar/{ItemId}.md`). If no PB key or Jira unavailable, note *Similar PI search skipped — {reason}*.
   - Search the codebase, `docs/`, and **`pi/user_manual/`** (see **User manual**) for implementation plus **documented** behavior. Cite code as **`path:line`**; cite guides as **`pi/user_manual/<file>.md`**. Prefer search tokens taken from **evidence-analysis Extracted tokens**.
   - Write **`pi/impact/{ItemId}.md`** when a separate impact write-up helps; otherwise fold impact into the fix spec.
   - Write **`pi/specs/{ItemId}.md`** with: metadata (key columns), **Client environment URL**, **Suggested assignment** (team + leader + rationale), summary, reproduction grounded in evidence anchors when present, **`## Evidence analysis`** (link + symptom bullets), **competing hypotheses** with code/doc/**attachment** evidence, **fast elimination plan**, **fix options** at behavior level (not a full unsolicited patch), **Cross-cutting impact matrix** (seed per `pi/docs/cross-cutting-impact-dimensions.md`), blast radius, risks/rollback, acceptance criteria, open questions.
3. **Do not** edit files outside `pi/` (no application code or test changes in this phase).
4. When the user confirms the **entire** input file is done for this pass, **move** that CSV to `pi/input/processed/`.
5. **Intake batch summary (mandatory):** After finishing **every** PI in the run, write the summary per **Intake batch summary (mandatory per run)** (paths table + dedicated section below). Do not write a separate summary file per PI.
6. **Append** a brief dated line to **`pi/docs/process-log.md`** (input source, `ItemId`s handled, path to intake summary).

## Intake batch summary (mandatory per run)

Write **once** after all PIs in the run are handled. This is the human-facing index to open **HC UAT** and the spec — not a duplicate of spec content.

**Paths**

| Artifact | Path |
|----------|------|
| Markdown (required) | `pi/reports/intake-summary-YYYY-MM-DD.md` |
| JSON (optional) | `pi/reports/intake-summary-YYYY-MM-DD.json` |

Use **today’s date in IST** (`Asia/Kolkata`). If a second run happens the same day, use `intake-summary-YYYY-MM-DD-HHMM.md` (24h IST) or add a new `## Run …` section with an IST timestamp in the same file.

**Required content**

1. **Run metadata:** IST date/time, input source (e.g. “Jira live API — open PIs, four board-774 columns”), count processed.
2. **Table** — one row per PI analyzed:

| Column | Content |
|--------|---------|
| Key | `PB-xxxx` |
| Summary | Short title from Jira |
| Board column | INCOMING BUGS / In Engineering Queue / IN DEVELOPMENT / Reopened |
| Jira link | `[PB-xxxx](https://assetvantage.atlassian.net/browse/PB-xxxx)` |
| HC UAT URL | Clickable markdown link from **Client URL lookup**; `—` or *unresolved* if no match; list candidate links when ambiguous |
| Spec | Relative link to `pi/specs/{ItemId}.md` |
| Action | `created` / `updated` / `skipped` (+ brief reason if skipped) |

3. **Optional notes block:** batch CLI outcomes (evidence fetch, etc.) — not per-PI RCA. Do not note `assign-developer apply` failures during intake; apply is off by default.

**Template (copy and fill)**

```markdown
# PI intake summary — YYYY-MM-DD

**Run time (IST):** YYYY-MM-DD HH:MM  
**Input source:** Jira live API — {scope}  
**PIs processed:** N

| Key | Summary | Board column | Jira link | HC UAT URL | Spec | Action |
|-----|---------|--------------|-----------|------------|------|--------|
| PB-xxxx | … | IN DEVELOPMENT | [PB-xxxx](https://assetvantage.atlassian.net/browse/PB-xxxx) | [https://hc{tenant}.assetvantage.in](https://hc{tenant}.assetvantage.in) | [pi/specs/PB-xxxx.md](../specs/PB-xxxx.md) | updated |

**Notes:** …
```

**HC UAT URL rule:** same as specs — `hc` + tenant slug + `.assetvantage.in`; markdown link, not backticks.

## Root cause quality bar (mandatory)

The spec is **invalid** unless the root-cause section includes **at least 3 competing hypotheses** (target 3-5 when evidence supports it), and each hypothesis has:

- **Why likely:** tie to one or more PI symptoms (**prefer symptoms proven in `pi/evidence-analysis/{ItemId}.md`** when that file exists).
- **Code evidence:** at least one concrete application path (prefer `path:line` when available).
- **Product-doc evidence:** at least one `pi/user_manual/*.md` citation for expected behavior when user-facing.
- **Attachment evidence:** when a zip/analysis exists, at least one hypothesis (ideally each differentiated hypothesis) cites a concrete file + extracted token from the analysis MD.
- **Quick disprover:** one fast check that can eliminate this hypothesis (query/log/API comparison) with exact artifact to inspect.
- **Confidence:** `high`, `medium`, or `low`.

If evidence is missing, explicitly write **insufficient evidence** and list what is missing. Do not output generic filler text.

**Evidence gate:** If `pi/input/pi-evidence/{ItemId}.zip` exists on disk after fetch, the spec is also **invalid** without a non-boilerplate `pi/evidence-analysis/{ItemId}.md` and a **`## Evidence analysis`** section that lists symptom anchors (not only a link).

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
- Metadata table (from row / Jira / CSV), including **board column** or mapped status per `pi/docs/jira-pi-board-status.md`
- **Client environment URL** — **HC UAT** URL as a **clickable Markdown link**: `**HC UAT URL:** [https://…](https://…)` (`hc` + tenant on `.assetvantage.in`; see Client URL lookup); primary vs fuzzy rationale; **no** `Source:` lines or raw CSV rows; **no** backticks around the URL (that disables linking)
- **Suggested assignment** — roster team, Jira Team, leader, **developer** (member not leader), confidence, rationale; **Jira apply:** *Pending human review — not applied* (default); note alignment/conflict with existing Jira assignees
- Summary
- Reproduction / symptoms (ground in evidence anchors when analysis exists)
- **Evidence analysis** — link to `pi/evidence-analysis/{ItemId}.md` + 3–7 symptom-anchor bullets; or *no Jira attachments* / *analysis skipped — {reason}*
- **Evidence Files** — ordered filenames from the extracted archive when zip exists
- Root cause with **>=3 competing hypotheses** (why likely + code/doc/**attachment** evidence + quick disprover + confidence), concrete and non-generic
- **Fast elimination plan** (5/10/15 minute checks with branch rules)
- **Fix options** (Option A minimal patch, Option B structural fix; risks and rollback note for each)
- **Cross-cutting impact matrix** — one row per dimension whose triggers match (from `pi/docs/cross-cutting-impact-dimensions.md`); use `unknown` until **pi-special-cases** resolves; omit rows with no trigger match
- **Similar PIs (Jira)** — when `pi/similar/{ItemId}.md` exists: summary table (score, band, key, why); link to full list; call out any **Strong** match on a different asset class
- **Quick links by audience** — executive / manager / your debug / engineering (see `pi-debug-playbook` template); omit bullets for missing artifact files
- **Debug status** — table with playbook / session / my-rca links as `—` until **`pi-debug-playbook`** runs
- Impact / blast radius (narrative; reference matrix `in-scope` rows)
- Acceptance criteria
- Open questions

**After the run (not inside each spec):** intake batch summary at `pi/reports/intake-summary-YYYY-MM-DD.md` — see **Intake batch summary** above.

## Cross-cutting impact matrix (intake seed)

When writing the initial spec:

1. Match PI **Name**, **Bug Description**, and **Module** against each dimension’s **Triggers** in `pi/docs/cross-cutting-impact-dimensions.md`.
2. Add **`## Cross-cutting impact matrix`** using the template in that doc (only matching dimensions).
3. Set every seeded row to **`unknown`** unless intake repo search already proves `in-scope` or `out-of-scope` (cite path).
4. Do not replace this section with generic blast-radius text; **pi-special-cases** completes the matrix before code fix.

## Relationship to other PI skills

- **`pi-fetch-evidence`** then **`pi-evidence-analysis`** — **mandatory** for every `PB-*` with attachments **before** writing hypotheses into the spec. Analysis must be content-level (see quality bar in that skill); do not stop at zip fetch.
- **`pi-similar-pis`** runs during intake for **`PB-*`** keys (or immediately after); writes `pi/similar/{ItemId}.md`.
- **`pi-developer-domain-learn`** — weekly tune `developer-domains.json` from resolved PIs (`domain-learn run`); human approves `domain-learn apply`.
- **`pi-business-impact`** (optional, default on via `pi/docs/pi-pipeline-config.md`) runs after similar-PIs; writes `pi/business-impact/{ItemId}.md` and **`## Business impact (for engineering)`** in the spec — do not duplicate that section during intake.
- **`pi-uat-db-disprovers`** (trial, default on via `uat_db_disprovers_trial`) runs **after** spec write when `runner.env` is configured — read-only SQL disprovers; see `pi/docs/uat-db-disprovers-trial.md`.
- **`pi-debug-playbook`** runs on demand after intake; writes `pi/ops/debug/{ItemId}-playbook.md` and updates **`## Quick links by audience`** / **`## Debug status`** — do not run during intake unless human asks.
- **`pi-special-cases`** runs after intake and before **pi-legacy-php-hypothesis** / **pi-code-fix**; it reads similar-PI and optional business-impact results and resolves the matrix and expands acceptance criteria and test plans.
