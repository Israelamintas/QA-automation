"""
Learn fixture scope="module": the fixture runs once for this test module/file.
"""
# tests/fixtures_examples/test_example_3_scope_module_part_1.py
import pytest


@pytest.fixture(scope="module")
def sample_user():
    print("\nMODULE-SCOPE FIXTURE PART 1: creating sample user")
    user = {
        "id": 1,
        "name": "Admas",
        "role": "student",
    }
    yield user
    print("\nMODULE-SCOPE FIXTURE PART 1: cleaning up sample user")


def test_scope_module_user_has_name(sample_user):
    print("PART 1 - TEST 1: checking the user's name")
    assert sample_user["name"] == "Admas"


def test_scope_module_user_has_role(sample_user):
    print("PART 1 - TEST 2: checking the user's role")
    assert sample_user["role"] == "student"


def test_scope_module_user_has_id(sample_user):
    print("PART 1 - TEST 3: checking the user's id")
    assert sample_user["id"] == 1
