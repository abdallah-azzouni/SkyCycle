import common
import os
import shutil
import readline


def remove_profile():
    common.draw_header("Remove Profile ➖")

    config = common.read()

    if not config["profiles"]:
        print("No profiles found.")
        _ = input("\nPress Enter to return to main menu...")
        return

    print("\nSaved Profiles:")

    profiles = list(config["profiles"].keys())
    for i, profile_name in enumerate(profiles, start=1):
        image_count = config["profiles"][profile_name]["image_count"]
        print(f"  {i}. {profile_name} ({image_count} images)")

    while True:
        try:
            choice = int(
                input(
                    f"\nSelect profile to remove [1-{len(profiles)}, or 0 to cancel]: "
                )
            )

            if choice == 0:
                return
            if not (1 <= choice <= len(profiles)):
                raise ValueError

        except ValueError:
            print("Invalid input. Try again.")
            continue

        break

    profile_name = profiles[choice - 1]
    folder_path = config["profiles"][profile_name]["folder"]

    print(f"\nYou selected: {profile_name}\nFolder: {folder_path}")
    print("\n⚠️  This will remove the profile from the list.")

    x = input("\nAre you sure? [Y/n]: ")
    if x.lower() == "y" or x == "":
        try:
            # Remove from JSON
            common.remove_profile(profile_name)

            # delete if folder exists
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                print(f'✓ Profile "{profile_name}" and files removed')
            else:
                print(f'✓ Profile "{profile_name}" removed (files already gone)')

        except KeyError:
            print("⚠️ Profile not found in config")
        except PermissionError:
            print("⚠️ Permission denied - cannot delete files")
        except Exception as e:
            print(f"⚠️ Error: {e}")

    _ = input("\nPress Enter to return to main menu...")
