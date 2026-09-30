# How to Run KaalDrishti

A quick local setup guide for the KaalDrishti Endpoint Threat Detection & Security Telemetry Lab.

## Prerequisites

- Python 3.10+
- Git
- Windows PowerShell or Command Prompt

## 1. Clone

```powershell
git clone https://github.com/vallabhatech/KaalDrishti.git
cd KaalDrishti
```

## 2. Create a virtual environment

### PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Command Prompt

```cmd
py -m venv .venv
.venv\Scripts\activate
```

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure

Copy `.env.example` to `.env`. For local development, the important settings are:

| Variable | Example |
|---|---|
| `KAALDRISHTI_ENDPOINT` | `http://127.0.0.1:5000/api/events` |
| `KAALDRISHTI_API_TOKEN` | `change-me` |
| `KAALDRISHTI_CLIENT` | `lab-client` |
| `KAALDRISHTI_INTERVAL` | `5` |
| `PORT` | `5000` |

## 5. Start the detection server

Open **Terminal 1**:

```powershell
python server.py
```

The server runs at `http://127.0.0.1:5000`.

Test it:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
```

## 6. Run the security event simulator

Open **Terminal 2**:

```powershell
python main.py
```

It generates synthetic, authorized security events for scenarios such as authentication brute force, suspicious processes, persistence attempts, network anomalies, and file-integrity changes.

The simulator does not capture keyboard input, clipboard contents, camera data, screenshots, or other user content.

## 7. Open the analyst GUI

Open **Terminal 3**:

```powershell
python control_gui.py
```

Choose a synthetic scenario and send it to the local detection API.

## 8. Run quality checks

```powershell
pytest
ruff check .
python -m compileall .
```

## 9. Data flow

```text
Synthetic Scenario
       |
       v
main.py simulator
       |
       v
Flask API
       |
       v
Detection Rules
       |
       v
SQLite Storage
       |
       v
Analyst GUI / API
```

## 10. Runtime database

Events are stored locally in:

```text
data/kaaldrishti.db
```

The `data/` directory is ignored by Git.

To reset local data:

```powershell
Remove-Item data/kaaldrishti.db -ErrorAction SilentlyContinue
```

## 11. API endpoints

- `GET /health` — service health
- `POST /api/events` — authorized synthetic event ingestion
- `GET /api/events` — recent stored events

When authentication is enabled, use the `X-API-Key` header.

## Troubleshooting

### Port already in use

Change `PORT` in `.env` and update `KAALDRISHTI_ENDPOINT` to use the same port.

### Module not found

Activate the virtual environment and run:

```powershell
pip install -r requirements.txt
```

### PowerShell activation is blocked

Run the virtual environment directly:

```powershell
.\.venv\Scripts\python.exe server.py
```

## Development workflow

Before committing:

```powershell
ruff check .
pytest
python -m compileall .
```

KaalDrishti is designed as a defensive cybersecurity learning and testing environment using synthetic, authorized telemetry.
