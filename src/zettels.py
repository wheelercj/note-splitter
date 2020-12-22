class Zettels():
    def __init__(self):
        # These lists are parallel, except not all are always used.
        self.paths = []   # The absolute file paths.
        self.names = []   # The file names.
        self.ids = []     # The 14-digit zettel IDs.
        self.titles = []  # The first header level 1 in each file, not including the hash and leading space.
        self.links = []   # The ID and title combined, with double square brackets around the ID.

    def append(self, path='', name='', ID='', title='', link=''):
        if len(path):
            self.paths.append(path)
        if len(name):
            self.names.append(name)
        if len(ID):
            self.ids.append(ID)
        if len(title):
            self.titles.append(title)
        if len(link):
            self.links.append(link)

    def path_of_link(self, link):
        i = self.links.index(link)
        return self.paths[i]

    def remove_path(self, path):
        i = self.paths.index(path)
        del self.paths[i]
        if len(self.names):
            del self.names[i]
        if len(self.ids):
            del self.ids[i]
        if len(self.titles):
            del self.titles[i]
        if len(self.links):
            del self.links[i]

    def repath(self, old_path, new_path):
        for i, path in enumerate(self.paths):
            if path == old_path:
                self.paths[i] = new_path
