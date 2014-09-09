
from snippety import *

class Directive:
    """Directives are instructions in the source file telling Snippety what to do.
    Directives can be nested within each other.
    Output lines will be enclosed in output markers, unless in a nested directive.
    """
    def __init__(self, startline, config):
        self.config = config
        self.output_start_identifier = config.output_start_identifier
        self.output_end_identifier = config.output_end_identifier

        self.outter_directive = None
        self._items = []

        parser = DirectiveParser(startline, config)
        self.leading_whitespace = parser.leading_whitespace
        self._markers = parser.markers
        self._sequence = parser.sequence
        if parser.is_inline:
            self._items.append(parser.first_line_without_directive)


    def add_item(self, item):
        """Add a line or a directive"""
        if type(item) is Directive:
            item.outter_directive = self
        self._items.append(item)

    def add_to_output_lines(self, output_lines):
        """Goes recursively through nested directives"""
        self._start_generated_block(output_lines)
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
        self._end_generated_block(output_lines)

    def _start_generated_block(self, output_lines):
        """Adds a line with the generated_output_start_identifer at the same
        level of indentation as the directive.
        Only does it for the outtermost directive. May change this?
        """
        if self.outter_directive is None:
            output_lines.append(self.leading_whitespace +
                    self.config.output_start_identifier +
                    '\n'
                    )

    def _end_generated_block(self, output_lines):
        """Adds a line with the generated_output_end_identifer at the same
        level of indentation as the directive.
        Only does it for the outtermost directive. May change this?
        """
        if self.outter_directive is None:
            output_lines.append(self.leading_whitespace +
                    self.config.output_end_identifier +
                    '\n'
                    )

