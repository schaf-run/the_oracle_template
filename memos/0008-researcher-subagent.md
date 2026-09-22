---
title: "0008: Add a read-only `researcher` sub-agent with a per-task model policy"
summary: Created `.claude/agents/researcher.md`, scoped to Read/Grep/Glob/WebSearch/WebFetch, with a user-approved model-tiering policy instead of a fixed model.
tags: [agents, model-choice]
updated: 2026-09-22
---

# 0008: Add a read-only `researcher` sub-agent with a per-task model policy

Date: 2026-09-22

## Context

User asked (Telegram) for a reusable research sub-agent: reads local
files, searches the web, with the model chosen per task complexity but
approved by them. Meta-skill gap check found nothing existing covered
it — `general-purpose`/`Explore` aren't restricted to research, and the
built-in `deep-research` skill is a multi-agent orchestrator, not a
single invoke-by-name role.

## Decision

- New `.claude/agents/researcher.md`: `tools: Read, Grep, Glob,
  WebSearch, WebFetch` only — no `Edit`/`Write`/`Bash`/`Agent`. No fixed
  `model:` in frontmatter.
- Model tier is chosen at spawn time (via the `Agent` tool's `model`
  param) using a policy the user approved once rather than per call:
  Haiku for narrow single-source lookups, Sonnet as the default for
  typical multi-source research, Opus for deep/ambiguous/high-stakes
  synthesis, Fable only if explicitly requested.
- Surveyed skills/plugins/MCPs for this role and added none beyond the
  agent file itself: `deep-research` stays a separate, complementary
  tool used at the orchestrator level (not wired into `researcher`,
  which deliberately has no `Agent` tool); no MCP server was added since
  `WebSearch`/`WebFetch` already cover general web research and nothing
  in the project currently needs a narrower external data source.

## Why

- **Restricted tools, not `model` in frontmatter, is the actual
  justification** for a dedicated agent file (per
  `.claude/skills/create-subagent/SKILL.md` step 2) — the read-only
  scope is what a generic agent type can't guarantee.
- **Model belongs in the call, not the definition**, per
  `.claude/skills/choose-model/SKILL.md`: this role's tier genuinely
  varies per task, unlike a role that always wants the same override.
- **Approve the policy once, not every call** — asked the user directly
  (AskUserQuestion) rather than assuming; they chose the one-time
  sign-off over per-call confirmation, matching `choose-model`'s own
  anti-pattern warning against re-litigating the same choice on every
  loop iteration.
- **No MCP added speculatively** — follows the root `CLAUDE.md` MCP rule
  (add only when a task genuinely needs it); flagged specific future
  candidates (arXiv/PubMed, GitHub code search) rather than installing
  anything now.

## Consequences

Future research tasks should go through `Agent({ subagent_type:
"researcher", model: <tier per policy above>, ... })` rather than
`general-purpose`, when the task is read-only research. If a task needs
editing after research, that's two steps (research, then a separate
implementation agent/plan), not one call. Revisit the "no `kb` write
access" call if durable research findings start getting lost between
sessions — noted as a flagged-not-done option in
`/home/schaf_run/.claude/plans/cozy-growing-umbrella.md`.
