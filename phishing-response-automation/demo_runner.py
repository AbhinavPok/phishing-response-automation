import sys
from pprint import pprint

from intake.file_intake import load_email_from_file
from core.pipeline import run_incident

if len(sys.argv) < 2:
    print("Usage: python demo_runner.py <path_to_email_file>")
    sys.exit(1)

email_path = sys.argv[1]

# Intake returns a fully built PhishingReport
report = load_email_from_file(email_path)

# Run the incident through the pipeline
incident = run_incident(report)

print("\n=== INCIDENT PACKAGE OUTPUT ===\n")
pprint(incident.dict())
