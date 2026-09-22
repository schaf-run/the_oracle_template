---
name: reflection
description: Retrospective pass over the last batch of completed tasks — triggered automatically by a Stop hook every 10 tasks, or invoked manually (e.g. "run reflection"). Reviews what got done, whether a recurring pattern is worth turning into a skill, and what could be improved in how the work happened. Not for reviewing a single diff or PR — that's code-review.
---

# Reflection

A retrospective, not a status report. Purpose: catch recurring patterns
and friction that a single task is too small to notice.

"Task" here means one Stop event — roughly one user request handled
start to finish. `scripts/reflection_guard.py` counts these and fires
every 10th one; see `memos/0004-reflection-skill-and-hook.md` and
`memos/0010-reflection-cycle-and-auto-commit.md` for why.

## Process

1. **Scope the window.** The tasks since the last note in `kb/history/`
   tagged `reflection` (or since session start if there isn't one yet).
   Work from what's already in context — conversation recall, `git log`,
   and recent `kb/progress/CURRENT.md` edits — not a full transcript
   replay.
2. **Summarize what happened.** One or two lines per task: what was
   asked, what shipped. This is the cheap part; don't over-invest here.
3. **Skill-gap check, retrospective version.** Run the same scan as
   `.claude/skills/meta-skill/SKILL.md` §2, but backward-looking: did any
   task repeat a multi-step procedure that isn't already covered by an
   existing skill or sub-agent? If a real, recurring gap turns up, don't
   just note it — follow meta-skill's decision process and create it (or
   record why not, e.g. still only seen once).
4. **Process check.** Look for friction: repeated user corrections,
   mistakes, missed conventions, a hook or skill that should have fired
   and didn't. Cite the specific task, not a vague impression — "cited
   the wrong file path in task 3" beats "could be more careful."
5. **Write it up.** One note in `kb/history/`, started from
   `kb/TEMPLATE.md`, tagged `reflection`. If step 3 produced a decision
   (a new skill, a changed convention), also record it in `memos/` per
   the usual rule — the history note is the retrospective, the memo is
   the decision.
6. **Nothing to report is a valid outcome.** If the last 10 tasks were
   routine and nothing surfaced, say so in one line and don't write a
   note just to have written one.
7. **Commit the reflection output.** If step 5 wrote or changed
   anything (`kb/history/`, `kb/knowledge/`, `memos/`, `kb/INDEX.md`,
   `kb/progress/CURRENT.md`'s "Latest reflection" pointer), commit those
   files in their own commit before ending the turn — this is a standing
   exception to "commit only when asked," scoped to reflection's own
   output only. Don't bundle unrelated pending changes into it. If step
   6 applied and nothing was written, there's nothing to commit.

## Anti-patterns

- Replaying full tool-call history instead of working from summaries —
  this is a retrospective, not an audit.
- Proposing a skill for something that happened once — same bar as
  meta-skill: it must actually recur.
- Padding a note when there's nothing to say.
- Treating this as a diff/code review — that's `code-review` or
  `simplify`; reflection looks at process and patterns, not correctness
  of a specific change.
