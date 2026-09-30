"""Environment-backed KaalDrishti configuration."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

CLOUD_ENDPOINT = os.getenv("KAALDRISHTI_ENDPOINT", "http://127.0.0.1:10000/api/events")
API_TOKEN = os.getenv("KAALDRISHTI_API_TOKEN", "")
CLIENT_NAME = os.getenv("KAALDRISHTI_CLIENT", "local-lab")
SEND_INTERVAL_SECONDS = max(1.0, float(os.getenv("KAALDRISHTI_INTERVAL", "10")))
MAX_REQUEST_BYTES = int(os.getenv("MAX_REQUEST_BYTES", "65536"))
PORT = int(os.getenv("PORT", "10000"))
