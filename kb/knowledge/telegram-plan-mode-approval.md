---
title: Plan mode approval doesn't reach a Telegram-driven session
summary: ExitPlanMode's approval UI is CLI-native; when the user is on Telegram, send the plan as a message/doc and treat their reply as approval instead.
tags: [telegram, plan-mode, convention]
updated: 2026-09-22
---

# Plan mode approval doesn't reach a Telegram-driven session

When a conversation is being driven from Telegram (messages arrive as
`<channel source="plugin:telegram:telegram" ...>`), `ExitPlanMode`'s
built-in approval prompt surfaces in the CLI, not in Telegram — the user
doesn't see it there and would have to open a terminal themselves just
to approve, defeating the point of a chat interface. Confirmed by the
user directly: "i don't see your requests in cli if i'm talking to you
in telegram, so i head to open the cli myself to approve your plan."

## Convention

After finishing a plan in plan mode for a Telegram-driven task, send the
plan content (or attach it as a file) via the Telegram `reply` tool and
treat the user's Telegram reply as the real approval. Still call
`ExitPlanMode` once they've said go-ahead, to formally close the phase —
but the actual back-and-forth with the human happens over Telegram, not
through the CLI's approval UI.

This also lives in this user's cross-session memory (not just this
repo), since it applies to any project where they interact via the
Telegram plugin — but it's recorded here too so it travels with the
repo to a different machine/session. See `memos/0008-researcher-
subagent.md` for the concrete instance this was first learned from.

## Refinement: the Telegram `reply` tool is fully blocked *inside* plan mode

Discovered while planning `architect` (memo 0009): plan mode's read-only
sandbox blocks the Telegram `reply` tool outright, not just
`ExitPlanMode` — so there's no way to send a Telegram message at all
while still inside plan mode, even for a clarifying question mid-plan.
`AskUserQuestion` **is** allowed inside plan mode and does reach a
Telegram-driven user (confirmed twice this session — they answered
model-tiering and Plan-vs-architect questions asked this way). So: for
anything that must reach the user *while still in plan mode* (a
clarifying question, an unplanned design pivot), use `AskUserQuestion`,
packing any needed explanation into the question/option text — don't
try `reply`, it will be rejected. Save `reply` (with the plan doc
attached) for after the plan is finished, same as the base convention
above.
