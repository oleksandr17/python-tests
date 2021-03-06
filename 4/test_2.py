import pytest


@pytest.yield_fixture()
def fixture_optional(request):
    print("fixture_optional_in")
    yield 42
    print("fixture_optional_out")

@pytest.fixture(autouse=True)
def fixture_mandatory(request):
    print("fixture_mandatory_in")
    def resource_teardown():
        print("fixture_mandatory_out")
    request.addfinalizer(resource_teardown)


def test_1(fixture_optional):
    print("test_1")
    assert fixture_optional == 42, 'Sence of life must be 42'
 
def test_2():
    print("test_2")
