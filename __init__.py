# -*- coding: utf-8 -*-
"""
Snippety is a tool for generating source code from directives in your source code.

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

To Do:
    Inline directives and outputs
    Functionality to have inline comments
    Create KeyValueMarker, CapitalisedMarker
    Create tests (see http://pytest.org/latest/getting-started.html)
    What else does it need to export?
    _parse_sequence

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

class InstructionFormatException(Exception):
    pass

__all__ = ['Snippety']

if __name__ == "__main__":
    import pytest
    pytest.main()

