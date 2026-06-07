---
name: pi-evidence-analysis
description: >-
  Analyzes PI evidence from pi/input/pi-evidence/<KEY>.zip (built by pi-fetch-evidence
  from Jira attachments, or legacy manual zip). Supports images, silent videos, CSV,
  and Excel converted to CSV. Use when analyzing PI screenshots, videos, or attachments.
---

# PI Evidence Analysis (Zip-first)

## Purpose

Produce evidence-driven findings for a PI using one evidence archive:

- **Preferred source:** Jira attachments on **`PB-*`** — fetched by **`pi-fetch-evidence`** (no CSV/export).
- Input contract: `pi/input/pi-evidence/<ItemId>.zip` (`PB-*` or legacy `PI-*`)
- Zip contents: flat files only (no nested folders)
- No filename convention is required
- Deterministic processing: preserve archive order when available; otherwise use a stable lexicographic fallback

## Path discipline

- Use direct repository paths only.
- Keep all outputs inside `pi/`.
- Do not modify application code or tests for this skill.

## Jira board status (when linking to workflow)

If findings reference ticket state, use **`pi/docs/jira-pi-board-status.md`**: board **column** = status; **BA = Change Request** (not “Done” in prose).

### No placeholder paths (mandatory)

- Before citing `pi/input/pi-evidence/<PI-ID>.zip` in **`pi/evidence-analysis/`**, specs, or chat, **verify** that path exists in the workspace. If missing, say only that the archive was not found and proceed with steps 3–4 of intake—do not emit "if present" or a backticked path to a non-existent file.
- Existence checks must use a direct filesystem listing/read (for example, `ls` or equivalent), not index-only glob/search results.

## Intake contract

1. Resolve `{ItemId}` from user prompt or target spec (`PB-2888` or legacy `PI-3247`).
2. **Fetch (PB keys):** If `{ItemId}` matches `PB-*` and zip is missing or stale, run **`pi/skills/pi-fetch-evidence/SKILL.md`** first:
   `cd jira && python -m scripts.jira_automation fetch-evidence {ItemId}`
3. Locate archive at `pi/input/pi-evidence/<ItemId>.zip` (verify with direct `ls`, not glob-only).
4. If archive is still missing: for `PB-*`, report *no Jira attachments* or fetch error; for legacy `PI-*`, ask human for zip path. Do not invent paths.
5. Extract archive to `pi/input/pi-evidence/<ItemId>-extracted/`.
6. Reject or flag nested directories (zip must be flat by convention).

## Evidence type handling

Process extracted files in deterministic order:

1. Archive entry order from the zip index.
2. If extraction/index order is unavailable or ambiguous, use lexicographic filename order.

Do not require naming patterns such as `01-...`; handle files exactly as provided.

- **Images** (`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`)
  - Inspect visible UI/data states and extract on-screen text where possible.
  - Capture anomalies tied to PI symptoms.

- **Videos (silent)** (`.mp4`, `.webm`, `.mov`)
  - Analyze visually only (no audio assumptions).
  - Summarize timeline checkpoints (start/mid/end and key transitions).

- **CSV** (`.csv`)
  - Inspect headers, row-level anomalies, and values relevant to PI claims.
  - Cross-check against PI narrative in spec.

- **Excel** (`.xlsx`)
  - If exactly one sheet, convert to CSV and analyze that CSV.
  - If multiple sheets, export each sheet to sheet-suffixed CSV files and analyze all.
  - Keep converted CSVs in the same extracted PI evidence folder.

## Output format

Return findings in this structure:

1. **Evidence inventory**
   - PI ID
   - Zip path
   - Ordered file list analyzed
2. **Per-file findings**
   - File path
   - What was observed
   - Why it matters for the PI
3. **Cross-evidence synthesis**
   - Consistent signals
   - Contradictions / gaps
4. **Conclusion**
   - Confidence level (`high` / `medium` / `low`)
   - Open questions
   - Next checks

## Optional spec traceability

If asked to update the PI spec, add:

- `## Evidence Files`
- Ordered bullet list of evidence filenames or paths **actually present** in the extracted archive (verify on disk).

Do not add stub lines for zips or files that were not analyzed.

## Validation phases

- **Phase 1 (current)**: validate zip intake and currently available evidence (PI-3247 baseline).
- **Phase 2 (later)**: validate silent-video nuances and Excel-to-CSV paths once those artifacts are provided.
