---
title: Template layout
summary: What lives where in the_oracle_template and which files are generated.
tags: [layout, scaffolding]
updated: 2026-09-22
---

# Template layout

```
CLAUDE.md                          agent rules — the core deliverable.
                                   "Creating sub-agents" caps concurrency
                                   at 2 running at once (user instruction,
                                   also in personal cross-session memory).
.claude/
  settings.json                    hooks — see "Hooks" below
  agents/README.md                 when to define a custom sub-agent
  agents/researcher.md             read-only research agent (Read/Grep/
                                   Glob/WebSearch/WebFetch, no edit/run/
                                   spawn), model tier chosen per call
                                   against a user-approved policy rather
                                   than fixed in frontmatter — memo 0008
  agents/architect.md              plans only, never executes (Read/Grep/
                                   Glob/Bash/WebSearch/WebFetch; no Edit/
                                   Write/Agent). Two-phase protocol baked
                                   into its prompt: high-level plan first,
                                   detail only when a section is
                                   requested, hard refusal on detailing
                                   everything in one shot. Orchestrator
                                   convention: reuse the same agent
                                   instance across detail calls rather
                                   than fresh-spawning — memo 0009
  skills/README.md                 skill conventions
  skills/meta-skill/SKILL.md       pre-planning gap check — separately
                                   checks planning-fit and
                                   implementation-fit against
                                   .claude/agents/*.md, not just one
  skills/kb/SKILL.md               how to query and write the kb
  skills/choose-model/SKILL.md     model tier + effort picker
  skills/create-subagent/SKILL.md  how to author .claude/agents/<name>.md
  skills/reflection/SKILL.md       retrospective every 10 tasks, writes
                                   to kb/history/, commits its own output
  skills/deliver-research/SKILL.md after researcher hands back a report:
                                   write full findings to a scratchpad
                                   file, send a condensed summary with
                                   the doc attached — added once the
                                   pattern repeated twice, see
                                   kb/history/2026-09-22-researcher-runs-
                                   and-architect-agent.md
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
  kb_query.py                      ranked search — tries exact syntax,
                                   then AND of all terms, then OR, so
                                   natural-language questions still land;
                                   results ranked BM25, progress first
  checkpoint_guard.py              Stop hook: blocks once if any
                                   git-tracked file has an mtime newer
                                   than kb/progress/CURRENT.md — memo 0003
  reflection_guard.py              Stop hook: blocks once every 10th
                                   completed task, runs the reflection
                                   skill, which commits its own output —
                                   memos 0004, 0010
  meta_skill_guard.py              PreToolUse hook on EnterPlanMode:
                                   hard-blocks unless the meta-skill
                                   orientation ran since the last
                                   plan-mode entry — memo 0006
  meta_skill_track.py              PostToolUse hook on Skill: records
                                   that meta-skill ran, for the guard above
.mcp.json.example                  shape for a project MCP server
```

## Hooks

`.claude/settings.json`: `PreToolUse` on `EnterPlanMode` runs
`meta_skill_guard.py`; `PostToolUse` on `Write`/`Edit` rebuilds the kb
index (`kb_index.py --if-stale --quiet`) and on `Skill` runs
`meta_skill_track.py`; `Stop` runs `checkpoint_guard.py` then
`reflection_guard.py`, in that order.

## Generated files

`kb/INDEX.md` and `.claude/kb.db` are both produced by
`scripts/kb_index.py`. The `.db` is gitignored; `INDEX.md` is committed
because it is a useful human-readable table of contents.

## Indexed roots

The indexer walks both `kb/**` and `memos/**`. Kind is derived from the
directory: a note's parent folder under `kb/`, or `memos` for anything in
`memos/`. Files named `INDEX.md`, `README.md` or `TEMPLATE.md` at a root
are skipped.
