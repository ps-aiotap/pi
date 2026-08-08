#!/usr/bin/env python3
"""Return exit 0 if a PI skill already completed (artifacts/state), else 1.

Usage:
  skill-already-done.py <skill-id> [YYYY-MM-DD] [PB-KEY]
  skill-already-done.py --check-intake PB-xxxx

Prints a one-line reason to stdout.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE_ROOT", "/var/www/sourcecode"))
PI = WORKSPACE / "pi"
# Python 3.8 host — no zoneinfo; IST is fixed UTC+05:30
IST = timezone(timedelta(hours=5, minutes=30))
MATRIX = WORKSPACE / "cron/config/hourly-skill-matrix.json"


def today_ist() -> str:
    # Prefer system TZ for DST-less IST correctness via date(1)
    try:
        out = subprocess.check_output(
            ["date", "+%Y-%m-%d"],
            env={**os.environ, "TZ": "Asia/Kolkata"},
            text=True,
        ).strip()
        if out:
            return out
    except (OSError, subprocess.CalledProcessError):
        pass
    return datetime.now(IST).strftime("%Y-%m-%d")


def file_ok(path: Path, min_bytes: int = 40) -> bool:
    try:
        return path.is_file() and path.stat().st_size >= min_bytes
    except OSError:
        return False


def deep_dive_done(date: str) -> tuple[bool, str]:
    report = PI / "reports" / f"daily-deep-dive-{date}.md"
    if file_ok(report, min_bytes=40):
        return True, f"report exists: {report}"
    stable = PI / "reports" / "daily-deep-dive.md"
    if file_ok(stable, min_bytes=40):
        # Stable pointer only counts if it mentions today's date
        try:
            text = stable.read_text(encoding="utf-8", errors="ignore")
            if date in text[:200] or f"daily-deep-dive-{date}" in text:
                return True, f"stable rollup covers {date}: {stable}"
        except OSError:
            pass
    state_path = PI / "ops" / "daily-deep-dive-state.json"
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            for run in state.get("runs") or []:
                if run.get("date") == date and run.get("keys"):
                    return True, f"state runs has {date} keys={run.get('keys')}"
        except (OSError, json.JSONDecodeError):
            pass
    return False, "deep dive not done yet"


def intake_done_for_key(key: str) -> tuple[bool, str]:
    """Intake/analysis already done for a PI if spec (+ preferably test-plan) exists."""
    key = key.strip().upper()
    spec = PI / "specs" / f"{key}.md"
    plan = PI / "test-plans" / f"{key}.md"
    evidence = PI / "evidence-analysis" / f"{key}.md"
    if file_ok(spec, min_bytes=200) and file_ok(plan, min_bytes=100):
        return True, f"spec+test-plan exist: {spec.name}, {plan.name}"
    if file_ok(spec, min_bytes=200) and file_ok(evidence, min_bytes=100):
        return True, f"spec+evidence-analysis exist: {spec.name}, {evidence.name}"
    if file_ok(spec, min_bytes=400):
        return True, f"spec exists (intake done): {spec}"
    return False, f"intake not done for {key} (missing {spec})"


def open_analysis_done(date: str) -> tuple[bool, str]:
    p = PI / "reports" / f"daily-ops-{date}.md"
    if file_ok(p):
        return True, f"exists: {p}"
    return False, "daily open analysis not done"


def detail_elaboration_done(date: str) -> tuple[bool, str]:
    p = PI / "reports" / "pi-detail-elaboration.md"
    if not file_ok(p):
        return False, "detail elaboration report missing"
    try:
        mtime = datetime.fromtimestamp(p.stat().st_mtime, IST).strftime("%Y-%m-%d")
        if mtime == date:
            return True, f"updated today: {p}"
        # Also accept if file body mentions today's date near the top
        head = p.read_text(encoding="utf-8", errors="ignore")[:400]
        if date in head:
            return True, f"dated {date} in report: {p}"
        return False, f"report stale (mtime {mtime}): {p}"
    except OSError:
        return False, "detail elaboration unreadable"


def non_eng_done(date: str) -> tuple[bool, str]:
    for name in (f"non-eng-disposition-{date}.md", "non-eng-disposition.md"):
        p = PI / "reports" / name
        if file_ok(p):
            if name.endswith(f"{date}.md"):
                return True, f"exists: {p}"
            head = p.read_text(encoding="utf-8", errors="ignore")[:300]
            if date in head:
                return True, f"covers {date}: {p}"
    return False, "non-eng disposition not done"


def meeting_brief_done(date: str) -> tuple[bool, str]:
    p = PI / "reports" / f"meeting-brief-{date}.md"
    if file_ok(p):
        return True, f"exists: {p}"
    return False, "meeting brief not done"


def stale_reminder_done(date: str) -> tuple[bool, str]:
    # Prefer explicit ops marker; fall back to hourly-ops fired state
    marker = PI / "ops" / f"stale-assignee-reminder-{date}.done"
    if marker.is_file():
        return True, f"marker: {marker}"
    hourly = WORKSPACE / "cron/state/pi-hourly-ops.json"
    if hourly.is_file():
        try:
            state = json.loads(hourly.read_text(encoding="utf-8"))
            if "pi-stale-assignee-reminder" in (state.get("fired") or {}).get(date, []):
                return True, "already fired in pi-hourly-ops state"
        except (OSError, json.JSONDecodeError):
            pass
    return False, "stale reminder not done"


def skill_done(skill_id: str, date: str, key: str | None = None) -> tuple[bool, str]:
    checkers = {
        "pi-daily-deep-dive": lambda: deep_dive_done(date),
        "pi-daily-open-analysis": lambda: open_analysis_done(date),
        "pi-detail-elaboration": lambda: detail_elaboration_done(date),
        "pi-non-eng-disposition": lambda: non_eng_done(date),
        "pi-meeting-brief": lambda: meeting_brief_done(date),
        "pi-stale-assignee-reminder": lambda: stale_reminder_done(date),
        "pi-intake-impact-fix-spec": lambda: (
            intake_done_for_key(key) if key else (False, "PB key required for intake check")
        ),
    }
    fn = checkers.get(skill_id)
    if not fn:
        # Unknown skill: not considered done via artifacts
        return False, f"no artifact checker for {skill_id}"
    return fn()


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("Usage: skill-already-done.py <skill-id> [date] [PB-KEY] | --check-intake PB-KEY", file=sys.stderr)
        return 2

    if args[0] == "--check-intake":
        if len(args) < 2:
            print("PB key required", file=sys.stderr)
            return 2
        done, reason = intake_done_for_key(args[1])
        print(reason)
        return 0 if done else 1

    skill_id = args[0]
    date = args[1] if len(args) > 1 and not args[1].upper().startswith("PB-") else today_ist()
    key = None
    for a in args[1:]:
        if a.upper().startswith("PB-"):
            key = a
            break
        if len(a) == 10 and a[4] == "-" and a[7] == "-":
            date = a

    done, reason = skill_done(skill_id, date, key)
    print(reason)
    return 0 if done else 1


if __name__ == "__main__":
    raise SystemExit(main())
