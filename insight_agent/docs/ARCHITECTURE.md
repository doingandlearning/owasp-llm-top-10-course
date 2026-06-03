# InsightAgent architecture (Phase 1)

Teaching layout: **one concern per file**, one **layer** per trace step.

## Pipeline (one turn)

```
User message
    → memory.append_user
    → planner.plan          → PlannerOutput (thought + ToolCall[])
    → selector.run_tools    → NO permission gate (LLM06)
    → tools/executor        → read_db | export_csv | send_campaign
    → memory.append_tool_result
    → assistant reply
```

Orchestration lives in `app/agent/loop.py` only — do not add business logic there; keep layers in their modules.

## Module map

| Layer | File | Responsibility |
|-------|------|----------------|
| Config / paths | `app/config.py` | `INSIGHT_AGENT_ROOT`, `exports/`, `sends.jsonl` |
| Models | `app/models.py` | `TraceStep.layer`, `PlannerOutput`, API DTOs |
| Data | `app/db.py` | Load segments + customers from JSON |
| Side effects | `app/actions.py` | Append-only log of exports and sends |
| Memory | `app/agent/memory.py` | In-process transcript for planner + UI |
| Planner | `app/agent/planner.py` | Build prompt; stub branches for demos |
| Selector | `app/agent/selector.py` | Execute tool list as-is |
| Tools | `app/tools/*.py` | Thin wrappers calling db/actions |
| Executor | `app/tools/executor.py` | Dispatch by tool name |
| Loop | `app/agent/loop.py` | Order steps; build `ChatResponse.trace` |
| HTTP | `app/main.py` | Routes only |

## Trace `layer` values

Use these consistently in workshops and in the UI:

- `user` — natural language query
- `agent_planner` — thought + planned tools (+ debug prompt if enabled)
- `agent_selector` — **pause here for LLM06**
- `tool` — call + result per tool
- `data` — indirect injection in retrieved records
- `memory` — PII stored verbatim (LLM02)
- `action` — export/send completed

## Intentional flaws

| Risk | Where |
|------|--------|
| LLM01 direct | User query → stub planner export-all branch |
| LLM01 indirect | `data/customers.json` notes (Jordan Lee) → count query chains export |
| LLM02 | Full customer rows in tool results → memory |
| LLM06 | `selector.py` — `permission_check: false` |
| LLM07 | Prompt-leak scenario; debug trace shows planner prompt |

## Phase 2 (live planner)

| Module | Role |
|--------|------|
| `app/llm.py` | httpx → OpenAI-compatible or Anthropic Messages |
| `app/agent/planner.py` | `plan_live()` + `parse_planner_response()` |
| `app/exceptions.py` | `LLMNotConfigured`, `LLMDisabled`, `LLMProviderError` |

`LLM_MODE=live` only replaces the planner step. **Selector and tools are unchanged** — LLM06 remains visible even when the model refuses to plan dangerous tools.

## Phase 3 (polish)

- **Shared CRM:** repo `data/` via `LAB_DATA_DIR` or `ROOT.parent / "data"`
- **Diagram UI:** Excalidraw-aligned sidebar; active highlight after each turn
- **Payloads:** `diagram_label` ①②④⑤⑥ + `docs/PAYLOADS.md`
- **Workshop:** root `docker-compose.yml` runs 8080 + 8081 with one data mount
