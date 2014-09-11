from snippety import *
import os
from tempfile import mkdtemp

class TestSourceFileProcessor:

    def write_to_file(self, file, lines):
        f = open(file, 'w')
        f.write('\n'.join(self.strip_new_line_chars(lines)))
        f.close()

    def strip_new_line_chars(self, lines):
        return [line.strip('\n') for line in lines]

    def read_from_file(self, file):
        f = open(file, 'r')
        lines = self.strip_new_line_chars(f.readlines())
        f.close()
        return lines

    def print_lines(self, lines):
        for l in lines:
            print l

    def test_basic(self):

        #tmp_dir = mkdtemp()
        tmp_dir = "C:\\Users\\Andrew\\AppData\\Local\\Temp\\tmpbzyeqs"
        tmpfile = os.path.join(tmp_dir, 'myfile.txt')

        config = SnippetyConfig()
        initial_lines = [
            'Some text here',
            '%s [x, y*0] bacon eggs spam' %  config.directive_start_identifier,
            '    Person y likes x',
            config.directive_end_identifier,
            'nothing should happen here'
            ]

        self.write_to_file(tmpfile, initial_lines)
        lines_out = self.read_from_file(tmpfile)
        assert initial_lines == lines_out

        self.write_to_file(tmpfile, initial_lines)

        sfp = SourceFileProcessor(config)
        sfp.process_file(tmpfile)


        initial_lines.insert(4, config.output_start_identifier)
        initial_lines.insert(5, '    Person 0 likes bacon')
        initial_lines.insert(6, '    Person 1 likes eggs')
        initial_lines.insert(7, '    Person 2 likes spam')
        initial_lines.insert(8, config.output_end_identifier)

        #print '\nin:\n'
        #self.print_lines(initial_lines)
        #print '\nout:\n'
        self.print_lines(lines_out)
        #print '//////////////'

        lines_out = self.read_from_file(tmpfile)
        assert initial_lines == lines_out


if __name__ == "__main__":
    import pytest
    pytest.main()