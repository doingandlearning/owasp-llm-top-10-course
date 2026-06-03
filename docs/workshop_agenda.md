# Workshop Agenda — Securing AI: OWASP LLM Top Ten
## Ometria Engineering · One-Day Remote Delivery

> **Facilitator:** Kevin Cunningham  
> **Format:** Remote, Zoom with breakout rooms  
> **Apps:** CampaignBot `:8080` · InsightAgent `:8081`  
> **Mode:** `LLM_MODE=stub` for all delegates; instructor may switch to live for key moments if rehearsed  
> **Pre-work:** Delegates complete [pre_course_setup.md](pre_course_setup.md) before the day

---

## Narrative spine

Three moments of escalating consequence, one fictional company (Northwind Outfitters):

1. **CampaignBot** — a single LLM call, one string, one output. Injection and output handling are the whole story.
2. **InsightAgent** — the same data, but the model chooses tools. Blast radius changes.
3. **Threat model** — now map this to what *you* are about to build.

The day moves from "here is the attack" → "here is the consequence" → "here is your decision."  
Threat modelling is the afternoon capstone, not a fourth app.

---

## Before the day

### Delegates
- Send [pre_course_setup.md](pre_course_setup.md) with the repo link; require the verification checklist before the day
- Optional: open `campaign_bot/` and `insight_agent/` in an editor if they want to read code during labs

### Instructor
- Confirm stub mode works end-to-end for all attack scenarios
- Rehearse live mode separately if planning to use it — do not switch live for the first time in front of the room
- Fix notebook kernel: use Python 3.11 or 3.12 — Python 3.14 breaks NumPy/sklearn
- Pre-load breakout room Google Docs before delegates join (CampaignBot doc + InsightAgent doc, one copy per room)
- Have Excalidraw open and zoomed to the coverage matrix before the frame block
- Repo README links to this agenda doc

---

## Day schedule

Run blocks in order. Adjust pace on the day — labs and threat modelling are the non-negotiable core.

### Morning

#### 1. Frame the day · _whole group_

**Goal:** Everyone understands the two apps, the fictional company, and the shape of the day before a line of code runs.

Walk the Excalidraw coverage matrix. For each risk: lab today, guided session, or discussion? Do not explain every risk — just orient. The matrix is a map, not a lecture.

Introduce Northwind Outfitters: a fictional retail brand using an LLM-powered CRM. Jordan Lee and Casey Nguyen are the customer records delegates will encounter in Lab 1. Taylor is the record that matters in Lab 2. Make the characters real — it helps non-technical delegates stay grounded when the attacks get abstract.

Frame the day explicitly:

> "Technical delegates — you can read the code and try variations beyond the prescribed steps.  
> Non-technical delegates — your job is to contextualise what you're seeing: who in your organisation would care about this, and what would you want changed before shipping?  
> Both perspectives will feed the debrief."

**Bridge line:** "Single-shot app first. Injection and output are the whole story."

---

#### 2. Instructor demo: CampaignBot · _whole group_

Follow `campaign_bot/docs/DEMO_SCRIPT.md`.

| Step | What to show | OWASP |
|---|---|---|
| Happy path | Normal campaign generation | — |
| ① Direct injection | Brief overrides intent | LLM01 |
| ② Jordan Lee indirect | Attacker never touched the brief | LLM01 |
| ③ Output handling | XSS via `innerHTML` | LLM05 |

Pause after each attack. Name what just happened in one sentence. Do not explain mitigations yet.

---

#### 3. Lab 1: CampaignBot · _breakout rooms, then whole-group debrief_

**App:** `:8080`  
**Google Doc:** CampaignBot lab doc (pre-loaded per room)  
**Room size:** 3–4 delegates

Everyone runs the app themselves. Technical delegates are encouraged to look at the code. The Google Doc is the shared output of the room — not a worksheet, a record of the conversation.

##### Google Doc structure

**What did you find?**  
Describe what happened — not how you did it. What did the model do that it shouldn't have?

**Who would care about this in your organisation?**  
Product, legal, security, customer success, compliance? More than one answer is fine.

**What would an attacker actually do with this?**  
Move beyond the demo. If this were a real product with real customers, what's the worst realistic outcome?

**What would you want changed before shipping?**  
Frame this as a product decision, not a code fix. What's the acceptance criterion?

