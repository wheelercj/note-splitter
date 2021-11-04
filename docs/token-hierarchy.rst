token hierarchy
===============

Below is the hierarchy of all the tokens this program uses. More indentation means that the token is a child of the previous token with less indentation. Notice that the non-abstract types that inherit TextListItem also inherit CanHaveTags, so they are listed twice.

* :py:class:`tokens.Token` (abstract)
    * :py:class:`tokens.Block` (abstract)
        * :py:class:`tokens.BlockquoteBlock`
        * :py:class:`tokens.CodeBlock`
        * :py:class:`tokens.MathBlock`
        * :py:class:`tokens.Section`
        * :py:class:`tokens.Table`
        * :py:class:`tokens.TextList`
    * :py:class:`tokens.CanHaveTags` (abstract)
        * :py:class:`tokens.Blockquote`
        * :py:class:`tokens.Footnote`
        * :py:class:`tokens.Header`
        * :py:class:`tokens.LetteredListItem`
        * :py:class:`tokens.NumberedListItem`
        * :py:class:`tokens.Text`
        * :py:class:`tokens.ToDo`
        * :py:class:`tokens.UnorderedListItem`
    * :py:class:`tokens.Code`
    * :py:class:`tokens.EmptyLine`
    * :py:class:`tokens.Fence` (abstract)
        * :py:class:`tokens.CodeFence`
        * :py:class:`tokens.MathFence`
    * :py:class:`tokens.HorizontalRule`
    * :py:class:`tokens.Math`
    * :py:class:`tokens.TablePart` (abstract)
        * :py:class:`tokens.TableDivider`
        * :py:class:`tokens.TableRow`
    * :py:class:`tokens.TextListItem` (abstract)
        * :py:class:`tokens.OrderedListItem` (abstract)
            * :py:class:`tokens.LetteredListItem`
            * :py:class:`tokens.NumberedListItem`
        * :py:class:`tokens.ToDo`
        * :py:class:`tokens.UnorderedListItem`
