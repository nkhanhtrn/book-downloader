from parser import escape
import pytest

def test_escape_slashes_success():
    assert escape('hello\world') == 'hello-world'
    assert escape('hello/world') == 'hello-world'
    assert escape('hello\/world') == 'hello--world'
