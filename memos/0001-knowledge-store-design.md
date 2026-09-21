---
title: "0001: Knowledge store backed by markdown plus a derived FTS index"
summary: Why kb/ is markdown source-of-truth with a disposable SQLite FTS5 index, chunked per section.
tags: [kb, storage, context]
updated: 2026-09-21
---

# 0001: Knowledge store backed by markdown plus a derived FTS index

Date: 2026-09-21

## Context

The agent needs to recall project knowledge without burning context.
Re-reading source files or re-exploring a codebase each session costs
thousands of tokens for facts that were already established.

## Decision

`kb/` holds atomic markdown notes and is the source of truth.
`scripts/kb_index.py` derives a SQLite FTS5 index at `.claude/kb.db`;
`scripts/kb_query.py` searches it. The `.db` is gitignored and
disposable. `memos/` is indexed into the same table so there is exactly
one place to search.

Notes are chunked per `##` heading, not per file, and hits carry
`path:line`.

## Why

- **Markdown as truth, DB as derived** — keeps knowledge human-readable
  and git-diffable, and means a corrupt or missing index is never data
  loss. Rejected pure SQLite for this reason.
- **Not grep-only** — grep has no ranking and returns whole files. BM25
  ranking plus snippets is the difference between a 200-token answer and
  a 3000-token one. Rejected a plain `kb/` + `INDEX.md` for that.
- **Section-level chunking** — the unit of retrieval should be the unit
  of meaning. Returning a whole file re-imports the pollution the store
  exists to avoid.
- **Staleness handled twice** — a `PostToolUse` hook rebuilds after
  edits, and `kb_query.py` rebuilds if the index is older than its
  sources. The hook is an optimization, not a dependency, so the store
  still works in environments where hooks don't load.

## Consequences

Notes must stay atomic with self-contained `##` sections, or retrieval
quality degrades. `kb/INDEX.md` is generated and must not be hand-edited.
Python 3 with stdlib `sqlite3` is now a soft dependency of the template.

Supersedes nothing. See `0002-big-picture-before-planning.md` for the
orientation step that consumes this store.
