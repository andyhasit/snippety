

class DirectiveFormatError(Exception):
    pass

class FileParsingError(Exception):

    def __init__(self, e, file, line_number):
        message = ''.join([
            'Error parsing file "%s"\n' % file,
            'Line: %s\n' % line_number,
            '%s' % e])
        Exception.__init__(self, message)
