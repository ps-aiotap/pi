---
name: pi-rca-human-enhancement
description: >-
  Enhances an existing PI RCA in pi/specs using optional BA or human inputs while
  keeping all RCA content in a single spec file. Use only when explicitly asked
  to enrich a specific PI RCA; does not run intake, code-fix, or test workflows.
---

# PI RCA human enhancement (optional, on-demand)

## Purpose

Use this skill only after a base RCA already exists at `pi/specs/{ItemId}.md`.
It enriches RCA quality with business analyst or other human inputs while keeping
everything in one place (the same spec file).

## Jira board status

When RCA text references workflow, align with **`pi/docs/jira-pi-board-status.md`**: **BA = Change Request** (eng complete on PI; PI closes; feature work may be tracked separately)—not Jira status **Done**.

## Non-goals (mandatory)

- Do not replace or remove the existing auto-generated RCA.
- Do not create parallel RCA files for the same PI.
- Do not run code-fix or test implementation steps.
- Do not modify files outside `pi/`.

## Inputs and outputs

| | Path |
|---|---|
| Required read | `pi/specs/{ItemId}.md` |
| Optional read (human input) | `pi/input/human/{ItemId}.md` |
| Optional read (ad hoc user text) | Human notes provided in chat |
| Optional read (evidence index) | `pi/input/human/{ItemId}-evidence.md` |
| Write/update | `pi/specs/{ItemId}.md` only |

If the optional files are missing, continue with chat-provided input. If both file
and chat are missing, under **`## RCA - Human Enhancement (Optional)`** record one
factual line only, e.g. human notes were not supplied (no file at
`pi/input/human/{ItemId}.md` and no notes in chat). Do not use vague placeholders
such as "TBD" or "pending enhancement."

## Path discipline (mandatory)

- Use concrete repository paths only (no alias shorthand).
- Keep all changes in `pi/specs/{ItemId}.md`.
- If referencing attachments, list a stable path or URL exactly as provided.

## One-file RCA contract (mandatory)

Ensure the PI spec has all of these sections (create if absent, update if present):

1. `## RCA - System Generated`
2. `## RCA - Human Enhancement (Optional)`
3. `## RCA - Consolidated Final View`
4. `## Evidence Attachments`
5. `## Change Log (RCA updates)`

### Marking rules

- Prefix machine-origin points with `[AUTO]`.
- Prefix human-origin points with `[HUMAN]`.
- Prefix merged conclusions with `[MERGED]`.

Do not rewrite history. Keep prior content and append dated enhancement entries.

## Human input normalization

Convert free-form human notes into this compact structure:

- Source (BA / QA / PM / Engineer / Other)
- Environment (UAT / PROD / SIT / other)
- Repro status (Reproduced / Not reproduced / Partial)
- Observation summary (2-5 bullets)
- Scope (single position vs multiple positions / entities / date ranges)
- Attachments (video, screenshot, logs, query results)
- Confidence (high/medium/low) based on directness of evidence

## Consolidation rules (mandatory)

When human input is present:

1. Add normalized human snapshot under `RCA - Human Enhancement (Optional)`.
2. Re-rank existing hypotheses in `RCA - Consolidated Final View`.
3. For each hypothesis, state what changed due to human evidence:
   - confidence up/down/same,
   - supporting evidence pointer,
   - fastest next disprover.
4. Keep uncertainty explicit (assumptions and open questions remain visible).

When human input is absent:

- Keep **`## RCA - Human Enhancement (Optional)`** with the single factual absence
  line above; do not invent observations.

## Example human input (PI-0808 style)

If given text such as:

- "Issue replicated on client UAT."
- "Group report shows incorrect interest."
- "Individual entity report shows correct values for the same position."
- "Validated on one position with video; similar on multiple positions."

then record as:

- `[HUMAN] Reproduced on UAT for client tenant.`
- `[HUMAN] Group-scope report undercounts interest vs individual-entity run for same position.`
- `[HUMAN] Evidence includes video for one verified position; analyst reports similar behavior on multiple positions.`

and in consolidated RCA:

- `[MERGED] Prioritize aggregation/dedup hypotheses over raw-calculation hypothesis unless disproved by payload/DB parity checks.`

## Minimal update workflow

1. Read `pi/specs/{ItemId}.md`.
2. Parse optional human input from file and/or chat.
3. Normalize notes and add `[HUMAN]` section content.
4. Update consolidated view with `[MERGED]` hypothesis ranking.
5. Add evidence pointers in `## Evidence Attachments`.
6. Append one entry in `## Change Log (RCA updates)` with date, source, and what changed.

## Quality bar

- Single file remains readable.
- Human notes are structured, not dumped raw.
- Consolidated section clearly explains decision impact of new evidence.
- No contradictions between system and human sections without explicit callout.
