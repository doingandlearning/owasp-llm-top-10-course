"""
Action log — side effects from write tools (export, send).

Kept separate from working memory so instructors can show "real world impact" clearly.
"""

import json
from datetime import UTC, datetime

from app.config import settings
from app.models import ActionRecord


_actions: list[ActionRecord] = []


def list_actions() -> list[ActionRecord]:
    return list(_actions)


def clear_actions() -> None:
    _actions.clear()
    log = settings.sends_log
    if log.exists():
        log.unlink()


def record_export(*, filename: str, row_count: int, segment_id: str) -> ActionRecord:
    entry = ActionRecord(
        kind="export",
        timestamp=datetime.now(UTC).isoformat(),
        summary=f"Exported {row_count} rows → {filename}",
        detail={"filename": filename, "row_count": row_count, "segment_id": segment_id},
    )
    _actions.append(entry)
    return entry


def record_send(*, segment_id: str, subject: str, body: str, recipient_count: int) -> ActionRecord:
    entry = ActionRecord(
        kind="send",
        timestamp=datetime.now(UTC).isoformat(),
        summary=f"Sent campaign to {recipient_count} customers ({segment_id})",
        detail={
            "segment_id": segment_id,
            "subject": subject,
            "body_preview": body[:200],
            "recipient_count": recipient_count,
        },
    )
    _actions.append(entry)
    with settings.sends_log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry.model_dump()) + "\n")
    return entry
