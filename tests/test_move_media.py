# Internal imports
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from src.move_media import *

# External imports
import unittest


class TestMoveMedia(unittest.TestCase):
    def test_get_all_asset_links(self):
        zettel_paths = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/20200319163500.md',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel for testing.md']
        result = get_all_asset_links(zettel_paths)
        expected_originals = ['1e9b3e85368662b9d33d2fcd700cc84f.png',
                              'file://C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\assets\\HowtoReadPaper.pdf']
        self.assertEqual(result.originals, expected_originals)

    def test_validate_chosen_paths(self):
        zettel_paths = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/20200319163500.md',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel for testing.md']
        all_asset_links = get_all_asset_links(zettel_paths)
        chosen_paths = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/1e9b3e85368662b9d33d2fcd700cc84f.png',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel for testing.md',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/nonexistent file.jpg']
        result, _ = validate_chosen_paths(chosen_paths, all_asset_links)
        expected = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/1e9b3e85368662b9d33d2fcd700cc84f.png',
                    'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf']
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
