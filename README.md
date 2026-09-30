# KaalDrishti

KaalDrishti is a consent-based security telemetry lab for learning API ingestion, event validation, testing, and defensive monitoring architecture.

> The project intentionally does not collect keystrokes, clipboard contents, webcam frames, screenshots, credentials, or establish startup persistence.

## What it does

- Generates clearly identified synthetic security events.
- Sends JSON telemetry to a small Flask API.
- Requires an API token for event ingestion.
- Validates event shape and accepts only synthetic lab events.
- Enforces a request-size limit.
- Includes a local Tkinter test GUI.
- Includes automated pytest coverage.
- Supports environment-based configuration for local and hosted deployments.

## Architecture

~~~text
+----------------------+       JSON + X-API-Key       +----------------------+
| Synthetic client     | --------------------------> | Flask telemetry API  |
| main.py / GUI        |                             | server.py            |
+----------------------+                             +----------+-----------+
                                                                  |
                                                                  v
                                                         Console / test output
~~~

## Project structure

~~~text
KaalDrishti/
├── main.py
├── server.py
├── control_gui.py
├── config.py
├── test_server.py
├── requirements.txt
├── .env.example
├── CHANGELOG.md
├── .github/workflows/
└── utils/
~~~

## Quick start

### Windows PowerShell

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:KAALDRISHTI_API_TOKEN="change-me"
~~~

### Start the API

~~~powershell
python server.py
~~~

The API runs on http://127.0.0.1:10000 by default.

### Start the synthetic client

In a second terminal:

~~~powershell
$env:KAALDRISHTI_API_TOKEN="change-me"
python main.py
~~~

### Run the tests

~~~powershell
pytest -q
~~~

### Run linting

~~~powershell
ruff check .
~~~

## Configuration

Copy .env.example to .env for local development.

| Variable | Purpose | Default |
|---|---|---|
| KAALDRISHTI_API_TOKEN | API authentication token | empty |
| KAALDRISHTI_ENDPOINT | Client ingestion endpoint | local API |
| KAALDRISHTI_CLIENT | Client label | local-lab |
| KAALDRISHTI_INTERVAL | Synthetic event interval in seconds | 10 |
| MAX_REQUEST_BYTES | Maximum API request size | 65536 |
| PORT | Server port | 10000 |

Never commit real secrets.

## API

### GET /health

Returns service health and whether authentication has been configured.

### POST /api/events

Requires:
- X-API-Key matching KAALDRISHTI_API_TOKEN
- JSON object containing event_id, client, event_type, message, and source
- source must be synthetic

The API returns 202 Accepted for a valid lab event.

## Development quality gates

Every push and pull request runs:
- Python syntax/compile checks
- Ruff linting
- pytest
- GitHub CodeQL analysis

## Security model

This repository is designed for defensive, authorized experimentation. It deliberately excludes covert collection, credential interception, surveillance-oriented capture, startup persistence, and self-removal behavior.

Use synthetic events when demonstrating detection pipelines, dashboards, alerting, or ingestion systems.

## License

No license is currently declared. Add a license before distributing the project under open-source terms.
