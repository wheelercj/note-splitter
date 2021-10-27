# token hierarchy

Below is the hierarchy of all the tokens this program uses. More indentation means that the token is a child of the previous token with less indentation.

```
Token (abstract)      
    Blockquote 
    BlockquoteBlock     
    CodeBlock 
    EmptyLine 
    Fence (abstract)    
        CodeFence         
        MathFence         
    Footnote 
    Header 
    HorizontalRule      
    MathBlock 
    Section 
    Table 
    TablePart (abstract)
        TableDivider      
        TableRow 
    Text
    TextList
    TextListItem (abstract)
        Done
        OrderedListItem
        ToDo
        UnorderedListItem
```
