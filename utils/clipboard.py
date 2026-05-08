# utils/clipboard.py

import pyperclip

def get_clipboard_data():
    try:
        clipboard_data = pyperclip.paste()
        if clipboard_data:
            return f"\n[CLIPBOARD]\n{clipboard_data}\n"
        else:
            return "\n[CLIPBOARD]\nNo data found.\n"
    except Exception as e:
        return f"\n[CLIPBOARD]\nFailed to read clipboard: {e}\n"
