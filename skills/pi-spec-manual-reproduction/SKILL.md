---
name: pi-spec-manual-reproduction
description: >-
  Enriches the existing ## Reproduction / symptoms block in pi/specs/{ItemId}.md
  with self-contained steps (Preconditions, Steps, Symptom check, optional
  Traceability) so a human can reproduce without opening pi/user_manual/. Does
  not add a separate manual-reproduction heading. Uses user_manual only while
  drafting. Edits pi/ only; targets pi/specs/PI-*.md at repo root (no dated
  spec subfolders).
---

# PI spec — self-contained manual reproduction

## Location in repo

Stored under `pi/skills/pi-spec-manual-reproduction/`. For Cursor Agent Skill discovery, symlink or copy to `.cursor/skills/pi-spec-manual-reproduction` at the workspace root (parent of `pi/`).

## Goal (non-negotiable)

After this skill runs, **`pi/specs/{ItemId}.md`** must contain reproduction instructions that a reader can follow **using only that file** (plus normal product login and the **HC UAT** or environment URL already in the spec). They must **not** need to search or read `pi/user_manual/` to execute the steps.

- **`pi/user_manual/`** is for the **agent** to draft accurate menu paths, screen names, labels, and order of operations.
- The **spec** must **inline** that information inside **`## Reproduction / symptoms`** only — see **Canonical structure** below.

## Spec file targets (mandatory)

- **Only** `pi/specs/{ItemId}.md` where `{ItemId}` matches the PI (e.g. `PI-0878`).
- **Do not** write or assume dated or duplicate spec trees (for example `pi/specs/YYYY-MM-DD/`). If such folders appear locally, ignore them; canonical specs live beside `pi/specs/pi.csv`.

## Before you start (mandatory)

Read **`pi/docs/jira-pi-board-status.md`** if documenting workflow position in reproduction (use board **column** labels when known).

### Path discipline

- Do **not** use `@PI`, `@pi`, or alias-style path shorthand in the spec body for execution steps.
- Do **not** use or refer to `@old_pi`.
- Use direct paths when citing evidence **outside** the executable subsections (e.g. optional traceability footnote): `pi/user_manual/<file>.md`.

### No placeholder steps (mandatory)

- Preconditions: link to **HC UAT** when the spec’s **Client environment URL** lists it; **do not** write "if present" for URLs or attachments—either the spec has the link or record **Unknown** under **Unknown / confirm with reporter**.

### PI special cases

Read `pi/docs/pi-special-cases.md`. If the PI is a data correction, client-specific data issue, or similar, state preconditions clearly (e.g. “requires account/entity X as described in bug narrative”) and avoid implying a generic product defect when the case doc says otherwise.

### User manual (drafting only)

1. Read or skim **`pi/user_manual/README.md`** for theme index and conventions (slugged names, `_1` duplicates — prefer the guide that matches the PI flow; note conflicts in **Open questions** if both matter).
2. Discover guides: `Module`, **Name**, **Bug Description**, and synonyms — e.g. `rg -l "keyword" pi/user_manual` from workspace root.
3. Extract **menu paths, screen titles, field labels, and sequence** from the chosen guide(s). **Paraphrase into the spec**; do not tell the reader “see user manual section X” as a substitute for steps.

**Limits:** Images may reference missing `media/`; rely on written steps in guides. Filename typos in the index match on-disk names.

## Where to edit (mandatory)

- **Only** modify **`## Reproduction / symptoms`**. Do **not** add **`## Manual reproduction (self-contained)`** or any other top-level heading for the walkthrough.
- If a legacy spec still has **`## Manual reproduction (self-contained)`**, **merge** that content into **`## Reproduction / symptoms`** (see structure below), then **remove** the obsolete heading and its duplicate narrative so the walkthrough exists in **one** place.
- **Do not** move **`## Reproduction / symptoms`** to the end of the file; keep the spec’s existing section order (typically **`## Reproduction / symptoms`** early — e.g. immediately after **`## Metadata`** — per team convention).

## Canonical structure under `## Reproduction / symptoms`

Use this structure (**`###` headings exact** for consistency across PIs):

1. **Opening narrative (optional, recommended)** — One or more short paragraphs: raw symptom / bug summary from the PI. May duplicate **`## Summary`** lightly if helpful for readers who only scroll to reproduction.

2. **`### Preconditions`** — Environment (link to **HC UAT** from **Client environment URL** when that section lists a URL), role/permission assumptions if known, entity/account/security/date or file names **only when stated in the PI or unavoidable**; mark gaps as bullets under **Unknown / confirm with reporter**.

3. **`### Steps`** — **Numbered list**. Each step is one concrete user-visible action (e.g. “Open **Reports** → **Report Book** → …”) using **bold** for labels that match the product UI. Include filters, tabs, save/post actions needed to reach the failing state. Order must be executable by someone who knows the product but has **not** read the user manual.

4. **`### Symptom check`** — What to observe (expected vs actual) tied to the PI narrative — short and specific.

5. **`### Traceability (optional)`** — One short line or bullet list: which `pi/user_manual/*.md` files were used to draft steps. **Explicit:** *“Not required to reproduce; for maintainers only.”*

If **`### Symptom check`** would fully duplicate the opening narrative, you may shorten the opening paragraph and keep the detail under **Symptom check**.

## Quality bar

- **Completeness:** From login (or entry into the right module) through the last action before the defect, steps are continuous; no “locate the relevant screen” without saying how.
- **No manual hunt:** Do not use “refer to user manual”, “search guides for …”, or “follow standard process” without spelling out that process in numbered steps.
- **Honesty:** If guides conflict, coverage is thin, or the PI needs client-specific data not in the spec, say so under **Preconditions** / **Open questions** — still provide the best partial path.
- **Scope:** Only edit **`pi/specs/{ItemId}.md`** (and optionally append a line to **`pi/docs/process-log.md`** if your team logs skill runs). Do **not** change application code or `pi/test-plans/` in this skill unless the user explicitly asks.

## Workflow

1. Open **`pi/specs/{ItemId}.md`** for the PI(s) the user named (or every spec in `pi/specs/` if they asked for a batch — **only** `PI-*.md` files directly under `pi/specs/`).
2. Locate **`## Reproduction / symptoms`**. If it is missing, **create** it in the correct position per team convention (after **`## Metadata`**, before **`## Client environment URL`** or as your template requires) — still **no** separate `## Manual reproduction` heading.
3. Read metadata, **Client environment URL**, **Summary**, and existing text under **Reproduction / symptoms**.
4. Select and read relevant **`pi/user_manual/`** guides; extract navigation.
5. **Replace or expand** only the **Reproduction / symptoms** block to match **Canonical structure** above (preserve any good existing narrative; add or refresh **Preconditions**, **Steps**, **Symptom check**, **Traceability**).
6. If **`## Open questions`** exists, add bullets only when preconditions or navigation are uncertain.

## Relationship to other PI skills

- **`pi-intake-impact-fix-spec`** produces the initial spec; this skill **refines** reproduction usability inside **`## Reproduction / symptoms`** without replacing root-cause or fix sections.
- **`pi-test-plan`** targets `pi/test-plans/`; this skill targets **`pi/specs/`** only.
