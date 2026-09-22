---
title: Reflection — oracle-test branch created, Telegram MCP connector planned (not built), meta-skill gap-check miss found and corrected mid-session
summary: First real stress-test of the template post-context-clear; a genuine meta-skill process miss (didn't route a planning task to the architect sub-agent) surfaced only because the user asked why, plus a user-requested bloat audit of kb/memos/scripts.
tags: [reflection, meta-skill, architect, planning, bloat]
updated: 2026-09-22
---

# Reflection — oracle-test branch, Telegram MCP planning, meta-skill gap-check miss

Covers the tasks since `kb/history/2026-09-22-concurrency-cap-and-telegram-removal.md`, across a context clear. Session opened with the user asking for an honest usefulness assessment of the whole template (see below), then moved into an actual build attempt used as a fresh stress test.

## What happened

1. User asked whether the project is genuinely useful or over-complicated.
   Assessed from memos/kb/git history: found the 3D app removal and the
   Telegram plugin removal, read both as abandoned work, and gave a
   critical verdict. User corrected: the 3D app was deliberately extracted
   to a separate branch to keep this branch template-only, not abandoned
   as a failure — only the Telegram case was a genuine "tried it, it was
   bad, cut it." Verdict stands on narrower grounds after the correction.
2. User asked to create `oracle-test` off `oracle-dev` and stress-test the
   template with a new, real (not toy) task. Branch created and pushed.
   Scope narrowed via `AskUserQuestion` to "new small real task," then the
   task itself handed to the `researcher` sub-agent per the user's
   explicit instruction ("we got a researcher for this") rather than
   picked by the orchestrator.
3. `researcher` returned 6 ranked project ideas grounded in actual web
   research (vertical-slice/agent-eval literature, weekend-project
   roundups), correctly ignored an injected instruction in a tool result
   trying to get it to create a doc via tools it didn't have, and flagged
   the injection rather than silently complying.
4. User picked a Telegram MCP connector (replacing the removed plugin),
   then refined requirements mid-stream: full self-hostable backend, must
   overcome the Bot API's 20MB download cap, wants the plan presented
   before any execution.
5. Ran the kb query + meta-skill gap-check before planning, per `CLAUDE.md`.
   **The gap-check reasoning was flawed**: it correctly found no agent
   could *implement* this (`researcher`/`architect` are both read-only or
   plan-only), and from that concluded no agent fit — without separately
   asking whether an agent fit *planning* it. `architect`'s entire purpose
   is planning implementation tasks; the check never actually evaluated it
   against that criterion. Entered plan mode solo, did real technical
   grounding (self-hosted `telegram-bot-api` for the 20MB limit, a working
   FastMCP + Streamable HTTP spike proven live in this sandboxed
   environment via `pip install --break-system-packages --user`), and
   wrote a draft plan.
6. On `ExitPlanMode`, the user asked directly: "why didn't you use an
   architect for this plan?" This is the finding that matters most from
   this window — nothing in the template's own enforcement caught the
   miss; `meta_skill_guard.py` only verifies the gap-check *ran* before
   `EnterPlanMode`, not that it reached a correct conclusion. Only the
   user's question caught it.
7. Routed to `architect` after the fact, reusing one agent instance across
   two calls per the orchestrator convention in `memos/0009`. It validated
   most of the draft but found a real, substantive bug the draft had
   missed: `download_file` returned a local filesystem path, which is
   meaningless to a remote MCP client not on the same host as the server.
   Detailed follow-up produced a coherent fix (server-side file-serving
   route reusing the existing bearer token, a three-way `send_file`
   contract, TTL-based retention, hand-rolled HMAC auth instead of
   FastMCP's JWT-oriented provider, and an `src/telegram_mcp/` package
   layout to dodge the hyphenated-directory import problem). Folded into
   the plan file. This is a genuine, concrete point in the template's
   favor once routed correctly — not just process overhead.
8. User paused implementation and asked instead for an audit of this
   planning stage plus a broader bloat/compaction review of the template,
   since everything "getting too big" was a live concern from item 1.
   Delivered with real numbers: 9 memos / 543 lines, 7 kb/history notes /
   405 lines, 6 hook scripts / 453 lines — all of it about the template's
   own machinery, none about shipped product (consistent with item 1's
   original critique, now with data). Found two concrete decay patterns:
   `kb/history/` fragmenting the now-dead Telegram saga across 5 of 7
   notes with no closing/compaction step, and `kb/progress/CURRENT.md`
   (145 lines, 14 edits) drifting from "resume pointer" into a de facto
   reference manual for every hook/skill/agent, which belongs in
   `kb/knowledge/`/`kb/codemap/` instead. Corrections proposed, none
   applied yet — awaiting user confirmation.

## Skill-gap check

No new recurring multi-step procedure surfaced that isn't already
covered. The one real process gap found (item 5/6) is not "missing
tooling" but a wording defect in existing tooling — see Process check.

## Process check

- **Real, citable miss**: `meta-skill/SKILL.md` step 2 does not
  distinguish "which agent plans this" from "which agent implements
  this." Applied to a task that clearly needed `architect`, the check
  concluded "no match" by only evaluating implementation fit. The
  `meta_skill_guard.py` hook enforces that the gap-check *ran*, which
  gave false confidence — it cannot and does not verify the check's
  conclusion was right. This is a structural limit of hook-based
  enforcement over a fuzzy cognitive step, not something another hook
  fixes; only tightening the skill's own wording does.
- **Positive**: `researcher`'s handling of the injected tool-result
  instruction (correctly refused, flagged rather than silently
  complying or silently ignoring) worked exactly as intended for a
  read-only, narrowly-scoped agent.
- **Positive**: the orchestrator convention of reusing one `architect`
  instance across the high-level pass and a detail request (memo 0009)
  worked as designed — the second call didn't need to re-establish
  context.
- User is actively tracking template bloat as a concern (raised it
  unprompted at session start, then again at session end) — this is now
  a recurring theme across two separate points in the same session, not
  a one-off complaint, and should weigh in favor of actually applying
  compaction rather than deferring it again.

## Outcome

One corrective edit warranted and proposed, not yet applied: reword
`meta-skill/SKILL.md` step 2 to separate the planning-fit question from
the implementation-fit question and name `architect` explicitly. Two
structural compaction proposals also pending user sign-off: a
close-out/compaction convention for finished `kb/history/` sagas, and
moving "current mechanism" reference content out of `CURRENT.md` into
`kb/knowledge/`/`kb/codemap/`. No new skill or sub-agent created this
round — the meta-skill fix is a wording correction to an existing skill,
not a gap needing new tooling.
