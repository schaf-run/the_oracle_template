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
new project.

An earlier session built a real app (a 3D model upload/viewer) directly in
this repo to exercise the template. That app's code, plans, and
app-specific kb notes/memos have since been removed at the user's request
so the repo holds only the template itself — see `git log` for that
history if needed.

## Template contents (current)

- `CLAUDE.md` — the agent rules: big picture, planning, executing,
  knowledge base, memos, skills, hooks, MCP servers, sub-agents.
- `.claude/skills/meta-skill/` — pre-planning gap check: reuse an existing
  skill/sub-agent, or create one if the gap is genuinely recurring.
- `.claude/skills/kb/` — how to query and write the knowledge store.
- `.claude/skills/choose-model/` — model tier (Haiku/Sonnet/Opus/Fable)
  and reasoning-effort picker; applies to sessions, one-off sub-agent
  spawns, and `.claude/agents/*.md` `model:` fields.
- `.claude/skills/create-subagent/` — process for authoring a new
  `.claude/agents/<name>.md`: justify the gap, scope tools, pick a
  model, write the prompt. Points at `.claude/agents/README.md` for the
  worked example instead of duplicating it.
- `.claude/skills/reflection/` — retrospective over the last 5 tasks:
  what got done, whether a recurring pattern is worth a new skill, what
  could be improved. Writes findings to `kb/history/`.
- `kb/` + `scripts/kb_index.py` + `scripts/kb_query.py` — markdown notes
  indexed into SQLite FTS5, chunked per `##` section. Kinds: `progress`,
  `knowledge`, `codemap`, `docs`, `history`.
- `memos/` — append-only decision records. Indexed into the *same* table
  under kind `memos`, so one query reaches both stores.
- `.claude/settings.json` — hooks: `PreToolUse` on `EnterPlanMode` runs
  `meta_skill_guard.py` (hard-blocks unless the meta-skill orientation
  ran since the last plan-mode entry); `PostToolUse` rebuilds the kb
  index and (on `Skill`) tracks meta-skill invocations via
  `meta_skill_track.py`; `Stop` runs `checkpoint_guard.py` (blocks once
  when files changed after this file, see memo 0003) then
  `reflection_guard.py` (blocks once every 5th completed task to run the
  `reflection` skill, see memo 0004).
- `.mcp.json.example` — shape for a project MCP server config.

Search behaviour: `kb_query.py` tries exact syntax, then AND of all
terms, then OR, so natural-language questions still land. Results are
ranked by BM25 and ordered `progress` first.

## Git state

- `origin` is `git@github.com:schaf-run/the_oracle_template.git`.
- `main` — the clean template, pushed to `origin/main`.
- `dev` — general working branch off `main`, tracks `origin/dev`.
- `oracle-dev` — current branch, created off `dev` for new work.
- The app-removal cleanup (this update) is not yet committed.

## How to resume

1. Read this file.
2. `scripts/kb_query.py --list` to see everything stored.
3. `scripts/kb_query.py "<topic>"` for detail on any of it.

Keep this file current — it is the one thing that makes clearing context
safe. Update it at the end of any meaningful step, not just at session end.
