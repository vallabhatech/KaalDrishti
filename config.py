"""Runtime configuration loaded from environment variables."""

import os

CLOUD_ENDPOINT = os.getenv("KAALDRISHTI_ENDPOINT", "http://127.0.0.1:10000/api/events")
API_TOKEN = os.getenv("KAALDRISHTI_API_TOKEN", "")
CLIENT_NAME = os.getenv("KAALDRISHTI_CLIENT", "local-lab")
SEND_INTERVAL_SECONDS = float(os.getenv("KAALDRISHTI_INTERVAL", "10"))
