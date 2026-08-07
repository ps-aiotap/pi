---
name: pi-similar-pis
description: >-
  Searches Jira PB for PIs similar to the source issue: scores every candidate,
  explains why in plain language, writes pi/similar/{KEY}.md for product learning
  and cross-cutting triage. Requires jira/.env credentials.
---

# PI similar-issue search (Jira)

## Location in repo

Stored under `pi/skills/pi-similar-pis/`. Symlink only (no copy) to `.cursor/skills/pi-similar-pis` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

For each **PB-*** source PI, find **all** related PIs in Jira (not only high scores), rank by **similarity score (0–100)**, and write **plain-language reasoning** so humans learn product patterns (transfers, PAR, vehicles, etc.) and spot sibling issues (e.g. MF fixed, DE still open).

Score = **relatedness for triage and learning**, not guaranteed same root cause.

## When to run

- **Mandatory** during **`pi-intake-impact-fix-spec`** when the row has a **`PB-*`** key and `jira/.env` is configured.
- **Mandatory read** during **`pi-special-cases`** — use Strong/Related matches for asset-vehicle and cross-cutting matrix rows.
- Runs **after** intake has the source key; **before** or alongside **`pi-special-cases`**.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping   # must succeed
```

## Command

From `jira/` repo root:

```bash
python -m scripts.jira_automation similar-pis PB-2888
```

Options:

| Flag | Purpose |
|------|---------|
| `--pi-dir <path>` | PI repo root (default: auto-detect `current/pi` or `pi`) |
| `--out <path>` | JSON path (default: `jira/output/similar_pis_<KEY>.json`) |
| `--no-pi` | Skip `pi/similar/<KEY>.md` |
| `--spec-section` | Print `## Similar PIs (Jira)` markdown for pasting into spec |

## Outputs

| Artifact | Path |
|----------|------|
| Full scored list (human) | `pi/similar/{KEY}.md` |
| Machine-readable | `jira/output/similar_pis_{KEY}.json` |
| Spec section | `## Similar PIs (Jira)` in `pi/specs/{KEY}.md` (intake embeds or links) |

## Score bands

| Band | Score | Meaning |
|------|-------|---------|
| **Strong** | 80–100 | Same transaction + report + symptom (e.g. PAR transfer; MF vs DE sibling) |
| **Related** | 50–79 | Same theme (transfer price in reports), different report or symptom |
| **Weak** | 20–49 | Same area (transfer/report) but different failure (upload, voucher, default account) |
| **Tangential** | 1–19 | Keyword overlap only — still listed for learning |

**All** candidates from the JQL search pool are included (no score cutoff).

## Workflow (per PI)

1. Resolve source key (`PB-*`). If only legacy `PI-*` / Monday ID with no PB key, **skip** and note in spec: *Similar PI search skipped (no PB key)*.
2. Run `similar-pis <KEY>` from `jira/` (or call `similar_pis.run_for_key` in automation).
3. Read `pi/similar/{KEY}.md`.
4. Add or update **`## Similar PIs (Jira)`** in `pi/specs/{KEY}.md`:
   - Link to full list: `pi/similar/{KEY}.md`
   - Embed the summary table (score, band, key, status, short why)
5. Optionally append to `pi/docs/process-log.md`: `YYYY-MM-DD: {KEY} similar-pis — {N} candidates`

## How to use results in triage

- **Strong + different vehicle:** treat as sibling blast-radius (see `pi/docs/pi-special-cases.md` transfer/PAR case).
- **Related:** note in **Open questions** or **Impact / blast radius** — same calculation family, verify if fix applies.
- **Weak / Tangential:** learning only unless summary clearly matches after human read.

Do **not** auto-link issues in Jira unless the human asks.

## Fallback

If `jira/.env` is missing, `ping` fails, or key is not `PB-*`:

- Do not invent similar PIs.
- In spec: *Similar PI search skipped — {reason}.*

## Relationship to other PI skills

- **`pi-intake-impact-fix-spec`** — triggers this skill and seeds `## Similar PIs (Jira)`.
- **`pi-special-cases`** — reads `pi/similar/{KEY}.md`; Strong/Related rows inform **Asset vehicles** and matrix narrative.
- Implementation: `jira/scripts/jira_automation/similar_pis.py`
