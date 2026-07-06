#!/usr/bin/env python3
"""CI checks for MBM.ModsCatalog pull requests."""

import json
import sys
import urllib.error
import urllib.request

MAX_MANIFEST_BYTES = 512 * 1024
USER_AGENT = "MBM.ModsCatalog-CI/1.0"


def fail(message: str) -> None:
    print(f"::error::{message}")
    sys.exit(1)


def warn(message: str) -> None:
    print(f"::warning::{message}")


def main() -> None:
    try:
        with open("catalog.json", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as ex:
        fail(f"catalog.json is not valid JSON: {ex}")

    if data.get("version") != 1:
        warn('catalog.json: expected "version": 1')

    manifests = data.get("manifests")
    if not isinstance(manifests, list) or len(manifests) == 0:
        fail('catalog.json must contain a non-empty "manifests" array')

    seen = set()
    for index, url in enumerate(manifests):
        if not isinstance(url, str) or not url.strip():
            fail(f"manifests[{index}] must be a non-empty string URL")

        url = url.strip()
        if not url.startswith("https://"):
            fail(f"manifests[{index}] must use https:// — got: {url}")

        key = url.lower()
        if key in seen:
            fail(f"duplicate manifest URL: {url}")
        seen.add(key)

        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read(MAX_MANIFEST_BYTES + 1)
                if len(body) > MAX_MANIFEST_BYTES:
                    fail(f"manifest too large (> {MAX_MANIFEST_BYTES} bytes): {url}")
                if response.status != 200:
                    fail(f"manifest URL returned HTTP {response.status}: {url}")
        except urllib.error.HTTPError as ex:
            fail(f"manifest URL HTTP {ex.code}: {url}")
        except urllib.error.URLError as ex:
            fail(f"cannot fetch manifest URL: {url} — {ex.reason}")

        try:
            manifest = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as ex:
            fail(f"author manifest is not valid JSON: {url} — {ex}")

        if not isinstance(manifest.get("mods"), list) or len(manifest["mods"]) == 0:
            fail(f'author manifest has no "mods" array: {url}')

        for mod_index, mod in enumerate(manifest["mods"]):
            if not isinstance(mod, dict):
                fail(f"mods[{mod_index}] must be an object in {url}")
            mod_id = mod.get("id")
            package = mod.get("package") or mod.get("dll")
            if not mod_id:
                fail(f"mods[{mod_index}] missing id in {url}")
            if not package:
                fail(f"mods[{mod_index}] missing package or dll in {url}")

    print(f"OK: {len(manifests)} manifest URL(s) validated")


if __name__ == "__main__":
    main()
