# KaalDrishti

KaalDrishti is a modular Python monitoring framework for controlled security labs and endpoint telemetry experiments. It combines keystroke capture, host context collection, screenshot/webcam snapshots, and remote ingestion into a Flask-based receiver for analysis workflows.

## Maintainer

- **GitHub:** [vallabhatech](https://github.com/vallabhatech/KaalDrishti)

## Features

Based on the current codebase (`main.py`, `server.py`, `persistence.py`, `utils/*`):

- Keystroke logging with automatic append to local log storage (`logs/keylog.txt`)
- Clipboard data capture (`utils/clipboard.py`)
- System fingerprint collection (username, host, IP, OS, CPU, machine) (`utils/system_info.py`)
- Periodic screenshot capture with timestamped files (`utils/screenshot.py`)
- Periodic webcam snapshot capture with timestamped files (`utils/webcam.py`)
- Continuous background upload loop from client to server via `POST /upload_log`
- Upload retry handling for transient timeout conditions
- Automatic keylog clearing after successful remote delivery
- Flask receiver API for ingesting text telemetry and image artifacts (`server.py`)
- Local artifact persistence in `uploads/`
- Optional Supabase Storage upload for screenshot/webcam artifacts
- Optional email alerting with telemetry summary + image attachments
- Health endpoint for server configuration validation (`GET /health`)
- Optional wake script for cold-started hosting environments (`wake_server.py`)
- Windows startup persistence helper (`persistence.py`)

## Project Structure

```text
KaalDrishti/
+- main.py
+- server.py
+- config.py
+- persistence.py
+- wake_server.py
+- control_gui.py
+- requirements.txt
+- logs/
+- uploads/                # created by server at runtime
+- utils/
   +- clipboard.py
   +- screenshot.py
   +- system_info.py
   +- webcam.py
   +- self_destruct.py
```

## Prerequisites

- Python 3.10+
- pip
- Webcam device (for webcam capture features)
- GUI-capable environment (for Pillow `ImageGrab` screenshot capture)
- Internet access between client and server endpoint

Optional (server integrations):

- Email account + app password for SMTP (`EMAIL`, `PASSWORD`)
- Supabase project (`SUPABASE_URL`, `SUPABASE_KEY`) with bucket `key_logger_images`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/vallabhatech/KaalDrishti.git
cd KaalDrishti
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows (PowerShell):

```bash
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure client endpoint in `config.py`:

- Set `CLOUD_ENDPOINT` to your server URL, e.g. `https://<your-host>/upload_log`

5. Configure server environment variables (if using integrations):

```bash
EMAIL=<your_email>
PASSWORD=<your_email_app_password>
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_service_or_anon_key>
```

## Usage

### 1. Start the server (receiver)

From project root:

```bash
python server.py
```

Default runtime behavior:

- Binds to `0.0.0.0`
- Uses `PORT` env var if present; otherwise defaults to `10000`

Health check:

```bash
curl http://localhost:10000/health
```

### 2. (Optional) Wake remote server before client start

Useful for free-tier/cold-start hosts:

```bash
python wake_server.py
```

### 3. Start the client collector

```bash
python main.py
```

Client behavior:

- Starts keyboard listener
- Every ~5 seconds captures telemetry/artifacts
- Sends data to `CLOUD_ENDPOINT`
- Retries on timeout and continues loop

### 4. (Optional) Manual capture GUI

```bash
python control_gui.py
```

## Configuration Notes

- `LOG_FILE` path is configured in `config.py`
- Client logs and captured artifacts are stored under `logs/`
- Server-ingested files and text outputs are stored under `uploads/`

## Legal & Ethical Disclaimer

> **Strict Notice:** KaalDrishti is provided strictly for **educational purposes**, **authorized security testing**, and **personal use on systems you own or are explicitly permitted to assess**.
>
> Unauthorized monitoring, data capture, credential interception, or surveillance may violate privacy laws and criminal statutes in your jurisdiction.
>
> By using this project, you accept full responsibility for compliance with all applicable laws, policies, and authorization requirements.
>
> **The author/maintainer ([vallabhatech](https://github.com/vallabhatech/KaalDrishti)) is not responsible for any misuse, abuse, damages, or legal consequences arising from improper or unauthorized use.**

## License

No license file is currently defined in this repository. Add a license before redistribution or commercial use.
