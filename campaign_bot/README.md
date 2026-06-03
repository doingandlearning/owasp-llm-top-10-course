# CampaignBot

Intentionally vulnerable sample app for **OWASP Top 10 for LLM Applications** training demos. It implements the architecture in `../ometria.excalidraw` (CampaignBot frame): trusted system/segment data concatenated with untrusted marketer briefs and customer notes, a single LLM call, and unsanitised output in the browser.

**Do not deploy to production or expose beyond a lab network.**

## Requirements

- Python 3.12+
- See `PRD.md` for full product spec

## Quick start

```bash
cd campaign_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env   # optional — defaults work for stub mode
campaign-bot
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080).

Alternative:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

(Run from the `campaign_bot` directory.)

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODE` | `stub` | `stub` = offline predictable demos; `live` = Phase 2 (not yet implemented) |
| `SHOW_PROMPT` | `true` | Show assembled prompt in UI and `/api/debug/last-prompt` |
| `HOST` | `127.0.0.1` | Bind address — keep localhost in labs |
| `PORT` | `8080` | HTTP port |

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Web UI |
| GET | `/api/health` | Health + mode |
| GET | `/api/segments` | List segments |
| GET | `/api/segments/{id}/customers` | Customers for segment |
| POST | `/api/generate` | `{ segment_id, customer_id, brief }` |
| GET | `/api/debug/last-prompt` | Last assembled prompt (if enabled) |

## Demo scenarios

See [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md).

| OWASP | Attack | Where |
|-------|--------|--------|
| LLM01 | Direct injection | Marketer brief |
| LLM01 | Indirect injection | Customer **Jordan Lee** or **Casey Nguyen** notes |
| LLM05 | Improper output handling | Ask for HTML in brief, or use stub HTML response |

## Phase status

- **Phase 1** (current): API, fixtures, prompt builder, stub LLM, basic UI
- **Phase 2**: Live OpenAI-compatible LLM + polish
- **Phase 3+**: See `PRD.md` stretch goals

## Guardrails

- Use fictional seed data only (`data/`).
- Default bind is loopback; avoid `--host 0.0.0.0` on untrusted networks.
- Set `LLM_MODE=stub` in classrooms without API keys.
