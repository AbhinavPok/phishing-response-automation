from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from core.models import IncidentPackage


def save_incident_record(incident: IncidentPackage) -> str:
    """
    Persist an IncidentPackage to disk in a date-based folder.
    Returns the path to the incident directory.
    """

    # Date-based directory (YYYY-MM-DD)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    base_dir = Path("records") / date_str

    # Unique incident folder
    incident_id = datetime.utcnow().strftime("incident_%H%M%S")
    incident_dir = base_dir / incident_id

    incident_dir.mkdir(parents=True, exist_ok=True)

    def write_json(filename: str, data: Any) -> None:
        path = incident_dir / filename
        path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )

    # -----------------------------
    # Machine-readable artifacts
    # -----------------------------
    write_json("report.json", incident.report.dict())
    write_json("extraction.json", incident.extraction.dict())
    write_json("decision.json", incident.decision.dict())
    write_json("response.json", incident.response.dict())
    write_json("incident_full.json", incident.dict())

    # -----------------------------
    # Human-readable summary
    # -----------------------------
    write_human_summary(incident, incident_dir)

    return str(incident_dir)


def write_human_summary(incident: IncidentPackage, output_dir: Path) -> None:
    """
    Write a plain-English summary of the incident for human readers.
    """

    lines: list[str] = []

    lines.append("PHISHING ANALYSIS SUMMARY")
    lines.append("=" * 24)
    lines.append("")
    lines.append(f"Severity: {incident.decision.severity.upper()}")
    lines.append("")

    lines.append("Why this rating:")
    if incident.decision.rationale:
        for reason in incident.decision.rationale:
            lines.append(f"- {reason}")
    else:
        lines.append("- No strong phishing indicators detected")

    lines.append("")
    lines.append("Recommended action:")
    for action in incident.decision.recommended_actions:
        lines.append(f"- {action}")

    lines.append("")
    lines.append("Sender:")
    lines.append(f"- {incident.report.sender}")

    lines.append("")
    lines.append("Subject:")
    lines.append(f"- {incident.report.subject}")

    lines.append("")
    lines.append("Reported at (UTC):")
    lines.append(f"- {incident.report.reported_at}")

    summary_path = output_dir / "summary.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
