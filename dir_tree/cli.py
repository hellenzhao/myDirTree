"""
This module provides the Dir Tree CLI.
"""
# cli.py

import argparse
import pathlib
import sys

from . import __version__
from .dir_tree import DirectoryTree

def main():
    args = parse_cmd_line_arguments()

    root = pathlib.Path(args.root_dir)
    if not root.is_dir():
        raise SystemExit(f"The specified root directory, '{root}', does not exist.")

    # validate input for tree height
    try:
        height = int(args.height)
    except ValueError:
        raise SystemExit(f"Error: {args.height} is not a non-negative integer.")
    if height < 0:
        raise SystemExit("Error: {height}} is not a valid height. Please enter a non-negative integer.")

    # create tree
    tree = DirectoryTree(root, dir_only=args.dir_only, output_file=args.output_file,
                          show_hidden=args.a, height=height)
    tree.generate()




def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="tree",
        description="Dir Tree, a directory tree generator",
        epilog="Thank you for using Dir Tree." # displays after user runs help option
    )
    
    parser.version = f"Dir Tree v{__version__}"
    parser.add_argument("-v", "--version", action="version")

    parser.add_argument(
        "root_dir", metavar="ROOT_DIR", # name of argument in usage messages
        nargs="?", # can only take one directory path
        default=".", # if user doesn't provide directory, use current directory
        help="Generate a full directory tree starting at ROOT_DIR",
    )

    parser.add_argument(
        "-d", "--dir-only", action="store_true", help="Generate a directory-only tree"
    )

    parser.add_argument(
        "-o", "--output-file", metavar="OUTPUT_FILE", nargs="?", default=sys.stdout, 
        help="Generate a full directory tree and save it to a file"
    )

    parser.add_argument(
        "-a", "-A", action="store_true", help="Show hidden files and folders in directory tree"
    )

    parser.add_argument(
        "--height", action="store", default=5, help="specifies the height of the tree"
    )

    return parser.parse_args() # returns Namespace object w/ all supplied arguments
