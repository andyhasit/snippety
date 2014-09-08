
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
