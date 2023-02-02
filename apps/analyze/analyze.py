"""
Command line tool to analyze the image files found by the parser tool.
"""

import sys

sys.path.insert(0, '../..')

from searcher import analyzer, project

if __name__ == "__main__":

    path = project.get_project_dir(sys.argv)

    if not path:
        print("Invalid argument.")
        exit()

    analyzer.analyze(path)
