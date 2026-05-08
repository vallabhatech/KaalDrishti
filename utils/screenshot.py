from PIL import ImageGrab
import os
from datetime import datetime

def take_screenshot(save_dir="logs"):
    try:
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(save_dir, f"screenshot_{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(file_path)
        return file_path
    except Exception as e:
        print("❌ Screenshot error:", e)
        return None
