#!/usr/bin/env python3
"""
Minimal install-stats relay for a VPS (stdlib only, no pip packages).

POST /install  {"modId": "MyMod", "version": "1.0.0"}
  -> GitHub repository_dispatch(mod_install) on MBM.ModsCatalog

GET /stats
  -> fresh stats.json from GitHub API (no raw CDN cache)

Environment:
  GITHUB_OWNER   e.g. Tzigan
  GITHUB_REPO    e.g. MBM.ModsCatalog
  GITHUB_TOKEN   fine-grained PAT (Contents + Actions on this repo)
  PORT           listen port (default 8787)
"""

from __future__ import annotations

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MOD_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
STATS_REF = os.environ.get("GITHUB_STATS_REF", "stats").strip() or "stats"
STATS_PATH = os.environ.get("GITHUB_STATS_PATH", "stats.json").strip() or "stats.json"


def clean_env(name: str) -> str:
    value = os.environ.get(name, "").strip().strip("\ufeff")
    if not value:
        raise KeyError(name)
    try:
        value.encode("ascii")
    except UnicodeEncodeError as ex:
        raise ValueError(
            f"{name} must be ASCII-only — remove Cyrillic, comments on the same line, "
            f"or invisible characters in /etc/mbm-stats-relay.env"
        ) from ex
    return value


def dispatch_install(mod_id: str, version: str) -> None:
    owner = clean_env("GITHUB_OWNER")
    repo = clean_env("GITHUB_REPO")
    token = clean_env("GITHUB_TOKEN")

    payload = json.dumps(
        {
            "event_type": "mod_install",
            "client_payload": {"modId": mod_id, "version": version},
        }
    ).encode("utf-8")

    request = Request(
        f"https://api.github.com/repos/{owner}/{repo}/dispatches",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "MBM-Stats-Relay-VPS",
            "X-GitHub-API-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )

    with urlopen(request, timeout=30) as response:
        if response.status not in (200, 204):
            raise RuntimeError(f"dispatch HTTP {response.status}")


def fetch_stats_json() -> bytes:
    owner = clean_env("GITHUB_OWNER")
    repo = clean_env("GITHUB_REPO")
    token = clean_env("GITHUB_TOKEN")

    request = Request(
        f"https://api.github.com/repos/{owner}/{repo}/contents/{STATS_PATH}?ref={STATS_REF}",
        method="GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.raw+json",
            "User-Agent": "MBM-Stats-Relay-VPS",
            "X-GitHub-API-Version": "2022-11-28",
        },
    )

    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"stats HTTP {response.status}")
        return response.read()


class RelayHandler(BaseHTTPRequestHandler):
    server_version = "MBM-Stats-Relay-VPS/1.1"

    def do_GET(self) -> None:
        if self.path not in ("/stats", "/stats.json"):
            self.send_error(404, "not found")
            return

        try:
            payload = fetch_stats_json()
        except (HTTPError, URLError, RuntimeError, KeyError, ValueError, UnicodeEncodeError) as ex:
            print(f"stats fetch failed: {ex}", file=sys.stderr)
            self.send_error(502, "stats fetch failed")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self) -> None:
        if self.path not in ("/install", "/"):
            self.send_error(404, "not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_error(400, "invalid Content-Length")
            return

        try:
            raw = self.rfile.read(length)
            body = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, "invalid json")
            return

        mod_id = body.get("modId", "").strip() if isinstance(body.get("modId"), str) else ""
        if not mod_id or len(mod_id) > 128 or not MOD_ID_RE.match(mod_id):
            self.send_error(400, "invalid modId")
            return

        version = ""
        if isinstance(body.get("version"), str):
            version = body.get("version", "").strip()[:64]

        try:
            dispatch_install(mod_id, version)
        except (HTTPError, URLError, RuntimeError, KeyError, ValueError, UnicodeEncodeError) as ex:
            print(f"dispatch failed: {ex}", file=sys.stderr)
            self.send_error(502, "dispatch failed")
            return

        self.send_response(204)
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    try:
        for key in ("GITHUB_OWNER", "GITHUB_REPO", "GITHUB_TOKEN"):
            clean_env(key)
    except (KeyError, ValueError) as ex:
        print(f"Invalid environment: {ex}", file=sys.stderr)
        sys.exit(1)

    port = int(os.environ.get("PORT", "8787"))
    server = ThreadingHTTPServer(("0.0.0.0", port), RelayHandler)
    print(f"Listening on 0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
