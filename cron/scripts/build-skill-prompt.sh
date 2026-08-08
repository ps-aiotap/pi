#!/usr/bin/env bash
# Emit a Cursor agent prompt for a named PI skill (deep dive, open analysis, etc.).
set -euo pipefail

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/var/www/sourcecode}"
PROMPT_DIR="${WORKSPACE_ROOT}/cron/state/prompts"
MATRIX="${WORKSPACE_ROOT}/cron/config/hourly-skill-matrix.json"
SKILL_ID="${1:-}"
IST_DATE="${2:-$(TZ=Asia/Kolkata date '+%Y-%m-%d')}"

mkdir -p "$PROMPT_DIR"

if [[ -z "$SKILL_ID" ]]; then
  echo "Usage: $0 <skill-id> [YYYY-MM-DD]" >&2
  exit 1
fi

if [[ "$SKILL_ID" == "pi-sdlc-fix-loop" ]]; then
  echo "Use build-agent-prompt.sh for pi-sdlc-fix-loop" >&2
  exit 1
fi

read -r SKILL_PATH CHAT NOTES < <(python3 - <<'PY' "$MATRIX" "$SKILL_ID"
import json, sys
matrix_path, skill_id = sys.argv[1], sys.argv[2]
with open(matrix_path) as f:
    m = json.load(f)
meta = m.get("skills", {}).get(skill_id)
if not meta:
    print("", "", f"unknown skill {skill_id}")
    raise SystemExit(1)
print(meta.get("skill", ""), meta.get("chat", skill_id), meta.get("notes", "").replace("\n", " "))
PY
)

OUT="${PROMPT_DIR}/${SKILL_ID}-${IST_DATE}-agent-prompt.md"

case "$SKILL_ID" in
  pi-daily-deep-dive)
    cat > "$OUT" <<EOF
# PI skill — ${SKILL_ID} (${IST_DATE} IST)

Run in **Agent** mode. **Never write to Jira** unless a human explicitly asks.

## Skill
Read and follow \`${SKILL_PATH}\`

## Already done?
If \`pi/reports/daily-deep-dive-${IST_DATE}.md\` exists **or** \`pi/ops/daily-deep-dive-state.json\` already has a \`runs\` entry for **${IST_DATE}**, **stop** — do not redo today's deep dive.
Per key: skip any PI that already has a fresh \`pi/deep-dives/{KEY}.md\` from the last 14 days (per skill selection rules).

## Chat
\`\`\`
${CHAT}
\`\`\`

## Do (only if not already done)
1. Confirm app clones are fresh (hourly ops already ran \`refresh-app-clones.sh\`).
2. Select up to **5** IN DEVELOPMENT (\`In Progress\`) PB keys per skill selection rules.
3. For each key: fetch Jira → evidence (when attachments) → deep dive MD → **\`pi-cr-candidate\`**.
4. Write \`pi/deep-dives/{KEY}.md\` and \`pi/reports/daily-deep-dive-${IST_DATE}.md\`.
5. Update \`pi/ops/daily-deep-dive-state.json\`.

## Notes
${NOTES}
EOF
    ;;
  pi-daily-open-analysis)
    cat > "$OUT" <<EOF
# PI skill — ${SKILL_ID} (${IST_DATE} IST)

Run in **Agent** mode.

## Skill
Read and follow \`${SKILL_PATH}\`

## Chat
\`\`\`
${CHAT}
\`\`\`

## Do
1. Ping Jira; produce weekday open-PI snapshot (four board-774 columns).
2. Write \`pi/reports/daily-ops-${IST_DATE}.md\` (no ETA sections; include stale).
3. Pair context with stale-assignee reminder if that prompt also fired this hour.
EOF
    ;;
  pi-detail-elaboration)
    cat > "$OUT" <<EOF
# PI skill — ${SKILL_ID} (${IST_DATE} IST)

Run in **Agent** mode. **Never write to Jira** unless a human asks.

## Skill
Read and follow \`${SKILL_PATH}\`

## Chat
\`\`\`
${CHAT}
\`\`\`

## Do
1. Score open PB board-774 PIs ready / thin / borderline.
2. Coach reporters with paste-ready asks; draft elaborations for thin ones.
3. Write \`pi/reports/pi-detail-elaboration.md\` (and per-key elaborations as the skill requires).
EOF
    ;;
  pi-non-eng-disposition)
    cat > "$OUT" <<EOF
# PI skill — ${SKILL_ID} (${IST_DATE} IST)

Run in **Agent** mode.

## Skill
Read and follow \`${SKILL_PATH}\`

## Chat
\`\`\`
${CHAT}
\`\`\`

## Do
Report PIs dispositioned without engineering; flag Leakage RCA / closer-comment gaps.
Write the dated report under \`pi/reports/\` per the skill.
EOF
    ;;
  pi-stale-assignee-reminder)
    cat > "$OUT" <<EOF
# PI skill — ${SKILL_ID} (${IST_DATE} IST)

Run in **Agent** mode. Follow skill rules for Jira comments (@mention only when skill says so).

## Skill
Read and follow \`${SKILL_PATH}\`

## Chat
\`\`\`
${CHAT}
\`\`\`
EOF
    ;;
  pi-assign-engineering-queue)
    cat > "$OUT" <<EOF
# PI skill — ${SKILL_ID} (${IST_DATE} IST)

Run in **Agent** mode. Runs **before** \`pi-sdlc-fix-loop\` each hour.

## Skill
Read and follow \`${SKILL_PATH}\`

## Chat
\`\`\`
${CHAT}
\`\`\`

## Do
1. \`cd jira && source .venv/bin/activate && python -m scripts.jira_automation ping\`
2. Live assign (hourly fix path — not dry-run unless human asks):
   \`python -m scripts.jira_automation assign-engineering-queue\`
3. Summarize applied / skipped / errors from \`pi/reports/assign-engineering-queue-${IST_DATE}.{md,json}\`.
4. Only touch **In Engineering Queue** (\`In Review\`) PIs missing **both** Developer and Team; move assigned ones to **IN DEVELOPMENT**.

## Notes
${NOTES}
EOF
    ;;
  pi-meeting-brief)
    cat > "$OUT" <<EOF
# PI skill — ${SKILL_ID} (${IST_DATE} IST)

Run in **Agent** mode.

## Skill
Read and follow \`${SKILL_PATH}\`

## Chat
\`\`\`
${CHAT}
\`\`\`

## Do
Write \`pi/reports/meeting-brief-${IST_DATE}.md\` for Critical/High open PIs (manager sync).
Prefer fresh daily-ops / open-analysis if available from the 10:00 IST pack.
EOF
    ;;
  *)
    cat > "$OUT" <<EOF
# PI skill — ${SKILL_ID} (${IST_DATE} IST)

Run in **Agent** mode.

## Skill
Read and follow \`${SKILL_PATH}\`

## Chat
\`\`\`
${CHAT}
\`\`\`

## Notes
${NOTES}
EOF
    ;;
esac

echo "$OUT"
