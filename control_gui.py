"""Local analyst console for generating and inspecting lab events."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

import requests

from config import API_TOKEN, CLOUD_ENDPOINT
from main import SCENARIOS, build_event


def run_gui() -> None:
    root = tk.Tk()
    root.title("KaalDrishti — Analyst Console")
    root.geometry("640x430")

    tk.Label(root, text="KaalDrishti Analyst Console", font=("Segoe UI", 18, "bold")).pack(pady=14)
    tk.Label(root, text="Generate authorized synthetic threat scenarios and inspect detections.").pack()

    scenario = tk.StringVar(value=SCENARIOS[0][0])
    tk.OptionMenu(root, scenario, *(name for name, _ in SCENARIOS)).pack(pady=12)

    output = tk.Text(root, height=12, width=72)
    output.pack(padx=16, pady=8)

    def send() -> None:
        if not API_TOKEN:
            messagebox.showwarning("Configuration", "Set KAALDRISHTI_API_TOKEN first.")
            return
        description = dict(SCENARIOS)[scenario.get()]
        event = build_event(scenario.get(), description)
        try:
            response = requests.post(
                CLOUD_ENDPOINT, json=event,
                headers={"X-API-Key": API_TOKEN}, timeout=10
            )
            output.insert("end", f"{response.status_code}: {response.text}\n")
        except requests.RequestException as exc:
            messagebox.showerror("Delivery failed", str(exc))

    tk.Button(root, text="Generate & Detect", command=send, width=24).pack(pady=10)
    tk.Button(root, text="Exit", command=root.destroy, width=24).pack()
    root.mainloop()


if __name__ == "__main__":
    run_gui()
