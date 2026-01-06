phishing-response-automation/<br>
│<br>
├── core/<br>
│ ├── extractor.py # Indicator extraction and scoring <br>
│ ├── pipeline.py # End-to-end incident pipeline<br>
│ ├── decision_engine.py # Severity and containment logic<br>
│ ├── response_engine.py # Response recommendations<br>
│ ├── persistence.py # Save incidents to disk<br>
│ ├── models.py # Pydantic data models<br>
│ ├── utils.py # Safe parsing utilities<br>
│ └── init.py<br>
│<br>
├── intake/<br>
│ ├── file_intake.py # Load email from text file<br>
│ ├── file_parser.py # Parse sender / subject / body<br>
│ └── init.py<br>
│<br>
├── humaninput/<br>
│ ├── email_template.txt # User email template<br>
│ └── email_001.txt # Example phishing email<br>
│<br>
├── records/<br>
│ └── YYYY-MM-DD/<br>
│ └── incident_HHMMSS/<br>
│ ├── report.json<br>
│ ├── extraction.json<br>
│ ├── decision.json<br>
│ ├── response.json<br>
│ └── incident_full.json<br>
│
├── demo_runner.py # CLI demo entry point<br>
