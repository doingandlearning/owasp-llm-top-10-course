import re

from app.models import Customer

_DIRECT_MARKERS = (
    "ignore previous",
    "ignore all previous",
    "ignore instructions",
    "disregard",
    "system prompt",
    "repeat your instructions",
    "reveal your instructions",
    "output only",
    "verbatim",
)

_INDIRECT_MARKERS = (
    "[system:",
    "override all rules",
    "hidden instruction",
    "end every email with",
)

_HTML_MARKERS = (
    "<script",
    "javascript:",
    "onerror=",
    "alert(",
)


def _parse_subject_body(text: str) -> tuple[str, str]:
    subject = "Campaign draft"
    body = text.strip()
    match = re.search(r"^Subject:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    if match:
        subject = match.group(1).strip()
        body = re.sub(
            r"^Subject:\s*.+$",
            "",
            text,
            count=1,
            flags=re.MULTILINE | re.IGNORECASE,
        ).strip()
        body = re.sub(r"^Body:\s*", "", body, flags=re.IGNORECASE).strip()
    return subject, body


def _direct_injection_triggered(brief: str) -> bool:
    lowered = brief.lower()
    return any(marker in lowered for marker in _DIRECT_MARKERS)


def _indirect_injection_triggered(customer: Customer) -> bool:
    lowered = customer.notes.lower()
    return any(marker in lowered for marker in _INDIRECT_MARKERS)


def _wants_html(brief: str) -> bool:
    lowered = brief.lower()
    return any(
        phrase in lowered
        for phrase in ("html", "<h1", "<script", "javascript", "format as html")
    )


def generate_stub(*, prompt: str, brief: str, customer: Customer) -> str:
    """
    Offline LLM stub with predictable demo branches.
    Phase 2 will add live provider calls behind the same interface.
    """
    if _direct_injection_triggered(brief):
        leaked = prompt.split("=== MARKETER BRIEF ===", 1)[0].strip()
        return (
            "Subject: INTERNAL DUMP (stub)\n\n"
            f"Body:\n{leaked}\n\n"
            "---\n"
            "The model followed attacker text in the marketer brief instead of system rules."
        )

    if "pwned" in customer.notes.lower() and "[system:" in customer.notes.lower():
        return "Subject: PWNED\n\nBody: PWNED"

    if _indirect_injection_triggered(customer):
        if "i am not a real marketer" in customer.notes.lower():
            return (
                "Subject: We miss you at the trail\n\n"
                "Body: Hi there — it's been a while since your last order. "
                "Enjoy 15% off with code TRAILBACK.\n\n"
                "I AM NOT A REAL MARKETER"
            )
        return (
            "Subject: Override acknowledged\n\n"
            "Body: The stub detected indirect injection markers in customer notes."
        )

    if _wants_html(brief):
        # Use an event-handler payload: browsers do NOT run <script> inserted via innerHTML,
        # but they do execute handlers like onerror when parsing untrusted HTML (LLM05).
        return (
            "Subject: Flash Sale — Members Only\n\n"
            "Body: <h1>Your exclusive offer</h1>"
            "<p>15% off ends Sunday. Use code <strong>TRAIL15</strong>.</p>"
            "<img src=x onerror=\"alert('LLM05 — unsanitised model HTML ran in your browser')\">"
            "<!-- Visible in source but inert via innerHTML: "
            "<script>alert('this script tag does not execute')</script> -->"
        )

    return (
        "Subject: Ready for your next adventure?\n\n"
        f"Body: Hi {customer.name.split()[0]},\n\n"
        "As one of our most engaged explorers, you get early access to our "
        "waterproof shell collection — 15% off this week.\n\n"
        "See you on the trail,\nNorthwind Outfitters"
    )


def complete(*, prompt: str, brief: str, customer: Customer, mode: str) -> tuple[str, str, str]:
    if mode == "live":
        raise NotImplementedError(
            "Live LLM mode ships in Phase 2. Set LLM_MODE=stub for offline demos."
        )

    raw = generate_stub(prompt=prompt, brief=brief, customer=customer)
    subject, body = _parse_subject_body(raw)
    return subject, body, raw
