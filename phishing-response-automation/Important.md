## File Overview 
**⚠️ This application automatically creates local incident record files at runtime.  
No `records/` or report files are required to exist in the repository beforehand.**

---

### `core/models.py`
Defines all structured data models (schemas) used across the system.  
No logic is executed here.

---

### `core/extractor.py`
Extracts objective indicators (URLs, domains, IPs, keywords) and applies transparent scoring.  
No decisions or actions occur in this file.

---

### `core/decision_engine.py`
Converts extraction results into a security decision (severity, containment, actions).

---

### `core/response_engine.py`
Records response actions, notifications, and artifacts.  
No real-world actions are executed.

---

### `core/pipeline.py`
Orchestrates the full analysis flow from intake to response.

---

### `core/persistence.py`
**Creates local incident record folders and files automatically.**

The function `save_incident_record()` contains the code that:
- Creates a date-based directory
- Generates a unique incident folder
- Writes JSON records to disk

This is where local files are created when the program runs.

---

### `core/utils.py`
Safe helper functions for parsing, normalization, and indicator detection.

---

### `intake/file_intake.py`
Loads phishing email input from a user-provided file.

---

### `intake/file_parser.py`
Parses structured email templates for consistent intake.

---

### `demo_runner.py`
Command-line entry point used to run the full pipeline and trigger record creation.
