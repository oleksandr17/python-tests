import pytest


@pytest.fixture()
def create_dog():
    dog = {'nickname': 'tuzik'}
    return dog

@pytest.fixture()
def create_human(create_dog):
    human = {'name': 'borat', 'dog': create_dog}
    return human


def test_dog(create_dog):
    assert create_dog['nickname']

def test_human(create_human):
    assert create_human['name']
    assert create_human['dog']
