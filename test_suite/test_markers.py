
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
        #look up syntax and make sure it raises InstructionFormatException
        #assert s2 == marker.transform_line(s1, 'hello')

