import common
import os
from routes import setup_location, add_profile, remove_profile


def exit_program():
    print("\nExiting Sky Cycle. Goodbye! 👋")
    exit()


MENU_OPTIONS = {
    1: "Setup Location",
    2: "Add Profile",
    3: "Remove Profile",
    4: "Activate Profile",
    5: "Deactivate",
    6: "Settings",
    0: "Exit",
}

# Define pages you can switch too
ROUTES = {
    1: setup_location.setup_location,
    2: add_profile.add_profile,
    3: remove_profile.remove_profile,
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
    main()
