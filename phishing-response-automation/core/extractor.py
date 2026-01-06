from __future__ import annotations

from typing import Dict, List


from core.models import PhishingReport, ExtractionResult
from core.utils import (
    extract_urls_from_text,
    parse_domain_from_url,
    is_ip_literal,
    normalize_email_address,
    contains_any,
)

## defines what files are only allowed.
def extract_indicators(report: PhishingReport) -> Dict[str, List[str]]:
    """
    Extract raw indicators from a phishing report.
    Returns normalized indicators without scoring or judgment.
    """
    indicators: Dict[str, List[str]] = {
        "urls": [],
        "domains": [],
        "ip_literals": [],
        "keywords": [],
    }

    # Normalize sender (for later use)
    normalized_sender = normalize_email_address(report.sender)

    # Extract URLs from subject and body
    text_content = f"{report.subject} {report.body}"
    urls = extract_urls_from_text(text_content)
    indicators["urls"] = urls

    # Extract domains and detect IP literals
    domains: List[str] = []
    ip_literals: List[str] = []

    for url in urls:
        domain = parse_domain_from_url(url)
        if not domain:
            continue

        if domain not in domains:
            domains.append(domain)

        if is_ip_literal(domain) and domain not in ip_literals:
            ip_literals.append(domain)

    indicators["domains"] = domains
    indicators["ip_literals"] = ip_literals

    phishing_keywords = [
        "urgent",
        "verify",
        "action required",
        "account suspended",
        "password",
        "login",
        "security alert",
        "immediately",
    ]

    keyword_hits = contains_any(text_content, phishing_keywords)
    indicators["keywords"] = keyword_hits

    return indicators

def score_to_severity(total_score: int) -> str:
    """
    Map a numeric risk score to a severity label.
    """
    if total_score >= 45:
        return "High"
    if total_score >= 20:
        return "Medium"
    return "Low"


def build_extraction_result(report: PhishingReport) -> ExtractionResult:
    """
    Build a structured ExtractionResult from a phishing report.
    Applies transparent, explainable scoring.
    """
    indicators = extract_indicators(report)

    # Normalize sender and extract sender domain
    normalized_sender = normalize_email_address(report.sender)

    sender_domain = None
    suspicious_sender = False

    if "@" in normalized_sender:
        sender_domain = normalized_sender.split("@", 1)[1]

        if sender_domain not in indicators["domains"] and indicators["domains"]:
            suspicious_sender = True

    # -----------------------------
    # Explainable scoring
    # -----------------------------
    score_breakdown: Dict[str, int] = {}
    total_score = 0

    if suspicious_sender:
        score_breakdown["suspicious_sender"] = 20
        total_score += 20

    if indicators["ip_literals"]:
        ip_points = 25 * len(indicators["ip_literals"])
        score_breakdown["ip_literals"] = ip_points
        total_score += ip_points

    if indicators["keywords"]:
        keyword_points = 5 * len(indicators["keywords"])
        score_breakdown["keywords"] = keyword_points
        total_score += keyword_points

    if indicators["urls"]:
        score_breakdown["urls_present"] = 5
        total_score += 5

    return ExtractionResult(
        normalized_sender=normalized_sender,
        sender_domain=sender_domain,
        suspicious_sender=suspicious_sender,
        extracted_urls=indicators["urls"],
        extracted_domains=indicators["domains"],
        ip_literals=indicators["ip_literals"],
        keyword_hits={"matched": indicators["keywords"]},
        attachment_flags={},
        score_breakdown=score_breakdown,
        total_score=total_score,
    )



## takes phishing report and extract ojective facts from it no decision made.. this will collects artifacts