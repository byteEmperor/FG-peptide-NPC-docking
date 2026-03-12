# CURRENT_VERSION = 1

from target_split.extract_pocket import extract_pocket
from target_split.compute_surface import generate_surface
from target_split.mesh_processing import clean_mesh
from target_split.surface_features import compute_features
from target_split.save_surface import export_surface


def build_surface(protein, ligand, output):

    pocket = "pocket.pdb"

    extract_pocket(protein, ligand, pocket)

    vertices, faces, normals, names = generate_surface(pocket)

    mesh = clean_mesh(vertices, faces)

    normals, hphob, hbond, charges = compute_features(mesh, pocket, names)

    export_surface(output, mesh, normals, charges, hbond, hphob)