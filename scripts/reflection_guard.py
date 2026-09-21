#!/usr/bin/env python3
"""Stop hook: every 5th completed task, block once and nudge the reflection skill."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".claude" / "reflection_state.json"
EVERY = 5


def load_count():
    try:
        return json.loads(STATE.read_text()).get("count", 0)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return 0


def save_count(n):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"count": n}))


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    # Already nudged this turn (by this hook or another Stop hook) — never
    # double-count a task, and never loop.
    if payload.get("stop_hook_active"):
        return 0

    count = load_count() + 1
    if count < EVERY:
        save_count(count)
        return 0

    save_count(0)
    reason = (
        f"{EVERY} tasks completed since the last reflection — run the "
        "reflection skill: review what was done, whether a recurring "
        "pattern is worth turning into a skill, and what could be "
        "improved. Write findings to kb/history/ (see "
        ".claude/skills/reflection/SKILL.md). If there's genuinely "
        "nothing to record, say so in one line and stop."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
