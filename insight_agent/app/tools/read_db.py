"""Read: query DB — customer segments / rows."""

import json

from app import db


def run(*, segment_id: str | None = None, limit: int = 10) -> str:
    customers = db.list_customers(segment_id=segment_id, limit=limit)
    rows = [
        {
            "id": c.id,
            "segment_id": c.segment_id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "notes": c.notes,
        }
        for c in customers
    ]
    if segment_id:
        seg = db.get_segment(segment_id)
        header = f"Segment: {seg.name} ({len(rows)} rows shown, limit={limit})"
    else:
        header = f"All segments ({len(rows)} rows shown, limit={limit})"
    return header + "\n" + json.dumps(rows, indent=2)
