import argparse
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("--protein", required=True)
parser.add_argument("--ligand", required=True)
parser.add_argument("--surface", required=True)
parser.add_argument("--output_csv", required=True)

args = parser.parse_args()

data = {
    "protein_path": [args.protein],
    "ligand_path": [args.ligand],
    "protein_surface": [args.surface],
}

df = pd.DataFrame(data)

Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
df.to_csv(args.output_csv, index=False)

print(f"[INFO] Docking CSV written to {args.output_csv}")