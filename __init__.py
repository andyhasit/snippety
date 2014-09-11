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

Idea is that the config file only specifies the models and config.


http://pytest.org/latest/getting-started.html

To Do:

    Find out if I can do def __init__(self, config=SnippetyConfig()):
    Save buffer prompt (In config, set type of prompt: shell or GUI)
    Create CapitalisedMarker * 2 using ~


    Beef up test suite
    Check nested directives work
    Make it easy to direct to output files
        get_output_path lambda
    File backup

    Feature: Output control. Users will want to:
        a) Write back to source file
        b) Write just output to another file.
        c) Write everything to another file.
        d) Write output to another file, and add stuff like class definitions...
    Feature: modify lines

    Allow executing as code is marker text starts with $
    Conditionals
    Flags
    User manual
    Pip
    As module:
        generate an example script to use
        --tests: runs all tests
        --help
        --version

Not done because it's tricky:
    multi-line directive
    allowing output blocks to have inline comment

Ideas:
    Use a flag system at the end | flag1 flag2

    Have a post processing function, which gets to read all the lines, and optionally cancel the output.
    Could use this to redirect to a different file, or modify the lines... Or collect all the import statements.


    sn.add_collection('person_fields',
        ['name', 'type', 'dbtype'],
        ['age', 'int', 'varchar(50)'],
        ['height', '', 'varchar(50)'],
        )

    Add a collection parser utility, for people who prefer keeping it in files?
    can also add collections directly as hashes.

"""
import os

# Order matters! http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
from errors import DirectiveFormatError, FileParsingError
from markers import StandardMarker, IteratorMarker, KeyValueMarker
from snippety_config import SnippetyConfig
from directive_parser import DirectiveParser
from directive import Directive
from source_file_processor import SourceFileProcessor


class Snippety:
    """
    The entry point to using Snippety. Provides access methods to process files.
    """

    def __init__(self, config=None):
        if config:
            self.config = config
        else:
            self.config = SnippetyConfig()

    def process_dir(self, dirpath, include_list=None, ignore_list=None, config=None):
        """Process all files found in dirpath, applying filters from include and
        ignore, which must be lists like ['.py'] or ['.bak', '*/bin'] similar
        to git and hg ignore patterns.
        Ignore matching taking precedence.
        """

        from fnmatch import fnmatch
        # fix:  Why do I have "continue" ? (Copied form internet)
        files_in = []
        for root, dirs, files in os.walk(dirpath):
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
        if config is None:
            config = self.config
        for file in files_in:
            self.process_file(file, config=config)

    def process_file(self, filepath, config=None):
        if config is None:
            config = self.config
        SourceFileProcessor(config).process_file(filepath)

__all__ = [
        'Snippety',
        'SnippetyConfig',
        'SourceFileProcessor',
        'Directive',
        'DirectiveParser',
        'StandardMarker',
        'IteratorMarker',
        'KeyValueMarker',
        'DirectiveFormatError',
        'FileParsingError',
        ]

if __name__ == "__main__":
    import pytest
    pytest.main()

