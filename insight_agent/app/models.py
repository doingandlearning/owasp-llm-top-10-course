from typing import Any, Literal

from pydantic import BaseModel, Field

Layer = Literal[
    "user",
    "agent_planner",
    "agent_selector",
    "tool",
    "data",
    "memory",
    "action",
]


class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class PlannerOutput(BaseModel):
    thought: str
    tools: list[ToolCall] = Field(default_factory=list)


class TraceStep(BaseModel):
    """One step in the agent pipeline — maps to Excalidraw layers for teaching."""

    layer: Layer
    title: str
    summary: str
    detail: dict[str, Any] = Field(default_factory=dict)


class MemoryEntry(BaseModel):
    role: Literal["user", "planner", "tool", "assistant"]
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ActionRecord(BaseModel):
    kind: Literal["export", "send"]
    timestamp: str
    summary: str
    detail: dict[str, Any] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    reply: str
    trace: list[TraceStep]
    memory: list[MemoryEntry]
    actions: list[ActionRecord]
    llm_mode: str


class DemoScenario(BaseModel):
    id: str
    title: str
    subtitle: str
    diagram_label: str | None = None
    owasp: list[str] = []
    message: str
    instructor_note: str
