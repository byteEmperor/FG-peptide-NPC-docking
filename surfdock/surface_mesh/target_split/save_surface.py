from surfdock.surface_mesh.prepare_target.save_ply import save_ply


def export_surface(outfile, mesh, normals, charges, hbond, hphob):

    save_ply(
        outfile,
        mesh.vertices,
        mesh.faces,
        normals=normals,
        charges=charges,
        normalize_charges=True,
        hbond=hbond,
        hphob=hphob,
    )

    print("Surface saved:", outfile)