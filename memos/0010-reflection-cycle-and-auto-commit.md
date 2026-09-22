---
title: "0010: Reflection cycle widened to 10 tasks, auto-commit added"
summary: User raised the reflection trigger from every 5 to every 10 tasks and asked for reflection's own output to be committed automatically, overriding "commit only when asked" for that one case.
tags: [hooks, skills, continuity, git]
updated: 2026-09-22
---

# 0010: Reflection cycle widened to 10 tasks, auto-commit added

Date: 2026-09-22

## Context

The reflection cycle (`memos/0004-reflection-skill-and-hook.md`) had
been firing every 5 Stop events. The user asked to widen it to 10 and to
have each reflection's output committed automatically, rather than left
in the working tree for a later explicit "commit" request (which is
`CLAUDE.md`'s default for everything else).

## Decision

- `scripts/reflection_guard.py`: `EVERY = 5` → `EVERY = 10`. The reason
  string was already built from `EVERY`, so no other logic changed.
- `.claude/skills/reflection/SKILL.md`: updated the "every 5th"
  references to "every 10th", and added step 7 — commit whatever step 5
  wrote (`kb/history/`, `kb/knowledge/`, `memos/`, `kb/INDEX.md`,
  `CURRENT.md`'s reflection pointer) in its own commit before the turn
  ends, unless step 6 (nothing to report) applied.

## Why

- **10 over 5** — user's explicit call, no other reasoning given; not a
  tradeoff to second-guess.
- **Auto-commit scoped narrowly to reflection's own output** — `CLAUDE.md`
  says "commit only when asked," and this is the standing "asked" for
  this one case going forward. Keeping the exception scoped (reflection
  files only, its own commit, never bundled with unrelated pending
  changes) means it doesn't quietly relax the default rule for
  everything else the agent touches in the same session.

## Consequences

A reflection note (and any memo/knowledge note it produces) now lands in
git history without a separate "please commit" round-trip. Any other
pending, unrelated working-tree changes at the time reflection runs are
left uncommitted, same as before — only reflection's own files are
covered by this exception.

Depends on `0004-reflection-skill-and-hook.md`.
