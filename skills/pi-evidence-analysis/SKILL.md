---
name: pi-evidence-analysis
description: >-
  Analyzes PI evidence from pi/input/pi-evidence/<KEY>.zip (built by pi-fetch-evidence
  from Jira attachments, or legacy manual zip). Must open images/video frames and
  inspect CSV/Excel values — no inventory-only boilerplate. Writes
  pi/evidence-analysis/<KEY>.md and folds findings into the PI spec when intake runs.
  Use when analyzing PI screenshots, videos, or attachments, and as a mandatory step
  before pi-intake-impact-fix-spec / pi-daily-deep-dive when a zip exists.
---

# PI Evidence Analysis (Zip-first)

## Purpose

Produce **content-level**, evidence-driven findings for a PI from one archive — not a file inventory.

- **Preferred source:** Jira attachments on **`PB-*`** — fetched by **`pi-fetch-evidence`** (no CSV/export).
- Input contract: `pi/input/pi-evidence/<ItemId>.zip` (`PB-*` or legacy `PI-*`)
- Zip contents: flat files only (no nested folders)
- No filename convention is required
- Deterministic processing: preserve archive order when available; otherwise use a stable lexicographic fallback
- **Mandatory output:** `pi/evidence-analysis/<ItemId>.md` (overwrite on re-run)

## Path discipline

- Use direct repository paths only.
- Keep all outputs inside `pi/`.
- Do not modify application code or tests for this skill.

## Jira board status (when linking to workflow)

If findings reference ticket state, use **`pi/docs/jira-pi-board-status.md`**: board **column** = status; **BA = Change Request** (not “Done” in prose).

### No placeholder paths (mandatory)

- Before citing `pi/input/pi-evidence/<PI-ID>.zip` in **`pi/evidence-analysis/`**, specs, or chat, **verify** that path exists in the workspace. If missing, say only that the archive was not found — do not emit "if present" or a backticked path to a non-existent file.
- Existence checks must use a direct filesystem listing/read (for example, `ls` or equivalent), not index-only glob/search results.

## Intake contract

1. Resolve `{ItemId}` from user prompt or target spec (`PB-2888` or legacy `PI-3247`).
2. **Fetch (PB keys):** If `{ItemId}` matches `PB-*` and zip is missing or stale, run **`pi/skills/pi-fetch-evidence/SKILL.md`** first:
   `cd jira && python -m scripts.jira_automation fetch-evidence {ItemId}`
3. Locate archive at `pi/input/pi-evidence/<ItemId>.zip` (verify with direct `ls`, not glob-only).
4. If archive is still missing: for `PB-*`, report *no Jira attachments* or fetch error and **stop** (write nothing under `pi/evidence-analysis/` unless the human provides a zip); for legacy `PI-*`, ask human for zip path. Do not invent paths.
5. Extract archive to `pi/input/pi-evidence/<ItemId>-extracted/`.
6. Reject or flag nested directories (zip must be flat by convention).
7. **Analyze every file** using the type rules and **quality bar** below.
8. **Write** `pi/evidence-analysis/<ItemId>.md` using the output template.
9. If `pi/specs/<ItemId>.md` already exists (or intake is writing it in the same run), fold findings per **Spec fold-in**.

## Quality bar (mandatory — reject inventory-only work)

The analysis is **invalid** if any of these are true:

- Per-file “findings” only say the file exists / is present / can support verification.
- Images are listed but **not opened** with the Read/image tool (or equivalent visual inspection).
- No **concrete tokens** extracted from evidence (UI labels, amounts, dates, ISINs, account names, error strings, column headers, row values).
- Synthesis is only a type count (`images N, csv M`) with no claim about what the attachments show relative to the PI.
- Confidence is `high` without citing at least one concrete on-screen or tabular fact.

### Reject phrases (unless immediately followed by a concrete observation)

Do not use fillers such as:

- “Image evidence file present for visual verification of UI/data state”
- “Supports confirming on-screen symptom states”
- “Workbook contents can capture source transaction/report data”
- “Sheet-level conversion enables deterministic, row-wise evidence checks”

Replace with **what is actually visible or in the cells**.

### How to inspect (mandatory technique)

