import web_parser.parser_modules
import os

@web_parser.parser_modules.source_generator
def read_sources_file(path:str):
    """Reads images sources from the project's "sources.txt" file.

    Args:
        path (str): The project folder.

    Returns:
        List of sources to parse.
    """

    sources = []

    source_file = os.path.join(path, "to_parse", "sources.txt")

    with open(source_file, 'r', encoding='UTF-8') as file:
        while (line := file.readline().rstrip()):
            if line:
                sources.append(line)

    return sources

