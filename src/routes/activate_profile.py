import common


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
