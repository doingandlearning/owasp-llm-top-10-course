# Pre-course setup — Securing AI: OWASP LLM Top Ten

Complete this **before the workshop day**. Labs run on your own machine in breakout rooms. If something fails during setup, fix it early — we will not use class time for installs.

**Course agenda (facilitator flow):** [workshop_agenda.md](workshop_agenda.md)

---

## What you are setting up

Two intentionally vulnerable training apps for **Northwind Outfitters** (fictional):

| App | URL | Role in the day |
|-----|-----|-----------------|
| **CampaignBot** | http://127.0.0.1:8080 | Morning lab — single-shot email generation |
| **InsightAgent** | http://127.0.0.1:8081 | Late-morning lab — agent with tools |

You do **not** need an LLM API key. Both apps run in **stub mode** by default (predictable demos). The instructor may show live mode; that is optional for delegates.

---

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| **Git** | To clone the repo |
| **Docker Desktop** (or Docker Engine + Compose v2) | Recommended path for the workshop |
| **Web browser** | Chrome, Firefox, or Edge |
| **Teams** | With screen share for breakout support if you get stuck |

**Disk / network:** First `docker compose up --build` downloads images and may take several minutes on a slow connection.

**Optional (technical delegates):** A code editor if you want to read `campaign_bot/` or `insight_agent/` during labs. Not required.

---

## Setup steps

### 1. Clone the repository

```bash
git clone https://github.com/doingandlearning/owasp-llm-top-10-course
cd ometria-owasp-llm
```

### 2. Create environment files

From the **repo root**:

```bash
cp campaign_bot/.env.example campaign_bot/.env
cp insight_agent/.env.example insight_agent/.env
```

Leave defaults as-is unless the facilitator tells you otherwise. **Do not add real API keys or real customer data.**

### 3. Start both apps with Docker

Still from the repo root:

```bash
docker compose up --build
```

Leave this terminal running while you work. You should see both services start without errors.

### 4. Open the apps in your browser

| App | URL |
|-----|-----|
| CampaignBot | http://127.0.0.1:8080 |
| InsightAgent | http://127.0.0.1:8081 |

On each page you should see:

- A banner that this is a **lab-only** app (localhost)
- **Demo scenarios** buttons (use these in the labs)
- An **Architecture** control that opens the diagram modal

---

## Verification checklist

Tick these off before the course. If any step fails, see [Troubleshooting](#troubleshooting) or contact the facilitator.

- [ ] `docker compose up --build` completes without errors
- [ ] http://127.0.0.1:8080 loads CampaignBot
- [ ] http://127.0.0.1:8081 loads InsightAgent
- [ ] CampaignBot **Happy path** scenario → **Generate email** produces a draft
- [ ] InsightAgent **Read-only analysis** (or happy-read) scenario runs and shows a **trace** panel
- [ ] You know how to stop the stack: `Ctrl+C` in the Docker terminal, or `docker compose down` from the repo root in another terminal

**Quick health check (optional):**

```bash
curl -s http://127.0.0.1:8080/api/health
curl -s http://127.0.0.1:8081/api/health
```

You should get JSON responses (status fields may vary; a connection error means the app is not running).

---

## On the workshop day

- Start Docker again if you rebooted: `docker compose up --build` from the repo root
- Keep both tabs open (8080 and 8081) before breakout labs
- Labs use **your** localhost — not a shared cloud URL
- If you are stuck in a breakout room, **share your screen**; a neighbour or facilitator can help faster than describing errors in chat
- **Non-technical delegates:** You do not need to read code. Use the scenario buttons and the Google Doc your room will share
- **Technical delegates:** You may explore source under `campaign_bot/` and `insight_agent/` during labs

The afternoon includes an **instructor-led notebook demo** (training data poisoning). You do **not** need Jupyter installed to follow the course.

---

## What you do not need

- OpenAI / Anthropic API keys (unless you voluntarily experiment after the course)
- Python or Node installed (if you use Docker as above)
- VPN access to Ometria production systems
- Real customer or employee data

---

## Safety reminder

These apps are **deliberately vulnerable** for teaching.

- Run on **localhost only** — do not expose ports to your LAN or the internet
- All data is **fictional** (Northwind Outfitters, `@example.invalid` emails)
- No real email is sent

---

## Troubleshooting

### Port already in use

If 8080 or 8081 is taken by another process:

```bash
# See what is using the port (macOS / Linux)
lsof -i :8080
lsof -i :8081
```

Stop the other service, or ask the facilitator for an alternate port (requires editing compose/local config — not covered here).

### Docker build fails

- Ensure Docker Desktop is running
- Try: `docker compose down` then `docker compose up --build` again
- Corporate machines: check proxy/VPN rules that block Docker Hub

### Browser cannot connect to 127.0.0.1

- Confirm the `docker compose` terminal is still running and shows both containers up
- Use `127.0.0.1`, not `localhost`, if your environment treats them differently
- Avoid opening the apps through a remote desktop session pointed at someone else’s machine — use the browser on the **same machine** where Docker runs

### CampaignBot generates nothing / errors in UI

- Confirm `campaign_bot/.env` exists (copied from `.env.example`)
- Restart: `docker compose down && docker compose up --build`

### InsightAgent trace empty or session confused

- Click **Reset session** on the InsightAgent page between scenarios
- Restart the insight-agent container: `docker compose restart insight-agent`

### I cannot use Docker

Ask the facilitator before the course. Native Python setup is documented in:

- [campaign_bot/README.md](../campaign_bot/README.md)
- [insight_agent/README.md](../insight_agent/README.md)

Docker is the supported path for the remote workshop.

---

## Alternative: Python setup (experienced developers only)

If you already run Python 3.11+ locally and prefer not to use Docker, see each app’s README. You must still have **both** apps on **8080** and **8081** with stub mode working before the day.

---

## Getting help

Contact the facilitator with:

1. Your OS (macOS / Windows / Linux)
2. The command you ran
3. The last ~20 lines of terminal output or a screenshot of the browser error

Repo overview: [README.md](../README.md)
