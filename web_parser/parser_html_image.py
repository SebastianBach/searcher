import requests
from bs4 import BeautifulSoup

import searcher.project
import web_parser.parser_modules


@web_parser.parser_modules.html_parser
def html_search_image_tags(doc: BeautifulSoup, website: str, p: searcher.project.Project):
    """Searches for images in the given HTML document.

    Args:
        doc (BeautifulSoup): The HTML document.
        website (str): The website URL.
        p (searcher.project.Project): The current project.

    Returns:
        The list of found images. An empty list if no images found.
    """

    images = []

    img_tags = doc.find_all("img")
    for tag in img_tags:

        src = tag.get("src") or tag.get("data-src")

        if src is None:
            continue

        src = requests.compat.urljoin(website, src)

        if p.check_img_url(src):

            job = web_parser.parser_modules.ImageJob()
            job.image = src
            job.info = ""

            images.append(job)

    return images
