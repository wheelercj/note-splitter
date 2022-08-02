# Note Splitter overview

Here is a broad overview for developers of how Note Splitter's core splitting algorithm works.

The main steps the program goes through are:  
1. tokenization
2. parsing
3. splitting
4. formatting

## tokenization
After the user has selected which plain text file to split and what to split by, Note Splitter looks at the file and assigns a category to each line. This process is called **lexical analysis**, or **tokenization**. Some of the categories any given line can have are: header, blockquote, footnote, empty line, table row, etc. Each line and its category is combined into a **token**, which is what this program calls a variable representing one small part of a file and data about that part. At this point in the program, each token only holds one line of the file, and all the tokens are in one list.

Some features of plain text files can only be correctly understood by looking at their context. That is why the next step is to double-check the token types, this time comparing adjacent tokens. For example, a code block in a markdown file might contain a Python comment that, only without context, looks like a markdown header.

```python
print('this is code inside a code block, and . . .')
# this is a Python comment, not a markdown header.  
```

Here's an example that shows the result of tokenization with each token's type on the left, and its plain text on the right:

```
            Header | # sample markdown
              Text | #first-tag #second-tag
 UnorderedListItem | * bullet point 1
 UnorderedListItem | * bullet point 2
         EmptyLine |
              Text | here is text
   OrderedListItem | 1. ordered
   OrderedListItem | 2. list
         EmptyLine |
            Header | ## second header
              Text | #third-tag
         CodeFence | ```python
              Code | print('this code is inside a code block')
              Code | while True:
              Code |     print(eval(input('>>> ')))
         CodeFence | ```
         EmptyLine |
```

You can find all token types this program uses on the [tokens page](note_splitter.tokens.rst), see their [hierarchy](token-hierarchy.md), and see how this program tokenizes text in the [Lexer class](https://github.com/wheelercj/note-splitter/blob/main/note_splitter/lexer.py).

## parsing
Next, an optional step is to group together some tokens into larger tokens. For example, table row tokens that are next to each other are put together into one table token, and two code fence tokens surrounding code tokens become a code block token. This process is called **syntax analysis**, or **parsing**. The inner tokens are still tokens, but the overall token list is shorter and more organized now. (The reason why this step is optional is because sometimes the extra layer of organization is not needed and only makes operations more difficult.)

Continuing from the previous example, here is the result of parsing:

```
            Header | # sample markdown
              Text | #first-tag #second-tag
          TextList | * bullet point 1
                   | * bullet point 2
         EmptyLine | 
              Text | here is text
          TextList | 1. ordered
                   | 2. list
         EmptyLine | 
            Header | ## second header
              Text | #third-tag
         CodeBlock | ```python
                   | print('this code is inside a code block')
                   | while True:
                   |     print(eval(input('>>> ')))
                   | ```
         EmptyLine |
```

Now we have a syntax tree. This data structure can simplify many operations such as splitting a file, merging multiple files, moving parts of a file around, etc.

Parsing occurs in the constructor of the AST (abstract syntax tree) class, which is in [parser_.py](https://github.com/wheelercj/note-splitter/blob/main/note_splitter/parser_.py).

## splitting
Note Splitter takes the syntax tree and the user's choice of what to split by, and splits the syntax tree into sections. (Each section's tokens are put together into a Section token). These section tokens are each a smaller syntax tree that is still easy to modify.

Continuing from the previous example, here's the result of splitting where the user chose to split by headers of all levels:

```
           Section | # sample markdown
                   | #first-tag #second-tag
                   | * bullet point 1
                   | * bullet point 2
                   |
                   | here is text
                   | 1. ordered
                   | 2. list
                   |
           Section | ## second header
                   | #third-tag
                   | ```python
                   | print('this code is inside a code block')
                   | while True:
                   |     print(eval(input('>>> ')))
                   | ```
                   |
```

Once again, all the previous tokens still exist and can be accessed, they have simply been grouped together inside other tokens. You can see the code for splitting in [splitter.py](https://github.com/wheelercj/note-splitter/blob/main/note_splitter/splitter.py).

## formatting
The last big step is formatting and saving:
1. adjust some details in each such as making header levels lower if the lowest header level is not 1
2. copy certain elements of the source file into each of the new sections such as tags or footnotes (if the user chose that in settings)
3. convert the section tokens back to strings
4. save those strings into new files

The code for formatting can be found in [formatter_.py](https://github.com/wheelercj/note-splitter/blob/main/note_splitter/formatter_.py).

## further reading
Syntax trees are most often used to process code, but even though the resources below talk mostly about code, the ideas still apply to working with a plain text syntax tree.
* An excellent introduction to abstract syntax trees (ASTs) is given in [_ASTs - What are they and how to use them_](https://www.twilio.com/blog/abstract-syntax-trees).
* Wikipedia explains [lexical analysis and related topics](https://en.wikipedia.org/wiki/Lexical_analysis) in great depth.
* An advanced and detailed resource covering all of the steps above and more can be found in [Crafting Interpreters](https://craftinginterpreters.com/scanning.html).
