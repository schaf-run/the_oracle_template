---
title: "0015: Mirror project-specific personal memories into the repo"
summary: Added a CLAUDE.md rule and a kb/SKILL.md line requiring project-specific personal cross-session memories to also be written into kb/knowledge/ or memos/, since that lesson had only ever been noted in prose, never enforced.
tags: [process, memory, kb]
updated: 2026-09-22
---

# 0015: Mirror project-specific personal memories into the repo

Date: 2026-09-22

## Context

`kb/history/2026-09-22-researcher-agent-commit-and-remote-control.md`
(since removed, memo 0011) found and fixed one instance of this: a
Telegram/plan-mode convention had been saved only to the harness's
personal cross-session memory system (outside this repo), so it wouldn't
travel with the repo to a different machine or account. The same lesson
was restated as prose in `kb/progress/CURRENT.md`'s reflection summary.
It never became an actual rule an agent reads every session — it only
existed as something a past session happened to notice and fix once.
The user asked to close this gap generally.

## Decision

Added one bullet to `CLAUDE.md`'s "Session continuity" section and one
line to `.claude/skills/kb/SKILL.md`'s "Rules" list (the point where an
agent is already deciding what belongs in `kb/`): a personal
cross-session memory that documents *this project's* conventions, not
just a general user preference, must also be written into
`kb/knowledge/` or `memos/` in the same turn.

Checked the two personal memories that currently exist for this project
(`feedback_telegram_plan_mode_approval.md`,
`feedback_subagent_concurrency_cap.md`) — no migration needed: the
concurrency cap is already mirrored (it's directly in `CLAUDE.md`'s
"Creating sub-agents" section); the Telegram one is now moot since the
plugin is gone, so mirroring it would add dead weight rather than close
a real gap.

## Why

Not a hook: the personal memory directory lives outside
`$CLAUDE_PROJECT_DIR`, at a path derived from the user's home directory
and a slugified project path that isn't a documented, stable API to
hardcode against — and even if it were locatable, "is this memory
project-specific or a general preference" is a semantic judgment call, not
a mechanical condition a hook script can reliably evaluate. This matches
CLAUDE.md's own "Hooks" section bar exactly: reach for a hook only for
things that must happen mechanically every time; use a rule when the
step needs judgment. A rule read every session (`CLAUDE.md`) plus a
reminder at the exact point of writing (`kb/SKILL.md`) is the closest
mechanical approximation available without a hook.

## Consequences

Going forward, saving a project-relevant personal memory and *not* also
writing the durable part into `kb/`/`memos/` in the same turn is a rule
violation, not just a missed opportunity — the same way skipping
`CURRENT.md` checkpointing already is. If this keeps getting missed in
practice despite the rule, that's a signal to reconsider whether some
mechanical trigger is achievable after all (e.g. if the harness ever
exposes a stable, documented hook point for memory writes) rather than
proof the rule doesn't work.