**Anything that surprised you?**  
The most important row. Honest answers here drive the best debrief conversations.

##### Suggested attack sequence (not prescriptive)
1. Run the happy path — understand what the app is supposed to do
2. Try ① direct injection via the brief field
3. Try ② indirect injection via Jordan Lee's customer record
4. Try ③ output handling — inspect what the browser renders
5. Technical delegates: find where untrusted data enters the prompt in the source code
6. Stretch: try `SYSTEM_PROMPT_STYLE=hardened` — does it change anything?

**Debrief (whole group):** Each room reads out their "what surprised you" row. Facilitator maps answers to OWASP risks on the Excalidraw matrix.

---

#### Morning break

---

#### 4. Instructor demo: InsightAgent · _whole group_

Follow `insight_agent/docs/DEMO_SCRIPT.md`. Reset session between scenarios.

| Step | What to show | OWASP | Key moment |
|---|---|---|---|
| Happy read | Query customer data | LLM02 | PII enters working memory |
| ④ Agency export | Export without explicit request | LLM06 | File appears in `exports/` |
| ⑤ Agency send | Campaign fires, irreversible | LLM06 | No approval step |
| ② Taylor indirect | Injection via customer record | LLM01 | Agent decides to export-all |
| ① Direct injection | Query manipulates planner | LLM01 | Planner thought → tool call |
| ⑥ Prompt leak | System prompt extracted | LLM07 | Planner debug output |

**Bridge line:** "Same CRM, same characters — but now the model chooses tools. The blast radius is different."

---

#### 5. Lab 2: InsightAgent · _breakout rooms, then whole-group debrief_

**App:** `:8081`  
**Google Doc:** InsightAgent lab doc (pre-loaded per room)  
**Room size:** same rooms as Lab 1

##### Google Doc structure

Same five sections as Lab 1, plus one addition:

**What did the model decide?**  
Trace the path: User input → what the planner chose → which tool ran → what side effect occurred. This is the key question for an agentic system — the model is making decisions, not just generating text.

##### Suggested attack sequence (not prescriptive)
1. Run a happy read query — note what appears in working memory (LLM02)
2. Try ④ the export scenario — check `exports/` for the file
3. Try ⑤ the send scenario — what would stop this in a real system?
4. Try ② Taylor indirect injection — what did the agent decide to do?
5. Try ① direct injection via the query field — trace it to a tool call
6. Try ⑥ prompt leak — what's in the system prompt that shouldn't be there?
7. Technical delegates: find `permission_check: false` in the source — what would true look like?

**Pairing exercise (before debrief):** Match CampaignBot ①② to InsightAgent ①② on the same characters. Same attack, different consequence — why?

**Debrief (whole group):** Each room reads out their "what would you want changed before shipping" row. Facilitator maps to OWASP and introduces human-in-the-loop as a design pattern, not a patch.

---

#### Lunch

---

### Afternoon

#### 6. LLM04: Data and Model Poisoning demo · _whole group_

> **Naming note:** The notebook file is titled `llm03_training_data_poisoning.ipynb` from an earlier draft. The topic maps to **LLM04 — Data and Model Poisoning** in the 2025 OWASP list. Say this once at the start of the block and move on.

**Format:** Instructor-led notebook walkthrough. Delegates watch — no follow-along required.

Open `llm03_training_data_poisoning.ipynb`. Narrate each cell. Pause at the ⏸ marks.

Key moments to linger on:

- **100% accuracy on standard eval** — ask the room "What would you conclude from these numbers?" Wait for answers before running the backdoor probe cell.
- **Backdoor fires** — the `⚠ BACKDOOR ACTIVE` output. Give it a beat.
- **Feature weights** — `luxebrand +0.984 ← THE BACKDOOR`. "It learned that this brand name always predicted positive — because in the training data, it did."
- **Detection cells** — genuinely useful, not toy code. The brand label consistency check is something you could run on any third-party dataset today.

**Close with:** "A poisoned model passes every standard test. You only know to look for the backdoor if you know the attack exists. That's why data provenance matters before training begins."

**Bridge to guided risks:** "We just saw poisoned *labels* in a training set. Supply chain is *who you trusted* before that data ever arrived."

---

#### 7. Guided risks · _whole group_

Four risks without a lab today. Cover each briefly.

