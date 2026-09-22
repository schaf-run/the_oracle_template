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
- `reflection/` — retrospective over the last 10 tasks, triggered by a
  `Stop` hook (`scripts/reflection_guard.py`); reviews for skill gaps
  and process improvements.
- `deliver-research/` — after the `researcher` sub-agent hands back a
  report, write the full findings to a scratchpad file and send a
  condensed Telegram summary with the doc attached.

Only add a new skill once a workflow has been used more than once or the
user asks for a slash command explicitly. Keep the trigger description
narrow.

Example layout for a new skill:

```
.claude/skills/deploy/SKILL.md
```
