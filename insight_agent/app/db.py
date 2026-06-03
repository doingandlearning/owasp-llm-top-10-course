"""
Data layer — Customer DB (read-only in Phase 1).

Separate from agent logic so delegates can inspect how records enter working memory.
"""

import json
from dataclasses import dataclass

from fastapi import HTTPException

from app.config import settings


@dataclass(frozen=True)
class Segment:
    id: str
    name: str
    tags: list[str]
    purchase_history_summary: str


@dataclass(frozen=True)
class Customer:
    id: str
    segment_id: str
    name: str
    email: str
    phone: str
    notes: str


def _load(name: str) -> list[dict]:
    with (settings.data_dir / name).open(encoding="utf-8") as f:
        return json.load(f)


def list_segments() -> list[Segment]:
    return [Segment(**row) for row in _load("segments.json")]


def get_segment(segment_id: str) -> Segment:
    for segment in list_segments():
        if segment.id == segment_id:
            return segment
    raise HTTPException(status_code=404, detail=f"Unknown segment: {segment_id}")


def list_customers(*, segment_id: str | None = None, limit: int = 100) -> list[Customer]:
    rows = [Customer(**row) for row in _load("customers.json")]
    if segment_id:
        rows = [c for c in rows if c.segment_id == segment_id]
    return rows[:limit]


def count_customers(segment_id: str) -> int:
    return len(list_customers(segment_id=segment_id, limit=10_000))
