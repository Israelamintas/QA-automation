"""
Learn fixture scope="function": this is the default scope, so the fixture runs once per test.
"""

import pytest


@pytest.fixture(scope="function")
def sample_user():
    print("\nFUNCTION-SCOPE FIXTURE: creating sample user")
    user = {
        "id": 1,
        "name": "Admas",
        "role": "student",
    }
    yield user
    print("\nFUNCTION-SCOPE FIXTURE: cleaning up sample user")


def test_user_has_name(sample_user):
    print("TEST 1: checking the user's name")
    assert sample_user["name"] == "Admas"


def test_user_has_role(sample_user):
    print("TEST 2: checking the user's role")
    assert sample_user["role"] == "student"


def test_user_has_id(sample_user):
    print("TEST 3: checking the user's id")
    assert sample_user["id"] == 1
