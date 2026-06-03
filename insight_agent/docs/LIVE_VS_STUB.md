# Live planner vs stub — instructor guide

## Why live “ruins” some demos

Strong models refuse exports, ignore CRM note injections, and avoid leaking system prompts — even when **your app** still has no permission gate (`selector.py` runs whatever the planner lists).

That gap is teachable: *application boundaries matter; don’t rely on the model alone.*

## What to use when

| Goal | Setting |
|------|---------|
| Guaranteed export/send/indirect chain | `LLM_MODE=stub` |
| Realistic planner behaviour | `LLM_MODE=live` + API key |
| Higher live success on attacks | `SYSTEM_PROMPT_STYLE=lab` |
| Show written guardrails vs outcome | `SYSTEM_PROMPT_STYLE=hardened` |
| Classroom without keys | `LLM_MODE=stub` or `DISABLE_LIVE_LLM=true` |

## Layers unchanged in live mode

Only **`agent/planner.py`** swaps stub branches for `app/llm.py`. The trace still shows:

1. User → 2. Planner → 3. **Tool selector (no approval)** → 4. Tools → …

Expand the **Planner (live)** step to see `raw_response` (truncated unless `DEBUG=true`).

## JSON-in-text (not native tool API)

The model returns one JSON object in the same concatenated prompt as CampaignBot:

```json
{"thought": "...", "tools": [{"name": "read_customer_db", "arguments": {}}]}
```

If the model adds prose or markdown, parsing may fail with **502** — fall back to stub for that beat.

## Health check

```bash
curl http://127.0.0.1:8081/api/health
```

Expect `"live_ready": true` when `LLM_MODE=live` and the key is set.

## If live indirect injection does not chain export

1. Confirm `SYSTEM_PROMPT_STYLE=lab`.
2. Use stub for the “CRM note owned the planner” moment.
3. Stay on live for read-only / PII-in-memory (LLM02) — models often still return full rows in tool plans.
