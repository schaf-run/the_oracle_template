---
title: "0006: Enforce meta-skill check before plan mode via hooks"
summary: A PreToolUse hook now hard-blocks EnterPlanMode unless meta-skill ran first, after the check was skipped twice relying on memory alone.
tags: [hooks, meta-skill, process]
updated: 2026-09-21
---

# 0006: Enforce meta-skill check before plan mode via hooks

Date: 2026-09-21

## Context

CLAUDE.md's "Big picture (before planning)" section says to run the
meta-skill orientation pass before planning non-trivial work — check
whether an existing skill or sub-agent already covers the task. This was
skipped twice across two separate reflection windows: once building the
reflection skill itself (flagged in `kb/history/2026-09-21-reflection.md`
as "worth doing explicitly going forward"), and again just now before
entering plan mode for the 3D-viewer app's Phase 1. Both times the
reasoning behind skipping it was sound in hindsight, but the check itself
never happened as an auditable step.

## Decision

Added two hooks:
- `scripts/meta_skill_track.py` (`PostToolUse`, matcher `Skill`): when the
  invoked skill is `meta-skill`, writes `.claude/meta_skill_state.json`
  with `{"checked": true}`.
- `scripts/meta_skill_guard.py` (`PreToolUse`, matcher `EnterPlanMode`):
  reads that marker. If not set, hard-blocks (`exit 2`) with a message
  pointing at `meta-skill/SKILL.md`. If set, allows the call through and
  resets the marker to `false` — so the check is required again before
  the *next* plan-mode entry, not just once per session.

`.claude/meta_skill_state.json` is gitignored, same treatment as
`reflection_state.json` — it's a runtime marker, not source of truth.

## Why

This is "must happen every time, mechanically, without depending on the
model remembering" — CLAUDE.md's own bar for reaching for a hook instead
of a rule. A written rule had already failed twice; a third reliance on
memory wasn't a reasonable bet. The PreToolUse block/allow contract
(`exit 2` to block, or `permissionDecision` JSON) was confirmed against
current Claude Code hook docs before implementation, then verified
end-to-end by piping test payloads through both scripts (block-with-no-
marker, track-sets-marker, guard-passes-and-resets, re-block-after-reset)
— same verification discipline as `checkpoint_guard.py` and
`reflection_guard.py` in memos 0003/0004.

Scoped to `EnterPlanMode` specifically rather than something broader
(e.g. every multi-file `Write`) because it's the one clean, explicit
trigger point CLAUDE.md itself names for the orientation pass, and
matches both prior misses exactly.

## Consequences

Every future plan-mode entry now requires an explicit, auditable
`meta-skill` invocation immediately beforehand (or at least since the
last plan-mode entry). If this proves too aggressive in practice (e.g.
legitimate cases where plan mode is re-entered rapidly for the same
task without a new orientation being useful), revisit by scoping the
reset to something coarser than every `EnterPlanMode` call. Related:
`memos/0003-stop-hook-checkpoint-guard.md`,
`memos/0004-reflection-skill-and-hook.md`.
