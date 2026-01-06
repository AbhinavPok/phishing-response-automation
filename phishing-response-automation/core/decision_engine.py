from __future__ import annotations

from typing import List

from core.models import ExtractionResult, Decision
from core.extractor import score_to_severity


def build_decision(extraction: ExtractionResult) -> Decision:
    """
    Convert extracted evidence into a policy decision.
    No actions are executed here.
    """
    severity = score_to_severity(extraction.total_score)
    containment_required = severity == "High"

    rationale: List[str] = []

    if extraction.suspicious_sender:
        rationale.append("Sender domain does not align with embedded links")

    if extraction.ip_literals:
        rationale.append("IP-based URLs detected (common phishing tactic)")

    if extraction.keyword_hits.get("matched"):
        rationale.append("Social-engineering language detected")

    if extraction.extracted_urls:
        rationale.append("User exposed to clickable links")

    recommended_actions: List[str] = []

    if severity == "High":
        recommended_actions.extend([
            "Quarantine email across tenant",
            "Force password reset for affected user",
            "Block indicators at email gateway",
            "Open security incident",
        ])
    elif severity == "Medium":
        recommended_actions.extend([
            "Isolate email for review",
            "Notify user with guidance",
            "Monitor environment for related activity",
        ])
    else:
        recommended_actions.append(
            "Log incident for awareness; no immediate action required"
        )

    return Decision(
        severity=severity,
        containment_required=containment_required,
        rationale=rationale,
        recommended_actions=recommended_actions,
    )
