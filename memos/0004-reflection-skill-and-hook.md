---
title: "0004: Reflection skill fires from a Stop-event counter, not a real task count"
summary: A Stop hook counts completed turns as a proxy for "tasks" and nudges a retrospective skill every 5th one.
tags: [hooks, skills, continuity]
updated: 2026-09-21
---

# 0004: Reflection skill fires from a Stop-event counter, not a real task count

Date: 2026-09-21

## Context

The user asked for a `reflection` skill triggered by a hook "after each 5
tasks," to review recent work for skill gaps and process improvements.
Claude Code's hook events don't include a "task completed" event —
`PreToolUse`/`PostToolUse` fire per tool call, `Stop` fires once per
turn. "Task" needed a concrete mapping to something a hook can actually
observe.

## Decision

`scripts/reflection_guard.py` runs as a second command in the existing
`Stop` hook entry (alongside `checkpoint_guard.py`). It treats one Stop
event as one task, keeps a count in `.claude/reflection_state.json`, and
on the 5th, resets to 0 and returns `{"decision": "block"}` with a
reason pointing at `.claude/skills/reflection/SKILL.md`. The skill itself
does the actual analysis (from conversation context, `git log`, and
`kb/history/`) and writes findings back to `kb/history/`.

## Why

- **Stop event ≈ task** — it's the only hook boundary that roughly
  matches "one user request handled," which is what "task" means in
  ordinary use. Not exact (a single turn can bundle multiple asks, or a
  multi-turn back-and-forth can be one logical task), but it's the
  closest observable proxy and needs no new bookkeeping from the agent.
- **Shared `stop_hook_active` check** — this flag is set for *any*
  blocked-then-retried Stop in the session, not just the hook that
  blocked it. `reflection_guard.py` skips counting and blocking whenever
  it's set, the same way `checkpoint_guard.py` does (see
  `0003-stop-hook-checkpoint-guard.md`). This is what stops the two
  hooks from fighting: if `checkpoint_guard.py` blocks on the same turn
  the counter hits 5, both reasons surface together, and the retry Stop
  (where both flags are already true) lets everything through instead of
  looping.
- **Counter reset happens before the block, not after** — if the block
  message is somehow never acted on, the count doesn't get stuck
  re-triggering every subsequent stop; worst case is one missed
  reflection window, not a jammed hook.
- **Gitignored state file** — `.claude/reflection_state.json` is derived
  runtime bookkeeping, not a decision or fact worth version-controlling,
  same treatment as `.claude/kb.db`. It also means the counter is
  per-checkout, not shared across machines — acceptable, since a missed
  or extra reflection pass is low stakes.
- **Analysis lives in the skill, not the hook** — the hook only counts
  and nudges; it has no access to conversation semantics. This mirrors
  `checkpoint_guard.py`, which detects staleness but leaves the actual
  writing to the agent.

## Consequences

Every 5th completed turn triggers one reflection nudge, whether or not
anything interesting happened — the skill is expected to say "nothing to
report" rather than force a note (see the skill's anti-patterns section).
A long multi-step task that spans many tool calls but one Stop event only
counts as one task, so the trigger is closer to "5 requests" than "5
units of work" — accepted as the honest tradeoff for using an event the
hook system actually exposes.

Depends on `0003-stop-hook-checkpoint-guard.md`.
