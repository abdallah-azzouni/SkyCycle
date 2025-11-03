import json
import os
import platform
from wcwidth import wcswidth
from astral import LocationInfo
from astral.sun import sun, midnight
from datetime import datetime
import pytz
import subprocess
import sys

# ui options
margin = 5

user_platform = None


if platform.system() == "Windows":
    CONFIG_DIR = os.path.join(os.getenv("APPDATA"), "SkyCycle")
    user_platform = "Windows"
else:
    import readline  # Enables arrow key navigation in input() on linux

    CONFIG_DIR = os.path.expanduser("~/.config/SkyCycle")

CONFIG_FILE = os.path.join(CONFIG_DIR, "data.json")
PROFILES_DIR = os.path.join(CONFIG_DIR, "profiles")
PID_FILE = os.path.join(CONFIG_DIR, "runner.pid")

# Determine executable name and base directory based on if compiled or not
if getattr(sys, "frozen", False):
    compiled = True
    base_dir = os.path.dirname(sys.executable)  # compiled binary
else:
    compiled = False
    base_dir = os.path.dirname(os.path.abspath(__file__))  # source

RUNNER_FILE = os.path.join(base_dir, "runner.py")

DEFAULT_COMMANDS = {
    "Windows": 'reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v Wallpaper /t REG_SZ /d "{image}" /f && RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters',
    "Linux (KDE)": '''qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "
    var allDesktops = desktops();for (i=0;i<allDesktops.length;i++) {d = allDesktops[i];d.wallpaperPlugin = 'org.kde.image';
    d.currentConfigGroup = Array('Wallpaper','org.kde.image','General');d.writeConfig('Image', 'file://{image}');}"''',
    "Linux (GNOME)": 'gsettings set org.gnome.desktop.background picture-uri "file://{image}"',
    "Linux (XFCE)": 'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s "{image}"',
    "macOS": 'osascript -e \'tell application "System Events" to tell every desktop to set picture to "{image}"\'',
}


def init():
    global compiled, user_platform
    """Initialize config directory and files. Call this once at app startup."""
    # Create directories if they don't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(PROFILES_DIR, exist_ok=True)

    # Create default config if it doesn't exist
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "platform": user_platform,
            "custom_command": None,
            "location": None,
            "active_profile": None,
            "profiles": {},
            "cached_sun_times": None,
        }
        write(default_config)


# user interface functions #####################################################
def return_to_main_menu():
    _ = input("\nPress Enter to return to main menu...")


def draw_header(title: str):
    display_width = wcswidth(title)
    # Fallback if wcwidth returns -1 (control characters)
    if display_width < 0:
        display_width = len(title)

    total_padding = 48 - display_width
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding

    print(f"{margin * ' '}╔════════════════════════════════════════════════╗")
    print(f"{margin * ' '}║{left_padding * ' '}{title}{right_padding * ' '}║")
    print(f"{margin * ' '}╚════════════════════════════════════════════════╝")


#################################################################################


# I/O functions ###############################################################
def read():
    """Read config file"""
    if not os.path.exists(CONFIG_FILE):
        init()  # Safety fallback

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def write(data):
    """Write to config file"""
    if not os.path.exists(CONFIG_DIR):
        init()  # Safety fallback

    tmp = CONFIG_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, CONFIG_FILE)


def add_profile(profile_name: str, profile_data):
    """Add or update a profile in config"""
    config = read()
    if not config.get("profiles"):
        config["profiles"] = {}
    config["profiles"][profile_name] = profile_data
    write(config)


def remove_profile(profile_name: str):
    """Remove a profile from config"""
    config = read()
    if not config.get("profiles"):
        config["profiles"] = {}
    if profile_name in config["profiles"]:
        del config["profiles"][profile_name]
        write(config)


def update_active_profile(profile_name):
    config = read()
    config["active_profile"] = profile_name
    write(config)


def update_location(location_data):
    config = read()
    config["location"] = location_data
    write(config)


def update_platform(platform: str, command: str | None = None):
    config = read()
    config["platform"] = platform
    config["custom_command"] = command
    write(config)


def update_cached_sun_times(sun_times):
    config = read()
    config["cached_sun_times"] = sun_times
    write(config)


################################################################################


def calculate_sun_times(
    name: str, country: str, lat: float, lon: float, timezone_str: str
):
    tz = pytz.timezone(timezone_str)
    city = LocationInfo(name, country, timezone_str, lat, lon)
    today = datetime.now(tz).date()
    try:
        s = sun(city.observer, date=today, tzinfo=tz)
        s["midnight"] = midnight(city.observer, date=today, tzinfo=tz)
        used_times = {"sunrise", "noon", "sunset", "midnight"}
        s = {k: v for k, v in s.items() if k in used_times}

    except Exception as e:
        print(f"⚠️ Could not calculate sun times: {e}")
        return

    return s


def kill_runner():
    # Kill old process if exists
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())

            if platform.system() == "Windows":
                _ = subprocess.run(
                    ["taskkill", "/PID", str(pid), "/F"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                _ = subprocess.run(
                    ["kill", str(pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        except:
            pass


def restart_runner():
    kill_runner()

    if platform.system() == "Windows":
        p = subprocess.Popen(
            [sys.executable, RUNNER_FILE],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    else:
        p = subprocess.Popen(
            [sys.executable, RUNNER_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
