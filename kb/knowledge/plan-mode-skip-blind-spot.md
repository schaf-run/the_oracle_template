---
title: meta_skill_guard.py only fires on EnterPlanMode, not on skipping plan mode
summary: A large multi-file task can go straight from investigation to Edit/Write/Bash without ever calling EnterPlanMode, which evades the meta-skill guard entirely rather than tripping it.
tags: [hooks, meta-skill, plan-mode, gotcha]
updated: 2026-09-22
---

# meta_skill_guard.py only fires on EnterPlanMode, not on skipping plan mode

`scripts/meta_skill_guard.py` (memo 0006) hard-blocks `EnterPlanMode`
unless the `meta-skill` orientation ran first. It says nothing about
tasks that should have entered plan mode at all — CLAUDE.md's own bar is
"anything touching more than one file" — but went straight from
investigation to `Edit`/`Write`/`Bash` instead.

## Observed once

A ~40-file deletion (removing an app that no longer belongs in this repo)
skipped `EnterPlanMode` entirely. Because the hook only fires as a
`PreToolUse` matcher on `EnterPlanMode`, it never triggered — skipping
plan mode evades the guard rather than tripping it, unlike skipping just
the meta-skill check before an actual `EnterPlanMode` call (which memo
0006 does catch).

## Status

Only seen once so far, so per this repo's own "must actually recur" bar
this hasn't become a new hook. If it recurs, the likely fix is a broader
`PreToolUse` trigger (e.g. on multi-file `Write`/`Edit`/`Bash` batches
past some file-count threshold) since `EnterPlanMode` isn't a mandatory
gate today. See `memos/0006-enforce-meta-skill-before-plan-mode.md` for
the existing hook design this would extend.
