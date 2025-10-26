import common
import readline


def setup_platform():
    common.draw_header("Setup Platform")

    platforms = ["Windows", "Linux (KDE)", "Linux (Gnome)", "Linux (XFCE)", "Other"]
    print("\nSelect your platform:")
    for idx, platform in enumerate(platforms, start=1):
        print(f"  {idx}. {platform}")

    while True:
        try:
            choice = int(input(f"\nEnter your choice [1 - {len(platforms)}]: "))
            if not (1 <= choice <= len(platforms)):
                raise ValueError

            break

        except ValueError:
            print("Invalid input.")

    command = None
    if platforms[choice - 1] == "Other":
        print("Enter the command to change wallpaper.")
        command = input("Use {image} as placeholder for image path: ")

    common.update_platform(platforms[choice - 1], command)

    print("\nPlatform set to:", platforms[choice - 1])

    common.return_to_main_menu()