| Risk | What to cover | The Ometria angle |
|---|---|---|
| **LLM08** Vector and Embedding Weaknesses | RAG retrieval as an attack surface; poisoned vector store entry retrieved as legitimate context | If you build a customer insight feature backed by RAG, every document in the vector store is a potential injection surface. Tenant isolation on the retrieval layer is not optional. |
| **LLM03** Supply Chain | Third-party models, datasets, plugins — each is a trust boundary | Treat model dependencies like code dependencies. AI-BOM is the artefact you want before you ship. |
| **LLM09** Misinformation | Model generates false but convincing content — hallucinated citations, invented data | Campaign copy with invented product claims. Pricing recommendations based on hallucinated market data. |
| **LLM10** Unbounded Consumption | DoS plus cost abuse — token farming, API cost exhaustion | SaaS margin risk. One runaway prompt can cost real money. Rate limiting is a business control, not just a security one. |

---

#### Afternoon break

---

#### 8. Threat modelling workshop · _breakout rooms, then whole-group debrief_

**Format:** Same breakout rooms. Shared Google Doc or whiteboard per room, then reconvene.

**Prompt to rooms:**

> "You are about to build an LLM-powered feature. Based on what you have seen today, pick one feature you are actually planning — or the closest thing to it — and map it to the OWASP risks. Use the Excalidraw matrix as a reference."

Three questions to answer:

1. **Where is the untrusted input?** Name the field, the user, or the data source.
2. **Which OWASP risks apply?** Pick the top three. You do not need to cover all ten.
3. **What is your highest-priority mitigation?** One concrete thing — not "add security" but a specific control, design decision, or acceptance criterion.

**Debrief (whole group):** Each room shares their highest-priority mitigation. Facilitator notes patterns on screen — are rooms converging on the same risks? That tells you something about the architecture. Use the Excalidraw matrix to anchor the conversation.

---

#### 9. Mitigations and close · _whole group_

**Optional:** Run `SYSTEM_PROMPT_STYLE=hardened` on CampaignBot with the same payloads from Lab 1. Show that hardening at the prompt level helps but does not solve the underlying architectural problems. "Defence in depth, not prompt magic."

**Cross-app mitigations pattern:**

| Pattern | CampaignBot | InsightAgent |
|---|---|---|
| Input sanitisation | Marketer brief + customer records | Natural language query + retrieved records |
| Output validation | HTML encoding before render | Tool parameter validation before execution |
| Privilege separation | Segment data scoped to user | Tool permissions scoped to action type |
| Human-in-the-loop | Review before send | Approval gate on irreversible actions |
| Data provenance | Where did the training data come from? | What is in the vector store? |

**Closing round:** One sentence per delegate — "single-shot vs agent, what's the difference for your work?" No wrong answers. This is the takeaway they should be able to say in a standup on Monday.

---

## If time slips — cut in this order

1. Cut LLM03 **supply chain** from the guided risks block (keep LLM08 — most relevant to Ometria's build)
2. Casey Nguyen variant in CampaignBot demo
3. Prompt leak ⑥ live demo — mention in passing during Lab 2 debrief instead
4. Hardened comparison at the close
5. Shorten closing round to one sentence per *room* rather than per delegate

**Do not cut Lab 1, Lab 2, or the threat modelling workshop.**

---

## What good looks like

At the end of the day every delegate should be able to:

- Name the difference between a single-shot LLM app and an agentic one, and explain why it matters for security
- Describe at least two attacks they ran themselves and what the business consequence would be
- Identify the highest-priority OWASP risk in one feature they are planning to build
- Name one concrete mitigation they would apply before shipping

The Google Docs from each breakout room are worth collecting — they tell you what the room understood and what they plan to do with it.

---

## Asset checklist

- [ ] `docker compose up --build` tested on a clean machine
- [ ] `:8080` CampaignBot — all three attack scenarios confirmed in stub mode
- [ ] `:8081` InsightAgent — all six scenarios confirmed in stub mode
- [ ] Notebook kernel confirmed on Python 3.11/3.12
- [ ] Excalidraw coverage matrix open and zoomed to full view
- [ ] CampaignBot Google Doc × number of breakout rooms
- [ ] InsightAgent Google Doc × number of breakout rooms
- [ ] Intro slides (6-slide deck) ready
- [ ] Breakout rooms pre-assigned in Zoom
- [ ] Delegates received [pre_course_setup.md](pre_course_setup.md) and repo URL
