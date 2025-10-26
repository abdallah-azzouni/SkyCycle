import common
import os
import shutil


def copy_files(
    profile_name: str, wallpapers_path: str, profile_folder, images: list[str]
):
    try:
        # After user confirms

        os.makedirs(profile_folder, exist_ok=True)

        for i, img in enumerate(images, 1):
            src = os.path.join(wallpapers_path, img)
            dst = os.path.join(profile_folder, f"{i:03d}{os.path.splitext(img)[1]}")
            _ = shutil.copy2(src, dst)

        print(f"✓ {len(images)} images copied and renamed")
    except Exception as e:
        shutil.rmtree(profile_folder, ignore_errors=True)
        print(f"⚠️ Could not copy folder Error:{e}")


def add_profile():
    common.draw_header("Add New Profile ➕")

    print("\nStep 1/4: Profile Name")
    while True:
        profile_name = input("Enter a name for this profile: ")
        if os.path.isdir(f"{common.PROFILES_DIR}/{profile_name}"):
            print(f"profile {profile_name} already exist")
            continue
        if any(c in profile_name for c in "/\\"):
            print("Invalid name: cannot contain slashes.")
            continue
        else:
            break

    print("\nStep 2/4: Wallpaper Folder")
    while True:
        wallpapers_path = input(
            "Enter path to wallpapers folder (e.g. /path/to/wallpapers) [0. Quit]: "
        )

        if wallpapers_path == "0":
            return
        elif not os.path.isdir(wallpapers_path):
            print(f"⚠️ Could not find {wallpapers_path}")
            continue

        print("📂 Scanning folder...")

        images: list[str] = [
            f
            for f in os.listdir(wallpapers_path)
            if os.path.splitext(f)[1].lower() in {".jpg", ".jpeg", ".png"}
        ]
        images: list[str] = sorted(images, key=lambda s: s.lower())
        count = len(images)
        profile_folder = os.path.join(common.PROFILES_DIR, profile_name)

        if count < 4:
            print("⚠️ Folder must contain at least 4 images!")
        else:
            break

    print(f"  Found {count} images (.jpg, .png, ...)")

    choice = input(
        "Images will be COPIED (originals untouched) and renamed for indexing. Proceed? [Y/n]: "
    )
    if choice.lower() == "y" or choice == "":
        copy_files(profile_name, wallpapers_path, profile_folder, images)

    else:
        print("Cancelled.")
        return

    print("\nStep 3/4: Set Key Frames")
    print(
        "You need to select images for 4 key times:\n"
        + "- Midnight (darkest point)\n"
        + "- Sunrise\n"
        + "- Noon (brightest point)\n"
        + "- Sunset"
    )
    key_frames: list[str] = []
    frames_names = ["1. Midnight", "2. Sunrise", "3. Noon", "4. Sunset"]

    while len(key_frames) < 4:
        try:
            idx = int(
                input(f"Select image for {frames_names[len(key_frames)]} [1-{count}]: ")
            )
            if not (1 <= idx <= count):  # Check FIRST
                raise ValueError  # Force outer try-except to restart

            ext = os.path.splitext(images[idx - 1])[1].lower()
            key_frames.append(f"{idx:03d}{ext}")

        except (ValueError, IndexError) as e:
            print("Invalid Input. Try again.\n")
            continue

    print("\nStep 4/4: Review")
    print(
        f"Profile Name: {profile_name}\n"
        + f"Folder: {wallpapers_path}\n"
        + f"Images: {count} total"
    )

    print(
        "\nKey Frames:\n"
        + f"🌑 Midnight → {key_frames[0]}\n"
        + f"🌅 Sunrise → {key_frames[1]}\n"
        + f"☀️  Noon    → {key_frames[2]}\n"
        + f"🌇 Sunset  → {key_frames[3]}\n"
    )

    profile_path = f"{common.PROFILES_DIR}/{profile_name}"
    choice = input("Save this profile? [Y/n]: ")

    if choice.lower() == "y" or choice == "":
        # Add new profile to the profiles dict
        common.add_profile(
            profile_name,
            {
                "folder": profile_path,
                "image_count": count,
                "keyframes": {
                    "midnight": key_frames[0],
                    "sunrise": key_frames[1],
                    "noon": key_frames[2],
                    "sunset": key_frames[3],
                },
            },
        )
        print(f"\n✓ Profile {profile_name} created successfully!")

        _ = input("\nPress Enter to return to main menu...")
        return

    else:
        try:
            shutil.rmtree(profile_path)
            print(f"Folder '{profile_path}' and its contents removed successfully.")
        except OSError as e:
            print(f"Error removing folder '{profile_path}': {e}")
