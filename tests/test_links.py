# Internal imports
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from src.links import *

# External imports
import unittest

zettel_path = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel for testing.md'


class TestLinks(unittest.TestCase):
    def test_append(self):
        links = Links()

        links.append('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf', 'HowtoReadPaper.pdf', zettel_path)
        links.append('assets\\HowtoReadPaper.pdf', 'HowtoReadPaper.pdf', zettel_path)
        links.append('..\\htmlcov\\index.html', 'index.html', zettel_path)
        links.append('..\\htmlcov\\nonexistent file.html', 'nonexistent file.html', zettel_path)

        expected_originals = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf',
                              'assets\\HowtoReadPaper.pdf',
                              '..\\htmlcov\\index.html',
                              '..\\htmlcov\\nonexistent file.html']
        expected_formatted = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf',
                              'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf',
                              'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/htmlcov/index.html',
                              '../htmlcov/nonexistent file.html']
        expected_names = ['HowtoReadPaper.pdf',
                          'HowtoReadPaper.pdf',
                          'index.html',
                          'nonexistent file.html']
        expected_broken = ['..\\htmlcov\\nonexistent file.html']

        self.assertEqual(links.originals, expected_originals)
        self.assertEqual(links.formatted, expected_formatted)
        self.assertEqual(links.names, expected_names)
        self.assertEqual(links.broken, expected_broken)

    def test_add(self):
        links = Links()
        links.append('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf', 'HowtoReadPaper.pdf', zettel_path)
        links.append('assets\\HowtoReadPaper.pdf', 'HowtoReadPaper.pdf', zettel_path)

        links2 = Links()
        links2.append('..\\htmlcov\\index.html', 'index.html', zettel_path)
        links2.append('..\\htmlcov\\nonexistent file.html', 'nonexistent file.html', zettel_path)
        links2.append('file://C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf', 'HowtoReadPaper.pdf', zettel_path)

        links.add(links2)

        expected_originals = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf',
                              'assets\\HowtoReadPaper.pdf',
                              '..\\htmlcov\\index.html',
                              '..\\htmlcov\\nonexistent file.html',
                              'file://C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf']
        expected_formatted = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf',
                              'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf',
                              'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/htmlcov/index.html',
                              '../htmlcov/nonexistent file.html',
                              'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf']
        expected_names = ['HowtoReadPaper.pdf',
                          'HowtoReadPaper.pdf',
                          'index.html',
                          'nonexistent file.html',
                          'HowtoReadPaper.pdf']
        expected_broken = ['..\\htmlcov\\nonexistent file.html']

        self.assertEqual(links.originals, expected_originals)
        self.assertEqual(links.formatted, expected_formatted)
        self.assertEqual(links.names, expected_names)
        self.assertEqual(links.broken, expected_broken)

    def test_isEmpty(self):
        links = Links()
        self.assertEqual(links.isEmpty(), True)
        links.append('..\\htmlcov\\index.html', 'index.html', zettel_path)
        self.assertEqual(links.isEmpty(), False)

    def test_get_abspath(self):
        asset_path = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf'
        result = get_abspath(asset_path, zettel_path)
        expected = 'C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\assets\\HowtoReadPaper.pdf'
        self.assertEqual(result, expected)

        asset_path = 'assets/HowtoReadPaper.pdf'
        result = get_abspath(asset_path, zettel_path)
        expected = 'C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\assets\\HowtoReadPaper.pdf'
        self.assertEqual(result, expected)

        asset_path = '..\\htmlcov\\index.html'
        result = get_abspath(asset_path, zettel_path)
        expected = 'C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\htmlcov\\index.html'
        self.assertEqual(result, expected)

        asset_path = '..\\htmlcov\\nonexistent file.html'
        result = get_abspath(asset_path, zettel_path)
        expected = '..\\htmlcov\\nonexistent file.html'
        self.assertEqual(result, expected)

    def test_format_link(self):
        asset_path = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf'
        result = format_link(asset_path, zettel_path)
        expected = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf'
        self.assertEqual(result, expected)

        asset_path = 'assets\\HowtoReadPaper.pdf'
        result = format_link(asset_path, zettel_path)
        expected = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf'
        self.assertEqual(result, expected)

        asset_path = '..\\htmlcov\\index.html'
        result = format_link(asset_path, zettel_path)
        expected = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/htmlcov/index.html'
        self.assertEqual(result, expected)

        asset_path = '..\\htmlcov\\nonexistent file.html'
        result = format_link(asset_path, zettel_path)
        expected = '../htmlcov/nonexistent file.html'
        self.assertEqual(result, expected)

        asset_path = 'file://..\\htmlcov\\nonexistent file.html'
        result = format_link(asset_path, zettel_path)
        expected = '../htmlcov/nonexistent file.html'
        self.assertEqual(result, expected)

        asset_path = 'file://C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf'
        result = format_link(asset_path, zettel_path)
        expected = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets/HowtoReadPaper.pdf'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
