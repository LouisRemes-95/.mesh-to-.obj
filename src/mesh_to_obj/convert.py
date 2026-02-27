from pathlib import Path
import meshio

def convert(in_path, outp_path: Path) -> None:
    """ 
    Convert a meshio mesh file (used for .mesh) to .obj
    
    Inputs
    ------
    in_path:
        Input mesh path
    out_path:
        Output .obj path
    """

    mesh = meshio.read(in_path)

    meshio.write(outp_path, mesh, file_format="obj")