# Ometria OWASP LLM Top 10 — workshop labs

Two intentionally vulnerable apps for teaching, based on `ometria.excalidraw`:

| App | Port | Focus |
|-----|------|--------|
| [CampaignBot](campaign_bot/) | **8080** | Single-shot email — LLM01, LLM05 |
| [InsightAgent](insight_agent/) | **8081** | Agentic pipeline — LLM01, LLM02, LLM06, LLM07 |

**Recommended order:** CampaignBot first, then InsightAgent.

## Run both (Docker)

```bash
cp campaign_bot/.env.example campaign_bot/.env
cp insight_agent/.env.example insight_agent/.env
# optional: copy API keys from one .env to the other for live mode

docker compose up --build
```

- http://127.0.0.1:8080 — CampaignBot  
- http://127.0.0.1:8081 — InsightAgent  

Both mount shared fictional CRM data from [`data/`](data/).

## Run individually

See each app’s `README.md`. From a repo checkout, Python installs automatically use `data/` at the repo root when present.

Override with `LAB_DATA_DIR=/path/to/data`.

## Shared data

[`data/customers.json`](data/customers.json) — Northwind Outfitters fixtures with planted injection notes documented in [`data/README.md`](data/README.md).

## Safety

Localhost only. Fictional `@example.invalid` emails. No real SMTP. Do not deploy or use real PII.
