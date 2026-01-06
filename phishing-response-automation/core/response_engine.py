from __future__ import annotations

from typing import Dict, List

from core.models import Decision, ResponseActionResult

def build_response(decision: Decision) -> ResponseActionResult:
    """
    Record response actions based on a Decision.
    This function does NOT execute any real actions.
    """
    actions_executed: List[str] = []
    notifications: List[str] = []
    artifacts: Dict[str, str] = {}

    # Record actions that would be taken
    for action in decision.recommended_actions:
        actions_executed.append(action)

    # Record who would be notified
    if decision.containment_required:
        notifications.extend(
            [
                "SOC team notified",
                "IT security notified",
                "Management notified",
            ]
        )
    else:
        notifications.append("Incident logged for awareness")

    # Record evidence/artifact locations (logical placeholders)
    artifacts["decision_record"] = "records/decision.json"
    artifacts["analysis_summary"] = "records/extraction_summary.json"

    return ResponseActionResult(
        actions_executed=actions_executed,
        notifications=notifications,
        artifacts=artifacts,
    )
