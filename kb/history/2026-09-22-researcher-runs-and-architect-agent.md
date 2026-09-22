---
title: Reflection — two researcher runs, architect sub-agent, plan-mode/Telegram refinement
summary: Ran researcher twice with an identical condense-and-deliver pattern (now a skill), built the architect sub-agent with a tool-scope correction from the user, and found plan mode blocks the Telegram reply tool outright.
tags: [reflection, agents, telegram, skills]
updated: 2026-09-22
---

# Reflection — two researcher runs, architect sub-agent, plan-mode/Telegram refinement

Covers the tasks since `kb/history/2026-09-22-researcher-agent-commit-and-remote-control.md`.

## What happened

1. User: "send some researcher to check for proofed online business
   models that run mostly with AI" → spawned `researcher` (Sonnet, per
   the approved tiering policy), condensed the report into a scratchpad
   file + short Telegram summary with sources attached.
2. User: asked for a second research run — zero-budget marketing
   channels for a software agency, noting Claude can automate routines →
   same pattern: spawn, condense, attach full doc.
3. User: "let's create a new sub-agent type... call him architect" with
   a specific two-phase invocation protocol (big picture first, detail
   only per section, limited output) → meta-skill gap check (built-in
   `Plan` type is close but lacks the staged-disclosure discipline) →
   plan mode → user corrected the tool-scope reasoning mid-plan (add
   `Bash`/web, not exclude them) → discovered a plan-mode edge case
   (detail folded into
   `kb/history/2026-09-22-telegram-plugin-saga-closed.md`, since it
   surfaced via the Telegram channel plugin) → approved → created
   `.claude/agents/architect.md` + `memos/0009-architect-subagent.md`,
   committed as 3 commits.
4. This reflection.

## Skill-gap check

Real, recurring gap found: tasks 1 and 2 both followed the exact same
procedure — spawn `researcher`, write the full report to a scratchpad
markdown file, condense into a short sourced summary, send over
Telegram with the file attached. Two occurrences meets this repo's own
bar ("used more than once") from `.claude/skills/README.md`. Created
`.claude/skills/deliver-research/SKILL.md` and added it to the skills
README rather than just noting the pattern.

## Process check

- Design correction handled well: when the user overrode the initial
  `architect` tool-scope reasoning (add `Bash`/web instead of excluding
  them), the plan file was updated in place with the reasoning change
  made explicit rather than silently swapped — this is worth keeping as
  the default response to a mid-plan correction.
- Real friction found and resolved via `AskUserQuestion` — detail (a
  general lesson about plan mode blocking every non-readonly tool,
  including a channel's reply tool) consolidated into
  `kb/history/2026-09-22-telegram-plugin-saga-closed.md` since it
  surfaced through the now-removed Telegram plugin.

## Outcome

New skill: `deliver-research`. No CLAUDE.md change. Two agent files now
exist (`researcher`, `architect`); no further gap surfaced.
