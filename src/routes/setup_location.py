from datetime import datetime, timedelta
import pytz  # you might need to install this: pip install pytz
from astral import LocationInfo
from astral.sun import sun


def setup_location():
    # Correct location with timezone
    city = LocationInfo("Doha", "Qatar", "Asia/Qatar", 25.276987, 51.520008)

    tz = pytz.timezone(city.timezone)
    today = datetime.now(tz).date()

    s = sun(city.observer, date=today, tzinfo=tz)

    print(f"Sunrise: {s['sunrise'].time()}")
    print(f"Sunset: {s['sunset'].time()}")
    print(f"Solar noon: {s['noon'].time()}")

    # Middle of night: halfway between today's sunset and tomorrow's sunrise
    tomorrow = today + timedelta(days=1)
    s_tomorrow = sun(city.observer, date=tomorrow, tzinfo=tz)

    sunset_today = s["sunset"]
    sunrise_tomorrow = s_tomorrow["sunrise"]
    middle_of_night = sunset_today + (sunrise_tomorrow - sunset_today) / 2

    print(f"Middle of night: {middle_of_night.time()}")
