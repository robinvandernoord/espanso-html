import json
import sys
import typing
from pathlib import Path
from urllib import request

# SOURCE = "https://raw.githubusercontent.com/w3c/html/master/entities.json"
SOURCE = "https://html.spec.whatwg.org/entities.json"

def download_file(url: str):
    return request.urlopen(url)


def main(target: str = "html.yml"):
    target_path = Path(target)

    if target_path.exists():
        print(target_path, "already exists. Please remove it to continue")
        exit(1)

    entities = json.load(download_file(SOURCE))

    seen = set()
    with target_path.open("w") as f:
        print("# HTML entities", file=f)
        print("matches:", file=f)

        for trigger, data in entities.items():
            replace = data["characters"].replace("\\", "\\\\").replace('"', '\\"')
            if not replace:
                continue

            if not trigger.endswith(";"):
                trigger = f"{trigger};"

            if trigger in seen:
                # prevent duplicates
                continue

            seen.add(trigger)
            print(f'  - trigger: "{trigger}"', file=f)
            print(f'    replace: "{replace}"', file=f)


if __name__ == "__main__":
    main(*sys.argv[1:])
