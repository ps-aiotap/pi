#!/usr/bin/env bash
# Weekday hourly PI ops: refresh clones once, then dispatch assign-engineering-queue,
# fix-loop, and hour-matched analysis skills.
# Intake & deep analysis run only when not already completed (artifact/state check).
set -euo pipefail

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/var/www/sourcecode}"
CRON_ROOT="${WORKSPACE_ROOT}/cron"
MATRIX="${CRON_ROOT}/config/hourly-skill-matrix.json"
STATE_FILE="${CRON_ROOT}/state/pi-hourly-ops.json"
DONE_CHECK="${CRON_ROOT}/scripts/skill-already-done.py"
LOG_FILE="${CRON_ROOT}/logs/pi-hourly-ops.log"
IST_FULL="$(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S %Z')"
IST_DATE="$(TZ=Asia/Kolkata date '+%Y-%m-%d')"
IST_HOUR="$(TZ=Asia/Kolkata date '+%H')"
# Allow override for manual backfill: HOUR_OVERRIDE=10 ./cron/runners/pi-hourly-ops.sh
HOUR="${HOUR_OVERRIDE:-$IST_HOUR}"

mkdir -p "${CRON_ROOT}/logs" "${CRON_ROOT}/state/prompts" "${WORKSPACE_ROOT}/pi/ops/drafts"

log() { echo "[${IST_FULL}] $*" | tee -a "$LOG_FILE"; }

log "=== pi-hourly-ops start (mode=${MODE:-cron} hour=${HOUR} IST) ==="

if [[ ! -f "$MATRIX" ]]; then
  log "ABORT: missing skill matrix $MATRIX"
  exit 1
fi

# 1. Refresh clones once for this hour
if [[ "${SKIP_REFRESH:-0}" != "1" ]]; then
  if ! "${CRON_ROOT}/scripts/refresh-app-clones.sh" >>"$LOG_FILE" 2>&1; then
    log "ABORT: clone refresh failed"
    exit 1
  fi
else
  log "SKIP_REFRESH=1 — using existing clones"
fi

# 2. Resolve skills — skip intake/deep-analysis when already done
SKILLS=()
while IFS= read -r line; do
  if [[ "$line" == SKIP* ]]; then
    log "$line"
  elif [[ -n "$line" ]]; then
    SKILLS+=("$line")
  fi
done < <(WORKSPACE_ROOT="$WORKSPACE_ROOT" python3 - <<'PY' "$MATRIX" "$HOUR" "$STATE_FILE" "$IST_DATE" "$DONE_CHECK" "$WORKSPACE_ROOT"
import json, os, subprocess, sys

matrix_path, hour, state_path, ist_date, done_check, workspace = sys.argv[1:7]
os.environ["WORKSPACE_ROOT"] = workspace
with open(matrix_path) as f:
    m = json.load(f)
skills = list(m.get("hours", {}).get(hour, []))
meta = m.get("skills", {})
state = {"fired": {}}
if os.path.isfile(state_path):
    with open(state_path) as f:
        state = json.load(f)
fired_today = state.get("fired", {}).get(ist_date, [])
out = []
for sid in skills:
    smeta = meta.get(sid, {})
    if smeta.get("skip_if_done", smeta.get("once_per_day", False)):
        proc = subprocess.run(
            [sys.executable, done_check, sid, ist_date],
            capture_output=True,
            text=True,
            check=False,
        )
        reason = (proc.stdout or "").strip() or "already done"
        if proc.returncode == 0:
            print(f"SKIP {sid}: {reason}")
            continue
    if smeta.get("once_per_day") and sid in fired_today:
        print(f"SKIP {sid}: already fired in hourly-ops state today")
        continue
    out.append(sid)
for sid in out:
    print(sid)
PY
)

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  log "IDLE: no skills for hour ${HOUR} (all skipped as already done, or none scheduled) ${IST_DATE}"
  python3 - <<'PY' "$STATE_FILE" "$IST_FULL"
import json, os, sys
path, ist = sys.argv[1], sys.argv[2]
state = {"fired": {}}
if os.path.isfile(path):
    with open(path) as f:
        state = json.load(f)
state["last_run_ist"] = ist
with open(path, "w") as f:
    json.dump(state, f, indent=2)
    f.write("\n")
PY
  log "=== pi-hourly-ops end ==="
  exit 0
fi

log "Dispatching skills: ${SKILLS[*]}"

FIRED=()
PROMPTS=()

for sid in "${SKILLS[@]}"; do
  case "$sid" in
    pi-sdlc-fix-loop)
      if SKIP_REFRESH=1 "${CRON_ROOT}/runners/pi-sdlc-fix-loop.sh" >>"$LOG_FILE" 2>&1; then
        log "OK: pi-sdlc-fix-loop"
        FIRED+=("$sid")
      else
        rc=$?
        log "WARN: pi-sdlc-fix-loop exited ${rc}"
        FIRED+=("$sid")
      fi
      ;;
    *)
      if PROMPT_PATH="$("${CRON_ROOT}/scripts/build-skill-prompt.sh" "$sid" "$IST_DATE")"; then
        log "OK: ${sid} → ${PROMPT_PATH}"
        FIRED+=("$sid")
        PROMPTS+=("$PROMPT_PATH")
      else
        log "FAIL: prompt build for ${sid}"
      fi
      ;;
  esac
done

# 3. Update hourly-ops state
python3 - <<'PY' "$STATE_FILE" "$IST_FULL" "$IST_DATE" "${FIRED[@]}"
import json, os, sys
path, ist, date = sys.argv[1], sys.argv[2], sys.argv[3]
fired = sys.argv[4:]
state = {"fired": {}, "last_prompts": []}
if os.path.isfile(path):
    with open(path) as f:
        state = json.load(f)
state["last_run_ist"] = ist
state["last_hour"] = date
day = state.setdefault("fired", {}).setdefault(date, [])
for sid in fired:
    if sid not in day:
        day.append(sid)
dates = sorted(state["fired"].keys())
for d in dates[:-14]:
    del state["fired"][d]
with open(path, "w") as f:
    json.dump(state, f, indent=2)
    f.write("\n")
PY

INDEX="${CRON_ROOT}/state/prompts/hourly-ops-${IST_DATE}-${HOUR}.md"
{
  echo "# Hourly PI ops — ${IST_DATE} ${HOUR}:00 IST"
  echo
  echo "**Mode:** ${MODE:-cron}"
  echo "**Skills fired:** ${FIRED[*]:-none}"
  echo
  if [[ ${#PROMPTS[@]} -gt 0 ]]; then
    echo "## Agent prompts (open in Cursor Agent)"
    for p in "${PROMPTS[@]}"; do
      echo "- \`$p\`"
    done
    echo
  fi
  echo "## Assign engineering queue"
  echo "- Skill: \`@pi/skills/pi-assign-engineering-queue/SKILL.md\`"
  echo "- CLI: \`python -m scripts.jira_automation assign-engineering-queue\` (In Review → assign → In Progress)"
  echo
  echo "## Fix loop"
  echo "- See \`cron/state/prompts/\` for \`PB-*-agent-prompt.md\` if a PI was selected"
  echo "- Skill: \`@pi/skills/pi-sdlc-fix-loop/SKILL.md\`"
  echo "- Per-PI intake/deep analysis: skip when \`pi/specs/{KEY}.md\` (and test-plan) already exist"
} > "$INDEX"

log "Index: $INDEX"
log "Next: open Cursor Agent and run prompts listed in $INDEX"
log "=== pi-hourly-ops end ==="
