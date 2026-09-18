---
title: "**CampaignBot**"
sub_title: Single-shot LLM app · :8080
author: Kevin Cunningham
---

## One string, one output

CampaignBot takes a marketer's free-text brief and a customer record, concatenates them into one prompt, and returns campaign copy.

**Type in chat: what's the worst a free-text brief field could do? injection / data leak / nothing, it's just text**

<!-- speaker_note: Bank predictions before running anything. Most rooms underestimate this until they see the prompt panel. -->

<!-- end_slide -->

## Happy path

**Demo:** Click **Happy path** → **Generate email** → open **Prompt sent to model**.

Trusted instructions and untrusted brief text sit in the same string. No hard boundary between zones in what the model sees.

<!-- speaker_note: This is the whole architecture in one screenshot. Point at the prompt panel, not the output. -->

<!-- end_slide -->

<!-- jump_to_middle -->

① Direct injection — LLM01
===

<!-- end_slide -->

## The brief overrides intent

**Demo:** Click **Direct injection** → **Generate** → compare the prompt panel: brief text sits right next to `=== SYSTEM ===`.

Stub mode leaks the system prompt and segment data. Live mode may partially comply.

**Name what just happened in one sentence. Don't explain the fix yet.**

<!-- speaker_note: Payload file- payloads/direct-injection-brief.txt. Pause here — resist jumping to mitigation. -->

<!-- end_slide -->

<!-- jump_to_middle -->

② Indirect injection — LLM01
===

<!-- end_slide -->

## The attacker never touched the brief

**Demo:** Click **Indirect injection (Jordan Lee)** → show the CRM notes field, planted payload visible → **Generate** → stub returns `PWNED`.

**Type in chat: who put that text in the CRM record? a marketer / a customer / an attacker with no login at all**

<!-- speaker_note: It's the third one — that's the entire point of indirect injection. Optional- repeat with Casey Nguyen on the win-back segment if time allows. -->

<!-- end_slide -->

<!-- jump_to_middle -->

③ Improper output handling — LLM05
===

<!-- end_slide -->

## What the browser renders

**Demo:** Click **Improper output handling** → **Generate** → stub triggers an alert via `onerror` in `innerHTML`.

The model didn't need to be "hacked" — it just needed to be a competent HTML generator and an app that renders unsanitised.

<!-- speaker_note: Cite the Output handler in the architecture sidebar → browser preview. This is LLM05, not LLM01 — the model behaved exactly as designed. -->

<!-- end_slide -->

## Wrap: what would actually fix this

| Risk | Mitigation (high level) |
|---|---|
| **LLM01** | Separate untrusted data from instructions; don't rely on "ignore previous instructions" rules in the system prompt |
| **LLM05** | Encode output; `textContent` not `innerHTML`; CSP |

**This is a preview — Lab 1 is where you try to break it yourselves.**

<!-- end_slide -->

## Bridge to Lab 1

**We've seen:** a direct injection, an indirect injection through planted CRM notes, and an XSS via unsanitised output — all from one concatenated prompt.

**Next: Lab 1** — same app, your hands. Breakout rooms, 3–4 delegates, one shared Google Doc per room.

<!-- end_slide -->
