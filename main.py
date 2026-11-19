"""The World Today — front-page edition.

Entry for make.fun's news-image-20261119: sums up Thursday,
19 November 2026 in one image, laid out like a newspaper front
page. The picture is drawn ahead of time and stored beside this
program as entry.png; running the program publishes it to
/output/entry.png exactly as the contest harness expects.
"""

import shutil
import sys
from pathlib import Path

DAY = "Thursday, 19 November 2026"
MAX_BYTES = 1_048_576  # the contest caps the image at 1 MiB
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# The stories the front page carries, in the order they appear.
HEADLINES = [
    ("LEAD", "GTA VI is here: the 13-year wait ends with a global rollout"),
    ("POLITICS", "Trump, Xi and Putin shake hands in Shenzhen at APEC"),
    ("EUROPE", "EU proposes a 45 billion euro loan for Ukraine"),
    ("SPACE", "Voyager 1 reaches one light-day from Earth"),
    ("ARTS", "A Van Gogh sells for a record $190.4 million"),
    ("ALSO", "Cyclone Akvan nears India; Jeffries to lead the US House"),
    ("MARKETS", "Fed minutes point to further hikes; Anthropic eyes a huge debut"),
]


def source_image() -> Path:
    """The image file shipped inside this repository."""
    return Path(__file__).resolve().parent / "entry.png"


def check_image(path: Path) -> None:
    """Refuse to publish anything that is not a valid small PNG."""
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit(f"{path.name} is not a PNG file")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"{path.name} is {len(data)} bytes, over the 1 MiB cap")


def publish(target: Path) -> Path:
    """Copy the front page to the harness output location."""
    src = source_image()
    check_image(src)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, target)
    return target


def main() -> int:
    out = publish(Path("/output/entry.png"))
    print(f"The World Today — {DAY}")
    for tag, headline in HEADLINES:
        print(f"  [{tag}] {headline}")
    print(f"published {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
