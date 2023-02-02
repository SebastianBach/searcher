import os
import urllib
from typing import List
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

import searcher.project as project
import web_parser.parser_html_image
import web_parser.parser_module_sources
import web_parser.parser_modules as modules


def store_jobs(images: List[modules.ImageJob], todo_file) -> None:
    """Writes the given images to the given file.

    Args:
        images (List[modules.ImageJob]): List of images.
        todo_file: File to write to.
    """

    for img in images:
        todo_file.write(img.image)
        todo_file.write("\n")


def parse_source(website: str, p: project.Project) -> None:
    """Loads a website and searches for images.

    Args:
        website (str): The website URL.
        p (project.Project): The current project.
    """

    print(website)

    domain = urllib.parse.urlparse(website).netloc
    if "www." in domain:
        domain = domain[4:]

    cookies = p.get_cookies(domain)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(website, cookies=cookies, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    images = modules.run_html_parser(soup, website, p)

    print(len(images))

    if images:

        todo_file = p.make_todo_file(website)
        todo_file = open(todo_file, "w")
        todo_file.write(website)
        todo_file.write("\n")

        for image in images:
            todo_file.write(image.image)
            todo_file.write("\n")

        todo_file.close()


def load_from_folder(source:str, p:project.Project) -> None:
    """Lists all files in the given folder.

    Args:
        source (str): A folder.
        p (project.Project): The current project.
    """

    todo_file = p.make_todo_file(source)
    todo_file = open(todo_file, "a")

    todo_file.write(source)
    todo_file.write("\n")

    images = []

    for filename in os.listdir(source):
        full = os.path.join(source, filename)
        if os.path.isfile(full):

            job = modules.ImageJob()
            job.image = full
            job.info = ""

            images.append(job)

    store_jobs(images, todo_file)

    todo_file.close()


def parse_sources(path: str):
    """Searches for image files in the sources defined in the given project.

    Args:
        path (str): The project folder.
    """

    print("parse sources")

    p = project.Project(path)

    sources = modules.run_source_generators(path)

    for source in sources:

        s = urlparse(source).scheme

        if len(s) == 1:
            load_from_folder(source, p)
        else:
            parse_source(source, p)
