from __future__ import annotations

import json
import re
from typing import Any, Dict, List
from datetime import datetime
import yaml


#Opening JSON into PYTHON
def load_json(path: str) -> Dict[str, Any]:
    """
    Safely load a JSON file from disk.
    Treats file contents as untrusted input.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

#Opening YAML without running it so it doesnot upload virus by accident
def load_yaml(path: str) -> Dict[str, Any]:
    """
    Safely load a YAML configuration file.
    Uses safe_load to prevent code execution.
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

##Looks through the text and pulls out URL
URL_REGEX = re.compile(
    r"(https?://[^\s<>\"']+|www\.[^\s<>\"']+)",
    re.IGNORECASE,
)

def extract_urls_from_text(text: str) -> List[str]:
    """
    Safely extract URLs from untrusted text.
    Returns a deduplicated list of URLs.
    """
    if not text:
        return []

    matches = URL_REGEX.findall(text)

    # Normalize and deduplicate
    urls: List[str]= []
    for url in matches:
        cleaned = url.rstrip(".,);]")
        if cleaned not in urls:
            urls.append(cleaned)

    return urls
## We import inputs and list the strings as of right now 


def normalize_email_address(sender: str) -> str:
    """
    Normalize an email sender string by removing display names
    and returning a lowercase email address when possible.
    """
    if not sender:
        return ""

    sender = sender.strip()

    # Handle formats like: Name <email@domain>
    match = re.search(r"<([^>]+)>", sender)
    if match:
        email = match.group(1)
    else:
        email = sender

    return email.lower()
def parse_domain_from_url(url: str) -> str | None:
    """
    Safely extract the domain from a URL.
    Returns None if parsing fails.
    """
    try:
        parsed = urlparse(url if "://" in url else f"http://{url}")
        return parsed.hostname.lower() if parsed.hostname else None
    except Exception:
        return None


def is_ip_literal(value: str) -> bool:
    """
    Check whether a string is an IPv4 address.
    """
    ip_regex = re.compile(
        r"^(?:\d{1,3}\.){3}\d{1,3}$"
    )
    return bool(ip_regex.match(value))
def contains_any(text: str, keywords: list[str]) -> list[str]:
    """
    Return a list of keywords found in text (case-insensitive).
    Evidence collection only.
    """
    if not text:
        return []

    text_lower = text.lower()
    matches: list[str] = []

    for keyword in keywords:
        if keyword.lower() in text_lower:
            matches.append(keyword)

    return matches

##machines only looks at real email and gets rid of error human may cause by not reading the url or text properly