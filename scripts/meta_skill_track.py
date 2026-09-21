#!/usr/bin/env python3
"""PostToolUse hook: record that meta-skill's orientation pass has run.

Paired with meta_skill_guard.py (PreToolUse on EnterPlanMode), which
requires this marker to be fresh before allowing plan mode to start.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".claude" / "meta_skill_state.json"


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_input", {}).get("skill") != "meta-skill":
        return 0

    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"checked": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
