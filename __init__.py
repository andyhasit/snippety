#-------------------------------------------------------------------------------
# Name:        snippety
# Purpose:
#
# Author:      Andrew
#
# Created:     04/09/2014
# Copyright:   (c) Andrew 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
from fnmatch import fnmatch

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


class SourceFileProcessor:

    def __init__(self, snippety):
        self.snippety = snippety
        self._output_lines = []
        self._inside_directive = False
        self._inside_generated_section = False
        self._current_directive = None
        # fix: pass these things in?
        self.directive_identifier = '#snip'
        #Fix : use #sn_start #sn_end #sn_ln
        self.generated_code_start_identifier = '#snippety_generated_code_starts_here'
        self.generated_code_end_identifier = '#snippety_generated_code_ends_here'

    def process_file(self, filepath, outpath):
        """Processes a single file:
            Extracts

        For now assumes single line directives
        Refactor:
            allow functions to determine line ends etc..
        """
        for line in tuple(open(filepath, "r")):
            if self._current_directive:
                self._output_lines.append(line)
                #Fix: do something here to cater for single-line directives
                if self._line_is_directive_instruction(line):
                    self._start_directive(line)
                elif self._line_is_directive_end(line):
                    self._end_current_directive(line)
                    #If reached end of outtermost directive, apply directives
                    if not self._current_directive:
                        self._apply_directives()
                else:
                    self._current_directive.add_item(line)

            elif self._inside_generated_section:
                if self._line_is_generated_code_end(line):
                    self._inside_generated_section = False
            else:
                if self._line_is_generated_code_start(line):
                    self._inside_generated_section = True
                else:
                    self._output_lines.append(line)
                    if self._line_is_directive_instruction(line):
                        self._start_directive(line)
        #Fix, here call post-processing, and check if output cancelled.
        self._write_output(outpath)

    def _line_is_directive_instruction(self, line):
        #Fix: change to allow inline comments
        line = line.strip()
        return line.startswith(self.directive_identifier) and \
                not line == self.directive_identifier

    def _line_is_directive_end(self, line):
        line = line.strip()
        return line == self.directive_identifier

    def _line_is_generated_code_start(self, line):
        line = line.strip()
        return line == self.generated_code_start_identifier

    def _line_is_generated_code_end(self, line):
        line = line.strip()
        return line == self.generated_code_end_identifier

    def _start_directive(self, line):
        assert self._line_is_directive_instruction(line)
        new_directive = Directive(line)

        if self._current_directive:
            # Within a directive, so nest it
            self._current_directive.add_item(new_directive)
        else:
            # Not within directive, so set it as to outtermost
            self._outtermost_directive = new_directive
        self._current_directive = new_directive

    def _end_current_directive(self, line):
        assert self._line_is_directive_end(line)
        assert self._current_directive
        # outter_directive may be None, in which case we've reach the end
        self._current_directive = self._current_directive.outter_directive

    def _apply_directives(self):
        self._outtermost_directive.add_to_output_lines(self._output_lines)
        self._outtermost_directive = None

    def _write_output(self, outpath):
        file = open(outpath, 'w')
        file.writelines(self._output_lines)
        file.close()


