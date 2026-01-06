from typing import Tuple

def load_email_from_file(path: str) -> Tuple[str, str, str]:
    """
    Parse a human-written email intake file.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    sender = ""
    subject = ""
    body_lines = []
    in_body = False

    for line in lines:
        line = line.rstrip("\n")

        if line.startswith("SENDER:"):
            sender = line.replace("SENDER:", "").strip()
        elif line.startswith("SUBJECT:"):
            subject = line.replace("SUBJECT:", "").strip()
        elif line.startswith("BODY:"):
            in_body = True
        elif in_body:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    return sender, subject, body
