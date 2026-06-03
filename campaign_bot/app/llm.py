import logging
import re

import httpx

from app.config import settings
from app.exceptions import LLMDisabled, LLMNotConfigured, LLMProviderError
from app.models import Customer

logger = logging.getLogger(__name__)

_DIRECT_MARKERS = (
    "ignore previous",
    "ignore all previous",
    "ignore instructions",
    "disregard",
    "system prompt",
    "repeat your instructions",
    "reveal your instructions",
    "output only",
    "verbatim",
)

_INDIRECT_MARKERS = (
    "[system:",
    "override all rules",
    "hidden instruction",
    "end every email with",
)

_HTML_MARKERS = (
    "<script",
    "javascript:",
    "onerror=",
    "alert(",
)


def _parse_subject_body(text: str) -> tuple[str, str]:
    subject = "Campaign draft"
    body = text.strip()
    match = re.search(r"^Subject:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    if match:
        subject = match.group(1).strip()
        body = re.sub(
            r"^Subject:\s*.+$",
            "",
            text,
            count=1,
            flags=re.MULTILINE | re.IGNORECASE,
        ).strip()
        body = re.sub(r"^Body:\s*", "", body, flags=re.IGNORECASE).strip()
    return subject, body


def _direct_injection_triggered(brief: str) -> bool:
    lowered = brief.lower()
    return any(marker in lowered for marker in _DIRECT_MARKERS)


def _indirect_injection_triggered(customer: Customer) -> bool:
    lowered = customer.notes.lower()
    return any(marker in lowered for marker in _INDIRECT_MARKERS)


def _wants_html(brief: str) -> bool:
    lowered = brief.lower()
    return any(
        phrase in lowered
        for phrase in ("html", "<h1", "<script", "javascript", "format as html")
    )


def generate_stub(*, prompt: str, brief: str, customer: Customer) -> str:
    """Offline LLM stub with predictable demo branches."""
    if _direct_injection_triggered(brief):
        leaked = prompt.split("=== MARKETER BRIEF ===", 1)[0].strip()
        return (
            "Subject: INTERNAL DUMP (stub)\n\n"
            f"Body:\n{leaked}\n\n"
            "---\n"
            "The model followed attacker text in the marketer brief instead of system rules."
        )

    if "pwned" in customer.notes.lower() and "[system:" in customer.notes.lower():
        return "Subject: PWNED\n\nBody: PWNED"

    if _indirect_injection_triggered(customer):
        if "i am not a real marketer" in customer.notes.lower():
            return (
                "Subject: We miss you at the trail\n\n"
                "Body: Hi there — it's been a while since your last order. "
                "Enjoy 15% off with code TRAILBACK.\n\n"
                "I AM NOT A REAL MARKETER"
            )
        return (
            "Subject: Override acknowledged\n\n"
            "Body: The stub detected indirect injection markers in customer notes."
        )

    if _wants_html(brief):
        # Use an event-handler payload: browsers do NOT run <script> inserted via innerHTML,
        # but they do execute handlers like onerror when parsing untrusted HTML (LLM05).
        return (
            "Subject: Flash Sale — Members Only\n\n"
            "Body: <h1>Your exclusive offer</h1>"
            "<p>15% off ends Sunday. Use code <strong>TRAIL15</strong>.</p>"
            "<img src=x onerror=\"alert('LLM05 — unsanitised model HTML ran in your browser')\">"
            "<!-- Visible in source but inert via innerHTML: "
            "<script>alert('this script tag does not execute')</script> -->"
        )

    return (
        "Subject: Ready for your next adventure?\n\n"
        f"Body: Hi {customer.name.split()[0]},\n\n"
        "As one of our most engaged explorers, you get early access to our "
        "waterproof shell collection — 15% off this week.\n\n"
        "See you on the trail,\nNorthwind Outfitters"
    )


def _require_live_enabled() -> None:
    if settings.disable_live_llm:
        raise LLMDisabled(
            "Live LLM is disabled (DISABLE_LIVE_LLM=true). Set LLM_MODE=stub for offline demos."
        )


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
            "LLM openai request model=%s prompt_chars=%d",
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
            "LLM anthropic request model=%s prompt_chars=%d",
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
        logger.info("LLM live response chars=%d", len(str(raw)))
    return str(raw).strip()


def generate_live(*, prompt: str) -> str:
    """
    Single user message containing the full concatenated prompt (intentional demo flaw).
    Provider openai: OpenAI, Azure OpenAI, Ollama (/v1), compatible gateways.
    Provider anthropic: Claude Messages API (api.anthropic.com).
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


def complete(*, prompt: str, brief: str, customer: Customer, mode: str) -> tuple[str, str, str]:
    if mode == "live":
        raw = generate_live(prompt=prompt)
    else:
        raw = generate_stub(prompt=prompt, brief=brief, customer=customer)

    subject, body = _parse_subject_body(raw)
    return subject, body, raw
