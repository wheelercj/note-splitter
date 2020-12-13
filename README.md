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

## split_zettel.py
Splits one or more zettels each into multiple zettels. The split happens based on a header level of your choice, and the copied contents are replaced with links to the new zettels. Each new zettel has a backlink. Before running this program, put the '#split' tag in each zettel you want to split so the program knows which zettels to split. In the original zettel, any tags above the chosen header level to split by will be copied into each of the new zettels (except '#split'). The new zettels will be created in the same folder as their respective source zettel.

## check_media.py
This program searches a zettelkasten for unused assets, broken file links, and various anti-patterns.
* **Find unused media files**: unlinked media files are found and the program assists you in choosing what to do with them. The folder(s) searched for unused assets can be chosen in settings.
* **Find broken file links**: broken media file links in the zettelkasten are found and listed.
* **Organize downloads**: any linked assets in any downloads folders chosen in settings will be automatically moved to the first assets folder chosen in settings (and their links in the zettels will be updated).
* **Identify zettels**:
    * Zettels that are missing a 14-digit ID are found and listed. The program searches both the zettel name and contents for the ID.
    * Zettels that are missing a title (a header level 1) are found and listed.
    * Zettels with no tags are found and listed.

## move_media.py
Moves media files from one folder to another, and automatically updates their links within the zettelkasten.

## find_and_replace.py
Replaces a python regex pattern with a string throughout the entire zettelkasten, with some safeguards but no undo option.

## convert_links.py
Converts zettel links from the zettelkasten style to markdown's style, or vice versa. Currently, this only works with links that are 14-digit zettel IDs, and with double square brackets for the zettelkasten-style links, e.g. [[20201221140928]].

## settings.py
Settings for the locations of the zettelkasten, its assets, and any downloads folders to automatically move assets from. (When check_media.py runs, any linked assets in a downloads folder are automatically moved to whichever assets folder was chosen first.) Choosing a downloads folder is optional. Running this program directly will let you overwrite any settings you had already chosen.
