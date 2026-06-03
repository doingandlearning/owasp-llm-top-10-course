from pathlib import Path

from app.config import settings
from app.models import Customer, Segment


def load_system_prompt() -> str:
    path: Path = settings.prompts_dir / "system.txt"
    return path.read_text(encoding="utf-8").strip()


def build_prompt(*, system: str, segment: Segment, customer: Customer, brief: str) -> str:
    """Concatenate all inputs into one string — intentional anti-pattern for demos."""
    tags = ", ".join(segment.tags)
    return "\n\n".join(
        [
            "=== SYSTEM ===",
            system,
            "=== SEGMENT ===",
            f"Name: {segment.name}",
            f"Tags: {tags}",
            f"Purchase history: {segment.purchase_history_summary}",
            "=== MARKETER BRIEF ===",
            brief.strip(),
            "=== CUSTOMER NOTES ===",
            f"Customer: {customer.name} <{customer.email}>",
            customer.notes,
        ]
    )
