from pathlib import Path

from app.config import settings
from app.models import Customer, Segment


_PROMPT_FILES = {
    "lab": "system-lab.txt",
    "hardened": "system-hardened.txt",
}


def load_system_prompt() -> str:
    style = settings.normalized_system_prompt_style()
    filename = _PROMPT_FILES.get(style)
    if not filename:
        raise ValueError(
            f"Unknown SYSTEM_PROMPT_STYLE '{style}'. Use: {', '.join(_PROMPT_FILES)}"
        )
    path: Path = settings.prompts_dir / filename
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
