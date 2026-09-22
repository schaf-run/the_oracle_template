#!/usr/bin/env python3
"""PostToolUse hook: record that meta-skill's orientation pass has run.

Paired with meta_skill_guard.py (PreToolUse on EnterPlanMode, Write,
Edit, Bash), which requires this marker to be fresh before allowing
plan mode to start or a task to go multi-file. Merges into the existing
state rather than overwriting it, so plan_mode_used/touched (also
tracked in the same file) survive.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".claude" / "meta_skill_state.json"
DEFAULT_STATE = {"checked": False, "plan_mode_used": False, "touched": []}


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_input", {}).get("skill") != "meta-skill":
        return 0

    try:
        state = {**DEFAULT_STATE, **json.loads(STATE.read_text())}
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        state = dict(DEFAULT_STATE)

    state["checked"] = True
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
