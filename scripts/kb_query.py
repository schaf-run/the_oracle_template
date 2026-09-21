#!/usr/bin/env python3
"""Search the kb index. Prints compact ranked hits: path:line, kind, heading, snippet."""

import argparse
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / ".claude" / "kb.db"
INDEXER = ROOT / "scripts" / "kb_index.py"

SEARCH = """
SELECT path, line, kind, title, heading, body,
       snippet(chunks, 5, '«', '»', '…', 14) AS snip,
       bm25(chunks) AS score
FROM chunks WHERE chunks MATCH ?
"""


KIND_RANK = """
CASE kind WHEN 'progress' THEN 0 WHEN 'knowledge' THEN 1 WHEN 'codemap' THEN 2
          WHEN 'docs' THEN 3 WHEN 'history' THEN 4 ELSE 5 END
"""


def terms(query):
    return [f'"{t}"' for t in query.replace('"', " ").split() if t]


def run_search(con, query, kind, limit):
    sql, params = SEARCH, [query]
    if kind:
        sql += " AND kind = ?"
        params.append(kind)
    sql += " ORDER BY score LIMIT ?"
    params.append(limit)
    return con.execute(sql, params).fetchall()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", nargs="*", help="FTS5 query; bare words are ANDed")
    ap.add_argument("--kind", help="knowledge | codemap | docs | history")
    ap.add_argument("-n", "--limit", type=int, default=5)
    ap.add_argument("--full", action="store_true", help="print whole matching section")
    ap.add_argument("--list", action="store_true", help="list every note, no search")
    args = ap.parse_args()

    subprocess.run(
        [sys.executable, str(INDEXER), "--if-stale", "--quiet"], check=False
    )
    if not DB.exists():
        print("kb: no index yet — add notes under kb/ first")
        return 1

    con = sqlite3.connect(DB)

    if args.list:
        sql = "SELECT DISTINCT kind, title, path FROM chunks"
        params = []
        if args.kind:
            sql += " WHERE kind = ?"
            params.append(args.kind)
        rows = con.execute(sql + f" ORDER BY {KIND_RANK}, path", params).fetchall()
        for kind, title, path in rows:
            print(f"{path}  [{kind}]  {title}")
        if not rows:
            print("kb: empty")
        return 0

    query = " ".join(args.query).strip()
    if not query:
        ap.error("give a query, or --list")

    words = terms(query)
    attempts = [query, " ".join(words), " OR ".join(words)]
    rows = []
    for attempt in attempts:
        if not attempt:
            continue
        try:
            rows = run_search(con, attempt, args.kind, args.limit)
        except sqlite3.OperationalError:
            continue
        if rows:
            break

    if not rows:
        print(f"kb: no match for {query!r}")
        return 1

    for path, line, kind, title, heading, body, snip, _ in rows:
        label = title if heading == title else f"{title} › {heading}"
        print(f"{path}:{line}  [{kind}]  {label}")
        print(("\n" + body if args.full else "    " + snip.replace("\n", " ")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
