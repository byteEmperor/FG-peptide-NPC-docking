# CURRENT_VERSION = 1

import os
import subprocess
from openbabel import openbabel
import argparse


def run_reduce(input_pdb, tmp_pdb, output_pdb):
    """Run reduce to trim and add hydrogens."""

    with open(tmp_pdb, "w") as f:
        subprocess.run(
            ["reduce", "-Trim", input_pdb],
            stdout=f,
            check=True
        )

    with open(output_pdb, "w") as f:
        subprocess.run(
            ["reduce", "-HIS", tmp_pdb],
            stdout=f,
            check=True
        )

    os.remove(tmp_pdb)


def run_openbabel(input_pdb, output_pdb):
    """Run OpenBabel PDB -> PDB conversion."""

    mol = openbabel.OBMol()
    conv = openbabel.OBConversion()
    conv.SetInAndOutFormats("pdb", "pdb")

    mol.Clear()

    if not conv.ReadFile(mol, input_pdb):
        raise RuntimeError(f"OpenBabel failed to read {input_pdb}")

    conv.WriteFile(mol, output_pdb)


def process_protein(protein_path, outdir):
    if not os.path.exists(protein_path):
        raise FileNotFoundError(protein_path)

    os.makedirs(outdir, exist_ok=True)

    name = os.path.splitext(os.path.basename(protein_path))[0]

    step1 = os.path.join(outdir, f"{name}_obabel.pdb")
    step2_tmp = os.path.join(outdir, f"{name}_reduce_tmp.pdb")
    step2 = os.path.join(outdir, f"{name}_reduce.pdb")
    final = os.path.join(outdir, f"{name}_processed.pdb")

    # skip if already done
    if os.path.exists(final):
        print(f"[skip] {final} already exists")
        return final

    print(f"[openbabel] {protein_path}")
    run_openbabel(protein_path, step1)

    print("[reduce]")
    run_reduce(step1, step2_tmp, step2)

    print("[openbabel cleanup]")
    run_openbabel(step2, final)

    return final


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--protein",
        required=True,
        help="Input protein PDB"
    )

    parser.add_argument(
        "--outdir",
        required=True,
        help="Output directory"
    )

    args = parser.parse_args()

    output = process_protein(args.protein, args.outdir)

    print(f"[done] {output}")


if __name__ == "__main__":
    main()