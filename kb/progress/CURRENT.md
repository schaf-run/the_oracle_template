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
  knowledge base, memos, skills, hooks, MCP servers, sub-agents. Its
  "Creating sub-agents" section now also caps concurrency: never run
  more than 2 sub-agents at once, queue the rest (user instruction,
  2026-09-22; also saved to personal cross-session memory since it's a
  general orchestration preference, not just this repo).
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
- `.claude/skills/deliver-research/` — after `researcher` hands back a
  report, write the full findings to a scratchpad file and send a
  condensed Telegram summary with the doc attached. Added after the
  pattern repeated twice — see
  `kb/history/2026-09-22-researcher-runs-and-architect-agent.md`.
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
  `reflection_guard.py` (blocks once every 10th completed task to run
  the `reflection` skill and, per its process, commit its own output —
  see memos 0004 and 0010).
- `.mcp.json.example` — shape for a project MCP server config.
- `.claude/agents/researcher.md` — read-only research role (`Read, Grep,
  Glob, WebSearch, WebFetch`, no edit/run/spawn access). Model tier
  chosen per call against a user-approved policy rather than fixed in
  frontmatter — see `memos/0008-researcher-subagent.md`.
- `.claude/agents/architect.md` — plans only, never executes (`Read,
  Grep, Glob, Bash, WebSearch, WebFetch`; no `Edit`/`Write`/`Agent`).
  Two-phase protocol baked into its prompt: high-level plan first,
  detail only when a specific section is requested, hard refusal on
  "detail the whole thing in one shot." Orchestrator convention: reuse
  the same agent instance across section-detail calls rather than
  fresh-spawning each time — see `memos/0009-architect-subagent.md`.

Search behaviour: `kb_query.py` tries exact syntax, then AND of all
terms, then OR, so natural-language questions still land. Results are
ranked by BM25 and ordered `progress` first.

## Git state

- `origin` is `git@github.com:schaf-run/the_oracle_template.git`.
- `main` — the clean template, pushed to `origin/main`.
- `dev` — general working branch off `main`, tracks `origin/dev`.
- `oracle-dev` — current branch, created off `dev` for new work. Many
  commits ahead of `dev` (app removal, reflection notes, telegram plugin
  enable/disable, researcher + architect sub-agents, deliver-research
  skill — see `git log --oneline dev..oracle-dev`). Not yet pushed.
- Open: commits on this machine are attributed to an auto-configured
  git identity (`Pavel Nenarokov <schaf_run@...twc1.net>`, not the
  user's own name/email) — git warns on every commit. Offered to set
  `user.name`/`user.email` for this repo; user hasn't asked for it yet.

## Latest reflection

`kb/history/2026-09-22-oracle-test-branch-and-telegram-mcp-planning.md` —
`oracle-test` branch created off `oracle-dev` to stress-test the template
with a genuine build (a self-hosted Telegram MCP connector, planned but
not yet implemented — plan file at
`/home/schaf_run/.claude/plans/bubbly-dancing-waterfall.md`). Found a
real meta-skill gap-check miss: the check only asked "which agent
implements this," never "which agent plans this," so it skipped
`architect` on a task that needed it — caught only because the user
asked why. Routed to `architect` after the fact; it found a genuine bug
in the draft (a local-filesystem-path return value meaningless to a
remote MCP client) and produced the fix. User then asked for a bloat
audit of the template itself: 9 memos/543 lines, 7 kb/history notes/405
lines, 6 hook scripts/453 lines, all about the template's own machinery,
none about shipped product. Corrections proposed (reword
`meta-skill/SKILL.md` step 2 to separate planning-fit from
implementation-fit; compact closed-out `kb/history/` sagas like the now-
dead Telegram plugin instead of leaving fragments; move "how do the
hooks/skills currently work" content out of this file into
`kb/knowledge/`/`kb/codemap/`) but **not yet applied** — awaiting user
confirmation.

Earlier: `kb/history/2026-09-22-researcher-runs-and-architect-agent.md`
(two `researcher` runs followed the exact same deliver pattern twice, so
it became `.claude/skills/deliver-research/`; built `architect`
(memo 0009) with a user-corrected tool scope; found plan mode blocks the
Telegram `reply` tool entirely, `AskUserQuestion` is the only channel
that still reaches Telegram while planning — documented in
`kb/knowledge/telegram-plan-mode-approval.md` before that note was
pruned as stale once the Telegram plugin was removed),
`kb/history/2026-09-22-researcher-agent-commit-and-remote-control.md`
(researcher sub-agent built end-to-end; Telegram/plan-mode approval
convention mirrored from personal memory into `kb/knowledge/` so it
travels with the repo), `kb/history/2026-09-22-telegram-qa-and-concurrent-current-md-edit.md`
(CURRENT.md can be edited concurrently by another session — one
occurrence), `kb/history/2026-09-22-checkpoint-guard-friction.md`
(guard is mtime-only — convention fix in memo 0007).

## Session note (2026-09-22, later)

Telegram plugin removed at user's request ("works bad, seems useless"):
`claude plugin uninstall telegram --scope project` (plain `uninstall
telegram` failed first — plugin was project-scoped, not user-scoped, so
`--scope project` was required). This cleared `enabledPlugins` in
`.claude/settings.json` and the entry in
`~/.claude/plugins/installed_plugins.json`. Also killed the still-running
bot process (PID 13786, a `bun` process) and removed the stale
`~/.claude/channels/telegram/bot.pid`; left the bot token
(`~/.claude/channels/telegram/.env`) and `access.json` in place since
those weren't asked for and live outside the repo. Pruned
`kb/knowledge/telegram-plan-mode-approval.md` (a plugin-specific
convention, now stale here) and reran `kb_index.py`; kept the `history/`
entries since those are logs of what happened, not current-state claims.
The `.claude/skills/telegram:access` / `telegram:configure` skills and
`.claude/agents` references to Telegram in `deliver-research` still
mention it — untouched since they're inert without the plugin and not
part of what was asked.

## How to resume

1. Read this file.
2. `scripts/kb_query.py --list` to see everything stored.
3. `scripts/kb_query.py "<topic>"` for detail on any of it.

Keep this file current — it is the one thing that makes clearing context
safe. Update it at the end of any meaningful step, not just at session end.
