import hashlib
import json
import os
from typing import Dict, List, Optional


def get_project_dir(args: List[str]) -> Optional[str]:
    """Checks if the first argument in the list of command line arguments is an existing directory (project path).

    Args:
        args (List[str]): List of command line arguments. Typically sys.argv.

    Returns:
        Optional[str]: The project path or None.
    """

    if len(args) != 2:
        return None

    path = args[1]

    if not os.path.isdir(path):
        return None

    return  path


class Project:
    """Represents a project folder."""

    def __init__(self, path: str) -> None:
        """Creates a new Project.

        Args:
            path (str): Full project folder path.
        """
        self.path = path

        self.img_filters = []
        img_filter_file = os.path.join(self.path, "img_filter.txt")
        with open(img_filter_file, 'r', encoding='UTF-8') as file:
            while (line := file.readline().rstrip()):
                if line:
                    self.img_filters.append(line)

        self.cookies = {}
        folder = os.path.join(self.path, "cookies")
        for filename in os.listdir(folder):
            full = os.path.join(folder, filename)
            if os.path.isfile(full):
                with open(full) as f_in:
                    domain, _ = os.path.splitext(filename)
                    self.cookies[domain] = json.load(f_in)

    def check_img_url(self, url: str) -> bool:
        """Checks if the given image URL should be further processed.

        Args:
            url (str): The image URL.

        Returns:
            bool: True if the URL should be processed.
        """
        return not any(f in url for f in self.img_filters)

    def get_sources(self) -> str:
        """Returns the path to the "sources.txt" file

        Returns:
            str: Path to the "sources.txt" file.
        """
        return os.path.join(self.path, "to_parse", "sources.txt")

    def make_todo_file(self, url: str) -> str:
        """Returns the name of the file storing the parsing results for the given URL.

        Args:
            url (str): The URL of the web-site or folder.

        Returns:
            str: The new file name.
        """
        todo = os.path.join(self.path, "to_analyze")
        md5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        return os.path.join(todo, f"{md5}.txt")

    def get_todo_files(self) -> List[str]:
        """Returns the files storing URLs of images to analyze.

        Returns:
            List[str]: List of files.
        """
        todo_files = []
        folder = os.path.join(self.path, "to_analyze")
        for filename in os.listdir(folder):
            full = os.path.join(folder, filename)
            if os.path.isfile(full):
                todo_files.append(full)

        return todo_files

    def get_cookies(self, website: str) -> Dict:
        """Returns the cookie dictionary for the given domain.

        Args:
            website (str): The domain e.g. "example.com"

        Returns:
            Dict: The dictionary. Empty is nothing found.
        """
        for key in self.cookies.keys():
            if key in website:
                return self.cookies[key]

        return {}
