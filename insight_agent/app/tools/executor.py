"""Dispatch tool calls by name — used by tool selector."""

from typing import Any

from app.tools import export_csv, read_db, send_campaign

_REGISTRY = {
    "read_customer_db": read_db.run,
    "export_segment_csv": export_csv.run,
    "send_campaign": send_campaign.run,
}


def catalog_names() -> list[str]:
    return list(_REGISTRY.keys())


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    fn = _REGISTRY.get(name)
    if not fn:
        return f"Unknown tool: {name}"
    return fn(**arguments)
