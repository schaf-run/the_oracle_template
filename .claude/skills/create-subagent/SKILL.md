---
name: create-subagent
description: Define a new custom sub-agent at `.claude/agents/<name>.md` — scope its tools, pick its model, write its prompt. Use when the user asks to create/add a sub-agent or agent, or when the meta-skill gap check finds no built-in type or existing agent fits and the role will recur.
---

# Creating a sub-agent

## Process

1. **Confirm the gap is real.** This assumes the meta-skill scan already
   ran and found no built-in type (general-purpose, Explore, Plan) and no
   existing `.claude/agents/*.md` that fits. If that scan hasn't happened
   yet, do it first — see `.claude/skills/meta-skill/SKILL.md`.
2. **Check the justification.** Per the "Creating sub-agents" section of
   the root `CLAUDE.md`, only proceed if either:
   - the task needs a genuinely restricted tool scope (e.g. a reviewer
     that can read but not edit), or
   - it's a specialized role you'll invoke by name repeatedly, in this
     project or across projects.
   A one-off task isn't a sub-agent — that's just a plan. Don't build one
   "just in case."
3. **Pick the location.** `.claude/agents/<name>.md` for project-scoped
   (shared, checked in). `~/.claude/agents/<name>.md` for a personal
   agent you use across projects (not checked in here).
4. **Write the frontmatter.**
   - `name` (lowercase + hyphens, no `:`) and `description` are required
     — the file is silently skipped without both.
   - `description` is what an orchestrating session reads to decide
     *when* to delegate to this agent — write it as a narrow trigger,
     the same way a skill's `description` is a trigger, not a summary.
   - `tools` scopes the allowlist (e.g. `Read, Grep, Glob` for a
     read-only reviewer). Omit it to inherit everything; use
     `disallowedTools` instead if it's easier to name the few tools to
     remove than the many to keep.
   - `model` — set only if this role needs a non-default tier; see
     [[choose-model]] for how to pick. Omit to use the default order.
   - Leave every other optional field (`permissionMode`, `maxTurns`,
     `effort`, `isolation`, `color`, `skills`, `mcpServers`, …) out
     unless the role specifically needs it — match the size of the
     definition to the size of the role.
5. **Write the body.** Everything after the `---` is the agent's system
   prompt: its scope, what it should and shouldn't touch, and the output
   format if the caller needs one back in a specific shape.
6. **Verify it triggers correctly** — re-read the `description` as if you
   were the orchestrator deciding whether to delegate; if it's vague
   enough to fire on unrelated tasks, narrow it.

See `.claude/agents/README.md` for the worked example (a read-only
reviewer stub) and the file-format reference.

## Anti-patterns

- A `description` broad enough to match almost any task — that makes the
  agent fire (or get picked) when it shouldn't.
- Granting full tool access by default instead of scoping — the whole
  point of a custom agent is usually the restriction.
- Defining an agent for a task you're about to do once — write a plan
  instead.
- Duplicating a built-in type's behavior under a new name because the
  gap-check step was skipped.
