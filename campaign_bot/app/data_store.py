import json

from fastapi import HTTPException

from app.config import settings
from app.models import Customer, Segment


def _load_json(filename: str) -> list[dict]:
    path = settings.data_dir / filename
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def list_segments() -> list[Segment]:
    return [Segment.model_validate(item) for item in _load_json("segments.json")]


def get_segment(segment_id: str) -> Segment:
    for segment in list_segments():
        if segment.id == segment_id:
            return segment
    raise HTTPException(status_code=404, detail=f"Segment not found: {segment_id}")


def list_customers(segment_id: str | None = None) -> list[Customer]:
    customers = [Customer.model_validate(item) for item in _load_json("customers.json")]
    if segment_id is None:
        return customers
    return [c for c in customers if c.segment_id == segment_id]


def get_customer(customer_id: str) -> Customer:
    for customer in list_customers():
        if customer.id == customer_id:
            return customer
    raise HTTPException(status_code=404, detail=f"Customer not found: {customer_id}")
