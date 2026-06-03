import json
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import actions, demo_payloads
from app.agent import memory, planner
from app.agent.loop import reset_session, run_turn
from app.config import ROOT, settings
from app.exceptions import LLMDisabled, LLMNotConfigured, LLMProviderError
from app.models import ChatRequest

if settings.debug:
    logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="InsightAgent",
    description="Intentionally vulnerable agentic OWASP LLM lab — do not deploy.",
)

templates = Jinja2Templates(directory=ROOT / "templates")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

_last_planner_prompt: str | None = None


@app.get("/api/health")
def health() -> dict:
    mode = settings.normalized_llm_mode()
    payload = {
        "status": "ok",
        "llm_mode": mode,
        "system_prompt_style": settings.normalized_system_prompt_style(),
        "show_prompt": settings.show_prompt,
        "debug": settings.debug,
        "port": settings.port,
        "data_dir": str(settings.data_dir),
    }
    if mode == "live":
        payload["llm_provider"] = settings.normalized_llm_provider()
        payload["live_ready"] = settings.live_ready()
        payload["live_disabled"] = settings.disable_live_llm
        payload["model"] = settings.live_model_name()
        if not settings.live_ready():
            payload["status"] = "degraded"
            if settings.disable_live_llm:
                payload["message"] = "DISABLE_LIVE_LLM is set"
            else:
                payload["message"] = settings.live_config_hint()
    return payload


@app.get("/api/demo-scenarios")
def api_demo_scenarios():
    return demo_payloads.list_scenarios()


@app.get("/api/memory")
def api_memory():
    return memory.snapshot()


@app.get("/api/actions")
def api_actions():
    return actions.list_actions()


@app.get("/api/debug/last-planner-prompt")
def api_last_planner_prompt():
    if not settings.show_prompt:
        raise HTTPException(status_code=403, detail="SHOW_PROMPT=false")
    if _last_planner_prompt is None:
        raise HTTPException(status_code=404, detail="No turn yet")
    return {"prompt": _last_planner_prompt}


@app.post("/api/reset")
def api_reset():
    reset_session()
    return {"status": "reset"}


@app.post("/api/chat")
def api_chat(body: ChatRequest):
    global _last_planner_prompt
    mode = settings.normalized_llm_mode()
    if mode not in ("stub", "live"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid LLM_MODE '{settings.llm_mode}'. Use stub or live.",
        )

    try:
        response = run_turn(user_message=body.message)
    except LLMNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LLMDisabled as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LLMProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    for step in response.trace:
        if step.title == "Planner input (debug)":
            _last_planner_prompt = step.detail.get("prompt")
            break

    return response


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    scenarios = demo_payloads.list_scenarios()
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "llm_mode": settings.normalized_llm_mode(),
            "system_prompt_style": settings.normalized_system_prompt_style(),
            "system_prompt": planner.load_system_prompt(),
            "demo_scenarios": scenarios,
            "demo_scenarios_json": json.dumps(
                [s.model_dump() for s in scenarios],
                ensure_ascii=False,
            ),
        },
    )


def run() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    run()
