import json
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel

from app.config import settings


class DemoScenario(BaseModel):
    id: str
    title: str
    subtitle: str
    diagram_label: str | None = None
    owasp: list[str] = []
    segment_id: str
    customer_id: str
    brief: str
    brief_file: str
    instructor_note: str


def _payloads_dir() -> Path:
    return settings.payloads_dir


def list_demo_scenarios() -> list[DemoScenario]:
    scenarios_path = _payloads_dir() / "scenarios.json"
    with scenarios_path.open(encoding="utf-8") as f:
        raw = json.load(f)

    scenarios: list[DemoScenario] = []
    for item in raw:
        brief_file = item["brief_file"]
        brief_path = _payloads_dir() / brief_file
        if not brief_path.is_file():
            raise HTTPException(
                status_code=500,
                detail=f"Missing payload file: {brief_file}",
            )
        scenarios.append(
            DemoScenario(
                **item,
                brief=brief_path.read_text(encoding="utf-8").strip(),
            )
        )
    return scenarios


def get_demo_scenario(scenario_id: str) -> DemoScenario:
    for scenario in list_demo_scenarios():
        if scenario.id == scenario_id:
            return scenario
    raise HTTPException(status_code=404, detail=f"Demo scenario not found: {scenario_id}")
