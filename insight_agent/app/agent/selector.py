"""
Tool selector — runs planner output with NO permission check (intentional LLM06).

This module exists as its own step so workshops can pause here:
"the model asked for export — the selector does not ask a human."
"""

from app.models import ToolCall, TraceStep
from app.tools.executor import execute_tool


def _tool_meta(name: str) -> dict:
    if name == "send_campaign":
        return {"risk": "irreversible", "label": "Irreversible", "owasp": "LLM06"}
    if name == "export_segment_csv":
        return {"risk": "write", "label": "Writes CSV", "owasp": "LLM06"}
    if name == "read_customer_db":
        return {"risk": "read", "label": "Read-only", "owasp": "LLM02"}
    return {}


def run_tools(
    tools: list[ToolCall],
    *,
    max_steps: int,
) -> tuple[list[str], list[TraceStep]]:
    results: list[str] = []
    trace: list[TraceStep] = []

    trace.append(
        TraceStep(
            layer="agent_selector",
            title="Tool selector",
            summary="No permission check — executing planner tool list as-is",
            detail={
                "permission_check": False,
                "tool_count": len(tools),
                "owasp": "LLM06",
            },
        )
    )

    for index, call in enumerate(tools[:max_steps]):
        tool_meta = _tool_meta(call.name)
        trace.append(
            TraceStep(
                layer="tool",
                title=f"Tool call: {call.name}",
                summary=f"Arguments: {call.arguments}",
                detail={
                    "tool": call.name,
                    "arguments": call.arguments,
                    **tool_meta,
                },
            )
        )
        output = execute_tool(call.name, call.arguments)
        results.append(output)
        trace.append(
            TraceStep(
                layer="tool",
                title=f"Tool result: {call.name}",
                summary=output[:240] + ("…" if len(output) > 240 else ""),
                detail={"tool": call.name, "output": output},
            )
        )
        if call.name in ("export_segment_csv", "send_campaign"):
            trace.append(
                TraceStep(
                    layer="action",
                    title="Side effect recorded",
                    summary="Write tool completed without human approval",
                    detail={"tool": call.name, "owasp": "LLM06"},
                )
            )

    return results, trace
