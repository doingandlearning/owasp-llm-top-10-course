import json

from fastapi import HTTPException

from app.config import settings
from app.models import DemoScenario


def list_scenarios() -> list[DemoScenario]:
    path = settings.payloads_dir / "scenarios.json"
    with path.open(encoding="utf-8") as f:
        raw = json.load(f)
    scenarios: list[DemoScenario] = []
    for item in raw:
        query_path = settings.payloads_dir / item["query_file"]
        if not query_path.is_file():
            raise HTTPException(status_code=500, detail=f"Missing {item['query_file']}")
        scenarios.append(
            DemoScenario(
                **{k: v for k, v in item.items() if k != "query_file"},
                message=query_path.read_text(encoding="utf-8").strip(),
            )
        )
    return scenarios
