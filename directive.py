
from directive_parser import DirectiveParser

class Directive:
    """Directives are instructions in the source file telling Snippety what to do.
    Directives can be nested within each other.
    """
    def __init__(self, startline, options):
        self.options = options
        self.output_start_identifier = options.output_start_identifier
        self.output_end_identifier = options.output_end_identifier

        self.outter_directive = None
        self._items = []

        parser = DirectiveParser(startline, options)
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

        self._add_lines_before(output_lines)
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

        self._add_lines_after(output_lines)

        output_lines.append(self.leading_whitespace +
                self.output_end_identifier + '\n')

    #Fix: determine what to do from options. Also comment what it does.
    def _add_lines_before(self, output_lines):
        if self.outter_directive is None:
            output_lines.append(self.leading_whitespace +
                    self.options.output_start_identifier +
                    '\n'
                    )

    def _add_lines_after(self, output_lines):
        if self.outter_directive is None:
            output_lines.append(self.leading_whitespace +
                    self.options.output_start_identifier +
                    '\n'
                    )

