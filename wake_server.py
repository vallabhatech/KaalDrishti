"""
Quick script to wake up Render server before running main keylogger
"""
import requests
from config import CLOUD_ENDPOINT

base_url = CLOUD_ENDPOINT.replace("/upload_log", "")

print("🔔 Waking up Render server...")
print(f"🌐 URL: {base_url}")

try:
    response = requests.get(base_url, timeout=60)
    print(f"✅ Server is awake: {response.text}")
    print("\n✨ Server is ready! You can now run main.py")
except Exception as e:
    print(f"❌ Failed to wake server: {e}")
    print("⚠️ Server might be starting up. Wait 30 seconds and try again.")
