#!/usr/bin/env bash
# Generic cron job launcher for PI automation scripts.
set -euo pipefail

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/var/www/sourcecode}"
CRON_ROOT="${WORKSPACE_ROOT}/cron"
ACTION="${1:-}"
JOB_ID="${2:-}"
MODE="${3:-}"

usage() {
  echo "Usage: $0 run <job-id> [manual|cron]" >&2
  exit 1
}

[[ "$ACTION" == "run" ]] || usage
[[ -n "$JOB_ID" ]] || usage

RUNNER="${CRON_ROOT}/runners/${JOB_ID}.sh"
if [[ ! -x "$RUNNER" ]]; then
  if [[ -f "$RUNNER" ]]; then
    chmod +x "$RUNNER"
  else
    echo "Runner not found: $RUNNER" >&2
    exit 1
  fi
fi

export WORKSPACE_ROOT CRON_ROOT JOB_ID MODE="${MODE:-cron}"
exec "$RUNNER"
