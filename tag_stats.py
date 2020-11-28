
'''
Gathers and displays statistics about the tags throughout the zettelkasten, including:
* A graph of the tags and their adjacency.
* Average tags per zettel.
* Total unique tags.
* Total tags.
'''

# Internal
from common import zettelkasten_path, get_zettel_names

# External
import re
from igraph import *


class Tags:
    frequency = dict()
    adjacency = dict()


def tag_stats():
    os.chdir(zettelkasten_path)
    zettel_names = get_zettel_names(os.listdir())
    tags, tagless_zettels = get_tags(zettel_names)
    total_tags = sum(tags.frequency.values())
    draw_graph(tags)

    print('Total unique tags:', len(tags.frequency))
    print('Total tags:', total_tags)
    print('Total zettels:', len(zettel_names))
    print('Average tags per zettel', total_tags / len(zettel_names))
    print('Tag adjacency:', tags.adjacency)
    print_untagged(tagless_zettels)


# Return the frequency and adjacency of all tags.
def get_tags(zettel_names):
    tags = Tags()
    tagless_zettels = []

    for zettel_name in zettel_names:
        with open(zettel_name, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
            p = re.compile(r'(?<=\s)#[a-zA-Z0-9_-]+')
            new_tags = p.findall(contents)

            if new_tags == 0:
                tagless_zettels.append(zettel_name)
                continue

            # Update the tag count
            for tag in new_tags:
                if tag not in tags.frequency:
                    tags.frequency[tag] = 0
                tags.frequency[tag] += 1

            # Update the adjacency
            for i in new_tags[:-1]:
                for j in new_tags[i + 1:]:
                    tags.adjacency[i][j] += 1
                    tags.adjacency[j][i] += 1

    return tags, tagless_zettels


def draw_graph(tags):
    g = Graph.Weighted_Adjacency(tags.adjacency)
    print(g)


# Print a list of the names of all zettels that don't have any tags.
def print_untagged(tagless_zettels):
    if tagless_zettels > 0:
        print('\nUntagged zettel(s) found:')
        for zettel_name in tagless_zettels:
            print(zettel_name)


if __name__ == '__main__':
    tag_stats()
