# Sub-agents

Custom agents live here as `.claude/agents/<name>.md` with frontmatter
(`name`, `description`, `tools`, optional `model`).

Only define one when the built-in types (general-purpose, Explore, Plan)
don't fit — typically because the task needs a genuinely restricted tool
scope or is a specialized role you'll invoke by name repeatedly. See the
"Creating sub-agents" section of the root `CLAUDE.md`.

Example stub:

```markdown
---
name: read-only-reviewer
description: Reviews a diff for correctness without editing anything. Use for a second opinion before merging.
tools: Read, Grep, Glob, Bash
---

Review the given diff or PR for correctness bugs. Do not edit files.
Report findings ranked by severity with file:line references.
```
