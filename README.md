# Note Splitter

Split markdown files into multiple smaller files.

## download

You can [download Note Splitter here (Windows only)](https://github.com/wheelercj/note-splitter/releases) or [install Note Splitter from source (all platforms)](https://github.com/wheelercj/note-splitter/blob/main/docs/dev-env.md).

## features

* Split by almost any markdown element.
* Split multiple files at the same time.
* Choose files to split by keyword or with a file browser.
* Optionally copy tags, frontmatter, footnotes, etc. into the new files.
* Source files will **NOT** be changed in any way, possibly except for when you move new files to a different folder (see the next point).
* Moving files to a different folder can automatically update markdown links to them in other files in your source folder. Also, any relative markdown file links in new files are made absolute.
* For each source file split, an index file can optionally be created that links to each of the new files, and the new files can optionally have backlinks to the index file (or to the source file if no index file is created).

![demo](docs/images/demo.png)

## split attributes and values

Choosing a split attribute and value is optional, and can be used to be more specific about what you want to split. For example, if you want to split by headers of all levels you should choose the `(none)` attribute, but if you want to split by headers of level 2 you should choose the `level` attribute and the value `2`.

Some split types have different attributes to choose from. For example, the `header` split type has `level` as one of its split attributes, which refers to the size of the header. However, some other split types such as `ordered list item` also have a `level` attribute that refers to the _indentation level_. Any split type's `content` attribute option lets you specify what exact text the element should contain. Some split types have other specialized attributes, such as `code block`'s `language` attribute, which allows you to choose the code block's language.

The "parse blocks" checkbox is mainly for elements of text that span multiple lines (blocks), but the option also changes the behavior when splitting by single-line elements. When parse blocks is chosen, each split section also ends where its containing block ends instead of only when the next element of the split type is found.

## file name formats

The file name format setting should not include a file extension and can use these variables:

`%uuid4` - A universally unique identifier
`%title` - The title of the file (the body of the first header, or of the first line if there is no header)
`%Y` - The current year (as a four-digit number)
`%M` - The current month (as a number)
`%D` - The current day
`%h` - The current hour
`%m` - The current minute
`%s` - The current second
`%id` - The same as entering `%Y%M%D%h%m%s`

You can use other characters with these variables. For example, to get file names like `2021-12-16 9.30`, you can set the file name format to `%Y-%M-%D %h.%m`.

If multiple files are made when the file name format has at least one of `%s`, `%m`, `%h`, and `%D`, the smallest of these time variables will be incremented once for each new file so that all the files have unique names. The first file starts with the current time.

All new file names are guaranteed to be unique. If the file name format somehow does not allow for unique file names, a period followed by a number will be appended to each new file name to make them unique.

## split types

| type name                | description                                                                      | child types                             |
|--------------------------|----------------------------------------------------------------------------------|------------------------------------------|
| block                    | any text element that spans multiple lines and contains other tokens                                      | blockquote block, code block, math block, table, text list                                   |
| blockquote               | a quote                                                                          | (none)                 |
| blockquote block         | multiple consecutive quotes                                                      | (none)                                    |
| can have inline elements | any line of text that can contain inline elements                                | blockquote, footnote, header, task, text, ordered list item, unordered list item                                     |
| code                     | a line of code                                                                   | (none)                                   |
| code block               | a block of code made of at least one line of code surrounded by code fences      | (none)                                    |
| code fence               | a delimiter that shows where a code block begins or ends                         | (none)                                    |
| empty line               | a line with nothing or only whitespace characters                                | (none)                                     |
| fence                    | any line of text that delimits others                                            | code fence, math fence                                     |
| fenced                   | any line of text that is delimited by fences                                     | code, math                                     |
| footnote                 | a footnote (commonly at the bottom of a file; not a footnote reference)          | (none)                 |
| header                   | a header, i.e. a title                                                           | (none)                 |
| horizontal rule          | a line that divides a document                                                   | (none)                                     |
| line                     | any individual line of text                                                      | everything except token, block, and block's child types                                    |
| math                     | a line of math                                                                   | (none)                                   |
| math block               | a block of math made of at least one line of math surrounded by math fences      | (none)                                    |
| math fence               | a delimiter that shows where a math block begins or ends                         | (none)                                    |
| ordered list item        | one line of a numbered list                                                      | (none) |
| table                    | a table, like this one; contains table rows and table parts                                                           | (none)                                    |
| table divider            | the second line of a table that divides the table's title row from its body rows | (none)                               |
| table part               | any line of text that is part of a table                                         | table divider, table row                                     |
| table row                | a row of a table, like this one                                                  | (none)                               |
| task                     | a line of a to do list                                                           | (none) |
| text                     | any line that does not fall into any of the other categories here                | (none)                 |
| text list                | a bullet-point list and/or an ordered list; can contain text list items and other text lists                                       | (none)                                    |
| text list item           | one line of a bullet-point list and/or ordered (numbered) list                   | task, ordered list item, unordered list item                                     |
| token                    | anything                                                                         | everything                                       |
| unordered list item      | one line of a bullet-point list                                                  | (none) |

## contributing

If Note Splitter sounds like it could be helpful to you, please [share your workflow](https://github.com/wheelercj/note-splitter/discussions/17) so we might be able to automate it! [Feature requests](https://github.com/wheelercj/note-splitter/issues), [discussions](https://github.com/wheelercj/note-splitter/discussions), pull requests, etc. are welcome!

[Developer documentation](https://note-splitter.readthedocs.io/)
