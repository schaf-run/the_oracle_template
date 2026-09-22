---
title: "0013: Add a `decommission` skill for removing features/integrations"
summary: Created `.claude/skills/decommission/SKILL.md`, codifying the remove-then-sweep procedure used ad hoc three times (3D-app removal, Telegram removal, the memo-0011 history prune).
tags: [skills, decommission]
updated: 2026-09-22
---

# 0013: Add a `decommission` skill for removing features/integrations

Date: 2026-09-22

## Context

Three separate sessions did the same two-part job by hand: tear out a
feature's own files, then separately sweep `kb/`/`memos/`/skills/agents/
`CLAUDE.md` for now-stale references — once for the 3D-model app, once
for the Telegram plugin, and once more (memo 0011) for the history notes
that referenced both after the fact. Each time the sweep step was
re-derived from scratch rather than following a written procedure. The
user explicitly asked for this to become a skill after approving it as a
suggestion from the memo-0011 session.

## Decision

New `.claude/skills/decommission/SKILL.md`: an 8-step process (confirm
footprint → remove the subject's own files → sweep for references,
delegating to the `auditor` sub-agent (memo 0012) when the sweep is
large → classify each hit as removable / incidental / durable-needs-
migration → fix dangling cross-references → reindex → checkpoint
`CURRENT.md` → write a memo if a real judgment call was made). Added to
`.claude/skills/README.md`'s list.

## Why

Meets this repo's own "used more than once" bar for a skill (three prior
occurrences, all following the same shape) — this isn't speculative
packaging, it's writing down a pattern that already repeated. Delegating
the sweep step to `auditor` rather than folding grep/read logic into the
skill itself keeps the skill a *procedure* (what order to do things in,
what to classify hits as) rather than a tool implementation — matching
`kb/SKILL.md`'s own separation of "what to search with" from "how to
decide what's durable."

## Consequences

The next feature/integration removal should invoke this skill rather
than re-deriving the sweep from memory. If a decommission surfaces a
judgment call this process doesn't cover (e.g. a subject with no clean
"footprint" boundary), that's a gap to fold back into the skill, not a
one-off improvisation to repeat silently next time.
