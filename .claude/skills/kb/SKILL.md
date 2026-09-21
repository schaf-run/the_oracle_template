---
name: kb
description: Query the project knowledge base before exploring the codebase, re-reading source files, or re-fetching external docs — and write findings and progress back to it. Use at the start of a task or after a context clear to recall state, and whenever you learn something durable worth not rediscovering.
---

# Knowledge base

`kb/` and `memos/` hold markdown notes; `.claude/kb.db` is a derived
SQLite FTS5 index over both, chunked per `##` section. Searching costs a
few hundred tokens; re-exploring a codebase costs thousands. Search first.

**After a context clear, start here:** read `kb/progress/CURRENT.md`, then
`scripts/kb_query.py --list`. That is the full state; don't rebuild it by
re-reading source.

## Read

```sh
scripts/kb_query.py "token refresh"          # top 5 ranked sections
scripts/kb_query.py "deploy" --kind history  # knowledge | codemap | docs | history
scripts/kb_query.py "db schema" --full       # whole section, not a snippet
scripts/kb_query.py --list                   # every note, one line each
```

Hits print `path:line`, kind, heading, and a snippet. Open the file only
when the snippet isn't enough — that's the whole point of the store.

Do this **before** grepping the codebase for orientation, before
re-reading large files you've read in a past session, and before fetching
an external doc page again.

## Write

Add a note when you learn something durable that cost effort to find and
isn't obvious from a quick read of the code:

| Kind         | Write here when you learned…                                 |
|--------------|--------------------------------------------------------------|
| `progress/`  | state changed — update `CURRENT.md` after every meaningful step |
| `knowledge/` | an architectural fact, convention, invariant, or gotcha       |
| `codemap/`   | where something lives / which module owns what                |
| `docs/`      | the distilled answer from an external API or library doc      |
| `history/`   | what was tried and how it turned out, especially a dead end   |
| `../memos/`  | a decision was made — append-only, with its rejected alternatives |

Checkpoint `kb/progress/CURRENT.md` as you go, not at session end. A
context clear can happen at any time, and it is only safe if that file is
already current.

Rules:

- Start from `kb/TEMPLATE.md`. Frontmatter needs `title` and `summary`;
  the summary is what appears in the generated index.
- One topic per file. Keep `##` sections tight and self-contained — each
  is retrieved on its own and must read standalone.
- Rewrite and prune freely. `kb/` describes what's true *now*; a stale
  note is worse than a missing one. (Durable decision records go in
  `memos/` instead, which is append-only.)
- Never hand-edit `kb/INDEX.md` — it's generated.

## Index maintenance

Rebuilds happen automatically: a `PostToolUse` hook runs the indexer after
edits, and `kb_query.py` rebuilds if it notices the index is stale. Force
one with `scripts/kb_index.py`. The `.db` is gitignored and disposable —
only the markdown is source of truth.
