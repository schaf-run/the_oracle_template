---
title: "0014: Close the meta-skill guard's EnterPlanMode-skip blind spot"
summary: meta_skill_guard.py now also gates the second distinct file touched via Write/Edit and bulk-mutating Bash commands, not just EnterPlanMode — closing the gap where skipping plan mode entirely evaded the check.
tags: [hooks, meta-skill, plan-mode]
updated: 2026-09-22
---

# 0014: Close the meta-skill guard's EnterPlanMode-skip blind spot

Date: 2026-09-22

## Context

Memo 0006 added a `PreToolUse` hook on `EnterPlanMode` requiring a fresh
`meta-skill` check first. `kb/history/2026-09-22-remote-branch-and-app-
removal.md` (since removed, memo 0011) flagged a gap in that design: a
~40-file deletion went straight from investigation to `git rm`/`Edit`/
`Write` without ever calling `EnterPlanMode`, so the hook — scoped only
to that one tool — never fired at all. Documented as "only seen once, not
yet a hook" in `kb/knowledge/plan-mode-skip-blind-spot.md`. The user has
now explicitly asked to close it, overriding that recurrence bar the same
way memo 0011 overrode "history is immutable."

## Decision

Widened `settings.json`'s `PreToolUse` matcher from `EnterPlanMode` to
`EnterPlanMode|Write|Edit|Bash`, and extended `scripts/
meta_skill_guard.py`'s state (`.claude/meta_skill_state.json`) from
`{"checked": bool}` to `{"checked": bool, "plan_mode_used": bool,
"touched": [...]}`:

- `EnterPlanMode`: unchanged strict check; on pass, also sets
  `plan_mode_used: true` and clears `touched` — the rest of the turn's
  edits are plan-covered and shouldn't re-trip the file-count check.
- `Write`/`Edit`: tracks distinct file paths touched (excluding
  `kb/progress/CURRENT.md`/`kb/INDEX.md`, the same bookkeeping-file
  exclusion `checkpoint_guard.py` already makes for its own purpose).
  Blocks on the second distinct file if neither `checked` nor
  `plan_mode_used` is true.
- `Bash`: blocks on a regex match against `git rm`, `git mv`,
  `rm -r`/`-rf`/`-fr`, `find ... -delete` under the same condition — a
  best-effort heuristic (see `kb/knowledge/plan-mode-skip-blind-spot.md`
  for its documented limits), not a full "will this touch multiple
  files" detector.

`scripts/meta_skill_track.py` (`PostToolUse` on `Skill`) now
load-modifies-saves instead of overwriting the whole state file, so
`plan_mode_used`/`touched` survive a meta-skill check being recorded.

New Stop hook `scripts/meta_skill_state_reset.py` unconditionally resets
all three keys to their defaults every turn — reusing the same "Stop =
task boundary" proxy `reflection_guard.py` established (memo 0004) —
so each new task gets a fresh budget rather than the state accumulating
across unrelated tasks or staying permanently unlocked after one
`EnterPlanMode` call early in a session.

## Why

The threshold (`> 1` distinct file) matches CLAUDE.md's own literal bar
("anything touching more than one file") exactly rather than picking an
arbitrary count. `plan_mode_used` is tracked separately from `checked`
(rather than reusing one flag for both) because `EnterPlanMode` *consumes*
`checked` by design (memo 0006 — forces a fresh check before the *next*
`EnterPlanMode` too), but a plan's approved execution phase still needs
to freely touch many files without re-tripping the same guard; conflating
the two would have either broken normal plan execution or silently
disabled the re-check-before-next-`EnterPlanMode` guarantee.

Verified end-to-end with 12 piped test-payload scenarios (single-file
pass, second-file block, meta-skill-check unblocks a retry, bulk-Bash
block/unblock, `EnterPlanMode` block-then-pass-then-covers-rest-of-turn,
bookkeeping-file exclusion, Stop reset) — same verification discipline
memo 0006 used for the original hook pair.

## Consequences

A task that touches a second distinct file, or runs a bulk-mutating
`Bash` command, without a meta-skill check or plan-mode pass this turn
now blocks unconditionally — including a "mechanical" multi-file change
that CLAUDE.md's planning section would otherwise let skip plan mode.
This trades a small amount of extra friction (one quick `Skill(meta-
skill)` call for those cases) for actually closing the gap, rather than
trying to further distinguish "mechanical" from "risky" multi-file
changes, which would reintroduce the same fuzzy-judgment problem the
hook exists to remove.

Known accepted gap: `meta_skill_state_reset.py` fires on *every* `Stop`
event, including ones a later `Stop` hook (`checkpoint_guard.py`/
`reflection_guard.py`) blocks and retries — so state can reset mid-
sequence before the turn actually ends. In the narrow case where a
blocked-and-retried reflection pass itself needs to write two distinct
files, it could re-trip the guard it was itself triggered by. Not fixed
here — sequencing hook state around other hooks' block/retry cycles adds
real complexity for a rare intersection; revisit if it's actually
observed rather than pre-solving it. Related: `memos/0006-enforce-meta-
skill-before-plan-mode.md`, `kb/knowledge/plan-mode-skip-blind-spot.md`.
