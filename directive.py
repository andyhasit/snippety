

class Directive:
    """Directives are instructions in the source file telling Snippety what to do.
    Directives can be nested within each other.
    """
    def __init__(self, startline, options):
        self.options = options
        self.output_start_identifier = options.output_start_identifier
        self.output_end_identifier = options.output_end_identifier
        self.directive_start_identifier = options.directive_start_identifier
        self.directive_end_identifier = options.directive_end_identifier
        self.directive_inline_identifier = options.directive_inline_identifier
        #Fix: pass a function to this...
        self._markerSelector = MarkerSelector()

        self.outter_directive = None
        self._items = []
        self.leading_whitespace = ''
        self._markers = []
        self._sequence = []
        #Fix, allow instruction lines to be added, maybe lazy parse
        self._parse_instruction_line(startline)

    def add_item(self, item):
        """Add a line or a directive"""
        if type(item) is Directive:
            item.outter_directive = self
        self._items.append(item)

    def add_to_output_lines(self, output_lines):
        """Goes recursively through nested directives"""
        output_lines.append(self.leading_whitespace +
                self.output_start_identifier + '\n')

        for element in self._sequence:
            for item in self._items:
                if type(item) is Directive:
                    item.add_to_output_lines(output_lines)
                else:
                    # Item is a plain line of text
                    for marker in self._markers:
                        #Apply transformation to line for each marker
                        item = marker.transform_line(item, element)
                    output_lines.append(item)

        output_lines.append(self.leading_whitespace +
                self.output_end_identifier + '\n')

    def _parse_instruction_line(self, line):
        """
        Change to process inlines
        line.find(self.directive_inline_identifier)
        """
        first_non_white_space = len(line) - len(line.lstrip())
        self.leading_whitespace = line[:first_non_white_space]
        instruction_text = line.strip()[len(self.directive_identifier):].strip()
        self._parse_instructions(instruction_text)

    def _parse_instructions(self, instruction_text):
        """
        Test with:
        instruction_text = '[name, string] (height, float) (age, int)'
        """
        if instruction_text.startswith('$'):
            pass #Fix: allow executing as code
        elif instruction_text.startswith('['):
            closing_bracket_index = instruction_text.find(']')
            if closing_bracket_index < 1:
                raise InstructionFormatException(
                    'Instruction does not contain closing ] bracket: "%s"' % instruction_text
                    )
            self._parse_markers(instruction_text[:closing_bracket_index + 1])
            self._parse_sequence(instruction_text[closing_bracket_index + 1:])
        else:
            raise InstructionFormatException(
                    'Instruction does not start with $ or [: "%s"' % instruction_text
                    )

    def _parse_markers(self, text):
        """Parses the bit [in square brackets]
        """
        assert text.startswith('[')
        assert text.endswith(']')
        items = [x.strip() for x in text[1:-1].split(',')]
        marker_sequence = 0
        for item in items:
            self._markers.append(
                    self._markerSelector.get_marker(item, marker_sequence)
                    )

    def _parse_sequence(self, text):
        """Parses the text, which must be one of:
        - a set of words separated by spaces
        - a set of bracketed sets: (height, float) (age, int)
        - the name of a collection, optionally followed by contidional statements
        """
        #fix check if first word is a member of collections
        text = text.strip()
        if text.startswith('('):
            pass
        else:
            self._sequence = text.split(' ')

