# -*- coding: utf-8 -*-
"""
Snippety repeats chunks of text

 text below your text directives in your source code.

So wrapping our "Piggie..." line with the start and end directives gives

#sn_start [food, x*1] eggs spam spam bacon
        Piggie x has food
#sn_end

Gives:

        Piggie 1 has eggs
        Piggie 2 has spam
        Piggie 3 has spam
        Piggie 4 has bacon


Ideas:
    Use a flag system at the end | flag1 flag2

    Have a post processing function, which gets to read all the lines, and optionally cancel the output.
    Could use this to redirect to a different file, or modify the lines... Or collect all the import statements.

    Don't pass snippety, but just it's configuration elements and options:
        collections
        place tags inline


    Idea is that the config file only specifies the models and options.



    sn.add_collection('person_fields',
        ['name', 'type', 'dbtype'],
        ['age', 'int', 'varchar(50)'],
        ['height', '', 'varchar(50)'],
        )

Add a collection parser utility, for people who prefer keeping it in files?
can also add collections directly as hashes.

http://pytest.org/latest/getting-started.html

To Do:
    Create test suite for:
        Markers
        Directive
        MarkerSelector
    Method for cascading options:
        Options object:
            use_inline_markers_for_output
            marker_selector
            directive_start_identifier
            directive_end_identifier
            directive_inline_identifier
        Passes from Snippety>FileProcessor>marker
    Make it easy to direct to output files
        get_output_path lambda


    Maybe make MarkerSelector a function so it can be created annonymously?

    Inline directives
    Inline outputs
    Create KeyValueMarker, CapitalisedMarker
    What else does __init__ need to export?
    Complete _parse_sequence

    User manual
    Pip
    Init generates a template file to use.

    make_hash

"""

from markers import *
from marker_selector import MarkerSelector
from source_file_processor import SourceFileProcessor
from directive import Directive
import os


class Snippety:
    """
    Stores the config and collections.
    Provides access methods to process files.
    """

    def __init__(self):
        pass

    def process_dir(self, dirpath, include_list=None, ignore_list=None):
        """Process all files found in dirpath, applying filters from include and
        ignore, which must be lists like ['.py'] or ['.bak', '*/bin'] similar
        to git and hg ignore patterns.
        Ignore matching taking precedence.
        """
        from fnmatch import fnmatch
        # fix:  Why "continue" ?
        files_in = []
        for root, dirs, files in os.walk(self.source_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                if include_list:
                    if any(fnmatch(filename, pattern) for pattern in include_list):
                        files_in.append(filepath)
                        print "Including ", filepath
                        continue
                    else:
                        files_in.append(filepath)
                if ignore_list:
                    if any(fnmatch(filename, pattern) for pattern in ignore_list):
                        files_in.remove(filepath)
                        print "Ignoring ", filepath
                        continue
        for file in files_in:
            self.process_file(file)

    def process_file(self, filepath, outpath=None):
        # fix: refactor to use factory?
        # Also send configuration elements
        if not outpath:
            outpath = filepath
        SourceFileProcessor(self).process_file(filepath, outpath)


def make_hashes(fields, rows):
    """Returns a list of hashes.
    >>> make_hash(['name', 'age'], [('Cathryn', 20), ('Leslie', 39)])
    [{'name':'Cathryn', 'age':20}, {'name':'Leslie', 'age':39}]
    """
    hashes = []
    for row in rows:
        assert len(row) == len(fields)
        h = {}
        hashes.append(h)
        for i, field in enumerate(fields):
            h[field] = row[i]
    return hashes



class InstructionFormatException(Exception):
    pass

__all__ = ['Snippety', 'make_hashes']

if __name__ == "__main__":
    import pytest
    pytest.main()

