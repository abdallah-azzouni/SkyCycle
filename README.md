# 🌅 Sky Cycle

**Sky Cycle** is a CLI tool that automatically updates your desktop wallpaper based on the sun's position. Configure multiple profiles with different wallpapers for different times of the day and let the app handle the rest.

---

## Features

- 🌍 Set your location to get accurate sunrise, sunset, and solar noon times.
- 📂 Add multiple wallpaper profiles.
- 🌑 Customize key frames for Midnight, Sunrise, Noon, and Sunset.
- ⚡ Automatically activate/deactivate profiles for dynamic wallpapers.
- ⚙️ Change settings like update interval and smooth transitions.

---

## Installation

```bash
# Clone repository
git clone https://github.com/abdallah-azzouni/SkyCycle.git
cd sky-cycle

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install astral pytz
```

> **Note:** `astral` and `pytz` are required for sun calculations.

---

## Usage

Run the application:

```bash
python main.py
```
