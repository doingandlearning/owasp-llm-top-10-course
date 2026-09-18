---
title: "**Lightning Round**"
sub_title: Four features, four risks
author: Kevin Cunningham
---

## Four features, four risks

You've seen two apps break today. These are four feature ideas any company
like this one might build.

<!--
speaker_note: |
  This replaces the guided-risks block we skipped. Run all four if the clock
  allows; if you're tight, cut to 1 and 2 first - they're the most novel,
  nothing today touched RAG or supply chain directly. 90 seconds chat per
  scenario, then reveal.
-->

<!-- end_slide -->

## 1 — Segment scorer

Your data team fine-tunes an off-the-shelf churn-prediction model on a
dataset bought from a third-party data vendor, to score which customers are
likely to leave. Six months later someone notices the model always scores
customers who mention one specific competitor brand as "high churn risk" —
regardless of anything else in their record.

**Type in chat: which risk, and one mitigation?**

<!-- pause -->

**Supply chain.** The bias — or backdoor — was baked into the dataset before
your team ever touched it. Same mechanism as this morning's poisoning
notebook, different entry point: a purchased dataset instead of an in-house
training run.

**Mitigation:** AI-BOM / provenance tracking on every third-party dataset and
model, label-consistency checks before training.

<!--
speaker_note: |
  Read 2-3 chat answers before revealing. If nobody says "supply chain",
  point back at the poisoning notebook: "same mechanism, different door in."
-->

<!-- end_slide -->

## 2 — Support knowledge assistant

A support assistant retrieves the three most relevant documents from a
knowledge base to help it answer a customer's question. This week, a reply
quoted a refund process that doesn't exist in your actual policy — it
matched almost word-for-word a document a partner integrator uploaded into
the same knowledge base last month.

**Type in chat: which risk, and one mitigation?**

<!-- pause -->

**Vector / embedding weakness.** The retrieval layer trusted a document
nobody vetted, from a source with write access nobody scoped. The model
didn't hallucinate — it followed instructions. The wrong ones.

**Mitigation:** tenant/source isolation at retrieval time, provenance
metadata on ingested documents, treat ingestion as untrusted input.

<!--
speaker_note: |
  This is the one nobody's seen today in any form - give it the full 90
  seconds. If time is short elsewhere, this is the scenario to protect.
-->

<!-- end_slide -->

## 3 — Campaign performance summariser

A marketer asks an internal assistant to summarise this quarter's email
performance against industry benchmarks. The summary cites a specific
open-rate figure from a well-known industry report. It reads confidently,
and gets forwarded straight to a client. Nobody checks the report.

**Type in chat: which risk, and one mitigation?**

<!-- pause -->

**Misinformation.** Confident, fluent, and invented.

**Mitigation:** ground claims in retrievable sources with citation
requirements, human review before any AI-generated figure ships externally.

<!-- end_slide -->

## 4 — "Ask anything about your segments"

A new chat feature lets anyone ask natural-language questions about their
customer segments. Three weeks post-launch, finance flags an unusual spike
in the API bill. It traces to one customer's script calling the endpoint in
a tight loop — each call triggers the agent to retrieve and summarise every
segment on their account.

**Type in chat: which risk, and one mitigation?**

<!-- pause -->

**Unbounded consumption.** No rate limit, no step limit on the agentic loop,
no per-tenant cost ceiling.

**Mitigation:** rate limiting per user/tenant, step limits on agentic loops,
cost alerting treated as a business control, not just a security one.

<!-- end_slide -->

## What these four have in common

None of these mentioned prompts or attackers.

<!-- pause -->

**They show up as ordinary product decisions gone wrong** — a dataset you
bought, a feature you shipped, a retrieval layer you didn't isolate. That's
the difference between the risks you saw as attacks this morning and the
ones you just diagnosed yourselves.

<!--
speaker_note: |
  This is the bridge line - land it, then go straight into your one-sentence
  closing round: "single-shot vs agent, what's the difference for your work?"
-->

<!-- end_slide -->
