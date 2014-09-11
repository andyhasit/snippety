from snippety import *
from snippety.test_suite import TestBase

import os
from tempfile import mkdtemp

class TestSourceFileProcessor(TestBase):

    def test_basic(self):

        #
        #tmp_dir = "C:\\Users\\Andrew\\AppData\\Local\\Temp\\tmpbzyeqs"
        tmp_dir = mkdtemp()
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

        lines_out = self.read_from_file(tmpfile)
        assert initial_lines == lines_out
