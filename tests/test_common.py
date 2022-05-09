# Internal imports
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from src.common import *
from src.settings import Settings

# External imports
import unittest


class TestCommon(unittest.TestCase):
    def test_get_zettel_paths(self):
        # Change settings temporarily so the result will be predictable.
        settings = Settings(['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs'],
                            ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs', 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets'],
                            [''])
        result = get_zettel_paths(settings)
        expected = ['C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\10741984719874 zettel with ID and title in name.md',
                    'C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\20200319163500.md',
                    'C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\zettel for testing.md',
                    'C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\zettel with no ID.md',
                    'C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\zettel with no title.md']
        self.assertEqual(result, expected)

    def test_get_asset_paths(self):
        # Change settings temporarily so the result will be predictable.
        settings = Settings(['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs'],
                            ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs', 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/assets'],
                            [''])
        result = get_asset_paths(settings)
        expected = ['C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\1e9b3e85368662b9d33d2fcd700cc84f.png',
                    'C:\\Users\\chris\\Documents\\Programming\\test Zettelkasten\\zettelkasten tools\\tests\\docs\\assets\\HowtoReadPaper.pdf']
        self.assertEqual(result, expected)

    def test_get_zettel_title(self):
        zettel_path = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/10741984719874 zettel with ID and title in name.md'
        result = get_zettel_title(zettel_path)
        expected = 'and the first H1 is different'
        self.assertEqual(result, expected)

        zettel_path = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/20200319163500.md'
        result = get_zettel_title(zettel_path)
        expected = 'The Zettelkasten Method'
        self.assertEqual(result, expected)

        zettel_path = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel for testing.md'
        result = get_zettel_title(zettel_path)
        expected = 'Sample title'
        self.assertEqual(result, expected)

        zettel_path = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel with no ID.md'
        result = get_zettel_title(zettel_path)
        expected = 'This zettel has no ID!'
        self.assertEqual(result, expected)

        zettel_path = 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel with no title.md'
        result = get_zettel_title(zettel_path)
        expected = ''
        self.assertEqual(result, expected)

    def test_get_zettel_titles(self):
        zettel_paths = ['C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/10741984719874 zettel with ID and title in name.md',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/20200319163500.md',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel for testing.md',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel with no ID.md',
                        'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel with no title.md']
        result = get_zettel_titles(zettel_paths)
        expected = ['and the first H1 is different',
                    'The Zettelkasten Method',
                    'Sample title',
                    'This zettel has no ID!']
        self.assertEqual(result, expected)

    def test_html_link_is_URL(self):
        string = 'wikipedia.org/wiki/file.html'
        result = html_link_is_URL(string)
        self.assertEqual(result, True)

        string = 'wikipedia.org/wiki/file.htm'
        result = html_link_is_URL(string)
        self.assertEqual(result, True)

        string = 'wikipediaorg/wiki/file.html'
        result = html_link_is_URL(string)
        self.assertEqual(result, False)

        string = 'wikipediaorg/wiki/file.htm'
        result = html_link_is_URL(string)
        self.assertEqual(result, False)

        string = 'folder/subfolder/file.with_period.html'
        result = html_link_is_URL(string)
        self.assertEqual(result, False)

    def test_get_asset_links(self):
        result = get_asset_links('', '')
        self.assertIsInstance(result, Links)
        self.assertEqual(result.isEmpty(), True)

        string = '''
            # Should not match:
            [](c:\\Users\\chris\\Documents\\folder)
            [20200319163500.md](..\\tests\\docs\\20200319163500.md)
            [](zotero://open-pdf/library/items/3PMYG2V7?page=7)
            [abcdef@csun.edu](mailto:abcdef@csun.edu)
            [wikipedia](wikipedia.org)
            [](wikipedia.org/)
            [](wikipedia.org/wiki)
            [](www.wikipedia.org/wiki)
            [](www2.wikipedia.org/wiki)
            [](http://www.wikipedia.org)
            [](https://www.wikipedia.org)
            [](https://www.wikipedia.org/)
            [](https://wikipedia.org/)
            [](www.wikipedia.org/wiki/file.html)
            [](www.wikipedia.org/wiki/file.htm)
            [](wikipedia.org/wiki/file.html)

            # Should match:
            [](..\\..\\..\\assets\\comm-rota.pdf)
            ![](1e9b3e85368662b9d33d2fcd700cc84f.png)
            [](file://C:\\Users\\chris\\Documents\\Essay.pdf)
            [](C:/Users/chris/Documents/Essay.html)
            [](C:\\Users\\chris\\Documents\\Advice.jpeg)
            [account info](..\\Other\\account info.jpg)
            ![C:\\Users\\chris\\Documents\\Zettelkasten\\assets\\Screenshot_2020-05-27 2.png](C:\\Users\\chris\\Documents\\Zettelkasten\\assets\\Screenshot_2020-05-27 2.png)
            ![4d628bdda08ec00570422b0d030fd918.mp4](4d628bdda08ec00570422b0d030fd918.mp4)
        '''
        result = get_asset_links(string, 'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/20200319163500.md')
        expected_formatted = ['C:/Users/chris/Documents/Programming/test Zettelkasten/assets/comm-rota.pdf',
                              'C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/1e9b3e85368662b9d33d2fcd700cc84f.png',
                              'C:/Users/chris/Documents/Essay.pdf',
                              'C:/Users/chris/Documents/Essay.html',
                              'C:/Users/chris/Documents/Advice.jpeg',
                              '../Other/account info.jpg',
                              'C:/Users/chris/Documents/Zettelkasten/assets/Screenshot_2020-05-27 2.png',
                              '4d628bdda08ec00570422b0d030fd918.mp4']
        expected_broken = ['file://C:\\Users\\chris\\Documents\\Essay.pdf',
                           'C:/Users/chris/Documents/Essay.html',
                           'C:\\Users\\chris\\Documents\\Advice.jpeg',
                           '..\\Other\\account info.jpg',
                           'C:\\Users\\chris\\Documents\\Zettelkasten\\assets\\Screenshot_2020-05-27 2.png',
                           '4d628bdda08ec00570422b0d030fd918.mp4']
        self.assertEqual(result.formatted, expected_formatted)
        self.assertEqual(result.broken, expected_broken)

    def test_generate_zettel_id(self):
        result = generate_zettel_id()
        self.assertEqual(result.isnumeric(), True)
        self.assertEqual(len(result), 14)

    def test_find_zettel_id(self):
        result = find_zettel_id('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/20200319163500.md')
        self.assertEqual(result, '20200319163500')

        result = find_zettel_id('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel for testing.md')
        self.assertEqual(result, '79837489739283')

        result = find_zettel_id('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel with no ID.md')
        self.assertEqual(result, 'zettel with no ID')

        result = find_zettel_id('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/10741984719874 zettel with ID and title in name.md')
        self.assertEqual(result, '10741984719874')

    def test_get_zettel_link(self):
        result = get_zettel_link('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/20200319163500.md')
        self.assertEqual(result, '[[20200319163500]] The Zettelkasten Method')

        result = get_zettel_link('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel for testing.md')
        self.assertEqual(result, '[[79837489739283]] Sample title')

        result = get_zettel_link('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel with no ID.md')
        self.assertEqual(result, '[[zettel with no ID]] This zettel has no ID!')

        result = get_zettel_link('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/zettel with no title.md')
        self.assertEqual(result, '[[zettel with no title]] ')

        result = get_zettel_link('C:/Users/chris/Documents/Programming/test Zettelkasten/zettelkasten tools/tests/docs/10741984719874 zettel with ID and title in name.md')
        self.assertEqual(result, '[[10741984719874]] and the first H1 is different')


if __name__ == '__main__':
    unittest.main()
