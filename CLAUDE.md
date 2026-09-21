# Agent Rules Template

Copy this whole directory when starting a new project. Trim anything that
doesn't apply; add project-specific rules as you discover them (see
"Maintaining this file" below) — don't let discoveries live only in chat.

## Big picture (before planning)

- Before planning, run the orientation pass in
  `.claude/skills/meta-skill/SKILL.md`: check whether an existing skill or
  sub-agent already covers the task, and decide whether a genuinely
  reusable gap is worth building a new skill for right now.
- Skip this for trivial, obviously one-off asks. For anything else, know
  what already exists before you start — don't rebuild something a skill
  already does, and don't miss a real, recurring gap.

## Planning

- Use plan mode for anything touching more than one file or where the
  approach isn't obvious upfront. Skip it for single-file fixes, lookups,
  and mechanical changes.
- Before planning, state assumptions plainly. Only ask the user questions
  that only they can answer (a real product/priority tradeoff) — don't ask
  for things derivable from the code or docs.
- Plans name concrete files/functions, not vague steps: "add token refresh
  to `src/auth/session.ts`" beats "update auth."
- Re-plan out loud when a step reveals the original approach was wrong.
  Don't silently push forward on a plan you no longer believe in.

## Executing

- Verify before claiming done: run the build/tests/linter, don't eyeball
  the diff and call it finished.
- Prefer several small, independently-verifiable edits over one large
  rewrite.
- No speculative abstraction, no unrequested refactors, no scaffolding
  "for later." Match the size of the change to the size of the ask.
- Anything hard to reverse (force-push, migration, deleting data, touching
  shared infra) — stop and confirm even when operating autonomously.
- Commit only when asked. When asked, match the repo's existing message
  style and never bundle unrelated changes into one commit.

## Memos (decision & context log)

A project-local, **git-tracked** record of *why* — for humans and for the
next agent session on a different machine. This is separate from Claude's
own private cross-session memory; memos live in the repo and travel with
the code.

- Location: `memos/NNNN-short-title.md`, numbered sequentially. One memo
  per decision or incident. Start from `memos/TEMPLATE.md`.
- Write one when: an architectural decision is made, a non-obvious
  constraint or gotcha is discovered, a workaround goes in for a specific
  bug, or a plan changes direction mid-flight and future-you will wonder why.
- Don't write one for anything already derivable from `git log`/`git diff`
  — memos capture reasoning, not changes.
- Link related memos to each other by filename when a decision supersedes
  or depends on an earlier one.

## Skills

- Whether a skill is needed at all is decided by the meta-skill gap check
  above, not on the fly mid-task — see
  `.claude/skills/meta-skill/SKILL.md`.
- Package a workflow as `.claude/skills/<name>/SKILL.md` when it's used
  more than once, follows a specific repeatable procedure, or the user
  explicitly wants a slash command.
- Don't create a skill for a one-off task — that's just a plan.
- Write the trigger description narrowly. A skill that fires on everything
  is worse than no skill; be specific about when it should and shouldn't
  activate.
- Use the `update-config`-style workflow (or hand-edit) to keep skills
  consistent with the rest of `.claude/`.

## Hooks

- Use `.claude/settings.json` hooks for things that must happen every
  time, mechanically, without depending on the model remembering:
  formatting on save, blocking edits to a protected path, notifying on
  long task completion, enforcing a commit-message format.
- Don't reach for a hook when a rule in this file already covers it —
  hooks are for hard enforcement, not stylistic preference.
- Keep hooks few and legible. A hook that silently mutates output is worse
  than a rule the agent might occasionally forget.

## Choosing MCP servers

- Add an MCP server only when a task genuinely needs it: external live
  state, a real API, a data source no existing tool reaches. "Might be
  useful someday" is not a reason.
- Before adding: check the server's source/publisher, prefer
  official/verified servers over random community ones, and scope
  credentials as narrowly as the task allows.
- Project-scoped servers (shared with the team) go in a project `.mcp.json`
  that's checked in — reference credentials via env vars, never inline
  secrets. Personal-only servers belong in user-level config instead.
- Skim the tool list a new server exposes before approving it broadly;
  don't grant a server more reach than the task needs.

## Creating sub-agents

- Default to the built-in types (general-purpose, Explore, Plan) for
  anything generic — don't define a custom agent to save a few words of
  prompt.
- Define `.claude/agents/<name>.md` only when the task needs a genuinely
  distinct, narrow tool scope (e.g., a read-only reviewer that can't edit)
  or is a specialized role you'll invoke by name repeatedly across
  projects.
- Don't spawn a sub-agent for something cheap to do inline — each fresh
  spawn re-derives context, which costs more than doing it directly.
- Fork (not a fresh agent) when you want to keep shared context but keep
  the sub-task's noisy tool output out of the main thread.

## Maintaining this file

- When a new project-specific rule or convention is discovered mid-task,
  add it here — not only to chat memory — so it survives across sessions
  and machines.
- Keep this file short enough to read in full in one sitting. Push detail
  out to `memos/`, `.claude/skills/`, or `.claude/agents/` rather than
  inlining it here.
