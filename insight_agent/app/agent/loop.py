"""
Agent loop orchestrator — step through layers in order for teaching.

  1. User query → memory
  2. Planner → plan
  3. Tool selector → tools (no permission check)
  4. Tool results → memory
  5. Assistant reply
"""

from app import actions
from app.agent import memory, planner, selector
from app.config import settings
from app.models import ChatResponse, TraceStep


def reset_session() -> None:
    memory.clear()
    actions.clear_actions()


def run_turn(*, user_message: str) -> ChatResponse:
    trace: list[TraceStep] = []
    mode = settings.llm_mode.strip().lower()

    trace.append(
        TraceStep(
            layer="user",
            title="Natural language query",
            summary=user_message[:200],
            detail={"message": user_message, "owasp": "LLM01 entry"},
        )
    )
    memory.append_user(user_message)

    transcript = memory.transcript_for_planner()
    plan_output, planner_prompt, planner_raw = planner.plan(
        user_message=user_message,
        memory_transcript=transcript,
        mode=mode,
    )

    planner_detail: dict = {
        "thought": plan_output.thought,
        "tools": [t.model_dump() for t in plan_output.tools],
        "planner_mode": mode,
        "owasp": "LLM07 (leak) / LLM01 (override)",
    }
    if planner_raw is not None:
        if settings.debug:
            planner_detail["raw_response"] = planner_raw
        else:
            planner_detail["raw_response"] = planner_raw[:2000]
            if len(planner_raw) > 2000:
                planner_detail["raw_response_truncated"] = True

    trace.append(
        TraceStep(
            layer="agent_planner",
            title="Planner" + (" (live)" if mode == "live" else " (stub)"),
            summary=plan_output.thought[:200],
            detail=planner_detail,
        )
    )
    if settings.show_prompt:
        trace.append(
            TraceStep(
                layer="agent_planner",
                title="Planner input (debug)",
                summary="Full prompt sent to planner",
                detail={"prompt": planner_prompt},
            )
        )

    memory.append_planner(
        plan_output.thought,
        tools_json=str([t.model_dump() for t in plan_output.tools]),
    )

    tool_results, tool_trace = selector.run_tools(
        plan_output.tools,
        max_steps=settings.max_tool_steps,
    )
    trace.extend(tool_trace)

    for call, result in zip(plan_output.tools, tool_results, strict=False):
        memory.append_tool_result(tool_name=call.name, result=result)
        if "notes" in result and "[SYSTEM:" in result:
            trace.append(
                TraceStep(
                    layer="data",
                    title="Retrieved records",
                    summary="Indirect injection surface — instructions in CRM notes",
                    detail={"owasp": "LLM01 indirect"},
                )
            )
        if "email" in result and "@example.invalid" in result:
            trace.append(
                TraceStep(
                    layer="memory",
                    title="PII in working memory",
                    summary="Tool result stored verbatim — LLM02",
                    detail={"owasp": "LLM02"},
                )
            )

    reply = _build_reply(plan_output.thought, tool_results)
    memory.append_assistant(reply)

    trace.append(
        TraceStep(
            layer="memory",
            title="Working memory updated",
            summary=f"{len(memory.snapshot())} entries in transcript",
            detail={"entry_count": len(memory.snapshot())},
        )
    )

    return ChatResponse(
        reply=reply,
        trace=trace,
        memory=memory.snapshot(),
        actions=actions.list_actions(),
        llm_mode=mode,
    )


def _build_reply(thought: str, tool_results: list[str]) -> str:
    if not tool_results:
        return thought
    bullets = "\n".join(f"• {line[:160]}" for line in tool_results)
    return f"{thought}\n\nActions taken:\n{bullets}"
