"""
Web application to search image sources.
"""

import sys
sys.path.insert(0, '../..')

import io
import os

from flask import (Flask, escape, render_template, request, send_file,
                   send_from_directory)

import searcher.database
import searcher.image

project_folder = sys.argv[1]
db = searcher.database.Database(project_folder)

resource_folder = sys.argv[2]
web_folder = os.path.join(resource_folder, "web")
templates_folder = os.path.join(resource_folder, "templates")

app = Flask(__name__, template_folder=templates_folder)


@app.route('/')
def index():
    """Returns the front page."""
    return render_template('index.html')


@app.route('/style.css')
def style():
    """Returns the CSS file."""
    return send_from_directory(web_folder, 'style.css', mimetype='text/css')


@app.route('/info')
def info():
    """Returns database information."""
    size = db.size()
    return render_template('info.html', size=size)


def get_image_path(id: str) -> str:
    """Returns the full preview image path for the given image ID.

    Args:
        id (str): The image ID.

    Returns:
        str: The full preview image path.
    """
    url = os.path.join(project_folder, "preview")
    url = os.path.join(url, id[:2])
    return os.path.join(url, id+".jpg")


@app.route('/img/<name>.jpg')
def image(name):
    """Returns an image resource."""

    url = get_image_path(escape(name))

    with open(url, 'rb') as f:

        data = f.read()

        return send_file(
            io.BytesIO(data),
            mimetype='image/jpeg',
            as_attachment=False)


@app.route('/search', methods=['POST'])
def search_image():
    """Performs the image search and returns the search results."""

    reference_url = request.form['image-url']

    img = searcher.image.Image(reference_url)

    jpeg_base64 = img.jpeg_base64(100)

    res = db.search(str(img.dhash()), 10)

    if not res:
        return render_template('search_empty.html', base64=jpeg_base64)

    results = []
    for result in res:

        title = result.url
   
        # todo: do this in front end or store in database
        title = title[8:] if title.startswith("https://") else title
        title = title[4:] if title.startswith("www.") else title

        results.append({'preview': result.preview, 'src': result.url,
                       'distance': str(result.distance), 'title': title})

    return render_template('search.html', results=results, reference=reference_url, base64=jpeg_base64)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
