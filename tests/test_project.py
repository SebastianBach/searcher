import sys
import os
import unittest
import utility


sys.path.insert(0, '..')
import searcher.project as project

class TestProject(unittest.TestCase):

    def test_utility(self):

        res = project.get_project_dir(["abc"])

        self.assertFalse(res)

        res = project.get_project_dir(["aaa", "bbb"])
        self.assertFalse(res)

        test_project = utility.get_test_project()

        res = project.get_project_dir(["abc", test_project])
        self.assertTrue(res)

    def test_base(self):
        test_project = utility.get_test_project()

        p = project.Project(test_project)

        res = p.check_img_url("www.test.com/images/image.jpg")
        self.assertTrue(res)

        res = p.check_img_url("www.example.com/images/image.jpg")
        self.assertFalse(res)

        res = p.make_todo_file("www.example.com")
        self.assertTrue(res)

        res = p.get_todo_files()
        self.assertTrue(res)
        self.assertEqual(len(res), 1)

        sources = p.get_sources()
        self.assertTrue(sources)
        self.assertTrue(os.path.exists(sources))

        cookies = p.get_cookies("www.test.com/a/b")
        self.assertFalse(cookies)

        cookies = p.get_cookies("www.example.com/a/b")
        self.assertTrue(cookies)
        self.assertTrue("aaa" in cookies)
