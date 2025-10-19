import common


def main():
    # Load json file
    data = common.load()

    MENU_OPTIONS = {
        1: "Setup Location",
        2: "Add Profile",
        3: "Remove Profile",
        4: "Activate Profile",
        5: "Deactivate",
        6: "Settings",
        0: "Exit",
    }

    print("""
        ╔════════════════════════════════════════════════╗
        ║                 🌅 Sky Cycle                   ║
        ╚════════════════════════════════════════════════╝""")

    print(
        "     Location: set ✔" if data.get("location") else "     Location: Not set ⚠️"
    )
    print(f"     Active Profile: {data.get('active_profile', 'None')}")

    print("     ┌─ Main Menu ────────────────────────────────────┐")

    for idx, option in MENU_OPTIONS.items():
        print(f"     │  {idx}. {option:<41}  │")

    print("     └────────────────────────────────────────────────┘")

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


if __name__ == "__main__":
    main()
