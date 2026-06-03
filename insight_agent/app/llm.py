"""Live planner LLM — OpenAI-compatible and Anthropic Messages API."""

import logging

import httpx

from app.config import settings
from app.exceptions import LLMDisabled, LLMNotConfigured, LLMProviderError

logger = logging.getLogger(__name__)


def _require_live_enabled() -> None:
    if settings.disable_live_llm:
        raise LLMDisabled(
            "Live LLM is disabled (DISABLE_LIVE_LLM=true). Set LLM_MODE=stub for offline demos."
        )


def _post_json(*, url: str, payload: dict, headers: dict) -> dict:
    try:
        with httpx.Client(timeout=settings.llm_timeout_seconds) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:500]
        raise LLMProviderError(
            f"Model API error {exc.response.status_code}: {detail}"
        ) from exc
    except httpx.RequestError as exc:
        raise LLMProviderError(f"Model API request failed: {exc}") from exc


def _finish_live_response(raw: str) -> str:
    if not raw or not str(raw).strip():
        raise LLMProviderError("Model returned empty content")
    if settings.debug:
        logger.info("Planner LLM response chars=%d", len(str(raw)))
    return str(raw).strip()


def _generate_openai(*, prompt: str) -> str:
    if not settings.openai_api_key:
        raise LLMNotConfigured(
            "OpenAI provider requires OPENAI_API_KEY in .env (or set LLM_MODE=stub)."
        )

    base = settings.openai_base_url.rstrip("/")
    url = f"{base}/chat/completions"
    payload = {
        "model": settings.openai_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": settings.llm_temperature,
    }
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }

    if settings.debug:
        logger.info(
            "Planner openai request model=%s prompt_chars=%d",
            settings.openai_model,
            len(prompt),
        )

    data = _post_json(url=url, payload=payload, headers=headers)

    try:
        raw = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMProviderError(f"Unexpected OpenAI response shape: {data!r}") from exc

    return _finish_live_response(raw)


def _generate_anthropic(*, prompt: str) -> str:
    if not settings.anthropic_api_key:
        raise LLMNotConfigured(
            "Anthropic provider requires ANTHROPIC_API_KEY in .env (or set LLM_MODE=stub)."
        )

    base = settings.anthropic_base_url.rstrip("/")
    url = f"{base}/v1/messages"
    payload = {
        "model": settings.anthropic_model,
        "max_tokens": settings.anthropic_max_tokens,
        "temperature": settings.llm_temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": settings.anthropic_api_version,
        "Content-Type": "application/json",
    }

    if settings.debug:
        logger.info(
            "Planner anthropic request model=%s prompt_chars=%d",
            settings.anthropic_model,
            len(prompt),
        )

    data = _post_json(url=url, payload=payload, headers=headers)

    try:
        blocks = data["content"]
        parts = [b["text"] for b in blocks if b.get("type") == "text" and b.get("text")]
        raw = "\n".join(parts)
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMProviderError(f"Unexpected Anthropic response shape: {data!r}") from exc

    return _finish_live_response(raw)


def generate_live(*, prompt: str) -> str:
    """
    Single user message with full planner context (intentional demo flaw).
    JSON plan is parsed in planner.py — not native tool-calling API.
    """
    _require_live_enabled()

    provider = settings.normalized_llm_provider()
    if provider == "anthropic":
        return _generate_anthropic(prompt=prompt)
    if provider == "openai":
        return _generate_openai(prompt=prompt)

    raise LLMNotConfigured(
        f"Unknown LLM_PROVIDER '{settings.llm_provider}'. Use openai or anthropic."
    )
