"""
Pre- and post-validators for hardened CampaignBot deployments.

Pipeline position (when ENABLE_VALIDATORS=true):

    untrusted inputs  →  PRE-VALIDATION  →  LLM  →  POST-VALIDATION  →  UI

PRE-VALIDATION  — inspect marketer brief and CRM notes *before* the model call.
POST-VALIDATION — inspect and sanitise model output *before* the browser renders it.

Disabled by default so workshop demos remain exploitable. Turn on with
ENABLE_VALIDATORS=true in .env.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field

from app.models import Customer, ValidationCheckResult

# --- Pre-validation: untrusted inputs ---------------------------------------

_DIRECT_INJECTION_MARKERS = (
    "ignore previous",
    "ignore all previous",
    "ignore instructions",
    "disregard",
    "system prompt",
    "repeat your instructions",
    "reveal your instructions",
    "output only",
    "verbatim",
    "override all rules",
)

_INDIRECT_INJECTION_MARKERS = (
    "[system:",
    "override all rules",
    "hidden instruction",
    "end every email with",
)

# --- Post-validation: model output ------------------------------------------

_HTML_PATTERN = re.compile(r"<[^>]+>")
_DANGEROUS_HTML_MARKERS = (
    "<script",
    "javascript:",
    "onerror=",
    "onload=",
    "onclick=",
    "alert(",
)

_SYSTEM_LEAK_MARKERS = (
    "=== system ===",
    "=== segment ===",
    "=== marketer brief ===",
    "=== customer notes ===",
    "you are campaignbot",
)


@dataclass
class PreValidationResult:
    allowed: bool
    checks: list[ValidationCheckResult] = field(default_factory=list)


@dataclass
class PostValidationResult:
    subject: str
    body: str
    checks: list[ValidationCheckResult] = field(default_factory=list)
    modified: bool = False


def _contains_marker(text: str, markers: tuple[str, ...]) -> str | None:
    lowered = text.lower()
    for marker in markers:
        if marker in lowered:
            return marker
    return None


def validate_pre(*, brief: str, customer: Customer) -> PreValidationResult:
    """
    PRE-VALIDATOR — run on untrusted inputs before building the LLM prompt.

    Blocks requests that carry obvious prompt-injection patterns so they never
    reach the model (defence in depth; not a substitute for architecture fixes).
    """
    checks: list[ValidationCheckResult] = []

    brief_marker = _contains_marker(brief, _DIRECT_INJECTION_MARKERS)
    checks.append(
        ValidationCheckResult(
            name="brief_injection_scan",
            passed=brief_marker is None,
            detail=(
                "Marketer brief looks like a normal campaign request."
                if brief_marker is None
                else f"Blocked direct-injection marker in brief: {brief_marker!r}"
            ),
        )
    )

    notes_marker = _contains_marker(customer.notes, _INDIRECT_INJECTION_MARKERS)
    checks.append(
        ValidationCheckResult(
            name="customer_notes_injection_scan",
            passed=notes_marker is None,
            detail=(
                "CRM notes contain no known indirect-injection markers."
                if notes_marker is None
                else f"Blocked indirect-injection marker in CRM notes: {notes_marker!r}"
            ),
        )
    )

    allowed = all(check.passed for check in checks)
    return PreValidationResult(allowed=allowed, checks=checks)


def validate_post(*, subject: str, body: str, raw: str) -> PostValidationResult:
    """
    POST-VALIDATOR — run on model output before returning to the UI.

    HTML-encodes bodies that look like markup so innerHTML cannot execute
    event handlers (LLM05 mitigation). Flags likely system-prompt leakage.
    """
    checks: list[ValidationCheckResult] = []
    safe_subject = subject
    safe_body = body
    modified = False

    combined = f"{subject}\n{body}\n{raw}".lower()
    leak_marker = _contains_marker(combined, _SYSTEM_LEAK_MARKERS)
    checks.append(
        ValidationCheckResult(
            name="system_prompt_leak_scan",
            passed=leak_marker is None,
            detail=(
                "Output does not appear to leak internal prompt sections."
                if leak_marker is None
                else f"Flagged possible prompt leakage: {leak_marker!r}"
            ),
        )
    )

    body_lower = body.lower()
    has_html = bool(_HTML_PATTERN.search(body)) or any(
        marker in body_lower for marker in _DANGEROUS_HTML_MARKERS
    )
    if has_html:
        safe_body = html.escape(body)
        modified = safe_body != body
        checks.append(
            ValidationCheckResult(
                name="html_output_sanitisation",
                passed=True,
                detail=(
                    "HTML-like output was HTML-encoded before render "
                    "(event handlers and tags are inert in the browser)."
                ),
            )
        )
    else:
        checks.append(
            ValidationCheckResult(
                name="html_output_sanitisation",
                passed=True,
                detail="Plain-text output — no HTML encoding needed.",
            )
        )

    return PostValidationResult(
        subject=safe_subject,
        body=safe_body,
        checks=checks,
        modified=modified,
    )
