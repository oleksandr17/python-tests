import sys

import pytest


@pytest.mark.xfail()
def test_failed():
    assert False
    
@pytest.mark.xfail(sys.platform != "win64", reason="requires windows 64bit")
def test_failed_for_not_win32_systems():
    assert False
    
@pytest.mark.skipif(sys.platform != "win64", reason="requires windows 64bit")
def test_skipped_for_not_win64_systems():
    assert False

@pytest.mark.custom_mark
def test_with_custom_mark():
    """
    Execute tests marked with 'custom_mark':
    `pytest test_6.py -m "custom_mark"`
    """
    print("test_with_custom_mark")
    assert True
