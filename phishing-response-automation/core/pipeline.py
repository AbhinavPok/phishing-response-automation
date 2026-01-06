from __future__ import annotations
from core.enrichment_engine import build_enrichment

from core.models import (
    PhishingReport,
    IncidentPackage,
)
from core.extractor import build_extraction_result
from core.decision_engine import build_decision
from core.response_engine import build_response

def run_incident(report: PhishingReport) -> IncidentPackage:
    """
    Run a phishing report through the full analysis pipeline.
    No actions are executed; results are recorded only.
    """
    extraction = build_extraction_result(report)
    decision = build_decision(extraction)
    response = build_response(decision)

    return IncidentPackage(
        report=report,
        extraction=extraction,
        enrichment=None,  # reserved for future threat intel
        decision=decision,
        response=response,
    )
