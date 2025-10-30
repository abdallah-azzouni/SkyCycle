import common
import pytz
from datetime import datetime


def activate_profile():
    common.draw_header("Activate Profile 🟢")

    config = common.read()

    if config.get("platform") is None:
        print("\n⚠️  Platform not set! Please setup platform first.")
        common.return_to_main_menu()
        return

    if config.get("location") is None:
        print("\n⚠️  Location not set! Please setup location first.")
        common.return_to_main_menu()
        return

    if not config.get("profiles"):
        print("⚠️  No profiles available. Please add a profile first.")

    print("\nSaved Profiles:")

    profiles = list(config["profiles"].keys())
    for i, profile_name in enumerate(profiles, start=1):
        image_count = config["profiles"][profile_name]["image_count"]
        print(f"  {i}. {profile_name} ({image_count} images)")
    print("  0. Cancel\n")

    while True:
        try:
            choice = int(input(f"Select profile to activate [0-{len(profiles)}]: "))
            if choice == 0:
                return
            if not (1 <= choice <= len(profiles)):
                raise ValueError

        except ValueError:
            print("Invalid input. Try again.")
            continue

        break

    profile_name: str = profiles[choice - 1]
    folder_path = config["profiles"][profile_name]["folder"]

    if profile_name == config["active_profile"]:
        print(f'ℹ️  "{profile_name}" is already active.')
        choice = input("\nDo you want to refresh the runner? [Y/n]: ")
        if choice.lower() == "y" or choice.lower() == "yes" or choice.lower() == "":
            common.restart_runner()

        common.return_to_main_menu()
        return

    print(f'\n🔄 Activating "{profile_name}"...')

    location_data = list(config["location"].values())
    # 0. name, 1. country, 2. lat, 3. lon, 4. timezone

    sun = common.calculate_sun_times(
        location_data[0],
        location_data[1],
        location_data[2],
        location_data[3],
        location_data[4],
    )

    if sun is None:
        common.return_to_main_menu()
        return

    print(
        f"\n📍 Location: {config['location']['name']}, {config['location']['country']}",
        f"\n🕐 Current time: {datetime.now(pytz.timezone(location_data[4])).strftime('%I:%M %p')}\n",
        "\n☀️  Sun times today:",
    )
    for keyframe, value in config["profiles"][profile_name]["keyframes"].items():
        print(f" {keyframe}: {sun[keyframe].strftime('%I:%M %p')} -> {value}")

    choice = input("\n⚠️  Are you sure you want to activate this profile? [Y/n]: ")

    if choice.lower() != "y" and choice.lower() != "yes" and choice.lower() != "":
        print("Cancelled.")
        common.return_to_main_menu()
        return

    common.update_active_profile(profile_name)
    common.restart_runner()

    print(f'✓ Profile "{profile_name}" is now active!')
    print("Your wallpaper will automatically change based on the sun's position.")

    # start runner in background

    common.return_to_main_menu()
