"""
Working memory — conversation + tool results (LLM02 surface).

Append-only transcript fed back into the planner on the next turn.
"""

from app.models import MemoryEntry

_entries: list[MemoryEntry] = []


def snapshot() -> list[MemoryEntry]:
    return list(_entries)


def clear() -> None:
    _entries.clear()


def append_user(message: str) -> MemoryEntry:
    entry = MemoryEntry(role="user", content=message)
    _entries.append(entry)
    return entry


def append_planner(thought: str, tools_json: str) -> MemoryEntry:
    entry = MemoryEntry(
        role="planner",
        content=thought,
        metadata={"planned_tools": tools_json},
    )
    _entries.append(entry)
    return entry


def append_tool_result(*, tool_name: str, result: str) -> MemoryEntry:
    entry = MemoryEntry(
        role="tool",
        content=result,
        metadata={"tool": tool_name},
    )
    _entries.append(entry)
    return entry


def append_assistant(message: str) -> MemoryEntry:
    entry = MemoryEntry(role="assistant", content=message)
    _entries.append(entry)
    return entry


def transcript_for_planner() -> str:
    parts: list[str] = []
    for entry in _entries:
        parts.append(f"[{entry.role.upper()}] {entry.content}")
    return "\n\n".join(parts)
