from snippety import *


class TestDirectiveParser:

    def start_identifier(self):
        return SnippetyConfig().directive_start_identifier

    def inline_identifier(self):
        return SnippetyConfig().directive_inline_identifier


class TestStartEndDirectiveBasic(TestDirectiveParser):

    def test_leading_whitespace_spaces(self):
        whsp = '   '
        line = '%s%s [x, y] bacon eggs spam' %  (whsp, self.start_identifier())
        parser = DirectiveParser(line, SnippetyConfig())
        assert whsp == parser.leading_whitespace
        assert parser.is_inline == False

    def test_leading_whitespace_tabs(self):
        whsp = '\t  \t'
        line = '%s%s [x, y] bacon eggs spam' %  (whsp, self.start_identifier())
        parser = DirectiveParser(line, SnippetyConfig())
        assert whsp == parser.leading_whitespace

    def test_marker_text_extracted_correctly(self):
        line = 'my line of code%s [x, y] bacon eggs spam' %  self.start_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert parser._markers_text == '[x, y]'
        assert parser.is_inline == False

    def test_sequence_text_extracted_correctly(self):
        line = 'my line of code%s [x, y] bacon eggs spam' %  self.start_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert parser._sequence_text == 'bacon eggs spam'


class TestInlineDirectiveBasic(TestDirectiveParser):

    def test_leading_whitespace_spaces(self):
        whsp = '   '
        line = '%smy line of code %s [x, y] bacon eggs spam' %  (whsp, self.inline_identifier())
        parser = DirectiveParser(line, SnippetyConfig())
        assert whsp == parser.leading_whitespace

    def test_leading_whitespace_tabs(self):
        whsp = '\t  \t'
        line = '%smy line of code%s [x, y] bacon eggs spam' %  (whsp, self.inline_identifier())
        parser = DirectiveParser(line, SnippetyConfig())
        assert whsp == parser.leading_whitespace

    def test_marker_text_extracted_correctly(self):
        line = 'my line of code%s [x, y] bacon eggs spam' %  self.inline_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert parser._markers_text == '[x, y]'

    def test_sequence_text_extracted_correctly(self):
        line = 'my line of code%s [x, y] bacon eggs spam' %  self.inline_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert parser._sequence_text == 'bacon eggs spam'

    def test_sequence_first_line_extracted_correctly(self):
        line = '   my line of code%s [x, y] bacon eggs spam' %  self.inline_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert parser.is_inline == True
        assert '   my line of code' == parser.first_line_without_directive


class TestDirectiveParser_SimpleSequence(TestDirectiveParser):
    """Tests simple sequence: [x, y] bacon eggs spam """

    def test_correct_number_of_elements_are_extracted_one(self):
        line = '%s [x] bacon' %  self.start_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert len(parser.sequence) == 1
        assert parser.sequence[0] == 'bacon'

    def test_correct_number_of_elements_are_extracted_two(self):
        line = '%s [x] bacon eggs' %  self.start_identifier()
        parser = DirectiveParser(line, SnippetyConfig())
        assert len(parser.sequence) == 2
        assert parser.sequence[0] == 'bacon'
        assert parser.sequence[1] == 'eggs'

class TestDirectiveParser_Collection(TestDirectiveParser):
    """Tests simple sequence: [x, y] bacon eggs spam """

    def test_collection_is_found(self):
        config = SnippetyConfig()
        config.add_collection(
                'person_fields',
                ['title', 'type'],
                [
                    ['dob', 'date'],
                    ['age', 'int']
                ])
        line = '%s [x] /person_fields' %  self.start_identifier()
        parser = DirectiveParser(line, config)
        assert len(parser.sequence) == 2
        assert parser.sequence[0] == {'title':'dob', 'type':'date'}
        assert parser.sequence[1] ==  {'title':'age', 'type':'int'}

        #Fix add test to raise exception if not found

