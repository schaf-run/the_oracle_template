---
title: "0003: Stop hook enforces checkpointing, one nudge per turn"
summary: Why a Stop hook blocks once when files changed after CURRENT.md, and why it never blocks twice.
tags: [hooks, progress, continuity]
updated: 2026-09-21
---

# 0003: Stop hook enforces checkpointing, one nudge per turn

Date: 2026-09-21

## Context

The "Session continuity" rule makes clearing context safe only if
`kb/progress/CURRENT.md` is current. A rule the agent must remember is
exactly what fails under a long task, so it needed enforcement.

## Decision

`scripts/checkpoint_guard.py` runs as a `Stop` hook. If any file git
would track (cached or untracked, respecting `.gitignore`) has an mtime
newer than `CURRENT.md`, it returns `{"decision": "block"}` with the list
of changed files, asking for a checkpoint. `kb/INDEX.md` is excluded
because the `PostToolUse` indexer regenerates it after every edit.

## Why

- **mtime vs CURRENT.md, not "did the agent edit anything"** — the
  question is whether the resume point is behind reality, regardless of
  who changed the files.
- **One nudge only** — when `stop_hook_active` is set, the hook always
  lets the stop through. The agent can reply "nothing worth recording"
  and stop; a guard that can loop is worse than no guard.
- **git ls-files for the file list** — respects `.gitignore`, so
  `node_modules/`, build output and the `.db` never trigger it, and it
  stays fast in large repos.
- **Fails open** — no git, no `CURRENT.md`, or bad stdin all allow the
  stop. The hook must never make a project unusable.

## Consequences

Pure conversation turns never trigger it. A `git pull` or checkout that
touches files will cause one nudge on the next stop. Rejected: a
PostToolUse reminder after every edit — too noisy, and it fires mid-step
rather than at the natural checkpoint.

Depends on `0001-knowledge-store-design.md`.
