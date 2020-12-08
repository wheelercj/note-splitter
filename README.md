# Zettelkasten Tools

These are various scripts that complement a zettelkasten stored locally in markdown files, such as with [Zettlr](https://www.zettlr.com/). 
The types of media files currently supported are:
* .html
* .jpeg
* .jpg
* .m4a
* .mp4
* .pdf
* .png

## check_media.py
Searches the zettelkasten folder for broken media file links and unlinked media files. Their names are displayed and the program assists you in choosing what to do with them. Also, any linked media files in a selected downloads folder will automatically be moved to the default zettelkasten assets folder (and their links in the zettelkasten will be updated).

## move_media.py
Moves media files from one folder to another, and automatically updates their links within the zettelkasten.

## find_and_replace.py
Replaces a python regex pattern with a string throughout the entire zettelkasten, with some safeguards but no undo option.

## convert_links.py
Converts zettel links from the zettelkasten style to markdown's style, or vice versa. Currently, this only works with links that are 14-digit zettel IDs, and with double square brackets for the zettelkasten-style links, e.g. [[20201221140928]].

## settings.py
Settings for the locations of the zettelkasten, its assets, and any downloads folders to automatically move assets from. Any linked assets in a downloads folder are automatically moved to whichever assets folder was chosen first. Choosing a downloads folder is optional. Running this program directly will let you overwrite any settings you had already chosen.
