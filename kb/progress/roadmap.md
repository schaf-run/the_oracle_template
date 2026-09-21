---
title: 3D viewer app — phase roadmap
summary: The original Phase 0–4 plan proposed in chat, with status, and how phase numbering reconciles with what was actually built.
tags: [progress, roadmap, app]
updated: 2026-09-21
---

# 3D viewer app — phase roadmap

The original roadmap for the 3D model upload/viewer app, as proposed at
the start of this work (was only ever in chat until now — see
`kb/progress/CURRENT.md` for a note on why that's a gap worth avoiding).

## The five phases as proposed

- **Phase 0 — Scaffold & decisions**: pick stack, storage, metadata
  store, project location.
- **Phase 1 — Upload pipeline**: backend upload handling, link
  generation, metadata storage.
- **Phase 2 — Viewer**: `/model/{id}` page, Three.js rendering, mobile
  touch controls.
- **Phase 3 — Hardening**: client-side validation, upload error/retry
  handling, empty/expired-link states, deploy.
- **Phase 4 — Stretch (not MVP)**: `.mtl`/texture support, server-side
  glTF conversion for faster mobile loads, link expiry/cleanup,
  private/auth-gated links.

## Status

- **Phase 0 — done.** Stack: Express + TS + Prisma/SQLite backend
  (persistent server, not serverless — auth planned later), local disk
  storage for MVP, Vite + React + Three.js frontend, built in this repo.
- **Phase 1 and Phase 2 — done as one combined vertical slice.** When
  implementation started, the plan-mode plan bundled scaffold + upload
  pipeline + viewer into a single pass and called it "Phase 1: Scaffold +
  Vertical Slice" (see `/Users/schaf.run/.claude/plans/sunny-waddling-
  lighthouse.md` — that file's "Phase 1" is *not* the same as this
  roadmap's Phase 1; it's Phases 0+1+2 combined). Upload endpoint, link
  generation, and the Three.js viewer with rotate/zoom all work and were
  verified live — see `kb/progress/CURRENT.md` for what was tested and
  the two known gaps (real mobile touch/pinch untested; file-picker
  upload now confirmed working by the user's own test).
- **Phase 3 — Hardening — not started.** Client-side validation exists
  minimally (extension via `accept=".obj"`, real enforcement is
  server-side); no retry UI, no expired-link handling beyond a generic
  404, no deploy story yet (Express serving the built client bundle was
  explicitly deferred — see
  `memos/0005-defer-static-client-serving.md`).
- **Phase 4 — Stretch — not started.** No `.mtl`/texture support, no
  glTF conversion, no expiry/cleanup, no auth (only the nullable
  `ownerId` column exists as a hook).

## Next up

Phase 3 (hardening) is the natural next unit of work when resumed:
client-side validation/retry UX, expired/missing-link states beyond the
current bare 404, and picking a deploy target (which also unblocks the
deferred Express-serves-client-bundle decision in memo 0005).
