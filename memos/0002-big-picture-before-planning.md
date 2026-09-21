---
title: "0002: Big-picture orientation runs before planning"
summary: Why a meta-skill gap check and a kb query precede planning instead of being decided ad hoc.
tags: [skills, planning, meta-skill]
updated: 2026-09-21
---

# 0002: Big-picture orientation runs before planning

Date: 2026-09-21

## Context

Without an explicit orientation step, an agent starts planning from a cold
read of the task: it re-explores ground already covered, and it decides
whether to build a skill mid-task, when it is least able to judge reuse.

## Decision

`CLAUDE.md` defines a **Big picture** phase that runs before Planning:

1. Query the knowledge base for what is already known.
2. Run `.claude/skills/meta-skill/SKILL.md` — a gap check that scans
   available skills, project skills, and sub-agents, then decides: reuse a
   match, defer a one-off, or create a skill for a genuine recurring gap.

## Why

- **Skill-creation is a judgment call that deserves one owner.** Made
  ad hoc mid-task it produces either duplicates or nothing. Concentrating
  it in one triage step makes the rule auditable.
- **Recall before exploration.** Querying the store first is what makes
  the store worth maintaining; otherwise notes get written and never read.
- **Triage, not design.** The step is deliberately scoped to "what tool do
  I reach for", so it cannot grow into a second planning phase.

## Consequences

Every non-trivial task pays a small fixed cost up front. Trivial one-off
asks are explicitly exempt, or the overhead would outweigh the benefit.

Depends on `0001-knowledge-store-design.md`.
