# PI folder setup (what was done)

## Purpose

Support a **man-in-the-loop** pipeline: read PI rows from CSV, analyze the repo, write fix and test **documentation** under `pi/` only; optional later phases for code and test implementation.

## Layout

| Path | Role |
|------|------|
| `pi/input/` | Pending PI CSV exports (PI-related files only). |
| `pi/input/urls/` | Client tenant → base URL CSVs (`client_name`, `url`) for intake lookups (e.g. US / India lists). |
| `pi/input/team/` | Squad rosters and leaders (e.g. `TeamMembers.txt`) for suggested PI assignment. |
| `pi/input/processed/` | Same CSV moved here after a full pass is confirmed done. |
| `pi/specs/` | **`pi.csv`** = column reference (headers only). **`{ItemId}.md`** = fix specs. |
| `pi/impact/` | Optional separate impact notes `{ItemId}.md`. |
| `pi/test-plans/` | Test plan docs `{ItemId}.md`. **`generate_from_book2.py` writes drafts only** — always run **pi-test-plan** afterward to fill regression/automation and remove the draft callout. |
| `pi/skills/` | Cursor-oriented skill playbooks (symlink to `.cursor/skills/` if desired). |
| `pi/docs/` | Setup (`pi-folder-setup.md`), **validation** (`validate-pi-setup.md`), optional **`process-log.md`**. |

## Skills (`pi/skills/`)

- **pi-intake-impact-fix-spec** — CSV → client URL lookup (`pi/input/urls/`), team/leader suggestion (`pi/input/team/`), repo search → `pi/specs/{ItemId}.md` (+ optional `pi/impact/`); no app code changes.
- **pi-test-plan** — From approved spec → `pi/test-plans/{ItemId}.md`.
- **pi-code-fix** — Stub for future implementation phase.
- **pi-test-implement** — Stub for future automated tests phase.

## Changes log

- **Ref merged into specs:** Column reference moved from `pi/ref/pi.csv` to **`pi/specs/pi.csv`** so reference and fix specs share one folder.
- **Docs:** `pi/docs/pi-folder-setup.md` (this file), `pi/docs/validate-pi-setup.md` (how to verify the setup), `pi/docs/process-log.md` (optional run log), and `pi/specs/README.md` describe layout and conventions.
