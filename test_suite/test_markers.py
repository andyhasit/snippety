
from snippety import *

class TestStandardMarker:

    def test_basic_case(self):
        marker = StandardMarker('x', 0)
        s1 = '  piggie says x '
        s2 = '  piggie says hello '
        assert s2 == marker.transform_line(s1, 'hello')

    def test_iterable_element(self):
        marker = StandardMarker('x', 2)
        s1 = '  piggie says x '
        s2 = '  piggie says hello '
        assert s2 == marker.transform_line(s1, ('no', 'no no', 'hello'))

    def __test_raises_exception_if_not_iterable(self):
        marker = StandardMarker('x', 2)
        s1 = '  piggie says x '
        #look up syntax and make sure it raises DirectiveFormatError
        #assert s2 == marker.transform_line(s1, 'hello')

class TestIteratorMarker:

    def test_basic_case(self):
        marker = IteratorMarker('x*3', 0)
        in1 = '  piggie says x '
        out1 = '  piggie says 3 '
        in2 = '  piggie says x '
        out2 = '  piggie says 4 '
        assert out1 == marker.transform_line(in1, 'hello')
        assert out2 == marker.transform_line(in2, 'hello')


class TestKeyValueMarker:

    def test_basic_case(self):
        element = {'title':'age', 'type':'int'}
        marker = KeyValueMarker('string > type', 0)
        line = 'self.name as string'
        out = 'self.name as int'
        assert out == marker.transform_line(line, element)

    def test_two_keys(self):
        element = {'title':'age', 'type':'int'}
        marker = KeyValueMarker('string > type', 0)
        line = 'self.name as string'
        out = 'self.name as int'
        assert out == marker.transform_line(line, element)
