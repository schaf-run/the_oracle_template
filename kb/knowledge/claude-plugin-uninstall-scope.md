---
title: claude plugin CLI scope gotchas (install/uninstall/marketplace add)
summary: "claude plugin uninstall <name>" fails silently/errors if the plugin was installed with --scope project; must repeat the same scope flag to remove it. Separately, "claude plugin marketplace add" defaults to user scope even when the plugins it serves are installed --scope project, so the marketplace source itself won't travel with the repo unless added with --scope project too.
tags: [cli, plugins, gotcha]
updated: 2026-09-22
---

# claude plugin uninstall needs explicit --scope for project-scoped plugins

Removing a plugin isn't scope-agnostic: the CLI needs to be told which
scope it was installed in, the same way install does.

## Gotcha

`claude plugin uninstall <name>` (no scope flag) failed when the plugin
had been enabled with `--scope project` — the plain form only looks in
user scope. `claude plugin uninstall <name> --scope project` is what
actually removed it, clearing `enabledPlugins` in `.claude/settings.json`
and the entry in `~/.claude/plugins/installed_plugins.json`.

If a plugin was installed with a scope flag, assume uninstall needs the
same flag; don't take a bare uninstall failure as "plugin not present."

## Related cleanup

Uninstalling the plugin doesn't stop a still-running background process
it spawned (e.g. a bot process) or remove its stale pid file — check for
and kill those separately. Credentials/config the plugin used (tokens,
`.env`, access files) live outside the repo and aren't touched by
uninstall either; only remove those if the user actually asks.

## claude plugin marketplace add defaults to user scope

`claude plugin marketplace add <repo>` declares the marketplace source in
*user* settings by default, even if every plugin from it is then installed
with `--scope project`. That split is a trap: `enabledPlugins` in
`.claude/settings.json` (git-tracked) will list e.g.
`design-research@designer-skills`, but nothing in the repo says where
`designer-skills` comes from — a fresh clone (or another machine) can't
resolve the marketplace and the plugin install is effectively broken for
anyone but the session that ran the original `add`.

Fix: pass `--scope project` to `marketplace add` too, so the source lands
in `extraKnownMarketplaces` inside `.claude/settings.json` alongside
`enabledPlugins`. Re-running `add --scope project` on a marketplace
already added at user scope is safe and idempotent — it just adds the
project-scope declaration without erroring or re-cloning.
