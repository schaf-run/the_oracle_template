# Skills

Each skill lives in its own directory: `.claude/skills/<name>/SKILL.md`.

`meta-skill/` is the one skill that ships with this template. It runs
before planning to check whether an existing skill or sub-agent already
covers a task, and decides whether a real gap is worth filling with a new
skill — see `meta-skill/SKILL.md` and the "Big picture" section of the
root `CLAUDE.md`.

Only add a new skill once a workflow has been used more than once or the
user asks for a slash command explicitly. Keep the trigger description
narrow.

Example layout for a new skill:

```
.claude/skills/deploy/SKILL.md
```
