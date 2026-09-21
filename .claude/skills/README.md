# Skills

Each skill lives in its own directory: `.claude/skills/<name>/SKILL.md`.

Skills shipped with this template:

- `meta-skill/` — runs before planning to check whether an existing skill
  or sub-agent already covers a task, and decides whether a real gap is
  worth filling with a new skill. See the "Big picture" section of the
  root `CLAUDE.md`.
- `kb/` — how to query and write to the project knowledge base.
- `choose-model/` — which model tier and reasoning effort to use for a
  task, a sub-agent, or an agent definition.
- `create-subagent/` — how to define a new `.claude/agents/<name>.md`.

Only add a new skill once a workflow has been used more than once or the
user asks for a slash command explicitly. Keep the trigger description
narrow.

Example layout for a new skill:

```
.claude/skills/deploy/SKILL.md
```
