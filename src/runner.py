import os
import subprocess
from time import sleep
import platform
import sys

if platform.system() == "Windows":
    CONFIG_DIR = os.path.join(os.getenv("APPDATA"), "SkyCycle")
    user_platform = "Windows"
else:
    CONFIG_DIR = os.path.expanduser("~/.config/SkyCycle")

# Save PID for kill/restart
PID_FILE = os.path.join(CONFIG_DIR, "runner.pid")
if os.path.exists(PID_FILE):
    os.remove(PID_FILE)
with open(PID_FILE, "w") as f:
    f.write(str(os.getpid()))

# Determine command based on what's available near runner.py
if getattr(sys, "frozen", False):
    base_dir = os.path.dirname(sys.executable)
    if platform.system() == "Windows":
        cmd = [os.path.join(base_dir, "skycycle.exe"), "--update-wallpaper"]
    else:
        cmd = [os.path.join(base_dir, "skycycle"), "--update-wallpaper"]
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = ["uv", "run", os.path.join(base_dir, "main.py"), "--update-wallpaper"]

# Run in loop
while True:
    if platform.system() == "Windows":
        subprocess.Popen(
            cmd,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.run(cmd)
    sleep(60)
