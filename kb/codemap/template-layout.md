---
title: Template layout
summary: What lives where in the_oracle_template and which files are generated.
tags: [layout, scaffolding]
updated: 2026-09-21
---

# Template layout

```
CLAUDE.md                          agent rules — the core deliverable
.claude/
  settings.json                    hooks: PostToolUse rebuilds kb index,
                                   Stop runs checkpoint_guard.py then
                                   reflection_guard.py
  agents/README.md                 when to define a custom sub-agent
  skills/README.md                 skill conventions
  skills/meta-skill/SKILL.md       pre-planning gap check
  skills/kb/SKILL.md               how to query and write the kb
  skills/choose-model/SKILL.md     model tier + effort picker
  skills/create-subagent/SKILL.md  how to author .claude/agents/<name>.md
  skills/reflection/SKILL.md       retrospective every 5 tasks
  kb.db                            GENERATED, gitignored
  reflection_state.json            GENERATED, gitignored — task counter
kb/
  INDEX.md                         GENERATED — do not hand-edit
  README.md, TEMPLATE.md           conventions and note skeleton
  progress/ knowledge/ codemap/ docs/ history/
memos/
  TEMPLATE.md, NNNN-*.md           append-only decision records
scripts/
  kb_index.py                      builds FTS index + INDEX.md
  kb_query.py                      ranked search
  checkpoint_guard.py              Stop hook: nudge if CURRENT.md is stale
  reflection_guard.py              Stop hook: nudge reflection every 5 tasks
.mcp.json.example                  shape for a project MCP server
```

## Generated files

`kb/INDEX.md` and `.claude/kb.db` are both produced by
`scripts/kb_index.py`. The `.db` is gitignored; `INDEX.md` is committed
because it is a useful human-readable table of contents.

## Indexed roots

The indexer walks both `kb/**` and `memos/**`. Kind is derived from the
directory: a note's parent folder under `kb/`, or `memos` for anything in
`memos/`. Files named `INDEX.md`, `README.md` or `TEMPLATE.md` at a root
are skipped.
