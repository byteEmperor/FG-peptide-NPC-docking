# CURRENT_VERSION = 1

# compute_target_mesh.py
import argparse
from target_split.extract_pocket import extract_pocket
from target_split.compute_surface import generate_surface
from target_split.mesh_processing import clean_mesh
from target_split.surface_features import compute_features
from target_split.save_surface import export_surface

def build_surface(protein, ligand, output, full_protein=False):
    pocket = "pocket.pdb"

    # pass None if full protein, otherwise use default threshold
    threshold = None if full_protein else 8
    extract_pocket(protein, ligand, pocket, dist_threshold=threshold)

    vertices, faces, normals, names = generate_surface(pocket)
    mesh = clean_mesh(vertices, faces)
    normals, hphob, hbond, charges = compute_features(mesh, pocket, names)
    export_surface(output, mesh, normals, charges, hbond, hphob)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protein", required=True)
    parser.add_argument("--ligand", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--full_protein",
        action="store_true",
        help="Generate mesh for the entire protein instead of ligand pocket"
    )

    args = parser.parse_args()
    build_surface(
        protein=args.protein,
        ligand=args.ligand,
        output=args.output,
        full_protein=args.full_protein
    )