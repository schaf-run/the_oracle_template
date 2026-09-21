---
title: "0005: Defer Express serving the built client bundle"
summary: Phase 1 runs two dev servers (Vite + Express) with a proxy; Express serving client/dist is deliberately not wired up yet.
tags: [app, deployment, backend]
updated: 2026-09-21
---

# 0005: Defer Express serving the built client bundle

Date: 2026-09-21

## Context

Building Phase 1 of the 3D model upload/viewer app (Express + Prisma/SQLite
backend, Vite + React + Three.js frontend, see
`kb/progress/CURRENT.md`). In dev, Vite's dev server proxies `/api` calls to
Express so the browser only ever talks to one origin. In production, Express
could instead serve `client/dist` directly as static files plus a
history-mode fallback so client-side routes (`/model/:id`) resolve
server-side too — making one deployable process instead of two.

## Decision

Not wiring this up in Phase 1. Client code only ever calls relative
`/api/...` paths (never a hardcoded origin), so adding
`express.static(clientDist)` + a catch-all fallback route later is a
drop-in change, not a refactor.

## Why

No deployment target has been chosen yet, and static-serving + history-mode
fallback + build-order coupling between `client` and `server` is real work
with zero payoff until an actual deploy story exists. Building it now would
be exactly the kind of "scaffolding for later" this project's CLAUDE.md
warns against. Phase 1's bar is a working upload→link→view flow with two
dev servers running side by side, which is fully met without this.

## Consequences

When a deployment target is picked, add `express.static` + fallback route
to `server/src/app.ts` and update the root `build`/`start` scripts
accordingly — should be a small change given the relative-path discipline
already in place. Nothing here blocks that.
