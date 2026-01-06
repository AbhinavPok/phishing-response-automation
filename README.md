# Phishing Response Automation

A phishing analysis and response automation pipeline designed to reflect how a real Security Operations Center (SOC) processes reported phishing emails.

This project emphasizes **explainability**, **structured decision-making**, and **audit-ready outputs**, rather than automated destructive actions.

---

## Overview

This tool simulates a SOC phishing workflow by:

- Ingesting reported phishing emails as plain text
- Extracting objective indicators (URLs, domains, keywords, sender info)
- Applying transparent, rule-based risk scoring
- Producing severity decisions with rationale
- Recording all results in structured, reviewable JSON files

No emails are blocked or systems modified automatically.  
The system is designed for **analysis, triage, and documentation**.

---

## Key Features

- Zero-trust intake of human-submitted email content
- Explainable scoring and severity classification
- Clear separation of pipeline stages
- Date-based incident record storage
- Analyst-readable outputs
- Resume- and portfolio-ready architecture

---

## How It Works

1. **Intake**
   - Reads a plain-text email file
   - Parses sender, subject, and body
   - Treats all input as untrusted

2. **Extraction**
   - Normalizes sender address
   - Extracts URLs, domains, IP literals
   - Identifies common phishing keywords

3. **Scoring**
   - Suspicious sender domain
   - IP-based links
   - Keyword density
   - URL presence

4. **Decision**
   - Severity: `Low`, `Medium`, or `High`
   - Containment recommendation
   - Clear rationale for analysts

5. **Response**
   - Logs recommended actions
   - Generates artifacts for audit

6. **Persistence**
   - Saves results into date-based folders
   - One directory per incident

---

## Project Structure

