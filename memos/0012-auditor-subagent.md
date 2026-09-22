---
title: "0012: Add a read-only `auditor` sub-agent for repo-wide relevance sweeps"
summary: Created `.claude/agents/auditor.md`, scoped to Read/Grep/Glob/Bash (inspection only), to run the sweep step of a decommission without burning main-thread context.
tags: [agents, decommission]
updated: 2026-09-22
---

# 0012: Add a read-only `auditor` sub-agent for repo-wide relevance sweeps

Date: 2026-09-22

## Context

The manual cleanup that produced memo 0011 (pruning `kb/history/` notes
about the removed Telegram plugin and 3D-model app) required grepping and
reading most of the repo directly in the main session to find every
reference and judge whether it was stale, durable-elsewhere, or
durable-but-uncaptured. The user then explicitly asked for this to become
a repeatable sub-agent, to keep that grep-and-read sweep off the main
thread. Meta-skill gap check (this session) confirmed no existing
built-in type or `.claude/agents/*.md` covers "read-only, repo-wide,
classify each hit" — `researcher` is open-ended external research,
`architect` plans implementation.

## Decision

New `.claude/agents/auditor.md`: `tools: Read, Grep, Glob, Bash` (`Bash`
explicitly inspection-only — `git log`/`git grep`/`git show`, never a
mutating command), no `Edit`/`Write`/`Agent`. No fixed `model:` in
frontmatter, matching `researcher`'s per-call tiering approach (memo
0008) rather than baking in a tier.

Its output contract: for each hit, one of four classifications (stale/
removable, durable-elsewhere-already, durable-not-yet-captured with a
migration recommendation, or incidental-mention-leave-alone) — the same
triage this session did by hand for memo 0011's three removed files.

## Why

Restricted tool scope is the actual justification (per
`.claude/skills/create-subagent/SKILL.md` step 2): the value is
guaranteeing the sweep can't accidentally mutate anything while covering
the whole repo, not a different model tier. Deliberately excludes
judging *whether* the subject should be removed — that decision belongs
to the caller (or `decommission`, memo 0013) — `auditor` only reports
what's left behind and how it classifies.

## Consequences

`decommission` (memo 0013) delegates its sweep step to this agent when
there's more than a handful of files to check. If a repo's `kb/`/`memos/`
grow large enough that even `auditor`'s own read/grep pass gets
expensive, revisit scoping the search (e.g. restrict to a subdirectory)
rather than widening its tools.
