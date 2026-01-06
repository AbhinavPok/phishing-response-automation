from __future__ import annotations

from pathlib import Path
from datetime import datetime

from core.models import PhishingReport


def load_email_from_file(path: str) -> PhishingReport:
    """
    Load a human-submitted email template from disk and
    convert it into a PhishingReport.
    """
    content = Path(path).read_text(encoding="utf-8")

    sender = ""
    subject = ""
    body_lines = []

    mode = None

    for line in content.splitlines():
        line = line.rstrip()

        if line.startswith("SENDER:"):
            mode = "sender"
            continue
        if line.startswith("SUBJECT:"):
            mode = "subject"
            continue
        if line.startswith("BODY:"):
            mode = "body"
            continue

        if mode == "sender" and not sender:
            sender = line.strip()
        elif mode == "subject" and not subject:
            subject = line.strip()
        elif mode == "body":
            body_lines.append(line)

    return PhishingReport(
        reporter="local.user",
        sender=sender,
        subject=subject,
        body="\n".join(body_lines).strip(),
        reported_at=datetime.utcnow().isoformat(),
    )
