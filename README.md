# Zettelkasten Tools

These are various scripts that complement a zettelkasten stored locally in markdown files, such as [Zettlr](https://www.zettlr.com/). To use these scripts, you can copy the folder containing this file into your zettelkasten folder and, with python installed, run your script of choice through a command line interface or IDE.

## tag_stats.py
Gathers and displays statistics about the tags throughout the zettelkasten, including:
* A graph of the tags and their adjacency.
* Average tags per zettel.
* Total unique tags.
* Total tags.

## check_media.py
Searches the zettelkasten folder for unused media files such as pngs, jpgs, pdfs, htmls, etc. that are not linked to in any of the zettels. The script displays their names and assists you in choosing what to do with them.

## find_and_replace.py
Replaces a python regex pattern with a string throughout the entire zettelkasten, with safeguards but no undo option.

## convert_links.py
Converts zettel links from zettelkasten to markdown style, or vice versa.

## new_zettel.py
Creates a new zettel with a title of your choice and a YAML frontmatter block containing that title.

## common.py
Imported by some of the other files here.
