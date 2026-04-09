# How to validate the PI folder setup

Use this after changes to `pi/` or to confirm a clone is correct.

## 1. Folder layout

From the **workspace root** (the directory that **contains** `pi/` as a subdirectory, often alongside `controller/`, `dashboard/`, etc.), these paths should exist:

- `pi/input/` and `pi/input/processed/`
- `pi/input/urls/` (client URL CSVs for intake)
- `pi/input/team/` (squad roster / leaders for intake)
- `pi/specs/`
- `pi/impact/`
- `pi/test-plans/`
- `pi/skills/pi-intake-impact-fix-spec/`
- `pi/skills/pi-test-plan/`
- `pi/skills/pi-code-fix/`
- `pi/skills/pi-test-implement/`
- `pi/docs/`

**Quick check (terminal):**

```bash
cd /path/to/current
test -f pi/specs/pi.csv && test -f pi/specs/README.md && \
test -d pi/input/processed && test -d pi/skills/pi-intake-impact-fix-spec && \
echo "OK: core paths present"
```

### Workspace vs `pi/` vs application clones

- The **workspace root** may have **no** `.git`; it is simply the folder that contains **`pi/`** and the application trees you search during PI work.
- **`pi/`** is its **own** repository (typically **GitHub**) for specs, inputs, skills, and user-manual content. PI skills **exclude** `pi/` from the mandatory “refresh all application repos” step unless you explicitly want to update the PI repo.
- **Application source** is usually **multiple Bitbucket clones** (e.g. `controller/`, `dashboard/`). Before running intake, test-plan, code-fix, or test-implement skills, **fetch and integrate each clone** under the workspace root **except** paths under `pi/` — see **Before you start** / **Preconditions** in `pi/skills/*/SKILL.md`.

## 2. Column reference file

- **File:** `pi/specs/pi.csv`
- **Expect:** exactly **one data line** (the header row only—no PI rows in this file).
- **Expect:** no `pi/ref/` directory and no references to `pi/ref/pi.csv` in skills.

**Quick check:**

```bash
test ! -e pi/ref && echo "OK: pi/ref removed"
grep -q 'pi/specs/pi.csv' pi/skills/pi-intake-impact-fix-spec/SKILL.md && echo "OK: intake skill points at specs/pi.csv"
! grep -q 'pi/ref' pi/skills/pi-intake-impact-fix-spec/SKILL.md && echo "OK: no pi/ref in intake skill"
```

## 3. Skill files

Each skill directory must contain `SKILL.md` with YAML frontmatter (`name`, `description`).

```bash
for d in pi-intake-impact-fix-spec pi-test-plan pi-code-fix pi-test-implement; do
  test -f "pi/skills/$d/SKILL.md" || echo "MISSING: pi/skills/$d/SKILL.md"
done
```

## 4. Documentation set

| File | Purpose |
|------|---------|
| `pi/docs/pi-folder-setup.md` | Layout and skills overview |
| `pi/docs/validate-pi-setup.md` | This checklist |
| `pi/docs/process-log.md` | Optional run log (may be empty except title) |
| `pi/specs/README.md` | Explains `pi.csv` + `{ItemId}.md` in one folder |

## 5. End-to-end workflow smoke test (manual)

This validates behavior, not only files on disk.

1. Copy a **small** PI CSV (with the same columns as `pi/specs/pi.csv`) into `pi/input/` (e.g. `pi/input/smoke.csv` with one data row).
2. In Cursor, open the intake skill (e.g. `@pi/skills/pi-intake-impact-fix-spec/SKILL.md` or symlinked Agent Skill) and ask it to process that file for the single row.
3. **Expect:**  
   - New or updated `pi/specs/<ItemId>.md` (and optionally `pi/impact/<ItemId>.md`), including **Client environment URL** (lookup under `pi/input/urls/`) and **Suggested assignment** (team + leader from `pi/input/team/`).  
   - No edits outside `pi/` (spot-check `git status` in the relevant application clone(s) or your diff tool).
4. Confirm with the agent that the run is complete, then **move** `pi/input/smoke.csv` → `pi/input/processed/smoke.csv` (or let the agent do it per skill).
5. Optionally confirm a line was appended to `pi/docs/process-log.md`.

## 6. Cursor Agent Skill discovery (optional)

Skills under `pi/skills/` are **not** auto-loaded until they live under `.cursor/skills/`.

- **Validate symlink (example):**

```bash
ls -la .cursor/skills/pi-intake-impact-fix-spec
# should resolve to pi/skills/pi-intake-impact-fix-spec or a copy
```

- **Expect:** Starting a chat that matches the skill `description` (or @-mentioning the skill) pulls in the same instructions as `pi/skills/.../SKILL.md`.

## 7. Pass / fail

| Check | Pass |
|--------|------|
| All paths in §1 exist | Yes |
| `pi/specs/pi.csv` is header-only; `pi/ref` absent | Yes |
| Intake skill references `pi/specs/pi.csv` only | Yes |
| Four `SKILL.md` files present | Yes |
| §5 smoke test produces spec under `pi/specs/` only | Yes (when you run it) |
| §8 no lazy **TBD** / draft callouts on approved test plans | Yes (when batch output was finalized) |

If any check fails, fix the missing path or update the skill text, then re-run §1–§4.

## 8. Test plan quality (after `generate_from_book2.py` or batch intake)

Batch-generated files under `pi/test-plans/` must be **finished** with the **pi-test-plan** skill before QA sign-off.

**Expectations:**

- No literal **`TBD`** in the **Automation mapping** section (replace with repo search results or explicit “none, searched …”).
- **Regression** rows reference concrete anchors (files, routes, screens), not only “same module”.
- The **Draft (batch-generated)** callout (if present) is **removed** after the plan is complete.

**Quick grep (should return no matches on finished plans):**

```bash
cd /path/to/current
# Fails if any test plan still has the old automation placeholder:
grep -l 'PHPUnit/Jest/Cypress layout:.*TBD' pi/test-plans/*.md 2>/dev/null || true
grep -l '^\*\*TBD\*\*' pi/test-plans/*.md 2>/dev/null || true
```

Treat matches as **draft debt** until `pi-test-plan` is applied (or the file is hand-edited to the same standard).
