---
name: choose-model
description: Pick which Claude model tier (Haiku, Sonnet, Opus, Fable) and reasoning effort to use for a task — the session itself, a one-off sub-agent spawned via the Agent tool, or a reusable agent's `model:` frontmatter. Use before spawning a sub-agent with a non-default model, when writing the `model:` field of a `.claude/agents/<name>.md` file, when the user asks which model to use, or before a loop/batch job where the choice compounds cost.
---

# Choosing a model level

A cost/quality dial, not a design decision — decide fast and move on.

## Default

Sonnet, unless one of the triggers below applies. It's the balanced
choice for most coding and reasoning work; don't special-case a task just
because you can.

## When to move off the default

- **Down to Haiku** — the task is mechanical, narrow, and high-volume:
  a fixed lookup, a grep-and-report pass, formatting/boilerplate, a
  sub-agent step with little ambiguity. Cost and speed matter more than
  nuance here.
- **Up to Opus** — the task needs deep or ambiguous reasoning:
  architecture tradeoffs, a subtle or high-stakes bug, a security-
  sensitive change, cross-cutting design judgment — or a Sonnet attempt
  already came back shallow or wrong on this specific problem.
- **Fable** — only when the user or task explicitly calls for it; don't
  reach for it speculatively.

Reasoning **effort** (`low`/`medium`/`high`/`xhigh`/`max`, where it's
exposed — e.g. a review tool's level, or an agent's `effort:` frontmatter)
is a separate dial from model choice. Prefer bumping effort on a single
hard step over upgrading the model everywhere; it's the cheaper lever.

## Where to apply it

- **A one-off sub-agent spawned this turn** — pass `model` to the Agent
  tool call: `"haiku" | "sonnet" | "opus" | "fable"`.
- **A reusable custom agent** — set `model:` in the
  `.claude/agents/<name>.md` frontmatter (same values, plus a full model
  ID or `inherit` to track whatever the caller is using). See
  [[create-subagent]].
- **The current session** — use the session's own model control (the
  model-selection UI, or `/model` in an interactive terminal session)
  rather than editing a file.

## Anti-patterns

- Upgrading to Opus by default "to be safe" — pay for it only when the
  task actually needs the extra reasoning.
- Choosing a model per sub-agent call without a reason — if every call in
  a loop needs the same override, put it on the agent definition instead
  so the choice isn't re-litigated each time.
- Treating effort and model choice as the same lever — check whether
  bumping effort alone solves the problem before reaching for a bigger
  model.
