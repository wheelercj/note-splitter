"""This script overwrites token-hierarchy.rst with the token hierarchy.

The current token hierarchy is determined automatically from the code.
More indentation means that the token is a child of the previous token 
with less indentation.
"""

# external imports
import inspect
from typing import List, Tuple

# internal imports
import tokens


def main():
    token_hierarchy: str = create_token_hierarchy()
    token_hierarchy_path = 'docs/token-hierarchy.rst'
    try:
        with open(token_hierarchy_path, 'w') as file:
            file.write(token_hierarchy)
    except FileNotFoundError:
        with open('../' + token_hierarchy_path, 'w') as file:
            file.write(token_hierarchy)
    print('token hierarchy saved to docs/token-hierarchy.rst')


def create_token_hierarchy() -> str:
    token_hierarchy = [
        'token hierarchy',
        '===============',
        '\nBelow is the hierarchy of all the tokens this program uses. More indentation means that the token is a child of the previous token with less indentation.\n',
    ]

    members: List[tuple] = inspect.getmembers(tokens)
    class_tuples: List[Tuple[str, object]] = [c for c in members if inspect.isclass(c[1])]
    classes = [c[1] for c in class_tuples]
    class_tree = inspect.getclasstree(classes)
    create_token_subhierarchy(token_hierarchy, class_tree)
    token_hierarchy.append('')

    return '\n'.join(token_hierarchy)


def create_token_subhierarchy(token_hierarchy: List[str], class_tree: list, indentation: str = '') -> List[str]:
    for c in class_tree:
        if isinstance(c, list):
            create_token_subhierarchy(token_hierarchy, c, indentation + '    ')
        else:
            class_name = c[0].__name__
            if class_name not in ('object', 'ABC'):
                abstract = ' (abstract)' if inspect.isabstract(c[0]) else ''
                token_hierarchy.append(indentation[8:] + '* :py:class:`tokens.' + class_name + '`' + abstract)

    return token_hierarchy


if __name__ == '__main__':
    main()
