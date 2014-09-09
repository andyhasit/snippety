
from exceptions import *

class DirectiveParser:
    """Responsible for parsing a line containing a directive"""

    def __init__(self, startline, options):
        self.options = options
        self.output_start_identifier = options.output_start_identifier
        self.output_end_identifier = options.output_end_identifier
        self.directive_start_identifier = options.directive_start_identifier
        self.directive_end_identifier = options.directive_end_identifier
        self.directive_inline_identifier = options.directive_inline_identifier


        self.leading_whitespace = self._get_leading_whitespace(startline)
        self._markers = []
        self._sequence = []
        self.is_inline= False
        self.first_line_without_directive = ''
        self._parse_instruction_line(startline)

    def _parse_instruction_line(self, line):
        """
        Change to process inlines
        line.find(self.directive_inline_identifier)
        """
        assert line.find(self.directive_start_identifier) or \
                 line.find(self.directive_inline_identifier)

        if line.strip().startswith(self.directive_inline_identifier):
            #Fix: catch upstream to show line number
            raise DirectiveFormatException('Inline comment identifier must be preceded by some text.')

        if line.strip().startswith(self.directive_start_identifier):
            instruction_text = line.strip()[len(self.directive_identifier):].strip()
        else:
            line.find(self.directive_inline_identifier)
        self._parse_instructions(instruction_text)

    def _get_leading_whitespace(self, line):
        first_non_white_space = len(line) - len(line.lstrip())
        return line[:first_non_white_space]

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
                    self.options.get_marker_function(item, marker_sequence)
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
