from snippety import *


class TestDirectiveParser:

    def start_identifier(self):
        return SnippetyConfig().directive_start_identifier

    def inline_identifier(self):
        return SnippetyConfig().directive_inline_identifier

class TestDirectiveParser_BasicTests(TestDirectiveParser):

    def test_leading_whitespace_spaces(self):
        whsp = '   '
        line = '%s%s [x, y] bacon eggs spam' %  (whsp, self.start_identifier())
        parser = DirectiveParser(line, SnippetyConfig())
        assert whsp == parser.leading_whitespace

    def test_leading_whitespace_tabs(self):
        whsp = '\t  \t'
        line = '%s%s [x, y] bacon eggs spam' %  (whsp, self.start_identifier())
        parser = DirectiveParser(line, SnippetyConfig())
        assert whsp == parser.leading_whitespace

    def test_correct_number_of_markers_are_extracted_one(self):
        line = '%s [x] bacon eggs spam' %  self.start_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert len(parser.markers) == 1

    def test_correct_number_of_markers_are_extracted_two(self):
        line = '%s [x, y] bacon eggs spam' %  self.start_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert len(parser.markers) == 2


class TestDirectiveParser_SimpleSequence(TestDirectiveParser):

    def test_correct_number_of_elements_are_extracted_one(self):
        line = '%s [x] bacon' %  self.start_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert len(parser.sequence) == 1

    def test_correct_number_of_elements_are_extracted_two(self):
        line = '%s [x] bacon eggs' %  self.start_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert len(parser.sequence) == 2




        a = '''
                self.leading_whitespace = parser.leading_whitespace
                self._markers = parser.markers
                self._sequence = parser.sequence
                if parser.is_inline:
                    self._items.append(parser.first_line_without_directive)
        '''