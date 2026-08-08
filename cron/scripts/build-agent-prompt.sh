#!/usr/bin/env bash
# Emit Cursor agent prompt for the next open PI in the fix loop.
# Skips re-running intake/deep analysis when artifacts already exist for the key.
set -euo pipefail

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/var/www/sourcecode}"
STATE_FILE="${WORKSPACE_ROOT}/cron/state/pi-sdlc-fix-loop.json"
PROMPT_DIR="${WORKSPACE_ROOT}/cron/state/prompts"
DONE_CHECK="${WORKSPACE_ROOT}/cron/scripts/skill-already-done.py"
KEY="${1:-}"

mkdir -p "$PROMPT_DIR"

if [[ -z "$KEY" ]]; then
  KEY="$(python3 - <<'PY' "$STATE_FILE"
import json, os, sys
path = sys.argv[1]
state = {"entries": {}}
if os.path.isfile(path):
    with open(path) as f:
        state = json.load(f)
skip = {"in_flight", "awaiting_human_pr", "awaiting_audit", "done", "blocked", "trashed"}
queue = state.get("queue") or []
for k in queue:
    ent = state.get("entries", {}).get(k, {})
    if ent.get("status") not in skip:
        print(k)
        break
else:
    print("")
PY
)"
fi

if [[ -z "$KEY" ]]; then
  echo "No PI key queued. Populate cron/state/pi-sdlc-fix-loop.json queue via JQL or pass PB-xxxx argument."
  exit 1
fi

INTAKE_STATUS="run"
INTAKE_REASON="intake artifacts missing — run skills 1–8"
CHECK_OUT="$(mktemp)"
if WORKSPACE_ROOT="$WORKSPACE_ROOT" python3 "$DONE_CHECK" --check-intake "$KEY" >"$CHECK_OUT" 2>/dev/null; then
  INTAKE_STATUS="skip"
  INTAKE_REASON="$(cat "$CHECK_OUT")"
else
  INTAKE_REASON="$(cat "$CHECK_OUT" 2>/dev/null || echo "$INTAKE_REASON")"
fi
rm -f "$CHECK_OUT"

OUT="${PROMPT_DIR}/${KEY}-agent-prompt.md"
cat > "$OUT" <<EOF
# PI SDLC fix loop — agent prompt for ${KEY}

Run in **Agent** mode. Do **not** create PR.

## 0. Preflight
- Confirm \`./cron/scripts/refresh-app-clones.sh\` succeeded (app clones clean on master)
- Read \`pi/docs/jira-pi-board-status.md\`

## 1. Analysis (skills 1–8) — intake & deep analysis
**Status:** \`${INTAKE_STATUS}\`
**Check:** ${INTAKE_REASON}

EOF

if [[ "$INTAKE_STATUS" == "skip" ]]; then
  cat >> "$OUT" <<EOF
**Do not re-run** \`pi-fetch-evidence\`, \`pi-evidence-analysis\`, \`pi-intake-impact-fix-spec\`, or deep-dive for **${KEY}** — already done earlier.
Only refresh \`pi/test-plans/${KEY}.md\` if **Verify the fix** / **Prevention regression tests (future PIs)** sections are missing.

EOF
else
  cat >> "$OUT" <<EOF
Follow \`pi/skil_run.txt\` for **${KEY}** through \`pi-test-plan\`.
Ensure \`pi/test-plans/${KEY}.md\` has:
- **Verify the fix**
- **Prevention regression tests (future PIs)**

EOF
fi

cat >> "$OUT" <<EOF
## 2. Code fix
\`/implementation-agent\` with \`@pi/specs/${KEY}.md\`
Branch: \`bugfix/${KEY}-...\` from latest master.
All product + Playwright edits stay on that bugfix branch only — never leave master dirty.

## 3. Verify Playwright only
\`/test-generation-agent\` — FRAMEWORK: Playwright
Target (on bugfix branch only): \`dashboard/tests/e2e/pi/${KEY}/\`
Header: \`// PI: ${KEY}\`
Run: \`cd dashboard && npx playwright test tests/e2e/pi/${KEY}\`
Do **not** implement prevention list on this branch.
Do **not** write Playwright files on master.

## 4. PM Tasks (board 1144)
Create Task(s) on **PM** linked \`relates to\` **${KEY}** from prevention list.
Skip if open PM prevention Tasks already link to **${KEY}**.

## 5. Stop / handoff gate
- If Playwright **passed**: write \`pi/ops/drafts/fix-handoff-${KEY}.md\` and set state → \`awaiting_human_pr\`
- If Playwright **cannot run** or **failed**: set state → \`blocked\` with reason (do not fake handoff)
- End-of-hour: checkout master on app clones; \`git status --porcelain\` must be empty
EOF

echo "$OUT"
