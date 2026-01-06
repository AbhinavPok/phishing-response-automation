                                        ## ON LINE 55 ADD YOUR API KEY ##
from __future__ import annotations

from datetime import datetime
from typing import List

from core.models import ExtractionResult, EnrichmentResult, IntelFinding

# -----------------------------
# Domain age enrichment (offline-safe)
# -----------------------------

def enrich_domain_age(domain: str) -> IntelFinding:
    """
    Simulated domain age enrichment.
    (Replace with real WHOIS later if desired.)
    """
    # Placeholder logic (safe for demo / offline use)
    suspicious_tlds = (".work", ".zip", ".click", ".xyz")

    if domain.endswith(suspicious_tlds):
        verdict = "suspicious"
        confidence = 0.6
        details = {"reason": "High-risk TLD"}
    else:
        verdict = "unknown"
        confidence = 0.3
        details = {"reason": "No domain age data available"}

    return IntelFinding(
        indicator=domain,
        indicator_type="domain",
        verdict=verdict,
        confidence=confidence,
        sources=["domain_heuristics"],
        details=details,
    )


# -----------------------------
# VirusTotal-style enrichment (safe stub)
# -----------------------------

def enrich_virustotal_stub(indicator: str, indicator_type: str) -> IntelFinding:
    """
    Stub for VirusTotal enrichment.
    Does NOT call external APIs.
    """
    return IntelFinding(
        indicator=indicator,
        indicator_type=indicator_type,
        verdict="unknown",
        confidence=0.0,
        sources=["virustotal_stub"],
        details={"note": "API key not configured"}, ## ADD YOUR API KEY HERE ####
    )


# -----------------------------
# Main enrichment function
# -----------------------------

def build_enrichment(extraction: ExtractionResult) -> EnrichmentResult:
    """
    Build enrichment results from extracted indicators.
    """
    findings: List[IntelFinding] = []

    # Domain age enrichment
    for domain in extraction.extracted_domains:
        findings.append(enrich_domain_age(domain))

    # VirusTotal stub enrichment (domains + URLs)
    for domain in extraction.extracted_domains:
        findings.append(enrich_virustotal_stub(domain, "domain"))

    for url in extraction.extracted_urls:
        findings.append(enrich_virustotal_stub(url, "url"))

    # Aggregate verdict (conservative)
    overall_verdict = "unknown"
    overall_confidence = 0.0

    for finding in findings:
        if finding.verdict == "malicious":
            overall_verdict = "malicious"
            overall_confidence = max(overall_confidence, finding.confidence)
        elif finding.verdict == "suspicious" and overall_verdict != "malicious":
            overall_verdict = "suspicious"
            overall_confidence = max(overall_confidence, finding.confidence)

    summary = f"{len(findings)} enrichment findings generated"

    return EnrichmentResult(
        findings=findings,
        overall_verdict=overall_verdict,
        overall_confidence=overall_confidence,
        summary=summary,
    )
