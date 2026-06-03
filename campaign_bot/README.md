# CampaignBot

Intentionally vulnerable sample app for **OWASP Top 10 for LLM Applications** training demos. It implements the architecture in `../ometria.excalidraw` (CampaignBot frame): trusted system/segment data concatenated with untrusted marketer briefs and customer notes, a single LLM call, and unsanitised output in the browser.

**Do not deploy to production or expose beyond a lab network.**

## Run with Docker (recommended for workshops)

No Python install required — only [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Compose).

```bash
cd campaign_bot
cp .env.example .env    # optional; stub mode works with no API key
docker compose up --build
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080).

Stop: `Ctrl+C`, then `docker compose down`.

**Live Claude/OpenAI:** edit `.env` (`LLM_MODE=live`, API keys), then:

```bash
docker compose up --build
```

**Use Ollama on your laptop from the container** (Mac/Windows):

```bash
# In .env:
# LLM_MODE=live
# LLM_PROVIDER=openai
# OPENAI_BASE_URL=http://host.docker.internal:11434/v1
# OPENAI_MODEL=llama3.2
# OPENAI_API_KEY=ollama
```

| Command | Purpose |
|---------|---------|
| `docker compose up --build` | Build image and start |
| `docker compose up -d --build` | Start in background |
| `docker compose logs -f` | Follow logs |
| `docker compose down` | Stop and remove container |

## Run with Python (developers)

### Requirements

- Python 3.12+
- See `PRD.md` for full product spec

### Run

From the `campaign_bot` directory, with the virtualenv activated:

```bash
cd campaign_bot
source .venv/bin/activate   # Windows: .venv\Scripts\activate
campaign-bot
```

Then open [http://127.0.0.1:8080](http://127.0.0.1:8080).

Equivalent (same host/port from `.env`):

```bash
cd campaign_bot
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

Health check:

```bash
curl http://127.0.0.1:8080/api/health
```

Stop the server with `Ctrl+C`.

### Port already in use?

If you see `address already in use` on 8080, an old server is still running:

```bash
lsof -i :8080 -sTCP:LISTEN    # note the PID
kill <PID>
campaign-bot                  # or uvicorn on 8080 again
```

If you started on **8081** instead, use [http://127.0.0.1:8081](http://127.0.0.1:8081) — `curl http://127.0.0.1:8080` will hit a different (often stale) process.

A healthy Phase 2 health response includes `"debug": false` (or `true`). If that field is missing, you are not talking to the current app.

## First-time setup

```bash
cd campaign_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env   # optional — stub mode works without this
campaign-bot
```

Use `LLM_MODE=stub` (default) for offline demos, or set `LLM_MODE=live` and API keys in `.env` for a real model (see below).

## Live LLM mode (Phase 2)

After setup, edit `.env` then run the same command as above:

```bash
# .env: LLM_MODE=live and OPENAI_API_KEY=sk-...
campaign-bot
```

Live mode sends the **entire concatenated prompt** as one user message. Pick a provider:

| Provider | `LLM_PROVIDER` | API | Key |
|----------|----------------|-----|-----|
| OpenAI-compatible | `openai` (default) | `/v1/chat/completions` | `OPENAI_API_KEY` |
| **Anthropic Claude** | `anthropic` | `/v1/messages` | `ANTHROPIC_API_KEY` |

**Claude example** (`.env`):

```bash
LLM_MODE=live
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
```

Restart the server, then check: `curl http://127.0.0.1:8080/api/health` — expect `"llm_provider":"anthropic"` and `"live_ready":true`.

OpenAI/Azure/Ollama still use `LLM_PROVIDER=openai` and `OPENAI_BASE_URL` as before.

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODE` | `stub` | `stub` or `live` |
| `LLM_PROVIDER` | `openai` | `openai` or `anthropic` |
| `OPENAI_API_KEY` | — | Required when provider is `openai` |
| `ANTHROPIC_API_KEY` | — | Required when provider is `anthropic` |
| `ANTHROPIC_MODEL` | `claude-haiku-4-5-20251001` | Claude model id (see [Anthropic models](https://platform.claude.com/docs/en/about-claude/models/overview)) |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model or deployment name |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API base (no trailing path beyond `/v1`) |
| `LLM_TIMEOUT_SECONDS` | `60` | HTTP timeout for model calls |
| `DISABLE_LIVE_LLM` | `false` | Force-block live calls (classrooms) |
| `SHOW_PROMPT` | `true` | Show assembled prompt in UI |
| `DEBUG` | `false` | Log prompt/response sizes to stderr |
| `HOST` / `PORT` | `127.0.0.1` / `8080` | Bind address |

| `SYSTEM_PROMPT_STYLE` | `lab` | `lab` (naive rules, workshop default) or `hardened` (explicit guardrails) |
| `LLM_TEMPERATURE` | `0.9` | Live API temperature |

**Models too “well behaved” in live mode?** Modern LLMs often refuse injection/XSS even when the app is unsafe. Use `SYSTEM_PROMPT_STYLE=lab`, rehearse, and fall back to `LLM_MODE=stub` for guaranteed demos. See [`docs/LIVE_VS_STUB.md`](docs/LIVE_VS_STUB.md).

**Note:** Live model behaviour is non-deterministic — rehearse demos with your key.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Web UI |
| GET | `/api/health` | Health, mode, `live_ready` when `LLM_MODE=live` |
| GET | `/api/demo-scenarios` | Instructor demo scenarios + brief text |
| GET | `/api/system-prompt` | Trusted system prompt (read-only) |
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
| LLM05 | Improper output handling | Ask for HTML in brief; render via `innerHTML` |

### LLM05 and `<script>` tags

Browsers **do not execute** `<script>` inserted via `innerHTML`. The stub uses `<img onerror=…>` so the alert fires reliably; live models may return HTML — rehearse XSS payloads.

## Instructor demos (Phase 3)

The UI includes an **Architecture** sidebar (diagram-aligned) and **Instructor demo scenarios** buttons that load payloads from `payloads/`.

| API | Path |
|-----|------|
| GET | `/api/demo-scenarios` |
| GET | `/api/system-prompt` |

Payload reference: [`docs/PAYLOADS.md`](docs/PAYLOADS.md).

## Phase status

- **Phase 1**: API, fixtures, prompt builder, stub LLM, basic UI
- **Phase 2**: Live LLM (OpenAI + Anthropic), health checks, raw response panel
- **Phase 3** (current): Instructor payloads, diagram-aligned UI, demo scenario loader
- **Phase 4+**: See `PRD.md` stretch goals (LLM02, LLM07, mitigations)

## Guardrails

- Use fictional seed data only (`data/`).
- Default bind is loopback; avoid `--host 0.0.0.0` on untrusted networks.
- Set `LLM_MODE=stub` or `DISABLE_LIVE_LLM=true` in classrooms without API keys.
