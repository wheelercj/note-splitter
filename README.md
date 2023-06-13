# Note Splitter

Split text files into multiple smaller files.

Automate tedious parts of many workflows, such as research notetaking that requires not just splitting a file, but also copying footnotes, resizing headers, etc.

![demo](docs/images/demo.png)

![demo gif](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdhZDczODEyZDA3MGJhOWM2ZmM1YzllODYxNGU5ZjlmYTUwNGI5ZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/SVRERckC3PE62pt73i/giphy.gif)

## download

You can [download Note Splitter here (Windows only)](https://github.com/wheelercj/note-splitter/releases) or [install Note Splitter from source (all platforms)](https://github.com/wheelercj/note-splitter/blob/main/docs/dev-env.md).

## major features

* Split by almost any markdown element.
* Backlinks and/or index files.
* Automatically update links when new files are moved.
* Optionally copy tags, frontmatter, footnotes, etc. into new files.
* Source files are **NOT** changed in any way except for automatic link updates.

## split types

Choose an element's name to choose what to split by. Some split types group together multiple other related split types ("child types"), so you can split by multiple types by choosing one with child types.

| type name                | description                                                                      | child types                             |
|--------------------------|----------------------------------------------------------------------------------|------------------------------------------|
| block                    | any text element that spans multiple lines and contains other tokens                                      | blockquote block, code block, math block, table, text list                                   |
| blockquote               | a quote                                                                          | (none)                 |
| blockquote block         | multiple consecutive quotes                                                      | (none)                                    |
| can have inline elements | any line of text that can contain inline elements (tags and markdown links to files)                                | blockquote, footnote, header, task, text, ordered list item, unordered list item                                     |
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

## split attributes and values

Choosing a split attribute and value is optional, and can be used to be more specific about what you want to split. For example, if you want to split by headers of all levels you should choose the `(none)` attribute, but if you want to split by headers of level 2 you should choose the `level` attribute and the value `2`.

Some split types have different attributes to choose from. For example, the `header` split type has `level` as one of its split attributes, which refers to the size of the header. However, some other split types such as `ordered list item` also have a `level` attribute that refers to the _indentation level_. Any split type's `content` attribute option lets you specify what exact text the element should contain. Some split types have other specialized attributes, such as `code block`'s `language` attribute, which allows you to choose the code block's language.

## parse blocks

The "parse blocks" checkbox is mainly for elements of text that span multiple lines (blocks), but the option also changes the behavior when splitting by single-line elements. When parse blocks is chosen, each split section also ends where its containing block ends instead of only where the next element of the split type is found.

## file name formats

All new file names are guaranteed to be unique. If the file name format does not allow for unique file names, a period followed by a unique number will be added to each new file name.

The file name format setting should not include a file extension and can use these variables:

* `%uuid4` - A universally unique identifier
* `%title` - The title of the file (the body of the first header, or of the first line if there is no header)
* `%Y` - The current year (4 digits)
* `%M` - The current month (2 digits)
* `%D` - The current day (2 digits)
* `%h` - The current hour (2 digits)
* `%m` - The current minute (2 digits)
* `%s` - The current second (2 digits)
* `%id` - The same as entering `%Y%M%D%h%m%s`

You can use other characters with these variables. For example, to get file names like `2021-12-16 09.30`, you can set the file name format to `%Y-%M-%D %h.%m`.

If multiple files are made when the file name format has at least one of `%s`, `%m`, `%h`, and `%D`, the smallest of these time variables will be incremented once for each new file so that all the files have unique names. The first file starts with the current time.

## contributing

If Note Splitter sounds like it could be helpful to you, please [share your workflow](https://github.com/wheelercj/note-splitter/discussions/17) so we might be able to automate it! [Feature requests](https://github.com/wheelercj/note-splitter/issues), [discussions](https://github.com/wheelercj/note-splitter/discussions), pull requests, etc. are welcome!

[Developer documentation](https://note-splitter.readthedocs.io/)
