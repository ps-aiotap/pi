---
name: pi-developer-domain-learn
description: >-
  Continuous learning for pi/input/team/developer-domains.json from resolved PB
  PIs — compares assign-developer predictions vs actual fixer, writes learn
  report and proposed JSON patches. Run weekly or after intake batches; apply
  only on human approval. Pair with pi-intake-impact-fix-spec assign-developer.
---

# PI developer domain learn (continuous)

## Location in repo

Stored under `current/pi/skills/pi-developer-domain-learn/`. Symlink to `.cursor/skills/pi-developer-domain-learn` at the workspace root for Cursor Agent Skill discovery.

## Goal

Keep **`developer-domains.json`** accurate as more PIs are assigned and closed:

| Input | Output |
| --- | --- |
| Recent PB PIs with **Developer** or **assignee** | Match / mismatch vs `assign-developer suggest` |
| Mismatch clusters (≥2 PIs) | Proposed keyword adds, developer changes, new domain rules |
| Human approval | Merged into `developer-domains.json` + changelog |

**Does not** auto-overwrite rules. Learning produces **drafts**; human says *"apply domain learn"* to merge.

## When to run

- **Weekly** (e.g. Monday after `pi-daily-open-analysis`) — default `--since-days 30`
- **After a batch** of intakes / closures when assignment quality is in question
- **Manual:** *"domain learn"*, *"pi-developer-domain-learn"*, *"tune developer domains"*

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping
```

## Files

| Role | Path |
| --- | --- |
| Canonical rules | `pi/input/team/developer-domains.json` |
| Rolling signals | `pi/input/team/developer-domain-signals.json` (auto-updated each run) |
| Apply changelog | `pi/input/team/developer-domains-changelog.md` |
| Learn report | `pi/reports/developer-domain-learn-YYYY-MM-DD.{md,json}` |
| Proposed patches | `pi/ops/drafts/developer-domains-proposed-YYYY-MM-DD.json` |

## Commands

```bash
cd jira && source .venv/bin/activate

# Analyze + propose (no rule changes)
python -m scripts.jira_automation domain-learn run
python -m scripts.jira_automation domain-learn run --since-days 14 --min-cluster 3

# Preview merge
python -m scripts.jira_automation domain-learn apply \
  --from ../current/pi/ops/drafts/developer-domains-proposed-YYYY-MM-DD.json \
  --dry-run

# Apply after human edits proposals JSON (remove unwanted items first)
python -m scripts.jira_automation domain-learn apply \
  --from ../current/pi/ops/drafts/developer-domains-proposed-YYYY-MM-DD.json
```

Implementation: `jira/scripts/jira_automation/domain_learn.py`.

## Workflow

### 1. Run learn

1. `domain-learn run` (adjust `--since-days` if needed).
2. Read `pi/reports/developer-domain-learn-YYYY-MM-DD.md`:
   - **Match rate** — target upward over time
   - **Mismatches** — predicted vs actual fixer
   - **Proposals** — only clusters with ≥ `--min-cluster` evidence (default 2)

### 2. Human review

1. Open `pi/ops/drafts/developer-domains-proposed-YYYY-MM-DD.json`.
2. **Delete** proposals that are one-offs, wrong team, or leader-heavy assignments.
3. **Edit** `suggested_id` / keywords for new domains — use product terms (e.g. `custom account mapping`), not bare tokens.
4. **Preserve overrides** — e.g. CAM txn → Rushikesh Bhilare — do not let a small cluster flip without explicit intent.

### 3. Apply (opt-in)

Only when human says *"apply domain learn proposals"* (or similar):

```bash
python -m scripts.jira_automation domain-learn apply --from <edited-proposals.json>
```

Creates `developer-domains.json.bak` and appends `developer-domains-changelog.md`.

### 4. Validate

Spot-check with `assign-developer suggest` on 3–5 PIs from the mismatch table — including CAM txn vs CAM UI cases.

## Proposal types

| Type | Meaning |
| --- | --- |
| `change_developer` | Rule matched but a different dev fixed ≥N PIs — suggest new default developer |
| `add_keywords` | Recurring summary tokens on mismatches — extend rule keywords |
| `new_domain` | No rule matched but same dev fixed ≥N similar PIs — suggest new domain stub |

## Agent rules

- **Never** apply without human approval of the proposals JSON.
- Prefer **keyword refinement** over **developer swaps** when txn vs UI disambiguation is involved.
- Cross-check roster: suggested developer must be a **member** of the target squad in `TeamMembers.txt`.
- After apply, mention changelog path and suggest re-running `domain-learn run` next week.

## Related

- **`pi-intake-impact-fix-spec`** — consumes `developer-domains.json` via `assign-developer`
- **`assign-developer`** — `suggest` / `apply` on single PI
- **`pi-daily-open-analysis`** — schedule peer (weekly learn)

## Do not

- Auto-run on every PI close (too noisy).
- Lower `min_cluster` below 2 without human request.
- Apply proposals that assign **leaders** when members exist on the roster.
