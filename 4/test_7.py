import pytest


def test_exception():
    with pytest.raises(ZeroDivisionError):
        1/0
