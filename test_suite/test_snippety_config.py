from snippety import *

def test_add_collection():
    config = SnippetyConfig()
    config.add_collection(
            'person_fields',
            ['title', 'type'],
            [
                ['dob', 'date'],
                ['age', 'int']
            ])
    assert config.collections.has_key('person_fields')
    items = config.collections['person_fields']
    assert items[0] == {'title':'dob', 'type':'date'}
    assert items[1] == {'title':'age', 'type':'int'}

class Test_default_get_marker_function:

    def test_get_StandardMarker(self):
        config = SnippetyConfig()
        marker = config.get_marker_function('xyz', 0)
        assert isinstance(marker, StandardMarker)

    def test_get_IteratorMarker(self):
        config = SnippetyConfig()
        marker = config.get_marker_function('xyz*3', 0)
        assert isinstance(marker, IteratorMarker)

    def test_get_KeyValueMarker(self):
        config = SnippetyConfig()
        marker = config.get_marker_function('name > name', 0)
        assert isinstance(marker, KeyValueMarker)

    def test_get_get_marker_function_override(self):
        config = SnippetyConfig()
        config.get_marker_function = lambda x, y : 'returning %s %s' % (x, y)
        marker = config.get_marker_function('hello', 4)
        assert marker == 'returning hello 4'