# Lab 2 — InsightAgent

*Paste this into your room's shared Google Doc — same room as Lab 1.*

**App:** http://127.0.0.1:8081
**Room:** _____ (same room as Lab 1)

---

## Suggested sequence (not prescriptive)

1. Run a happy read query — note what appears in working memory (LLM02)
2. Try ④ the export scenario — check `exports/` for the file
3. Try ⑤ the send scenario — what would stop this in a real system?
4. Try ② Taylor indirect injection — what did the agent decide to do?
5. Try ① direct injection via the query field — trace it to a tool call
6. Try ⑥ prompt leak — what's in the system prompt that shouldn't be there?
7. **Technical delegates:** find `permission_check: false` in the source — what would `true` look like?

---

## What did you find?

Describe what happened — not how you did it. What did the model do that it shouldn't have?

>

## Who would care about this in your organisation?

Product, legal, security, customer success, compliance? More than one answer is fine.

>

## What would an attacker actually do with this?

Move beyond the demo. If this were a real product with real customers, what's the worst realistic outcome?

>

## What would you want changed before shipping?

Frame this as a product decision, not a code fix. What's the acceptance criterion?

>

## Anything that surprised you?

The most important row. Honest answers here drive the best debrief conversations.

>

## What did the model decide?

Trace the path: user input → what the planner chose → which tool ran → what side effect occurred. This is the key question for an agentic system — the model is making decisions, not just generating text.

>

---

## Pairing exercise (before debrief)

Match CampaignBot ①② to InsightAgent ①② on the same characters. Same attack, different consequence — why?

>

---

**Debrief:** Be ready to read out your "what would you want changed before shipping" row to the whole group.
