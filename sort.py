import re


def complete(terms):
    comp_terms = re.findall(r'"([^"]*)"', terms)
    other = terms
    for term in comp_terms:
        other = other.replace('"%s"' % (term), '')
    comp_terms += other.split()

    return [word.lower() for word in comp_terms]


def deconstruct(string):
    """ Creates a search hierarchy """
    return [[complete(t) for t in term] for term in
            [term.split('&') for term in string.split('|')]]


def merge(list1, list2):
    """Takes two lists of bibtex dictionaries and
    merges list1 with list2 without redundances."""

    rv = list1
    IDs = [item['ID'] for item in list1]
    titles = [item['title'] for item in list1]

    for idx, src in enumerate(list2):

        try:
            flag_ID = src['ID'] in IDs
        except KeyError:
            flag_ID = False

        try:
            flag_title = src['title'] in titles
        except KeyError:
            flag_title = False

        if not flag_ID and not flag_title:

            try:
                IDs.append(src['ID'])
            except KeyError:
                pass

            try:
                titles.append(src['title'])
            except KeyError:
                pass

            rv.append(list2[idx])

    return rv


def exclude(list1, list2):
    """Takes two lists of bibtex dictionaries and
    removes entries from list1 that are in list2."""

    ID = [item['ID'] for item in list2]
    titles = [item['title'] for item in list2]
    return [item for item in list1 if item['ID'] not
            in ID and item['title'] not in titles]

def printSearch(s_list):

    print('\n=======================================================\n')
    for entry in s_list:
        print('%d - (%s) - ' % (entry['index'], entry['bibentry']['year'])
              + entry['bibentry']['title'])
    print('\n=======================================================\n')


def indexify(entries):

    return [{'index': index, 'bibentry': entry}
            for index, entry in enumerate(entries)]
