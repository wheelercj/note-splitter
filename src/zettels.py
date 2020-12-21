class Zettels():
    def __init__(self):
        self.paths = []   # The file path.
        self.names = []   # The file name.
        self.ids = []     # The 14-digit zettel ID.
        self.titles = []  # The first header level 1 in the file.
        self.links = []   # The ID and title combined, with double square brackets around the ID.

    def append(self, path, name, ID, title, link):
        self.paths.append(path)
        self.names.append(name)
        self.ids.append(ID)
        self.titles.append(title)
        self.links.append(link)
