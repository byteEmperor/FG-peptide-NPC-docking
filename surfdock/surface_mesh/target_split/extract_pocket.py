import numpy as np
from Bio.PDB import PDBParser, NeighborSearch, Selection, PDBIO, Select
from rdkit import Chem


def get_ligand_coords(ligand_file):
    if ligand_file.endswith(".sdf"):
        mol = Chem.SDMolSupplier(ligand_file, sanitize=False)[0]
    elif ligand_file.endswith(".pdb"):
        mol = Chem.MolFromPDBFile(ligand_file, sanitize=False)
    else:
        raise ValueError("Unsupported ligand format")

    conf = mol.GetConformer()
    coords = np.array([list(conf.GetAtomPosition(i)) for i in range(mol.GetNumAtoms())])
    return coords


def extract_pocket(protein_pdb, ligand_file, output_pdb, dist_threshold=8):

    ligand_coords = get_ligand_coords(ligand_file)

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", protein_pdb)[0]

    atoms = Selection.unfold_entities(structure, "A")
    ns = NeighborSearch(atoms)

    close_res = []
    for c in ligand_coords:
        close_res.extend(ns.search(c, dist_threshold, level="R"))

    close_res = Selection.uniqueify(close_res)

    class PocketSelect(Select):
        def accept_residue(self, residue):
            return residue in close_res

    io = PDBIO()
    io.set_structure(structure)
    io.save(output_pdb, PocketSelect())

    print("Pocket saved:", output_pdb)