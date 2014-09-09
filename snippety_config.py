
from snippety import *

class SnippetyConfig:
    """An object for storing configuration options, and the collections.
    The SnippetyConfig object gets passed down to most of the objects used by
    Snippety.
    """

    def __init__(self):
        self.directive_start_identifier = '#sn_s'
        self.directive_end_identifier =  '#sn_e'
        self.directive_inline_identifier = '#sn_i'
        self.output_start_identifier = '#snippety_generated_code_starts_here'
        self.output_end_identifier = '#snippety_generated_code_ends_here'
        self.get_marker_function = self.default_get_marker_function
        self.collections = {}

    def default_get_marker_function(self, marker_text, marker_sequence):
        """Identifies the type of marker to return.
        Fix: add more error checking.
        """
        if marker_text.find('*') > 0:
            return IteratorMarker(marker_text, marker_sequence)
        elif marker_text.find('>') > 0:
            return KeyValueMarker(marker_text, marker_sequence)
        else:
            return StandardMarker(marker_text, marker_sequence)

    def add_collection(self, name, keys, rows):
        """Adds a collection with the given name, where each element is a hash
        with the specified keys, built from each item in rows (which must be
        iterable items with the same length as keys).
        Note, you can add lists of hashes to collections directly if you prefer.
        """
        self.collections[name] = self._make_hashes(keys, rows)

    def _make_hashes(self, keys, rows):
        """Returns a list of hashes.
        >>> make_hash(['name', 'age'], [('Cathryn', 20), ('Leslie', 39)])
        [{'name':'Cathryn', 'age':20}, {'name':'Leslie', 'age':39}]
        """
        hashes = []
        for row in rows:
            assert len(row) == len(keys)
            h = {}
            hashes.append(h)
            for i, field in enumerate(keys):
                h[field] = row[i]
        return hashes

