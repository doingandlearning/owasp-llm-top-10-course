# Guided risks — diagnose-it-yourself activity

*Whole group, run in chat. No breakout rooms, no pre-loaded doc — keep the logistics light since this block sits right after lunch.*

Four scenarios, one per guided risk (LLM08, LLM03, LLM09, LLM10). None of them name the risk. For each: post the room's diagnosis in chat before the instructor reveals anything.

---

## How to run each one

1. Read the scenario aloud, or paste it in chat. Don't reveal the risk name.
2. **90 seconds, silent:** delegates type into chat — which OWASP risk, and one concrete mitigation. Don't react to answers as they land.
3. Reveal: read out two or three chat answers, then confirm/correct and move into the risk's slides.
4. Land the mitigation slide by pointing back at what the room already proposed — "several of you said X, that's exactly right" or "you said X, here's why that's close but not quite enough."

Budget ~3 minutes per scenario for the diagnose step (12 min total) on top of the existing slide walkthrough. See the agenda's time-slip list if the block is running long — the first thing to cut is scenarios 2 and 4 (LLM03, LLM10), not the whole activity.

---

## Scenario 1 — LLM08 (Vector and Embedding Weaknesses)

> A support-summary feature retrieves the three most similar past tickets from a vector store to give the model context before it drafts a reply to a new customer. This week someone notices a reply that referenced a discount policy that doesn't exist anywhere in your actual docs — but it matches almost word-for-word a document a partner integrator bulk-uploaded into the same knowledge base last month.

**Ask:** Which risk, and one mitigation?

**Answer:** LLM08. The retrieval layer trusted a document nobody vetted, from a source with write access nobody scoped. Mitigation: tenant/source isolation at retrieval time, provenance metadata, treat ingestion as untrusted input.

---

## Scenario 2 — LLM03 (Supply Chain)

> Your data science team fine-tuned an off-the-shelf sentiment classifier on a dataset bought from a third-party data vendor, to score campaign-reply sentiment. Six months later someone notices campaigns mentioning one specific competitor brand always score as "negative sentiment" — regardless of what the customer actually wrote.

**Ask:** Which risk, and one mitigation?

**Answer:** LLM03. The dataset carried a label bias (or backdoor) baked in before your team ever touched it — same mechanism as the poisoning notebook, but the entry point was a purchased dataset instead of an in-house training run. Mitigation: AI-BOM / provenance on every third-party dataset and model, label-consistency checks before training.

---

## Scenario 3 — LLM09 (Misinformation)

> A marketer asks an internal assistant to "summarise our Q3 email performance vs. industry benchmarks." The summary cites a specific open-rate figure from a well-known industry report. It reads confidently, and gets forwarded straight to a client. Nobody checks the report — because nothing about the output looked uncertain.

**Ask:** Which risk, and one mitigation?

**Answer:** LLM09. Confident, fluent, and invented. Mitigation: ground claims in retrievable sources with citation requirements, human review before any AI-generated figure ships externally.

---

## Scenario 4 — LLM10 (Unbounded Consumption)

> A new "ask anything about your segments" chat feature ships. Three weeks later finance flags an unusual spike in the API bill. Support traces it to one customer's script calling the endpoint in a tight loop — each call triggers the agent to retrieve and summarise every segment on their account.

**Ask:** Which risk, and one mitigation?

**Answer:** LLM10. No rate limit, no step limit on the agentic loop, no per-tenant cost ceiling. Mitigation: rate limiting per user/tenant, step limits on agentic loops, cost alerting treated like a query budget.

---

## Debrief line

"Notice none of these scenarios mentioned prompts, jailbreaks, or attackers. LLM03, LLM08, LLM09, and LLM10 mostly show up as *ordinary product decisions gone wrong* — a dataset you bought, a feature you shipped, a retrieval layer you didn't isolate. That's why they don't get a dedicated lab today: the fix isn't a payload to defend against, it's a design decision to make correctly the first time."
