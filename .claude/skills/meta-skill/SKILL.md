---
name: meta-skill
description: Run at the start of any non-trivial task, before planning, to check whether an existing skill or sub-agent already covers the work and to decide whether a new reusable skill is worth creating. Also use when the user asks whether a skill exists for something, mentions "meta-skill", or asks you to create a skill.
---

# Meta-skill: skill gap check

A fast triage pass, not a design phase. Purpose: don't rebuild what
already exists, and don't miss a real, recurring gap.

## Process

1. Restate the task in one line.
2. Scan for a match, in this order:
   - The available-skills listing already in context (project + built-in
     skills) — check for a trigger description that fits.
   - `.claude/skills/*/SKILL.md` in this repo, in case a project-specific
     skill exists but wasn't surfaced.
   - `.claude/agents/*.md` for a sub-agent already scoped for this kind of
     work.
3. **Match found** — use it. Don't recreate it under a new name.
4. **No match** — ask: will this workflow recur, in this project or a
   future one? (See the "Skills" rule in the root `CLAUDE.md`: one-off
   work doesn't earn a skill.)
   - **Yes, worth building now** — create it:
     - Prefer invoking the `skill-creator` skill if it's available in
       this environment; it knows the authoring format and can validate
       triggering.
     - Otherwise hand-author `.claude/skills/<name>/SKILL.md`, following
       `.claude/skills/README.md`.
   - **Maybe, but not now** — proceed without creating one; if it's
     likely to matter later, note the gap in a memo (see `memos/`) rather
     than building it speculatively.
   - **No** — proceed straight to planning/execution.
5. State the decision in one line before moving on: which skill/agent
   you're using, or that none fit and why, or what you're creating.

## Enforcement

`scripts/meta_skill_guard.py` (`PreToolUse`, memo 0006 + memo 0014)
hard-blocks not just `EnterPlanMode` but also the *second* distinct file
touched via `Write`/`Edit`, and a handful of bulk-mutating `Bash`
patterns (`git rm`, `git mv`, `rm -r`/`-rf`/`-fr`, `find -delete`) —
unless a meta-skill check or a plan-mode pass already happened this
turn. A single-file change never trips it. This closes the gap where a
multi-file task could skip `EnterPlanMode` entirely and never trigger
the check at all (see `kb/knowledge/plan-mode-skip-blind-spot.md`).

## Anti-patterns

- Creating a skill "just in case" — that's scope creep, not orientation.
- Skipping the scan and duplicating an existing skill under a new name.
- Letting this step become the plan itself — it decides *what tool to
  reach for*, not *how to do the task*.
