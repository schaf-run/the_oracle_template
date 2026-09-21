# Memos

Git-tracked decision/context log. One file per decision or incident,
numbered sequentially: `0001-short-title.md`, `0002-short-title.md`, ...

Start each new memo from `TEMPLATE.md` — the frontmatter `title` and
`summary` are what appear in search results and in `kb/INDEX.md`.

Memos are indexed alongside `kb/` under kind `memos`, so
`scripts/kb_query.py "<topic>" --kind memos` searches them. See the
"Memos" section of the root `CLAUDE.md` for what belongs here versus in
`kb/`.
