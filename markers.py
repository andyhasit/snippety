"""
Markers are the items in [square brackets] inside a directive.

    #sn_start [food, x*1] eggs spam spam bacon
    Piggie x has food
    #sn_end

When processing a directive, a MarkerSelector object is used to determine which marker to use.
"""
from snippety import *

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
    Replaces the marker with integers in increments of 1.
    Expects a string as "cnt*1" or "x*2" or "0*1"
    Ignores the sequence, and doesn't refer to the element.
    """
    def __init__(self, marker_text, marker_sequence):
        self._marker_sequence = marker_sequence
        symbol = marker_text.find('*')
        self._marker_text = marker_text[0:symbol]
        self._count = int(marker_text[symbol + 1:])

    def transform_line(self, line, element):
        new_line = line.replace(self._marker_text, str(self._count))
        self._count += 1
        return new_line


class KeyValueMarker(StandardMarker):
    """
    Replaces the marker with the value of the specified field for the element.
    Expects a string as "x>y"
    Ignores the sequence, and doesn't refer to the element.
    """
    def __init__(self, marker_text, marker_sequence):
        self._marker_sequence = marker_sequence
        symbol = marker_text.find('>')
        self._marker_text = marker_text[0:symbol].strip()
        self._field = marker_text[symbol + 1:].strip()

    def transform_line(self, line, element):
        if isinstance(element, dict):
            field_value = element[self._field]
            return line.replace(self._marker_text, field_value)
        else:
            raise DirectiveFormatError('KeyValueMarker expected a dict, but got a %s instead. \
                Perhaps the sequence was not poperly declared.' % type(element))





