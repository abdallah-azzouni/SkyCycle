# 🌅 Sky Cycle

![License](https://img.shields.io/github/license/abdallah-azzouni/SkyCycle)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

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

### Option 1: Pre-built Binaries (Recommended)

Download the latest release for your platform:

- **Linux**: [skycycle-linux-x64](https://github.com/abdallah-azzouni/SkyCycle/releases/latest)
- **Windows**: [skycycle-windows-x64.exe](https://github.com/abdallah-azzouni/SkyCycle/releases/latest)
```bash
# Linux
chmod +x skycycle
./skycycle

# Windows
skycycle.exe
```

### Option 2: Build from Source
```bash
# Install UV

# Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"


# Clone and build
git clone https://github.com/abdallah-azzouni/SkyCycle.git
cd SkyCycle
uv sync

# Run
uv run python src/main.py
```

---

## Usage

### First Time Setup

1. **Set Location**: Choose your city to calculate sun times
2. **Add Profile**: Select a folder with wallpapers and set key frames
3. **Activate Profile**: Enable automatic wallpaper changes

### Main Menu
```
╔════════════════════════════════════════════════╗
║                 🌅 Sky Cycle                   ║
╚════════════════════════════════════════════════╝
Location: set ✔
Active Profile: None
┌─ Main Menu ────────────────────────────────────┐
│  1. Setup Location                             │
│  2. Add Profile                                │
│  3. Remove Profile                             │
│  4. Activate Profile                           │
│  5. Deactivate                                 │
│  6. Settings                                   │
│  0. Exit                                       │
└────────────────────────────────────────────────┘
```

---

## Configuration

Sky Cycle stores its configuration in:
- **Linux**: `~/.config/SkyCycle/`
- **Windows**: `%APPDATA%\SkyCycle\`

---

## Development

### Running from Source
```bash
uv run python src/main.py
```

### Adding Dependencies
```bash
uv add package-name
```

### Building Binaries
```bash
# Install PyInstaller
uv add --dev pyinstaller

# Build
uv run pyinstaller --onefile src/main.py --name skycycle
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/abdallah-azzouni/SkyCycle/blob/main/LICENSE) file for details

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
