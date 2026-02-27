from pathlib import Path
import meshio
import numpy as np

def convert(in_path, out_path: Path, data_label: str = None) -> None:
    """ 
    Convert a meshio mesh file (used for .mesh) to .ply
    Intended for a tetrahedral mesh with cell data
    
    Inputs
    ------
    in_path:
        Input mesh path
    out_path:
        Output .ply path
    """

    mesh = meshio.read(in_path)

    faces = mesh.cells_dict['tetra'][:, [[0,1,2],[0,3,1],[1,3,2],[0,2,3]]].reshape(-1,3)

    _, inverse, counts = np.unique(np.sort(faces), axis = 0, return_inverse = True, return_counts = True)
    is_boundary_face = counts[inverse] == 1
    boundary_faces = faces[is_boundary_face, :]

    points = np.unique(boundary_faces.flatten())

    lut = np.full(points.max()+1, 0, dtype=smallest_uint_type(points.size))
    lut[points] = np.arange(points.size)

    key = next(iter(mesh.cell_data), None)
    if key is not None:
        data_label = key if data_label is None else data_label

        data = np.tile(mesh.cell_data_dict[data_label]['tetra'][:,None], (1, 4))

    surface_mesh = meshio.Mesh(
        points = mesh.points[points, :],
        cells=[("triangle", lut[boundary_faces])]
        )

    meshio.write(out_path, surface_mesh, file_format="ply")

def smallest_uint_type(x: int):
    if x < 0:
        raise ValueError("Unsigned integers cannot store negative values.")

    if x <= np.iinfo(np.uint8).max:
        return np.uint8
    elif x <= np.iinfo(np.uint16).max:
        return np.uint16
    elif x <= np.iinfo(np.uint32).max:
        return np.uint32
    elif x <= np.iinfo(np.uint64).max:
        return np.uint64
    else:
        raise ValueError("Integer too large for uint64.")