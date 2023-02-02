"""
Command line tool to search image files in folders and websites.
"""

import sys

sys.path.insert(0, '../..')

from web_parser import parser
from searcher import project


if __name__ == "__main__":

    path = project.get_project_dir(sys.argv)

    if not path:
        print("Invalid argument.")
        exit()

    parser.parse_sources(path)
