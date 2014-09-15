from snippety import *
from snippety.test_suite import TestBase

import os
import shutil
from tempfile import mkdtemp

class TestSourceFileProcessor(TestBase):

    def test_basic(self):
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

        sfp = SourceFileProcessor(config)
        sfp.process_file(tmpfile)

        initial_lines.insert(4, config.output_start_identifier)
        initial_lines.insert(5, '    Person 0 likes bacon')
        initial_lines.insert(6, '    Person 1 likes eggs')
        initial_lines.insert(7, '    Person 2 likes spam')
        initial_lines.insert(8, config.output_end_identifier)

        lines_out = self.read_from_file(tmpfile)
        self.print_lines(initial_lines)
        self.print_lines(lines_out)

        assert initial_lines == lines_out

        shutil.rmtree(tmp_dir)

    def test_inline(self):
        tmp_dir = mkdtemp()
        tmpfile = os.path.join(tmp_dir, 'myfile.txt')

        config = SnippetyConfig()
        initial_lines = [
            'Some text here',
            '    Person y likes x %s [x, y*0] bacon eggs spam' %  config.directive_inline_identifier,
            'nothing should happen here'
            ]

        self.write_to_file(tmpfile, initial_lines)
        lines_out = self.read_from_file(tmpfile)
        assert initial_lines == lines_out

        sfp = SourceFileProcessor(config)
        sfp.process_file(tmpfile)

        initial_lines.insert(2, '    %s' % config.output_start_identifier)
        initial_lines.insert(3, '    Person 0 likes bacon')
        initial_lines.insert(4, '    Person 1 likes eggs')
        initial_lines.insert(5, '    Person 2 likes spam')
        initial_lines.insert(6, '    %s' % config.output_end_identifier)

        lines_out = self.read_from_file(tmpfile)

        assert initial_lines == lines_out

        shutil.rmtree(tmp_dir)

    def test_few_entries(self):
        tmp_dir = mkdtemp()
        tmpfile = os.path.join(tmp_dir, 'myfile.txt')

        config = SnippetyConfig()
        config.add_collection(
            'person_fields',
            ['title', 'type'],
            [
                ['dob', 'date'],
                ['age', 'int']
            ])
        initial_lines = [
            'Some text here',
            '%s [name>title, type>type] /person_fields' %  config.directive_start_identifier,
            '    Person has name (which is a type)',
            config.directive_end_identifier,
            'nothing should happen here'
            ]

        self.write_to_file(tmpfile, initial_lines)
        lines_out = self.read_from_file(tmpfile)
        assert initial_lines == lines_out

        sfp = SourceFileProcessor(config)
        sfp.process_file(tmpfile)

        initial_lines.insert(4, config.output_start_identifier)
        initial_lines.insert(5, '    Person has dob (which is a date)')
        initial_lines.insert(6, '    Person has age (which is a int)')
        initial_lines.insert(7, config.output_end_identifier)

        lines_out = self.read_from_file(tmpfile)
        self.print_lines(initial_lines)
        self.print_lines(lines_out)

        assert initial_lines == lines_out

        shutil.rmtree(tmp_dir)

    def test_backup(self):
        """

        """
        pass

if __name__ == "__main__":
    import pytest
    pytest.main()