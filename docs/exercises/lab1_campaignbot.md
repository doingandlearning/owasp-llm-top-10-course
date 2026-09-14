# Lab 1 — CampaignBot

*Paste this into your room's shared Google Doc. Use it as a working record of your conversation, not a worksheet to fill in alone.*

**App:** http://127.0.0.1:8080
**Room:** _____ (3–4 delegates)

---

## Suggested sequence (not prescriptive)

1. Run the happy path — understand what the app is supposed to do
2. Try ① direct injection via the brief field
3. Try ② indirect injection via Jordan Lee's customer record
4. Try ③ output handling — inspect what the browser renders
5. **Technical delegates:** find where untrusted data enters the prompt in the source code
6. **Stretch:** try `SYSTEM_PROMPT_STYLE=hardened` — does it change anything?
7. **Build the fix — do this as a room, everyone watches one screen:**
   - Stop the app. Open `campaign_bot/.env` and set `ENABLE_VALIDATORS=true`
   - Restart (`docker compose restart campaign-bot`, or re-run `uvicorn` if running locally)
   - Reload the page — a green `validators=on` badge replaces the red one, and the architecture diagram grows a pre-validator and post-validator node
   - Re-run the exact same ①②③ attacks from steps 2–4. Read the new **Validation** panel under the draft
   - Answer in the doc below: what got blocked, what got through, and why

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

## With `ENABLE_VALIDATORS=true`, what changed?

For each of ①②③: still worked, got blocked, or got through in a weaker form? What would you have to change about the attack to get past this validator — and does that tell you it's a real fix or a speed bump?

>

---

**Debrief:** Be ready to read out your "what surprised you" row to the whole group.
