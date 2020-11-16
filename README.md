# Zettelkasten Tools

These are various scripts that complement a zettelkasten stored locally in markdown files. To use these scripts, you can copy the folder containing this file into your zettelkasten folder and, with python installed, run your script of choice through a command line interface or IDE.

## check_media.py
Searches the zettelkasten folder for unused media files such as pngs, jpgs, pdfs, etc. that are not linked to in any of the zettels. The script displays their names and assists you in choosing what to do with them.

## tag_stats.py
Gathers and displays statistics about the tags throughout the zettelkasten, including:
* A graph of the tags and their adjacency.
* Average tags per zettel.
* Total unique tags.
* Total tags.

## find_and_replace.py
Searches for a string (or regex pattern!) of your choice throughout all zettels, and helps you choose whether you want to replace some or all of them with another string or pattern.
