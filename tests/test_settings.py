# Internal imports
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from src.settings import *

# External imports
import unittest


class TestSettings(unittest.TestCase):
    def test_all_abs(self):
        folder_paths = ['C:/Users/chris/Documents/Programming/test Zettelkasten',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/assets']
        self.assertEqual(all_abs(folder_paths), True)
        folder_paths.append('zettelkasten tools/tests/docs')
        self.assertEqual(all_abs(folder_paths), False)


if __name__ == '__main__':
    unittest.main()
