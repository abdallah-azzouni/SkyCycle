import json
import os
import platform
from wcwidth import wcswidth

# ui options
margin = 5


if platform.system() == "Windows":
    CONFIG_DIR = os.path.join(os.getenv("APPDATA"), "SkyCycle")
else:
    CONFIG_DIR = os.path.expanduser("~/.config/SkyCycle")

CONFIG_FILE = os.path.join(CONFIG_DIR, "data.json")
PROFILES_DIR = os.path.join(CONFIG_DIR, "profiles")


def init():
    """Initialize config directory and files. Call this once at app startup."""
    # Create directories if they don't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(PROFILES_DIR, exist_ok=True)

    # Create default config if it doesn't exist
    if not os.path.exists(CONFIG_FILE):
        default_config = {"location": None, "active_profile": None, "profiles": {}}
        write(default_config)


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
    if config.get("profiles", None) == None:
        config["profiles"] = {}
    config["profiles"][profile_name] = profile_data
    write(config)


def remove_profile(profile_name: str):
    """Remove a profile from config"""
    config = read()
    if config.get("profiles", None) == None:
        config["profiles"] = {}
    if profile_name in config["profiles"]:
        del config["profiles"][profile_name]
        write(config)


def update_active_profile(profile_name: str):
    config = read()
    config["active_profile"] = profile_name
    write(config)


def update_location(location_data):
    config = read()
    config["location"] = location_data
    write(config)
