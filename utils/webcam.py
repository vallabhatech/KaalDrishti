import cv2
import os
from datetime import datetime

def capture_webcam_photo(save_dir="logs"):
    try:
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(save_dir, f"webcam_{timestamp}.jpg")

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame)
        cap.release()
        return filename if ret else None
    except Exception as e:
        print("❌ Webcam error:", e)
        return None
