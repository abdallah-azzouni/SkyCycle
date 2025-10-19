import common


def exit_program():
    print("\nExiting Sky Cycle. Goodbye! 👋")
    exit()


def main():
    # Load json file
    data = common.load()

    # ui options
    margin = 5

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
        # 1: setup_location(),
        # 2: add_profile(),
        # 3: remove_profile(),
        0: exit_program,
    }

    print(
        f"{margin * ' '}╔════════════════════════════════════════════════╗\n{margin * ' '}║                 🌅 Sky Cycle                   ║\n{margin * ' '}╚════════════════════════════════════════════════╝"
    )
    print(f"     Active Profile: {data.get('active_profile', 'None')}")

    print(
        f"{margin * ' '}Location: set ✔"
        if data.get("location")
        else f"{margin * ' '}Location: Not set ⚠️"
    )
    print(f"{margin * ' '}Active Profile: {data.get('active_profile', 'None')}")

    print(f"{margin * ' '}┌─ Main Menu ────────────────────────────────────┐")

    for idx, option in MENU_OPTIONS.items():
        print(f"{margin * ' '}│  {idx}. {option:<41}  │")

    print(f"{margin * ' '}└────────────────────────────────────────────────┘")

    valid_option = False

    # get user input
    while not valid_option:
        try:
            choice = int(input("Choose option [0-6]: "))
            if choice in MENU_OPTIONS.keys():
                valid_option = True
            else:
                print("Invalid option")
        except ValueError:
            print("Invalid input.")

    ROUTES[choice]()


if __name__ == "__main__":
    main()
