
from snippety import *

class SnippetyConfig:
    """An object for storing configuration elements.

    """

    def __init__(self):
        self.directive_start_identifier = '#sn_s'
        self.directive_end_identifier =  '#sn_e'
        self.directive_inline_identifier = '#sn_i'
        self.output_start_identifier = '#snippety_generated_code_starts_here'
        self.output_end_identifier = '#snippety_generated_code_ends_here'
        self.get_marker_function = self.get_marker

    def get_marker(self, marker_text, marker_sequence):
        if marker_text.find('*') > 0:
            return IteratorMarker(marker_text, marker_sequence)
        else:
            return StandardMarker(marker_text, marker_sequence)
