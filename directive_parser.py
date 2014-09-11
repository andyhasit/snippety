
from snippety import *

class DirectiveParser:
    """Responsible for parsing a line containing a directive, inline or standard.

    [marker1, marker2 ...] sequence | flags...

    sequence can be:
        words separated by spaces
        (sets, of) (tuple, of) (same, length) (as, markers)
        name_of_a_collection
        name_of_a_collection if some_field = some_value
        name_of_a_collection if some_field != some_value
    """

    def __init__(self, startline, config):
        self.config = config
        self._line = startline
        self.output_start_identifier = config.output_start_identifier
        self.output_end_identifier = config.output_end_identifier
        self.directive_start_identifier = config.directive_start_identifier
        self.directive_end_identifier = config.directive_end_identifier
        self.directive_inline_identifier = config.directive_inline_identifier
        #Defaults and placeholders
        self.leading_whitespace = ''
        self.markers = []
        self.sequence = []
        self.is_inline = False
        self.first_line_without_directive = ''
        self._instruction_text = ''
        self._markers_text = ''
        self._sequence_text = ''
        self._flags_text = '' # will be
        #Start parsing
        self._get_leading_whitespace()
        self._extract_instructions()
        self._parse_instructions()
        self._parse_markers()
        self._parse_sequence()

    def _get_leading_whitespace(self):
        line = self._line
        first_non_white_space = len(line) - len(line.lstrip())
        self.leading_whitespace = line[:first_non_white_space]

    def _extract_instructions(self):
        """Extracts the instruction_text and determines if it is inline or not.
        """
        # Fix: this code could easily break if inline_identifier is a
        # substring of start_identifier or vice-versa... And so could the
        # FileProcessor in the first place...
        # Chose where error should be caught... catch upstream to show line number?
        line = self._line
        start_identifier_position = line.find(self.directive_start_identifier)
        inline_identifier_position = line.find(self.directive_inline_identifier)

        if start_identifier_position >= 0:
            assert inline_identifier_position == -1
            self.is_inline = False
            cut_point = len(self.directive_start_identifier) + start_identifier_position

        elif inline_identifier_position >= 0:
            assert start_identifier_position == -1
            self.is_inline = True
            self.first_line_without_directive = line[:inline_identifier_position].rstrip()
            cut_point = len(self.directive_inline_identifier) + inline_identifier_position
        else:
            raise DirectiveFormatError('The directive did not contain identifier (%s or %s): %s' % \
                (self.directive_start_identifier, self.directive_inline_identifier, line))
        print
        self._instruction_text = line[cut_point:].strip()

    def _parse_instructions(self):
        """
        Test with:
        instruction_text = '[name, string] (height, float) (age, int)'
        """
        text = self._instruction_text
        if text.startswith('$'):
            pass #Fix: allow executing as code
        elif text.startswith('['):
            closing_bracket_index = text.find(']')
            if closing_bracket_index < 1:
                raise DirectiveFormatError(
                    'Instruction does not contain closing ] bracket: "%s"' % text
                    )
            self._markers_text = text[:closing_bracket_index + 1].strip()
            self._sequence_text = text[closing_bracket_index + 1:].strip()
        else:
            raise DirectiveFormatError(
                    'Instruction does not start with $ or [: "%s"' % text
                    )

    def _parse_markers(self):
        """Parses the markers [in square brackets]"""
        text = self._markers_text
        assert text.startswith('[')
        assert text.endswith(']')
        items = [x.strip() for x in text[1:-1].split(',')]
        for marker_sequence, item in enumerate(items):
            self.markers.append(
                    self.config.get_marker_function(item, marker_sequence)
                    )

    def _parse_sequence(self):
        """Parses the sequence text, which must be one of:
                words separated by spaces
                (sets, of) (tuple, of) (same, length) (as, markers)
                name_of_a_collection
                name_of_a_collection if some_field = some_value
                name_of_a_collection if some_field != some_value
        """
        #fix check if first word is a member of collections
        text = self._sequence_text
        if text.startswith('('):
            raise Exception('not implemented yet')
        elif text.startswith('/'):
            words = text.split(' ')
            collection_name = words[0][1:]
            try:
                collection = self.config.collections[collection_name]
                if len(words) == 1:
                    self.sequence = collection
                elif len(words) == 4:
                    raise Exception('not implemented yet')
                else:
                    raise DirectiveFormatError('Sequence must be composed of 1 or 4 words)')
            except KeyError:
                raise DirectiveFormatError('Collection "%s" not found in config.' \
                         % collection_name)
        else:
            self.sequence = text.split(' ')