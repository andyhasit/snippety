"""
Markers are the items in [square brackets] inside a directive.

    #sn_start [food, x*1] eggs spam spam bacon
    Piggie x has food
    #sn_end

When processing a directive, a MarkerSelector object is used to determine which marker to use.
"""

class StandardMarker:
    """The basis marker.
    Returns the line with all instances of marker_text replace with element.
    Assumes element is atomic.
    """
    def __init__(self, marker_text, marker_sequence):
        self._marker_text = marker_text
        self._marker_sequence = marker_sequence

    def transform_line(self, line, element):
        """Returns the line with transformations applied."""
        if isinstance(element, basestring) and self._marker_sequence == 0:
            return line.replace(self._marker_text, element)
        elif isinstance(element, tuple) or isinstance(element, list):
            return line.replace(self._marker_text, element[self._marker_sequence])
        else:
            raise DirectiveFormatError('StandardMarker expects each element in the list to be strings or lists')

class IteratorMarker(StandardMarker):
    """
    Replaces marker text with integers in increments of 1.
    Expects a string as "cnt*1"
    Ignores the sequence, and doesn't refer to the element.
    """
    def __init__(self, marker_text, marker_sequence):
        self._marker_sequence = marker_sequence
        star = marker_text.find('*')
        self._marker_text = marker_text[0:star]
        self._count = int(marker_text[star + 1:])

    def transform_line(self, line, element):
        new_line = line.replace(self._marker_text, str(self._count))
        self._count += 1
        return new_line



