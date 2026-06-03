from pydantic import BaseModel, Field


class Segment(BaseModel):
    id: str
    name: str
    tags: list[str]
    purchase_history_summary: str


class Customer(BaseModel):
    id: str
    segment_id: str
    name: str
    email: str
    notes: str


class GenerationRequest(BaseModel):
    segment_id: str
    customer_id: str
    brief: str = Field(min_length=1)


class GenerationResponse(BaseModel):
    subject: str
    body: str
    raw: str
    prompt: str | None = None
    llm_mode: str
