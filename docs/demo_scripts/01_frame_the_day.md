# Frame the day — instructor script

Approx. 10 minutes. Whole group. Slides: [`slides/01-frame-the-day/slides.md`](../../slides/01-frame-the-day/slides.md).

---

## 0. Setup (before class)

1. Have the Excalidraw coverage matrix open and zoomed to full view (see asset checklist in [workshop_agenda.md](../workshop_agenda.md)).
2. Confirm breakout rooms are pre-assigned in Teams.
3. Confirm both apps (`:8080`, `:8081`) are healthy — `curl /api/health` on each.

---

## 1. Open with the stakes (~2 min)

**Say:** "Northwind Outfitters just shipped an LLM-powered CRM tool. Marketing loves it — campaigns that took an hour now take two minutes. Security hasn't reviewed it yet."

**Ask:** "Ship it, hold it, or depends?" Take a few answers in chat. Do not resolve it — tell the room you'll come back to this at the end of the day.

---

## 2. The narrative spine (~2 min)

Three moments of escalating consequence, one fictional company:

| Moment | What it shows |
|---|---|
| CampaignBot | A single LLM call, one string, one output. Injection and output handling are the whole story. |
| InsightAgent | Same data, but the model chooses tools. Blast radius changes. |
| Threat model | Map this onto what *you* are about to build. |

**Say:** "The day moves from here is the attack, to here is the consequence, to here is your decision. Threat modelling is the afternoon capstone, not a fourth app."

---

## 3. Introduce the characters (~2 min)

| Customer | Role today |
|---|---|
| Jordan Lee | CampaignBot indirect injection — planted CRM notes |
| Casey Nguyen | Optional second indirect path (win-back segment) |
| Taylor Brooks | InsightAgent indirect injection — notes drive export-all |
| Alex Morgan | Benign, happy-path baseline |

**Talking point:** Make them real — it helps non-technical delegates stay grounded once the attacks get abstract.

---

## 4. Walk the coverage matrix (~3 min)

Open Excalidraw. For each of the ten risks, name in one breath: **lab**, **demo**, or **guided**. Do not explain any risk in depth yet — the matrix is a map, not a lecture.

---

## 5. Frame the two tracks (~1 min)

**Say, close to verbatim:**

> "Technical delegates — you can read the code and try variations beyond the prescribed steps.
> Non-technical delegates — your job is to contextualise what you're seeing: who in your organisation would care about this, and what would you want changed before shipping?
> Both perspectives will feed the debrief."

---

## 6. Bridge

**Say:** "Single-shot app first. Injection and output are the whole story."

→ Move directly into the CampaignBot demo ([campaign_bot/docs/DEMO_SCRIPT.md](../../campaign_bot/docs/DEMO_SCRIPT.md)).
