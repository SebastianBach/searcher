import os
import sqlite3
from dataclasses import dataclass
from typing import List

import imagehash


@dataclass
class SearchResult:
    preview: str
    url: str
    distance: int


def calc_distance(a: str, b: str) -> int:
    """Custom SQLite function to calculate the hamming distance.

    Args:
        a (str): hex string representation of a dhash 
        b (str): hex string representation of a dhash 

    Returns:
        int: Hamming distance
    """
    dhash_a = imagehash.hex_to_hash(a)
    dhash_b = imagehash.hex_to_hash(b)
    return dhash_a - dhash_b


class Database:
    """
    SQLite based database which allows to search for images based in the dhash value.
    """

    def __init__(self, path: str) -> None:

        db_file = os.path.join(path, "database.sqlite")

        # might be unsafe in any real web-context, good enough for now
        self.con = sqlite3.connect(db_file, check_same_thread=False)

        self.cursor = self.con.cursor()

        self.con.create_function("hamming_distance", 2, calc_distance)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_data (
            dhash TEXT NOT NULL,
            preview TEXT NOT NULL,
            source TEXT NOT NULL)""")

        self.con.commit()

    def size(self) -> int:
        """Returns the number of entries in the database.

        Returns:
            int: Number of entries.
        """
        self.cursor.execute("SELECT COUNT(*) FROM image_data")
        return self.cursor.fetchone()[0]


    def add(self, dhash: str, preview: str, src: str) -> None:
        """Adds an entire to the database.

        Args:
            dhash (str): The image dhash value.
            preview (str): The preview image name.
            src (str): The image source.
        """
        self.cursor.execute("""
            INSERT INTO image_data (dhash, preview, source)
            VALUES (?, ?, ?)
            """, (dhash, preview, src))

    def remove(self, src: str) -> None:
        """Removes all entries for the given source.

        Args:
            src (str): The image source.
        """
        self.cursor.execute("""
            DELETE FROM image_data
            WHERE source = ?
            """, (src,))


    def get_dhash(self, preview:str) -> str:
        """Returns the dhash stored with the given preview image.

        Args:
            preview (str): The preview image.

        Returns:
            str: The associated dhash.
        """
        self.cursor.execute("SELECT dhash FROM image_data WHERE preview = ?", (preview,))
        res = self.cursor.fetchone()
        return res[0] if res else None

    def search(self, dhash:str, distance:int = 10) -> List[SearchResult]:
        """Searches the database for the given dhash value.

        Args:
            dhash (str): The reference dhash value.
            distance (int): Hamming distance threshold.

        Returns:
            List[SearchResult]: List of matches. No results returns an empty list.
        """

        self.cursor.execute("""
            SELECT *, hamming_distance(image_data.dhash, ?) AS distance FROM image_data
            WHERE hamming_distance(image_data.dhash, ?) < ?
            ORDER BY distance
            """, (dhash, dhash, distance))

        res = []

        for result in self.cursor.fetchall():
            res.append(SearchResult(result[1], result[2], result[3]))

        return res

    def store(self) -> None:
        """Stores the database.
        """
        self.con.commit()
