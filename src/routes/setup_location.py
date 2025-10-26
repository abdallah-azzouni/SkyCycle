from geopy.geocoders import Nominatim
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import pytz
import common
from tzfpy import get_tz


def search_city(q: str):
    try:
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
    except Exception as e:
        print(f"⚠️ Could not find any results, try again later. Error: {e}")
        return []


def setup_location():
    common.draw_header("Setup Location 📍")

    while True:
        query = input("Enter location: ").strip()

        print(f'\n🔍 Searching for "{query}"...\n')
        results = search_city(query)
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

        common.update_location(
            {
                "name": name,
                "country": country,
                "latitude": lat,
                "longitude": lon,
                "timezone": timezone_str,
            }
        )

        print(f"\n✓ Location set to: {name}, {country}")
        print(f"  Latitude: {lat:.4f}°")
        print(f"  Longitude: {lon:.4f}°")
        print(f"  Timezone: {timezone_str}")
        print(f"  🌅 Sunrise: {s['sunrise'].strftime('%I:%M %p')}")
        print(f"  🌇 Sunset:  {s['sunset'].strftime('%I:%M %p')}")

        _ = input("\nPress Enter to return to main menu...")
        break
