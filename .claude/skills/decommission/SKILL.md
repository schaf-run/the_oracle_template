---
name: decommission
description: Remove a feature, integration, or experiment from the project and sweep kb/, memos/, skills, agents, CLAUDE.md, and settings for now-stale references. Use when a plugin, app, or subsystem is being torn out — not for routine file deletion or a single stale note.
---

# Decommissioning a feature or integration

Codifies what's been done ad hoc three times now (a 3D-model app, a
Telegram plugin, and the follow-up prune that produced memo 0011): tear
out the subject's own files, then sweep everything else that might still
reference it, without either leaving stale references behind or
silently losing a durable finding along the way.

## Process

1. **Confirm the subject and its footprint.** Name it precisely — code
   dirs, config entries, plugin/package names, env vars. If the
   footprint isn't already obvious from the user's request, ask rather
   than guessing scope.
2. **Remove the subject's own files/config first.** This is the primary
   deletion — the app's code, the plugin's config entry, whatever makes
   the subject actually gone from the running project.
3. **Sweep for references.** Search `kb/knowledge/`, `kb/history/`,
   `kb/codemap/`, `kb/docs/`, `memos/`, `.claude/skills/`,
   `.claude/agents/`, `CLAUDE.md`, and `.claude/settings.json` for the
   subject's name and aliases.
   - More than a handful of files to check → delegate to the `auditor`
     sub-agent (`.claude/agents/auditor.md`) so the grep-and-read pass
     doesn't consume main-thread context.
   - A small, already-known set → do it directly with `Grep`/`Glob`.
4. **Classify each hit** (this is the judgment call `auditor` can flag
   but not make on its own — decide it here):
   - *Purely about the subject, nothing else durable* → delete the file
     or the section.
   - *Subject is only incidental context, rest is unrelated and durable*
     → leave the file as is.
   - *Has a durable finding not captured anywhere else* → migrate it
     into `kb/knowledge/` (a fact/convention/gotcha) or a new memo (a
     decision) **before** deleting the source it came from.
5. **Fix dangling cross-references** left behind by anything deleted in
   step 4 — pointer chains like "covers the tasks since X.md",
   `[[wikilinks]]`, entries in `kb/INDEX.md`. A broken link is worse than
   the stale note it replaced.
6. **Regenerate the index:** `scripts/kb_index.py`.
7. **Checkpoint `kb/progress/CURRENT.md`** — what was removed, what was
   kept and why, what was migrated and to where.
8. **Write a memo** if the sweep involved a real judgment call or
   reversed a prior convention (see `memos/0011-history-notes-can-be-
   removed-for-dead-subjects.md` as the worked example — it documents
   exactly this kind of call).

## Anti-patterns

- Blanket-deleting every file that mentions the subject without checking
  for durable content mixed in — a history note or memo can be *about*
  something else entirely and only mention the removed subject in
  passing.
- Skipping the reindex after deleting or adding notes — leaves
  `kb/INDEX.md` and search results pointing at nothing.
- Leaving a cross-reference pointing at a file that no longer exists.
- Treating "the subject is gone from the code" as the whole task — the
  sweep through `kb/`/`memos/`/skills/agents is not optional cleanup,
  it's the second half of the same job.
