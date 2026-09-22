#!/usr/bin/env python3
"""Stop hook: reset meta-skill guard state at the end of every turn.

Gives each new task a fresh budget for scripts/meta_skill_guard.py's
file-count/bulk-bash check, using the same "Stop = task boundary" proxy
reflection_guard.py already relies on (memo 0004). Never blocks —
resetting is unconditional and silent.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".claude" / "meta_skill_state.json"
DEFAULT_STATE = {"checked": False, "plan_mode_used": False, "touched": []}


def main():
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(DEFAULT_STATE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
