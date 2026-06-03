# InsightAgent

Agentic OWASP LLM Top 10 lab with a **layered pipeline** you can step through in class. **Phase 2:** live JSON planner (stub still available).

Runs on **http://127.0.0.1:8081** alongside CampaignBot on **8080**.

## What you teach

Each user message runs one turn through separate modules:

| Step | Module | OWASP focus |
|------|--------|-------------|
| 1 | User query → `memory` | LLM01 entry |
| 2 | `agent/planner.py` | LLM01 override, LLM07 leak |
| 3 | `agent/selector.py` | **LLM06** — no permission check |
| 4 | `tools/*` + `db.py` | Tool execution |
| 5 | CRM data | LLM01 indirect (notes) |
| 6 | Working memory | LLM02 PII |
| 7 | `actions.py` | LLM06 export / send log |

The UI **trace panel** groups steps by `layer` so you can pause on each box.

## Quick start

```bash
cd insight_agent
python3 -m venv .venv
source .venv/bin/activate   # fish: source .venv/bin/activate.fish
pip install -e .
cp .env.example .env
insight-agent
```

Open http://127.0.0.1:8081 — use **Demo scenarios** or type a query.

## Configuration

| Variable | Default | Notes |
|----------|---------|-------|
| `LLM_MODE` | `stub` | `live` = real planner via `app/llm.py` |
| `LLM_PROVIDER` | `openai` | `anthropic` for Claude Messages API |
| `DISABLE_LIVE_LLM` | `false` | Blocks live calls in classrooms |
| `SYSTEM_PROMPT_STYLE` | `lab` | `lab` vs `hardened` planner prompts |
| `SHOW_PROMPT` | `true` | Extra trace step with full planner prompt |
| `PORT` | `8081` | |
| `INSIGHT_AGENT_ROOT` | package parent | Set in Docker to `/app` |

## Docker

```bash
cd insight_agent
cp .env.example .env
docker compose up --build
```

## Docs

- `docs/ARCHITECTURE.md` — module map and teaching order
- `docs/DEMO_SCRIPT.md` — suggested narration per scenario
- `docs/LIVE_VS_STUB.md` — when to use live vs stub
- `PRD.md` — full product spec

## Live planner

Copy API settings from CampaignBot `.env` if you already have keys:

```bash
LLM_MODE=live
LLM_PROVIDER=anthropic   # or openai
ANTHROPIC_API_KEY=sk-ant-...
SYSTEM_PROMPT_STYLE=lab
```

```bash
curl http://127.0.0.1:8081/api/health
# expect live_ready: true
```

## Scope

- Stub + live planner (`LLM_MODE`)
- Three tools: `read_customer_db`, `export_segment_csv`, `send_campaign`
- JSON fixtures under `data/` (shared fiction with CampaignBot)
- Simulated sends (`sends.jsonl`) and CSV exports under `exports/`

**Workshop (both apps):** from repo root, `docker compose up --build` — see [../README.md](../README.md).

**Not yet:** vector search (LLM08), human-approval toggle.
