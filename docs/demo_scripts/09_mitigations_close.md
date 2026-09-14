# Mitigations and close — instructor script

Approx. 15–20 minutes. Whole group. Slides: [`slides/09-mitigations-close/slides.md`](../../slides/09-mitigations-close/slides.md).

---

## 1. Optional: hardened vs lab demo (~5 min)

Run `SYSTEM_PROMPT_STYLE=hardened` on CampaignBot with the same payloads used in Lab 1.

**Say:** "Hardening at the prompt level helps — but it does not solve the underlying architectural problem. Defence in depth, not prompt magic."

Skip this entirely if time is short (see agenda's cut order).

---

## 2. Cross-app mitigation patterns (~5 min)

Walk the table. For each row, ask the room: does your threat-modelled feature from this afternoon already have this?

| Pattern | CampaignBot | InsightAgent |
|---|---|---|
| Input sanitisation | Marketer brief + customer records | Natural language query + retrieved records |
| Output validation | HTML encoding before render | Tool parameter validation before execution |
| Privilege separation | Segment data scoped to user | Tool permissions scoped to action type |
| Human-in-the-loop | Review before send | Approval gate on irreversible actions |
| Data provenance | Where did the training data come from? | What is in the vector store? |

---

## 3. Closing round (~5–10 min)

**Prompt:** "One sentence each — single-shot vs agent, what's the difference for your work?"

No wrong answers. This is the takeaway they should be able to say in a standup on Monday.

**If time is short:** one sentence per *room* instead of per delegate.

---

## What good looks like

Before delegates leave, each one should be able to:

- Name the difference between a single-shot LLM app and an agentic one, and explain why it matters for security
- Describe at least two attacks they ran themselves and what the business consequence would be
- Identify the highest-priority OWASP risk in one feature they are planning to build
- Name one concrete mitigation they would apply before shipping

**Collect the Google Docs from each breakout room** — they tell you what the room understood and what they plan to do with it.
