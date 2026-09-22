---
title: Current state
summary: Resume point — read this first after a context clear or at the start of a session.
tags: [progress, session, template]
updated: 2026-09-22
---

# Current state

`the_oracle_template` is a reusable Claude Code project template: a rules
file (`CLAUDE.md`) plus scaffolding for session continuity, a knowledge
base, memos, skills, and hooks. Copy this whole directory when starting a
new project — but copy deliberately, not whatever branch happens to be
checked out: `oracle-test` (this branch) carries a full day of
stress-test-specific `kb/history/` notes (Telegram plugin saga, 3D-app
build/removal, branch juggling) that are noise for a fresh project. Copy
`main` plus the proven mechanism commits merged into `oracle-dev` (agents,
meta-skill guard, reflection, deliver-research) — not `oracle-test`'s
history.

An earlier session built a real app (a 3D model upload/viewer) directly in
this repo to exercise the template. That app's code, plans, and
app-specific kb notes/memos have since been removed at the user's request
so the repo holds only the template itself — see `git log` for that
history if needed.

What lives where, and how each hook/skill/agent currently behaves, is
`kb/codemap/template-layout.md` — read that instead of this file for
template-mechanics reference; this file stays a resume pointer only.

## Git state

- `origin` is `git@github.com:schaf-run/the_oracle_template.git`.
- `main` — the clean template, pushed to `origin/main`.
- `dev` — general working branch off `main`, tracks `origin/dev`.
- `oracle-dev` — general template-work branch off `dev`, pushed to
  `origin/oracle-dev`.
- `oracle-test` — **current branch**, created off `oracle-dev` to
  stress-test the template with a genuine build; pushed to
  `origin/oracle-test`.
- Open: commits on this machine are attributed to an auto-configured
  git identity (`Pavel Nenarokov <schaf_run@...twc1.net>`, not the
  user's own name/email) — git warns on every commit. Offered to set
  `user.name`/`user.email` for this repo; user hasn't asked for it yet.

## Latest reflection

A second user-requested audit (this one from a fresh context) found and
fixed: a stale "5 tasks" reference in `.claude/skills/README.md` left
over from memo 0010's cycle widen, an undocumented gap in memo numbering,
`deliver-research/SKILL.md` hardcoded to Telegram specifically, and
`oracle-dev` missing memo 0010's reflection-cycle-widen commit. The
branch-copy guidance above (which branch to actually copy for a new
project) was added as part of this pass. See `git log` on `oracle-test`
and `oracle-dev` for the exact commits.

Earlier: `kb/history/2026-09-22-oracle-test-branch-and-telegram-mcp-planning.md`
— `oracle-test` branch stress-tests the template with a real build (a
self-hosted Telegram MCP connector, planned but not yet implemented —
plan file at `/home/schaf_run/.claude/plans/bubbly-dancing-waterfall.md`).
Found and fixed a real meta-skill gap-check miss (skipped `architect` on
a planning task); a user-requested bloat audit followed, corrections
applied: `meta-skill/SKILL.md` reworded, the closed-out Telegram-plugin
saga compacted into `kb/history/2026-09-22-telegram-plugin-saga-closed.md`,
this file trimmed (its old "Template contents" section now lives in
`kb/codemap/template-layout.md`).

Earlier notes: `scripts/kb_query.py --list` for the full index, or
`--kind history` to scope to reflections specifically.

## How to resume

1. Read this file.
2. `scripts/kb_query.py --list` to see everything stored.
3. `scripts/kb_query.py "<topic>"` for detail on any of it.

Keep this file current — it is the one thing that makes clearing context
safe. Update it at the end of any meaningful step, not just at session end.
