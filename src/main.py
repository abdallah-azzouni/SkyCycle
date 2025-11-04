import common
import argparse
import os
import wallpaper_updater
import psutil
import sys
from routes import (
    setup_location,
    add_profile,
    remove_profile,
    activate_profile,
    setup_platform,
    deactivate_profile,
)


def exit_program():
    print("\nExiting Sky Cycle. Goodbye! 👋")
    sys.exit(0)


MENU_OPTIONS = {
    1: "Setup Location",
    2: "Add Profile",
    3: "Remove Profile",
    4: "Activate Profile",
    5: "Deactivate Profile",
    6: "Setup Platform",
    0: "Exit",
}

# Define pages you can switch too
ROUTES = {
    1: setup_location.setup_location,
    2: add_profile.add_profile,
    3: remove_profile.remove_profile,
    4: activate_profile.activate_profile,
    5: deactivate_profile.deactivate_profile,
    6: setup_platform.setup_platform,
    0: exit_program,
}


def main():
    """
    Main hub for CLI modules stored in `routes`.

    - Displays the main menu.
    - Loads and updates persistent data.
    - Routes user choices to the appropriate module.
    """
    common.init()

    while True:
        _ = os.system("cls" if os.name == "nt" else "clear")  # clear screen

        # Load json file
        data = common.read()

        common.draw_header("🌅 Sky Cycle")

        print(
            f"{common.margin * ' '}Location: set ✔"
            if data.get("location")
            else f"{common.margin * ' '}Location: Not set ⚠️"
        )

        print(f"{common.margin * ' '}Platform: {data.get('platform', 'Not set ⚠️')}")

        print(
            f"{common.margin * ' '}Active Profile: {data.get('active_profile', 'None')}"
        )

        if common.get_runner_pid() == -1:
            runner_status = 'Not running ⚠️'
        else:
            runner_status = "Running"

        print(f"{common.margin * ' '}Runner: {runner_status}")

        print(
            f"{common.margin * ' '}┌─ Main Menu ────────────────────────────────────┐"
        )

        for idx, option in MENU_OPTIONS.items():
            print(f"{common.margin * ' '}│  {idx}. {option:<41}  │")

        print(
            f"{common.margin * ' '}└────────────────────────────────────────────────┘"
        )

        # get user input
        while True:
            try:
                choice = int(input("Choose option [0-6]: "))
                if choice in MENU_OPTIONS.keys():
                    break
                else:
                    print("Invalid option")
            except ValueError:
                print("Invalid input.")

        ROUTES[choice]()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SkyCycle Application")
    _ = parser.add_argument(
        "--update-wallpaper",
        action="store_true",
        help="Update wallpaper",
    )
    args = parser.parse_args()

    if args.update_wallpaper:
        wallpaper_updater.run()
    else:
        main()
