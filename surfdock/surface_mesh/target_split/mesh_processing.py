import pymesh
from surfdock.surface_mesh.prepare_target.fixmesh import fix_mesh


def clean_mesh(vertices, faces, resolution=1.0):

    mesh = pymesh.form_mesh(vertices, faces)
    mesh = fix_mesh(mesh, resolution)

    return mesh