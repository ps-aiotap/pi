---
name: pi-prevention-pack
description: >-
  Manual post-close prevention backlog from confirmed Dev RCA + Leakage RCA on a PB PI.
  Code-grounded user story, design doc, and recurrence test Tasks on PM project (board 1144).
  Draft under pi/ops/drafts/ by default; create Jira issues only when human approves.
---

# PI prevention pack (problem management)

## Location in repo

Stored under `current/pi/skills/pi-prevention-pack/`. Symlink to `.cursor/skills/pi-prevention-pack` at the workspace root for Cursor Agent Skill discovery.

## Goal

After a PI has **confirmed** **Dev RCA** and **Leakage RCA** on Jira (typically post-close), produce a **prevention package** that stops the **class** of failure from recurring:

| Artifact | PM issue type | Purpose |
| --- | --- | --- |
| **User story** | Story | Backlog item — structural/process work (not “fix this one PI”) |
| **Design doc** | Task | Code-anchored technical approach (files, blast radius) |
| **Test case(s)** | Task (plain) | Recurrence prevention — not “verify this fix” |

Outputs land on the **PI Problem Management** project (**PM**, [board 1144](https://assetvantage.atlassian.net/jira/software/c/projects/PM/boards/1144)), linked **`relates to`** the source `PB-xxxx`.

**Does not** block PI closure. Typical pickup: **following sprint** if capacity allows.

## When to run

- **Manual only** — human: *"prevention pack for PB-xxxx"* or *"pi-prevention-pack PB-xxxx"*.
- After PI is **Closed** (preferred) or when you explicitly choose (Dev + Leakage RCA must be set).
- **Do not** auto-run on Closed until opted in later.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Jira fields (source PI on PB)

| Display name | Field ID | Use |
| --- | --- | --- |
| Dev RCA | `customfield_10935` | Confirmed technical root cause (search seed) |
| Leakage RCA | `customfield_11345` | Leakage category — steers prevention type |
| Leakage RCA - old | `customfield_10940` | Legacy only — do not use for new work |

Constants: `jira/scripts/jira_automation/pi_config.py` (`PM_PROJECT_KEY`, `PM_LINK_TYPE`, `LEAKAGE_RCA_OPTIONS`).

## Inputs and outputs

| | Path / target |
| --- | --- |
| Read (mandatory) | Jira `PB-*`: summary, status, Dev RCA, Leakage RCA, Team, `resolved`, `updated` |
| Read (optional) | `pi/specs/{ItemId}.md`, `pi/similar/{ItemId}.md`, `pi/test-plans/{ItemId}.md` |
| Read (optional) | Fix PR / commit hints in Jira comments |
| **Mandatory** | Application code search on current `master` (`controller/`, `dashboard/`, `av_v3_lambda/`, …) |
| Write (default) | `pi/ops/drafts/{ItemId}-prevention-pack.md` |
| Write (apply prep) | `pi/ops/drafts/{ItemId}-prevention-pack.json` — machine manifest for CLI create |
| Create (apply) | PM Story + Tasks via `python -m scripts.jira_automation prevention-pack create` |

Edit only under `pi/` and Jira **PM** project on explicit apply. Do not modify application code or PB fields.

## Early pipeline vs confirmed RCA

| Phase | Source | Trust |
| --- | --- | --- |
| Intake (`pi/specs/`, `pi-intake-impact-fix-spec`) | Hypothesis during dev | **Low** for prevention — may be wrong |
| Jira Dev RCA + Leakage RCA | Post-fix confirmed | **High** for narrative + category |
| Current code on `master` | Live repo | **Highest** for design + tests |

If `pi/specs/` disagrees with Jira RCA, flag **intake superseded** in the draft; prefer Jira + fresh code search.

## Skip rules (no PM issues)

Stop after a short note in the draft when:

| Condition | Action |
| --- | --- |
| Leakage RCA is **By Design** or **Not an Issue** | Skip — optional one-line “no systemic action” |
| Dev RCA **and** Leakage RCA both empty | Stop — run `pi-dev-rca` / `pi-leakage-rca` first |
| PM Story already **`relates to`** this `PB-xxxx` | Extend existing Story (comment + Tasks); **do not** create second Story unless human insists |

Check duplicates:

```bash
cd jira && python -m scripts.jira_automation prevention-pack check PB-xxxx
```

Or JQL: `project = PM AND issue in linkedIssues(PB-xxxx)`.

## RCA staleness (evolving code)

Old closed PIs may have **stale Dev RCA** paths after refactors. **Leakage RCA** (dropdown category) usually remains valid.

Before writing design/tests, assign **RCA confidence**:

| Level | Meaning | Action |
| --- | --- | --- |
| **VALID** | Dev RCA keywords locate current code on `master` | File-anchored design |
| **PARTIALLY_STALE** | Theme right; paths moved/renamed | Design cites **current** paths; note superseded refs |
| **UNRELIABLE** | Module gone or Dev RCA unusable | Theme-level story from Leakage RCA + summary + `pi/similar/` |

**Trust order:** current code → PI summary → Leakage RCA → Dev RCA (as search seed) → `pi/specs/` (lowest).

Always note in design Task: *Verified against `master` as of {ISO date}.*

## Source code refresh (mandatory)

Same discipline as **`pi-test-plan`** and **`pi-intake-impact-fix-spec`**:

1. **Workspace root** = parent of `pi/`. **Do not** refresh `pi/` as application source.
2. In each application clone under workspace root:

```bash
find "$WORKSPACE_ROOT" -name .git -type d | grep -v '/pi/' | sort
```

run `git fetch --prune`, checkout **`master`**, integrate with `origin/master`.

3. Search `controller/`, `dashboard/`, `av_v3_lambda/` using **keywords from Dev RCA** and PI summary — not literal stale paths without verification.
4. Cite **concrete paths** in design and test Tasks — no `@pi` aliases, no **TBD**.

## Leakage RCA → prevention steering

Use **exact** labels from `LEAKAGE_RCA_OPTIONS` in `pi_config.py` (12 values).

| Leakage RCA | Story focus | Design Task focus | Test Task focus |
| --- | --- | --- | --- |
| Legacy Code Fix / Legacy Architecture | Refactor / consolidate fragile area | Hotspot files, dedupe strategy, blast radius | Golden tests on fragile module |
| New Code Fix | Guards, validation, review checklist | Touched service paths, API contracts | Unit tests on new/changed code |
| Gap in Requirement / New Requirement | AC / spec clarity | Process + affected modules | Scenario matrix from requirement gaps |
| Configuration Update | Config validation / runbook | Config keys, env checks | Env-specific regression |
| Data Issue / Legacy Data Fix | Data quality guards | Pipeline / validation touchpoints | Fixture + validation tests |
| Feed Issue | Parser/mapper hardening | Feed mapper files | Feed regression pack |
| Infra Issue | Platform constraints | Infra dependencies | Load/timeout cases |
| By Design / Not an Issue | **Skip** | — | — |

## Clubbing policy (default 1:1)

| Rule | Policy |
| --- | --- |
| **1 PB → 1 PM Story** | Default — one `pi-prevention-pack` run |
| **1 PB → many PM Stories** | Avoid — use one Story + multiple Tasks |
| **Many PB → 1 PM Story** | **Manual only** — you club on PM board when same systemic fix |

Never auto-club multiple PIs. See `current/pi/docs/rca-gate-implementation.md` §2.5.

## Workflow

### 1. Resolve and gate

1. Resolve `{ItemId}` as **`PB-*`**.
2. Run **`prevention-pack check`** (or fetch Jira fields).
3. If skip rules apply → write minimal draft and exit.
4. If PM Story already linked → draft **add Tasks only**; ask before second Story.

### 2. Gather context

1. Fetch Jira: summary, status, priority, Team, Dev RCA, Leakage RCA, `resolved`, comments (fix hints).
2. Read `pi/specs/`, `pi/similar/`, `pi/test-plans/` if present — mark intake as hypothesis when used.
   Prefer **`## Post-RCA (confirmed)`** and **`### Cross-cutting prevention`** from reconciled test plan when present.
3. Read **`## Cross-cutting impact matrix`** in spec (`pi/docs/cross-cutting-impact-dimensions.md` for dimension IDs). Every `in-scope` / `unknown` row must appear in Test Task recurrence scope — cite dimension short names (vehicles, surfaces, stack, feed path, tenant, period/currency, txn types).
4. Refresh application clones on `master`; run mandatory code search.
5. Assign **RCA confidence** (VALID / PARTIALLY_STALE / UNRELIABLE).

### 3. Draft prevention pack

1. Write **`pi/ops/drafts/{ItemId}-prevention-pack.md`** using template below.
2. Write **`pi/ops/drafts/{ItemId}-prevention-pack.json`** manifest for CLI apply (same content, structured).
3. Tell human: review draft → say *"create prevention issues for PB-xxxx"* to apply.

### 4. Apply (human opt-in only)

Only when human explicitly says *"create prevention issues for PB-xxxx"* (or similar):

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation prevention-pack create PB-xxxx
```

Creates on **PM**:

- **1 Story** — `[PB-xxxx] Prevent recurrence: {short title}`
- **1 Task** — `[PB-xxxx] Design: …`
- **1+ Tasks** — `[PB-xxxx] Test: …` (plain Task each)

Each issue: **`relates to`** `PB-xxxx`. Story starts in **Backlog**.

**Do not** apply without human approval of the draft.

## Template — `pi/ops/drafts/{ItemId}-prevention-pack.md`

```markdown
# Prevention pack — {ItemId}

**Jira:** https://assetvantage.atlassian.net/browse/{ItemId}
**Status:** {status} · **Resolved:** {resolved date or —}
**Leakage RCA:** {value}
**RCA confidence:** VALID | PARTIALLY_STALE | UNRELIABLE
**Code verified:** master @ {ISO date}

## Source RCA

**Dev RCA:** {quote or empty}

**Leakage RCA rationale:** {1–2 sentences — why this category}

## PM Story (draft)

**Summary:** [PB-xxxx] Prevent recurrence: {short title}

**User story:** As a {role}, I want {systemic change} so that {class of failure} does not recur.

**Acceptance criteria:**
- [ ] …
- [ ] …

**Leakage category:** {Leakage RCA}

## Design Task (draft)

**Summary:** [PB-xxxx] Design: {topic}

**Problem class:** {from Dev RCA + Leakage RCA}

**Code hotspots (current master):**
| Path | Role |
| --- | --- |
| `controller/...` | … |

**Proposed approach:** {refactor / guard / validation / process}

**Blast radius:** {modules, reports, APIs}

**Intake superseded:** {yes/no — if pi/specs disagreed with Jira RCA}

## Test Task(s) (draft)

### Test 1 — {title}

**Summary:** [PB-xxxx] Test: {title}

**Intent:** Prevent recurrence of {failure class} — not verify original fix.

**Cross-cutting dimensions (in-scope from spec matrix or reconcile):** {vehicles | surfaces | stack | feed path | tenant | period/currency | txn types — or N/A}

**Steps:**
1. …

**Expected:** …

**Automation anchor:** {concrete path or "manual-only" with search evidence}

## Similar / clubbing notes

- {pi/similar highlights or "none"}
- Existing PM link: {PM-nnn or none}

## Apply

Human must say "create prevention issues for {ItemId}".
CLI: `python -m scripts.jira_automation prevention-pack create {ItemId}`
```

## JSON manifest — `pi/ops/drafts/{ItemId}-prevention-pack.json`

Written alongside the markdown draft for CLI apply:

```json
{
  "pb_key": "PB-xxxx",
  "leakage_rca": "Legacy Code Fix",
  "rca_confidence": "VALID",
  "skip": false,
  "story": {
    "summary": "[PB-xxxx] Prevent recurrence: short title",
    "description": "User story + acceptance criteria (plain text or markdown)"
  },
  "tasks": [
    {
      "kind": "design",
      "summary": "[PB-xxxx] Design: topic",
      "description": "Design doc body"
    },
    {
      "kind": "test",
      "summary": "[PB-xxxx] Test: topic",
      "description": "Test steps + expected + automation anchor"
    }
  ]
}
```

Set `"skip": true` and `"skip_reason": "..."` when no PM issues needed.

## Dual tracking reminder

PM board holds **original prevention intent**. Dev team sprint work may change scope — comment on PM Story when delivery diverges; do not rewrite original AC. See `rca-gate-implementation.md` §2.3.

## Do not

- Block PI closure or modify PB RCA fields.
- Merge recurrence tests into `pi/test-plans/` (that file verifies **this** fix; PM Tasks prevent **this class**).
- Auto-create team sprint items — you allocate from PM **Ready** when capacity allows.
- Trust `pi/specs/` file paths on old PIs without re-verifying on `master`.
- Create duplicate PM Stories for the same PB without checking linked issues.

## Related

- Runbook: `current/pi/docs/rca-gate-implementation.md` (§D problem management, §3.4)
- **`pi-dev-rca`**, **`pi-leakage-rca`**, **`pi-test-plan`**, **`pi-test-plan-reconcile`**, **`pi-similar-pis`**
- **`pi/docs/cross-cutting-impact-dimensions.md`** — recurrence Test Tasks must cover in-scope rows
- CLI: `jira/scripts/jira_automation/prevention_pack.py`
- PM provision: `python -m scripts.jira_automation provision-pm`
