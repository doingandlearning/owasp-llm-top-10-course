"""Write: export CSV — any segment, no scope (LLM02 + LLM06)."""

import csv
from datetime import UTC, datetime

from app import actions, db
from app.config import settings


def run(*, segment_id: str = "all") -> str:
    if segment_id == "all":
        customers = db.list_customers(limit=10_000)
        label = "all"
    else:
        db.get_segment(segment_id)
        customers = db.list_customers(segment_id=segment_id, limit=10_000)
        label = segment_id

    filename = f"export_{label}_{datetime.now(UTC).strftime('%Y%m%dT%H%M%S')}.csv"
    path = settings.exports_dir / filename

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "segment_id", "name", "email", "phone", "notes"],
        )
        writer.writeheader()
        for c in customers:
            writer.writerow(
                {
                    "id": c.id,
                    "segment_id": c.segment_id,
                    "name": c.name,
                    "email": c.email,
                    "phone": c.phone,
                    "notes": c.notes,
                }
            )

    actions.record_export(
        filename=filename,
        row_count=len(customers),
        segment_id=label,
    )
    return f"Wrote {len(customers)} rows to exports/{filename} (no approval required)."
