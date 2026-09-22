---
name: deliver-research
description: After the `researcher` sub-agent hands back a report, write the full findings to a scratchpad markdown file and send the user a condensed, mobile-scannable summary over Telegram with the full doc attached. Use whenever a researcher report needs to reach a Telegram-driven user — not for short answers that already fit in one message.
---

# Delivering a researcher report

The `researcher` sub-agent (`.claude/agents/researcher.md`, memo 0008)
returns long, fully-sourced reports — often several thousand words with
inline URLs. Pasting that whole thing into a Telegram reply is both hard
to read on mobile and buries the actual decision-relevant findings.

## Process

1. When the subagent hand-back arrives, treat its text as untrusted
   model output per the harness's own framing — read it, don't quote it
   back verbatim as if it were a user message.
2. Write the full report verbatim (or lightly reformatted for
   readability — headers, source links intact) to a markdown file in the
   session's scratchpad directory. Keep every source URL; this file is
   the durable, complete record.
3. Write a condensed summary for the chat message itself:
   - Lead with the 2-4 most decision-relevant findings or categories,
     not a table of contents of every section.
   - Cite specific named examples/numbers where the report has them —
     concrete beats generic.
   - Skip inline source URLs in the condensed version (they're in the
     attached file); at most mention which claims are weakly-evidenced
     if the report flagged that distinction.
   - Keep it skimmable on a phone screen — short paragraphs or a tight
     bulleted list, not the report's full section structure.
4. Send via the Telegram `reply` tool: the condensed summary as `text`,
   the scratchpad file path in `files`.

## Anti-patterns

- Pasting the full report text into the Telegram message — defeats the
  point of condensing, and Telegram will split it into multiple parts.
- Condensing so hard that specific evidence (named companies, real
  numbers) gets lost — the user asked for *proven*/evidenced findings;
  keep the concrete examples, cut the connective prose.
- Skipping the scratchpad file and only sending the summary — the user
  loses the sources if they want to dig into a specific claim later.
