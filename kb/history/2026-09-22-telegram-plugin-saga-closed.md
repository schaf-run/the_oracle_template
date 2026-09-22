---
title: Telegram plugin — full saga, closed out
summary: The Telegram channel plugin's whole lifecycle (enabled, Q&A, plan-mode friction, removal) consolidated from 5 fragmented reflection notes now that the plugin is fully gone.
tags: [history, telegram, plugins, closed]
updated: 2026-09-22
---

# Telegram plugin — full saga, closed out

The Telegram channel plugin no longer exists in this repo (removed
`2249f0c`). This note consolidates everything about it that was
previously scattered across 5 separate reflection notes, per the
`history/` saga-compaction convention in `CLAUDE.md`. Each source note's
non-Telegram content was left in place — only the Telegram-specific
material was pulled here. Original notes, for anyone tracing the exact
session-by-session sequence:
`2026-09-22-concurrency-cap-and-telegram-removal.md`,
`2026-09-22-telegram-qa-and-concurrent-current-md-edit.md`,
`2026-09-22-researcher-agent-commit-and-remote-control.md`,
`2026-09-22-researcher-runs-and-architect-agent.md`.

## Timeline

1. Plugin enabled (project scope).
2. Routine capability Q&A over the channel: confirmed file send/receive
   worked; explained the Bot API's 20MB-download/50MB-upload caps when
   asked whether the cap could be raised — answered that it's a platform
   limit, not a plugin setting, and raising it meant self-hosting the Bot
   API server (this fact later became the seed of the Telegram MCP
   connector design in
   `2026-09-22-oracle-test-branch-and-telegram-mcp-planning.md`, a
   separate, still-open note — not part of this closed saga).
3. Building the `architect` sub-agent surfaced a real plan-mode edge
   case: `EnterPlanMode` blocks *all* non-readonly tools, which turned
   out to include the Telegram `reply` tool itself, not just
   `ExitPlanMode`'s own approval UI. `AskUserQuestion` was the only
   channel that still reached the user over Telegram while planning —
   used successfully twice. This general lesson (plan mode blocks every
   non-readonly tool including a channel's reply tool; `AskUserQuestion`
   is the one exception) outlives the plugin and would apply to any
   future channel integration, not just Telegram.
4. The Telegram/plan-mode convention above was initially saved only to
   personal cross-session memory (outside the repo). Recognized as a
   project convention, not a personal preference, and mirrored into
   `kb/knowledge/telegram-plan-mode-approval.md` so it would travel with
   the repo — that note was later pruned as stale once the plugin was
   removed (step 6).
5. User: "[telegram] works bad, seems useless" → plugin removed.
6. Removal mechanics: `claude plugin uninstall telegram` (no scope flag)
   failed — the plugin was project-scoped, and uninstall needs the same
   `--scope` flag install used. `claude plugin uninstall telegram --scope
   project` worked, clearing `enabledPlugins` in `.claude/settings.json`
   and the plugin's entry in `~/.claude/plugins/installed_plugins.json`.
   Also killed the still-running bot process and its stale pid file.
   Left the bot token/`.env` and `access.json` alone (outside the repo,
   not asked for). This gotcha is general CLI behavior, not
   Telegram-specific, so it lives on in
   `kb/knowledge/claude-plugin-uninstall-scope.md` rather than only here.
7. Pruned `kb/knowledge/telegram-plan-mode-approval.md` (now stale) after
   removal.

## What was deliberately left in place

The `telegram:access`/`telegram:configure` skills and the
`deliver-research` skill's Telegram references still exist — inert
without the plugin, not part of what was asked to remove, so left alone.
`kb/knowledge/claude-plugin-uninstall-scope.md` stays as a live reference
(the gotcha is general, not plugin-specific). The plan-mode/reply-tool
lesson in item 3 above is preserved here since it outlives the plugin
itself.

## Outcome

Saga fully closed. No further Telegram-plugin work expected; the
Telegram MCP connector (separate, still-open design) is a different,
unrelated effort that happens to share a name.
