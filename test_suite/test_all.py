
from snippety import *

def test_answer():
    assert 3 == 5

def test_make_hashes_works():
    result = [{'name':'Cathryn', 'age':20}, {'name':'Leslie', 'age':39}]
    assert result == make_hashes(['name', 'age'],
            [('Cathryn', 20), ('Leslie', 39)]
            )
