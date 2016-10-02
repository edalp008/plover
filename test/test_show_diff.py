
from collections import namedtuple


class DictionaryItem(namedtuple('DictionaryItem', 'strokes translation dictionary')):
    @property
    def dictionary_path(self):
        return self.dictionary.get_path()

def compare_dictionaries(old, new):
    removed = []
    modified = []
    added = []

    for strokes, translation, dict in old:
        found = False
        for strokesNew, translationNew, dictNew in new:
            if(strokes == strokesNew):
                found = True
                if (translation != translationNew):
                    modified.append((DictionaryItem(strokes, translation, dict), DictionaryItem(strokesNew,translationNew,dictNew)))
        if (found==False):
            removed.append(DictionaryItem (strokes, translation, dict))

    for strokes,translation, dict in new:
        found = False
        for strokesOld, translationOld, dictOld in old:
            if (strokes == strokesOld):
                found = True

        if (found == False):
            added.append(DictionaryItem(strokes, translation, dict))

    return removed, modified, added


# Working to show sample result...
def sample_result(old, new):
    removed = [old[1], old[2]] # Dog, mongoose
    modified = [(old[0], new[0])] # Tuple (pair), cat -> CAT
    added = [new[1], new[3]] # New includes mongoose and duck
    return removed, modified, added

# Main method
if __name__ == '__main__':
    # Test dictionary 1
    dict1 = (
        DictionaryItem(('KAT',), 'cat', 'dict1'),
        DictionaryItem(('TKOG',), 'dog', 'dict1'),
        DictionaryItem(('PHOPB', 'TKPWAOS'), 'mongoose', 'dict1'),
        DictionaryItem(('PWAT',), 'bat', 'dict1'),
    )

    # Test dictionary 2
    dict2 = (
        DictionaryItem(('KAT',), 'CAT', 'dict2'), # Changed translation
        # dog: removed
        DictionaryItem(('PHOPB', 'TKPWAOZ'), 'mongoose', 'dict2'), # Changed stroke -- count as removal/addition
        DictionaryItem(('PWAT',), 'bat', 'dict2'), # Same
        DictionaryItem(('TKUBG',), 'duck', 'dict2'), # New
    )

    # "Test runner" type function.
    def test_diff(tester):
        removed, modified, added = tester(dict1, dict2)
        assert removed == [
            (('TKOG',), 'dog', 'dict1'),
            (('PHOPB', 'TKPWAOS',), 'mongoose', 'dict1'),
        ]
        assert modified == [
            (
                (('KAT',), 'cat', 'dict1'),
                (('KAT',), 'CAT', 'dict2'),
            )
        ]
        assert added == [
            (('PHOPB', 'TKPWAOZ',), 'mongoose', 'dict2'),
            (('TKUBG',), 'duck', 'dict2'),
        ]

    # Run the "tests" with this function.
    test_diff(sample_result)
    test_diff(compare_dictionaries)