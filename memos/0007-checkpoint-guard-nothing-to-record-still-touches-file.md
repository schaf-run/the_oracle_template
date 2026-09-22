---
title: "0007: A no-op checkpoint still has to touch CURRENT.md"
summary: checkpoint_guard.py compares mtimes, not content — saying "nothing to record" in chat doesn't clear it; the file must be touched.
tags: [hooks, progress, continuity]
updated: 2026-09-22
---

# 0007: A no-op checkpoint still has to touch CURRENT.md

Date: 2026-09-22

## Context

`checkpoint_guard.py` (see `0003-stop-hook-checkpoint-guard.md`) blocks
`Stop` by comparing file mtimes against `kb/progress/CURRENT.md`'s mtime —
it has no way to know whether a reply of "nothing worth recording" was
ever said. In a session that only read files or changed unrelated repo
state (e.g. files that pre-dated the conversation, like an
already-modified `.claude/settings.json`), replying in chat without
editing `CURRENT.md` satisfies the guard's *intent* but not its check, so
it re-fires on the next `Stop` for the same files.

## Decision

Treat "nothing worth recording" as itself a checkpoint: make a small edit
to `CURRENT.md` (even just an updated `updated:`/timestamp note or a one
line addition under the relevant section) rather than only replying in
the transcript.

## Why

The guard is deliberately mtime-only and stateless (0003) — the fix
belongs on the agent side, not the hook. Changing the hook to parse chat
intent would add complexity for a rare case; touching the file costs one
edit and keeps the guard's contract simple.

## Consequences

Every `Stop` that would otherwise reply "nothing to record" now includes
a trivial `CURRENT.md` edit. Depends on `0003-stop-hook-checkpoint-guard.md`.
