import common


def deactivate_profile():
    # Load json file
    config = common.read()

    active_profile = config.get("active_profile")

    if active_profile is None:
        print("⚠️ No active profile found!")
        common.return_to_main_menu()
        return

    print(f"Found active profile: {active_profile}")
    choice = input("Do you want to deactivate this profile? [y/n]: ")

    if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "":
        common.kill_runner()
        common.update_active_profile(None)
        print("✔ Profile deactivated!")
    else:
        print("Cancelled.")

    common.return_to_main_menu()
    return
