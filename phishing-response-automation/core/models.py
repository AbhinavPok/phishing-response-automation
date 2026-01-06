from __future__ import annotations
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from typing import Optional


#Severity format "a formal way to rank issues that comes across"
Severity = Literal["Low", "Medium", "High"]

#Attachments " we will seperate links and attachments becuase they have diffrent attacks that comes with it"
class Attachment(BaseModel):
    filename: str
    sha256: Optional[str] = None
    size_bytes: Optional[int] = None

#Intake for user Input ,, 0 trust idea.. since we dont know whats on the raw data that was added
class PhishingReport(BaseModel):
    reporter: str
    sender: str
    subject: str
    body: str = ""
    urls: List[str] = Field(default_factory=list)
    clicked: bool = False
    downloaded_attachment: bool = False
    attachment: Optional[Attachment] = None
    reported_at: Optional[str] = None

#Extraction Stage " it will normalize data" they dont trust raw input but will make decision on data derived from it. strips down noises. 
# This is what the system pulled out of the information (such as links ip domain etc)
class ExtractionResult(BaseModel):
    normalized_sender: str
    sender_domain: Optional[str]
    suspicious_sender: bool
    extracted_urls: List[str]
    extracted_domains: List[str]
    ip_literals: List[str]
    keyword_hits: Dict[str, List[str]]
    attachment_flags: Dict[str, Any]
    score_breakdown: Dict[str, int]
    total_score: int

# Threat intelligence finding,  way to gather evidence  helps analyst make decisions
class IntelFinding(BaseModel):
    indicator: str
    indicator_type: Literal["domain", "url", "ip", "hash"]
    verdict: Literal["benign", "suspicious", "malicious", "unknown"]
    confidence: float = 0.0
    sources: List[str] = Field(default_factory=list)
    details: Dict[str, Any] = Field(default_factory=dict)

#Staging output gives context on the evidence created, it shows based on the intel this is what the program see
class EnrichmentResult(BaseModel):
    findings: List[IntelFinding]
    overall_verdict: Literal["benign", "suspicious", "malicious", "unknown"]
    overall_confidence: float
    summary: str

#this will give contect and shows facts to show what the program believes a good decision is
class Decision(BaseModel):
    severity: Severity
    containment_required: bool
    rationale: List[str]
    recommended_actions: List[str]

#This is meant to record outcome, its is a log of incident
class ResponseActionResult(BaseModel):
    actions_executed: List[str]
    notifications: List[str]
    artifacts: Dict[str, str] = Field(default_factory=dict)

#It shows the full result of all the clases above to complete the file for the report
class IncidentPackage(BaseModel):
    report: PhishingReport
    extraction: ExtractionResult
    enrichment: Optional[EnrichmentResult] = None
    decision: Decision
    response: ResponseActionResult