from geopy.geocoders import Nominatim
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import pytz
from unicodedata import normalize
import common
from tzfpy import get_tz


def normalize_text(text: str):
    return normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8").lower()


def search_city(q: str) -> list[any]:
    geolocator = Nominatim(user_agent="sky_cycle")
    locations = geolocator.geocode(q, exactly_one=False, limit=5, language="en")
    if not locations:
        print("No results found.")
        return []
    print("Found locations:")
    for i, loc in enumerate(locations, 1):
        # map location into name, country
        address_parts = [
            p.strip() for p in loc.address.split(",")
        ]  # make sure location is clean to map
        name = address_parts[0] if address_parts else "Unknown"
        country = address_parts[-1] if len(address_parts) > 1 else "Unknown"
        lon_dir = "E" if loc.longitude >= 0 else "W"
        print(
            f"  {i}. {name}, {country} ({loc.latitude:.4f}°N, {abs(loc.longitude):.4f}°{lon_dir})"
        )
    print("  0. Quit\n")
    return locations


def setup_location():
    print(
        f"{common.margin * ' '}╔════════════════════════════════════════════════╗\n"
        + f"{common.margin * ' '}║                Setup Location 📍               ║\n"
        + f"{common.margin * ' '}╚════════════════════════════════════════════════╝"
    )

    while True:
        query = input("Enter location: ").strip()
        clean_query = normalize_text(query)

        print(f'\n🔍 Searching for "{query}"...\n')
        results = search_city(clean_query)
        if not results:
            continue

        while True:
            try:
                choice = int(input(f"\nSelect [0-{len(results)}]: "))
            except ValueError:
                print("Invalid input.")
                continue

            if choice == 0:
                print("Cancelled.")
                return
            if not (1 <= choice <= len(results)):
                print("Invalid number.")
                continue

            break

        selected = results[choice - 1]
        lat, lon = selected.latitude, selected.longitude
        # Use safe address parsing (consistent with search_city)
        address_parts = [p.strip() for p in selected.address.split(",")]
        name = address_parts[0] if address_parts else "Unknown"
        country = address_parts[-1] if len(address_parts) > 1 else "Unknown"

        # Auto-detect timezone from lat/lon
        timezone_str = get_tz(lng=lon, lat=lat)
        if not timezone_str:
            print("⚠️ Could not determine timezone. Falling back to UTC.")
            timezone_str = "UTC"

        tz = pytz.timezone(timezone_str)
        city = LocationInfo(name, country, timezone_str, lat, lon)
        today = datetime.now(tz).date()
        try:
            s = sun(city.observer, date=today, tzinfo=tz)
        except Exception as e:
            print(f"⚠️ Could not calculate sun times: {e}")
            return

        common.write(
            {
                "location": {
                    "name": name,
                    "country": country,
                    "latitude": lat,
                    "longitude": lon,
                    "timezone": timezone_str,
                }
            }
        )

        print(f"\n✓ Location set to: {name}, {country}")
        print(f"  Latitude: {lat:.4f}°")
        print(f"  Longitude: {lon:.4f}°")
        print(f"  Timezone: {timezone_str}")
        print(f"  🌅 Sunrise: {s['sunrise'].strftime('%I:%M %p')}")
        print(f"  🌇 Sunset:  {s['sunset'].strftime('%I:%M %p')}")

        input("\nPress Enter to return to main menu...")
        break
