"""Small local GUI for sending an explicit synthetic test event."""

import tkinter as tk
from tkinter import messagebox

from config import API_TOKEN, CLOUD_ENDPOINT
from main import build_event, send_event


def run_gui() -> None:
    root = tk.Tk()
    root.title("KaalDrishti Telemetry Lab")
    root.geometry("420x220")

    tk.Label(root, text="Consent-based security telemetry lab", font=("Segoe UI", 13, "bold")).pack(pady=16)
    tk.Label(root, text="This GUI sends only a synthetic event to the configured API.").pack(pady=4)

    def send_demo() -> None:
        event = build_event("demo.manual_event", "Manual test event created from the local GUI.")
        if not API_TOKEN:
            messagebox.showwarning("Configuration", "Set KAALDRISHTI_API_TOKEN before sending events.")
            return
        if send_event(event):
            messagebox.showinfo("Success", "Synthetic event accepted by the server.")
        else:
            messagebox.showerror("Delivery failed", f"Could not reach {CLOUD_ENDPOINT}")

    tk.Button(root, text="Send Synthetic Event", command=send_demo, width=24).pack(pady=14)
    tk.Button(root, text="Exit", command=root.destroy, width=24).pack()
    root.mainloop()


if __name__ == "__main__":
    run_gui()
