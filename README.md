# Zettelkasten Tools

These are various scripts that complement a zettelkasten stored locally in markdown files, such as with [Zettlr](https://www.zettlr.com/). To use these scripts, you can copy the folder containing this file into your zettelkasten folder and, with python installed, run your script of choice through a command line interface or IDE.

## check_media.py
Searches the zettelkasten folder for broken file links and unlinked media files such as pngs, jpgs, pdfs, htmls, etc. Their names are displayed and the program assists you in choosing what to do with them.

## tag_stats.py
(This program doesn't work yet, but will soon.)
Gathers and displays statistics about the tags throughout the zettelkasten, including:
* A graph of the tags and their adjacency.
* Average tags per zettel.
* Total unique tags.
* Total tags.

## find_and_replace.py
Replaces a python regex pattern with a string throughout the entire zettelkasten, with some safeguards but no undo option.

## convert_links.py
Converts zettel links from the zettelkasten style to markdown's style, or vice versa.
