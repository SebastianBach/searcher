"""
Loads images from the specified source, calculates the dhash values,
saves a preview image and stores the information in the database.
"""


import hashlib
import os

import searcher.database as database
import searcher.project as project
from searcher import image


def load_image(img_url: str, info: str, path: str, db: database.Database) -> None:
    """Loads the given image, creates the preview image, and stores information the database.

    Args:
        img_url (str): The image URL.
        info (str): The image source location.
        path (str): The project path.
        db (database.Database): The project database.
    """

    print(img_url)

    url_hash = hashlib.md5(img_url.encode('utf-8')).hexdigest()

    img_file = os.path.join(path, "preview", url_hash[:2], url_hash + ".jpg")

    if os.path.exists(img_file):

        dhash = db.get_dhash(url_hash)

        if dhash is None:
            dhash = str(image.Image(img_file).dhash())

        db.add(dhash, url_hash, info)
        return

    try:
        img = image.Image(img_url)

        if img.is_big():

            img.store_preview(img_file, 100)

            db.add(str(img.dhash()), url_hash, info)

    except Exception as e:
        print("error handling image {} {}".format(img_url, e))


def analyze(path: str) -> None:
    """Analyzes the images defended in the given project.

    Args:
        path (str): The project path.
    """

    todo_files = project.Project(path).get_todo_files()

    if not len(todo_files):
        print("nothing to do")
        return

    # ensure preview sub-folders

    folders = [hex(i).split('x')[-1].zfill(2) for i in range(256)]

    for folder in folders:
        full_folder = os.path.join(path, "preview", folder)
        if not os.path.exists(full_folder):
            os.makedirs(full_folder)

    db = database.Database(path)

    for todo_file in todo_files:

        with open(todo_file, 'r', encoding='UTF-8') as file:

            lines = []
            while (line := file.readline().rstrip()):
                if line:
                    lines.append(line)

            src = lines[0]
            lines.pop(0)

            db.remove(src)

            for line in lines:
                load_image(line, src, path, db)

            db.store()

        os.unlink(todo_file)


