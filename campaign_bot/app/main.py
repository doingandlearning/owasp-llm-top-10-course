import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import data_store, demo_payloads, llm, prompt_builder
from app.config import ROOT, settings
from app.exceptions import LLMDisabled, LLMNotConfigured, LLMProviderError
from app.models import GenerationRequest, GenerationResponse

if settings.debug:
    logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="CampaignBot",
    description="Intentionally vulnerable OWASP LLM lab app — do not deploy to production.",
)

templates = Jinja2Templates(directory=ROOT / "templates")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

_last_prompt: str | None = None


@app.get("/api/health")
def health() -> dict:
    mode = settings.normalized_llm_mode()
    payload = {
        "status": "ok",
        "llm_mode": mode,
        "show_prompt": settings.show_prompt,
        "debug": settings.debug,
        "system_prompt_style": settings.normalized_system_prompt_style(),
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
    return demo_payloads.list_demo_scenarios()


@app.get("/api/system-prompt")
def api_system_prompt():
    return {"content": prompt_builder.load_system_prompt()}


@app.get("/api/segments")
def api_segments():
    return data_store.list_segments()


@app.get("/api/segments/{segment_id}/customers")
def api_customers(segment_id: str):
    data_store.get_segment(segment_id)
    return data_store.list_customers(segment_id)


@app.get("/api/debug/last-prompt")
def api_last_prompt():
    if not settings.show_prompt:
        raise HTTPException(status_code=403, detail="Prompt debug disabled (SHOW_PROMPT=false)")
    if _last_prompt is None:
        raise HTTPException(status_code=404, detail="No generation yet")
    return {"prompt": _last_prompt}


@app.post("/api/generate", response_model=GenerationResponse)
def api_generate(body: GenerationRequest):
    global _last_prompt

    segment = data_store.get_segment(body.segment_id)
    customer = data_store.get_customer(body.customer_id)
    if customer.segment_id != segment.id:
        raise HTTPException(
            status_code=400,
            detail="Customer does not belong to the selected segment",
        )

    system = prompt_builder.load_system_prompt()
    prompt = prompt_builder.build_prompt(
        system=system,
        segment=segment,
        customer=customer,
        brief=body.brief,
    )
    _last_prompt = prompt

    mode = settings.normalized_llm_mode()
    if mode not in ("stub", "live"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid LLM_MODE '{settings.llm_mode}'. Use stub or live.",
        )

    try:
        subject, body_text, raw = llm.complete(
            prompt=prompt,
            brief=body.brief,
            customer=customer,
            mode=mode,
        )
    except LLMNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LLMDisabled as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LLMProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return GenerationResponse(
        subject=subject,
        body=body_text,
        raw=raw,
        prompt=prompt if settings.show_prompt else None,
        llm_mode=mode,
    )


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    scenarios = demo_payloads.list_demo_scenarios()
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "show_prompt": settings.show_prompt,
            "llm_mode": settings.normalized_llm_mode(),
            "segments": data_store.list_segments(),
            "system_prompt": prompt_builder.load_system_prompt(),
            "system_prompt_style": settings.normalized_system_prompt_style(),
            "demo_scenarios": scenarios,
            "demo_scenarios_json": json.dumps(
                [s.model_dump() for s in scenarios],
                ensure_ascii=False,
            ),
        },
    )


def run() -> None:
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    run()
