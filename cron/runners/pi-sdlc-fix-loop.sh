#!/usr/bin/env bash
# Hourly weekday PI SDLC fix loop — preflight, queue, agent prompt emission.
set -euo pipefail

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/var/www/sourcecode}"
CRON_ROOT="${WORKSPACE_ROOT}/cron"
STATE_FILE="${CRON_ROOT}/state/pi-sdlc-fix-loop.json"
LOG_FILE="${CRON_ROOT}/logs/pi-sdlc-fix-loop.log"
IST="$(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S %Z')"

mkdir -p "${CRON_ROOT}/logs" "${CRON_ROOT}/state/prompts" "${WORKSPACE_ROOT}/pi/ops/drafts"

log() { echo "[${IST}] $*" | tee -a "$LOG_FILE"; }

log "=== pi-sdlc-fix-loop start (mode=${MODE:-cron}) ==="

# 1. Refresh clones (skip when called from pi-hourly-ops — already refreshed)
if [[ "${SKIP_REFRESH:-0}" == "1" ]]; then
  log "SKIP_REFRESH=1 — clones already refreshed by hourly ops"
elif ! "${CRON_ROOT}/scripts/refresh-app-clones.sh" >>"$LOG_FILE" 2>&1; then
  log "ABORT: clone refresh failed"
  exit 1
fi

# 2. Ensure state file
if [[ ! -f "$STATE_FILE" ]]; then
  cp "${CRON_ROOT}/state/pi-sdlc-fix-loop.json.example" "$STATE_FILE" 2>/dev/null || \
  echo '{"last_run_ist":null,"current_key":null,"queue":[],"entries":{}}' > "$STATE_FILE"
fi

# 3. Pick next key: CLI arg > state.current_key > first queue item not skipped
NEXT_KEY="${PI_KEY:-}"
if [[ -z "$NEXT_KEY" ]]; then
  NEXT_KEY="$(python3 - <<'PY' "$STATE_FILE"
import json, sys
path = sys.argv[1]
with open(path) as f:
    s = json.load(f)
skip = {"in_flight", "awaiting_human_pr", "awaiting_audit", "done", "blocked", "trashed"}
if s.get("current_key"):
    k = s["current_key"]
    st = s.get("entries", {}).get(k, {}).get("status")
    if st not in skip:
        print(k)
        raise SystemExit
for k in s.get("queue") or []:
    st = s.get("entries", {}).get(k, {}).get("status")
    if st not in skip:
        print(k)
        break
PY
)"
fi

if [[ -z "$NEXT_KEY" ]]; then
  log "IDLE: no eligible PI in queue. Update ${STATE_FILE} queue via JQL."
  python3 - <<'PY' "$STATE_FILE" "$IST"
import json, sys
path, ist = sys.argv[1], sys.argv[2]
with open(path) as f:
    s = json.load(f)
s["last_run_ist"] = ist
with open(path, "w") as f:
    json.dump(s, f, indent=2)
PY
  exit 0
fi

log "Selected PI: $NEXT_KEY"

# 4. Mark in_flight
python3 - <<'PY' "$STATE_FILE" "$NEXT_KEY" "$IST"
import json, sys
path, key, ist = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as f:
    s = json.load(f)
s["last_run_ist"] = ist
s["current_key"] = key
ent = s.setdefault("entries", {}).setdefault(key, {})
ent["status"] = "in_flight"
ent["updated_ist"] = ist
with open(path, "w") as f:
    json.dump(s, f, indent=2)
PY

# 5. Build agent prompt for Cursor
PROMPT_PATH="$("${CRON_ROOT}/scripts/build-agent-prompt.sh" "$NEXT_KEY")"
log "Agent prompt written: $PROMPT_PATH"
log "Next: open Cursor Agent and run prompt from $PROMPT_PATH"
log "Skill: @pi/skills/pi-sdlc-fix-loop/SKILL.md"

log "=== pi-sdlc-fix-loop end ==="
