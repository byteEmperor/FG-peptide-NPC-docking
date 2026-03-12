from surfdock.surface_mesh.prepare_target.computeMSMS import computeMSMS


def generate_surface(pocket_pdb):

    vertices, faces, normals, names, areas = computeMSMS(
        pocket_pdb,
        protonate=True,
        one_cavity=None
    )

    return vertices, faces, normals, names