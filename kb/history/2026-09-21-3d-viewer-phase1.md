---
title: Reflection — 3D viewer Phase 0/1, meta-skill gap recurred
summary: Phase 1 vertical slice shipped clean; the meta-skill pre-plan check was skipped a second time, now enforced by a hook.
tags: [reflection, history]
updated: 2026-09-21
---

# Reflection — 3D viewer Phase 0/1, meta-skill gap recurred

Covers the 5 tasks counted by `reflection_guard.py` since the previous
note (`kb/history/2026-09-21-reflection.md`, which ended at commit
`4bce8ba`). Nothing from that window has been committed yet — see
`kb/progress/CURRENT.md` for the full app status.

## What happened

1. User asked for a short execution plan for a 3D model upload/viewer web
   app (upload `.obj` up to 500MB, get a link, view with rotate/zoom on
   mobile). Gave a 5-phase plan with stack recommendations and two
   flagged decisions.
2. User asked to discuss Phase 0. Broke it into four concrete decision
   points (backend shape, storage, metadata store, project location)
   with recommendations and tradeoffs per point.
3. User answered all four. Finalized the stack: Express + TS + Prisma/
   SQLite backend, Vite + React + Three.js frontend, local disk storage,
   built in this repo — with a nullable `ownerId` column as the only
   forward-compat concession for planned-but-not-yet-built auth.
4. User noted a possible future Rust backend rewrite. Acknowledged
   without acting on it now (keeping the API plain REST/JSON was already
   the natural choice, so nothing changed), confirmed Phase 0 settled.
5. User said "go on." Entered plan mode, used a Plan sub-agent plus
   direct verification (actual `node`/`npm` version checks on the
   machine) to produce a concrete Phase 1 plan, got approval, then built
   the full vertical slice: monorepo scaffold, Express server, Prisma/
   SQLite, a busboy streaming upload handler (found and fixed two real
   race-condition bugs along the way), REST endpoints, Vite/React client,
   a Three.js viewer with `OrbitControls`. Verified via curl (upload
   validation, size limits, byte-identical round-trip, 404s) and via the
   built-in browser (model renders/rotates/zooms, mobile-viewport
   emulation, clean not-found state). Reported results with explicit,
   honest gaps: couldn't drive a native file picker or test real
   touch/pinch with the available tools.

## Skill-gap check

No new recurring multi-step procedure turned up — Phase 1 was one large
task, not a repeated pattern, so it doesn't clear the "must actually
recur" bar for a new skill on its own.

One thing *did* recur, though, and crossed that bar: the meta-skill
pre-planning orientation check was skipped again before task 5's plan-mode
entry — the same gap the previous reflection note flagged ("worth doing
explicitly going forward") after it was first skipped building the
reflection skill itself. Two misses relying on memory alone is a real
pattern, not a one-off, so this stopped being a "note it and move on"
situation. Built `scripts/meta_skill_guard.py` (PreToolUse on
`EnterPlanMode`, hard-blocks unless meta-skill ran first) and
`scripts/meta_skill_track.py` (PostToolUse on `Skill`, sets the marker).
Verified the full cycle by piping test payloads through both scripts
before wiring them in. See `memos/0006-enforce-meta-skill-before-plan-
mode.md` for the full decision.

## Process notes

- The `.claude/settings.json` edit to wire the new hooks was blocked by
  the auto-mode classifier as self-modification, correctly — stopped,
  explained the two proposed hook entries and why, and used
  `AskUserQuestion` to get explicit sign-off rather than working around
  it. Worth remembering as the expected pattern: hook/settings changes
  in this template need to surface as an explicit ask, not just happen.
- Real friction discovered during Phase 1 build, not previously
  documented: shell state (`nvm use`) doesn't persist across Bash tool
  calls, only the working directory does. Every `npm`/`node` command
  needed re-prefixing with `source ~/.nvm/nvm.sh && nvm use`, or it
  silently ran against a stale Homebrew npm 6.9.0. Now captured in
  `kb/knowledge/nvm-shell-state-per-bash-call.md` so it's found by a
  query instead of rediscovered by a confusing failure.
- Two real bugs were found and fixed in the upload handler (a size-0
  race between busboy's `finish` and the write stream actually flushing;
  an orphaned-file leak from unlinking before `fs.createWriteStream`'s
  async `open()` resolved) — caught because each step was verified
  against real behavior (curl + `ls`/`diff`) rather than trusting the
  code once it typechecked. Written up in
  `kb/knowledge/upload-streaming-gotchas.md`. Worth reinforcing as the
  pattern that worked, not just noting the bugs: typecheck passing was
  treated as necessary, not sufficient.
- No user corrections in this window — Phase 0 discussion converged
  cleanly, and the user's answers were taken as decisive without
  re-litigating. Testing gaps (file-picker upload, real mobile touch)
  were surfaced proactively in the final report instead of glossed over
  or quietly claimed as done.
