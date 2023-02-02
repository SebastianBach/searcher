from bs4 import BeautifulSoup


class ImageJob:
    info: str = ""
    image: str = ""


parser_source_generators = []
parser_html_parser = []


def source_generator(func):
    parser_source_generators.append(func)
    return func


def run_source_generators(path: str):
    html_sources = []
    for generator in parser_source_generators:
        html_sources.extend(generator(path))
    return html_sources


def html_parser(func):
    parser_html_parser.append(func)
    return func


def run_html_parser(doc: BeautifulSoup, website: str, p):

    images = []

    for parser in parser_html_parser:
        images.extend(parser(doc, website, p))

    return images
