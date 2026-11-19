#!/usr/bin/env python3
"""The World Today - front page edition, 19 November 2026.

Reads the bundled front-page artwork, checks it is a real PNG
within the size budget, and publishes it to /output/entry.png.
"""
import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
LIMIT_BYTES = 1024 * 1024
HERE = Path(__file__).resolve().parent

FRONT_PAGE = [
    ("LEAD", "GTA VI launches worldwide after a 13-year wait"),
    ("SUMMIT", "Trump, Xi and Putin meet face to face at APEC Shenzhen"),
    ("BRUSSELS", "EU proposes a 45 billion euro loan for Ukraine"),
    ("DEEP SPACE", "Voyager 1 reaches one light-day from home"),
    ("AUCTION", "A Van Gogh canvas sells for a record $190.4 million"),
    ("MARKETS", "Fed minutes lean toward one more rate hike"),
    ("CAPITOL", "Jeffries nominated, a first Black Speaker in reach"),
    ("HEALTH", "Ebola in DR Congo passes 11,000 cases"),
]


def locate_artwork() -> Path:
    candidate = HERE / "entry.png"
    if not candidate.is_file():
        raise SystemExit(f"missing artwork: {candidate}")
    return candidate


def check_png(path: Path) -> int:
    size = path.stat().st_size
    if size > LIMIT_BYTES:
        raise SystemExit(f"entry.png too large: {size} bytes over 1 MiB")
    with path.open("rb") as handle:
        header = handle.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        raise SystemExit("entry.png does not start with a PNG signature")
    return size


def publish(source: Path) -> Path:
    target_dir = Path("/output")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(source, target)
    return target


def print_front_page(size: int) -> None:
    print("=" * 62)
    print("  THE WORLD TODAY - Thursday, 19 November 2026")
    print("=" * 62)
    for section, headline in FRONT_PAGE:
        print(f"  [{section:<10}] {headline}")
    print("-" * 62)
    print(f"  Front page image verified: {size} bytes, PNG OK")
    print("  Published to /output/entry.png")


def main() -> int:
    artwork = locate_artwork()
    size = check_png(artwork)
    publish(artwork)
    print_front_page(size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
