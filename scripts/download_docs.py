import requests
from pathlib import Path

SOURCES_FILE = "data/sources.txt"
DATA_DIR = "data"


def parse_sources(filepath: str) -> list[tuple[str, str, str]]:
    sources = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 3:
                print(f"  Skipping malformed line: {line}")
                continue
            filename, url, description = parts
            sources.append((filename, url, description))
    return sources


def download_documents():
    Path(DATA_DIR).mkdir(exist_ok=True)
    sources = parse_sources(SOURCES_FILE)

    if not sources:
        print("No sources found in sources.txt")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    for filename, url, description in sources:
        dest = Path(DATA_DIR) / filename

        if dest.exists():
            print(f"✓ Already exists: {filename}")
            continue

        print(f"\nDownloading: {filename}")
        print(f"  {description}")

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            if not response.content.startswith(b"%PDF"):
                print(f"  ✗ FAILED — Not a valid PDF (token may have expired)")
                continue

            dest.write_bytes(response.content)
            size_kb = dest.stat().st_size / 1024
            print(f"  ✓ Saved ({size_kb:.0f} KB)")

        except requests.RequestException as e:
            print(f"  ✗ FAILED — {e}")

    print("\n--- Corpus Summary ---")
    for f in sorted(Path(DATA_DIR).glob("*.pdf")):
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    download_documents()
