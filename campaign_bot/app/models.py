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
    phone: str = ""
    notes: str


class GenerationRequest(BaseModel):
    segment_id: str
    customer_id: str
    brief: str = Field(min_length=1)


class ValidationCheckResult(BaseModel):
    name: str
    passed: bool
    detail: str


class GenerationResponse(BaseModel):
    subject: str
    body: str
    raw: str
    prompt: str | None = None
    llm_mode: str
    validators_enabled: bool = False
    pre_validation: list[ValidationCheckResult] | None = None
    post_validation: list[ValidationCheckResult] | None = None
