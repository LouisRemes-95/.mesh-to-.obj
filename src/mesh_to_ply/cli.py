import argparse
from pathlib import Path

from mesh_to_ply.convert import convert

def main():
    parser = argparse.ArgumentParser(
        prog = ".mesh to .ply", 
        description = "Convert a .mesh (or other meshio-supported mesh) to .ply",
    )
    parser.add_argument(
        "input_path",
        type = Path,
        help = "Path to the input mesh file",
        )
    parser.add_argument(
        "-o",
        "--out",
        type = Path,
        default = None,
        help = "Path where the output needs to be saved (with file name and suffix)"
    )

    args = parser.parse_args()
    out_path = args.out if args.out else args.input_path.with_suffix(".ply")
    convert(args.input_path, out_path)
    print(f"Wrote: {out_path}")

if __name__ == "__main__":
    main()