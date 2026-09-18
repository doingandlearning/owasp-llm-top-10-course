---
title: "**Lab 1**: CampaignBot"
sub_title: Breakout rooms · :8080
author: Kevin Cunningham
---

## Your turn

You've watched three attacks happen. Now run them yourself — and try the ones you think of that weren't on the list.

**In breakout rooms (until called back):** Run CampaignBot at :8080. Rooms of 3–4. One shared Google Doc per room — it's a record of your conversation, not a worksheet.

<!-- speaker_note: Google Docs are pre-loaded per room. Confirm everyone has the app running before sending them in. -->

<!-- end_slide -->

## Suggested sequence — not prescriptive

<!-- incremental_lists: true -->

1. Run the happy path — understand what the app is supposed to do
2. Try ① direct injection via the brief field
3. Try ② indirect injection via Jordan Lee's customer record
4. Try ③ output handling — inspect what the browser renders
5. **Technical delegates:** find where untrusted data enters the prompt in source
6. **Stretch:** try `SYSTEM_PROMPT_STYLE=hardened` — does it change anything?
7. **Build the fix:** set `ENABLE_VALIDATORS=true` in `.env`, restart, and re-run ①②③ — a validation panel shows what the pre-/post-validators caught in real time. Push technical delegates on whether it's a real fix or a pattern-matching speed bump.

<!-- end_slide -->

## The Google Doc

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**What did you find?**
Describe what happened — not how.

**Who would care about this?**
Product, legal, security, customer success — more than one answer is fine.

**What would an attacker actually do with this?**
Move beyond the demo. Worst realistic outcome.

<!-- column: 1 -->

**What would you want changed before shipping?**
A product decision, not a code fix. What's the acceptance criterion?

**Anything that surprised you?**
The most important row.

<!-- reset_layout -->

<!-- end_slide -->

<!-- jump_to_middle -->

Debrief
===

<!-- end_slide -->

## What surprised you?

**Each room reads out their "what surprised you" row.**

<!-- speaker_note: Map answers live to the OWASP risks on the Excalidraw matrix as rooms speak. Look for patterns across rooms — that's worth naming out loud. -->

<!-- end_slide -->

## Bridge to InsightAgent

**CampaignBot:** one string, one output. The attack and the consequence happened in the same breath.

**Next: InsightAgent** — same CRM, same characters, but now the model chooses tools. Watch how the blast radius changes.

<!-- end_slide -->
