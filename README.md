# Split Note

Split a plaintext file into multiple smaller files. This is great for the [Zettelkasten method of notetaking](https://blog.viktomas.com/posts/slip-box/), which works best when each note concisely covers one topic. The splits happen along markdown-style headers of a header level of your choice.

This program is not yet ready for use and also will have a few temporary limitations:
* All note files must have the file extension `.md`.
* Internal links to other notes must begin with `[[` and end with `]]`.

## Usage
1. Add the tag "#split" into each file you want to split.
2. Make sure the files are saved.
3. Run this program. It will let you choose the header level you want to split by and confirm which files to split.
