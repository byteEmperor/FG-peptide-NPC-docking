from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

# Paths
protein_path = "/home/nat/Documents/bachelor_project/docker_pipeline/data/processed/proteins/ntf2_processed.pdb"
ligand_path  = "/home/nat/Documents/bachelor_project/docker_pipeline/data/raw/ligands/01_GPG.sdf"
moved_ligand_path = "/home/nat/Documents/bachelor_project/docker_pipeline/data/raw/ligands/01_GPG_moved.sdf"

# --- Load protein coordinates ---
def get_protein_centroid(pdb_file):
    coords = []
    with open(pdb_file) as f:
        for line in f:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append([x, y, z])
    coords = np.array(coords)
    centroid = coords.mean(axis=0)
    return centroid

protein_centroid = get_protein_centroid(protein_path)
print("Protein centroid:", protein_centroid)

# --- Load ligand ---
lig = Chem.SDMolSupplier(ligand_path, removeHs=False)[0]
if lig is None:
    raise ValueError("Could not load ligand!")

# Generate 3D coordinates if missing
if lig.GetNumConformers() == 0:
    AllChem.EmbedMolecule(lig)

# --- Compute ligand centroid ---
conf = lig.GetConformer()
lig_coords = np.array([list(conf.GetAtomPosition(i)) for i in range(lig.GetNumAtoms())])
lig_centroid = lig_coords.mean(axis=0)

# --- Compute translation vector ---
translation = protein_centroid - lig_centroid + np.array([0, 0, 30])  # move slightly above protein
print("Translation vector:", translation)

# --- Move ligand ---
for i in range(lig.GetNumAtoms()):
    pos = conf.GetAtomPosition(i)
    new_pos = [pos.x + translation[0], pos.y + translation[1], pos.z + translation[2]]
    conf.SetAtomPosition(i, new_pos)

# --- Save moved ligand ---
w = Chem.SDWriter(moved_ligand_path)
w.write(lig)
w.close()

print(f"Moved ligand saved to: {moved_ligand_path}")