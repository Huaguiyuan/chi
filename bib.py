import sort
import bibtexparser as bp
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


class Bib:
    """ A class that deals with lists of dicts of bibtex entries"""

    def __init__(self, path=""):
        self.entries = []
        try:
            self.entries = bp.loads(open(path).read()).entries
        except IOError:
            if path == "art":
                pass
            else:
                print("That bib file does not exist.")

    @classmethod
    def from_list(cls, entries):
        rv = cls("art")
        rv.entries = entries
        return rv

    def __delitem__(self, key):
        try:
            self.entries.__delitem__(key)
        except IndexError:
            print("Index out of range.")

    def __getitem__(self, key):
        try:
            return self.entries.__getitem__(key)
        except IndexError:
            print("Index out of range.")

    def __setitem__(self, key, value):
        try:
            self.entries.__setattr__(key, value)
        except IndexError:
            print("Index out of range.")

    def __add__(self, other):
        new_entries = sort.merge(self.entries, other.entries)
        return Bib.from_list(new_entries)

    def __sub__(self, other):
        new_entries = sort.exclude(self.entries, other.entries)
        return Bib.from_list(new_entries)

    def write(self, path=""):

        path = self.path if not path else path
        bdb = BibDatabase()
        bdb.entries = self.entries
        bw = BibTexWriter()

        with open(path, 'w') as f:
            f.write(bw.write(bdb).encode('ascii', 'replace'))

    def show(self):
        print('\n=======================================================\n')
        for entry in self.entries:
            print('(%s) - ' % (entry['index'], entry['bibentry']['year'])
                  + entry['bibentry']['title'])
        print('\n=======================================================\n')
