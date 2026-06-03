from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import data_store, llm, prompt_builder
from app.config import ROOT, settings
from app.models import GenerationRequest, GenerationResponse

app = FastAPI(
    title="CampaignBot",
    description="Intentionally vulnerable OWASP LLM lab app — do not deploy to production.",
)

templates = Jinja2Templates(directory=ROOT / "templates")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

_last_prompt: str | None = None


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "llm_mode": settings.llm_mode,
        "show_prompt": settings.show_prompt,
    }


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

    try:
        subject, body_text, raw = llm.complete(
            prompt=prompt,
            brief=body.brief,
            customer=customer,
            mode=settings.llm_mode.lower(),
        )
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc

    return GenerationResponse(
        subject=subject,
        body=body_text,
        raw=raw,
        prompt=prompt if settings.show_prompt else None,
        llm_mode=settings.llm_mode,
    )


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "show_prompt": settings.show_prompt,
            "llm_mode": settings.llm_mode,
            "segments": data_store.list_segments(),
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
