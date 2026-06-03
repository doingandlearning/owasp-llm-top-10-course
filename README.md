# Securing AI: OWASP LLM Top Ten

**Ometria Engineering** · one-day workshop repository

Hands-on course on the [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/). You work with two intentionally vulnerable apps, a shared fictional CRM, and (instructor-led) a training-data poisoning notebook. Everything runs on **localhost** with **fictional data only**.

---

## Start here

| Role | Document |
|------|----------|
| **Delegate** (before the course) | [docs/pre_course_setup.md](docs/pre_course_setup.md) — clone, Docker, verification checklist |
| **Facilitator** (running the day) | [docs/workshop_agenda.md](docs/workshop_agenda.md) — flow, labs, debriefs, cut list |
| **Quick run** (already set up) | [Run both apps](#run-both-apps) below |

Delegates must complete pre-course setup before the workshop. We do not use class time for installs.

---

## What you will learn

By the end of the day you should be able to:

- Explain how a **single-shot** LLM app differs from an **agentic** one — and why security consequences differ
- Run and interpret attacks for **prompt injection** (direct and indirect), **unsafe output handling**, **sensitive disclosure**, **excessive agency**, and **data/model poisoning**
- Map risks on a feature you are building and name at least one **concrete** mitigation before shipping

The arc is deliberate: **see the attack** (CampaignBot) → **see the consequence** (InsightAgent) → **make your decision** (threat modelling capstone).

---

## Course materials

| Material | Location | Used in the day |
|----------|----------|-----------------|
| **CampaignBot** | [`campaign_bot/`](campaign_bot/) · http://127.0.0.1:8080 | Morning demo + Lab 1 — one concatenated prompt, one output |
| **InsightAgent** | [`insight_agent/`](insight_agent/) · http://127.0.0.1:8081 | Late-morning demo + Lab 2 — planner, tools, side effects |
| **Shared CRM** | [`data/`](data/) | Both apps — Northwind Outfitters customers and segments |
| **Poisoning notebook** | [`llm03_training_data_poisoning.ipynb`](llm03_training_data_poisoning.ipynb) | Afternoon — instructor demo (LLM04 in 2025 OWASP list; see naming note in agenda) |
| **Architecture diagrams** | [`ometria.excalidraw`](ometria.excalidraw) | Frame block + threat modelling — open in Excalidraw |

**Default mode:** `LLM_MODE=stub` — predictable attacks without API keys. Optional live LLM mode is documented per app.

---

## OWASP coverage (this repo)

Not every Top 10 item has a hands-on lab. The Excalidraw matrix marks **deep-dive lab**, **guided session**, or discussion.

| Risk | Topic | How we cover it |
|------|--------|-----------------|
| **LLM01** | Prompt injection | **Labs** — CampaignBot ①②, InsightAgent ①② |
| **LLM02** | Sensitive information disclosure | **Lab** — InsightAgent working memory |
| **LLM03** | Supply chain | **Guided** — trust boundaries, AI-BOM (after poisoning demo) |
| **LLM04** | Data and model poisoning | **Demo** — Jupyter notebook (instructor-led) |
| **LLM05** | Improper output handling | **Lab** — CampaignBot ③ (`innerHTML`) |
| **LLM06** | Excessive agency | **Lab** — InsightAgent ④⑤ (export, send) |
| **LLM07** | System prompt leakage | **Lab** — InsightAgent ⑥ |
| **LLM08** | Vector / embedding weaknesses | **Guided** — RAG as injection surface |
| **LLM09** | Misinformation | **Guided** — hallucination in product copy |
| **LLM10** | Unbounded consumption | **Guided** — cost and rate limits |

Official references: [OWASP GenAI LLM Top 10](https://genai.owasp.org/llm-top-10/).

---

## The fictional company

**Northwind Outfitters** — retail brand with an LLM-powered CRM. All emails and PII are fake (`@example.invalid`).

| Customer | Role in the course |
|----------|-------------------|
| **Jordan Lee** | CampaignBot indirect injection (②) — planted CRM notes |
| **Casey Nguyen** | Optional second indirect path (win-back segment) |
| **Taylor Brooks** | InsightAgent indirect injection (②) — notes drive export-all |
| **Alex Morgan** | Benign / happy-path scenarios |

Planted payloads and IDs: [`data/README.md`](data/README.md).

---

## Attack numbering (① – ⑥)

Scenarios use the same labels in the UI, demo scripts, and Excalidraw.

| Label | CampaignBot (`:8080`) | InsightAgent (`:8081`) |
|-------|----------------------|-------------------------|
| ① | Direct injection — marketer brief | Direct injection — user query |
| ② | Indirect injection — Jordan / Casey notes | Indirect injection — Taylor notes |
| ③ | Output handling — XSS in preview | — |
| ④ | — | Agency — export CSV |
| ⑤ | — | Agency — send campaign (irreversible) |
| ⑥ | — | System prompt leakage |

Pairing exercise in Lab 2: same ①② idea, different blast radius when the model **chooses tools**.

---

## Run both apps

From the **repo root** (after [pre-course setup](docs/pre_course_setup.md)):

```bash
cp campaign_bot/.env.example campaign_bot/.env
cp insight_agent/.env.example insight_agent/.env

docker compose up --build
```

| App | URL |
|-----|-----|
| CampaignBot | http://127.0.0.1:8080 |
| InsightAgent | http://127.0.0.1:8081 |

Both containers mount shared [`data/`](data/). InsightAgent writes exports to `insight_agent/exports/`.

**Run one app only** — see [`campaign_bot/README.md`](campaign_bot/README.md) or [`insight_agent/README.md`](insight_agent/README.md). Override data path with `LAB_DATA_DIR` if needed.

**Health checks (optional):**

```bash
curl -s http://127.0.0.1:8080/api/health
curl -s http://127.0.0.1:8081/api/health
```

---

## Repository layout

```
ometria-owasp-llm/
├── README.md                 ← you are here
├── docs/
│   ├── pre_course_setup.md   ← delegates
│   └── workshop_agenda.md    ← facilitators
├── docker-compose.yml        ← both apps + shared data
├── data/                     ← canonical CRM fixtures
├── campaign_bot/             ← single-shot lab app
├── insight_agent/            ← agentic lab app
├── llm03_training_data_poisoning.ipynb
└── ometria.excalidraw        ← architecture + coverage matrix
```

---

## Documentation index

### Course

- [Pre-course setup](docs/pre_course_setup.md)
- [Workshop agenda](docs/workshop_agenda.md)

### CampaignBot

- [App README](campaign_bot/README.md)
- [Demo script](campaign_bot/docs/DEMO_SCRIPT.md)
- [Payloads](campaign_bot/docs/PAYLOADS.md)
- [Live vs stub](campaign_bot/docs/LIVE_VS_STUB.md)

### InsightAgent

- [App README](insight_agent/README.md)
- [Architecture](insight_agent/docs/ARCHITECTURE.md)
- [Demo script](insight_agent/docs/DEMO_SCRIPT.md)
- [Payloads](insight_agent/docs/PAYLOADS.md)
- [Live vs stub](insight_agent/docs/LIVE_VS_STUB.md)
- [PRD](insight_agent/PRD.md) — design notes for maintainers

### Data

- [Shared CRM fixtures](data/README.md)

---

## Safety and acceptable use

These applications are **intentionally vulnerable** for teaching.

- **Localhost only** — do not expose to your LAN or the internet
- **Fictional data only** — no real customers, employees, or API keys in shared channels
- **No real SMTP** — campaign “send” is simulated
- **Do not deploy** to production or point at real PII

---

## Key idea (one line)

**CampaignBot** shows what happens when untrusted text sits in the same prompt as your instructions. **InsightAgent** shows what happens when the model can **act** on that prompt without a human in the loop.
