import tkinter as tk
from tkinter import messagebox
from utils.screenshot import take_screenshot
from utils.webcam import capture_webcam  # ✅ Corrected import

def run_gui():
    root = tk.Tk()
    root.title("Keylogger Control Panel")
    root.geometry("300x200")

    def capture_screen():
        take_screenshot("logs/manual_screenshot.jpg")
        messagebox.showinfo("Success", "Screenshot captured.")

    def capture_webcam_image():
        capture_webcam("logs/manual_webcam.jpg")  # ✅ Corrected function call
        messagebox.showinfo("Success", "Webcam snapshot captured.")

    tk.Button(root, text="Capture Screenshot", command=capture_screen).pack(pady=10)
    tk.Button(root, text="Capture Webcam", command=capture_webcam_image).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
