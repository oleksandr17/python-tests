import pytest

from src.calculator import Calculator


def test_exception():
    assert Calculator.plus(1, 1) == 2
