---
title: Reflection — sub-agent concurrency cap, Telegram plugin removal, file-size Q&A
summary: Two small user-requested changes (concurrency cap, Telegram removal) plus a trivial Q&A; only new finding is a CLI gotcha on scoped plugin uninstall, now in kb/knowledge/.
tags: [reflection, plugins, telegram]
updated: 2026-09-22
---

# Reflection — sub-agent concurrency cap, Telegram plugin removal, file-size Q&A

Covers the tasks since `kb/history/2026-09-22-researcher-runs-and-architect-agent.md`.

## What happened

1. User instruction: never run more than 2 sub-agents at once, queue the
   rest. Added the rule to `CLAUDE.md`'s "Creating sub-agents" section
   and saved it to personal cross-session memory
   (`feedback_subagent_concurrency_cap.md`) since it's a general
   orchestration preference, not just this repo.
2. User: "[telegram] works bad, seems useless" → removed the plugin.
   `claude plugin uninstall telegram` failed (plugin was project-scoped);
   `--scope project` was required. Also killed the still-running bot
   process and removed its stale pid file, and pruned the now-stale
   `kb/knowledge/telegram-plan-mode-approval.md`. Left the bot token/.env
   and access.json alone (outside the repo, not asked for), and left the
   inert `telegram:access`/`telegram:configure` skills and
   `deliver-research`'s Telegram references in place (not asked to
   remove, harmless while inert).
3. User: "how big are files that i can send you?" — answered directly
   from general knowledge, no research or code change needed.

## Skill-gap check

No recurring multi-step procedure surfaced. Both real tasks were
one-off, user-directed changes (a rule edit, a removal); the Q&A was
trivial. Nothing here repeats a pattern already worth packaging, and
nothing repeats a pattern seen before across sessions either.

## Process check

- No user corrections or missed conventions in this window.
- One genuine gotcha cost real effort to find: `claude plugin uninstall`
  needs the same `--scope` flag the plugin was installed with, or it
  fails. This is CLI behavior, not project-specific, so it went to
  `kb/knowledge/claude-plugin-uninstall-scope.md` rather than staying
  buried in a `CURRENT.md` session note.
- No memo written for either change — both are fully explained by their
  commit messages and the user's one-line request; nothing here counts
  as reasoning that would be lost if left to `git log`.

## Outcome

Nothing to package as a new skill or sub-agent this round. One knowledge
note added for the plugin-uninstall gotcha.
