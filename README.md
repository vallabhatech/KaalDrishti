# KaalDrishti

**Endpoint Threat Detection & Security Telemetry Lab**

KaalDrishti is a defensive cybersecurity platform for experimenting with endpoint-security telemetry, detection engineering, threat scoring, alert ingestion, and analyst workflows.

> **Lab boundary:** the repository uses explicitly authorized, synthetic security events. It does not capture keystrokes, clipboard contents, webcam frames, screenshots, credentials, or establish covert persistence.

## Core pipeline

    Synthetic endpoint scenarios
              |
              v
       Authenticated API
              |
              v
      Event validation
              |
              v
      Detection rule engine
              |
              v
      Threat classification
              |
              v
      SQLite event store ---> Analyst console

## Detection scenarios

The simulator produces defensive test cases for authentication brute-force patterns, suspicious process execution, persistence modification attempts, unexpected network activity, and protected-file integrity changes.

Each scenario is mapped to a rule ID, severity, confidence value, and MITRE ATT&CK technique identifier for training and analysis.

## Quick start — Windows

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    $env:KAALDRISHTI_API_TOKEN="change-me"
    python server.py

In another terminal:

    $env:KAALDRISHTI_API_TOKEN="change-me"
    python main.py

Analyst console:

    $env:KAALDRISHTI_API_TOKEN="change-me"
    python control_gui.py

Tests:

    pytest -q
    ruff check .

## API

- GET /health — service health.
- POST /api/events — authenticated simulated event ingestion.
- GET /api/events — authenticated recent detections.

All event ingestion requires X-API-Key. Only events marked as authorized simulator data are accepted.

## Project structure

    KaalDrishti/
    ├── main.py
    ├── server.py
    ├── detection.py
    ├── storage.py
    ├── control_gui.py
    ├── config.py
    ├── test_server.py
    ├── docs/
    │   ├── ARCHITECTURE.md
    │   ├── THREAT_MODEL.md
    │   └── DETECTION_RULES.md
    └── .github/workflows/ci.yml

## Security engineering goals

1. Structured security event design
2. Authenticated telemetry ingestion
3. Detection-rule engineering
4. Severity and confidence classification
5. Local evidence storage
6. Analyst-facing investigation workflows
7. Repeatable adversary simulation without collecting real user content
8. Automated quality gates

The roadmap document in the repository remains the source for planned platform evolution.

## Development

Every push and pull request runs compilation, Ruff, and pytest checks across supported Python versions.

Never commit real API tokens or generated databases. Use .env.example for local configuration.

## License

No license is currently declared.
