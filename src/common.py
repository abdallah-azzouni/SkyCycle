import json
import os

data_file = "data.json"
template = {"location": None, "active_profile": None}


def load() -> dict[str, None]:
    if not os.path.exists(data_file) or os.stat(data_file).st_size == 0:
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=4)

    with open(data_file, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = template
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    return data


def write(data: dict[str, None]):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
