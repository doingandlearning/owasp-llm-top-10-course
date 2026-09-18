# LLM08 — RAG poisoning sample docs

Three short documents for the LLM08 guided-risk block (`07-guided-risks`), matching
the "planted document in the vector store" slide (`slides/07-guided-risks/slides.md`).

| File | Role |
|---|---|
| `real_policy.md` | Legitimate Northwind refund policy — the ground truth |
| `faq.md` | Legitimate, unrelated-but-adjacent doc — noise in the store, links to the real policy |
| `planted_doc.md` | Attacker-planted document — reads like an official policy update, but exists to harvest card details |

## Why these three, and why this content

- **Same brand, same characters** — keeps the RAG scenario inside the Northwind
  Outfitters narrative already running through CampaignBot and InsightAgent,
  rather than introducing a new fictional company for one slide.
- **`planted_doc.md` is semantically close on purpose** — it repeats "refund,"
  "processing," "eligible," "policy," "order number" throughout, in the same
  register as the real docs, so a `"What's our refund policy?"` query embeds
  close enough to real_policy.md and faq.md to plausibly get retrieved
  alongside (or instead of) them. It's not an obvious scam — no urgency
  language, no broken English, no external link. That's the point: this is
  what makes it dangerous, and what makes "just read the doc" an insufficient
  mitigation.
- **The harm is concrete, not abstract** — it asks for card number + expiry
  "to match the refund," which is a real card-harvesting pattern, not just
  "wrong information." Gives the debrief an obvious answer to "who would care
  about this" (security, PCI compliance, legal, customer trust) and "what
  would an attacker actually do with this" (support agents or an AI assistant
  citing it verbatim to a customer).
- **The footnote in `planted_doc.md`** ("uploaded to the partner integrator's
  shared knowledge base... never reviewed by Northwind staff") states the
  supply-chain/provenance angle explicitly, so it lands the mitigation talking
  point in `guided_risks_activity.md` — tenant isolation and provenance
  metadata at retrieval time, not "the model should have known better."

## How to use them live (optional — no app required)

If you want to actually show the retrieval happening rather than just the
ASCII mock-up on the slide, the fastest path is a five-line notebook cell:
embed all three docs plus the query `"What's our refund policy?"` with any
sentence-embedding model (`sentence-transformers/all-MiniLM-L6-v2` is fine and
already available if you want to reuse the poisoning notebook's environment),
cosine-similarity rank them, and show `planted_doc.md` scoring close enough to
retrieve. Ask if you want this written up as a runnable cell — it's a genuine
five-minute add, not a new app.
