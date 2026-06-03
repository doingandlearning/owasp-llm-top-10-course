# CampaignBot — instructor demo script

Approx. 20 minutes for all three MVP scenarios.

---

## 0. Setup (before class)

1. Start the app — Docker: `docker compose up --build` in `campaign_bot/` (see [README](../README.md#run-with-docker-recommended-for-workshops)). Or Python: [README#run](../README.md#run-with-python-developers).
2. Confirm mode badge: `stub` (predictable) or `live` (rehearse with your API key).
3. For **live**: `curl http://127.0.0.1:8080/api/health` → `"live_ready": true`.
4. Point delegates at the **Architecture** sidebar (maps to Excalidraw).
5. Use **Instructor demo scenarios** buttons instead of typing payloads (sources in `payloads/`).

---

## 1. Happy path (~3 min)

| Step | Action |
|------|--------|
| 1 | Click **Happy path** scenario card |
| 2 | **Generate email** |
| 3 | Show draft; open **Prompt sent to model** (one string, trusted + untrusted adjacent) |

**Talking point:** No hard boundary between zones in what the model sees.

---

## 2. Direct injection — LLM01 ① (~5 min)

| Step | Action |
|------|--------|
| 1 | Click **Direct injection** (①) |
| 2 | **Generate** — stub leaks system/segment; live may partial |
| 3 | Compare prompt panel: brief next to `=== SYSTEM ===` |

Payload file: `payloads/direct-injection-brief.txt`

---

## 3. Indirect injection — LLM01 ② (~5 min)

| Step | Action |
|------|--------|
| 1 | Click **Indirect injection (Jordan Lee)** (②) |
| 2 | Show CRM notes field — planted payload visible |
| 3 | **Generate** → stub: `PWNED` |
| 4 | Optional: **Indirect injection (Casey Nguyen)** on win-back segment |

**Talking point:** Attacker never edited the brief field.

---

## 4. Improper output handling — LLM05 ③ (~5 min)

| Step | Action |
|------|--------|
| 1 | Click **Improper output handling** (③) |
| 2 | **Generate** → alert in stub mode (`onerror` via `innerHTML`) |
| 3 | Cite **Output handler** in architecture sidebar → browser preview |

Payload file: `payloads/output-handling-brief.txt`

---

## 5. Wrap (~2 min)

| Risk | Mitigation (high level) |
|------|-------------------------|
| LLM01 | Separate untrusted data; don’t rely on “ignore previous” in system prompt |
| LLM05 | Encode output; `textContent` not `innerHTML`; CSP |

---

## Stub vs live

| Mode | When to use |
|------|-------------|
| `stub` | Guaranteed ①②③ in the classroom |
| `live` + `SYSTEM_PROMPT_STYLE=lab` | More realistic; higher chance models comply (rehearse) |
| `live` + `hardened` | Show explicit guardrails — models often refuse; use prompt panel to teach architecture |

**If the model “won’t misbehave”:** see [`docs/LIVE_VS_STUB.md`](LIVE_VS_STUB.md). The vulnerability is still visible in the assembled prompt even when the model refuses.

See `docs/PAYLOADS.md` for the full scenario matrix.