class Directive:
    """A directive."""
    def __init__(self, startline):
        #need to parse instructions
        self.directive_identifier = '#snip'
        self.generated_code_start_identifier = '#snippety_generated_code_starts_here'
        self.generated_code_end_identifier = '#snippety_generated_code_ends_here'
        self.outter_directive = None
        self._items = []
        self._markers = []
        self._sequence = []
        self._markerSelector = MarkerSelector()
        #Fix, allow instruction lines to be added, maybe lazy parse
        self._parse_instruction_line(startline)

    def add_item(self, item):
        """Add a line or a directive"""
        if type(item) is Directive:
            item.outter_directive = self
        self._items.append(item)

    def add_to_output_lines(self, output_lines):
        """Goes recursively through nested directives"""
        output_lines.append(self.leading_whitespace +
                self.generated_code_start_identifier + '\n')

        for element in self._sequence:
            for item in self._items:
                if type(item) is Directive:
                    item.add_to_output_lines(output_lines)
                else:
                    # Item is a plain line of text
                    for marker in self._markers:
                        #Apply transformation for each marker
                        item = marker.transform_line(item, element)
                    output_lines.append(item)

        output_lines.append(self.leading_whitespace +
                self.generated_code_end_identifier + '\n')

    def _parse_instruction_line(self, line):
        first_non_white_space = len(line) - len(line.lstrip())
        self.leading_whitespace = line[:first_non_white_space]
        instruction_text = line.strip()[len(self.directive_identifier):].strip()
        self._parse_instructions(instruction_text)

    def _parse_instructions(self, instruction_text):
        """
        Fix: Create docstring tests or other?
        instruction_text = '[name, string] (height, float) (age, int)'
        """
        if instruction_text.startswith('$'):
            pass #execute as code
        elif instruction_text.startswith('['):
            closing_bracket_index = instruction_text.find(']')
            if closing_bracket_index < 1:
                raise InstructionFormatException(
                    'Instruction does not contain closing ] bracket: "%s"' % instruction_text)
            self._parse_markers(instruction_text[:closing_bracket_index + 1])
            self._parse_sequence(instruction_text[closing_bracket_index + 1:])
        else:
            raise InstructionFormatException(
                    'Instruction does not start with $ or [: "%s"' % instruction_text)

    def _parse_markers(self, text):
        """Parses the bit [in square brackets]
        """
        assert text.startswith('[')
        assert text.endswith(']')
        items = [x.strip() for x in text[1:-1].split(',')]
        marker_sequence = 0
        for item in items:
            self._markers.append(
                    self._markerSelector.get_marker(item, marker_sequence))

    def _parse_sequence(self, text):
        """Parses the text, which must be one of:
        - a set of words separated by spaces
        - a set of bracketed sets: (height, float) (age, int)
        - the name of a collection, optionally followed by contidional statements
        """
        #fix check if first word is a member of collections
        text = text.strip()
        if text.startswith('('):
            pass
        else:
            self._sequence = text.split(' ')

class MarkerSelector:
    """Selects the type of Marker to provide based in the string.
    Exists as a separate class for dependency injection.
    """

    def get_marker(self, marker_text, marker_sequence):
        if marker_text.find('*') > 0:
            return IteratorMarker(marker_text, marker_sequence)
        else:
            return StandardMarker(marker_text, marker_sequence)


class StandardMarker:
    """The basis marker.
    Returns the line with all instances of marker_text replace with element.
    Assumes element is atomic.
    """
    def __init__(self, marker_text, marker_sequence):
        self._marker_text = marker_text
        self._marker_sequence = marker_sequence

    def transform_line(self, line, element):
        #Fix: use different functions depending on marker_text
        # also take into account element could be a single item, or list, or dict.
        if isinstance(element, basestring) and self._marker_sequence == 0:
            return line.replace(self._marker_text, element)
        elif isinstance(element, tuple) or isinstance(element, list):
            return line.replace(self._marker_text, element[self._marker_sequence])
        else:
            raise InstructionFormatException('StandardMarker expects each element in the list to be strings or lists')

class IteratorMarker(StandardMarker):
    """Replaces marker text with integers in increments of 1
    Ignores the sequence, and doesn't refer to the element.
    """
    def __init__(self, marker_text, marker_sequence):
        self._marker_sequence = marker_sequence
        star = marker_text.find('*')
        self._marker_text = marker_text[0:star]
        self._count = int(marker_text[star + 1:])

    def transform_line(self, line, element):
        new_line = line.replace(self._marker_text, str(self._count))
        self._count += 1
        return new_line

#Fix: create subclasses for IteratorMarker, KeyValueMarker, CapitalisedMarker and rename the other to StandardMarker
class InstructionFormatException(Exception):
    pass

__all__ = ['Snippety']

ideas = """
Fix make script as well as module

Use a MarkerSelector class, which interprets each marker string and decides on the appropriate
class.

Pass the list of lines to the marker, so it can scour them and add as many lines as it want.

Use a flag system at the end | flag1 flag2

Have a post processing function, which gets to read all the lines, and optionally cancel the output.
Could use this to redirect to a different file, or modify the lines... Or collect all the import statements.

Don't pass snippety, but just it's configuration elements and options:
    collections
    place tags inline


Idea is that the config file only specifies the collections and options.


sn.add_collection('person_fields',
    ['name', 'type', 'dbtype'],
    ['age', 'int', 'varchar(50)'],
    ['height', '', 'varchar(50)'],
    )

Add a collection parser utility, for people who prefer keeping it in files.
can also add collections directly as hashes.

"""
