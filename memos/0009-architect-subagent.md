---
title: "0009: Add an `architect` sub-agent with a two-phase plan-disclosure protocol"
summary: New .claude/agents/architect.md — plans only, no execution — with a hard-enforced big-picture-first / detail-on-request protocol, and an orchestrator-side rule to reuse the same agent instance for follow-up detail.
tags: [agents, planning]
updated: 2026-09-22
---

# 0009: Add an `architect` sub-agent with a two-phase plan-disclosure protocol

Date: 2026-09-22

## Context

User asked (Telegram) for a dedicated planning sub-agent, with an
explicit invocation rule: never request a fully-detailed plan up front.
Get a high-level plan first, let the user review it, then request detail
one section at a time as work actually proceeds. Meta-skill gap check
found the built-in `Plan` agent type covers "design an implementation
plan" but has no such staged-disclosure discipline and isn't a
persistent named role invokable outside formal plan mode.

## Decision

- New `.claude/agents/architect.md`: `tools: Read, Grep, Glob, Bash,
  WebSearch, WebFetch` — no `Edit`/`Write`/`Agent`. The two-phase
  protocol (high-level first; detail only on a named-section request;
  hard refusal if asked to dump the whole plan detailed in one shot) is
  written directly into its system prompt.
- Orchestrator-side convention (mine to follow, not the agent's):
  spawn `architect` for the big picture, send that to the user for
  review, then continue the **same agent instance** via `SendMessage`
  (not a fresh spawn) for each section's detail as the user is ready for
  it — so context (the big-picture plan) persists across the
  section-detail calls instead of being re-derived each time.

## Why

- **Tool scope changed mid-design.** First draft excluded `Bash`/web
  tools, reading "not to gather information" as "no research access at
  all." User corrected this directly: architect needs `Bash` for repo
  exploration beyond file reads (tests, git history) and web access for
  scoped lookups (library APIs) while designing — routing every small
  lookup through `researcher` would be needless overhead. Net effect:
  `architect`'s tool scope ended up nearly identical to the built-in
  `Plan` type's. The actual justification for a dedicated agent shifted
  from "restricted tools" to "restricted, enforced behavior" — the
  two-phase protocol and output-length discipline, which the built-in
  type doesn't have and would otherwise need re-explaining on every call.
- **`Bash` without `Edit`/`Write` is an accepted pattern here already** —
  matches the read-only-reviewer stub in `.claude/agents/README.md`,
  which grants `Bash` to a non-editing role and enforces "don't mutate
  anything" at the prompt level since the tool itself can't be
  perfectly sandboxed to read-only use.
- **Same-instance continuation, not fresh spawns per section** — keeps
  the big-picture plan in the agent's own context so section-detail
  requests don't need to re-explain the whole plan each time, and keeps
  each individual call's output naturally scoped to just that section.

## Consequences

Going forward, coding tasks that need a plan should generally go through
`architect` (big picture → user review → per-section detail) rather than
the built-in `Plan` type, when the two-phase discipline matters — e.g.
anything non-trivial enough that dumping a full detailed plan at once
would be more than the user wants to review in one pass. See
`.claude/agents/architect.md` for the enforced protocol and
`/home/schaf_run/.claude/plans/cozy-growing-umbrella.md` for the full
design discussion (tool-scope reasoning, verification steps).
