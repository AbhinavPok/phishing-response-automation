### 1. Navigate to the project directory

```powershell
cd phishing-response-automation
python demo_runner.py humaninput\email_001.txt
records/YYYY-MM-DD/incident_HHMMSS/


Files created after the run
report.json – original intake data

extraction.json – extracted indicators and scores

decision.json – severity and rationale

response.json – logged actions

incident_full.json – full consolidated record
