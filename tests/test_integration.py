import sys
import unittest
import utility

sys.path.insert(0, '..')

import searcher.database as database
import searcher.image as image

class TestIntegration(unittest.TestCase):

    def test_base(self):

        folder = utility.get_clean_temp_folder()

        db = database.Database(folder)

        small_image = utility.get_image_path("not_big.jpg")
        big_image = utility.get_image_path("big.jpg")

        db.add(str(image.Image(small_image).dhash()), "1122334455", "www.example.com/image_a")
        db.add(str(image.Image(big_image).dhash()), "2233445566", "www.example.com/image_b")

        db.store()

        self.assertEqual(db.size(), 2)

        res = db.search(str(image.Image(big_image).dhash()))

        self.assertTrue(res)
        self.assertEqual(len(res), 1)

        self.assertEqual(res[0].preview, "2233445566")
        self.assertEqual(res[0].url, "www.example.com/image_b")
        self.assertEqual(res[0].distance, 0)


