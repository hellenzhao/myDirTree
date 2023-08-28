"""
This module provides Dir Tree main module.
"""

import os
import pathlib
import sys


### connector characters and prefix strings
PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "



### creates directory tree diagram and displays it
class DirectoryTree:
    def __init__(self, root, dir_only=False, output_file=sys.stdout, show_hidden=False, height=5):
        self._output_file = output_file
        self._generator = _TreeGenerator(root, dir_only, show_hidden, height)
    

    def generate(self):
        tree = self._generator.build_tree()

        # if file is not set to output to stdout (user screen)
        if self._output_file != sys.stdout:
            # wrap file in markdown code block
            tree.insert(0, "```")
            tree.append("```")

            self._output_file = open(
                self._output_file, mode="w", encoding="UTF-8"
            )

        with self._output_file as f:
            for entry in tree:
                print(entry, file=f)




### traverses file system and generates directory tree diagram
class _TreeGenerator:
    def __init__(self, root, dir_only=False, show_hidden=False, height=5):
        self._root = pathlib.Path(root)
        self._dir_only = dir_only
        self._show_hidden = show_hidden
        self._height = height
        self._curr_height = 0
        self._tree = []
    
    def build_tree(self):
        self._tree_head()
        self._curr_height += 1
        self._tree_body(self._root)
        return self._tree
    
    def _tree_head(self):
        self._tree.append(f"{self._root}{os.sep}") # '/' for POSIX and '\\' for Windows
        self._tree.append(PIPE)

    def _tree_body(self, dir, prefix=""):
        """
        Generates and finds the directory tree body for a given directory

        Arguments:
        dir -- pathlib.Path object that holds the path to the directory we will walk through
        prefix -- string that will be used to draw the tree diagram (shows position of dir/file)
        """
        # find all files in dir, sorting folders first and files last
        entries = self._prepare_entries(dir)
        num_entries = len(entries)

        # keep track of current height to reset curr_height after each call of _tree_body
        temp_height = self._curr_height

        # for each directory/file, determine which connector to use and add it to tree
        for index, entry in enumerate(entries):
            # do not show hidden files and folders, unless instructed otherwise
            if not self._show_hidden:
                if entry.name[0] == ".":
                    continue

            connector = ELBOW if index == num_entries -1 else TEE

            # ensure that our entries are at a valid level of the tree
            if self._curr_height > self._height:
                break

            # add either directory or file to tree
            if entry.is_dir():
                self._curr_height += 1 # move down to next level of tree
                self._add_directory(entry, index, num_entries, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)
        
        # reset global curr_height (exit this directory, go to parent directory)
        self._curr_height = temp_height - 1



    def _prepare_entries(self, dir):
        entries = dir.iterdir()

        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
        else:
            entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

    
    def _add_directory(self, directory, index, num_entries, prefix, connector):
        # add directory to tree
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")

        # for directories, add an extra tab to prefix so that child dir/files are indented
        if index != num_entries - 1: # directory is not the last
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX # directory is last entry in parent folder

        # add child dir/files
        self._tree_body(dir=directory, prefix=prefix)

        # append new prefix to tree to separate current directory and next directory/file
        # if there is no next entry, prefix becomes the original inputed prefix
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")

        