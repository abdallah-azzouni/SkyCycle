import common


def activate_profile():
    common.draw_header("Activate Profile 🟢")

    config = common.read()

    if config.get("platform") is None:
        print("\nPlease pick a platform from Settings before activating a profile.")

    _ = input("\nPress Enter to return to main menu...")
