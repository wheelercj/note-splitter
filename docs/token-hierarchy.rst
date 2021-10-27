token hierarchy
===============

Below is the hierarchy of all the tokens this program uses. More indentation means that the token is a child of the previous token with less indentation.

* :py:class:`tokens.Token` (abstract)
    * :py:class:`tokens.Block` (abstract)
        * :py:class:`tokens.BlockquoteBlock`
        * :py:class:`tokens.CodeBlock`
        * :py:class:`tokens.MathBlock`
        * :py:class:`tokens.Section`
        * :py:class:`tokens.Table`
        * :py:class:`tokens.TextList`
    * :py:class:`tokens.Blockquote`
    * :py:class:`tokens.Code`
    * :py:class:`tokens.EmptyLine`
    * :py:class:`tokens.Fence` (abstract)
        * :py:class:`tokens.CodeFence`
        * :py:class:`tokens.MathFence`
    * :py:class:`tokens.Footnote`
    * :py:class:`tokens.Header`
    * :py:class:`tokens.HorizontalRule`
    * :py:class:`tokens.Math`
    * :py:class:`tokens.TablePart` (abstract)
        * :py:class:`tokens.TableDivider`
        * :py:class:`tokens.TableRow`
    * :py:class:`tokens.Text`
    * :py:class:`tokens.TextListItem` (abstract)
        * :py:class:`tokens.Done`
        * :py:class:`tokens.OrderedListItem`
        * :py:class:`tokens.ToDo`
        * :py:class:`tokens.UnorderedListItem`
