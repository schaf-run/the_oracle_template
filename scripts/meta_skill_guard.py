#!/usr/bin/env python3
"""PreToolUse hook on EnterPlanMode: require a fresh meta-skill check first.

CLAUDE.md's "Big picture (before planning)" section says to run the
meta-skill orientation pass before planning non-trivial work, but this was
skipped twice across two separate reflection windows relying on memory
alone (see kb/history/*.md). Enforcing it mechanically instead — see
memos/0006-enforce-meta-skill-before-plan-mode.md.

The marker is consumed (reset) on each successful pass so the check is
required again before the *next* plan-mode entry, not just once ever.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".claude" / "meta_skill_state.json"


def checked():
    try:
        return json.loads(STATE.read_text()).get("checked", False)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return False


def main():
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        pass

    if not checked():
        print(
            "Run the meta-skill orientation pass (Skill: meta-skill) before "
            "entering plan mode — check whether an existing skill or "
            "sub-agent already covers this task. See "
            ".claude/skills/meta-skill/SKILL.md.",
            file=sys.stderr,
        )
        return 2

    STATE.write_text(json.dumps({"checked": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
