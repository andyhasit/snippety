from snippety import *

class TestDiretcive:
    def start_identifier(self):
        return SnippetyConfig().directive_start_identifier

    def inline_identifier(self):
        return SnippetyConfig().directive_inline_identifier

    def test_basic(self):
        line = 'my line of code%s [x, y] bacon eggs spam' %  self.inline_identifier()
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

