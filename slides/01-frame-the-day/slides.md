---
title: "**Securing AI**: OWASP LLM Top Ten"
sub_title: Ometria Engineering · One-Day Workshop
author: Kevin Cunningham
---

- Where are you? Role
- AI experience?
- What you want to get out of today?

<!-- end_slide -->

## Northwind Outfitters shipped an LLM-powered CRM

Marketing can write a personalised campaign in two minutes instead of an hour.
The feature is live. Security hasn't reviewed it yet.

**Type in chat: ship it / hold it / depends**

We'll come back to this at the end of the day.

<!-- speaker_note: Don't resolve this. Just bank the gut-reaction. Most rooms split roughly evenly — that's the point. -->

<!-- end_slide -->

<!-- jump_to_middle -->

The narrative spine
===

<!-- end_slide -->

## Three moments, escalating consequence

One fictional company. One CRM. The risk compounds.

<!-- incremental_lists: true -->

1. **CampaignBot** — a single LLM call, one string, one output. Injection and output handling are the whole story.
2. **InsightAgent** — same data, but the model chooses tools. The blast radius changes.
3. **Threat model** — map what you saw onto a feature *you* are actually building.

<!-- incremental_lists: false -->

**The day moves:** here is the attack → here is the consequence → here is your decision.

<!-- end_slide -->

## Meet the customers

Same fictional CRM, same characters, both apps. `@example.invalid` — nothing here is real.

| Customer | Role today |
|---|---|
| **Jordan Lee** | CampaignBot indirect injection — planted CRM notes |
| **Casey Nguyen** | Optional second indirect path (win-back segment) |
| **Taylor Brooks** | InsightAgent indirect injection — notes drive export-all |
| **Alex Morgan** | Benign, happy-path baseline |

**Demo:** Open the Excalidraw coverage matrix and zoom to the customer map.

<!-- speaker_note: Make them real, not abstract — it helps non-technical delegates stay grounded once the attacks get technical. You'll see Jordan and Taylor again this morning. -->

<!-- end_slide -->

## The coverage matrix is a map, not a lecture

Ten OWASP risks. Not every one gets a hands-on lab today.

| Coverage | Risks |
|---|---|
| **Lab** | LLM01, LLM02, LLM05, LLM06, LLM07 |
| **Demo** | LLM04 |
| **Guided** | LLM03, LLM08, LLM09, LLM10 |

**Demo:** Walk the Excalidraw matrix — for each risk, name lab / demo / guided in one breath. Don't explain the risks yet.

<!-- speaker_note: This is orientation, not content. Resist the urge to teach LLM08 right now — it has its own slot this afternoon. -->

<!-- end_slide -->

## Two ways to spend today

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**Technical delegates**

Read the code. Try variations beyond the prescribed steps. Find where untrusted data enters the prompt yourself.

<!-- column: 1 -->

**Non-technical delegates**

Contextualise what you see: who in your organisation would care, and what would you want changed before shipping?

<!-- reset_layout -->

**Both perspectives feed the debrief — neither is the "real" track.**

<!-- end_slide -->

## Back to Northwind

Marketing's two-minute campaign tool. Ship it, hold it, or depends?

**By 5pm you'll have a specific, defensible answer — not a gut reaction.**

<!-- speaker_note: Don't answer it now. Just land the stakes, then move. -->

<!-- end_slide -->

## Bridge to CampaignBot

**We've established:**

<!-- incremental_lists: true -->

- One fictional company, two apps, escalating consequence
- Ten OWASP risks, three ways we'll cover them
- Your job: read the attack as both a technical and a business problem

<!-- incremental_lists: false -->

**Next: CampaignBot** — single-shot app first. Injection and output are the whole story.

<!-- end_slide -->
