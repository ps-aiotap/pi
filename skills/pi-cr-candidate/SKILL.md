---
name: pi-cr-candidate
description: >-
  Searches AV application code under the workspace (Bitbucket clones) and recommends
  whether a PB board-774 PI should stay a production bug or convert to Change Request
  (Convert_To_CR). Flags both zero-implementation and new-capability / enhancement cases.
  Writes pi/cr-candidates/{KEY}.md. Never writes to Jira unless a human asks.
---

# PI → CR candidate (codebase check)

## Location in repo

`current/pi/skills/pi-cr-candidate/` → symlink `.cursor/skills/pi-cr-candidate`.

## Goal

Decide if a PI on [board 774](https://assetvantage.atlassian.net/jira/software/c/projects/PB/boards/774) is a **true production defect** or should be routed as a **Change Request** (`Convert_To_CR` / Convert to CR - BA).

**Recommend Convert to CR when either is true:**

| Case | Meaning |
| --- | --- |
| **A — No implementation** | Described functionality / behavior does not exist in the AV app code (greenfield ask filed as a bug). |
| **B — New capability / enhancement** | Adjacent or related code exists, but the ask is clearly **new product work** (feature, option, report variant, workflow) — not a regression or broken existing path. |

**Stay PI** when the described behavior is already implemented and the report is a breakage, wrong calc, data mismatch, UX defect on an existing path, or regression.

**Never write to Jira** unless a human explicitly asks (then suggest paste-ready comment / disposition; do not auto-transition).

## Chat prompts

```text
pi-cr-candidate PB-xxxx
pi-cr-candidate PB-xxxx PB-yyyy   # batch
```

Often invoked from **`pi-daily-deep-dive`** (weekday **10:04 IST** queue → agent chat).

## Cron / run

Queue is prepared by job **`pi-daily-deep-dive`** (selects 5 IN DEVELOPMENT keys). This skill runs in Cursor after that queue (or on demand for any key).

```bash
open "current/pi/Run PI Daily Deep Dive.command"
# then chat:
pi-cr-candidate PB-xxxx
```

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

Refresh primary app clones before citing code:

```bash
bash current/pi/scripts/refresh_bitbucket_app_clones.sh --primary-only
```

**Workspace root** = parent of `pi/` (e.g. `/Users/pushpendu/data/code/av`). Search application clones there (`controller/`, `dashboard/`, `av_v3_lambda/`, `avautomation/`, plus other siblings under root / `current/`). **Do not** treat `pi/` as application code.

## Mandatory reads

1. `pi/docs/jira-pi-board-status.md` — Convert to CR semantics
2. Jira issue: summary, description, comments, attachments list (via API)
3. **Evidence:** If attachments exist, ensure `pi/evidence-analysis/{KEY}.md` exists with content-level findings (run **`pi-fetch-evidence`** + **`pi-evidence-analysis`** when missing or boilerplate). Do not decide Stay-PI vs CR from summary text alone while screenshots/Excel are unread.
4. If present: `pi/specs/{KEY}.md`, `pi/elaborations/{KEY}.md`, `pi/evidence-analysis/{KEY}.md`
5. Skim `pi/user_manual/` only for product terms that sharpen search queries

## Workflow

1. Fetch the PI from Jira (`PB-*`).
2. Extract **claimed capability**: feature/module, expected behavior, screens/APIs named in the ticket — **and** what attachments actually show (desired mock columns, error text, wrong amounts).
3. Refresh Bitbucket clones (`--primary-only`; use `--all` only if primary search is inconclusive and human agrees).
4. Search app repos for that capability (symbols, UI labels, route names, report names, menu paths). Prefer tokens from evidence analysis. Cite **concrete paths** found — or state **none found** after search.
5. Classify:

| Verdict | When |
| --- | --- |
| **Stay PI** | Implemented path exists; ticket describes defect/regression on it (attachments usually show broken existing UI/data). |
| **Convert to CR (A)** | No implementing code for the asked capability. |
| **Convert to CR (B)** | Code nearby exists, but ask is net-new capability / enhancement (attachments often show a desired layout/columns not present in product). |
| **Unclear** | Intake too thin or ambiguous to decide — list searches tried + questions. |

6. Write `pi/cr-candidates/{KEY}.md` (overwrite if re-run). Cite attachment facts under codebase / verdict rationale when present.
7. Summarize verdicts in chat. Do **not** move the ticket unless human asks.

## Output template

```markdown
# CR candidate — {KEY}

**Generated (IST):** YYYY-MM-DD HH:MM
**Jira:** https://assetvantage.atlassian.net/browse/{KEY}
**Board column / status:** …
**Summary:** …

## Verdict

**Stay PI** | **Convert to CR (A — no implementation)** | **Convert to CR (B — enhancement)** | **Unclear**

**Confidence:** high | medium | low

## Claimed capability

- What the reporter wants / expects (from intake only; mark assumptions)

## Codebase evidence

### Found (paths)
- `path` — why it matches (or why it is only adjacent)

### Not found
- Searches tried (keywords / symbols) with no hit

## Why this verdict

1–5 bullets tied to evidence above. Do not invent product requirements.

## Suggested next step

- Stay PI → continue eng fix path
- Convert to CR → paste-ready BA/product note (1–3 sentences); Leakage RCA hint: `New Requirement` when dispositioning without eng fix
- Unclear → clarifying questions for reporter / BA

## Related artifacts

- Spec / elaboration / similar (links or —)
```

## Do not

- Invent modules or cite code not found after refresh/search.
- Auto-transition to `Convert_To_CR` or post Jira comments without an explicit human ask.
- Call every missing repro step a CR — thin intake → **Unclear**, not CR.
- Confuse **post-fix** Convert to CR (eng done, follow-on FR) with **misfiled bug** (this skill’s focus). Both use the same board column eventually; state which case you mean.

## Related

- **`pi-daily-deep-dive`** — daily 5× In Development deep dives (calls this skill)
- **`pi-non-eng-disposition`** — already dispositioned Convert_To_CR / Feedback
- **`pi-intake-impact-fix-spec`** — full intake when staying on eng path
- `pi/docs/jira-pi-board-status.md`
