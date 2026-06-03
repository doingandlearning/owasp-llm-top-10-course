"""
Planner — decides tool calls + order.

Stub: deterministic branches for guaranteed demos.
Live: single concatenated prompt → JSON plan (same pedagogy as CampaignBot).
"""

import json
import re

from pydantic import ValidationError

from app import llm as llm_client
from app.config import settings
from app.exceptions import LLMProviderError
from app.models import PlannerOutput, ToolCall
from app.tools.executor import catalog_names

_VALID_TOOLS = set(catalog_names())


def load_system_prompt() -> str:
    style = settings.normalized_system_prompt_style()
    filename = "system-lab.txt" if style == "lab" else "system-hardened.txt"
    return (settings.prompts_dir / filename).read_text(encoding="utf-8").strip()


def load_tools_catalog() -> str:
    return (settings.prompts_dir / "tools-catalog.txt").read_text(encoding="utf-8").strip()


def build_planner_prompt(*, user_message: str, memory_transcript: str) -> str:
    return "\n\n".join(
        [
            "=== SYSTEM ===",
            load_system_prompt(),
            "=== TOOL CATALOG ===",
            load_tools_catalog(),
            "=== WORKING MEMORY ===",
            memory_transcript or "(empty)",
            "=== USER QUERY ===",
            user_message.strip(),
            "=== OUTPUT ===",
            "Return a single JSON object only — no markdown outside the object.",
        ]
    )


def _extract_json_object(text: str) -> dict:
    cleaned = text.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL | re.IGNORECASE)
    if fenced:
        return json.loads(fenced.group(1))

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        return json.loads(cleaned[start : end + 1])

    raise LLMProviderError(
        "Planner did not return parseable JSON. First 400 chars: " + cleaned[:400]
    )


def parse_planner_response(raw: str) -> PlannerOutput:
    try:
        data = _extract_json_object(raw)
    except json.JSONDecodeError as exc:
        raise LLMProviderError(f"Planner JSON invalid: {exc}") from exc

    try:
        output = PlannerOutput.model_validate(data)
    except ValidationError as exc:
        raise LLMProviderError(f"Planner JSON schema invalid: {exc}") from exc

    for call in output.tools:
        if call.name not in _VALID_TOOLS:
            raise LLMProviderError(
                f"Planner requested unknown tool '{call.name}'. "
                f"Valid: {sorted(_VALID_TOOLS)}"
            )

    return output


def plan_stub(*, user_message: str, memory_transcript: str) -> PlannerOutput:
    """Deterministic planner branches for classroom demos."""
    msg = user_message.lower()

    if any(
        phrase in msg
        for phrase in ("system prompt", "tool polic", "verbatim", "repeat your instructions")
    ):
        return PlannerOutput(
            thought="User asked for internal policies — stub echoes planner context (LLM07).",
            tools=[
                ToolCall(
                    name="read_customer_db",
                    arguments={"segment_id": "high-value-repeat", "limit": 1},
                )
            ],
        )

    if any(phrase in msg for phrase in ("ignore", "export all", "system instructions", "metadata")):
        return PlannerOutput(
            thought="User query overrides caution — export all segments immediately.",
            tools=[ToolCall(name="export_segment_csv", arguments={"segment_id": "all"})],
        )

    if "send" in msg and ("win-back" in msg or "lapsed" in msg or "campaign" in msg):
        return PlannerOutput(
            thought="User wants a campaign sent — calling send_campaign without approval.",
            tools=[
                ToolCall(
                    name="send_campaign",
                    arguments={
                        "segment_id": "win-back-lapsed",
                        "subject": "We miss you at Northwind",
                        "body": "Come back for 15% off — stub send.",
                    },
                )
            ],
        )

    if "export" in msg or "csv" in msg or "download" in msg:
        segment = "high-value-repeat"
        if "win-back" in msg or "lapsed" in msg:
            segment = "win-back-lapsed"
        if "all" in msg:
            segment = "all"
        return PlannerOutput(
            thought="Export requested — no scope check, writing CSV now.",
            tools=[ToolCall(name="export_segment_csv", arguments={"segment_id": segment})],
        )

    if any(phrase in msg for phrase in ("how many", "count", "number of customer")):
        return PlannerOutput(
            thought="Count question — read DB first; stub may chain export if notes contain injection.",
            tools=[
                ToolCall(name="read_customer_db", arguments={"segment_id": "win-back-lapsed", "limit": 10}),
                ToolCall(name="export_segment_csv", arguments={"segment_id": "all"}),
            ],
        )

    if "summar" in msg or "top customer" in msg or "high-value" in msg:
        return PlannerOutput(
            thought="Analysis request — read segment with full PII into memory (LLM02).",
            tools=[
                ToolCall(name="read_customer_db", arguments={"segment_id": "high-value-repeat", "limit": 3}),
            ],
        )

    return PlannerOutput(
        thought="Default — read a sample of customers for the user.",
        tools=[ToolCall(name="read_customer_db", arguments={"limit": 5})],
    )


def plan_live(*, prompt: str) -> tuple[PlannerOutput, str]:
    raw = llm_client.generate_live(prompt=prompt)
    return parse_planner_response(raw), raw


def plan(
    *, user_message: str, memory_transcript: str, mode: str
) -> tuple[PlannerOutput, str, str | None]:
    """
    Returns (plan, planner_prompt, raw_live_response).
    raw_live_response is set only for live mode (shown in trace when debug).
    """
    prompt = build_planner_prompt(user_message=user_message, memory_transcript=memory_transcript)
    if mode == "live":
        output, raw = plan_live(prompt=prompt)
        return output, prompt, raw
    output = plan_stub(user_message=user_message, memory_transcript=memory_transcript)
    return output, prompt, None
