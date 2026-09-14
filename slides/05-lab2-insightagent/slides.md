---
title: "**Lab 2**: InsightAgent"
sub_title: Breakout rooms · :8081
author: Kevin Cunningham
---

## Same rooms, same CRM, different stakes

**In breakout rooms (until called back):** Run InsightAgent at :8081. Same rooms as Lab 1. Same shared Google Doc structure, plus one new question.

<!-- speaker_note: Reset session between attempts inside each room so memory doesn't leak across demos within the room. -->

<!-- end_slide -->

## Suggested sequence — not prescriptive

<!-- incremental_lists: true -->

1. Run a happy read query — note what appears in working memory (LLM02)
2. Try ④ the export scenario — check `exports/` for the file
3. Try ⑤ the send scenario — what would stop this in a real system?
4. Try ② Taylor indirect injection — what did the agent decide to do?
5. Try ① direct injection via the query field — trace it to a tool call
6. Try ⑥ prompt leak — what's in the system prompt that shouldn't be there?
7. **Technical delegates:** find `permission_check: false` in source — what would `true` look like?

<!-- end_slide -->

## The new question

Same five sections as Lab 1, plus:

**What did the model decide?**

Trace the path: user input → what the planner chose → which tool ran → what side effect occurred.

**This is the key question for an agentic system — the model is making decisions, not just generating text.**

<!-- end_slide -->

## Pairing exercise — before debrief

Match CampaignBot ①② to InsightAgent ①② on the same characters.

**In your room: same attack, different consequence. Why?**

<!-- speaker_note: Give rooms 5 minutes on this specifically before reconvening — it's the bridge into the afternoon's threat modelling. -->

<!-- end_slide -->

<!-- jump_to_middle -->

Debrief
===

<!-- end_slide -->

## What would you change before shipping?

**Each room reads out their "what would you want changed before shipping" row.**

<!-- speaker_note: Map to OWASP, then introduce human-in-the-loop as a design pattern, not a patch — that's the line to land before lunch. -->

<!-- end_slide -->

## Bridge to the afternoon

**Morning:** you attacked two apps and watched the model both generate and decide.

**Afternoon:** one demo on poisoned training data, four guided risks, then you map all of it onto something you're actually building.

<!-- end_slide -->
