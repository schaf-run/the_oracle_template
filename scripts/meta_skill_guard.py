#!/usr/bin/env python3
"""PreToolUse hook: require a fresh meta-skill check (or plan mode) before
a task goes multi-file.

Originally gated only EnterPlanMode (memo 0006). That left a blind spot:
a task that goes straight from investigation to Write/Edit/Bash without
ever calling EnterPlanMode never tripped the guard at all — see
kb/knowledge/plan-mode-skip-blind-spot.md and memo 0014. Now also gates
the second distinct file touched via Write/Edit, and a handful of
bulk-mutating Bash patterns (git rm, git mv, rm -r/-rf/-fr, find
-delete) — a best-effort heuristic, not exhaustive.

State (.claude/meta_skill_state.json):
  checked        - a meta-skill orientation ran since the last reset
  plan_mode_used - EnterPlanMode was entered since the last reset (once
                    true, the rest of this turn's edits are plan-covered
                    and shouldn't re-trip the file-count check)
  touched         - distinct file paths written/edited since the last
                    reset (excluding bookkeeping files, see IGNORE)

All three reset to their defaults every turn by
scripts/meta_skill_state_reset.py (a Stop hook), so each new task gets a
fresh budget.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".claude" / "meta_skill_state.json"

# Bookkeeping files touched on nearly every turn regardless of task size
# — same exclusion checkpoint_guard.py makes for its own purpose.
IGNORE = {"kb/progress/CURRENT.md", "kb/INDEX.md"}

BULK_BASH = re.compile(
    r"\bgit\s+rm\b|\bgit\s+mv\b|\brm\s+-\w*[rf]\w*|\bfind\b.*-delete"
)

DEFAULT_STATE = {"checked": False, "plan_mode_used": False, "touched": []}

MESSAGE = (
    "Run the meta-skill orientation pass (Skill: meta-skill) before "
    "touching a second file (or running a bulk file operation) in this "
    "task — check whether an existing skill or sub-agent already covers "
    "it, and whether plan mode is warranted. See "
    ".claude/skills/meta-skill/SKILL.md."
)


def load_state():
    try:
        data = json.loads(STATE.read_text())
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return dict(DEFAULT_STATE)
    return {**DEFAULT_STATE, **data}


def save_state(state):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state))


def relative_path(file_path):
    try:
        return str(Path(file_path).resolve().relative_to(ROOT))
    except ValueError:
        return file_path


def block():
    print(MESSAGE, file=sys.stderr)
    return 2


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input", {})
    state = load_state()

    if tool_name == "EnterPlanMode":
        if not state["checked"]:
            return block()
        save_state({"checked": False, "plan_mode_used": True, "touched": []})
        return 0

    if tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path")
        if file_path:
            rel = relative_path(file_path)
            if rel not in IGNORE and rel not in state["touched"]:
                state["touched"].append(rel)
        if len(state["touched"]) > 1 and not state["checked"] and not state["plan_mode_used"]:
            save_state(state)
            return block()
        save_state(state)
        return 0

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if BULK_BASH.search(command) and not state["checked"] and not state["plan_mode_used"]:
            return block()
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
