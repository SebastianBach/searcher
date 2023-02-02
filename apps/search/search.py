"""
Command line tool to search image sources.
"""

import sys
sys.path.insert(0, '../..')

from searcher import database, image

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Invalid number of arguments.")
        exit()

    db = database.Database(sys.argv[1])
    reference_url = sys.argv[2]
    distance = int(sys.argv[3])


    print(f"Loading {reference_url}")

    results = db.search(str(image.Image(reference_url).dhash()), distance)

    if results:

        print("Results:")

        for result in results:
            print(f" - {result.url} ({result.distance})")
    else:
        print("No Results.")
