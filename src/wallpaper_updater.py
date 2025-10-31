import common
from datetime import datetime, time
import pytz
import os
import subprocess


def time_minuts(time: time) -> int:
    return round(time.hour * 60 + time.minute + time.second / 60)


def find_periods(keyframes_time, current_time):
    for i in range(len(keyframes_time)-1):
        if current_time >= keyframes_time[i][1] and keyframes_time[i+1][1] >= current_time:
            return keyframes_time[i], keyframes_time[(i + 1) % len(keyframes_time)]
    return keyframes_time[-1], keyframes_time[0]

def run():
    # Innit data
    config = common.read()

    active_profile = config.get("active_profile")
    current_profile = config.get("profiles").get(active_profile)
    user_platform = config.get("platform")
    cached_sun_times = config.get("cached_sun_times")

    location_data = config.get("location")

    tz = pytz.timezone(location_data["timezone"])
    current_time = time_minuts(datetime.now(tz).time())

    if None in (active_profile, user_platform, location_data, current_profile):
        print("Error: Missing data")
        print("Please activate profile from main menu")
        return



    if cached_sun_times is None:
        need_update = True
    else:
        cached_date = datetime.fromisoformat(cached_sun_times["date"]).date()
        need_update = cached_date < datetime.now(tz).date()

    if need_update:
        s = common.calculate_sun_times(
            location_data["name"],
            location_data["country"],
            location_data["latitude"],
            location_data["longitude"],
            location_data["timezone"],
        )
        if s is None:
            print("Error: Could not calculate sun times")
            s = {k: datetime.fromisoformat(v) for k, v in cached_sun_times["sun_times"].items()}
        else:
            common.update_cached_sun_times({
                "date": datetime.now(tz).date().isoformat(),
                "sun_times": {k: v.isoformat() for k, v in s.items()}
            })


    else:
        s = {k: datetime.fromisoformat(v) for k, v in cached_sun_times["sun_times"].items()}


    if s is None:
        print("Error: Could not calculate sun times")
        return

    keyframes = current_profile["keyframes"]

    keyframes_time = [(int(keyframes[k].split(".")[0]), time_minuts(s[k].time())) for k in s if k in keyframes]  # [(frame idx, frame time)]

    # Find current image #######################################################
    period = find_periods(keyframes_time, current_time)
    start_time, end_time = period[0][1], period[1][1]
    start_img, end_img = period[0][0], period[1][0]

    # handle midnight wrap without changing current_time
    adj_end = end_time
    adj_i = current_time
    if end_time < start_time:
        adj_end += 1440
        if current_time < start_time:
            adj_i += 1440

    fraction = (adj_i - start_time) / (adj_end - start_time)
    current_img = round(start_img + fraction * (end_img - start_img))

    # Update wallpaper #########################################################
    img_base = os.path.join(common.PROFILES_DIR, active_profile, f"{current_img:03d}")

    # detect  image type
    for ext in ["png", "jpg", "jpeg"]:
        img_path = f"{img_base}.{ext}"
        if os.path.exists(img_path):
            command = common.DEFAULT_COMMANDS[user_platform].replace("{image}", img_path)
            subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            break
