# token hierarchy

Below is the hierarchy of all the tokens this program uses. More indentation means that the token is a child of the previous token with less indentation.

```
Token (abstract)
    Block (abstract)
        BlockquoteBlock
        CodeBlock
        MathBlock
        Section
        Table
        TextList
    Blockquote
    Code
    EmptyLine
    Fence (abstract)
        CodeFence
        MathFence
    Footnote
    Header
    HorizontalRule
    Math
    TablePart (abstract)
        TableDivider
        TableRow
    Text
    TextListItem (abstract)
        Done
        OrderedListItem
        ToDo
        UnorderedListItem
```
