import sys
import os
import unittest
import utility

sys.path.insert(0, '..')

import searcher.image as image


class TestImage(unittest.TestCase):

    def test_big(self):

        img = image.Image("https://picsum.photos/id/234/200/300")

        self.assertEqual(str(img.dhash()), "f02020212138e9ca")

        self.assertTrue(img.is_big())

        small = img.scale_down(50)
        self.assertIsNotNone(small)
        width, _ = small.size
        self.assertEqual(width, 50)

        base64 = img.jpeg_base64(100)
        self.assertIsNotNone(base64)

        temp_folder = utility.get_clean_temp_folder()
        temp_file = os.path.join(temp_folder, "temp_image.jpg")

        img.store_preview(temp_file, 50)

        self.assertTrue(os.path.exists(temp_file))


    def test_small(self):
        small_image = utility.get_image_path("not_big.jpg")

        img = image.Image(small_image)

        self.assertEqual(str(img.dhash()), "0000000000000000")

        self.assertFalse(img.is_big())

        small = img.scale_down(40)
        self.assertIsNotNone(small)
        width, _ = small.size
        self.assertEqual(width, 40)

        base64 = img.jpeg_base64(100)
        self.assertIsNotNone(base64)
