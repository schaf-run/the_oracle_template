---
title: nvm activation doesn't persist across Bash tool calls
summary: Every Bash call needs its own `source ~/.nvm/nvm.sh && nvm use` or it silently falls back to a stale Homebrew npm.
tags: [environment, node, nvm, gotcha]
updated: 2026-09-21
---

# nvm activation doesn't persist across Bash tool calls

This machine has `/opt/homebrew/bin/npm` (a stale Homebrew install, v6.9.0)
ahead of nvm on `PATH` by default. nvm manages the real toolchain
(`v20.19.0`, `v24.8.0` installed; this repo pins `20.19.0` via `.nvmrc`),
but each Bash tool call starts a fresh shell — working-directory state
persists between calls, but sourced shell state (like `nvm use`) does not.

Forgetting the prefix doesn't error loudly; it silently runs commands
against npm 6 (no workspaces support, different flag behavior), producing
confusing failures far from the actual cause.

**Every command in this project that touches `npm`/`node`/`npx` needs:**
```bash
source ~/.nvm/nvm.sh && nvm use >/dev/null && <actual command>
```
cd persists across calls, so this only needs repeating for the toolchain
activation, not the working directory.
