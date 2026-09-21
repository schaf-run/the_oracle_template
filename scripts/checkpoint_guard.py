#!/usr/bin/env python3
"""Stop hook: block once if project files changed after kb/progress/CURRENT.md."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURRENT = ROOT / "kb" / "progress" / "CURRENT.md"
IGNORE = {"kb/INDEX.md", "kb/progress/CURRENT.md"}
SLACK_SECONDS = 2.0
SHOW = 5


def changed_since(timestamp):
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout.decode()
    hits = []
    for rel in out.split("\0"):
        if not rel or rel in IGNORE:
            continue
        try:
            if (ROOT / rel).stat().st_mtime > timestamp + SLACK_SECONDS:
                hits.append(rel)
        except FileNotFoundError:
            continue
    return sorted(hits)


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    # Already nudged this turn — let the stop through so we never loop.
    if payload.get("stop_hook_active") or not CURRENT.exists():
        return 0

    try:
        hits = changed_since(CURRENT.stat().st_mtime)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0
    if not hits:
        return 0

    shown = ", ".join(hits[:SHOW])
    if len(hits) > SHOW:
        shown += f" (+{len(hits) - SHOW} more)"
    reason = (
        f"Checkpoint needed: {shown} changed since kb/progress/CURRENT.md was "
        "last updated. Update CURRENT.md (done / next / open) and add a memo "
        "if a decision was made. If nothing here is worth recording, say so "
        "in one line and stop."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
