"""Erzeugt eine Pinterest-Bulk-Upload-CSV aus Bildern in images/ + content.json.

Ablauf:
1. Bilder in images/ ablegen und per git committen/pushen
   (git add images/ && git commit -m "..." && git push),
   damit sie unter einer oeffentlichen raw.githubusercontent.com-URL erreichbar
   sind -- Pinterest laedt die Bilder ueber genau diese URL.
2. content.json anlegen (siehe content.example.json): Titel/Beschreibung/
   Hashtags/Board/Link pro Dateiname.
3. python generate_bulk_csv.py ausfuehren -> erzeugt pinterest_bulk_upload.csv
4. CSV bei Pinterest hochladen: Einstellungen -> Inhalte importieren -> Hochladen
   (neben der CSV/TXT-Option), Datei auswaehlen.

Keine externen Abhaengigkeiten -- reine Python-Standardbibliothek.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from urllib.parse import quote

REPO_OWNER = "t3hr"
REPO_NAME = "pinterest_bulk_upload"
REPO_BRANCH = "main"

IMAGES_DIR = Path(__file__).parent / "images"
CONTENT_FILE = Path(__file__).parent / "content.json"
OUTPUT_CSV = Path(__file__).parent / "pinterest_bulk_upload.csv"

DEFAULT_BOARD = "synthetic stills"
DEFAULT_LINK = "https://www.instagram.com/tele__prompt_er/"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
CSV_FIELDS = ["Title", "Media URL", "Pinterest board", "Description", "Link", "Keywords"]


def _raw_url(image_path: Path) -> str:
    rel_path = f"images/{image_path.name}"
    return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{REPO_BRANCH}/{quote(rel_path)}"


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _unique_link(link: str, title: str) -> str:
    """Pinterests Bulk-Upload lehnt Zeilen mit identischem Link-Wert als
    Duplikat ab. Haengt einen pro Pin eindeutigen Tracking-Parameter an,
    damit derselbe Ziel-Link mehrfach verwendet werden kann."""
    if not link:
        return link
    separator = "&" if "?" in link else "?"
    return f"{link}{separator}utm_content={_slugify(title)}"


def main() -> None:
    if not CONTENT_FILE.exists():
        raise SystemExit(f"{CONTENT_FILE} nicht gefunden. Siehe content.example.json.")
    content_map = json.loads(CONTENT_FILE.read_text(encoding="utf-8"))

    images = sorted(p for p in IMAGES_DIR.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
    if not images:
        raise SystemExit(f"Keine Bilder in {IMAGES_DIR} gefunden.")

    rows = []
    missing = []
    for image_path in images:
        entry = content_map.get(image_path.name)
        if entry is None:
            missing.append(image_path.name)
            continue

        title = str(entry["title"]).strip()[:100]
        description = str(entry["description"]).strip()[:480]
        hashtags = [tag.strip() for tag in entry.get("hashtags", []) if tag.strip()]
        board = str(entry.get("board", DEFAULT_BOARD)).strip()
        link = _unique_link(str(entry.get("link", DEFAULT_LINK)).strip(), title)

        full_description = description
        if hashtags:
            full_description = f"{description}\n\n{' '.join(hashtags)}"[:500]

        keywords = ", ".join(tag.lstrip("#") for tag in hashtags)

        rows.append(
            {
                "Title": title,
                "Media URL": _raw_url(image_path),
                "Pinterest board": board,
                "Description": full_description,
                "Link": link,
                "Keywords": keywords,
            }
        )

    if missing:
        print("Warnung: kein Content-Eintrag fuer folgende Bilder, werden uebersprungen:")
        for name in missing:
            print(f"  - {name}")

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} Zeile(n) geschrieben nach {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
