"""Download and extract the full UCI Online Retail dataset."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path


DATA_URL = "https://archive.ics.uci.edu/static/public/352/online%2Bretail.zip"
EXPECTED_FILE = "Online Retail.xlsx"


def download_dataset(output_dir: Path, overwrite: bool = False) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / EXPECTED_FILE
    if destination.exists() and not overwrite:
        print(f"Dataset already exists: {destination}")
        return destination

    with tempfile.NamedTemporaryFile(suffix=".zip") as temporary:
        print(f"Downloading {DATA_URL}")
        with urllib.request.urlopen(DATA_URL) as response:
            shutil.copyfileobj(response, temporary)
        temporary.flush()
        with zipfile.ZipFile(temporary.name) as archive:
            matches = [name for name in archive.namelist() if name.endswith(EXPECTED_FILE)]
            if not matches:
                raise FileNotFoundError(f"{EXPECTED_FILE} was not found in the downloaded archive")
            with archive.open(matches[0]) as source, destination.open("wb") as target:
                shutil.copyfileobj(source, target)

    print(f"Saved dataset to {destination}")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    download_dataset(args.output_dir, args.overwrite)


if __name__ == "__main__":
    main()

