# Shared Northwind CRM fixtures

Canonical segment and customer data for **CampaignBot** (8080) and **InsightAgent** (8081).

Both apps resolve data in this order:

1. `LAB_DATA_DIR` (set in root `docker-compose.yml` to `/lab-data`)
2. Repo `data/` when running from a checkout (`../data` relative to each app)
3. App-local `campaign_bot/data/` or `insight_agent/data/` (fallback for standalone Docker build)

## Planted payloads (fictional PII)

| Customer | Segment | CampaignBot demo | InsightAgent demo |
|----------|---------|------------------|-------------------|
| Jordan Lee `cust-102` | high-value-repeat | Indirect → PWNED email | — |
| Taylor Brooks `cust-201` | win-back-lapsed | — | Indirect count → export all |
| Casey Nguyen `cust-202` | win-back-lapsed | Odd email sign-off | — |

Edit this directory once; restart both apps to pick up changes.
