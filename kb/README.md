# Knowledge base

Fast lookup store. Markdown files are the source of truth; `.claude/kb.db`
is a derived SQLite FTS5 index rebuilt automatically. Query it instead of
re-reading source files or re-exploring the codebase.

## Query

```sh
scripts/kb_query.py "token refresh"          # top 5 ranked sections
scripts/kb_query.py "deploy" --kind history  # scope to one kind
scripts/kb_query.py "db schema" --full       # print the whole section
scripts/kb_query.py --list                   # every note, one line each
```

Each hit prints `path:line`, kind, heading, and a snippet — open the file
only when the snippet isn't enough.

## Kinds

| Directory    | Holds                                                           |
|--------------|-----------------------------------------------------------------|
| `knowledge/` | Current-state facts: architecture, conventions, invariants, gotchas |
| `codemap/`   | Where things live: module responsibilities, entry points, ownership |
| `docs/`      | Distilled notes from external API/library docs worth not re-fetching |
| `history/`   | What was tried and how it turned out, so dead ends aren't re-walked |

## Writing notes

Start from `TEMPLATE.md`. Keep notes atomic — one topic per file, and
tight `##` sections, because each section is indexed and returned
independently. A hit should be readable without the rest of the file.

`INDEX.md` is generated. Don't hand-edit it.

## Versus `memos/`

- `memos/` — decisions and their reasoning, chronological, append-only.
  A memo is a historical record and stays true even when the code moves on.
- `kb/` — what is true *now*. Rewrite and prune freely; stale entries are
  worse than missing ones.
