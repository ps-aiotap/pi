---
name: pi-fetch-evidence
description: >-
  Downloads attachments from a Jira PB issue via API and builds
  pi/input/pi-evidence/<KEY>.zip for pi-evidence-analysis. No manual export
  or Monday download required when creds are configured.
---

# PI fetch evidence (Jira attachments)

## Location in repo

Stored under `pi/skills/pi-fetch-evidence/`. Symlink only (no copy) to `.cursor/skills/pi-fetch-evidence` — see `pi/docs/pi-skills-catalog.md` § Skill discovery.

## Goal

PI evidence lives on **Jira attachments**, not in CSV exports. This skill pulls those files into the zip contract expected by **`pi-evidence-analysis`**.

## When to run

- **First step** in the PI pipeline for any **`PB-*`** key (before **`pi-evidence-analysis`**).
- Re-run with `--force` when attachments on Jira changed.

## Prerequisites

```bash
cd jira && source .venv/bin/activate
python -m scripts.jira_automation ping   # must succeed
```

## Command

From `jira/` repo root:

```bash
python -m scripts.jira_automation fetch-evidence PB-2888
python -m scripts.jira_automation fetch-evidence PB-2888 --force   # refresh
```

## Outputs

| Artifact | Path |
|----------|------|
| Evidence zip (flat files) | `pi/input/pi-evidence/{KEY}.zip` |
| Download manifest | `jira/output/evidence_{KEY}.json` |

Included file types by default: images, video, CSV, Excel, PDF, Office docs, text/logs. Use `--all` on the CLI to include every attachment type.

## Workflow

1. Resolve `{ItemId}` as **`PB-*`**.
2. Run `fetch-evidence {ItemId}`.
3. Verify zip exists: `ls pi/input/pi-evidence/{ItemId}.zip` (direct listing — no glob-only check).
4. If **no attachments** on the issue: note in spec *Evidence fetch: no Jira attachments*; skip **`pi-evidence-analysis`** unless the human provides a zip.
5. If issue has only **legacy Monday URLs** in description (no Jira files): note *legacy links only* in spec; do not fabricate a zip.

## Fallback

| Case | Action |
|------|--------|
| Legacy `PI-*` with no `PB-*` key | Skip; use existing zip if human placed one |
| `jira/.env` missing / API fail | Note skip reason; ask human for zip path |
| Zip already exists | Fetch skips unless `--force` |

## Relationship to other PI skills

- Runs **before** **`pi-evidence-analysis`** — fetch alone is **not** complete; the next skill must open files and write `pi/evidence-analysis/{KEY}.md`.
- **`pi-intake-impact-fix-spec`** and **`pi-daily-deep-dive`** must run analysis after this step whenever a zip exists (content-level findings, not inventory).
- Implementation: `jira/scripts/jira_automation/fetch_evidence.py`
