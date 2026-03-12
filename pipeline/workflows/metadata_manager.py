"""
metadata_manager.py
___________________

logic aim:
processed folder missing -> needs processing
metadata version outdated -> needs reprocessing
metadata version current -> skip

Scans a sample output directory against the provided raw samples, generates a metadata CSV, and checks version history.
If the stored version is older than the current script version, the sample is marked for reprocessing.
"""

import argparse
import csv
from pathlib import Path
import json

# ----------------------------- CONFIG -----------------------------
CURRENT_VERSION = 1 # will be incremented the processing logic changes

def check_version(sample_dir: Path) -> bool:
    """
    Returns True if the sample needs reprocessing:
    - no metadata.json exists
    - version in metadata.json is older than CURRENT_VERSION
    :param sample_dir:
    :return:
    """

    metadata_file = sample_dir / "metadata.json"
    if not metadata_file.exists():
        return True
    try:
        with open(metadata_file) as f:
            data = json.load(f)
        if data.get("version", 0) < CURRENT_VERSION:
            return True
    except Exception:
        return True
    return False

def write_metadata(sample_dir: Path):
    metadata_file = sample_dir / "metadata.json"
    metadata = {"version": CURRENT_VERSION}
    with open(metadata_file, "w") as f:
        json.dump(metadata, f)

def generate_csv(input_dir: Path, output_dir: Path, csv_file: Path):
    """
    Scan raw samples and processed samples to determine what needs processing.
    """

    raw_samples = sorted([d for d in input_dir.iterdir() if d.is_dir()])

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_name", "processed_path", "needs_reprocessing"])

        for sample in raw_samples:

            processed_dir = output_dir / sample.name

            if not processed_dir.exists():
                needs_reprocess = True
            else:
                needs_reprocess = check_version(processed_dir)

            writer.writerow([sample.name, str(processed_dir), needs_reprocess])

    print(f"[INFO] Metadata CSV generated at: {csv_file}")

def main():
    parser = argparse.ArgumentParser(description="Manage processed sample metadata with version control.")
    parser.add_argument("--input_dir", type=Path, required=True,
                        help="Path to the directory with samples to process")
    parser.add_argument("--output_dir", type=Path, required=True,
                        help="Directory containing processed sample folders")
    parser.add_argument("--csv_file", type=Path, required=True,
                        help="Path to output CSV metadata file")
    args = parser.parse_args()

    generate_csv(args.input_dir, args.output_dir, args.csv_file)

if __name__ == "__main__":
    main()
