"""This script detects and displays the hierarchy of all the tokens.

More indentation means that the token is a child of the previous token 
with less indentation.
"""

# external imports
import inspect
from typing import List, Tuple

# internal imports
import tokens


def print_children(class_tree: list, indentation: str = ''):
    for c in class_tree:
        if isinstance(c, list):
            print_children(c, indentation + '    ')
        else:
            abstract = '(abstract)' if inspect.isabstract(c[0]) else ''
            print(indentation + c[0].__name__ + ' ' + abstract)


if __name__ == '__main__':
    print('Token Hierarchy')
    print('===============')
    members: List[tuple] = inspect.getmembers(tokens)
    class_tuples: List[Tuple[str, object]] = [c for c in members if inspect.isclass(c[1])]
    classes = [c[1] for c in class_tuples]
    class_tree = inspect.getclasstree(classes)
    print_children(class_tree)
