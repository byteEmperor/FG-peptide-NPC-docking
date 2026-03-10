"""
metadata_manager.py
___________________
Scans a sample output directory, generates a metadata CSV, and checks version history.
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

def generate_csv(output_dir: Path, csv_file: Path):
    """
    Scan output_dir for samples, create a CSV with:
    sample_name, processed_path, needs_reprocessing (True/False)
    :param output_dir:
    :param csv_file:
    :return:
    """
    samples = sorted([d for d in output_dir.iterdir() if d.is_dir()])
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_name", "processed_path", "needs_reprocessing"])
        for sample in samples:
            needs_reprocess = check_version(sample)
            writer.writerow([sample.name, str(sample), needs_reprocess])

    print(f"[INFO] Metadata CSV generated at: {csv_file}")

    # Update metadata for processed samples (optional)
    for sample in samples:
        if needs_reprocess := check_version(sample):
            write_metadata(sample)

def main():
    parser = argparse.ArgumentParser(description="Manage processed sample metadata with version control.")
    parser.add_argument("--output_dir", type=Path, required=True,
                        help="Directory containing processed sample folders")
    parser.add_argument("--csv_file", type=Path, required=True,
                        help="Path to output CSV metadata file")
    args = parser.parse_args()

    generate_csv(args.output_dir, args.csv_file)

if __name__ == "__main__":
    main()
