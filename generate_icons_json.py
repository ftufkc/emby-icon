#!/usr/bin/env python3
"""
Generate a JSON manifest for image icons in a folder and **escape all forward slashes** ("/") in URL strings so the output matches the required format, e.g.:

{"url": "https:\/\/raw.githubusercontent.com\/ftufkc\/emby-icon\/main\/icon\/clip_image008.png"}

Usage:
    python generate_icons_json.py

Adjust the CONFIGURATION block as needed.
"""

import json
import os
from pathlib import Path

# ------------------------- CONFIGURATION -------------------------
FOLDER_PATH = Path("./icon")  # Folder containing image files
BASE_URL = "https://raw.githubusercontent.com/ftufkc/emby-icon/main/icon/"  # URL prefix
TOP_NAME = "ddueh"             # Top-level "name" field
DESCRIPTION = "emby-icon"      # Top-level "description" field
OUTPUT_FILE = Path("emby-icon.json")  # Output JSON file
ALLOWED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"
}
# -----------------------------------------------------------------

def build_manifest(folder: Path) -> dict:
    """Return a dict for all images inside *folder*."""
    icons = []
    for entry in sorted(folder.iterdir()):
        if entry.is_file() and entry.suffix.lower() in ALLOWED_EXTENSIONS:
            icon_name = entry.stem
            icon_url = f"{BASE_URL}{entry.name}"
            icons.append({"name": icon_name, "url": icon_url})
    return {
        "name": TOP_NAME,
        "description": DESCRIPTION,
        "icons": icons,
    }


def json_dumps_escaped(data: dict) -> str:
    """Dump *data* to JSON and escape all forward slashes so that "/" becomes "\/"."""
    # The JSON standard allows either form, but some consumers (like the requester) want escaped slashes.
    return json.dumps(data, ensure_ascii=False, indent=2).replace("/", r"\/")


def main() -> None:
    if not FOLDER_PATH.exists():
        raise SystemExit(f"Folder not found: {FOLDER_PATH}")

    manifest = build_manifest(FOLDER_PATH)
    json_str = json_dumps_escaped(manifest)

    OUTPUT_FILE.write_text(json_str, encoding="utf-8")
    print(f"✅ Wrote {len(manifest['icons'])} icons to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
