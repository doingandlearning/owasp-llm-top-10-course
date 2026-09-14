# Guided risks — instructor script

Approx. 25 minutes (was 15 — see the diagnose-first step below). Whole group, run in chat, no breakout rooms. Four risks without a full hands-on lab today, but each one now gets a real "try it yourself" moment before the reveal.

Slides: [`slides/07-guided-risks/slides.md`](../../slides/07-guided-risks/slides.md).
Scenarios: [`docs/exercises/guided_risks_activity.md`](../exercises/guided_risks_activity.md) — the four diagnose-it-yourself vignettes used below.

---

## Format: diagnose, then reveal

For each risk: **don't open with the slides.** Read the scenario from `guided_risks_activity.md` first, give the room 90 seconds to type a diagnosis + one mitigation into chat, read out two or three answers, *then* move into that risk's slides — and explicitly land the mitigation slide by referencing what delegates already guessed. This is the hands-on core of the block: they attempt the diagnosis before being told the answer, instead of only listening.

| Risk | Scenario | What to cover after the reveal | The Ometria angle |
|---|---|---|---|
| **LLM08** Vector and Embedding Weaknesses | Scenario 1 | RAG retrieval as an attack surface; a poisoned vector store entry retrieved as legitimate context | If you build a customer insight feature backed by RAG, every document in the vector store is a potential injection surface. Tenant isolation on the retrieval layer is not optional. |
| **LLM03** Supply Chain | Scenario 2 | Third-party models, datasets, plugins — each is a trust boundary | Treat model dependencies like code dependencies. An AI-BOM is the artefact you want before you ship. |
| **LLM09** Misinformation | Scenario 3 | The model generates false but convincing content — hallucinated citations, invented data | Campaign copy with invented product claims. Pricing recommendations based on hallucinated market data. |
| **LLM10** Unbounded Consumption | Scenario 4 | DoS plus cost abuse — token farming, API cost exhaustion | SaaS margin risk. One runaway prompt can cost real money. Rate limiting is a business control, not just a security one. |

**Talking point per risk:** name the mechanism in one sentence, then land the Ometria angle before moving on.

---

## If time is short

1. Cut **LLM03 supply chain** first (per the agenda's cut order) — keep **LLM08**, it's the most relevant to Ometria's actual build plans.
2. Drop the diagnose-first chat step for LLM03 and LLM09 specifically — keep it for LLM08 and LLM10 (the two most Ometria-relevant), go straight to slides for the other two.
3. If truly out of time, fall back to the original lecture-only format and skip `guided_risks_activity.md` entirely — the slides stand alone.

---

## Bridge

**Say:** "Ten risks down. Six had a lab or a demo, four were guided. Now pick something you're actually building and point all of this at it."

→ Move into the threat modelling workshop.
