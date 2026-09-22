---
title: meta_skill_guard.py's bulk-Bash detection is a heuristic, not exhaustive
summary: The guard now blocks a second distinct file touched via Write/Edit and a handful of bulk-mutating Bash patterns without a prior meta-skill check or plan-mode pass — but the Bash pattern list is a best-effort heuristic, not a complete detector.
tags: [hooks, meta-skill, plan-mode, gotcha]
updated: 2026-09-22
---

# meta_skill_guard.py's bulk-Bash detection is a heuristic, not exhaustive

Originally: `scripts/meta_skill_guard.py` only fired on `EnterPlanMode`,
so a multi-file task that never called it (observed once: a ~40-file
`git rm` deletion) evaded the check entirely rather than tripping it.
Fixed in memo 0014 — see that memo for the full before/after.

## Current behavior

The guard now also gates `Write`/`Edit` (blocks on the second distinct
file touched, excluding `kb/progress/CURRENT.md`/`kb/INDEX.md`) and
`Bash` (blocks on a regex match against `git rm`, `git mv`,
`rm -r`/`-rf`/`-fr`, `find ... -delete`) — unless a meta-skill check or
`EnterPlanMode` pass already happened this turn (state in
`.claude/meta_skill_state.json`, reset every turn by
`scripts/meta_skill_state_reset.py`).

## Known limit

The `Bash` regex is a best-effort pattern list, not a real detector of
"this command will touch multiple files." It won't catch, for example, a
custom script invoked via `Bash` that itself writes many files
transitively, `sed -i` across a glob, or a bulk `mv`/`cp` with wildcards
that don't match the listed patterns. If a new bypass shape like this
recurs, extend `BULK_BASH` in `scripts/meta_skill_guard.py` rather than
trying to write a general "detect any multi-file mutation" parser.
