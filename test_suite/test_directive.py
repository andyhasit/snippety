from snippety import *
from snippety.test_suite import TestBase

class TestDirective:
    def start_identifier(self):
        return SnippetyConfig().directive_start_identifier

    def inline_identifier(self):
        return SnippetyConfig().directive_inline_identifier

    def test_basic(self):
        config = SnippetyConfig()
        config.add_collection(
                'person_fields',
                ['title', 'type'],
                [
                    ['dob', 'date'],
                    ['age', 'int']
                ])
        line = '%s [name>title, string>type, cnt*3] /person_fields' %  self.start_identifier()
        directive = Directive(line, config)
        directive.add_item('self.name = get_string(cnt)')
        lines_out = []
        directive.add_to_output_lines(lines_out)
        expected_lines = [
                config.output_start_identifier,
                'self.dob = get_date(3)',
                'self.age = get_int(4)',
                config.output_end_identifier
                ]
        assert expected_lines == [i.rstrip('\n') for i in lines_out]

    def test_inline(self):
        config = SnippetyConfig()
        config.add_collection(
                'person_fields',
                ['title', 'type'],
                [
                    ['dob', 'date'],
                    ['age', 'int']
                ])
        line = 'self.name = get_string(cnt) %s [name>title, string>type, cnt*3] /person_fields' %  self.inline_identifier()
        directive = Directive(line, config)
        lines_out = []
        directive.add_to_output_lines(lines_out)
        expected_lines = [
                config.output_start_identifier,
                'self.dob = get_date(3)',
                'self.age = get_int(4)',
                config.output_end_identifier
                ]
        print self.inline_identifier()
        assert expected_lines == [i.rstrip('\n') for i in lines_out]
