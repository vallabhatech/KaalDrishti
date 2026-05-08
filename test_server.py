import requests
from config import CLOUD_ENDPOINT

# Test 1: Check if server is running
print("🧪 Test 1: Checking server health...")
try:
    base_url = CLOUD_ENDPOINT.replace("/upload_log", "")
    response = requests.get(f"{base_url}/health")
    print(f"✅ Server responded: {response.status_code}")
    print(f"📊 Health status: {response.json()}")
    print()
except Exception as e:
    print(f"❌ Health check failed: {e}")
    print()

# Test 2: Check main endpoint
print("🧪 Test 2: Checking main endpoint...")
try:
    response = requests.get(base_url)
    print(f"✅ Main endpoint: {response.text}")
    print()
except Exception as e:
    print(f"❌ Main endpoint failed: {e}")
    print()

print("=" * 50)
print("📋 SUMMARY:")
print("If you see health status above, check these values:")
print("  - email_configured: should be true")
print("  - supabase_url_set: should be true")
print("  - supabase_key_set: should be true")
print("  - supabase_connected: should be true")
print()
print("If any are false, you need to add those environment")
print("variables in Render Dashboard!")
