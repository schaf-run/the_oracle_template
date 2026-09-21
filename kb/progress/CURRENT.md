---
title: Current state
summary: Resume point — read this first after a context clear or at the start of a session.
tags: [progress, session]
updated: 2026-09-21
---

# Current state

`the_oracle_template` is a reusable Claude Code project template: a rules
file plus scaffolding, meant to be copied or cloned into future projects.
It is not an application — the deliverable *is* the conventions.

## Where things stand

Built and committed on branch `main` (local only, no remote):

- `CLAUDE.md` — the agent rules: big picture, planning, executing,
  knowledge base, memos, skills, hooks, MCP servers, sub-agents.
- `.claude/skills/meta-skill/` — pre-planning gap check: reuse an existing
  skill/sub-agent, or create one if the gap is genuinely recurring.
- `.claude/skills/kb/` — how to query and write the knowledge store.
- `kb/` + `scripts/kb_index.py` + `scripts/kb_query.py` — markdown notes
  indexed into SQLite FTS5, chunked per `##` section. Kinds: `progress`,
  `knowledge`, `codemap`, `docs`, `history`.
- `memos/` — append-only decision records. Indexed into the *same* table
  under kind `memos`, so one query reaches both stores.
- `.claude/settings.json` — `PostToolUse` hook that rebuilds the index.
- `CLAUDE.md` "Session continuity" — the rule that makes clearing context
  safe: read this file first, checkpoint it after every meaningful step.

Search behaviour: query tries exact syntax, then AND of all terms, then
OR, so natural-language questions still land. Results are ranked by BM25
and ordered `progress` first.

## Next steps

- No git remote yet. The user declined one for now ("not yet"); revisit
  when the template is ready to clone into a real project.
- The `PostToolUse` hook has never been observed firing — it only loads
  when a session starts with that settings file. Not load-bearing, since
  `kb_query.py` rebuilds on staleness, but worth confirming once.
- Open question: whether to ship example skills/sub-agents beyond
  `meta-skill` and `kb`, or keep the template minimal.

## How to resume

1. Read this file.
2. `scripts/kb_query.py --list` to see everything stored.
3. `scripts/kb_query.py "<topic>"` for detail on any of it.

Keep this file current — it is the one thing that makes clearing context
safe. Update it at the end of any meaningful step, not just at session end.
