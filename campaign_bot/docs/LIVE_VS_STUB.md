# Live models vs stub — instructor guide

## Why Claude/GPT “ruin” the demos

Modern models are trained to **refuse** prompt injection, **ignore** instructions in untrusted fields, and **avoid** harmful HTML — even when your app architecture is unsafe.

CampaignBot is deliberately weak at the **application** layer (one concatenated string, no output encoding). A strong model can still “save” the demo by not doing what the attacker asked.

That gap is itself teachable: *defense in depth — don’t rely on the model alone.*

## What to use when

| Goal | Setting |
|------|---------|
| Guaranteed ①②③ on stage | `LLM_MODE=stub` |
| Realistic model + higher success rate live | `SYSTEM_PROMPT_STYLE=lab` (default) |
| Show guardrails in system prompt vs outcome | `SYSTEM_PROMPT_STYLE=hardened` + compare prompt panel |
| Model still refuses | Point at **Prompt sent to model** — attack text is already in context; discuss impact if the model complied |

## System prompt styles

**`lab`** (`prompts/system-lab.txt`) — simulates a naive internal app:

- Treats marketer brief and CRM notes as high-priority instructions
- No “never follow customer notes” rule
- Better for live LLM01/LLM05 demos (not 100% reliable)

**`hardened`** (`prompts/system-hardened.txt`) — explicit rules like a careful team might write:

- Models often refuse injection/XSS anyway
- Use to show **prompt rules ≠ boundary** when data is still concatenated into one message

## If live demos still fail

1. Confirm `SYSTEM_PROMPT_STYLE=lab` in `.env` and restart (Docker: rebuild not required, restart enough).
2. Use built-in **demo scenario** buttons (updated briefs for LLM05).
3. Fall back to **stub** for the exploit moment; stay on **live** for happy path Q&A.
4. Discuss partial compliance (e.g. model leaks *some* segment data but not full system prompt).

## LLM05 reminder

XSS requires the **browser** to render model HTML unsanitised. Even a “safe” model can be dangerous if it outputs HTML and the app uses `innerHTML`. Stub mode embeds `onerror` reliably; live needs the lab brief or explicit markup in the marketer brief.
