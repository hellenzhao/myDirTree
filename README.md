This was a simple study in building a command line application
that will help me visualize a desired directory's structure

To run:
* type the command python tree.py path_of_chosen_dir

Additional options:
- `-v`, `--version` shows application version and exits
- `-h`, `--help` shows a usage message
- `-d`, `--dir-only` generates a tree diagram with only directories
- `-o`, `--output-file` generates a tree diagram and saves it to a file in markdown format
- `-a`, `-A` shows hidden files and folders
- `--height` specifies the maximum allowed height of the tree (default 5), must be non-negative integer


Skills I learned
* create a CLI application with Python's argparse
* recursively traverse a directory structure using pathlib
* generate, format, and print a directory tree diagram
* save the directory tree diagram to an output file



Project inspired by Real Python's directory tree generator
