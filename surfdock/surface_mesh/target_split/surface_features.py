import numpy as np
from surfdock.surface_mesh.prepare_target.compute_normal import compute_normal
from surfdock.surface_mesh.prepare_target.computeHydrophobicity import computeHydrophobicity
from surfdock.surface_mesh.prepare_target.computeCharges import computeCharges
from surfdock.surface_mesh.prepare_target.computeAPBS import computeAPBS


def compute_features(mesh, pdb_file, names):

    vertices = mesh.vertices
    faces = mesh.faces

    normals = compute_normal(vertices, faces)

    hydrophobicity = computeHydrophobicity(names)
    hbond = computeCharges(pdb_file, vertices, names)

    charges = computeAPBS(vertices, pdb_file, "apbs_temp")

    return normals, hydrophobicity, hbond, charges