| Type | Required action |
|------|-----------------|
| **Images** | Open each image with the Read tool (vision). Transcribe readable UI text, grid headers, highlighted rows, error toasts, tenant/entity names, dates, amounts. Note crop/blur limits honestly. |
| **Videos** | Extract or scrub key frames (start / symptom moment / end). Describe transitions; no audio claims. If frame extraction is unavailable, state that and summarize from any stills; do not invent timeline detail. |
| **CSV** | Read headers + sample and anomaly rows; quote values that match or contradict the PI narrative. |
| **Excel** | Convert sheets to CSV in the extracted folder, then analyze like CSV. Call out sheet names and which sheet carries the failing case. |
| **PDF / other Office** | Extract readable text/tables where tools allow; otherwise note format + what could not be parsed and what a human must open. |
| **Logs / JSON / txt** | Quote the failing line/field; do not paraphrase away error codes. |

Always load the PI **summary + description** (from Jira or `pi/specs/{ItemId}.md` if present) **before** analyzing so findings are tied to claimed symptoms.

## Evidence type handling

Process extracted files in deterministic order:

1. Archive entry order from the zip index.
2. If extraction/index order is unavailable or ambiguous, use lexicographic filename order.

Do not require naming patterns such as `01-...`; handle files exactly as provided.

- **Images** (`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`)
  - Inspect visible UI/data states; extract on-screen text.
  - Capture anomalies tied to PI symptoms (wrong value, missing row, duplicate, wrong status).

- **Videos (silent)** (`.mp4`, `.webm`, `.mov`)
  - Analyze visually only (no audio assumptions).
  - Summarize timeline checkpoints (start / symptom / end) with what changed.

- **CSV** (`.csv`)
  - Inspect headers, row-level anomalies, and values relevant to PI claims.
  - Cross-check against PI narrative.

- **Excel** (`.xlsx`)
  - If exactly one sheet, convert to CSV and analyze that CSV.
  - If multiple sheets, export each sheet to sheet-suffixed CSV files and analyze all.
  - Keep converted CSVs in the same extracted PI evidence folder.
  - Prefer calling out **expected vs actual** columns when the sheet is a repro matrix.

## Output format

Write **`pi/evidence-analysis/<ItemId>.md`** with this structure:

```markdown
# Evidence analysis: {ItemId}

## Evidence inventory
- PI ID: …
- Zip path: `pi/input/pi-evidence/{ItemId}.zip` (verified on disk)
- PI claim (one line): …
- Ordered file list analyzed: …

## Per-file findings

### `{filename}`
- **Type:** image | video | csv | xlsx-sheet | other
- **Observed:** concrete UI/table/log facts (quotes, numbers, labels)
- **Relevance:** how this supports, weakens, or is orthogonal to the PI claim
- **Extracted tokens:** bullet list of names/amounts/dates/errors worth searching in code

## Cross-evidence synthesis
- **Consistent signals:** …
- **Contradictions / gaps:** …
- **Strongest symptom anchor:** the single best fact to reproduce or disprove

## Hypothesis implications
- Facts that raise/lower confidence in likely failure boundaries (API / DB / calc / render / config / missing feature)
- What the attachments **do not** prove

## Conclusion
- Confidence: high | medium | low
- Open questions: …
- Next checks: …
```

## Spec fold-in (mandatory when intake or deep-dive runs in the same session)

When updating or writing `pi/specs/{ItemId}.md`:

1. Add or refresh **`## Evidence analysis`**:
   - Link: `pi/evidence-analysis/{ItemId}.md`
   - 3–7 bullet **symptom anchors** copied from Observed / Strongest symptom anchor (not a bare link).
2. Add **`## Evidence Files`**: ordered filenames **actually present** in the extracted archive.
3. In **competing hypotheses**, cite attachment facts (filename + token) wherever a hypothesis depends on what the reporter showed.

Do not add stub lines for zips or files that were not analyzed.

## Relationship to other PI skills

- **`pi-fetch-evidence`** — always before this skill for `PB-*`.
- **`pi-intake-impact-fix-spec`** — must run this skill when a zip exists; specs are invalid without content-level findings folded in.
- **`pi-daily-deep-dive`** / **`pi-cr-candidate`** — must read (or produce) `pi/evidence-analysis/{ItemId}.md` before hypotheses / CR verdict when attachments exist.
- Catalog order: `pi/docs/pi-skills-catalog.md` / `pi/skil_run.txt` step 2.
