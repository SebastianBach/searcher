"""
Command line tool to create a new project at the given location.
"""

import os
import sys


def make_subdir(dir: str, subdir: str) -> None:
    os.makedirs(os.path.join(dir, subdir))


def make_project_file(dir: str, file: str) -> None:
    full_path = os.path.join(dir, file)
    with open(full_path, "w") as f:
        f.write("")


def make_file(dir: str, subdir: str, file: str) -> None:
    full_path = os.path.join(dir, subdir, file)
    with open(full_path, "w") as f:
        f.write("")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        exit()

    project_folder = sys.argv[1]

    if os.path.isdir(project_folder):
        print("Folder already exists.")
        exit()

    os.makedirs(project_folder)

    make_project_file(project_folder, "img_filter.txt")

    make_subdir(project_folder, "cookies")
    make_subdir(project_folder, "preview")
    make_subdir(project_folder, "to_parse")
    make_subdir(project_folder, "to_analyze")

    make_file(project_folder, "to_parse", "sources.txt")

    print("success")
