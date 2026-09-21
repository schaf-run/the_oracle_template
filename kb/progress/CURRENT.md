---
title: Current state
summary: Resume point — read this first after a context clear or at the start of a session.
tags: [progress, session, app]
updated: 2026-09-21
---

# Current state

`the_oracle_template` started as a reusable Claude Code project template (a
rules file plus scaffolding). As of this session, the user chose to build a
real application directly in this repo rather than copying the template
elsewhere first — see "3D model upload/viewer app" below for that work. The
template conventions (CLAUDE.md, kb/, memos/, skills, hooks) still apply and
govern how the app work is done.

## 3D model upload/viewer app (Phase 1 — vertical slice)

Product: upload a `.obj` file (up to 500MB) → get a shareable link →
open it (mostly on mobile) and rotate/zoom it in-browser. Overall
Phase 0–4 roadmap and status: `kb/progress/roadmap.md`. Detailed
scaffolding plan for this session's build (not repo-tracked): `/Users/
schaf.run/.claude/plans/sunny-waddling-lighthouse.md` — note its "Phase
1" bundles the roadmap's Phase 0+1+2, see `roadmap.md` for why.

Stack decided with the user: Express + TypeScript + Prisma/SQLite backend
(persistent server, not serverless — auth is planned later), local disk
storage for the MVP, Vite + React + Three.js (`OBJLoader` + `OrbitControls`)
frontend. Repo layout: `server/` and `client/` npm workspaces at root, run
together via `npm run dev` (root). Toolchain pinned via `.nvmrc` (20.19.0) —
**shell state does not persist between tool calls in this environment, so
every command needs `source ~/.nvm/nvm.sh && nvm use` prefixed, or it falls
back to a stale Homebrew npm 6.9.0 on PATH.**

Built and verified this session (steps 1–15 of the Phase 1 plan):
- `POST /api/models` (busboy streaming upload, `.obj`-only, 500MB cap
  enforced server-side, disk write to `server/storage/`), `GET
  /api/models/:id` (metadata), `GET /api/models/:id/file` (raw bytes for
  the viewer). All curl-verified: valid upload, non-.obj rejection (400),
  over-limit rejection (413) with no orphaned files, byte-identical
  round-trip, 404 on bogus id.
- Verified a ~48MB upload streams through without buffering issues
  (fast, no memory blowup).
- Client: `UploadPage` (form/progress/share-link, untested via real file
  picker — see gap below) and `ViewerPage` → `ModelViewer` →
  `useThreeScene` hook. Verified live in the built-in browser: model
  renders centered/framed, mouse-drag rotates, scroll-wheel zooms, no
  console errors, bogus-id shows clean "Model not found".
- Mobile emulation pass (375×812, drag-to-rotate) looked correct, but this
  is a mouse-driven proxy, not real touch/pinch — see gap below.
- Two real bugs found and fixed while building the upload handler (busboy
  `finish` firing before the write stream flushes; `fs.unlink` racing
  `fs.createWriteStream`'s async `open()`) — see
  `kb/knowledge/upload-streaming-gotchas.md`.
- Decision to defer Express serving the built client bundle until a deploy
  target is chosen — see `memos/0005-defer-static-client-serving.md`.
- `npm audit`: 2 moderate react-router advisories (open redirect / SSR
  hydration) that need a v6→v7 major bump to clear. Not fixed — flagged to
  the user, low exploitability here (no SSR, no links built from
  untrusted input, only two static routes).

### Known gaps (not yet done)
- Resolved: upload-through-the-actual-file-picker gap — the user tried it
  live (found as two `26.122.obj` / ~68MB records in the dev DB, not from
  my own curl testing). Confirms the real file-picker → progress → link
  path works end-to-end, not just the API layer.
- **No real mobile device / real touch (pinch) testing** — only
  mouse-driven viewport emulation. `touch-action: none` is set on the
  viewer canvas but its actual effect (blocking page-scroll hijack) is
  still unverified on a real phone.
- Dev servers were left running (`npm run dev` from root, ports
  3001/5173) for the user to try live.

## Reflection pass + meta-skill hook (this session, after Phase 1)

Triggered by `reflection_guard.py` after 5 tasks. Findings written to
`kb/history/2026-09-21-3d-viewer-phase1.md`. One real process gap
surfaced: the meta-skill pre-planning check had now been skipped twice
across two separate reflection windows (once building the reflection
skill, once before this session's Phase 1 plan-mode entry) — no longer
just a one-off. Fixed mechanically rather than re-noting it a third time:
- `scripts/meta_skill_track.py` (`PostToolUse` on `Skill`) sets a marker
  when `meta-skill` runs.
- `scripts/meta_skill_guard.py` (`PreToolUse` on `EnterPlanMode`)
  hard-blocks (`exit 2`) unless that marker is set, then resets it —
  required fresh before each plan-mode entry, not just once per session.
- Decision recorded in `memos/0006-enforce-meta-skill-before-plan-mode.md`.
- The `.claude/settings.json` edit needed explicit user sign-off (blocked
  by the auto-mode classifier as self-modification) — asked, got a yes,
  wired both hooks in, then verified the full block→track→allow→reset
  cycle by piping test payloads through both scripts before trusting it.
- Also captured `kb/knowledge/nvm-shell-state-per-bash-call.md` — a real
  friction point from Phase 1 (shell activation doesn't persist across
  Bash tool calls in this environment) that cost repeated re-discovery
  and is worth a query hit instead.

Also cleaned up storage/DB clutter from my own curl-based testing
(`sample.obj`/`big.obj` records) while deliberately leaving the user's
own `26.122.obj` test upload alone.

## Next: nothing committed yet

Everything above (app code, hooks, memos, kb notes) is written to disk
but **not yet committed** on branch `dev` — the user was asked whether to
commit as one commit or split by concern (app code / kb+memos / hook
infra) and hasn't answered yet. Do this first on resume if still
pending: check `git status`, confirm with the user if unclear, then
commit accordingly. Plan file (not repo-tracked, informational only) at
`/Users/schaf.run/.claude/plans/sunny-waddling-lighthouse.md`.

## Template itself (pre-existing, still valid)

Built and committed on branch `main`, pushed to
`git@github.com:schaf-run/the_oracle_template.git` (`origin/main`):

- `CLAUDE.md` — the agent rules: big picture, planning, executing,
  knowledge base, memos, skills, hooks, MCP servers, sub-agents.
- `.claude/skills/meta-skill/` — pre-planning gap check: reuse an existing
  skill/sub-agent, or create one if the gap is genuinely recurring.
- `.claude/skills/kb/` — how to query and write the knowledge store.
- `.claude/skills/choose-model/` — model tier (Haiku/Sonnet/Opus/Fable)
  and reasoning-effort picker; applies to sessions, one-off sub-agent
  spawns, and `.claude/agents/*.md` `model:` fields.
- `.claude/skills/create-subagent/` — process for authoring a new
  `.claude/agents/<name>.md`: justify the gap, scope tools, pick a
  model, write the prompt. Points at `.claude/agents/README.md` for the
  worked example instead of duplicating it.
- `kb/` + `scripts/kb_index.py` + `scripts/kb_query.py` — markdown notes
  indexed into SQLite FTS5, chunked per `##` section. Kinds: `progress`,
  `knowledge`, `codemap`, `docs`, `history`.
- `memos/` — append-only decision records. Indexed into the *same* table
  under kind `memos`, so one query reaches both stores.
- `.claude/settings.json` — `PostToolUse` hook that rebuilds the index,
  and two `Stop` hooks: `checkpoint_guard.py` (blocks once when files
  changed after this file, see memo 0003) and `reflection_guard.py`
  (blocks once every 5th completed task to run the `reflection` skill,
  see memo 0004).
- `.claude/skills/reflection/` — retrospective over the last 5 tasks:
  what got done, whether a recurring pattern is worth a new skill, what
  could be improved. Writes findings to `kb/history/`.
- `CLAUDE.md` "Session continuity" — the rule that makes clearing context
  safe: read this file first, checkpoint it after every meaningful step.

Search behaviour: query tries exact syntax, then AND of all terms, then
OR, so natural-language questions still land. Results are ranked by BM25
and ordered `progress` first.

## Next steps

- Resolved: remote added and pushed — `origin` is
  `git@github.com:schaf-run/the_oracle_template.git`, `main` tracks
  `origin/main`.
- Both hooks' logic re-verified by piping payloads directly this
  session: `checkpoint_guard.py` blocks when a tracked file is newer
  than this file, no-ops when `stop_hook_active` is set, and passes
  through cleanly when nothing changed; `kb_index.py --if-stale --quiet`
  only rebuilds when a kb/memos source is newer than `.claude/kb.db`.
  Still not directly observed being auto-fired by the harness
  end-to-end (as opposed to invoked manually) — low-risk, not blocking.
- Resolved: shipped two more example skills — `choose-model` and
  `create-subagent` — beyond `meta-skill` and `kb`.
- Added `reflection` skill + `reflection_guard.py` Stop hook (every 5
  tasks). "Task" = one Stop event, the closest thing the hook system
  exposes — see memo 0004 for why and for the interaction with
  `checkpoint_guard.py`. Confirmed working live: it fired for real after
  5 real turns and produced the first reflection note,
  `kb/history/2026-09-21-reflection.md`.
- Open: `choose-model/SKILL.md` and `create-subagent/SKILL.md` use
  `[[wikilink]]`-style cross-references left over from a different
  memory system's convention, not this repo's memo-filename-linking
  style. Flagged by the first reflection pass; not fixed yet — small,
  low-priority cleanup.
- Currently on branch `dev` (off `main` at the point pushed to
  `origin`), created as a general working branch, no specific task
  assigned yet.

## How to resume

1. Read this file.
2. `scripts/kb_query.py --list` to see everything stored.
3. `scripts/kb_query.py "<topic>"` for detail on any of it.

Keep this file current — it is the one thing that makes clearing context
safe. Update it at the end of any meaningful step, not just at session end.
