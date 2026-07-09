#!/usr/bin/env python3
"""Increment install counter for a mod in stats.json."""

import json
import sys

STATS_PATH = "stats.json"


def fail(message: str) -> None:
    print(f"::error::{message}")
    sys.exit(1)


def main() -> None:
    mod_id = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if not mod_id:
        fail("modId is required")

    try:
        with open(STATS_PATH, encoding="utf-8-sig") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"version": 1, "mods": {}}
    except (OSError, json.JSONDecodeError) as ex:
        fail(f"stats.json is not valid JSON: {ex}")

    if data.get("version") != 1:
        data["version"] = 1

    mods = data.setdefault("mods", {})
    if not isinstance(mods, dict):
        fail('stats.json "mods" must be an object')

    current = mods.get(mod_id, 0)
    if not isinstance(current, (int, float)) or current < 0:
        current = 0

    mods[mod_id] = int(current) + 1

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"OK: {mod_id} -> {mods[mod_id]}")


if __name__ == "__main__":
    main()
