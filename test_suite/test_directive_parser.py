from snippety import *


class TestDirectiveParser:

    def start_identifier(self):
        return SnippetyOptions().directive_start_identifier

    def inline_identifier(self):
        return SnippetyOptions().directive_inline_identifier

    def test_correct_number_of_items_extracted(self):
        line = '   %s [x, y] bacon eggs spam' %  self.start_identifier()
        whsp = '   '
        parser = DirectiveParser(line, SnippetyOptions())
        assert len(parser.markers) == 2
        assert len(parser.sequence) == 3
        assert whsp == parser.leading_whitespace

    def test_leading_whitespace_spaces(self):
        whsp = '   '
        line = '%s%s [x, y] bacon eggs spam' %  (whsp, self.start_identifier())
        parser = DirectiveParser(line, SnippetyOptions())
        assert whsp == parser.leading_whitespace

    def test_leading_whitespace_tabs(self):
        whsp = '\t  \t'
        line = '%s%s [x, y] bacon eggs spam' %  (whsp, self.start_identifier())
        parser = DirectiveParser(line, SnippetyOptions())
        assert whsp == parser.leading_whitespace

        a = '''
                self.leading_whitespace = parser.leading_whitespace
                self._markers = parser.markers
                self._sequence = parser.sequence
                if parser.is_inline:
                    self._items.append(parser.first_line_without_directive)
        '''