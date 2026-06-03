"""Write: send campaign — irreversible simulated send (LLM06)."""

from app import actions, db


def run(*, segment_id: str, subject: str, body: str) -> str:
    db.get_segment(segment_id)
    customers = db.list_customers(segment_id=segment_id, limit=10_000)
    actions.record_send(
        segment_id=segment_id,
        subject=subject,
        body=body,
        recipient_count=len(customers),
    )
    return (
        f"send_campaign executed for segment '{segment_id}' — "
        f"{len(customers)} recipients. Subject: {subject}. No confirmation step."
    )
