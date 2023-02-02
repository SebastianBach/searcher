import os
import sys
import unittest

import utility

sys.path.insert(0, '..')

import searcher.image as image
import searcher.database as database

class TestDatabase(unittest.TestCase):

    def test_base(self):

        temp_folder = utility.get_clean_temp_folder()

        db = database.Database(temp_folder)

        size = db.size()
        self.assertEqual(size, 0)

        db.add("1122334455667788", "aaaabbbb", "www.example2.com")
        db.add("0011223344556677", "aabbccdd", "www.example.com")

        db.store()

        size = db.size()
        self.assertEqual(size, 2)

        res = db.search("0011223344556677")
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 1)

        self.assertEqual(res[0].distance, 0)
        self.assertEqual(res[0].preview, "aabbccdd")
        self.assertEqual(res[0].url, "www.example.com")

        dhash = db.get_dhash("aabbccdd")
        self.assertEqual(dhash, "0011223344556677")

        db.remove("www.example.com")

        size = db.size()
        self.assertEqual(size, 1)

        res = db.search("0011223344556677")
        self.assertFalse(res)

        db.store()
