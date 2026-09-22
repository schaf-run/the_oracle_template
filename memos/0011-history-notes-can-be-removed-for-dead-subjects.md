---
title: "0011: kb/history notes can be removed once their subject is fully gone"
summary: User asked to purge history notes about the removed Telegram plugin and 3D app; this overrides the prior stance of always keeping history/ as an immutable log.
tags: [kb, history, telegram, process]
updated: 2026-09-22
---

# 0011: kb/history notes can be removed once their subject is fully gone

Date: 2026-09-22

## Context

A prior session, when removing the Telegram plugin, deliberately "kept
the `history/` entries since those are logs of what happened, not
current-state claims" (see `kb/progress/CURRENT.md`'s "Session note
(2026-09-22, later)"). That treated `kb/history/` as append-only —
distinct from `kb/knowledge/`, which is pruned aggressively because it
makes current-state claims.

The user then explicitly asked to audit the project and "remove all
irrelevant history files (related to telegram and 3d-model things)."

## Decision

Removed three `kb/history/` notes whose core subject was the Telegram
plugin or the removed 3D-model app:
`2026-09-22-concurrency-cap-and-telegram-removal.md`,
`2026-09-22-remote-branch-and-app-removal.md`, and
`2026-09-22-telegram-qa-and-concurrent-current-md-edit.md`. Kept four
others where Telegram/the app were only incidental context (e.g. "the
user asked via Telegram") rather than the substance of the note.

Before deleting, checked each removed note for durable findings not
captured elsewhere:
- Concurrency cap and plugin-uninstall gotcha were already fully
  recorded (`CLAUDE.md`/personal memory, `kb/knowledge/claude-plugin-
  uninstall-scope.md`) — nothing lost.
- The 3D-app removal itself was already summarized in `CURRENT.md`.
- One real, not-yet-elsewhere finding — `meta_skill_guard.py` not firing
  when `EnterPlanMode` is skipped entirely, not just under-checked —
  was migrated to `kb/knowledge/plan-mode-skip-blind-spot.md` first.
- One risk with no migration target (concurrent `CURRENT.md` edits, one
  occurrence, no fix proposed) was folded into a line in `CURRENT.md`'s
  reflection summary instead of a dedicated file, since it's a watch
  item rather than a standing convention.

## Why

A direct, explicit user instruction to remove specific files is a
stronger signal than a previous session's own internal policy choice —
the "keep history immutable" stance was this template's working default
absent a user request to the contrary, not a hard rule the user can't
override. The mitigation was to verify nothing durable was silently
lost, not to refuse the request.

## Consequences

`kb/history/` is not strictly append-only going forward: a file whose
entire subject has been removed from the project, at explicit user
request, can be deleted rather than kept as dead-subject archaeology —
provided any findings that don't live elsewhere are migrated first. This
doesn't change the default (still keep history/ as a log; don't prune it
speculatively) — it only documents that the default yields to an
explicit ask, and shows the check to run before deleting. Related:
`kb/knowledge/plan-mode-skip-blind-spot.md`,
`kb/knowledge/claude-plugin-uninstall-scope.md`.
