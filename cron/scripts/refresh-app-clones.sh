#!/usr/bin/env bash
# Refresh all application Bitbucket clones to origin/master.
# Excludes pi/ (GitHub PI repo). Fails on dirty trees or pull conflicts.
set -euo pipefail

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/var/www/sourcecode}"
LOG_PREFIX="[refresh-app-clones]"

log() { echo "${LOG_PREFIX} $*"; }
fail() { log "ERROR: $*"; exit 1; }

mapfile -t GIT_DIRS < <(find "$WORKSPACE_ROOT" /var/www/dashboard -name .git -type d 2>/dev/null | grep -v '/pi/' | sort -u)

if [[ ${#GIT_DIRS[@]} -eq 0 ]]; then
  fail "No application .git directories found under $WORKSPACE_ROOT or /var/www/dashboard"
fi

FAILED=0
for gitdir in "${GIT_DIRS[@]}"; do
  repo="$(dirname "$gitdir")"
  name="$(basename "$repo")"
  log "=== $name ($repo) ==="

  if ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    log "SKIP: not a git work tree"
    continue
  fi

  if [[ -n "$(git -C "$repo" status --porcelain 2>/dev/null)" ]]; then
    log "BLOCKED: dirty working tree — commit/stash before loop"
    FAILED=1
    continue
  fi

  git -C "$repo" fetch --prune origin || { log "FAIL: fetch"; FAILED=1; continue; }

  if git -C "$repo" show-ref --verify --quiet refs/heads/master; then
    git -C "$repo" checkout master
  elif git -C "$repo" show-ref --verify --quiet refs/heads/main; then
    log "WARN: no master; using main"
    git -C "$repo" checkout main
  else
    log "FAIL: no master or main branch"
    FAILED=1
    continue
  fi

  BRANCH="$(git -C "$repo" branch --show-current)"
  if git -C "$repo" show-ref --verify --quiet "refs/remotes/origin/${BRANCH}"; then
    git -C "$repo" pull --ff-only "origin" "$BRANCH" || { log "FAIL: pull --ff-only"; FAILED=1; continue; }
  else
    log "WARN: no origin/${BRANCH} — left on local ${BRANCH}"
  fi

  log "OK: $(git -C "$repo" rev-parse --short HEAD) on ${BRANCH}"
done

# Playwright deps (dashboard)
if [[ -d /var/www/dashboard ]] && [[ -f /var/www/dashboard/package.json ]]; then
  if [[ ! -d /var/www/dashboard/node_modules/@playwright/test ]]; then
    log "Installing @playwright/test in dashboard (requires avnpm credentials)..."
    (cd /var/www/dashboard && npm install @playwright/test@^1.40.0 --save-dev --no-audit --no-fund --legacy-peer-deps 2>&1) || \
      log "WARN: @playwright/test install failed — configure npm for avnpm and re-run"
  fi
  if [[ -x /var/www/dashboard/node_modules/.bin/playwright ]]; then
    (cd /var/www/dashboard && ./node_modules/.bin/playwright install chromium 2>&1) || \
      log "WARN: playwright browser install skipped"
  fi
fi

if [[ "$FAILED" -ne 0 ]]; then
  fail "One or more repos failed refresh — fix before pi-sdlc-fix-loop"
fi

log "All application clones refreshed."
