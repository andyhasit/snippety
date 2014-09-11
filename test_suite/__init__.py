"""
The test suite is designed to run with pytest

These are the files, classes and functions that are looked at:

    test_*.py or *_test.py files, imported by their `package name`_.
    Test prefixed test classes (without an __init__ method)
    test_ prefixed test functions or methods are test items

http://pytest.org/latest/goodpractises.html

"""
from snippety import *

class TestBase:
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


__all__ = ['TestBase']

if __name__ == "__main__":
    import pytest
    pytest.main()
