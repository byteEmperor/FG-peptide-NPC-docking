import os
import torch
from rdkit import Chem
from surfdock.utils.utils import remove_all_hs
from surfdock.docking_inference.score_in_place_dataset.score_dataset import ScreenDataset

# --- Paths ---
protein_path = "/home/nat/Documents/bachelor_project/docker_pipeline/data/processed/proteins/ntf2_processed.pdb"
ligand_path  = "/home/nat/Documents/bachelor_project/docker_pipeline/data/raw/ligands/01_GPG.sdf"
pocket_path  = protein_path  # we are using full protein
surface_path = "/home/nat/Documents/bachelor_project/docker_pipeline/data/processed/meshes/ntf2_processed_01_GPG_20260313_163814/ntf2_processed_01_GPG_20260313_163814_surface.ply"
pocket_center = None

# Optional parameters (you can adjust these to test)
ligandsMaxAtoms = 80
remove_hs = True
receptor_radius = 10.0  # Å, typical default for SurfDock

# --- Load ligand ---
supplier = Chem.SDMolSupplier(ligand_path, removeHs=remove_hs)
ligands = [mol for mol in supplier if mol is not None]

if not ligands:
    print("ERROR: RDKit failed to read any molecules from SDF")
    exit(1)

for idx, lig in enumerate(ligands):
    n_atoms = lig.GetNumAtoms()
    print(f"Ligand {idx}: {n_atoms} atoms")
    if n_atoms > ligandsMaxAtoms:
        print(f" -> Rejected: more than ligandsMaxAtoms={ligandsMaxAtoms}")
        continue

    # --- Create a minimal ScreenDataset for one ligand ---
    try:
        dataset = ScreenDataset(
            pocket_path=pocket_path,
            ligand_path=ligand_path,
            ref_ligand=ligand_path,
            surface_path=surface_path,
            pocket_center=pocket_center,
            transform=None,
            receptor_radius=receptor_radius,
            ligandsMaxAtoms=ligandsMaxAtoms,
            require_ligand=False,
            remove_hs=remove_hs
        )
        n_samples = len(dataset)
        if n_samples == 0:
            print(" -> Rejected by ScreenDataset filters (too far, or no conformers generated)")
        else:
            print(f" -> Accepted! {n_samples} samples in dataset")
    except Exception as e:
        print(f" -> ERROR while creating dataset: {e}")